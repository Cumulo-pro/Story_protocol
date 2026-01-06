# Story Mainnet — Node CLI Command Reference


## ⚙️ systemd — Service Operations

### Reload systemd units
```bash
sudo systemctl daemon-reload
```

### Start services
```bash
sudo systemctl start story-geth
sudo systemctl start story
```

### Stop services
```bash
sudo systemctl stop story
sudo systemctl stop story-geth
```

### Restart services (recommended order)
```bash
sudo systemctl restart story-geth && sleep 5 && sudo systemctl restart story
```

### Enable services at boot
```bash
sudo systemctl enable story story-geth
```

### Disable services
```bash
sudo systemctl disable story
sudo systemctl disable story-geth
```

### Check service status
```bash
sudo systemctl status story
sudo systemctl status story-geth
```

---

## 📜 Logs

### Follow both services
```bash
sudo journalctl -u story -u story-geth -f
```

### Follow individually (raw output)
```bash
sudo journalctl -u story -f -o cat
sudo journalctl -u story-geth -f -o cat
```

---

## 📡 Node Status & Sync

### Latest block height
```bash
curl -s localhost:26657/status | jq .result.sync_info.latest_block_height
```

### Syncing status
```bash
curl -s localhost:26657/status | jq .result.sync_info.catching_up
```

### Generic node info (auto-detect RPC port)
```bash
curl localhost:$(sed -n '/\[rpc\]/,/laddr/ { /laddr/ {s/.*://; s/".*//; p} }' $HOME/.story/story/config/config.toml)/status | jq
```

---

## 🌐 Peers

### Number of peers
```bash
curl -s http://localhost:26657/net_info | jq '.result.n_peers'
```

### List connected peers
```bash
curl -s http://localhost:26657/net_info | jq -r '.result.peers[] | "\(.node_info.id)@\(.remote_ip):26656"'
```

### Your node peer string
```bash
node_id=$(curl -s http://localhost:26657/status | jq -r '.result.node_info.id')
public_ip=$(curl -s ifconfig.me)
echo "${node_id}@${public_ip}:26646"
```

---

## 🔑 Validator Keys & Export

### Export validator keys
```bash
story validator export
```

### Export derived EVM private key
```bash
story validator export --export-evm-key
```

### Extract EVM public key only
```bash
story validator export | grep "EVM Public Key:" | awk '{print $NF}'
```

---

## 🧾 Validator Operations

### Create validator
```bash
story validator create \
  --stake 1035000000000000000000 \
  --moniker (moniker) \
  --chain-id 1514 \
  --unlocked=true \
  --commission-rate 500 \
  --max-commission-rate 2000 \
  --max-commission-change-rate 100
```

---

## 💰 Staking Operations

### Delegate to yourself
```bash
story validator stake \
  --chain-id 1514 \
  --validator-pubkey $(story validator export | grep "Compressed Public Key (hex)" | awk '{print $NF}') \
  --stake 1000000000000000000 \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

### Delegate
```bash
story validator stake \
  --chain-id 1514 \
  --validator-pubkey <VALIDATOR_PUB_KEY_IN_HEX> \
  --stake 1000000000000000000 \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

### Delegate on behalf of another delegator
```bash
story validator stake-on-behalf \
  --chain-id 1514 \
  --validator-pubkey <VALIDATOR_PUB_KEY_IN_HEX> \
  --delegator-pubkey <DELEGATOR_PUB_KEY_IN_HEX> \
  --stake 1000000000000000000 \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

### Add operator
```bash
story validator add-operator \
  --chain-id 1514 \
  --operator <OPERATOR_EVM_ADDRESS> \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

### Remove operator
```bash
story validator remove-operator \
  --operator <OPERATOR_EVM_ADDRESS> \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

### Set / change withdrawal address
```bash
story validator set-withdrawal-address \
  --withdrawal-address <YOUR_EVM_ADDRESS> \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

---

## 🔄 Unstaking

### Unstake (self)
```bash
story validator unstake \
  --chain-id 1514 \
  --validator-pubkey $(story validator export | grep "Compressed Public Key (hex)" | awk '{print $NF}') \
  --unstake 1000000000000000000 \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

### Unstake
```bash
story validator unstake \
  --chain-id 1514 \
  --validator-pubkey <VALIDATOR_PUB_KEY_IN_HEX> \
  --unstake 1000000000000000000 \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

### Unstake on behalf
```bash
story validator unstake-on-behalf \
  --chain-id 1514 \
  --validator-pubkey <VALIDATOR_PUB_KEY_IN_HEX> \
  --delegator-pubkey <DELEGATOR_PUB_KEY_IN_HEX> \
  --unstake 1000000000000000000 \
  --private-key $(cat $HOME/.story/story/config/.env | grep "PRIVATE_KEY" | awk -F'=' '{print $2}')
```

---

## ⛓️ story-geth (EVM) Commands

### Check running version
```bash
story-geth version
```

### Latest block
```bash
story-geth --exec "eth.blockNumber" attach ~/.story/geth/story/geth.ipc
```

### Check sync status
```bash
story-geth --exec "eth.syncing" attach ~/.story/geth/story/geth.ipc
```

### List peers
```bash
story-geth --exec "admin.peers" attach ~/.story/geth/story/geth.ipc
```

### Your enode
```bash
story-geth --exec "admin.nodeInfo.enode" attach ~/.story/geth/story/geth.ipc
```

### Gas price
```bash
story-geth --exec "eth.gasPrice" attach ~/.story/geth/story/geth.ipc
```

### Account balance
```bash
story-geth --exec "eth.getBalance('<YOUR_EVM_ADDRESS>')" attach ~/.story/geth/story/geth.ipc
```

---

## 🧹 Cleanup (Destructive)

### Stop services
```bash
sudo systemctl stop story story-geth
```

### Remove services
```bash
sudo rm /etc/systemd/system/story.service
sudo rm /etc/systemd/system/story-geth.service
sudo systemctl daemon-reload
```

### Remove node data
```bash
rm -rf $HOME/.story
rm -rf $HOME/story
```

---

## ✅ Notes

- Always restart **story-geth first**, then **story**
- Many commands assume default ports — adjust if you customized them
- Keep this file as a **runbook** for day-to-day operations
