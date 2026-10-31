import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

for fname in ["index.html", "catalog.html"]:
    fpath = os.path.join(BASE_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read().replace("\r\n", "\n")

    # Remove BAM option from dropdown
    html = re.sub(r'\s*<option value="BAM">BAM</option>', '', html)

    # Remove BAM button from quick chips
    html = re.sub(
        r'\s*<button type="button" onclick="selectBankChip\(\'BAM\', this\)"[^>]*>BAM</button>',
        '',
        html
    )

    with open(fpath, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(html)
    print(f"[OK] Removed BAM from {fname}")
