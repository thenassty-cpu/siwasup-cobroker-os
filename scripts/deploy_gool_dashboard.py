import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
DASH_PATH = os.path.join(WEB_DIR, "gool_executive_dashboard.html")

print("[*] Uploading gool_executive_dashboard.html to Cloudflare R2...")
with open(DASH_PATH, 'rb') as f:
    data = f.read()

st = put_object_r2("gool_executive_dashboard.html", data, "text/html; charset=utf-8")
print(f"[OK] Upload Status: {st}")
print(f"URL: https://assets.siwasup.com/gool_executive_dashboard.html")
