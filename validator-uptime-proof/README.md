# 📊 Story Validator Uptime Proof

This repository provides a **reproducible and on-chain verifiable method** to calculate **validator uptime on Story Mainnet**, based on **block commit signatures**, using an **archive RPC**.

It is designed to be used as **uptime proof** for delegation programs and validator evaluations.

---

## 🧠 What this measures (important)

This tool measures **validator consensus uptime**, defined as:

> The ability of a validator to actively participate in consensus by **signing block commits** when required.

It does **not** measure:
- server uptime
- process uptime
- RPC availability

Instead, it verifies **on-chain participation**, which is the metric that matters for Story validators.

---

## 📌 Methodology (high level)

1. Convert a **start date** (e.g. delegation start) into a **block height** using block timestamps.
2. Iterate over block heights from that point until the latest block.
3. For each block, inspect:
   ```
   block.last_commit.signatures[].validator_address
   ```
4. Check whether the validator **consensus address (valcons)** appears in the commit.
5. Count:
   - blocks where the validator **signed**
   - blocks where the validator **did not sign** (`commits_missing`)
6. Compute uptime percentage.

This method is:
- ✅ fully on-chain
- ✅ reproducible
- ✅ independent of local node state

---

## 🔧 Requirements

- Bash
- `curl`
- `jq`
- `screen` (optional, recommended for long runs)
- Access to a **Story archive RPC** (non-pruned)

Example archive RPC:
```
https://rpc-archive.story.node75.org
```

---

## ⚙️ Setup

### 1) Install dependencies (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y curl jq screen
```

### 2) Add the script

Create the file `story-uptime-since-date.sh` and paste the script contents (see the script section below), then:

```bash
chmod +x story-uptime-since-date.sh
```

### 3) Configure your validator identity

You must set the validator **consensus address (valcons) in HEX**, which is the exact format used inside block commits.

Example (Cumulo):
```
B93DD4D30F2837187D6BF66C6D53799F2E1A1272
```

> Tip: You can obtain it from your validator host with `story tendermint show-address`, then reuse it anywhere.

---

## 🆔 Validator identity

The validator is identified by its **consensus address in HEX** (valcons), for example:

```
B93DD4D30F2837187D6BF66C6D53799F2E1A1272
```

This is the exact format used in block commit signatures.

---

## ▶️ Script: Uptime since a given date

### `story-uptime-since-date.sh`

This script calculates validator uptime from a **given UTC date** until the present, using an **archive RPC**.

### Configuration variables (inside the script)

- `RPC` (archive RPC base URL)
- `START_ISO` (UTC date to start from)
- `CONS_HEX` (validator consensus address in HEX)
- `MONIKER` (used for output file naming)
- `STEP` (sampling step)

### Usage

```bash
./story-uptime-since-date.sh 10
```

Where:
- `10` = sampling step (see below)

---

## 🔍 Sampling step explained

The script checks **one block every N blocks**.

| STEP | Meaning | Precision | Runtime |
|------|--------|-----------|---------|
| 1    | Every block | Exact | Very slow |
| 10   | 1 of every 10 blocks | Very high | Moderate |
| 50   | 1 of every 50 blocks | High (defendable) | Fast |

> Sampling is statistically reliable for long ranges and widely accepted in technical audits.

---

## 🧾 Running it with `screen` (recommended)

When calculating long ranges (weeks/months), run the script inside a persistent terminal session so it keeps working after you disconnect.

### 1) Create a `screen` session

```bash
screen -S story-uptime
```

### 2) (Optional) Enable screen logging

Inside `screen`, press:
- `Ctrl + A`, then `H`

This will create `screenlog.0` in your current directory.

You can watch it from another terminal:
```bash
tail -f screenlog.0
```

### 3) Run the script

```bash
./story-uptime-since-date.sh 10
```

### 4) Detach and leave it running

Press:
- `Ctrl + A`, then `D`

### 5) Reattach later

```bash
screen -r story-uptime
```

### 6) List sessions (if you forget the name)

```bash
screen -ls
```

---

## 📄 Output (Uptime Proof)

The script generates a JSON file like:

```json
{
  "moniker": "Cumulo",
  "chain": "Story Mainnet",
  "start_time_utc": "2025-11-24T00:00:00Z",
  "start_height": 1234567,
  "end_height": 2345678,
  "sampling_step_blocks": 10,
  "blocks_checked": 105432,
  "commits_signed": 105420,
  "commits_missing": 12,
  "estimated_uptime_percent": 99.9886
}
```

### Field meanings

- **blocks_checked**  
  Number of blocks evaluated (based on sampling).

- **commits_signed**  
  Sampled blocks where the validator **signed the commit**.

- **commits_missing**  
  Sampled blocks where the validator **did not sign** (effective unavailability at consensus level).

- **estimated_uptime_percent**  
  Consensus uptime over the evaluated range (based on sampling).

---

## ⚠️ Interpretation notes

- A missing signature means the validator was **not participating in consensus** for that block.
- This can be due to downtime, desync, restart, or being outside the active set.
- From the network perspective, all cases are treated as **validator unavailability**.

---

## ✅ Why this is valid for delegation programs

- Uses **canonical on-chain data**
- Does not rely on explorer abstractions
- Reproducible by any third party
- Measures **actual consensus participation**

This aligns with how Cosmos-based networks evaluate validator reliability.

---

## 🧩 Troubleshooting

### Pruned RPCs
If your RPC is pruned, it may fail to query historical blocks:
- Use an **archive RPC** instead.

### Rate limits / slow runs
If the RPC rate-limits you or the script is too slow:
- increase `STEP` (e.g., `50`)
- run it with `screen` to let it finish reliably

---

## 📎 Recommended submission format

When submitting as uptime proof:

1. Upload the generated JSON file  
2. (Optional) Add a screenshot showing the script execution and file generation  

---

## 🏁 Conclusion

This repository provides a **transparent, auditable, and technically sound** method to prove validator uptime on Story Mainnet, suitable for professional validator operations and delegation assessments.

---

## 📜 Script (reference)

> Paste this into `story-uptime-since-date.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

