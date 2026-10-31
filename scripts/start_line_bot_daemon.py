import os
import sys
import time
import json
import re
import subprocess
import threading
import urllib.request
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DATA_DIR = os.path.join(BASE_DIR, "data")
CLOUDFLARED_EXE = os.path.join(BASE_DIR, "bin", "cloudflared.exe")
WEBHOOK_SCRIPT = os.path.join(SCRIPTS_DIR, "line_gemini_webhook.py")
STATUS_PATH = os.path.join(DATA_DIR, "line_bot_status.json")
CHAT_LOG_PATH = os.path.join(DATA_DIR, "line_chat_logs.json")
DAEMON_LOG_PATH = os.path.join(DATA_DIR, "daemon_run.log")

sys.path.append(SCRIPTS_DIR)
try:
    from overnight_r2_crawler import put_object_r2
except Exception:
    put_object_r2 = None

LINE_ACCESS_TOKEN = "nsjrJajD/02mW2tXzVo3+aJqo9VTIb6GAZF6xJfddGSTYhPdTBiV9u96/87adVQdQWAPQULuzfX2JIgwNl3CRvUGPlZU+R/6Wt2VN/CZlWCmIN8q+N7diGkWdW/+4nnOJLW57QmAHkTGTBztPeiwHgdB04t89/1O/w1cDnyilFU="


def log_msg(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(DAEMON_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def update_line_webhook_endpoint(tunnel_url):
    url = "https://api.line.me/v2/bot/channel/webhook/endpoint"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = json.dumps({"endpoint": tunnel_url}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="PUT")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status == 200


def test_line_webhook_endpoint(tunnel_url):
    url = "https://api.line.me/v2/bot/channel/webhook/test"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = json.dumps({"endpoint": tunnel_url}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def save_and_sync_status(tunnel_url, test_res):
    status_obj = {
        "bot_name": "Siwasupagent (@813nyyia)",
        "webhook_url": tunnel_url,
        "status": "ONLINE",
        "webhook_verified": test_res.get("success", False),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stats": {
            "followers_total": 2,
            "replies_2026_10_29": 18
        }
    }
    status_bytes = json.dumps(status_obj, ensure_ascii=False, indent=2).encode("utf-8")
    with open(STATUS_PATH, "wb") as f:
        f.write(status_bytes)

    if put_object_r2:
        try:
            put_object_r2("line_bot_status.json", status_bytes, "application/json; charset=utf-8")
            if os.path.exists(CHAT_LOG_PATH):
                with open(CHAT_LOG_PATH, "rb") as cf:
                    put_object_r2("line_chat_logs.json", cf.read(), "application/json; charset=utf-8")
            log_msg("[R2] Synced line_bot_status.json & line_chat_logs.json to assets.siwasup.com")
        except Exception as e:
            log_msg(f"[R2 Sync Warn]: {e}")


def main():
    with open(DAEMON_LOG_PATH, "w", encoding="utf-8") as f:
        f.write("=== LINE BOT DAEMON STARTED ===\n")

    log_msg("[1/3] Starting local LINE-Gemini Webhook server on port 5005...")
    webhook_proc = subprocess.Popen(
        [sys.executable, "-u", WEBHOOK_SCRIPT],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    def stream_webhook_logs():
        for line in webhook_proc.stdout:
            log_msg(f"[WEBHOOK] {line.strip()}")

    threading.Thread(target=stream_webhook_logs, daemon=True).start()
    time.sleep(3)

    log_msg("[2/3] Starting Cloudflared Quick Tunnel -> http://127.0.0.1:5005 ...")
    cf_proc = subprocess.Popen(
        [CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:5005"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    tunnel_url = None
    for line in cf_proc.stdout:
        log_msg(f"[TUNNEL] {line.strip()}")
        m = re.search(r"(https://[a-zA-Z0-9\-]+\.trycloudflare\.com)", line)
        if m and not tunnel_url:
            tunnel_url = m.group(1)
            log_msg(f"[3/3] Captured Tunnel URL: {tunnel_url}")
            time.sleep(4)
            try:
                ok = update_line_webhook_endpoint(tunnel_url)
                log_msg(f"[LINE API] Updated Webhook Endpoint -> {ok}")
                time.sleep(2)
                test_res = {}
                try:
                    test_res = test_line_webhook_endpoint(tunnel_url)
                    log_msg(f"[LINE API] Webhook Verification Result: {test_res}")
                except Exception as te:
                    log_msg(f"[LINE API] Webhook Test Notice: {te}")
                save_and_sync_status(tunnel_url, test_res)
            except Exception as e:
                log_msg(f"[LINE API Error]: {e}")


if __name__ == "__main__":
    main()
