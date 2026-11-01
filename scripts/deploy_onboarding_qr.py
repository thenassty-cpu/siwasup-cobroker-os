import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

files_to_deploy = [
    ("agent_onboarding_qr.html", "text/html; charset=utf-8"),
    ("agent_registration.html", "text/html; charset=utf-8"),
    ("admin_lobby_manager.html", "text/html; charset=utf-8"),
    ("gool_executive_dashboard.html", "text/html; charset=utf-8"),
    ("executive_quick_hub.html", "text/html; charset=utf-8"),
]

for filename, content_type in files_to_deploy:
    path = os.path.join(WEB_DIR, filename)
    print(f"[*] Uploading {filename} to Cloudflare R2...")
    with open(path, 'rb') as f:
        data = f.read()
    st = put_object_r2(filename, data, content_type)
    print(f"[OK] {filename} Upload Status: {st}")
    print(f"URL: https://assets.siwasup.com/{filename}")

print("\n[SUCCESS] All files including Admin Lobby Manager deployed to Cloudflare R2!")
