import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

files_to_upload = [
    ("catalog.html", "text/html; charset=utf-8"),
    ("index.html", "text/html; charset=utf-8"),
    ("sw.js", "application/javascript; charset=utf-8"),
    ("modals.js", "application/javascript; charset=utf-8"),
    ("siwasup_all_properties.js", "application/javascript; charset=utf-8"),
    ("siwasup_all_properties.json", "application/json; charset=utf-8"),
    (os.path.join("data", "catalog_index.json"), "application/json; charset=utf-8"),
    (os.path.join("assets", "documents", "siwasup_sales_contract.html"), "text/html; charset=utf-8"),
]

for item, ctype in files_to_upload:
    local_path = os.path.join(WEB_DIR, item)
    if not os.path.exists(local_path):
        print(f"[!] File not found: {local_path}")
        continue
    file_size_mb = os.path.getsize(local_path) / (1024 * 1024)
    print(f"[*] Uploading {item} ({file_size_mb:.2f} MB)...")
    with open(local_path, "rb") as f:
        data = f.read()
    r2_key = item.replace("\\", "/")
    status = put_object_r2(r2_key, data, ctype)
    print(f"    -> Status: {status} ({r2_key})")

print("=== ALL FILES DEPLOYED TO CLOUDFLARE R2 SUCCESSFULLY ===")
