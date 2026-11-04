# -*- coding: utf-8 -*-
import os, sys

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

shutdown_code = """import signal

def handle_render_shutdown(signum, frame):
    print(f"[*] Received shutdown signal ({signum}) from Render. Flushing all data to Cloudflare R2 before sleep...")
    try:
        if put_object_r2:
            with LOG_LOCK:
                store = load_chat_logs()
                data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
                put_object_r2("data/line_chat_logs.json", data_bytes, "application/json; charset=utf-8")
                print("[+] Chat logs successfully flushed to Cloudflare R2 before sleep!")
            with CONTRACTS_LOCK:
                c_store = load_contracts_data()
                c_bytes = json.dumps(c_store, ensure_ascii=False, indent=2).encode("utf-8")
                put_object_r2(_R2_CONTRACTS_VAULT_KEY, c_bytes, "application/json")
                print("[+] Exclusive contracts vault flushed to Cloudflare R2 before sleep!")
    except Exception as e:
        print(f"[-] Error during pre-sleep flush: {e}")
    sys.exit(0)

try:
    signal.signal(signal.SIGTERM, handle_render_shutdown)
    signal.signal(signal.SIGINT, handle_render_shutdown)
except Exception:
    pass
"""

target = "def run_server():"
if "def handle_render_shutdown" not in content and target in content:
    content = content.replace(target, shutdown_code + "\n\n" + target)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[+] Successfully added graceful shutdown handler to line_gemini_webhook.py!")
else:
    print("[!] Already present or target not found.")
