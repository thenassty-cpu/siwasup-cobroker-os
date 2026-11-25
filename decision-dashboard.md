# 🎯 Decision Dashboard: ปิดช่องโหว่ Access Control & ระบบสลับ 3 มุมมอง (`catalog.html`)
**สถานะ:** รอการประเมินคะแนน (Syb/Hai / Sena / MrX กรอกเฉพาะในตารางนี้ ห้ามเถียงในแชต)

## 📊 ตารางให้คะแนนทางเลือก (เต็ม 10 คะแนน/ด้าน)

| ทางเลือก (Options) | Sena (เสธฯ): โครงสร้าง & ตรงโจทย์ | Hai/Syb (ปฏิบัติ): ความเร็ว & ความง่าย | MrX (ตรวจสอบ): ความปลอดภัย & ไร้ Bug | คะแนนรวม (30) |
| :--- | :---: | :---: | :---: | :---: |
| **Option A:** Fail-Closed Client Default + Auto-Promote หลัง Auth + 3-View Admin Switcher | 9 | 9 | 9 | **27** |
| **Option B:** Minimal Hotfix (แก้ `else -> client` + Guard ใน `setMode()` + เปิด Switcher เดิม) | 6 | 10 | 7 | **23** |
| **Option C:** Strict Portal Split (บังคับ Redirect Login เมื่อเข้าโหมดตัวแทน + แถบ Preview 3 มุมแยก) | 8 | 6 | 6 | **20** |

## 📝 เหตุผลประกอบ (จำกัดคนละ 1 บรรทัดต่อ 1 ทางเลือก)
* **Option A:**
  * **Sena:** ปิดช่องโหว่ Fail-Closed 100% บน Production พร้อม Promote สิทธิ์หลัง Auth, เปิด 3 มุมมองให้คุณกูล (`SW001`), และคง Demo Sandbox บน `github.io` ได้ครบทุกโจทย์โดยไม่พัง Flow เดิม
  * **Hai/Syb:** แก้ใน `catalog.html` จุดเดียวต่อยอดจาก `verifySiwasupAgentSession()` เดิม ทำเร็วและไม่กระทบไฟล์อื่น
  * **MrX:** ปิดช่องโหว่ Fail-Open ตั้งแต่เฟรมแรกและ Promote เฉพาะหลัง Auth จริง แต่ต้องระวัง Guard ใน `setMode()` และ `toggleAdminConsoleUnlock()` ไม่ให้หลุดบน Prod
* **Option B:**
  * **Sena:** แก้จุดรั่วเร็วที่สุดแต่อาจเกิดอาการหน้าจอกระพริบสลับโหมดตอนโหลด และเมนูสลับโหมดสำหรับคุณกูลยังมี 5 ปุ่ม (รวม Contract/ฝึกหัด) ทำให้สับสน
  * **Hai/Syb:** แก้น้อยที่สุดไม่กี่บรรทัด เสร็จไวสุดแต่ UX สลับมุมมองสำหรับผู้บริหารยังไม่เนี้ยบ
  * **MrX:** อุดรูรั่วหลักได้เร็ว แต่เสี่ยง Bug เรื่อง Auto-Promote หลัง Auth, จอกระพริบ และ Switcher 5 ปุ่มเดิมเสี่ยงกดพลาด
* **Option C:**
  * **Sena:** แยกขอบเขตลูกค้า-ตัวแทนเด็ดขาดปลอดภัยสูงสุด แต่ต้องแก้ข้ามหลายไฟล์ (`welcome_landing.html`, `agent_registration.html`) และเปลี่ยนพฤติกรรมผู้ใช้เดิมมากเกินไป
  * **Hai/Syb:** ต้องแก้หลายไฟล์และเปลี่ยน Flow ลิงก์เดิม ใช้เวลาทำและเทสมากกว่า Option A
  * **MrX:** แยกสิทธิ์ปลอดภัยสูงแต่แก้ข้ามหลายไฟล์ เสี่ยง Bug เรื่อง Redirect Loop, Deep-link พัง และ Service Worker Cache ไม่ซิงก์กัน

---
## 👑 คำสั่งตัดสินใจของแม่ทัพ (Human Approval Gate)
- [x] เลือก Option A
- [ ] เลือก Option B
- [ ] เลือก Option C
**คำสั่งเพิ่มเติม:** อนุมัติทำ Option A ทันที (25-11-69 17:36)
