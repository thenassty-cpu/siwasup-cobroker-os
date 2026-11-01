import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

files_to_deploy = [
    ("agent_registration.html", os.path.join(WEB_DIR, "agent_registration.html")),
    ("agent_profile.html", os.path.join(WEB_DIR, "agent_profile.html"))
]

for name, path in files_to_deploy:
    print(f"[*] Uploading {name} to Cloudflare R2...")
    with open(path, 'rb') as f:
        data = f.read()
    st = put_object_r2(name, data, "text/html; charset=utf-8")
    print(f"[OK] {name} Upload Status: {st}")
    print(f"URL: https://assets.siwasup.com/{name}")

# Now link it in executive_quick_hub.html
QUICK_HUB_HTML = os.path.join(WEB_DIR, "executive_quick_hub.html")
with open(QUICK_HUB_HTML, 'r', encoding='utf-8') as f:
    hub_content = f.read()

if "agent_registration.html" not in hub_content:
    print("\n[*] Adding registration link to executive_quick_hub.html...")
    target = '<span>📋 ยุทธศาสตร์ & บทพูดพรีเซนต์ 3 นาที</span>\n                </a>'
    reg_btn = target + """
                <a href="https://assets.siwasup.com/agent_registration.html" target="_blank" style="background: linear-gradient(135deg, #3B82F6, #1D4ED8); color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 8px 18px; border-radius: 12px; text-decoration: none; box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4); display: inline-flex; align-items: center; gap: 6px;">
                    <span>📝 ฟอร์มลงทะเบียนทีมงานออฟฟิศ & นามบัตร</span>
                </a>"""
    if target in hub_content:
        hub_content = hub_content.replace(target, reg_btn, 1)
        with open(QUICK_HUB_HTML, 'w', encoding='utf-8') as f:
            f.write(hub_content)
        put_object_r2("executive_quick_hub.html", hub_content.encode('utf-8'), "text/html; charset=utf-8")
        print("[OK] Updated quick hub deployed to R2!")

print("\n[SUCCESS] Registration Portal is fully live!")
