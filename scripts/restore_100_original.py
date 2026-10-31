import os
import re
import shutil
import sys
import mimetypes

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
sys.path.append(os.path.join(WEB_DIR, "scripts"))
from overnight_r2_crawler import put_object_r2

# 1. Restore index.html.bak to index.html and catalog.html (100% identical to original)
bak_path = os.path.join(WEB_DIR, "index.html.bak")
index_path = os.path.join(WEB_DIR, "index.html")
catalog_path = os.path.join(WEB_DIR, "catalog.html")

shutil.copyfile(bak_path, index_path)
shutil.copyfile(bak_path, catalog_path)
print("[OK] Restored index.html and catalog.html to 100% original from index.html.bak")

# 2. Find all local assets referenced in index.html, modals.js, etc.
with open(index_path, "r", encoding="utf-8") as f:
    text = f.read()

matches = re.findall(r'(?:src|href|url)\s*[=(]\s*["\']?([^"\'\s)>]+)', text)
local_refs = set()
for m in matches:
    clean = m.split('?')[0].strip("'\"")
    if not clean.startswith(('http:', 'https:', '#', 'data:', 'javascript:', '$', '{')):
        local_refs.add(clean)

# Also add known root JS & manifest files
extra_files = [
    "manifest.json",
    "siwasup_all_properties.js",
    "siwasup_agents.js",
    "modals.js",
    "vinyl_generator.js",
    "welcome_landing.html",
    "assets/siwasup_logo.svg",
    "assets/fonts/RSU_BOLD.ttf",
    "assets/fonts/RSU_Regular.ttf"
]
for ef in extra_files:
    local_refs.add(ef)

# Also include all files in assets/icons and assets/characters
for sub in ["assets/icons", "assets/characters", "assets/logos", "assets/qr"]:
    sub_dir = os.path.join(WEB_DIR, sub)
    if os.path.exists(sub_dir):
        for root, _, files in os.walk(sub_dir):
            for file in files:
                rel = os.path.relpath(os.path.join(root, file), WEB_DIR).replace("\\", "/")
                local_refs.add(rel)

print(f"[*] Found {len(local_refs)} local files to sync to R2...")

# 3. Upload index.html and catalog.html
with open(index_path, "rb") as f:
    html_bytes = f.read()

put_object_r2("index.html", html_bytes, "text/html; charset=utf-8")
put_object_r2("catalog.html", html_bytes, "text/html; charset=utf-8")
print("[OK] Uploaded 100% original index.html & catalog.html to R2")

# 4. Upload all local assets to R2
uploaded = 0
for rel_path in sorted(local_refs):
    full_path = os.path.join(WEB_DIR, rel_path.replace("/", os.sep))
    if os.path.isfile(full_path):
        mime, _ = mimetypes.guess_type(full_path)
        if not mime:
            if full_path.endswith(".svg"):
                mime = "image/svg+xml"
            elif full_path.endswith(".js"):
                mime = "application/javascript; charset=utf-8"
            elif full_path.endswith(".json"):
                mime = "application/json; charset=utf-8"
            elif full_path.endswith(".ttf"):
                mime = "font/ttf"
            else:
                mime = "application/octet-stream"
        with open(full_path, "rb") as bf:
            data = bf.read()
        put_object_r2(rel_path, data, mime)
        uploaded += 1
        print(f"  -> Uploaded: {rel_path} ({mime})")

print(f"=== COMPLETED: {uploaded} assets + index.html + catalog.html synced 100% original ===")
