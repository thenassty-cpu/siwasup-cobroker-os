file_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\executive_quick_hub.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find('agent_registration.html')
if pos != -1:
    end_pos = content.find('</a>', pos)
    if end_pos != -1:
        new_buttons = '''
                <a href="https://assets.siwasup.com/agent_onboarding_qr.html" target="_blank" style="background: linear-gradient(135deg, #10B981, #047857); color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 8px 18px; border-radius: 12px; text-decoration: none; box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4); display: inline-flex; align-items: center; gap: 6px;">
                    <span>📲 ป้ายสแกน QR หน้างาน (Tent Card)</span>
                </a>
                <a href="https://assets.siwasup.com/gool_executive_dashboard.html" target="_blank" style="background: linear-gradient(135deg, #F59E0B, #B45309); color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 8px 18px; border-radius: 12px; text-decoration: none; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4); display: inline-flex; align-items: center; gap: 6px;">
                    <span>👑 แดชบอร์ดกูล & บัว (Single-Page)</span>
                </a>'''
        content = content[:end_pos+4] + new_buttons + content[end_pos+4:]
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Inserted QR and Dashboard links into executive_quick_hub.html successfully!")
    else:
        print("End tag not found")
else:
    print("agent_registration.html not found")
