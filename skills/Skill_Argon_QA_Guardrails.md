# Skill: Argon Critical QA Guardrails & Code Resilience (กฎเหล็กวิศวกรรมซอฟต์แวร์)
`[Triggers: Argon QA, Code Guardrails, Flash Blind-Spot, JS Scope, Base64 URI, Schema Sync, Mobile Executive Cards, Zero-Day Recovery, Roster Resilience]`

---

# 🛡️ ARGON CRITICAL QA GUARDRAILS (กฎเหล็กดักจับจุดบอดที่โมเดล Flash มักพลาด)

> **บันทึกโดย:** Argon (AI Senior Software Architect & QA Inspector)  
> **วันที่อัปเดต:** 2 พฤศจิกายน 2569  
> **วัตถุประสงค์:** ป้องกันบั๊กเงียบ (Silent Runtime & Syntax Bugs) ที่มักเกิดจากการใช้สคริปต์ Python แพตช์ไฟล์ HTML/JS ซ้อนทับกันหลายรอบโดยโมเดลความเร็วสูง (Flash)

---

## 🚨 6 จุดวิกฤตที่ห้ามพลาดเด็ดขาด (Flash Blind-Spot Checklist)

### 1. ห้ามแปะโค้ด JS นอกแท็ก `<script>` และห้ามประกาศ `let` / `const` ซ้ำใน Scope เดียวกัน
- **สาเหตุที่ Flash มักพลาด:** เวลาเขียนสคริปต์ Python ใช้ `.replace('</body>', new_js + '</body>')` หรือแทรกโค้ดซ้ำลงในไฟล์ HTML เดิม มักเผลอวางฟังก์ชันหลุดออกนอก `<script>...</script>` หรือประกาศ `let activeRescheduleCaseId = null;` / `let activeVoidCaseId = null;` ซ้ำ 2 รอบใน `<script>` เดียวกัน ซึ่งทำให้ JS ทั้งบล็อกพัง (`SyntaxError: Identifier has already been declared`)
- **กฎเหล็กป้องกัน:**
  - ทุกครั้งที่แก้ไขไฟล์ `.html` ที่มี `<script>` **บังคับต้องสกัดโค้ดใน `<script>` ออกมารัน `node --check <tmp.js>` เสมอ** ห้ามเด็ดขาดที่จะ Deploy ขึ้น Cloudflare R2 โดยไม่รัน `node --check`!
  - เช็คท้ายไฟล์เสมอว่าไม่มี `</body></html>` ซ้ำซ้อน

### 2. ระวังตัวแปรหลุด Scope ระหว่างฟังก์ชัน (`Uncaught ReferenceError: a is not defined`)
- **สาเหตุที่ Flash มักพลาด:** เวลาตัดแปะโค้ดจากฟังก์ชันหนึ่ง (เช่น `changeAgent(code)` ที่มี `const a = AGENTS[code]`) ไปใส่อีกฟังก์ชันหนึ่ง (เช่น `selectMetricOption(optKey)`) มักลืมประกาศ `const a = AGENTS[currentAgent] || AGENTS['S98'];` ในฟังก์ชันปลายทาง
- **ผลกระทบ:** โค้ดไม่เกิด SyntaxError ตอนตรวจด้วยตาเปล่า แต่จะ **Crash ทันทีที่รันจริง (`ReferenceError`)** ทำให้บรรทัดถัดไป (เช่น การเรนเดอร์ตาราง 4 มาตรฐานบริการ และการสลับโหมด `setMode('client')`) หยุดทำงานทั้งหมด!
- **กฎเหล็กป้องกัน:** ทุกฟังก์ชันที่อ้างอิงออบเจกต์สถานะหลัก ต้องดึงค่าจาก Global State (`AGENTS[currentAgent]`) ภายในฟังก์ชันตัวเองเสมอ และห้ามแก้ไขค่าอาร์เรย์ใน Constant ตั้งต้นโดยตรง (ต้อง Clone ด้วย `opt.metrics.map(m => ({ ...m }))` ก่อนแก้ไข)

