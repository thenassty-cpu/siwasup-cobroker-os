import os
import sys
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"

files_to_deploy = [
    ("property_curator.html", "text/html; charset=utf-8"),
    ("all_curation_properties.js", "application/javascript; charset=utf-8"),
    ("all_curation_properties.json", "application/json; charset=utf-8")
]

for fname, ctype in files_to_deploy:
    fpath = os.path.join(WEB_DIR, fname)
    with open(fpath, 'rb') as f:
        data = f.read()
    st = put_object_r2(fname, data, ctype)
    print(f"[R2] Uploaded {fname} ({len(data)} bytes) -> Status: {st}")
    
    if os.path.exists(G_DIR):
        dst = os.path.join(G_DIR, fname)
        shutil.copy2(fpath, dst)
        print(f"[G:\\] Mirrored {fname} -> {dst}")

print("=== CURATOR LIVE DEPLOYMENT COMPLETED ===")
