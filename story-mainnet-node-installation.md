# Story Mainnet (story-1) — Node Installation Guide (Clean Install)

**Chain ID:** `story-1`  
**Story (consensus client):** `v1.4.2-stable`  
**Story-Geth (execution client):** `v1.2.0-stable`  

This is a **clean, from-scratch** installation flow aligned with our internal guide:
- Install `story-geth` (execution)
- Build and install `story` (consensus)
- Init node
- Download `genesis.json` + `addrbook.json`
- Create `systemd` services
- Start services and follow logs
- (Optional) Create validator

> ⚠️ If you previously ran Story under a different user/home, remove old config before starting (see **Troubleshooting**).

---

## ✅ Recommended Hardware

- **CPU:** 8 cores+
- **RAM:** 32 GB+
- **Disk:** 400 GB+ NVMe
- **Network:** 100 Mbps+

---

## 🔌 Ports

| Component | Purpose | Bind | Port |
|---|---|---:|---:|
| story | REST API | 0.0.0.0 | 1307 |
| story-geth | EVM JSON-RPC (HTTP) | 0.0.0.0 | 8547 |
| story-geth | Engine API (AuthRPC, internal) | 127.0.0.1 | 8551 |

---

## 1) Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git wget htop tmux build-essential jq make lz4 gcc unzip
```

---

## 2) Install Go (required to build `story`)

```bash
cd $HOME
VER="1.22.5"
wget "https://golang.org/dl/go$VER.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$VER.linux-amd64.tar.gz"
rm "go$VER.linux-amd64.tar.gz"

[ ! -f ~/.bash_profile ] && touch ~/.bash_profile
echo "export PATH=\$PATH:/usr/local/go/bin:\$HOME/go/bin" >> ~/.bash_profile
source ~/.bash_profile

mkdir -p ~/go/bin
```

---

## 3) Install Story-Geth (Execution Client)

```bash
cd $HOME
rm -rf story-geth
wget -O story-geth https://github.com/piplabs/story-geth/releases/download/v1.2.0/geth-linux-amd64
chmod +x $HOME/story-geth
mv $HOME/story-geth $HOME/go/bin/
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
mv $HOME/story/story $HOME/go/bin/
```

Verify:

```bash
story version
# Version v1.4.2-stable
```

---

## 5) Initialize Node

```bash
story init --network story --moniker CumuloRPC
```

---

## 6) Download Genesis

Primary:

```bash
curl -Ls https://ss.story.nodestake.org/genesis.json > $HOME/.story/story/config/genesis.json
```

Alternative:

```bash
wget -O genesis.json https://snapshots.polkachu.com/genesis/story/genesis.json --inet4-only
mv genesis.json $HOME/.story/story/config/
```

---

## 7) Download Addrbook

Primary:

```bash
curl -Ls https://ss.story.nodestake.org/addrbook.json > $HOME/.story/story/config/addrbook.json
```

Alternative:

```bash
wget -O addrbook.json https://snapshots.polkachu.com/addrbook/story/addrbook.json --inet4-only
mv addrbook.json $HOME/.story/story/config/
```

---

## 8) Create `story.service` (Consensus)

File: `/etc/systemd/system/story.service`

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
  --engine-endpoint=http://127.0.0.1:8551

Restart=on-failure
RestartSec=5s
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF
```

---

## 9) Create `story-geth.service` (Execution)

File: `/etc/systemd/system/story-geth.service`

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
  --http \
  --http.addr 0.0.0.0 \
  --http.port 8547 \
  --http.api eth,net,web3,engine \
  --http.corsdomain "*" \
  --http.vhosts "*"

Restart=on-failure
RestartSec=3
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
EOF
```

---

## 10) Enable & Start Services

```bash
sudo systemctl daemon-reload
sudo systemctl enable story story-geth

sudo systemctl start story-geth
sudo systemctl start story

journalctl -u story -u story-geth -f
```

---

## 11) Check Logs

```bash
journalctl -u story -u story-geth -f
```

---

## 12) Create Validator (Optional)

```bash
story validator create --stake 1024000000000000000000 --moniker "Cumulo" --chain-id 1514 --unlocked=true
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

## Troubleshooting (only if you used old configs)

### A) JWT / engine errors after reusing a previous setup
If you see errors like:
- `engine-jwt-file = "/home/otheruser/.../jwtsecret"` or
- `open ... jwtsecret: no such file or directory`

It means your `story.toml` (or old home directory) contains a stale absolute path.

Fix by checking:

```bash
grep -nE "engine|jwt" $HOME/.story/story/config/story.toml
```

If it points to another user, either:
- reinstall clean (remove old config), or
- update `engine-jwt-file` path to your current `$HOME`.

### B) Clean reset of local state (destructive)
```bash
sudo systemctl stop story story-geth
rm -rf $HOME/.story/story/data
rm -rf $HOME/.story/geth/story/geth/chaindata
```

Then start services again.

---