### 3. ห้ามยัดรูป Base64 (`data:image/jpeg;base64,...`) ลงใน URL Query String (`?avatar=...`)
- **สาเหตุที่ Flash มักพลาด:** เมื่อทำระบบอัปโหลดรูปโปรไฟล์ด้วย Canvas (`toDataURL`) แล้วส่งต่อข้อมูลข้ามหน้าผ่าน URL (`agent_profile.html?name=...&avatar=${encodeURIComponent(avatar)}`)
- **ผลกระทบ:** สตริง Base64 ยาว 20,000–40,000 ตัวอักษรจะทำให้ Cloudflare R2 บล็อกคำขอทันทีด้วย **HTTP 414 URI Too Long** และส่งลิงก์ในแชท LINE ไม่ได้
- **กฎเหล็กป้องกัน:** ส่งเฉพาะ URL รูปที่เป็น `http/https` ใน Query String เท่านั้น ส่วนรูปที่อัปโหลดเองให้ส่งเป็น `?id=SW-APP-XXX` แล้วให้หน้าปลายทางดึงจาก Cloud API (`/api/lobby/status`) หรือ `localStorage`

### 4. การซิงก์ข้อมูลระหว่าง Frontend (`localStorage`) กับ Cloud Server (`Polling`) ต้องมี Schema ตรงกัน 100%
- **สาเหตุที่ Flash มักพลาด:**
  1. หน้าเว็บมี `setInterval(fetchCloudLobby, 3000)` ดึงข้อมูลจาก Server มาทับตัวแปร `lobbyData` ทุก 3 วินาที
  2. แต่ตอนเขียน API `/api/lobby/approve` ฝั่ง Python ลืมก๊อปปี้ฟิลด์ `avatar` จาก `pending` ไป `approved` หรือในไฟล์ตั้งต้น `data/lobby_applicants.json` ลืมใส่ฟิลด์ `badges` และ `title`
  3. ตอนกด `Revoke` หน้าเว็บสร้าง `rollbackId` เองคนละเวลากับที่ Server สร้าง
- **ผลกระทบ:** พอผ่านไป 3 วินาที ข้อมูลที่แสดงบนหน้าจอ (รูปโปรไฟล์, ป้ายสิทธิ์ Badges) จะหายวับไปเพราะถูกข้อมูล Cloud ที่ฟิลด์ไม่ครบเขียนทับ!
- **กฎเหล็กป้องกัน:** Schema ใน `lobby_applicants.json`, API Python (`line_gemini_webhook.py`), และ `DEFAULT_DATA` ใน HTML ต้องมีฟิลด์ครบตรงกันทุกตัว (`id, name, nickname, phone, line_id, zone, avatar, role, title, badges, permissions`) และใช้ `rollback_id` ที่ตอบกลับจาก Server เป็นหลัก

### 5. เวลาอัปเดตตัวเลข/ข้อความใน JS ต้องอัปเดต Static HTML ที่แสดงคู่กันด้วย
- **สาเหตุที่ Flash มักพลาด:** แก้ตัวแปร JS `METRIC_OPTIONS.opt1` เป็น 4 มาตรฐานบริการจริงแล้ว แต่ลืมแก้ข้อความในบล็อก HTML ด้านล่าง (`#executiveSelectorBox`) ทำให้ยังมีคำเคลมเก่า (`ดันกู้ผ่าน 50+ ราย`, `กู้ผ่าน 98%`) โผล่ค้างบนหน้าจอ
- **กฎเหล็กป้องกัน:** ใช้ `grep` ค้นหาคำเก่าทั้งไฟล์ `.html` ทุกครั้งหลังแพตช์ เพื่อให้แน่ใจว่าไม่มีข้อความเก่าตกค้างทั้งใน HTML และ JS

