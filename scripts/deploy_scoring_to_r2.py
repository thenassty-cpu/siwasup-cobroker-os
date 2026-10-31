import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

files_to_deploy = [
    ("scoring_summary_light.html", "text/html; charset=utf-8"),
    ("scoring_debate_dashboard.html", "text/html; charset=utf-8"),
    ("executive_quick_hub.html", "text/html; charset=utf-8")
]

for fname, ctype in files_to_deploy:
    fpath = os.path.join(WEB_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, 'rb') as f:
            data = f.read()
        st = put_object_r2(fname, data, ctype)
        print(f"[R2 Upload] {fname} ({len(data):,} bytes) -> Status: {st}")
    else:
        print(f"[Skip] File not found: {fname}")

print("\n=== DEPLOYMENT TO assets.siwasup.com FINISHED ===")
