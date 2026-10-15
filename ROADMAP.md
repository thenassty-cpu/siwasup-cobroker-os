# 🗺️ Product Roadmap: Siwasup Co-Broker & Renovation OS

**Project:** ระบบบริหารคลังทรัพย์รีโนเวท & เครือข่ายตัวแทนขาย (Co-Broker & Renovation OS)  
**Client:** บริษัท ศิวาทรัพย์ แอสเซท จำกัด (`@siwasup`)  
**Live URL:** [https://thenassty-cpu.github.io/siwasup-cobroker-os/](https://thenassty-cpu.github.io/siwasup-cobroker-os/)  
**Last Updated:** 15 ตุลาคม 2569  

---

## ✅ 1. สถานะงานที่ทำสำเร็จแล้ว (Completed Milestones)

### 🎨 Design System & Visual Architecture (100%)
- [x] **60-30-10 Brand Identity:** คุมสัดส่วน White 60% (Clean Canvas) - Red 30% (Brand/CTA) - Satin Gold 10% (Luxury Hooks จากป้ายโลโก้ 3D จริง)
- [x] **Pastel NPA Bank Badges:** แปลงป้ายธนาคาร (SCB, KBank, TTB, SAM, KTB, GSB, GHB, BBL, Siwasup) เป็น Soft Pastel ไม่แย่งซีนแบรนด์หลัก
- [x] **Lucide Icon System:** กำจัด Emoji หลากสีออกทั้งหมด ใช้ไอคอนเส้นขาวมาตรฐาน (`stroke-[1.5]`) ในคอนเทนเนอร์วงกลมเทาโปร่งแสง 50% (`.icon-circle`)
- [x] **Capsule Overlay Bar:** แถบค่าคอมมิชชั่นทรงแคปซูลโปร่งแสง 20% ผสานกระจกฝ้า (`rounded-full bg-white/20 backdrop-blur-md border border-white/40`)

### ⚙️ Core OS Functional Modules (Front-End Prototype 100%)
- [x] **Frictionless White-label Catalog:** ลูกค้าเข้าชมได้ทันทีไม่ต้องล็อกอิน ซ่อนค่าคอมมิชชั่น จำรหัสตัวแทน 60 วัน
- [x] **Multi-Role Switcher:** สลับโหมด Owner / Free Agent / Employee / Trainee / Client
- [x] **Smart Share Center:** สร้างลิงก์ดักจับสิทธิ์เจาะจง 5 ช่องทาง (FB, TikTok, LINE, Web, QR Code)
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
- [ ] **GPS & OCR Proof of Work:** ระบบถ่ายรูปตรวจเช็กพิกัด GPS ติดป้ายหน้าบ้านจริง

### 🧩 Architectural Optimization & Token Economy (100% Completed)
- [x] **Modal Component Extraction:** สกัด Template ของ Modals ทั้งหมด 10 ตัวออกจาก `index.html` ไปไว้ใน `modals.js` ช่วยลดโค้ดใน `index.html` ลงกว่า 530 บรรทัด (จาก 2,062 เหลือ 1,532 บรรทัด) ประหยัด Token สูงสุด
- [x] **Global CSS Style Presets:** กำหนด Class Utility กลาง `.capsule-glass-20` (`rounded-full bg-white/20 backdrop-blur-md border border-white/40`) และชุด Modal `.modal-backdrop`, `.modal-card`, `.modal-card-sm` ทำให้การปรับจูนสไตล์แก้เพียง 1 จุดแล้วมีผลทั่วทั้งระบบทันที

