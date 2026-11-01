import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
STRATEGY_HTML = os.path.join(WEB_DIR, "executive_launch_strategy_horizon1.html")
QUICK_HUB_HTML = os.path.join(WEB_DIR, "executive_quick_hub.html")

print("[*] Deploying executive_launch_strategy_horizon1.html to Cloudflare R2...")
with open(STRATEGY_HTML, 'rb') as f:
    strategy_bytes = f.read()

status1 = put_object_r2("executive_launch_strategy_horizon1.html", strategy_bytes, "text/html; charset=utf-8")
print(f"[OK] Strategy Deck Upload Status: {status1}")
print("URL: https://assets.siwasup.com/executive_launch_strategy_horizon1.html")

# Link it in executive_quick_hub.html
with open(QUICK_HUB_HTML, 'r', encoding='utf-8') as f:
    hub_content = f.read()

if "executive_launch_strategy_horizon1.html" not in hub_content:
    print("[*] Injecting strategy link into executive_quick_hub.html...")
    target = '<span>🚀 เปิดทดสอบสด (Live Sandbox)</span>\n                </a>'
    replacement = target + """
                <a href="https://assets.siwasup.com/executive_launch_strategy_horizon1.html" target="_blank" style="background: linear-gradient(135deg, #10B981, #059669); color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 8px 18px; border-radius: 12px; text-decoration: none; box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4); display: inline-flex; align-items: center; gap: 6px;">
                    <span>📋 ยุทธศาสตร์ & บทพูดพรีเซนต์ 3 นาที</span>
                </a>"""
    if target in hub_content:
        hub_content = hub_content.replace(target, replacement, 1)
        with open(QUICK_HUB_HTML, 'w', encoding='utf-8') as f:
            f.write(hub_content)
        print("[*] Uploading updated executive_quick_hub.html to Cloudflare R2...")
        status2 = put_object_r2("executive_quick_hub.html", hub_content.encode('utf-8'), "text/html; charset=utf-8")
        print(f"[OK] Quick Hub Upload Status: {status2}")
    else:
        print("[!] Target marker not found in quick hub, uploading strategy only.")

print("\n[ALL DONE] Horizon 1 Executive Deck is live!")