RPC="https://rpc-archive.story.node75.org"
START_ISO="2025-11-24T00:00:00Z"
STEP="${1:-50}"  # 50 recommended (fast). 10 more precise. 1 exact (very slow)

MONIKER="Cumulo"
CONS_HEX="B93DD4D30F2837187D6BF66C6D53799F2E1A1272"  # valcons hex

latest_height="$(curl -s "$RPC/status" | jq -r '.result.sync_info.latest_block_height')"

block_epoch () {
  local h="$1"
  local t
  t="$(curl -s "$RPC/block?height=$h" | jq -r '.result.block.header.time')"
  date -d "$t" +%s
}

start_epoch="$(date -d "$START_ISO" +%s)"

# binary search start height by timestamp
lo=1
hi="$latest_height"
while [ "$lo" -lt "$hi" ]; do
  mid=$(( (lo + hi) / 2 ))
  mid_epoch="$(block_epoch "$mid")"
  if [ "$mid_epoch" -lt "$start_epoch" ]; then
    lo=$(( mid + 1 ))
  else
    hi="$mid"
  fi
done
start_height="$lo"

checked=0
signed=0
missed=0

for ((h=start_height; h<=latest_height; h+=STEP)); do
  addrs="$(curl -s "$RPC/block?height=$h"     | jq -r '.result.block.last_commit.signatures[].validator_address // empty'     | tr '[:lower:]' '[:upper:]')"

  checked=$((checked+1))
  if echo "$addrs" | grep -q "$CONS_HEX"; then
    signed=$((signed+1))
  else
    missed=$((missed+1))
  fi
done

uptime="$(awk "BEGIN { if ($checked==0) print 0; else print (100*$signed/$checked) }")"

OUT="${MONIKER} - Story Mainnet Uptime Proof (since 2025-11-24, step${STEP}).json"
jq -n   --arg moniker "$MONIKER"   --arg rpc "$RPC"   --arg start_time "$START_ISO"   --arg cons_hex "$CONS_HEX"   --arg start_height "$start_height"   --arg end_height "$latest_height"   --arg step "$STEP"   --arg checked "$checked"   --arg signed "$signed"   --arg missed "$missed"   --arg uptime "$uptime" '{
  moniker: $moniker,
  chain: "Story Mainnet",
  rpc_used: $rpc,
  start_time_utc: $start_time,
  cons_address_hex: $cons_hex,
  start_height: ($start_height|tonumber),
  end_height: ($end_height|tonumber),
  sampling_step_blocks: ($step|tonumber),
  blocks_checked: ($checked|tonumber),
  commits_signed: ($signed|tonumber),
  commits_missing: ($missed|tonumber),
  estimated_uptime_percent: ($uptime|tonumber),
  note: "Estimated uptime calculated by sampling block commits in the height range and checking whether cons_address_hex appears in last_commit signatures. commits_missing counts sampled blocks where the signature was absent."
}' > "$OUT"

echo "Start height: $start_height"
echo "End height:   $latest_height"
echo "Checked:      $checked (step=$STEP)"
echo "Signed:       $signed"
echo "Missing:      $missed"
echo "Uptime %:     $uptime"
echo "Saved:        $OUT"
```
