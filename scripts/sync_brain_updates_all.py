# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime

HOME_BRAIN_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates"
G_BRAIN_DIR = r"G:"

# 1. Update 00_PROJECT_STATUS.md
status_entry = """
* **[31/10/2569 16:50] พัฒนา Mobile Quick Test Bar (แถบแดงบน Hub) + นามบัตร Alpha Squircle 37px + Golden Emblem ครบชุด ขึ้น R2 สำเร็จ 100% 🏆**
  * **โจทย์:** พี่ต้นเปิดเทสระบบบนมือถือแล้วพบว่าการส่งลิงก์เข้า LINE แชททำให้ประวัติข้อความดันลิงก์หาย หาลิงก์เก่ายาก และหน้าจอมือถือของนามบัตรตัวแทนสัดส่วนผิดเพี้ยน
  * **การส่งมอบ & แก้ไข:**
    1. **แถบสีแดงทดสอบด่วน (🔴 ACTIVE TEST ZONE):** ปักหมุดไว้บนสุดของ https://assets.siwasup.com/executive_quick_hub.html ล้อมกรอบแดงชัดเจน รวมลิงก์ทดสอบ 1-Click สำหรับเปิดบนมือถือ (นามบัตร 6 Alpha, ตัวเลือก 3 แบบให้กูลเคาะ, ตารางคะแนนไลท์โหมด, น้องศิวา AI) จบในที่เดียว ไม่ต้องก๊อปลิงก์ลง LINE
    2. **นามบัตรดิจิทัล Alpha (`agent_profile.html`):**
       - ปรับรูปโปรไฟล์เป็น Squircle ขอบมน 37px (`border-radius: 37px;`) ตรงตามไฟล์ Adobe Illustrator เป๊ะ
       - จัดเลย์เอาต์แนวนอน (Horizontal Side-by-Side) บนมือถือ รูปอยู่ซ้าย ข้อมูลอยู่ขวา ไม่หลุดไปซ้อนแนวตั้ง
       - ตัดคำว่า 'โทร' ออก เหลือเพียงเลข 10 หลักเว้นวรรคสวยงาม เช่น `096 645 8994`
       - เปลี่ยนมาใช้ **Golden Emblem** เวกเตอร์ทองทางการจาก `E:\\TON\\#Siwasub\\images\\Golden Emblem\\Golden__001_Folder` (สร้าง `Golden__001_lion.png` เพิ่มเติมให้ครบชุด 6 สัตว์)
       - ระบบแยกมุมมองภายใน (เห็นเหรียญทอง 3D) กับมุมมองลูกค้า (ซ่อนสัตว์ 100% เหลือเฉพาะป้ายทองทางการ)
       - ตัดเรตติ้งดาวแบบเปิดออก เพื่อป้องกันคู่แข่งหรือคนไม่หวังดีแกล้งกดตัดคะแนน
    3. **Deploy & Sync:** ขึ้น Cloudflare R2 (HTTP 200) + สำรองลง G:\\Siwasup_Presentation_2026\\ เรียบร้อย 100%
"""

