# Skill: Siwasup Co-Broker OS - Master Knowledge Hub & Router
`[Triggers: Siwasup OS, PropTech, ศิวาทรัพย์, Co-Broker, กูล, เจี๊ยบ, วรินทร, บัว, ลิลลี่, SW001]`

---

## 🧭 Executive Overview & Architecture Philosophy
**Siwasup Co-Broker OS** คือระบบปฏิบัติการอสังหาริมทรัพย์และตัวแทนร่วม (PropTech Operating System) ที่พัฒนาขึ้นโดย **คุณณัฐ ระวังภัย (Ton / NASSTY - Senior Technology Architect)** ร่วมกับ **คุณวรินทร กูลจีรัง (CEO - Gool / Jeab)** และทีมบริหารศิวาทรัพย์ แอสเซท

### 🏛️ กฎเหล็กสถาปัตยกรรม (Architectural Golden Rules):
1. **Deterministic Identity > Heuristic Guessing (ระบบใหญ่ห้าม AI เดาเอง)**:
   - สมาชิกทุกคนต้องยืนยันตัวตนด้วย **LINE UID (`sub`)** หรือ **เบอร์โทร OTP** เป็นหลัก ห้ามใช้ AI Fuzzy Matching เดาชื่อ-นามสกุลเองเด็ดขาด
   - ข้อมูลชื่อจริง นามบัตร และยศตำแหน่ง ต้องมาจาก Single Source of Truth (`data/lobby_applicants.json`)
2. **Neutral Fallback Only**:
   - หากข้อมูลยังโหลดไม่เสร็จ ให้แสดง Skeleton / Neutral UI (เช่น "ศิวาทรัพย์ แอสเซท") ห้ามนำชื่อหรือรูปตัวแทนคนอื่นมาแสดงรอเด็ดขาด
3. **Modular Brain Loading**:
   - เพื่อประหยัด Token และป้องกัน Context Clutter ให้เลือกโหลดเฉพาะโมดูลที่เกี่ยวข้องกับงานนั้นๆ ตามสารบัญด้านล่างนี้:

---

## 📂 Modular Skill Registry (แผนผังสกิลย่อย 4+1 เสาหลัก)

| โมดูลสกิล | ไฟล์จัดเก็บ | ขอบเขตความรู้ & Trigger Keywords |
|---|---|---|
| **1. Legal & Governance** | [`Skill_Siwasup_Legal_Shield.md`](file:///G:/Twin_Brain/Skill_Siwasup_Legal_Shield.md) | **เกราะคุ้มครองสัญญาและสิทธิ์:** ระบบตั๋วพาชม (Viewing Pass), Geofencing, กลไกป้องกันการตัดหน้า (Anti-Side-Selling), การเจรจาต่อราคา (3 Tier Offer), กฎเหล็ก PDPA, ระบบ 3 เสือ-อินทรี-กรีฟอน |
| **2. Field Operations** | [`Skill_Siwasup_Field_Ops.md`](file:///G:/Twin_Brain/Skill_Siwasup_Field_Ops.md) | **ปฏิบัติการหน้างานจริง:** Master Keybox ท่าข้าม 12, ระบบคิวเปิดบ้าน 2 รอบ/วัน, การส่งมอบกุญแจ (Key-Alike), ยุทธศาสตร์ "นกฮูก" (Introvert Closer) vs "เหยี่ยว" (Field Hawk) |
| **3. Business Synergy** | [`Skill_Siwasup_Business_Synergy.md`](file:///G:/Twin_Brain/Skill_Siwasup_Business_Synergy.md) | **พันธมิตรและสถาบันการเงิน:** KKP Propify Curated Feed & 4-Step SOP, แผนเจาะพอร์ตยักษ์ KBANK K-Property, Remora Protocol (ยุทธการเหาฉลาม), จิตวิทยาผู้บริหาร ต้น & กูล, กลยุทธ์พอร์ต 30/70 |
| **4. Tech Pipeline** | [`Skill_Siwasup_Tech_Pipeline.md`](file:///G:/Twin_Brain/Skill_Siwasup_Tech_Pipeline.md) | **วิศวกรรมคลาวด์และข้อมูล:** เครื่องจักรดูดทรัพย์ Multi-Bank (KTB, ALPHA, PAMCO, BAM, JAM, GHB), Ingestion Engine, Cloudflare R2, บอทน้องศิวา v2 (LINE OA), Hybrid State Machine |
| **5. Code QA Guardrails** | [`Skill_Argon_QA_Guardrails.md`](file:///G:/Twin_Brain/Skill_Argon_QA_Guardrails.md) | **กฎเหล็กวิศวกรรมซอฟต์แวร์:** ดักจับจุดบอด JS Scope, Duplicate Declarations, Base64 URI Bloat, Schema Sync, Mobile Executive Cards, Zero-Day Recovery |

---

## 🔗 Quick Links & Production Endpoints
* **Production Catalog (R2)**: `https://assets.siwasup.com/catalog.html?ref=SW001&view=client`
* **Lobby Waiting Room & Approval Center**: `https://assets.siwasup.com/admin_lobby_manager.html`
* **Agent Registration Portal**: `https://assets.siwasup.com/agent_registration.html`
* **GitHub Repository**: `C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os`
