# Story Mainnet — Scheduled Maintenance Runbook (Validators)

**Maintenance window**  
🗓 **January 14, 2026 — 23:30 UTC**  
⏳ Expected downtime: **24–48 hours**

This document describes the **production-grade procedure** used by **Cumulo** to safely halt and later restart **Story Mainnet validator infrastructure** during the scheduled maintenance announced by the Story team.

---

## 📢 Official Announcement Summary

During the maintenance window:

- ❌ Transactions will be unavailable  
- ✅ Explorers will remain viewable  

### What’s happening
- **Infrastructure migration to AWS**  
- **Fusaka upgrade** (**story-geth v1.2.0**, including **EIP-7702**)

### Required actions
- **Validators & Node Operators**  
  Halt nodes at **23:30 UTC Jan 14** and **do not restart until confirmed**
- **RPC Providers**  
  Keep nodes operational and communicate expected downtime

---

## 🎯 Scope of This Runbook

This runbook applies to:

- Active **Story validators**
- **Hot / backup validator nodes** capable of participating in consensus

It **does NOT** apply to:

- Public RPC nodes (per the official announcement, RPC providers keep nodes running)
- Snapshot or archive-only nodes

---

## 🧭 Design Principles

- **UTC-only coordination** (avoid local timezone mistakes across regions)
- **No `halt_height` / `halt_time`** (not supported by Story configs)
- **systemd-native scheduling**
- **STOP + DISABLE** (halt at a precise time and prevent auto-start on reboot)
- **Auditable and reproducible** (visible in `systemctl list-timers`)
- **Single-operator friendly**: services are *disabled* but can still be started manually — operator must wait for the official “all-clear”

> Note: `disabled` prevents automatic start (boot/targets), but does **not** block a manual `systemctl start/restart`.  
> If you need an absolute “start lock”, use a temporary systemd override. Cumulo does **not** require that for single-operator ops.

---

## ✅ Preconditions

Verify UTC and NTP:

```bash
timedatectl
```

Expected:
- `Time zone: Etc/UTC`
- `System clock synchronized: yes`
- `NTP service: active`

---

## 🛠️ Halt Strategy (Production-Grade)

**Method:** `systemd timer` + **STOP + DISABLE**

---

## 1️⃣ Create the maintenance halt service (STOP + DISABLE)

This unit will **stop** both services and **disable** them in the same action.

```bash
sudo tee /etc/systemd/system/story-maintenance-halt.service >/dev/null <<'EOF'
[Unit]
Description=Story Maintenance Halt (stop + disable story and story-geth)
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/systemctl disable --now story.service story-geth.service
EOF
```

---

## 2️⃣ Create the systemd timer (UTC explicit)

```bash
sudo tee /etc/systemd/system/story-maintenance-halt.timer >/dev/null <<'EOF'
[Unit]
Description=Story Maintenance Halt Timer (2026-01-14 23:30 UTC)

[Timer]
OnCalendar=2026-01-14 23:30:00 UTC
Persistent=true
Unit=story-maintenance-halt.service

[Install]
WantedBy=timers.target
EOF
```

---

## 3️⃣ Enable and verify the timer

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now story-maintenance-halt.timer
```

Verify:

```bash
systemctl list-timers | grep story-maintenance-halt
systemctl status story-maintenance-halt.timer
```

---

## ⏱ What Happens at 23:30 UTC

systemd will execute:

```bash
systemctl disable --now story.service story-geth.service
```

Which results in:

- `story` and `story-geth` stop cleanly
- both units become **disabled** (won’t auto-start on reboot)

---

## 🔎 Post-Halt Verification

Confirm both services are stopped:

```bash
systemctl status story story-geth --no-pager
```

Confirm both services are disabled:

```bash
systemctl is-enabled story
systemctl is-enabled story-geth
```

Expected output:

```text
disabled
disabled
```

---

## 🚫 During the Maintenance Window

- Do **not** restart validator services (`story`, `story-geth`)
- Ignore block-production alerts (expected while stopped)
- You may prepare the `story-geth v1.2.0` upgrade **without starting services**
- Wait for the official “all-clear” from Story (Discord + X)

---

## 🔓 Recovery Procedure (After All-Clear)

### 1) Re-enable services

```bash
sudo systemctl enable story story-geth
```

### 2) Disable and remove the maintenance timer (clean-up)

```bash
sudo systemctl disable --now story-maintenance-halt.timer
sudo rm -f /etc/systemd/system/story-maintenance-halt.service
sudo rm -f /etc/systemd/system/story-maintenance-halt.timer
sudo systemctl daemon-reload
```

### 3) Start services (recommended order)

Start Execution (EVM) first:

```bash
sudo systemctl start story-geth
```

Wait a few seconds:

```bash
sleep 10
```

Start Consensus:

```bash
sudo systemctl start story
```

---

## 4️⃣ Post-Restart Verification

### Logs

```bash
sudo journalctl -u story-geth -f
```

In another terminal:

```bash
sudo journalctl -u story -f
```

### Sync status (CometBFT)

> Adjust port if your local RPC is not `26657`.

```bash
curl -s localhost:26657/status | jq .result.sync_info
```

---

## 🏁 Final Status Checklist

- ✔ Validator halted safely at the agreed UTC time  
- ✔ Services remained stopped during the window  
- ✔ Restart executed only after official confirmation  
- ✔ Procedure is auditable and reproducible via systemd  
