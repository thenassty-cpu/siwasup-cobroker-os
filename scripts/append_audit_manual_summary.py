import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

skill_file = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates\Skill_PropTech_Siwasup_OS.md"
home_update_file = r"G:\Home_Brain_Update.txt"

content_skill = """
### 🛡️ Exclusive Listing Integrity & Circumvention Audit Playbook (คู่มือคุ้มครองสัญญาปิด):
- **เอกสารอ้างอิง:** `EXCLUSIVE_LISTING_AUDIT_MANUAL.md` (อยู่ใน Repo และ `G:\\Siwasup_Presentation_2026\\`)
- **วัตถุประสงค์:** ป้องกันเคสตัวแทนใช้แพลตฟอร์มเป็นทางผ่านเพื่อแอบปิดขายนอกระบบ แล้วอ้างว่า "เจ้าของขายเอง"
- **5 เสาหลักการป้องกันแบบมืออาชีพ (ไม่ใช้การข่มขู่ แต่ใช้พยานหลักฐาน):**
  1. **Contractual Protection:** ข้อสัญญาปิด ป.พ.พ. ระยะคุ้มครอง (Protection Period 6-12 เดือน) ครอบคลุมผู้ซื้อที่เคยรับข้อมูลผ่านบริษัท
  2. **Digital Chain of Custody:** รอยเท้าดิจิทัล QR ไวนิล, บันทึกการขอเบิกกุญแจ NPA, GPS Geofencing 100 เมตร
  3. **Behavioral Anomaly Flags:** สัญญาณเตือน `[Flag-A: High-Activity Sudden Delist]` (คนดูเยอะ เบิกกุญแจแล้ว แต่อ้างยกเลิกใน 7-14 วัน)
  4. **The Courteous Audit Call:** โทรหาเจ้าของบ้านในนาม "ฝ่ายดูแลความพึงพอใจลูกค้า" แสดงความยินดีที่บ้านขายได้ เพื่อให้เจ้าของบ้านเอ่ยชื่อผู้ซื้อจริงออกมาอย่างเป็นธรรมชาติ
  5. **Friendly Resolution:** เปิดทางลงให้ตัวแทนถือว่า "ลืมส่งเอกสารเบิกจ่าย" มากกว่าเจตนาทุจริต เพื่อเก็บรักษาความสัมพันธ์ทีม
"""

content_twin = """
6. Exclusive Listing Integrity SOP (Circumvention Audit Playbook):
   - Created `EXCLUSIVE_LISTING_AUDIT_MANUAL.md` for internal dispute prevention without aggressive threats.
   - 5 Pillars: Contractual Protection Period (6-12 mos), Digital Footprint (QR/GPS/Key log), Behavioral Anomaly Flags (High-Activity Sudden Delist), Courteous Service Audit Call to property owner, and Cadastral cross-check.
   - Escalation: Uses "Friendly Notice" (assuming agent forgot to submit billing report) to maintain team harmony while securing 50/50 co-broker commission.
"""

with open(skill_file, 'a', encoding='utf-8') as f:
    f.write(content_skill)
print(f"[OK] Appended to {skill_file}")

if os.path.exists(home_update_file):
    with open(home_update_file, 'a', encoding='utf-8') as f:
        f.write(content_twin)
    print(f"[OK] Appended to {home_update_file}")

print("=== AUDIT MANUAL SUMMARY RECORDED SUCCESSFULLY ===")
