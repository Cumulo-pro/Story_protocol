# Story Mainnet — Scheduled Maintenance Runbook (Validators)

**Maintenance window**  
🗓 **January 14, 2026 — 23:30 UTC**  
⏳ Expected downtime: **24–48 hours**

This document describes the **production-grade procedure** used by **Cumulo** to safely halt and later restart Story Mainnet validator infrastructure during the scheduled maintenance announced by the Story team.

---

## 📢 Official Announcement Summary

During the maintenance window:

- ❌ Transactions will be unavailable  
- ✅ Explorers will remain viewable  

### What’s happening
- **Infrastructure migration to AWS**  
- **Fusaka upgrade** (`story-geth v1.2.0`, including **EIP-7702**)

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

- Public RPC nodes
- Snapshot or archive-only nodes  

---

## 🧭 Design Principles

- **UTC-only coordination**
- **No `halt_height` / `halt_time`** (not supported by Story configs)
- **systemd-native scheduling**
- **Zero chance of accidental restart**
- **Auditable, reproducible, production-safe**

---

## ✅ Preconditions

```bash
timedatectl
```

Expected:
- `Time zone: Etc/UTC`
- `System clock synchronized: yes`
- `NTP service: active`

---

## 🛠️ Halt Strategy (Production-Grade)

**Method:** `systemd timer` + **STOP + MASK**

---

## 1️⃣ Create the maintenance halt service

```bash
sudo tee /etc/systemd/system/story-maintenance-halt.service >/dev/null <<'EOF'
[Unit]
Description=Story Maintenance Halt (stop + mask story and story-geth)
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash -lc 'set -e; systemctl stop story story-geth; systemctl mask story story-geth'
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

```bash
systemctl stop story story-geth
systemctl mask story story-geth
```

---

## 🚫 During the Maintenance Window

- Do not restart validator services
- Ignore block-production alerts
- Prepare `story-geth v1.2.0` upgrade **without starting services**

---

## 🔓 Recovery Procedure (After All-Clear)

```bash
sudo systemctl unmask story story-geth
sudo systemctl disable --now story-maintenance-halt.timer
sudo rm -f /etc/systemd/system/story-maintenance-halt.service
sudo rm -f /etc/systemd/system/story-maintenance-halt.timer
sudo systemctl daemon-reload
```

Start services:

```bash
sudo systemctl start story-geth
sleep 10
sudo systemctl start story
```

---

## 4️⃣ Post-Restart Verification

```bash
curl -s localhost:26657/status | jq .result.sync_info
```

---

## 🏁 Final Status

✔ Validator halted safely  
✔ Restart fully controlled  
✔ UTC-coordinated  
✔ Production-grade procedure
