# Siwasup Co-Broker OS (LINE LIFF Prototype) 🏢✨

ระบบบริหารจัดการพอร์ตอสังหาริมทรัพย์และเครือข่ายตัวแทนขาย (Co-Broker / Flipper OS) แบบ Real-time ผ่าน LINE LIFF  
ออกแบบสำหรับ **บริษัท ศิวทรัพย์ แอสเสท จำกัด (Siwasup Asset Co., Ltd.)**

---

## 🌟 Live Demo (GitHub Pages)
👉 **เปิดใช้งานผ่านมือถือ/คอมพิวเตอร์:** [https://thenassty-cpu.github.io/siwasup-cobroker-os/](https://thenassty-cpu.github.io/siwasup-cobroker-os/)

---

## 🎯 ฟังก์ชันหลัก (3-Way View Switching)

ระบบถูกออกแบบให้ทำงานบนหน้าจอเดียว แต่ปรับเปลี่ยนมุมมองและสิทธิ์ตามบทบาทผู้ใช้งานได้ทันที:

1. **👑 มุมมองเจ้าของ / แอดมิน (บัว & กูล):**
   - **Executive Dashboard:** แสดงตัวเลขสรุปทรัพย์ในพอร์ตสดๆ (ทั้งหมด, พร้อมขาย, ติดจอง, ขายแล้ว)
   - **1-Click Status:** สลับสถานะทรัพย์ได้ในคลิกเดียวจากมือถือ ไม่ต้องเปิดคอมแก้ Excel
   - **Financial Estimation:** คำนวณยอดเงินเตรียมจ่ายค่าคอมมิชชั่น 5% แต่ละเคสแบบอัตโนมัติ
   - **Drive Integration:** ปุ่มลัดเชื่อมต่อคลังโฟลเดอร์รูปภาพความละเอียดสูงบน Google Drive

2. **👔 มุมมองตัวแทนขาย (เอเจนต์ / ลูกศิษย์คอร์ส):**
   - **Commission Badge:** แสดงป้ายค่าคอมมิชชั่น 5% ชัดเจน (เช่น "รับ Agent คอม 5% (179,500 บ.)")
   - **White-Label Link:** ปุ่มก๊อปปี้ลิงก์ตัดเบอร์ติดต่อศิวทรัพย์ออก เพื่อส่งต่อให้ลูกค้าของตนเองได้ทันที
   - **Raw Photos:** ปุ่มขอรูปดิบไม่มีลายน้ำเพื่อนำไปทำสื่อการตลาด
   - **Booking Submission:** โมดัลแจ้งวางเงินจองพร้อมแนบสลิปส่งตรงถึงเจ้าของ

3. **👤 มุมมองลูกค้าปลายทาง (White-Label):**
   - ซ่อนข้อมูลค่าคอมมิชชั่นและข้อมูลติดต่อของศิวทรัพย์ทั้งหมด 100%
   - แสดงเฉพาะข้อมูลรายละเอียดทรัพย์ สเปกห้อง และราคาขาย
   - ปุ่ม Call-to-Action เชื่อมต่อไปยังเอเจนต์ผู้ส่งลิงก์เท่านั้น

---

## 📁 โครงสร้างไฟล์
- `index.html` : หน้าเว็บแอพพลิเคชันหลัก รองรับการเปิดบนเบราว์เซอร์และ LINE In-App Browser (LIFF)
- `siwasup_all_properties.js` : ฐานข้อมูลทรัพย์ 135 รายการในรูปแบบ JavaScript Object (Offline Ready)
- `siwasup_all_properties.json` : ข้อมูลทรัพย์ในรูปแบบ Raw JSON
- `siwasup_all_properties.csv` : ข้อมูลทรัพย์พร้อมเปิดใน Excel (UTF-8 with BOM)

---
*Developed by Ton (NASSTY) - Advisor & Tech Lead*
