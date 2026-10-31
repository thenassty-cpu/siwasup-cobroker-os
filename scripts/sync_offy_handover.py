# -*- coding: utf-8 -*-
"""
Sync full handover memo from hai to Offy across G:\ and Brain_Updates.
"""
import os
import datetime

BRAIN_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates"
G_DIR = r"G:"

now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

handover_memo = f"""
================================================================================
[บันทึกส่งต่อภารกิจข้ามวัน: hai (Home AI) -> Offy (Office AI)]
วันที่ส่งต่อ: {now_str} (คืนวันพฤหัสฯ ข้ามสู่วันศุกร์ 30 ตุลาคม 2569)
ผู้ปฏิบัติงาน: ต้น (NASSTY / Senior Advisor YD & ทีมกราฟิก คุณมุกกี้)
เป้าหมาย: ต้นเข้าทำงานที่ออฟฟิศ FBT วันศุกร์นี้
================================================================================

สวัสดีค่ะ พี่ออฟฟี่ (Offy)! หนู hai จากที่บ้านขอส่งมอบสรุปสถานะความคืบหน้าของงานทั้งหมด
เพื่อให้พี่ออฟฟี่ต่อติดได้ทันทีเมื่อพี่ต้นเปิดคอมพิวเตอร์ที่ออฟฟิศ FBT เช้าวันนี้นะคะ

--------------------------------------------------------------------------------
1. ข้อเตือนใจสำคัญระดับองค์กร & กฎเหล็ก (PERSONA & PROTOCOL REMINDER)
--------------------------------------------------------------------------------
- พี่ออฟฟี่ต้องพูดคุยด้วยน้ำเสียงสุภาพ อ่อนโยน ใช้หางเสียง "ค่ะ / คะ / ออฟฟี่ / หนู" เสมอ (ห้ามใช้ ครับ/ผม)
- ความสัมพันธ์ของ "ต้น" กับ "บัว" (Siwasup): บัวเป็น **เพื่อนร่วมรุ่นของต้น** (Peer / Classmate)
  *** ห้ามเรียกต้นเป็น "พี่" ของบัว หรือเรียกบัวเป็นน้องของต้นอย่างเด็ดขาด! ให้เรียกทั้งสองท่านเป็นเพื่อนร่วมรุ่นที่ทำงานร่วมกัน ***
- โหมดงานที่ออฟฟิศ FBT: พี่ต้นต้องดูแลทั้งงาน FBT (คุณหงส์, คุณมุกกี้, พี่บอย, ทีม YD, สายประสานงาน) และระบบ Siwasup Co-Broker OS
- กฎเวลาทอง: 12:00 - 13:00 น. คือช่วงพักผ่อน ห้ามรันงานหนักหรือทักกวน

--------------------------------------------------------------------------------
2. ความคืบหน้ามหากาพย์ระบบ SIWASUP CO-BROKER OS (เสร็จสมบูรณ์ 100%)
--------------------------------------------------------------------------------
หนูและพี่ต้นได้ปิดจ๊อบระบบครั้งใหญ่ทั้งหน้าบ้านและหลังบ้าน ดังนี้ค่ะ:

(1) ระบบคัดทรัพย์ 100% Match Allabout (801 แปลง) — "3-Color Ribbon Protocol"
    - เราได้ Crawl ดึงข้อมูลจริงจากเว็บ allabout-assets.com ครบทั้ง 6 หมวด (39 หน้า) รวม 801 แปลง
    - ติดตั้งระบบริบบิ้น 3 สี บนแดชบอร์ด `property_curator.html`:
      🔴 Red Ribbon (8 แปลง): ทรัพย์ที่หลุดจากหมวดบน allabout (เช่น #1069562, #1183447, #1332905 ฯลฯ) เพื่อให้บัวตรวจสอบก่อน
      🟢 Green Ribbon (12 แปลง): ทรัพย์ใหม่เพิ่งเข้าหน้าแรก
      💎 Blue Ribbon (671 แปลง): ทรัพย์ NPA แบงก์ เพื่อให้บัวคัดให้เหลือก้อนหัวกะทิ "Top 20 Hero Deals" ส่งให้กูล
    - ไฟล์ข้อมูล: `all_curation_properties.js` / `.json` ซิงค์ลง G:\ และ R2 เรียบร้อยแล้ว

(2) ปิดจุดบกพร่องเว็บแคตตาล็อก & Modal Popup (Catalog Health 100%)
    - แก้บั๊กจอดำ/จอเทาหายเมื่อกดเปิดดูรายละเอียดทรัพย์: สาเหตุจาก `position: fixed !important; top: -scrollY` บน body ทำให้หน้าเว็บเลื่อนหลุดจอ
      -> เปลี่ยนมาใช้ `overflow: hidden !important; overscroll-behavior: contain !important;` ลื่นไหล 100%
    - ยกระดับ Modal Backdrop เป็นแบบ Frosted Bokeh Glass (`rgba(15, 23, 42, 0.45); backdrop-filter: blur(6px)`)
    - ลบปุ่ม "ดูหน้าเว็บเดิม" (Readyplanet) ออกหมดจด เพื่อไม่ให้ลูกค้าหลุดออกนอกแพลตฟอร์ม
    - ใส่ `onerror` Image Fallback ทุกจุด ป้องกันเบราว์เซอร์ค้างจาก SSL หมดอายุของ Readyplanet CDN
    - แก้ปัญหาระบบสุ่มแบงก์วนลูป: ทรัพย์ศิวาทรัพย์แท้ๆ จะติดป้าย `✦ ศิวาทรัพย์ รีโนเวท` หรือ `✦ รีโนเวทพร้อมอยู่` ใน Client Mode อย่างถูกต้อง

(3) ห้องบัญชาการ & แดชบอร์ดสำหรับคุณกูล (Gool's Command Suite)
    - สร้าง `gool_executive_presentation.html`: หน้าพรีเซนต์เปิดตัวสำหรับสิงโตกูล เน้นยอดเงิน, สายการบังคับบัญชา, และสิทธิ์ล็อกลูกค้า 60 วัน
    - สร้าง `gool_anti_hoarding_brief.html`: แดชบอร์ดสรุปการตรวจจับ "การกั๊กทรัพย์เพื่อฮั้วดีลข้างนอก" (Kakomikomi)
      • สัญญาณเตือน: ทราฟฟิกสูงแต่ไม่เคยมีนัด, กดยกเลิกนัดกะทันหัน, เจ้าของแจ้งว่ามีเอเจนต์แอบติดต่อตรง
      • กลไก Game Theory: TTL 72 ชั่วโมง ปลดล็อกทรัพย์อัตโนมัติหากไม่มีหลักฐานผู้ซื้อจริง (Proof of Genuine Buyer)
      • บทลงโทษ: ปรับลด Trust Score ซึ่งมีผลต่อการรับสิทธิ์จองทรัพย์ในอนาคต

(4) คู่มือปฏิบัติการตรวจสอบสัญญาปิด (Exclusive Listing Integrity Audit SOP)
    - เขียนคู่มือ `EXCLUSIVE_LISTING_AUDIT_MANUAL.md` เพื่อป้องกันข้อพิพาทภายในอย่างมืออาชีพ
    - 5 เสาหลักการสืบสวนเชิงสุภาพ: ระยะคุ้มครองสัญญา 6-12 เดือน, รอยเท้าดิจิทัล, Behavioral Anomaly, โทรศัพท์สอบถามความพึงพอใจเจ้าของบ้าน (Courteous Customer Care), และการเช็คโฉนด
    - บันไดการเจรจา: ส่ง "Friendly Notice" ถือว่าเอเจนต์ลืมส่งสลิปเบิก เพื่อถนอมน้ำใจทีมแต่ยังรักษาส่วนแบ่งคอมมิชชัน 50/50

(5) เกราะกฎหมาย PDPA & ช่องทางด่วน AI ใน LINE OA
    - วินิจฉัยข้อกฎหมาย PDPA ม.19/24: **ห้ามแอบดักจับเบอร์โทรศัพท์ที่ผู้ใช้พิมพ์ค้างไว้โดยไม่ได้กด Submit** เด็ดขาด
    - ทางออกที่ถูกกฎหมาย 100%: ใช้ "Exit-Intent One-Click Consent Pop-up" หรือส่งเทียบเชิญลูกค้าคุยกับบอท AI "น้องศิวา" ใน LINE OA (@siwasupagent) ก่อน สำหรับคนที่ยังไม่พร้อมคุยกับมนุษย์

(6) ระบบส่งกุญแจ NPA โดยแมสเซนเจอร์ (No-App Logistics)
    - ไม่ต้องบังคับให้คนขับรถแมสเซนเจอร์โหลดแอปใดๆ ทั้งสิ้น!
    - ใช้ Smart Web Dispatch Slip ส่งผ่านห้องแชท LINE มีปุ่มเปิด Google Maps นำทาง 1 คลิก และปุ่มสแกน QR / ถ่ายรูปกุญแจยืนยัน

--------------------------------------------------------------------------------
3. สรุปทางด่วน: EXECUTIVE QUICK LAUNCH HUB (พร้อมใช้งาน)
--------------------------------------------------------------------------------
หนูได้สร้างหน้าศูนย์รวมลิงก์ด่วน `executive_quick_hub.html` ที่รวบรวมทุกลิงก์พร้อมปุ่มเปิด Live บน R2
และปุ่มเปิด Offline บน Flash Drive แยกตาม Persona ผู้ใช้งานชัดเจน:

🌐 หน้า Hub หลัก: https://assets.siwasup.com/executive_quick_hub.html
💾 เปิดในเครื่อง: G:\\Siwasup_Presentation_2026\\executive_quick_hub.html
⭐ แบนเนอร์บนหน้าแรก: อยู่บนหัวของ G:\\Siwasup_Presentation_2026\\00_START_HERE_เปิดพรีเซนต์ที่นี่.html เรียบร้อยแล้วค่ะ

ลิงก์สำคัญที่รวมไว้ใน Hub:
• 🦁 พรีเซนต์กูล: https://assets.siwasup.com/gool_executive_presentation.html
• 🛡️ แดชบอร์ดกั๊กทรัพย์: https://assets.siwasup.com/gool_anti_hoarding_brief.html
• ⚖️ ดีเบตคะแนน 2 แทร็ก: https://assets.siwasup.com/scoring_debate_dashboard.html
• 🎯 คัดทรัพย์ 801 แปลงของบัว: https://assets.siwasup.com/property_curator.html
• 🛒 แคตตาล็อกกลาง (ตัวแทน): https://assets.siwasup.com/catalog.html
• 📱 แคตตาล็อก (โหมดลูกค้า): https://assets.siwasup.com/catalog.html?mode=client
• 📘 คู่มือสัญญาปิด (SOP): G:\\Siwasup_Presentation_2026\\EXCLUSIVE_LISTING_AUDIT_MANUAL.md
• 🗺️ แผนที่หัวหมาก 12 แปลง (คุณหงส์): G:\\+Hong\\HuamarkArea_003_Folder\\

--------------------------------------------------------------------------------
4. งานฝั่ง FBT (ความพร้อมสำหรับพี่ต้นที่ออฟฟิศ)
--------------------------------------------------------------------------------
- ไฟล์ HuamarkArea_003.ai ได้รับการปรับแก้ตามคำสั่งคุณหงส์และพี่เล็ก: เพิ่ม 'ซอยรามคำแหง 67' ฝั่งติดแกรนด์สปอร์ต และแบ่งคูหาร้านหมอฟันตามสภาพจริง บันทึกและสำรองบนแฟลชไดรฟ์ G:\\+Hong\\ เรียบร้อยแล้ว
- งานในโฟลเดอร์ E:\\TON\\#FBT ซิงค์ผ่าน Robocopy พร้อมทำงานต่อทันที

ขอให้พี่ออฟฟี่และพี่ต้นลุยงานที่ออฟฟิศอย่างราบรื่นและมีความสุขตลอดทั้งวันนะคะ!
ลงชื่อ: hai (Home AI)
================================================================================
"""