status_path = os.path.join(HOME_BRAIN_DIR, "00_PROJECT_STATUS.md")
if os.path.exists(status_path):
    with open(status_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    target_header = "## 🟢 1. COMPLETED / ส่งมอบและปิดจ๊อบแล้ว (Done)"
    if target_header in content and "[31/10/2569 16:50]" not in content:
        content = content.replace(target_header, target_header + "\n" + status_entry)
        with open(status_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated 00_PROJECT_STATUS.md")

# 2. Update Skill_PropTech_Siwasup_OS.md
skill_entry = """
---

## 📱 15. Mobile Quick-Test Zone Architecture & Frictionless Feedback Loops

### 🎯 The "Single Bookmark Hub" Principle:
- **Pain Point:** การก็อปปี้ลิงก์ทดสอบส่งเข้า LINE แชท เมื่อมีการอัปเดตต่อเนื่อง ลิงก์ใหม่จะดันลิงก์เก่าหาย ทำให้เวลาเปิดทดสอบบนมือถือหาลิงก์ไม่เจอและเสียสมาธิ
- **Architecture Solution:** 
  - สร้างแถบ **🔴 ACTIVE TEST ZONE (ทดสอบเรื่องนี้)** ล้อมกรอบแดงเด่นชัด ปักหมุดไว้ที่ตำแหน่งบนสุดของ `executive_quick_hub.html`
  - ทำปุ่ม Tap ทางลัดขนาดใหญ่ระดับนิ้วโป้งแตะสะดวก (Min Touch Target 44px) รวบรวมทุกตัวแปรที่กำลังทดสอบ (เช่น รหัสตัวแทน S98, S120, S117, S90, มุมมองลูกค้า, ตัวเลือก 3 แบบ)
  - ผู้บริหาร Bookmark ลิงก์เดียว: `https://assets.siwasup.com/executive_quick_hub.html` ก็เข้าถึงงานอัปเดตล่าสุดได้ทันทีโดยไม่ต้องค้นแชท

### 🎨 Illustrator-to-Web Fidelity Rules (Squircle & Minimalist UI):
1. **Squircle Border Radius (37px):**
   - เมื่อ Designer ออกแบบ Round Corners ใน Adobe Illustrator กำหนด 37px ใน CSS ต้องใช้ `.squircle-37 { border-radius: 37px; }` หรือเทียบเท่า เพื่อรักษาสัดส่วนความโค้งมนอันเป็นเอกลักษณ์ (ห้ามใช้ `rounded-full` หรือ `rounded-2xl` ดาดๆ)
2. **Horizontal Side-by-Side on Mobile:**
   - การ์ดโปรไฟล์ตัวแทนต้องล็อกเลย์เอาต์ให้รูปโปรไฟล์อยู่ซ้าย และชื่อ/ข้อมูลอยู่ขวาเสมอ (ห้ามปล่อยให้ flex-col ซ้อนแนวตั้งบนมือถือ เพราะจะทำให้การ์ดยืดยาวและเสียความน่าเชื่อถือ)
3. **No Redundant "โทร" Label:**
   - สำหรับเบอร์โทรศัพท์ 10 หลัก ไม่ต้องใส่คำว่า "โทร" เพราะผู้ใช้เห็นไอคอนหูโทรศัพท์และตัวเลข 10 หลักที่มีการเว้นวรรค (`096 645 8994`) ก็เข้าใจได้ทันที ช่วยลดความรกรุงรังของหน้าจอ
4. **Golden Emblem Vector System:**
   - ใช้ภาพเวกเตอร์เหรียญทองทางการ (`Golden__001_*.png`) แทนภาพ 3D สัตว์ เพื่อคงความน่าเชื่อถือระดับสถาบัน
   - กฎเหล็ก: เมื่อแชร์ลิงก์ให้ลูกค้า (`?mode=client`) ต้องซ่อนรูปสัตว์ทั้งหมด 100% คงไว้เฉพาะแถบสีทอง `✦ Senior Property Advisor`

### 🛡️ Anti-Trolling & Trust Matrix:
- ห้ามทำระบบให้ดาวรีวิวแบบเปิด (Public 5-Star Rating) เพราะเสี่ยงต่อการโดนคู่แข่งหรือผู้ไม่ประสงค์ดีกด 1 ดาวกลั่นแกล้ง
- เปลี่ยนมาใช้ตัวเลขผลงานจริงที่พิสูจน์ได้ เช่น **"ปิดสำเร็จ 45+ หลัง"** และ **"ดันสินเชื่อผ่าน 98%"** ซึ่งสร้างความมั่นใจให้ผู้ซื้อบ้านได้ตรงจุดกว่า
"""

skill_path = os.path.join(HOME_BRAIN_DIR, "Skill_PropTech_Siwasup_OS.md")
if os.path.exists(skill_path):
    with open(skill_path, "r", encoding="utf-8") as f:
        skill_content = f.read()
    if "15. Mobile Quick-Test Zone Architecture" not in skill_content:
        with open(skill_path, "a", encoding="utf-8") as f:
            f.write(skill_entry)
        print("Updated Skill_PropTech_Siwasup_OS.md")

# 3. Update 01_FROM_HOME_TO_OFFICE.txt
handover_entry = """
==============================================================================
[2026-10-31 16:55] Home Session Handover (hai -> Offy): Siwasup OS Alpha Agent Card & Mobile Hub
==============================================================================
1. SIWASUP AGENT DIGITAL PROFILE CARD (agent_profile.html):
   - พัฒนานามบัตรดิจิทัลสำหรับ 6 ขุนพล Alpha (S98, S120, S117, S90, S94, S113)
   - ดึงรูปโปรไฟล์จาก LINE อัตโนมัติ พร้อมระบบ Smart Preview กดยืนยันรูป
   - กรอบรูปทรง Squircle ขอบมน 37px ตามไฟล์ Illustrator (Corners: 37px)
   - จัดเลย์เอาต์แนวนอนบนมือถือ (Horizontal Side-by-Side) ไม่ตกแต่งแนวตั้ง
   - ตัดคำว่า 'โทร' ออก แสดงเลข 10 หลักเว้นวรรค เช่น 096 645 8994
   - เชื่อมต่อ Golden Emblem จากโฟลเดอร์ E:\\TON\\#Siwasub\\images\\Golden Emblem\\Golden__001_Folder ครบ 6 สัตว์
   - กฎเหล็กการแชร์ลูกค้า: ซ่อนชื่อ/รูปสัตว์ 100% ลูกค้าเห็นเฉพาะป้ายทองทางการ 'Senior Property Advisor'
   - ระบบสลับ 3 ตัวเลือกตัวเลข (แบบ 1 สบายใจ/กู้ผ่าน, แบบ 2 โปร/ตอบไว, แบบ 3 ปรับคำซอฟต์) พร้อมตัดเรตติ้งดาวกันการแกล้งรีวิว

2. EXECUTIVE QUICK LAUNCH HUB (executive_quick_hub.html):
   - เพิ่มแถบสีแดงด้านบนสุด '🔴 ACTIVE TEST ZONE' รวมลิงก์ทดสอบด่วนบนมือถือ 1-Click
   - ไม่ต้องก๊อปลิงก์ลง LINE แชทให้ประวัติดันหาย เปิดหน้าเดียวทดสอบได้ครบทุกโมดูล

3. DEPLOYMENT & SYNC:
   - อัปโหลดขึ้น Cloudflare R2 (https://assets.siwasup.com/) เรียบร้อย 100%
   - ซิงก์สำรองลง Flash Drive G:\\ เรียบร้อย
==============================================================================
"""

handover_path = os.path.join(HOME_BRAIN_DIR, "01_FROM_HOME_TO_OFFICE.txt")
if os.path.exists(handover_path):
    with open(handover_path, "a", encoding="utf-8") as f:
        f.write(handover_entry)
    print("Updated 01_FROM_HOME_TO_OFFICE.txt")

# 4. Sync to G: drive
if os.path.exists(G_BRAIN_DIR):
    for fname in ["00_PROJECT_STATUS.md", "Skill_PropTech_Siwasup_OS.md", "01_FROM_HOME_TO_OFFICE.txt"]:
        src_f = os.path.join(HOME_BRAIN_DIR, fname)
        dst_f = os.path.join(G_BRAIN_DIR, fname)
        if os.path.exists(src_f):
            shutil.copy2(src_f, dst_f)
            print(f"Synced {fname} to G: drive")
            
    # Also append to G:\Home_Brain_Update.txt
    home_update_f = os.path.join(G_BRAIN_DIR, "Home_Brain_Update.txt")
    with open(home_update_f, "a", encoding="utf-8") as f:
        f.write(handover_entry)
    print("Appended to G:\\Home_Brain_Update.txt")

print("\n=== ALL BRAIN & SKILL FILES UPDATED & SYNCED SUCCESSFULLY ===")
