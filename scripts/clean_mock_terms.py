import os

files_to_clean = [
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\executive_quick_hub.html",
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\admin_dashboard.html",
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\squad_hub_system.html"
]

for p in files_to_clean:
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    c = c.replace("ตัวจำลองขอกุญแจ 7 สเต็ป", "ระบบขอรหัสกุญแจ OTP 7 สเต็ป")
    c = c.replace("ตัวจำลอง (Sandbox)", "ระบบทดสอบ (Sandbox)")
    c = c.replace("ตัวจำลอง Flow ขอกุญแจ", "ระบบขอรหัสกุญแจ OTP")
    if c != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Cleaned mock wording in: {os.path.basename(p)}")

print("Done cleaning mock terms.")