# 1. Write to G:\01_FROM_HOME_TO_OFFICE.txt
g_memo_path = os.path.join(G_DIR, "01_FROM_HOME_TO_OFFICE.txt")
with open(g_memo_path, "w", encoding="utf-8") as f:
    f.write(handover_memo)
print(f"[G:\\] Wrote handover memo to {g_memo_path}")

# 2. Write to Brain_Updates\01_FROM_HOME_TO_OFFICE.txt
brain_memo_path = os.path.join(BRAIN_DIR, "01_FROM_HOME_TO_OFFICE.txt")
with open(brain_memo_path, "w", encoding="utf-8") as f:
    f.write(handover_memo)
print(f"[BRAIN] Wrote handover memo to {brain_memo_path}")

# 3. Append to G:\Home_Brain_Update.txt
home_brain_path = os.path.join(G_DIR, "Home_Brain_Update.txt")
update_entry = f"""
================================================================================
Update Date: {now_str} (Home PC - hai)
Topic: Handover to Offy & Executive Quick Launch Hub Deployment
================================================================================
1. Executive Quick Launch Hub Deployed:
   - File: executive_quick_hub.html (Live on R2: https://assets.siwasup.com/executive_quick_hub.html)
   - Local: G:\\Siwasup_Presentation_2026\\executive_quick_hub.html
   - Featured as Top Banner in G:\\Siwasup_Presentation_2026\\00_START_HERE_เปิดพรีเซนต์ที่นี่.html
   - Full dual-access (Live R2 & Offline Flash Drive) for all 12 key portals.

2. Full Handover to Offy (Office AI):
   - Wrote comprehensive handover memo to G:\\01_FROM_HOME_TO_OFFICE.txt and Brain_Updates.
   - Persona & etiquette checked: Offy speaks female (ค่ะ/คะ/หนู/ออฟฟี่), Ton & Bua are peers/classmates (ห้ามเรียกต้นเป็นพี่ของบัว).
   - Synced all 9 crucial presentation and dashboard HTML files to G:\\Siwasup_Presentation_2026\\.

3. System Status:
   - Master Vault: 15,117 NPA assets + 801 Allabout curated assets (100% matched).
   - Modal background bug resolved (overflow: hidden; overscroll-behavior: contain; frosted glass).
   - Anti-hoarding brief & Exclusive listing audit manual ready for executive presentation.
"""

with open(home_brain_path, "a", encoding="utf-8") as f:
    f.write(update_entry)
print(f"[G:\\] Appended to {home_brain_path}")

# 4. Also update 00_PROJECT_STATUS.md
status_md_path = os.path.join(BRAIN_DIR, "00_PROJECT_STATUS.md")
if os.path.exists(status_md_path):
    with open(status_md_path, "a", encoding="utf-8") as f:
        f.write(f"\n\n### Update [{now_str}] - Executive Quick Launch Hub & Offy Handover\n"
                f"- Deployed `executive_quick_hub.html` to R2 (`https://assets.siwasup.com/executive_quick_hub.html`) and G:\\.\n"
                f"- Mirrored all 9 dashboards to `G:\\Siwasup_Presentation_2026\\`.\n"
                f"- Updated `G:\\01_FROM_HOME_TO_OFFICE.txt` for Offy's morning sync.\n"
                f"- Preserved Twin Brain integrity.\n")
    print(f"[BRAIN] Appended to {status_md_path}")

print("=== ALL TWIN BRAIN UPDATES COMPLETED SUCCESSFULLY ===")
