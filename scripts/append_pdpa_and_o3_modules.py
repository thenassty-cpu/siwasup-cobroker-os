import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

skill_file = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates\Skill_PropTech_Siwasup_OS.md"
home_update_file = r"G:\Home_Brain_Update.txt"
status_file = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates\00_PROJECT_STATUS.md"

content_skill = """
---

## 🔬 14. Advanced Behavioral Telemetry & PDPA Compliance Architecture (สถาปัตยกรรมดักจับพฤติกรรม & กำแพงคุ้มครอง PDPA)

### 📊 5 โมดูลตรวจจับเชิงรุก (อ้างอิงงานวิจัย Deep Research 8 หน้า):
1. **Lead Engagement & Response Tracker:**
   - Client-side Dwell Time (>30s = High-Intent) ผสาน `visibilitychange` (หยุดนับเวลาเมื่อพับแท็บจอ)
   - Speed-to-Lead: เอเจนต์โทรกลับใน 5 นาที เพิ่มโอกาสปิดการขาย 100 เท่า (หากเกินเวลาเตือนกูลเข้าแทรกแซง)
2. **Listing Hoarding & Ghost Lead Detector:**
   - ดักจับการกั๊กทรัพย์และลีดหลอก (Kakomikomi Prevention / Anti-Tragedy of the Commons)
   - กลไก Time-to-Live (TTL): ล็อกเวลาหมดอายุของการจองสิทธิ์ หากไม่มีความคืบหน้า ปลดล็อกคืนกองกลางอัตโนมัติ
   - Proof of Genuine Buyer: ตรวจสอบยืนยันตัวตนผู้ซื้อจริง
3. **Fake Lead & Bot Detection:**
   - สแกน Touch/Pointer Dynamics (เมาส์ตรงผิดปกติ, กรอกฟอร์มเร็วเหนือมนุษย์)
   - ป้องกัน Data Pollution และตัดวงจรเอเจนต์ปั่นลีดปลอม
4. **Agent Trust & Performance Scoring:**
   - กลไกทฤษฎีเกม Repeated Game สร้างสมุดพกเครดิตเอเจนต์ (Trust Score)
   - เอเจนต์คะแนนสูงได้รับ Whale Leads (ทรัพย์ 20-30 ล้าน) ก่อนใคร
5. **Form Abandonment & Exit-Intent Rescue:**
   - ดักจับลูกค้า 75% ที่เริ่มพิมพ์ข้อมูลแล้วเกิดความลังเลใจก่อนกดส่ง

---

### ⚖️ กฎเหล็ก PDPA: แก้ปัญหา "การดักจับเบอร์ที่พิมพ์ค้างไว้" ให้ถูกกฎหมาย 100%:
- **ข้อควรระวังทางกฎหมาย (PDPA มาตรา 19 & 24):**
  - เบอร์โทรศัพท์เป็นข้อมูลส่วนบุคคล (Personal Data) หากระบบแอบดักจับ (Keystroke Scraping) ก่อนที่ผู้ใช้จะกด Submit โดยไม่ได้รับความยินยอม **ถือว่าผิดกฎหมาย PDPA โทษปรับทางปกครองสูงสุด 3-5 ล้านบาท** และหากตัวแทนโทรไปหา ลูกค้าจะรู้สึกถูกละเมิดความเป็นส่วนตัว (Creepy Factor)
- **ท่าแก้เกมสากลที่ถูกต้อง 100% (The Exit-Intent Rescue Pop-up):**
  - **ห้ามดูดเบอร์เงียบๆ หลังบ้านเด็ดขาด!**
  - ให้ใช้ท่า **"Exit-Intent One-Click Consent Modal"**: เมื่อตรวจพบเคอร์เซอร์ขยับจะปิดแท็บหรือกด Back ให้เด้งป๊อปอัปช่วยเหลือแบบสุภาพทันที:
    > *"คุณกำลังสนใจ [ชื่อบ้าน] อยู่ใช่ไหมคะ? ให้เจ้าหน้าที่ส่งโปรโมชั่นส่วนลดพิเศษและคิวนัดชมให้ทาง LINE/โทรศัพท์ทันทีไหมคะ?*  
    > *[ ✅ ยินยอมให้ติดต่อกลับ ]  [ ✕ ไม่ต้องการ ]"*
  - หากลูกค้ากดปุ่มยืนยัน ➡️ ถือเป็น **Explicit Consent (ความยินยอมโดยชัดแจ้ง) ถูกกฎหมาย PDPA 100%** ทันที ไม่มีความเสี่ยงทางกฎหมาย และเอเจนต์สามารถโทรหาได้อย่างสง่างาม
- **การเก็บเชิงสถิติ (Anonymous Telemetry):**
  - ในส่วนหลังบ้าน บันทึกได้เฉพาะ Aggregate Counter เช่น "บ้านหลังนี้มีคนพิมพ์ค้างแล้วออก 12 ครั้ง" (เพื่อปรับปรุง UX ฟอร์ม โดยไม่บันทึกเลขเบอร์โทรศัพท์ของบุคคลใด)
"""

content_twin = """
7. Advanced Behavioral Telemetry & PDPA Compliance:
   - Evaluated 5 Deep Research Modules: Lead Response Tracker (Speed-to-Lead 5 mins), Listing Hoarding & TTL, Fake Lead Bot Detection, Agent Trust Score, and Exit-Intent Form Rescue.
   - CRITICAL PDPA COMPLIANCE: Capturing unsubmitted keystroke phone numbers without submission violates PDPA (Personal Data Protection Act).
   - Solution: NEVER silently scrape unsubmitted phone numbers. Use the 'Exit-Intent One-Click Consent Pop-up' asking the user explicitly if they want special discount info sent to their phone before tab close. Clicking confirms Explicit Consent (100% PDPA-compliant).
"""

with open(skill_file, 'a', encoding='utf-8') as f:
    f.write(content_skill)
print(f"[OK] Appended to {skill_file}")

if os.path.exists(home_update_file):
    with open(home_update_file, 'a', encoding='utf-8') as f:
        f.write(content_twin)
    print(f"[OK] Appended to {home_update_file}")

status_entry = """
### Update 2026-10-29 (Siwasup OS - Advanced Behavioral Telemetry & PDPA Compliance Architecture)
- **Integrated o3 Deep Research Report (8 Pages)**:
  - Formulated 5 Behavioral Telemetry Modules: Lead Engagement Tracker, Listing Hoarding TTL Engine, Fake Lead Bot Detection, Agent Trust Scoring, and Form Abandonment Rescue.
- **PDPA Legal Compliance Architecture**:
  - Addressed legal risk under PDPA Section 19/24 regarding partial form entry.
  - Standardized on 'Exit-Intent One-Click Consent Pop-up' to secure 100% Explicit Consent legally before capturing contact details.
- **Twin Brain & Skill Knowledge Synchronized**:
  - Section 14 added to `Skill_PropTech_Siwasup_OS.md` and synced to `G:\\Home_Brain_Update.txt`.
"""

with open(status_file, 'a', encoding='utf-8') as f:
    f.write(status_entry)
print(f"[OK] Appended to {status_file}")

print("=== ALL UPDATES SAVED WITH 100% PDPA COMPLIANCE ===")