### 6. กฎการใช้โลโก้ศิวาทรัพย์ (`siwasup_logo.svg` vs `assets/daimond.svg`)
- **เมื่อวางโลโก้เดี่ยวหรือต้องการแสดงชื่อแบรนด์ในตัวโลโก้:** ใช้โลโก้ศิวาทรัพย์แดงตัวเต็ม `https://assets.siwasup.com/siwasup_logo.svg`
- **เมื่อดีไซน์มี Text ชื่อบริษัทขนาดใหญ่วางคู่ด้านข้างอยู่แล้ว (เช่น Header นามบัตร หรือ Header หน้าลงทะเบียน/ป้าย QR):** ใช้ไอคอนเพชรแดง `assets/daimond.svg` ได้ทันที เพื่อไม่ให้ตัวหนังสือในโลโก้ย่อส่วนไปซ้อนทับกับชื่อบริษัทด้านข้าง (ห้ามใช้กล่องตัวอักษร `"S"` แทนโลโก้เด็ดขาด)

### 7. สถาปัตยกรรมการแปลงตารางเป็น Mobile Executive Cards (ถอดแบบจาก Illustrator `admin_001.ai`)
- **ปัญหาเดิมบนจอมือถือ (360px):** ตาราง 5 คอลัมน์ถูกบีบจนตัวอักษรหักบรรทัดน่าเกลียด (เช่น "โซนท่า\nข้าม-\nพระราม\n2") และปุ่มคำสั่งสำคัญอย่าง "ดูบัตร", "ปรับสิทธิ์", "คัดออก" หลุดขอบจอขวา ผู้ใช้บนมือถือต้องเลื่อนจอแนวนอน
- **ทางแก้ตามมาตรฐาน Mobile-First & Illustrator System:**
  1. แปลงเป็น **Executive Member Card** จัดสัดส่วนพอดีจอ 360px และเรียงเป็น **4 คอลัมน์บน PC (`xl:grid-cols-4`)**
  2. **ระบบสีแยกตามระดับบทบาท (Color Token Matrix):**
     - 👑 **Supreme EXE (คุณเจี๊ยบ / คุณบัว):** สีส้มอิฐ Terracotta Coral (`#e15b42`) + แคปซูลมงกุฎ
     - 🔑 **Key Master (พี่ลิลลี่):** สีกรมท่า Deep Royal Navy (`#014576`) + แคปซูลกุญแจ
     - 🛡️ **Administrator (ฝ่ายซัพพอร์ต/ออฟฟิศ):** สีเขียวมิ้นต์ Aqua Teal (`#68c4b6`) + แคปซูลโล่
     - 💻 **Tech Architect ([NASSTY]):** สีดำ-เทา Dark Charcoal (`#1e293b`) + แคปซูลแล็ปท็อป
  3. **การจัดวางลายน้ำชื่อเล่น:** ปรับความเข้มขึ้น 50% เป็น `text-slate-400/90` เพื่อให้อ่านออกชัดเจนบนจอ OLED/มือถือกลางแจ้ง

### 8. ระบบแท่นลากสิทธิ์ด่วน (Drag & Drop Privilege Dock) & ถังขยะเพิกถอนสิทธิ์
- **สำหรับ 3 ผู้บริหารสูงสุด ([NASSTY] • คุณบัว • คุณกูล):**
  - **แท่นลากสิทธิ์ (Dock):** รวมป้ายสิทธิ์ 8 หมวดหมู่ (เคาะราคาบ้าน, กุญแจสำรอง, คุมกุญแจ OTP, สิทธิ์บริหาร, ดูแชทลีด, Standard Admin, ช่วยคัดสต๊อก, Technical Admin)
  - **การมอบสิทธิ์:** ลากป้ายจาก Dock ไปปล่อยลงในการ์ดสมาชิก ➡️ สิทธิ์เพิ่มและซิงก์ขึ้นเซิร์ฟเวอร์ทันที
  - **การถอดสิทธิ์:** ลากป้ายสิทธิ์จากการ์ดสมาชิกมาปล่อยลง **ถังขยะเพิกถอนสิทธิ์ (`badgeTrashDropZone`)** ➡️ สิทธิ์หลุดและซิงก์ขึ้นเซิร์ฟเวอร์ทันที พร้อม Floating Toast แจ้งเตือน

