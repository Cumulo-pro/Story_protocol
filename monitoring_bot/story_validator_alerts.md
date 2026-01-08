# Story Validator Alerts 🤖🔔  
Telegram bot for **Story validators** to monitor **missed blocks**, **validator status (in/out of set)**, and generate **hourly reports**.

**Bot:** @story_validator_watcher_bot  
**Name:** Story Validator Alerts


<img width="360" height="158" alt="image" src="https://github.com/user-attachments/assets/72eb64e1-2c42-4c1c-b0c5-5fc65f59b298" />

---

## What this bot is for

If you operate a validator on **Story mainnet or testnet**, this bot helps you:

- Detect **missed blocks** in near real-time
- Track whether your validator is **ACTIVE (in set)** or **INACTIVE (out of set)**
- Get a periodic **hourly report** with signed vs missed blocks
- Query live validator info: voting power, rank, recent missed streaks
- Optionally resolve and display **VALOPER + Moniker** via **LCD**

---

## How it works (high level)

The bot uses two loops:

1. **Telegram loop (commands & chat interaction)**  
   Reads updates via Telegram Bot API and responds to commands like `/help`, `/info`, `/check`, etc.

2. **Watcher loop (alerts & reports)**  
   Runs continuously in the background and:
   - Reads each chat’s saved configuration (stored in `STATE_DIR/<chat_id>.json`)
   - Queries the configured Story RPC (`/status`, `/commit`, `/validators`, etc.)
   - Sends alerts when missed blocks are detected (only if `/watch on`)
   - Sends hourly reports (only if `/report on`)

---

## Key concepts (addresses)

To bind the bot to a validator **you must provide `VALCONS`**:

- **VALCONS** (required): 40-char HEX address (uppercase) used by CometBFT/Tendermint (the one you used: `B93DD4...`)

Optional:
- **VALOPER**: bech32 operator address (e.g. `storyvaloper1...`)
- **LCD**: REST endpoint to auto-resolve moniker/valoper

✅ Recommended: use **VALCONS** always. That’s the address used in `/commit` signatures.

---

## Quick start (in Telegram)

1) Open the bot: **@story_validator_watcher_bot**  
2) Run:

- `/start`  
- Paste your **VALCONS** (without a command)  
  or use: `/setvalcons <HEX>`

3) Enable alerts:
- `/watch on`

4) (Optional) Enable hourly reports:
- `/report on`

---

## Command menu (what each command does)

### Basic
- `/start`  
  Shows welcome message and prompts you to paste your VALCONS if missing.

- `/help`  
  Shows the full command list.

- `/ping`  
  Basic connectivity test.

### Network & endpoints
- `/network <mainnet|testnet>`  
  Switch between Story mainnet and testnet (Aeneid).

- `/setrpc <url>`  
  Set a custom RPC endpoint (overrides defaults).

- `/rpc default`  
  Reset RPC to the default for the selected network.

### LCD (optional, for moniker/valoper)
- `/setlcd <url>`  
  Set an LCD endpoint (REST). Used only to enrich `/info`.

- `/lcd default`  
  Remove custom LCD (falls back to environment default if configured).

### Validator identity
- `/setvalcons <HEX>`  
  Set your validator consensus address (required).

- `/setvaloper <bech32>` *(optional)*  
  Set operator address manually (useful if you don’t want LCD auto-resolve).

### Tuning
- `/setlag <N>`  
  How many blocks behind the tip to consider “stable” (default: `2`).

- `/setwin <N>`  
  Default analysis window for `/check` and reports (default: `200`).

### Alerts & reports
- `/watch on|off`  
  Enable/disable real-time missed-block alerts.

- `/report on|off`  
  Enable/disable hourly report messages.

### Inspection
- `/whoami`  
  Shows your current configuration (network, rpc, valcons, lag, window, watch/report).

- `/info`  
  Shows validator status:
  - ACTIVE / INACTIVE (in set)
  - voting power + share
  - rank by voting power
  - signed vs missed in the analysis window
  - missed streak + most recent missed blocks  
  If LCD is configured, it may include:
  - moniker
  - commission
  - jailed status

- `/check [N]`  
  Manual check for the last `N` blocks (or defaults to your configured window).

---

## What you can configure

### Per chat (saved in STATE_DIR)
Each Telegram chat has its own JSON file, so you can configure different validators per chat/user.

Settings include:
- network: mainnet/testnet
- rpc: custom RPC or default
- lcd: optional
- valcons: required
- valoper: optional
- lag, win
- watch/report on/off

### Environment variables (service-level defaults)

| Variable | Default | Description |
|---------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | (required) | Token from BotFather |
| `STATE_DIR` | `/var/lib/validator-bot` | Where chat configs are stored |
| `BOT_POLL_SEC` | `2` | Watcher loop sleep interval |
| `DEFAULT_MAINNET_RPC` | `https://rpc.story.cumulo.me` | Default mainnet RPC |
| `DEFAULT_TESTNET_RPC` | `https://rpc.story-aeneid.cumulo.me` | Default testnet RPC |
| `DEFAULT_MAINNET_LCD` | `""` | Optional default LCD (mainnet) |
| `DEFAULT_TESTNET_LCD` | `""` | Optional default LCD (testnet) |

> Tip: if `/info` is slow because you use a huge `win` (e.g. 5000), consider using a separate `INFO_WIN` in your fork, or keep `/info` on a smaller window and use `/check 5000` for deep audits.
