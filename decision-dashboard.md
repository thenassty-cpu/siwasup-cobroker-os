# 🎯 Decision Dashboard: แก้ระบบค้นหาทำเลทั่วประเทศ + "ขอลิงก์" + Nearest Fallback
**สถานะ:** อนุมัติ **Option B** แล้ว (โดยพี่ต้น) — กำลังดำเนินการพัฒนา

## 👑 คำสั่งตัดสินใจของแม่ทัพ (Human Approval Gate)
- [ ] เลือก Option A
- [x] เลือก Option B
- [ ] เลือก Option C

## 📋 สรุปขอบเขตทางเลือก (Options Scope)
- **Option A: Quick Regex + In-Memory Geo & Province Fallback**
  - แก้ `resolve_catalog_link_request` ให้ปล่อยผ่านคำขอที่มีทำเล/เงื่อนไขต่อท้าย (กันชน `m_link` & `is_onboarding_link_req`), ใช้ `thai_landmap_geo.js` + ชื่อตำบลที่มีใน `siwasup_all_properties.json` ทำ Greedy Longest-Match แยกคำติดกัน (เช่น `คานหามอยุธยา`), Fallback ใกล้เคียงด้วย Haversine จาก `DISTRICT_CENTROIDS` (68 โซน) หรือระดับจังหวัดเดียวกัน, และเพิ่ม `?q=&province=&cat=` (รวมกลุ่ม `บ้าน`) ใน `catalog.html` + bump `sw.js`
- **Option B: Static Thai Tambon Centroids (~7,400 ตำบล) + Cross-Province Haversine + Deep-Link (แนะนำ)**
  - แก้ `resolve_catalog_link_request` เช่นเดียวกับ A, เพิ่มไฟล์ `data/thai_geo_centroids.json` (7,400+ ตำบล / 928 อำเภอ / 77 จังหวัด พร้อม `lat, lng` + Alias จังหวัดเช่น `อยุธยา`) เพื่อแยกคำติดกันทั่วไทยและได้พิกัดศูนย์กลางตำบลทันทีแม้ไม่มีทรัพย์ในตำบลนั้น, คำนวณ Haversine เทียบทรัพย์ที่มีพิกัดทั้งหมด (cast `float()` PAMCO) เพื่อ Fallback **ข้ามจังหวัดที่ใกล้ที่สุด** (เช่น คานหาม → วังน้อย / บางปะอิน / หนองแค สระบุรี พร้อมระยะ กม.), และให้ `catalog.html` รองรับ `?q=&province=&cat=&lat=&lng=` + bump `sw.js`
- **Option C: Gemini NLU Location Extractor + External Geocoding Fallback**
  - ใช้ Gemini สกัดเจตนาและทำเลจากทุกประโยคแทน Regex, เรียก External Geocoding API (เช่น Nominatim/Google) หาพิกัดเมื่อไม่พบทรัพย์ตรงทำเลแล้วคำนวณ Haversine, ส่งลิงก์ `catalog.html` แบบ `?ids=` หรือ `?q=&province=&cat=` + bump `sw.js`

---

## 📊 ตารางให้คะแนนทางเลือก (เต็ม 10 คะแนน/ด้าน)

| ทางเลือก (Options) | Sena (เสธฯ): โครงสร้าง & ตรงโจทย์ | Syb/Hai (ปฏิบัติ): ความเร็ว & ความง่าย | MrX (ตรวจสอบ): ความปลอดภัย & ไร้ Bug | คะแนนรวม (30) |
| :--- | :---: | :---: | :---: | :---: |
| **Option A:** Quick Regex + In-Memory Geo & Province Fallback | 6 | 9 | 7 | **22** |
| **Option B:** Static Thai Tambon Centroids + Cross-Province Haversine | 9 | 7 | 9 | **25** |
| **Option C:** Gemini NLU + External Geocoding Fallback | 7 | 5 | 4 | **16** |

## 📝 เหตุผลประกอบ (จำกัดคนละ 1 บรรทัดต่อ 1 ทางเลือก)
* **Option A:**
  * **Sena:** ทำเร็วและไม่เพิ่มไฟล์ข้อมูลใหม่ แต่ Fallback ข้ามจังหวัดนอก 68 โซนยังไม่ตรงโจทย์ที่พี่ต้นต้องการ
  * **Syb/Hai:** แก้เฉพาะจุดในโค้ดเดิมได้เลย ไม่ต้องสร้างหรือดูแลไฟล์พิกัด 7,400 ตำบล
  * **MrX:** ไม่มี External API ที่เสี่ยงล่ม แต่ข้อมูลตำบลจำกัดแค่ที่มีในคลังและ Centroid มีแค่ 68 โซน เสี่ยงจับคู่ตำบลซ้ำชื่อผิดจังหวัดหรือได้ทรัพย์คนละฟากจังหวัดเมื่อ fallback
* **Option B:**
  * **Sena:** ตรงโจทย์ระยะยาว 100% ทั้งแยกคำติดกันทั่วไทยและหาทรัพย์ใกล้สุดข้ามจังหวัดแบบ Zero-latency ไม่พึ่ง External API
  * **Syb/Hai:** โค้ด Haversine + Greedy Match เขียนไม่ยาก แต่ต้องเตรียมชุดข้อมูลพิกัดตำบลทั่วไทยให้ครบและถูกต้อง
  * **MrX:** Deterministic 100% ทำงานใน Memory ไม่พึ่ง API ภายนอก ลดความเสี่ยง Timeout/Hallucination แต่ต้องตรวจความถูกต้องของไฟล์พิกัดตำบลซ้ำข้ามจังหวัดและการ cast `float()` พิกัด PAMCO ให้รัดกุม
* **Option C:**
  * **Sena:** ยืดหยุ่นด้านภาษาธรรมชาติสูงสุด แต่เพิ่ม Latency และความเสี่ยงจาก External API rate limit ในจุดที่ควรตอบไว
  * **Syb/Hai:** ต้องผูก External Geocoding API เพิ่มจุดพัง, timeout, และจัดการ rate limit ของ Render/LINE
  * **MrX:** เสี่ยงสูงสุดจาก Gemini latency/hallucination ชื่อทำเล, External Geocoding rate limit/timeout จน replyToken LINE หมดอายุ, และความเสี่ยง URL `?ids=` ยาวเกินกำหนดครับ

---
## 👑 คำสั่งตัดสินใจของแม่ทัพ (Human Approval Gate)
- [ ] เลือก Option A
- [ ] เลือก Option B
- [ ] เลือก Option C
**คำสั่งเพิ่มเติม:** 
