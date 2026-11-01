import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
HTML_PATH = os.path.join(WEB_DIR, "siwasup_keybox_interactive_roleplay.html")

print("[*] Uploading siwasup_keybox_interactive_roleplay.html to Cloudflare R2...")
with open(HTML_PATH, 'rb') as f:
    html_bytes = f.read()

status = put_object_r2("siwasup_keybox_interactive_roleplay.html", html_bytes, "text/html; charset=utf-8")
print(f"[OK] Upload status: {status}")
print("URL: https://assets.siwasup.com/siwasup_keybox_interactive_roleplay.html")
