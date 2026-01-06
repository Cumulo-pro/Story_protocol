# Story Node Installation Guide

**Chain ID:** `story-1`  
**Story (consensus client):** `v1.4.2-stable`  
**Story-Geth (execution client):** `v1.2.0-stable`  
**Audience:** Operators running a **full node / RPC / validator** on Story Mainnet.

> This guide installs **two services**:
> - `story-geth` → Execution client (EVM)
> - `story` → Consensus + ABCI app
>
> They communicate via **Engine API** on `127.0.0.1:8551` and must share the same **JWT secret**.

---

## ✅ Recommended Hardware

- **CPU:** 8 cores+
- **RAM:** 32 GB+
- **Disk:** 400 GB+ **NVMe**
- **Network:** 100 Mbps+

---

## 🔌 Ports Reference

### Local / Internal (recommended)
| Service | Purpose | Bind | Port |
|---|---|---:|---:|
| story-geth | Engine API (AuthRPC) | 127.0.0.1 | 8551 |

### Public (only if you intentionally expose them)
| Service | Purpose | Bind | Port |
|---|---|---:|---:|
| story | Story REST API | 0.0.0.0 | 1307 |
| story-geth | EVM JSON-RPC HTTP | 0.0.0.0 | 8547 |

> **Security note:** If you expose `1307` or `8547` publicly, protect them with firewall and/or reverse proxy (Nginx), rate limits, and allowlists.

---

## 1) Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git wget htop tmux build-essential jq make lz4 gcc unzip openssl
```

---

## 2) Install Go (required to build `story`)

```bash
cd $HOME
VER="1.22.5"
wget "https://golang.org/dl/go${VER}.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go${VER}.linux-amd64.tar.gz"
rm "go${VER}.linux-amd64.tar.gz"

[ ! -f "$HOME/.bash_profile" ] && touch "$HOME/.bash_profile"
echo "export PATH=\$PATH:/usr/local/go/bin:\$HOME/go/bin" >> "$HOME/.bash_profile"
source "$HOME/.bash_profile"

mkdir -p "$HOME/go/bin"
```

Check:

```bash
go version
```

---

## 3) Install Story-Geth (Execution Client)

```bash
cd $HOME
wget -O story-geth https://github.com/piplabs/story-geth/releases/download/v1.2.0/geth-linux-amd64
chmod +x story-geth
mv story-geth "$HOME/go/bin/"
```

Verify:

```bash
story-geth -v
# story-geth version 1.2.0-stable-6e7aa284
```

---

## 4) Install Story (Consensus Client)

```bash
cd $HOME
rm -rf story
git clone https://github.com/piplabs/story
cd story
git checkout v1.4.2
go build -o story ./client
mv story "$HOME/go/bin/"
```

Verify:

```bash
story version
# Version v1.4.2-stable
```

---

## 5) Initialize the Node

Choose a moniker:

```bash
export MONIKER="CumuloRPC"
```

Initialize:

```bash
story init --network story --moniker "$MONIKER"
```

This creates the directory layout:

- `~/.story/story` (consensus/app)
- `~/.story/geth` (execution client data)

---

## 6) Download Genesis

Primary source (NodeStake):

```bash
curl -Ls https://ss.story.nodestake.org/genesis.json > "$HOME/.story/story/config/genesis.json"
```

Alternative source (Polkachu):

```bash
wget -O genesis.json https://snapshots.polkachu.com/genesis/story/genesis.json --inet4-only
mv genesis.json "$HOME/.story/story/config/genesis.json"
```

Quick sanity check (chain id):

```bash
jq -r '.chain_id' "$HOME/.story/story/config/genesis.json"
# expected: story-1
```

---

## 7) Download Addrbook

Primary source (NodeStake):

```bash
curl -Ls https://ss.story.nodestake.org/addrbook.json > "$HOME/.story/story/config/addrbook.json"
```

Alternative source (Polkachu):

```bash
wget -O addrbook.json https://snapshots.polkachu.com/addrbook/story/addrbook.json --inet4-only
mv addrbook.json "$HOME/.story/story/config/addrbook.json"
```

---

## 8) Create Engine API JWT (Required)

This is the most common setup pitfall.

Story (consensus) connects to story-geth (execution) via **Engine API**.  
They must share a JWT file (32 bytes hex / 64 chars).

```bash
mkdir -p "$HOME/.story/geth/story/geth"
openssl rand -hex 32 > "$HOME/.story/geth/story/geth/jwtsecret"
chmod 600 "$HOME/.story/geth/story/geth/jwtsecret"
```

Confirm it exists:

```bash
ls -lah "$HOME/.story/geth/story/geth/jwtsecret"
```

---

## 9) (Important) Fix `story.toml` Engine Settings

If your node was initialized under a different user previously, your `story.toml` may contain a **wrong absolute path** for `engine-jwt-file` or the wrong port for `engine-endpoint`.

Open:

```bash
nano "$HOME/.story/story/config/story.toml"
```

Make sure these lines exist and match:

```toml
engine-endpoint = "http://127.0.0.1:8551"
engine-jwt-file = "$HOME/.story/geth/story/geth/jwtsecret"
```

If you prefer editing via CLI (no nano), replace values like this:

```bash
sed -i.bak   -e 's|^engine-endpoint *=.*|engine-endpoint = "http://127.0.0.1:8551"|'   -e "s|^engine-jwt-file *=.*|engine-jwt-file = \"$HOME/.story/geth/story/geth/jwtsecret\"|"   "$HOME/.story/story/config/story.toml"
```

Verify:

```bash
grep -nE 'engine-endpoint|engine-jwt-file' "$HOME/.story/story/config/story.toml"
```

> Note: `story` can also receive these via flags. This guide sets them in the service, but keeping `story.toml` correct avoids surprises.

---

## 10) Create systemd service: `story-geth.service`

> Start **execution** first.

```bash
sudo tee /etc/systemd/system/story-geth.service > /dev/null <<EOF
[Unit]
Description=Story Geth Client
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME

ExecStart=$(which story-geth) \
  --story \
  --syncmode full \
  --authrpc.addr 127.0.0.1 \
  --authrpc.port 8551 \
  --authrpc.vhosts="*" \
  --authrpc.jwtsecret $HOME/.story/geth/story/geth/jwtsecret \
  --http \
  --http.addr 0.0.0.0 \
  --http.port 8547 \
  --http.api eth,net,web3,engine \
  --http.corsdomain "*" \
  --http.vhosts "*"

Restart=on-failure
RestartSec=3
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF
```

---

## 11) Create systemd service: `story.service`

> Then start **consensus/app**.

```bash
sudo tee /etc/systemd/system/story.service > /dev/null <<EOF
[Unit]
Description=Story Node
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/.story/story

ExecStart=$(which story) run \
  --network story \
  --api-enable \
  --api-address=0.0.0.0:1307 \
  --engine-endpoint=http://127.0.0.1:8551 \
  --engine-jwt-file=$HOME/.story/geth/story/geth/jwtsecret

Restart=on-failure
RestartSec=5s
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF
```

---

## 12) Enable & Start Services (correct order)

```bash
sudo systemctl daemon-reload
sudo systemctl enable story-geth story

sudo systemctl start story-geth
sleep 5
sudo systemctl start story
```

---

## 13) Logs & Common “First Start” Messages

Follow both logs:

```bash
journalctl -u story-geth -f
```

```bash
journalctl -u story -f
```

You may see:

- `Upgrading IAVL storage...`  
  This is normal on first start and can take time depending on disk speed.

If you see:

- `load engine JWT file ... no such file or directory`  
  Then your `engine-jwt-file` path is wrong or permissions are incorrect.

---

## 14) Quick Health Checks

### Check Engine API port is listening
```bash
sudo ss -lntp | grep 8551
```

### Check EVM chainId (via JSON-RPC)
```bash
curl -s http://127.0.0.1:8547 \
  -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}' | jq
```

### Check syncing status
```bash
curl -s http://127.0.0.1:8547 \
  -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}' | jq
```

---

## 15) Validator Creation (Optional)

> Only run this if you are setting up a validator and have prepared keys and funding.

Basic example:

```bash
story validator create \
  --stake 1024000000000000000000 \
  --moniker "Cumulo" \
  --chain-id 1514 \
  --unlocked=true
```

With commission parameters:

```bash
story validator create \
  --stake 1035000000000000000000 \
  --moniker "Cumulo" \
  --chain-id 1514 \
  --unlocked=true \
  --commission-rate 500 \
  --max-commission-rate 2000 \
  --max-commission-change-rate 100
```

---

## ✅ Notes & Best Practices

- Always run **both services under the same user** to avoid path/JWT mismatches.
- Keep `--authrpc.addr 127.0.0.1` (local only) for security.
- If you expose `8547` publicly, consider:
  - Firewall allowlists
  - Nginx reverse proxy
  - Rate limiting and CORS tightening
- If you ever see the JWT path referencing another home (e.g. `/home/otheruser/...`), fix:
  - `~/.story/story/config/story.toml`
  - and/or the systemd unit flags

---

## Appendix: Clean restart

```bash
sudo systemctl restart story-geth
sleep 3
sudo systemctl restart story
```
