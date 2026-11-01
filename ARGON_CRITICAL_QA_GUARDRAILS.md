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


---

## 🚨 จุดตายที่ 6: ห้ามใช้ `.replace('</script>', ...)` แบบเหมาเข่ง (Corrupted External Script Tags)
- **สิ่งที่ Flash พลาดจริงในรอบล่าสุด:** ใช้ `html.replace('</script>', custom_js + '</script>')` โดยไม่จำกัดจุด ทำให้โค้ด JS 260 บรรทัดถูกยัดเข้าไปใน `<script src="https://cdn.tailwindcss.com">...</script>` และ `<script src="https://unpkg.com/lucide@latest">...</script>` ซ้ำซ้อนถึง 3 รอบ!
- **กฎเหล็ก:** ห้ามใช้ `.replace('</script>', ...)` เด็ดขาด ให้ใช้ `rpartition('</script>')` หรือวาง Anchor Comment เฉพาะเจาะจง และสคริปต์ตรวจ QA ต้องเช็กว่า `<script src="...">` ทุกตัวต้องมีเนื้อในว่างเปล่า (`len(inner.strip()) == 0`) เสมอ!

## 🚨 จุดตายที่ 7: ห้ามใช้ "เบอร์โทรศัพท์อย่างเดียว" ในการ Login หรือวางปุ่ม 1-Click Admin บนหน้าสาธารณะ (CWE-287 Authentication Bypass)
- **สิ่งที่ Flash พลาดจริง (และคุณต้นจับได้แม่นยำ):** ออกแบบให้กรอกแค่เบอร์โทร 10 หลักก็เข้าสู่ระบบได้เลย แถมวางปุ่ม 1-Click Quick Login ของ CEO (กูล/บัว/ต้น) ไว้หน้าบ้าน! ทั้งที่เบอร์โทรศัพท์ของทุกคนปรากฏเป็นสาธารณะอยู่บนนามบัตรดิจิทัล (`agent_profile.html`) ทำให้ใครก็สวมรอยเป็น CEO ได้!
- **กฎเหล็ก:**
  1. **ต้องใช้ 2 ปัจจัยเสมอ (Phone + 4-Digit Security PIN):** เบอร์โทรคือ Username (สาธารณะ) ต้องคู่กับรหัส PIN ลับเฉพาะตัวเสมอ
  2. **ห้ามโชว์ปุ่มลัด Admin หรือปุ่ม 1-Click บนหน้า Production:** ต้องซ่อนไว้หลัง Query Flag (`?demo=1`) เท่านั้น และหน้า `admin_lobby_manager.html` ต้องมี **Admin Security PIN Gate** ดักก่อนเข้าใช้งานเสมอ

## 🚨 จุดตายที่ 8: ห้ามให้ "การตรวจสิทธิ์" อยู่ฝั่งเบราว์เซอร์ และห้าม API ปล่อยข้อมูลลับ/แก้ไขข้อมูลโดยไม่ตรวจ session
- **สิ่งที่พลาดจริง:** `/api/lobby/list` ส่ง PIN ทุกคนออกมา, endpoint approve/revoke/update-permissions เปิดให้ใครก็เรียกได้, ด่าน PIN หน้าแอดมินตรวจใน JS
- **กฎเหล็ก:** (1) ทุก endpoint ที่แก้ข้อมูลต้องตรวจ session token ฝั่งเซิร์ฟเวอร์ + สิทธิ์จริงจากฐานข้อมูล (2) ห้ามส่ง secret/PIN/lineUserId ออก API (ผ่าน `sanitize_member`) (3) ต้องทดสอบด้วย curl ว่าไม่มี token แล้วได้ 401 ก่อนบอกว่า "ปลอดภัย" และห้ามให้คะแนน 100/100 โดยยังไม่ได้ทดสอบ endpoint แบบไม่ผ่านหน้าเว็บ
