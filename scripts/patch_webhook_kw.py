file_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

old_line = "if any(k in text_clean for k in ['สมัคร', 'ลงทะเบียน', 'login', 'เข้าสู่ระบบ', 'ขอนามบัตร', 'นามบัตร', 'โปรไฟล์', 'profile']):"
new_line = "if any(k in text_clean for k in ['สมัคร', 'ลงทะเบียน', 'login', 'เข้าสู่ระบบ', 'ขอนามบัตร', 'นามบัตร', 'โปรไฟล์', 'profile', 'เอเจนต์', 'เอเจน', 'ตัวแทน', 'ร่วมงาน', 'ขอเข้ากลุ่ม', 'เข้ากลุ่ม', 'นายหน้า', 'co-broker', 'cobroker', 'ขอลิงก์', 'ขอลิงค์', 'วิธีสมัคร', 'อยากเป็นเอเจนต์', 'ลิงก์สมัคร']):"

assert old_line in text, "old_line not found"
text = text.replace(old_line, new_line, 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated line_gemini_webhook.py successfully!")
