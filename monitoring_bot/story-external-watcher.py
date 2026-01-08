#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, json, socket, urllib.request, urllib.parse
from datetime import datetime, timezone

# ==========================
# Config (via env)
# ==========================
RPC_HTTP       = os.getenv("STORY_RPC_HTTP", "https://rpc.story.cumulo.me").rstrip("/")
VALCONS        = os.getenv("VALCONS_ADDRESS", "").strip().upper()
BOT_TOKEN      = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID        = os.getenv("TELEGRAM_CHAT_ID", "")
NETWORK        = os.getenv("NETWORK_LABEL", "story-1")

POLL_SEC       = int(os.getenv("POLL_INTERVAL_SEC", "2"))
BACKFILL_N     = int(os.getenv("BACKFILL_LAST_N", "100"))

STATE_FILE     = os.getenv("STATE_FILE", "/var/lib/story-external-watcher/state.json")

# RPC robustness / validators pagination
PAGES_MAX      = int(os.getenv("VALIDATORS_PAGES_MAX", "12"))
PER_PAGE       = int(os.getenv("VALIDATORS_PER_PAGE", "100"))
RETRY_HTTP     = int(os.getenv("RETRY_HTTP", "2"))

# Anti false-positives
BLOCK_CONFIRM_LAG    = int(os.getenv("BLOCK_CONFIRM_LAG", "2"))
FRESH_BLOCK_SKIP_SEC = int(os.getenv("FRESH_BLOCK_SKIP_SEC", "3"))
DOUBLE_CONFIRM       = os.getenv("DOUBLE_CONFIRM", "true").lower() == "true"
PENDING_TTL_SEC      = int(os.getenv("PENDING_TTL_SEC", "30"))  # how long to retry a pending height

HOSTNAME = socket.gethostname()

if not VALCONS or not BOT_TOKEN or not CHAT_ID:
    print("Missing VALCONS_ADDRESS or TELEGRAM_* in the environment.", file=sys.stderr)
    sys.exit(1)

# ==========================
# Utils
# ==========================
def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def http_get_json(url, timeout=8, retries=RETRY_HTTP):
    last_err = None
    for _ in range(max(1, retries)):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return json.load(r)
        except Exception as e:
            last_err = e
            time.sleep(0.4)
    if last_err:
        sys.stderr.write(f"[http] {last_err} url={url}\n")
    return None

def send_telegram(text):
    if not BOT_TOKEN or not CHAT_ID:
        return False
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode("utf-8"))
        with urllib.request.urlopen(req, timeout=8) as r:
            r.read()
        return True
    except Exception as e:
        sys.stderr.write(f"[telegram] error: {e}\n")
        return False

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            st = json.load(f)
    except Exception:
        st = {}
    # Defaults & backwards compatibility
    return {
        "last_checked":   int(st.get("last_checked", 0)),
        "alerted_misses": list(st.get("alerted_misses", [])),
        # kept for compatibility (not used anymore)
        "last_report_ts": int(st.get("last_report_ts", 0)),
        # dict: {"height": unix_ts}
        "pending_miss":   dict(st.get("pending_miss", {}))
    }

def save_state(st):
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w") as f:
             json.dump(st, f)
    except Exception as e:
        sys.stderr.write(f"[state] write error: {e}\n")

# ==========================
# RPC helpers
# ==========================
def get_latest_height():
    j = http_get_json(f"{RPC_HTTP}/status")
    if not j:
        return 0
    try:
        return int(j["result"]["sync_info"]["latest_block_height"])
    except Exception:
        return 0

def get_block_time_iso(height):
    j = http_get_json(f"{RPC_HTTP}/block?height={height}")
    try:
        return j["result"]["block"]["header"]["time"]
    except Exception:
        return None

def seconds_since(ts_iso):
    if not ts_iso:
        return 999999
    try:
        if ts_iso.endswith("Z"):
            ts_iso = ts_iso.replace("Z", "+00:00")
        t = datetime.fromisoformat(ts_iso)
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - t.astimezone(timezone.utc)).total_seconds()
    except Exception:
        return 999999

def commit_flag_for_valcons(height):
    """
    Returns 2/1/0 if VALCONS is present in commit signatures, or None if it's not present.
    """
    j = http_get_json(f"{RPC_HTTP}/commit?height={height}")
    if not j:
        return None
    try:
        sigs = j["result"]["signed_header"]["commit"]["signatures"]
        for s in sigs:
            if (s.get("validator_address", "").upper() == VALCONS):
                flag = s.get("block_id_flag", s.get("block_id_flag_str"))
                if isinstance(flag, int):
                    return flag
                if isinstance(flag, str):
                    if flag == "BLOCK_ID_FLAG_COMMIT": return 2
                    if flag == "BLOCK_ID_FLAG_NIL":    return 1
                    if flag == "BLOCK_ID_FLAG_ABSENT": return 0
                    return None
        return None
    except Exception:
        return None

def in_validator_set(height):
    """
    True if VALCONS is in the validator set at that height.
    """
    for p in range(1, PAGES_MAX + 1):
        j = http_get_json(f"{RPC_HTTP}/validators?height={height}&per_page={PER_PAGE}&page={p}")
        if not j:
            return False
        try:
            addrs = [v["address"].upper() for v in j["result"]["validators"]]
            if VALCONS in addrs:
                return True
            # stop if page is empty
            if not addrs:
                return False
        except Exception:
            return False
    return False

