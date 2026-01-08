# Story External Watcher (Telegram) — Setup Guide

This guide explains how to configure and run **`story-external-watcher.py`** as a **systemd service**.
The watcher monitors a Story validator (by **VALCONS**) using an RPC endpoint and sends Telegram alerts when it detects missed blocks.

> ✅ This is the **non-interactive / single-chat** watcher (one `CHAT_ID`).  
> If you need a multi-user interactive bot with `/commands`, use the other bot (`validator-bot`).

---

## What it does

- Polls the Story RPC (`/status`, `/commit`, `/validators`, `/block`)
- Confirms missed blocks (optional double-confirm logic)
- Sends alerts to Telegram:
  - watcher started
  - missed block events

---

## Requirements

- Linux server with **systemd**
- Python **3.8+**
- Outbound HTTPS allowed to:
  - your Story RPC endpoint
  - `api.telegram.org`

No external Python packages required (stdlib only).

---

## 1) Install the script

Choose a directory (example: `/opt/story-external-watcher`):

```bash
sudo mkdir -p /opt/story-external-watcher
sudo cp story-external-watcher.py /opt/story-external-watcher/story-external-watcher.py
sudo chmod +x /opt/story-external-watcher/story-external-watcher.py
```

---

## 2) Create a dedicated system user (recommended)

```bash
sudo useradd --system --home /opt/story-external-watcher --shell /usr/sbin/nologin story-watcher
```

Set ownership:

```bash
sudo chown -R story-watcher:story-watcher /opt/story-external-watcher
```

---

## 3) Create the state directory

The script stores a small state file (last checked height, pending confirmations, etc.).

```bash
sudo mkdir -p /var/lib/story-external-watcher
sudo chown -R story-watcher:story-watcher /var/lib/story-external-watcher
sudo chmod 750 /var/lib/story-external-watcher
```

---

## 4) Create the environment file

Create an env file (example: `/etc/story-external-watcher/story-external-watcher.env`):

```bash
sudo mkdir -p /etc/story-external-watcher
sudo nano /etc/story-external-watcher/story-external-watcher.env
```

Paste and edit values:

```bash
# ===== REQUIRED =====

# Story RPC base URL (no trailing slash)
STORY_RPC_HTTP="https://YOUR_STORY_RPC:26657"

# Your validator consensus address (HEX, 40 chars, uppercase)
# Example format: B93DD4D30F2837187D6BF66C6D53799F2E1A1272
VALCONS_ADDRESS="YOUR_VALCONS_HEX"

# Telegram bot token from @BotFather
TELEGRAM_BOT_TOKEN="123456789:AA..."

# Telegram Chat ID where alerts will be sent
# Tip: use @userinfobot, or add the bot to a group and get the group chat id.
TELEGRAM_CHAT_ID="123456789"

# Label included in alerts (optional)
NETWORK_LABEL="story-1"

# ===== OPTIONAL / TUNING =====

# Poll interval (seconds)
POLL_INTERVAL_SEC="2"

# On start: backfill last N blocks to position last_checked (no messages sent)
BACKFILL_LAST_N="100"

# State file path
STATE_FILE="/var/lib/story-external-watcher/state.json"

# Validators pagination
VALIDATORS_PAGES_MAX="12"
VALIDATORS_PER_PAGE="100"
RETRY_HTTP="2"

# Anti false positives / confirmation
BLOCK_CONFIRM_LAG="2"
FRESH_BLOCK_SKIP_SEC="3"
DOUBLE_CONFIRM="true"
PENDING_TTL_SEC="30"
```

Lock down permissions:

```bash
sudo chmod 640 /etc/story-external-watcher/story-external-watcher.env
sudo chown root:story-watcher /etc/story-external-watcher/story-external-watcher.env
```

> ✅ If you prefer, you can use group `root:root` and run the service as root,  
> but the above is safer (service user can **read** env, not write it).

---

## 5) Quick configuration checks

### Check the RPC responds

```bash
RPC="https://YOUR_STORY_RPC:26657"
curl -s "$RPC/status" | head
```

### Validate VALCONS format

VALCONS must be:
- 40 hex characters
- uppercase

Example:

```bash
echo "B93DD4D30F2837187D6BF66C6D53799F2E1A1272" | grep -E '^[0-9A-F]{40}$' && echo OK
```

### Test Telegram token (no secret printed)

```bash
TOKEN="123456789:AA..."
curl -s "https://api.telegram.org/bot${TOKEN}/getMe" | head
```

---

## 6) Create the systemd service

Create: `/etc/systemd/system/story-external-watcher.service`

```bash
sudo nano /etc/systemd/system/story-external-watcher.service
```

Paste:

```ini
[Unit]
Description=Story External Watcher (Telegram Alerts)
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=story-watcher
Group=story-watcher
WorkingDirectory=/opt/story-external-watcher

EnvironmentFile=/etc/story-external-watcher/story-external-watcher.env

ExecStart=/usr/bin/env python3 /opt/story-external-watcher/story-external-watcher.py

Restart=always
RestartSec=3

# Hardening (safe defaults)
NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=full
ProtectHome=true

# Allow writing only to state dir
ReadWritePaths=/var/lib/story-external-watcher

# Limits
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now story-external-watcher.service
```

---

## 7) Logs and status

Live logs:

```bash
sudo journalctl -u story-external-watcher.service -f
```

Status:

```bash
sudo systemctl status story-external-watcher.service --no-pager -l
```

---

## 8) How to get `TELEGRAM_CHAT_ID`

### Option A — Direct messages (private chat)
1. Open your bot in Telegram and press **Start**
2. Use a helper bot (e.g. `@userinfobot`) to get your user id  
   (this is often the same as the private chat id)

### Option B — Telegram group
1. Create a group and add your bot
2. Send a message in the group
3. Fetch updates using your bot token:

```bash
TOKEN="123456789:AA..."
curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates" | less
```

Look for `"chat":{"id":-123...}` (note the negative id for groups).  
Use that value in `TELEGRAM_CHAT_ID`.

---

## 9) Common issues

### Bot “doesn’t respond”
This watcher is **not interactive**. It only sends alerts to the configured `TELEGRAM_CHAT_ID`.

### No alerts are being sent
- Check logs (`journalctl`)
- Confirm:
  - correct `TELEGRAM_BOT_TOKEN`
  - correct `TELEGRAM_CHAT_ID`
  - the bot can message that chat (start the bot in DM / add it to the group)
- Confirm RPC is reachable from the server

### False positives around fresh blocks
Tune:
- `BLOCK_CONFIRM_LAG`
- `FRESH_BLOCK_SKIP_SEC`
- keep `DOUBLE_CONFIRM=true`

---

## 10) Update / deploy new versions

```bash
sudo systemctl stop story-external-watcher.service
sudo cp story-external-watcher.py /opt/story-external-watcher/story-external-watcher.py
sudo chown story-watcher:story-watcher /opt/story-external-watcher/story-external-watcher.py
sudo chmod +x /opt/story-external-watcher/story-external-watcher.py
sudo systemctl start story-external-watcher.service
```

---

## Security notes

- **Never** commit or publish:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID` (optional, but usually not shared)
  - internal RPC endpoints (if private)
- Keep the env file permissions restricted (`640`)
- Run as a dedicated user (`story-watcher`) with a write-only state directory.

---

## License

Add your preferred license here (MIT/Apache-2.0/etc).