### 9. ระบบตรวจสอบสถานะออนไลน์ตามจริง (Realtime Presence Engine)
- **เลิกใช้สถานะ Static Mockup:**
  - เพิ่ม **Heartbeat Ping (`/api/presence/heartbeat`)** ทุก 45 วินาทีขณะผู้ใช้เปิดหน้าจอ
  - เซิร์ฟเวอร์บันทึก `last_active_at` จากทั้งการเข้าเว็บและปฏิสัมพันธ์ในแอป LINE
  - เงื่อนไขการแสดงผล:
    - มีการเคลื่อนไหวภายใน 5 นาที (`diff <= 300s`) ➡️ `🟢 ONLINE` (ไฟเขียวกระพริบ)
    - ไม่มีการเคลื่อนไหวเกิน 5 นาที ➡️ `⚪ 10m ago`, `2h ago`, หรือ `OFFLINE`

### 10. กฎการ Deploy Cloudflare R2 เพื่อป้องกัน Browser Disk Cache ติดค้าง
- **สาเหตุที่ผู้ใช้กด F5 แล้วหน้าจอไม่เปลี่ยน:** Cloudflare R2 โดยค่าเริ่มต้นไม่ส่ง Header `Cache-Control` ทำให้ Google Chrome บน Windows จดจำไฟล์เก่าไว้ใน Disk Cache
- **กฎเหล็กแก้ไข:**
  - สคริปต์อัปโหลด R2 ต้องแนบ Header: `Cache-Control: no-cache, no-store, must-revalidate` เสมอ
  - ในกรณีทดสอบให้เติม URL Param ป้องกันแคช เช่น `?v=2`, `?v=3`

### 11. การคุ้มครองสิทธิ์ระดับ Super Tech Root ([NASSTY])
- **Backend Hardcoded Guard:** เซิร์ฟเวอร์ใน `line_gemini_webhook.py` ดักฟังก์ชัน `/api/lobby/update-permissions` และ `/api/lobby/revoke` ไว้อย่างเด็ดขาด: หากเป้าหมายคือ `app_office_004` แต่ผู้สั่งการไม่ใช่ `is_super_tech_root` เซิร์ฟเวอร์จะปฏิเสธด้วย `403 Forbidden`
- **UI Root Protection:** บนการ์ดแสดงป้าย `[ 🛡️ Root Protected ]` และ `[ 🔒 Root Locked ]` ปิดการกดแก้ไขและคัดออกจากระบบถาวร
- **Auto-Normalization:** มีฟังก์ชัน `normalizeNasstySeat` แปลงชื่อเป็น `[NASSTY]` และชื่อเล่นเป็น `NASSTY` อัตโนมัติทุกครั้งที่โหลดข้อมูล

### 4. Zero-Day Disaster Recovery & Roster Resilience (2026-11-05 Incident)
- **ทำเนียบสมาชิก 13 เสาหลักที่ได้รับการคุ้มครองถาวร:**
  1. `[NASSTY]` (081 555 5555): 💻 Tech Architect & Senior Advisor
  2. `👶JEab V@r¡nTh@rn👶🐥✨` (094 462 9796): 👑 Supreme EXE (CEO) [กู้คืนรูป LINE จริง]
  3. `ภมรมาศ ตันฑุลทุกุล (บัว)` (085 336 5703): 👑 Supreme EXE [สะกดถูกต้องตามผู้ใช้ชี้แนะ]
  4. `วรวลัญช์ ว่องสุวรรณวาร (ลิลลี่)` (092 583 6565): 🔑 Key Master (Head of Viewing)
  5. `สุภาพร By ศิวาทรัพย์ (ออย)` (098 212 2347): 🛡️ Administrator (Coordinator)
  6. `ณัฐสุดา พรพริ้ง (ป๊อปปี้)` (063 073 3022): 🛡️ Administrator (Coordinator)
  7. `จูน` (086 786 2841), `เจง` (085 128 9692), `กัญ` (093 961 5356), `โก้` (064 891 6569), `หลิว` (096 249 6253), `จี๊ด/แป้ง` (096 645 8994), `Jaidee Asset` (061 442 8555): 🤝 Certified Free Agents
- **กลไก Dual-Path Resilience:** `admin_lobby_manager.html` ใช้ Smart Union Merge + Fallback ดึง R2 Static Vault อัตโนมัติเมื่อ Render หลับ


---

