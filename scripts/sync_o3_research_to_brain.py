import os
import sys

# Paths
HOME_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates"
G_DRIVE = r"G:"
OFFY_PATH = r"G:\Offy_Brain_Update.txt"
HOME_UPDATE_PATH = r"G:\Home_Brain_Update.txt"
STATUS_FILE = os.path.join(HOME_DIR, "00_PROJECT_STATUS.md")
SKILL_PROPTECH_FILE = os.path.join(HOME_DIR, "Skill_PropTech_Siwasup_OS.md")
HANDOVER_FILE = os.path.join(HOME_DIR, "01_FROM_HOME_TO_OFFICE.txt")

RESEARCH_SUMMARY = """
### [Milestone Update: 31 Oct 2026 17:45] - ผลสรุปงานวิจัย o3 Deep Research & การปิดจุดตายสถิติตัวแทน (Lifetime Curse Solved)

1. **การแก้ปัญหา Goodhart's Law & The Lifetime Curse:**
   - พี่ต้นตั้งข้อสังเกตเรื่องสถิติ `% ดันสินเชื่อสำเร็จ 98%` ว่าหากเป็นตัวเลขสะสมตลอดชีพ จะกลายเป็น "ตราบาปติดตัวไปจนตาย" ทำให้ตัวแทนหมดไฟและปฏิเสธลูกค้าเคสยาก (เช่น อาชีพอิสระ, คนมีหนี้) เพื่อรักษาตัวเลข
   - **สูตรชนะเลิศจาก o3:** เปลี่ยนเป็น **Cumulative Positive Milestones (ยอดสะสมเชิงบวกที่มีแต่โตขึ้น)** เช่น `ดันผ่าน 50+ ราย` ไม่มีวันลด ไม่ประจานความล้มเหลว หรือหากใช้ % ต้องกำกับด้วย `รอบปี 2026 (Annual Window)` เท่านั้น

2. **สูตรทองคำ 4 ช่อง (The Ideal 4-Slot Architecture - ยาแก้ 4 ความกลัวของคนซื้อบ้าน):**
   - **ช่อง 1 (แก้กลัวโดนแอบคิดเงิน/บวกราคา):** `ค่านายหน้าผู้ซื้อ 0 บาท`
   - **ช่อง 2 (แก้กลัวกู้ไม่ผ่าน/ปลดล็อคจิตวิทยาตัวแทน):** `ช่วยกู้ผ่านแล้ว 50+ ราย`
   - **ช่อง 3 (แก้กลัวนายหน้ามือใหม่/สร้าง Trust):** `ปิดการขายสำเร็จ 45+ หลัง`
   - **ช่อง 4 (แก้กลัวทิ้งงาน/ติดต่อยาก):** `ตอบกลับเฉลี่ย 15 นาที` (SLA จากระบบ LINE Bot ชนะคู่แข่งตลาดที่เฉลี่ย 15 ชม.)
   - **Empathetic Tagline:** *"ซื้อบ้านเรื่องใหญ่ ปรึกษาเราได้ฟรี... ไม่ซื้อไม่ว่ากัน"*

3. **การอัปเกรดอัตลักษณ์แบรนด์ศิวาทรัพย์ (Red & Gold Luxury Theme):**
   - นำเข้าตราเพชรเวกเตอร์ทางการ `E:\\TON\\#Siwasub\\images\\daimond.svg` (`h-8 sm:h-9`) มาเป็นตราหลัก
   - จัดวางคู่กับชื่อบริษัท `SIWASUP` (แดงมงคล #ed2027) + `ASSET` (ดำคม)
   - ขยายชื่อตัวแทนเป็น `text-lg sm:text-xl` และลดน้ำหนักเป็น `font-medium` ไม่อึดอัด
   - วางตำแหน่ง `ที่ปรึกษาด้านการซื้อ-ขายอสังหาริมทรัพย์มืออาชีพ` ใต้ชื่อโดยตรง ไม่ใส่แคปซูล
   - ตัดแคปซูลเบอร์โทร/LINE ข้างชื่อที่ซ้ำซ้อนออก เหลือเฉพาะปุ่มใหญ่ที่ด้านล่างของการ์ด
   - เติมขอบมงกุฎบนสุดด้วย Gradient แดงมงคล-ทองคำ (`#991B1B` -> `#E5B54F` -> `#991B1B`) และขอบทองแชมเปญ

4. **สถานะการ Deploy:**
   - อัปโหลดขึ้น Cloudflare R2: `https://assets.siwasup.com/agent_profile.html` (Status 200)
   - Master Launchpad: `https://assets.siwasup.com/executive_quick_hub.html`
   - เอกสารวิจัยฉบับเต็ม 12 หน้า เซฟไว้ที่ `G:\\Siwasup_Presentation_2026\\O3_DEEP_RESEARCH_AGENT_CARD_METRICS.md`
"""

# Append to STATUS_FILE
if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    content += "\n\n" + RESEARCH_SUMMARY
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated 00_PROJECT_STATUS.md")

# Append to SKILL_PROPTECH_FILE
if os.path.exists(SKILL_PROPTECH_FILE):
    with open(SKILL_PROPTECH_FILE, "r", encoding="utf-8") as f:
        skill_content = f.read()
    skill_content += "\n\n## 16. o3 Deep Research & The 4-Slot Metric Architecture (Lifetime Curse Resolution)\n" + RESEARCH_SUMMARY
    with open(SKILL_PROPTECH_FILE, "w", encoding="utf-8") as f:
        f.write(skill_content)
    print("Updated Skill_PropTech_Siwasup_OS.md")

# Append to HANDOVER_FILE
if os.path.exists(HANDOVER_FILE):
    with open(HANDOVER_FILE, "r", encoding="utf-8") as f:
        handover = f.read()
    handover += "\n\n" + RESEARCH_SUMMARY
    with open(HANDOVER_FILE, "w", encoding="utf-8") as f:
        f.write(handover)
    print("Updated 01_FROM_HOME_TO_OFFICE.txt")

# Sync to G drive
if os.path.exists(G_DRIVE):
    for src, dst in [(STATUS_FILE, os.path.join(G_DRIVE, "00_PROJECT_STATUS.md")),
                     (SKILL_PROPTECH_FILE, os.path.join(G_DRIVE, "Skill_PropTech_Siwasup_OS.md")),
                     (HANDOVER_FILE, os.path.join(G_DRIVE, "01_FROM_HOME_TO_OFFICE.txt"))]:
        if os.path.exists(src):
            with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                f_out.write(f_in.read())
            print(f"Synced {os.path.basename(src)} to G: drive")
    
    # Append to Home_Brain_Update.txt
    with open(HOME_UPDATE_PATH, "a", encoding="utf-8") as f:
        f.write("\n" + "="*50 + "\n" + RESEARCH_SUMMARY + "\n")
    print(f"Appended to {HOME_UPDATE_PATH}")

print("\n=== ALL RESEARCH REPORTS & BRAIN FILES UPDATED & PERSISTED SUCCESSFULLY ===")
