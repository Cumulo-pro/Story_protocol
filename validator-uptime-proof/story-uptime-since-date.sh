#!/usr/bin/env bash
set -euo pipefail

RPC="https://rpc-archive.story.node75.org"
START_ISO="2025-11-24T00:00:00Z"
STEP="${1:-50}"  # 50 recomendado (rápido). 10 más preciso. 1 exacto (muy lento)

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

for ((h=start_height; h<=latest_height; h+=STEP)); do
  addrs="$(curl -s "$RPC/block?height=$h" \
    | jq -r '.result.block.last_commit.signatures[].validator_address // empty' \
    | tr '[:lower:]' '[:upper:]')"
  checked=$((checked+1))
  if echo "$addrs" | grep -q "$CONS_HEX"; then
    signed=$((signed+1))
  fi
done

uptime="$(awk "BEGIN { if ($checked==0) print 0; else print (100*$signed/$checked) }")"

OUT="${MONIKER} - Story Mainnet Uptime Proof (since 2025-11-24, step${STEP}).json"
jq -n \
  --arg moniker "$MONIKER" \
  --arg rpc "$RPC" \
  --arg start_time "$START_ISO" \
  --arg cons_hex "$CONS_HEX" \
  --arg start_height "$start_height" \
  --arg end_height "$latest_height" \
  --arg step "$STEP" \
  --arg checked "$checked" \
  --arg signed "$signed" \
  --arg uptime "$uptime" \
'{
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
  estimated_uptime_percent: ($uptime|tonumber),
  note: "Estimated uptime calculated by sampling block commits in the height range and checking whether cons_address_hex appears in last_commit signatures."
}' > "$OUT"

echo "Start height: $start_height"
echo "End height:   $latest_height"
echo "Saved:        $OUT"

