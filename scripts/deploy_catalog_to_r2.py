import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_HTML = os.path.join(WEB_DIR, "catalog.html")
CATALOG_JSON = os.path.join(WEB_DIR, "data", "catalog_index.json")

print("[*] Uploading catalog.html to Cloudflare R2...")
with open(CATALOG_HTML, 'rb') as f:
    html_bytes = f.read()

status_html = put_object_r2("catalog.html", html_bytes, "text/html; charset=utf-8")
print(f"[OK] Uploaded catalog.html! Status: {status_html}")
print("URL: https://assets.siwasup.com/catalog.html")

INDEX_HTML = os.path.join(WEB_DIR, "index.html")
print("[*] Uploading index.html to Cloudflare R2...")
with open(INDEX_HTML, 'rb') as f:
    idx_bytes = f.read()
status_idx = put_object_r2("index.html", idx_bytes, "text/html; charset=utf-8")
print(f"[OK] Uploaded index.html! Status: {status_idx}")

SW_JS = os.path.join(WEB_DIR, "sw.js")
print("[*] Uploading sw.js to Cloudflare R2...")
with open(SW_JS, 'rb') as f:
    sw_bytes = f.read()
status_sw = put_object_r2("sw.js", sw_bytes, "application/javascript; charset=utf-8")
print(f"[OK] Uploaded sw.js! Status: {status_sw}")

MODALS_JS = os.path.join(WEB_DIR, "modals.js")
print("[*] Uploading modals.js to Cloudflare R2...")
with open(MODALS_JS, 'rb') as f:
    modals_bytes = f.read()
status_modals = put_object_r2("modals.js", modals_bytes, "application/javascript; charset=utf-8")
print(f"[OK] Uploaded modals.js! Status: {status_modals}")

print("[*] Uploading catalog_index.json to Cloudflare R2...")
with open(CATALOG_JSON, 'rb') as f:
    json_bytes = f.read()

# Upload to both root and data/ for reliability
status_json1 = put_object_r2("catalog_index.json", json_bytes, "application/json; charset=utf-8")
status_json2 = put_object_r2("data/catalog_index.json", json_bytes, "application/json; charset=utf-8")
print(f"[OK] Uploaded catalog_index.json! Status: {status_json1}, {status_json2}")

print("=== DEPLOYMENT COMPLETED SUCCESSFULLY ===")