def classify_height(height):
    """
    SIGNED / MISSED / NOT_IN_SET / UNVERIFIED
    """
    flag = commit_flag_for_valcons(height)
    if flag is None:
        # Not present in commit → check whether it was in the validator set
        try:
            return "MISSED" if in_validator_set(height) else "NOT_IN_SET"
        except Exception:
            return "UNVERIFIED"

    if flag == 2:
        return "SIGNED"
    if flag in (0, 1):
        return "MISSED"
    return "UNVERIFIED"

# ==========================
# Stable window summary
# (used only to position last_checked; no reports are sent)
# ==========================
def summarize_window(tip, n=100):
    stable_tip = max(0, tip - BLOCK_CONFIRM_LAG)
    if stable_tip <= 0:
        return 0, 0, 0, 0, []

    start = max(1, stable_tip - n + 1)
    signed = 0
    missed = 0
    missed_heights = []

    for h in range(start, stable_tip + 1):
        bt = get_block_time_iso(h)
        if bt and seconds_since(bt) < FRESH_BLOCK_SKIP_SEC:
            continue
        res = classify_height(h)
        if res == "SIGNED":
            signed += 1
        elif res == "MISSED":
            missed += 1
            missed_heights.append(h)
        # NOT_IN_SET / UNVERIFIED are ignored in the summary

    return start, stable_tip, signed, missed, missed_heights

# ==========================
# Main loop
# ==========================
def main():
    st = load_state()
    last_checked    = int(st.get("last_checked", 0))
    alerted_misses  = set(st.get("alerted_misses", []))
    pending_miss    = dict(st.get("pending_miss", {}))  # height -> unix_ts (as string key)

    # Startup message only
    send_telegram(
        "✅ *Story External Watcher* started on `{}`\n"
        "Network: `{}` • RPC: `{}`\n"
        "VALCONS: `{}`\n"
        "Interval: `{}s`".format(HOSTNAME, NETWORK, RPC_HTTP, VALCONS, POLL_SEC)
    )

    # Initialize last_checked using a backfill window (no chat summary)
    tip = get_latest_height()
    if tip > 0:
        s, e, signed, missed, missed_list = summarize_window(tip, BACKFILL_N)
        if s and e:
            last_checked = e
            st["last_checked"] = last_checked
            st["alerted_misses"] = sorted(list(alerted_misses))[-2000:]
            save_state(st)

    while True:
        tip = get_latest_height()
        if tip <= 0:
            time.sleep(POLL_SEC)
            continue

        safe_tip = max(0, tip - BLOCK_CONFIRM_LAG)

        # 1) Retry pending heights (real double confirmation)
        if DOUBLE_CONFIRM and pending_miss:
            now_ts = int(time.time())
            for h_str in list(pending_miss.keys()):
                try:
                    h = int(h_str)
                except:
                    h = h_str
                first_ts = pending_miss.get(h_str, 0)

                # Skip if block is too fresh
                bt = get_block_time_iso(h)
                if bt and seconds_since(bt) < FRESH_BLOCK_SKIP_SEC:
                    continue

                res = classify_height(h)
                if res == "MISSED":
                    if h not in alerted_misses:
                        send_telegram(
                            "🚨 *Missed block*\n"
                            "• Height: *{}*\n"
                            "• Network: `{}`\n"
                            "• Watcher: `{}`\n"
                            "• Time: {}".format(h, NETWORK, HOSTNAME, now_iso())
                        )
                        alerted_misses.add(h)
                        if len(alerted_misses) > 5000:
                            alerted_misses = set(sorted(alerted_misses)[-2000:])
                    pending_miss.pop(h_str, None)
                elif res in ("SIGNED", "NOT_IN_SET"):
                    # Not a miss definitively
                    pending_miss.pop(h_str, None)
                else:
                    # UNVERIFIED: drop after TTL; otherwise keep for next cycle
                    if now_ts - int(first_ts) > PENDING_TTL_SEC:
                        pending_miss.pop(h_str, None)

        # 2) Process new heights (last_checked+1 .. safe_tip)
        start_h = max(1, last_checked + 1)
        if start_h <= safe_tip:
            for h in range(start_h, safe_tip + 1):
                bt = get_block_time_iso(h)
                if bt and seconds_since(bt) < FRESH_BLOCK_SKIP_SEC:
                    continue

                res = classify_height(h)
                if res == "MISSED":
                    if DOUBLE_CONFIRM:
                        if str(h) not in pending_miss and h not in alerted_misses:
                            pending_miss[str(h)] = int(time.time())
                    else:
                        if h not in alerted_misses:
                            send_telegram(
                                "🚨 *Missed block*\n"
                                "• Height: *{}*\n"
                                "• Network: `{}`\n"
                                "• Watcher: `{}`\n"
                                "• Time: {}".format(h, NETWORK, HOSTNAME, now_iso())
                            )
                            alerted_misses.add(h)
                            if len(alerted_misses) > 5000:
                                alerted_misses = set(sorted(alerted_misses)[-2000:])
                # SIGNED / NOT_IN_SET / UNVERIFIED: nothing else to do

            last_checked = safe_tip

        # Persist state (no periodic reports)
        st["last_checked"]   = last_checked
        st["alerted_misses"] = sorted(list(alerted_misses))[-2000:]
        st["pending_miss"]   = pending_miss
        save_state(st)

        time.sleep(POLL_SEC)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
