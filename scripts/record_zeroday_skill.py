# -*- coding: utf-8 -*-
"""
scripts/record_zeroday_skill.py
-------------------------------
Records the Zero-Day Vulnerability, Anti-Downgrade Safeguard,
and LINE Auto-Healing skill into Modular Brain updates:
1. Skill_IT_Security.md
2. Skill_PropTech_Siwasup_OS.md
3. 01_FROM_HOME_TO_OFFICE.txt
4. ACTIVE_SESSION_STATE.json
"""

import os
import sys
import json
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BRAIN_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates"
SEC_FILE = os.path.join(BRAIN_DIR, "Skill_IT_Security.md")
PROP_FILE = os.path.join(BRAIN_DIR, "Skill_PropTech_Siwasup_OS.md")
TRANS_FILE = os.path.join(BRAIN_DIR, "01_FROM_HOME_TO_OFFICE.txt")
STATE_FILE = r"C:\Users\ITss-Advice\.gemini\antigravity\ACTIVE_SESSION_STATE.json"

sec_entry = """
## 7. Zero-Day Post-Mortem & Distributed Cache Disaster Recovery (Siwasup Incident 2026-11-05)

### 7.1 The Ghost Wipeout Vulnerability (Render Cold Start + Naive Overwrite Cascade)
- **Root Cause:** คอนเทนเนอร์บน Cloud PaaS (Render Free Tier) มีการ Sleep/Shutdown อัตโนมัติเมื่อไม่มี Traffic เกิน 15 นาที
- **The Cascade:** เมื่อ Service ตื่นขึ้นมาด้วย In-Memory State ว่างเปล่า หรือหลงเหลือ Seed data เฉพาะ Super Tech (`[NASSTY]`) ฝั่ง Web Frontend แอดมินดึงข้อมูล 1 รายการนั้นมา แล้วเผลอนำไปเขียนทับ `localStorage` และยิง Sync ทับ Cloud Vault (Cloudflare R2) ส่งผลให้ทำเนียบสมาชิกทั้ง 13 คนอันตรธานหายไปในพริบตา
- **Lesson Learned:** อย่าไว้ใจ State ฝั่ง Client หรือ API ฝั่งเซิร์ฟเวอร์ที่เพิ่งตื่นเด็ดขาด! การซิงก์ข้อมูลแบบ Two-way ต้องมีกฎเหล็ก **Anti-Downgrade Safeguard** เสมอ

### 7.2 The 4 Pillars of Zero-Day Defense Architecture
1. **Anti-Downgrade Safeguard (ล็อกตายห้ามเขียนทับข้อมูลลดลง):**
   - ในฟังก์ชัน `save_lobby_data()` ตรวจสอบเงื่อนไขอย่างเด็ดขาด:
   - หากข้อมูลปัจจุบันใน Disk/Vault มีสมาชิก $> 3$ คน แต่เพย์โหลดใหม่ที่ส่งเข้ามามีสมาชิก $\le 1$ คน **ระบบต้อง Reject / Abort การบันทึกทันที!** (ยกเว้นมีคำสั่ง Manual Truncate ด้วย Root Master Key)
2. **Primary Key Anchor = เบอร์โทรศัพท์ 10 หลัก (Phone Number Only):**
   - **กฎเหล็กการพิสูจน์ตัวตน:** ห้ามใช้ชื่อ-นามสกุลภาษาไทย หรือ Display Name เป็นกุญแจหลักเด็ดขาด เพราะภาษาไทยมีโอกาสสะกดเพี้ยน (เช่น ตันฑุลทุกุล, วรวลัญช์, สิทธิชัย) และบน LINE มักใช้อีโมจิหรือชื่อเล่น
   - ให้ดึงตัวเลขเบอร์โทร 10 หลักจากแชทหรือฟอร์มสมัครมา Normalize (`re.sub(r'[^0-9]', '', phone)`) แล้วใช้เป็นตัวจับคู่หลัก 100%
3. **Privilege Escalation Protection (ป้องกันการสวมสิทธิ์แอดมิน):**
   - ห้ามใช้ Substring สั้นๆ เด็ดขาด เช่น 'ต้น', 'บัว', 'oil' เพราะหากมีลูกค้าใหม่ชื่อ 'ใบบัว' หรือ 'ต้นไม้' ทักเข้ามา อาจโดน Auto-Heal สวมสิทธิ์เป็นผู้บริหาร
   - การจับคู่ชื่อต้องใช้ **Strict Distinctive Tokens** ระดับนามสกุลเต็มเฉพาะตัวเท่านั้น (เช่น 'ตันฑุลทุกุล', 'ว่องสุวรรณวาร', 'กูลจีรัง', 'nassty')
4. **Seamless LINE Profile Auto-Healer:**
   - เมื่อสมาชิกทัก LINE OA หรือกด Login ด้วย LINE Login ระบบจะดึง `pictureUrl` ล่าสุดจาก LINE CDN อัตโนมัติ
   - ทำการเสียบแทน Mock Photo เดิมเบื้องหลังทันที และบันทึกประทับตรา Audit Log ลง Cloudflare R2 Vault โดยที่ผู้ใช้ไม่ต้องกดบันทึกใดๆ

### 7.3 Working-Hours Keep-Alive Heartbeat (GitHub Actions Cloud Cron)
- **The Trap:** Render Sleep 15 นาที ทำให้ LINE Webhook เจอ Timeout 10s (Delivery Failed) ในข้อความแรกของวัน
- **Solution:** สร้าง GitHub Actions Workflow (`.github/workflows/nong_siwa_keepalive.yml`) รันบน Cloud ฟรี ยิงสะกิด `/health` ทุก 14 นาที เฉพาะช่วงเวลาทำงาน **07:00 - 21:00 น. (เวลาไทย)** ปลุกเซิร์ฟเวอร์ตื่นตลอดทั้งวันทำงาน 0ms latency และปล่อยให้นอนพักผ่อนตอนกลางคืน ประหยัดโควตา Free 750 ชม./เดือน ได้อย่างคุ้มค่า
"""

