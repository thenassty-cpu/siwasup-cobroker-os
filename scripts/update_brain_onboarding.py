import sys

update_text = '''

==============================================================================
SESSION UPDATE: 1 พ.ย. 2569 (16:00 น.) - OFFICE ONBOARDING & STAFF REGISTRATION PORTAL
==============================================================================
1. OFFICE STAFF & AGENT REGISTRATION PORTAL (agent_registration.html):
   - สร้างและดีพลอยหน้าลงทะเบียน & เข้าสู่ระบบสำหรับทีมงานออฟฟิศและตัวแทน Co-Broker
   - URL: https://assets.siwasup.com/agent_registration.html (Status: 200 OK)
   - ฟอร์มกรอก: สังกัด (ทีมงานออฟฟิศ / Co-Broker), ชื่อ-นามสกุล, ชื่อเล่น, เบอร์โทร, โซนที่ดูแล
   - ระบบคำนวณและออก "นามบัตรดิจิทัลเฉพาะตัว (Dynamic Business Card)" ทันที พร้อมปุ่มแชร์เข้า LINE

2. DYNAMIC AGENT CARD ENGINE (agent_profile.html):
   - รองรับ Dynamic Query Parameters (?name=...&phone=...&zone=...&title=...)
   - เมื่อคนในออฟฟิศลงทะเบียนเสร็จ จะได้นามบัตรทางการที่เป็นชื่อและเบอร์ของตนเองทันที

3. LINE BOT ONBOARDING & WELCOME MESSAGE AUTOMATION (line_gemini_webhook.py):
   - รองรับ FollowEvent: เมื่อคนในออฟฟิศแอดเฟรนด์น้องศิวา จะได้รับข้อความต้อนรับ + ลิงก์ลงทะเบียนทันที
   - รองรับคีย์เวิร์ด: เมื่อพิมพ์ 'สมัคร', 'ลงทะเบียน', 'login', 'เข้าสู่ระบบ', 'นามบัตร' น้องศิวาจะส่งลิงก์ให้ทันที
   - พุชขึ้น GitHub Main และอัปเดตขึ้น Render.com Cloud เรียบร้อย 100%
==============================================================================
'''

with open(r'G:\Home_Brain_Update.txt', 'a', encoding='utf-8') as f:
    f.write(update_text)

print('Successfully appended Office Onboarding updates to G:\\Home_Brain_Update.txt')
