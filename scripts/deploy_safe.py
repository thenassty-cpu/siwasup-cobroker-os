import os
import sys
import re
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"


def is_valid_thai_id(digits13: str) -> bool:
    if len(digits13) != 13 or not digits13.isdigit():
        return False
    if digits13[0] in ('0', '9'):
        return False
    total = sum(int(digits13[i]) * (13 - i) for i in range(12))
    check = (11 - (total % 11)) % 10
    return check == int(digits13[12])


def pii_check(fname, data):
    text = data.decode("utf-8", errors="ignore")
    hits = []
    if re.search(r'"idCard"', text):
        hits.append('field "idCard"')
    if re.search(r'"address"\s*:\s*"[^"]{8,}', text):
        hits.append('field "address" with value')

    # Strip URLs/filenames with 13-digit timestamps (e.g. crop-1753250280224.jpg) before checking 13-digit Thai IDs
    text_no_urls = re.sub(r'https?://[^\s"\'<>]+', '', text)
    text_no_urls = re.sub(r'crop-\d{13}', '', text_no_urls)
    for m in re.finditer(r'(?<!\d)(\d{13})(?!\d)', text_no_urls):
        cand = m.group(1)
        if is_valid_thai_id(cand):
            hits.append(f'13-digit Thai National ID ({cand[:3]}...{cand[-2:]})')
            break
    return hits


def guess_ctype(fname):
    if fname.endswith(".js"):
        return "application/javascript; charset=utf-8"
    if fname.endswith(".json"):
        return "application/json; charset=utf-8"
    return "text/html; charset=utf-8"


files_to_deploy = [
    ("siwasup_viewing_flow_tester.html", "text/html; charset=utf-8"),
    ("siwasup_agents.js", "application/javascript; charset=utf-8"),
]
for a in sys.argv[1:]:
    n, _, c = a.partition("=")
    files_to_deploy.append((n, c or guess_ctype(n)))

blocked = 0
for fname, ctype in files_to_deploy:
    fpath = os.path.join(WEB_DIR, fname)
    with open(fpath, "rb") as f:
        data = f.read()
    hits = pii_check(fname, data)
    if hits:
        blocked += 1
        print(f"[BLOCKED] {fname}: possible personal data -> {', '.join(hits)} (NOT uploaded)")
        continue
    st = put_object_r2(fname, data, ctype)
    print(f"[R2] Uploaded {fname} ({len(data)} bytes) -> Status: {st}")
    if os.path.exists(G_DIR):
        shutil.copy2(fpath, os.path.join(G_DIR, fname))
        print(f"[G:\\] Mirrored {fname}")

print("=== DEPLOY DONE (blocked: %d) ===" % blocked)