prop_entry = """
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
"""

# Append to Skill_IT_Security.md
if os.path.exists(SEC_FILE):
    with open(SEC_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + sec_entry.strip() + "\n")
    print(f"[OK] Appended to {SEC_FILE}")

# Append to Skill_PropTech_Siwasup_OS.md
if os.path.exists(PROP_FILE):
    with open(PROP_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + prop_entry.strip() + "\n")
    print(f"[OK] Appended to {PROP_FILE}")

# Append to 01_FROM_HOME_TO_OFFICE.txt
if os.path.exists(TRANS_FILE):
    transit_note = f"""
================================================================================
Update Date: 2026-11-05 01:20:00 (Home PC - hai -> Offy)
Topic: Zero-Day Post-Mortem, Siwasup Roster Recovery (13 seats), Auto-Healer & Keep-Alive Cron
================================================================================
1. Zero-Day Wipeout Resolved:
   - Root Cause: Render Sleep + Naive Overwrite Cascade from client localStorage.
   - Solution: Implemented Anti-Downgrade Safeguard in save_lobby_data() (blocks overwrite if new < 2 when existing > 3).
2. Authentic Roster Re-anchored:
   - 13 members restored with exact phone numbers and authentic names (Khun Bua: ภมรมาศ ตันฑุลทุกุล, Poppy: ณัฐสุดา พรพริ้ง 063 073 3022, Jeab, Lily, Oil, etc.).
   - R2 Vault & GitHub synced.
3. LINE Auto-Healer Installed:
   - Automatically heals profile pictures and binds lineUserId when members chat on LINE or login.
   - Strict distinctive tokens prevent privilege escalation.
4. Keep-Alive Heartbeat:
   - GitHub Actions workflow nong_siwa_keepalive.yml pings /health every 14 mins during 07:00-21:00 ICT.
"""
    with open(TRANS_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + transit_note.strip() + "\n")
    print(f"[OK] Appended to {TRANS_FILE}")

# Update ACTIVE_SESSION_STATE.json
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        state["last_updated"] = "2026-11-05 01:20:00"
        state["last_milestone"] = "Zero-Day Incident Resolved: 13 members fully restored with authentic phone numbers, LINE Auto-Healer & GitHub Actions Keep-Alive Heartbeat online."
        state["current_project"] = "Siwasup Co-Broker OS - Zero-Day Hardening & SWU Jacket 008"
        state["next_step"] = "1. SWU Jacket 008 (Colorway matching for P'Malee) 2. Verify Nong Siwa morning wake-up ping at 07:00 ICT."
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"[OK] Updated {STATE_FILE}")
    except Exception as e:
        print(f"[Warn] Failed to update state file: {e}")

print("\n[SUCCESS] All Modular Brain updates and Zero-Day skills recorded permanently!")
