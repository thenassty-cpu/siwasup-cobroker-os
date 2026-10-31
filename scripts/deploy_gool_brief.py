import os
import sys
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"

fname = "gool_anti_hoarding_brief.html"
fpath = os.path.join(WEB_DIR, fname)

with open(fpath, 'rb') as f:
    data = f.read()

st = put_object_r2(fname, data, "text/html; charset=utf-8")
print(f"[R2] Uploaded {fname} ({len(data)} bytes) -> Status: {st}")

if os.path.exists(G_DIR):
    dst = os.path.join(G_DIR, fname)
    shutil.copy2(fpath, dst)
    print(f"[G:\\] Mirrored {fname} -> {dst}")

print("=== GOOL BRIEF DEPLOYED SUCCESSFULLY ===")
