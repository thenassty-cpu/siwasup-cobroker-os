# 🗺️ Product Roadmap: Siwasup Co-Broker & Renovation OS

**Project:** ระบบบริหารคลังทรัพย์รีโนเวท & เครือข่ายตัวแทนขาย (Co-Broker & Renovation OS)  
**Client:** บริษัท ศิวาทรัพย์ แอสเซท จำกัด (`@siwasup`)  
**Live URL:** [https://thenassty-cpu.github.io/siwasup-cobroker-os/](https://thenassty-cpu.github.io/siwasup-cobroker-os/)  
**Last Updated:** 15 ตุลาคม 2569  

---

## ✅ 1. สถานะงานที่ทำสำเร็จแล้ว (Completed Milestones)

### 🎨 Design System & Visual Architecture (100%)
- [x] **Homerun Platform Clean Aesthetic (2026 Modern Real Estate Standard):**
  - **4:3 Aspect Ratio Cards:** รูปทรัพย์สัดส่วน 4:3 คมชัด พร้อมเอฟเฟกต์ซูมละมุนเมื่อ Hover
  - **Translucent Floating Badges:** ป้ายหมวดหมู่แคปซูลกระจกดำโปร่งแสง (`bg-black/60 backdrop-blur-md`) มุมซ้ายบน พร้อมปุ่มวงกลมแก้วแชร์ & บันทึกหัวใจมุมขวาบน
  - **Vibrant Status Pills:** ป้าย `New` สีส้มอมแดงสดใส (`#FF3838`) วางเคียงข้างป้ายธนาคาร NPA แบบพาสเทลคลีนตา
  - **2-Tier Financial Pricing Layout:** แสดงราคาก่อนต่อรอง (สีฟ้า Ocean `#1E749C`) คู่กับหลักประกันต่อรองราคา (เช่น ฿50,000) สไตล์ Homerun เป๊ะ
  - **Signature Caramel Pill CTA:** ปุ่ม `ดูรายละเอียด` ทรงแคปซูลมนสีทองทรายซาติน (`#BCA371`) เต็มความกว้าง
  - **Sub-Header Quick Bar:** แถบหัวข้อย่อยสไตล์ Homerun พร้อมป้าย "รอบล่าสุด", ตัวสลับโหมด "ตาราง | แผนที่" และตัวนับจำนวนทรัพย์เรียลไทม์
  - **Property Detail Modal:** ป๊อปอัปดูรายละเอียดครบวงจร คำนวณยอดผ่อนรายเดือน (ล้านละ 3,500 บ.) และเชื่อมต่อไปยังป้ายไวนิล/แชร์สิทธิ์
- [x] **60-30-10 Brand Identity:** คุมสัดส่วน White 60% (Clean Canvas) - Red 30% (Brand/CTA) - Satin Gold 10% (Luxury Hooks จากป้ายโลโก้ 3D จริง)
- [x] **Pastel NPA Bank Badges:** แปลงป้ายธนาคาร (SCB, KBank, TTB, SAM, KTB, GSB, GHB, BBL, Siwasup) เป็น Soft Pastel ไม่แย่งซีนแบรนด์หลัก
- [x] **Lucide Icon System:** กำจัด Emoji หลากสีออกทั้งหมด ใช้ไอคอนเส้นขาวมาตรฐาน (`stroke-[1.5]`) ในคอนเทนเนอร์วงกลมเทาโปร่งแสง 50% (`.icon-circle`)
- [x] **Capsule Overlay Bar:** แถบค่าคอมมิชชั่นทรงแคปซูลโปร่งแสง 20% ผสานกระจกฝ้า (`rounded-full bg-white/20 backdrop-blur-md border border-white/40`)

### ⚙️ Core OS Functional Modules (Front-End Prototype 100%)
- [x] **Frictionless White-label Catalog:** ลูกค้าเข้าชมได้ทันทีไม่ต้องล็อกอิน ซ่อนค่าคอมมิชชั่น จำรหัสตัวแทน 60 วัน
- [x] **Multi-Role Switcher:** สลับโหมด Owner / Free Agent / Employee / Trainee / Client
- [x] **Smart Share Center (Responsive & Scrollbar-Free):** สร้างลิงก์ดักจับสิทธิ์เจาะจง 5 ช่องทาง (FB, TikTok, LINE, Web, QR Code) ดีไซน์ไร้แถบ Scrollbar กวนสายตา พร้อมการแสดงผล QR แบบปรับเปลี่ยนตามหน้าจออัตโนมัติ:
  - **Desktop / Tablet:** ขยายออกด้านข้างแบบ Side-by-Side Panel สวยงาม ไม่เพิ่มความสูงในแนวตั้ง
  - **Mobile:** เด้ง Sub-Modal ป๊อปอัปซ้อนขึ้นมาแบบคลีนตา 100% พร้อมปุ่มดาวน์โหลดรูป QR ชัดระดับ HD ใน 1 คลิก
- [x] **Lead Magnet & Trainee Mission:** หน้าต่างฝากขายทรัพย์ฟรี พร้อมภารกิจส่งทรัพย์ 3 หลังเพื่อปลดล็อก Free Agent
- [x] **MGM Referral:** ระบบชวนเพื่อนเป็นตัวแทนพร้อม QR Code และโครงสร้าง Overriding Commission 0.5%
- [x] **Submit Offer / Bank NPA:** ฟังก์ชันยื่นข้อเสนอต่อรองราคาธนาคารผ่านแอดมินบัว
- [x] **Smart Pricing Guardrails:** ระบบล็อกการแก้ไขราคาเมื่อติดจอง/ขายแล้ว พร้อมแจ้งเตือนจิตวิทยาการขายและบันทึก Price History
- [x] **Instant Bundle:** เครื่องมือมัดรวมทรัพย์สร้างหน้าเว็บ VIP ไมโครแคตาล็อกเฉพาะบุคคล พร้อมร่างแคปชั่นส่งเข้าแอป LINE ทันที

---

## ⏳ 2. งานที่ต้องทำต่อในเฟสถัดไป (Pending / Next Sprints)

### 🚀 Phase 1: Database & Backend Integration (Sprint ถัดไป)
- [ ] **Supabase Setup:** รันสคริปต์ `supabase_schema_phase1.sql` บน Supabase Cloud
- [ ] **Data Fetching API:** สลับจากการอ่านไฟล์ `siwasup_all_properties.js` ไปเป็นการดึงข้อมูล Real-time จาก Supabase Database
- [ ] **File Storage Bucket:** เชื่อมต่อระบบอัปโหลดสลิปเงินมัดจำ, โฉนดที่ดิน, และรูปภาพทรัพย์ฝากขายไปยัง Supabase Storage
- [ ] **Authentication:** เชื่อมต่อระบบล็อกอินตัวแทนผ่าน LINE LIFF (เข้าถึงรหัสตัวแทนอัตโนมัติจาก LINE User ID)

### 🤖 Phase 2: Automation & Data Pipelines
- [ ] **Bank NPA Scraper:** พัฒนาสคริปต์ดึงข้อมูลทรัพย์ NPA อัตโนมัติด้วย GitHub Actions (Cron สัปดาห์ละ 1 ครั้ง)
- [ ] **LINE OA Webhook:** แจ้งเตือนข้อความเข้าแอดมินบัว/เจี๊ยบทันทีที่มี Lead หรือการจองใหม่ผ่าน LINE Messaging API
- [ ] **Gamification Engine:** คำนวณแต้มสะสมจาก Lead และการส่งทรัพย์ขึ้น Leaderboard อัตโนมัติ

### 🖨️ Phase 3: Scale & Production Tools
- [x] **Auto PDF Vinyl Sign Generator:** สร้างไฟล์ PDF พิมพ์ป้ายไวนิลหน้าบ้านขนาดจริง (1:1 สเกลเป๊ะ 120x80 ซม., 150x80 ซม., 60x90 ซม.) พร้อม Dynamic QR Code ล็อกสิทธิ์ตัวแทน และดาวน์โหลดรูป HD ได้ในคลิกเดียวด้วย `pdf-lib` + `qrcode`
- [x] **Siwasup Agent Roster & 2-Track Automated Scoring Engine (`siwasup_agents.js`):**
  - ฐานข้อมูลตัวแทนจริง 125 ท่าน (`S02` ถึง `S126`) คลีนข้อมูลจาก Google Sheets พร้อมคำนวณ 5 ระดับเกียรติยศ (Trainee ➔ Active ➔ Silver ➔ Gold ➔ Diamond Master)
  - ระบบ Autocomplete ค้นหารหัสตัวแทนและชื่อเล่นแบบเรียลไทม์ ในหน้าต่าง Smart Share และ Auto PDF Vinyl Sign
  - หน้าต่าง **ทำเนียบตัวแทน & Live Leaderboard Modal** แสดงโพเดียม Top 3 (🥇, 🥈, 🥉), กรองแทร็กคะแนน (รวม, กิจกรรม, ผลงาน) และช่องค้นหาฉับไว
  - กลไกแจกแต้มอัตโนมัติ Zero-Admin Overhead:
    - ดาวน์โหลดแบบป้ายไวนิล: ได้ **+5 แต้ม** อัตโนมัติ
    - สแกน QR เช็คชื่อเข้าประชุมทีม/อบรม: ได้ **+10 แต้ม** อัตโนมัติ (พร้อมระบบฉาย QR จอใหญ่)
    - ส่งภาพติดป้ายหน้างานจริงพร้อมดึงพิกัด GPS (`navigator.geolocation`): ได้ **+15 แต้ม** อัตโนมัติ
    - แชร์ทรัพย์ผ่าน Smart Share Center: ได้ **+5 แต้ม** อัตโนมัติ
    - แอดมินกดยืนยันการจองบ้าน: ยิง **+100 แต้มผลงาน** เข้าตัวแทนผู้ดูแลเคสอัตโนมัติทันที
- [x] **Database Schema Update:** อัปเดต `supabase_schema_phase1.sql` เพิ่มตาราง `agent_point_transactions` และฟิลด์คะแนน/ระดับในตาราง `profiles`

### 🏛️ Phase 4: Future Scale & Engine v2.0 (Area-Based Sharding & Home Area Expansion)
- [ ] **Home Area Architecture & Alert System ([ARCHITECTURE_ENGINE_V2_HOME_AREA_SHARDING.md](file:///C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/ARCHITECTURE_ENGINE_V2_HOME_AREA_SHARDING.md)):**
  - เกณฑ์คณิตศาสตร์เปลี่ยนผ่านจาก Global Pool (ฐาน 125 Agents) สู่ระบบ Home Area (7 โซนหลัก)
  - 4 มิติคอขวด: Eagle Quota Cap (ชนเพดาน 15 คน), Erlang-C Co-Close Surge (>48 ชม.), Key Dispatch SLA (กูล/พี่ลิลลี่วิ่งข้ามโซน), Zone Density (45-50 Agents / 25 ทรัพย์)
  - Hybrid Soft Sharding 3 ระยะ: เก็บพิกัด Home Area ล่วงหน้า -> Carve-out Hot Zones -> Global Overflow Fallback 30 นาที
  - UI Executive Alert สไตล์ The Digital Luxury Ratio 75-15-5-5 (Amber 500 & Burgundy 900)

### 🧩 Architectural Optimization & Token Economy (100% Completed)
- [x] **Modal Component Extraction:** สกัด Template ของ Modals ทั้งหมด 10 ตัวออกจาก `index.html` ไปไว้ใน `modals.js` ช่วยลดโค้ดใน `index.html` ลงกว่า 530 บรรทัด (จาก 2,062 เหลือ 1,532 บรรทัด) ประหยัด Token สูงสุด
- [x] **Global CSS Style Presets:** กำหนด Class Utility กลาง `.capsule-glass-20` (`rounded-full bg-white/20 backdrop-blur-md border border-white/40`) และชุด Modal `.modal-backdrop`, `.modal-card`, `.modal-card-sm` ทำให้การปรับจูนสไตล์แก้เพียง 1 จุดแล้วมีผลทั่วทั้งระบบทันที

---
## 📌 อัปเดตล่าสุด (19 ต.ค. 2569 รอบดึก): Sold Out Purge, Client Guardrails & NPA Key Prototype

1. **ถอนรากถอนโคนทรัพย์ Sold Out จากภาพ 16 หลัง (Purge 16 Properties):**
   - ลบ 16 รหัสทรัพย์ที่มีตราประทับสีแดง Sold out ออกจาก `siwasup_all_properties.json` และ `siwasup_all_properties.js` อย่างถาวร (เหลือ 119 ทรัพย์คลีน 100%)
   - รหัสที่ลบ: `1090909`, `1090983`, `1091030`, `1100870`, `1140347`, `1165872`, `1174328`, `1178450`, `1204059`, `1908024-land-buengkum`, `code-105105`, `code-2005059`, `code-2007071`, `code-2007073`, `code-2009084`, `code-2112112`

2. **ระบบล็อกทรัพย์ "ติดจอง" ใน Client Mode:**
   - หน้ารายละเอียดทรัพย์ (Modal): ปิดปุ่ม "เสนอราคา" เป็นสถานะ Disabled `🔒 ทรัพย์นี้อยู่ระหว่างติดจอง (ปิดรับข้อเสนอชั่วคราว)` และมีปุ่มทางเลือก `💬 สอบถามคิวสำรองผ่าน LINE Official (@siwasup)`
   - ส่วนเอกสารสัญญา: ล็อกไม่ให้เปิด/ดาวน์โหลดสัญญาจะซื้อจะขาย พร้อมแจ้งเตือน `🔒 อยู่ระหว่างติดจอง ปิดดาวน์โหลดสัญญาชั่วคราว`
   - หน้าการ์ดรายการ: เปลี่ยนปุ่ม `LINE นัดชม` เป็น `คิวสำรอง` (ทัก LINE แบบระบุขอเป็นคิวสำรองกรณีหลุดจอง) และปิดปุ่มสัญญาเป็น `ปิดรับข้อเสนอ`

3. **แก้ไข Visual Noise ป้าย "New":**
   - ยกเลิกตรรกะเหมาเข่งเดิมที่แปะป้าย New ให้ทุกการ์ด
   - แสดงป้าย `New` สีแดงเฉพาะทรัพย์ใหม่จริง (6 รายการแรก หรือมี `is_new: true`) ทรัพย์ปกติแสดงเฉพาะรูปและหมวดหมู่คลีนตาตามมาตรฐาน Homerun

4. **ต้นแบบระบบเบิกกุญแจ NPA & ติดตาม Messenger (NPA Key Dispatch Demo):**
   - เพิ่ม Modal จำลองและปุ่มลัดในแถบเมนูหลัก + หน้ารายละเอียดทรัพย์
   - ครอบคลุม 3 ส่วน: (1) ยื่นขอเบิกกุญแจพร้อมคำนวณ Lead Time, (2) ติดตาม Messenger & รอบธนาคาร Live Tracker, (3) แผง 1-Click ประเมินตัดเกรด Agent Trust Score โดยพี่ลิลลี่ (Admin)
   - **📝 บันทึกงาน (Pending Handover):** *ระบบกุญแจยังไม่เคลียร์ดี อยู่ระหว่างรอหารือร่วมกับ กูล, บัว, พี่ลิลลี่ และรอ Argon กลับมาพัฒนาต่อ*
