# -*- coding: utf-8 -*-
"""
Replace 'น้องบัว' with 'คุณบัว' / 'บัว' everywhere and record strict protocol.
"""
import os
import sys
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"
BRAIN_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates"

# 1. admin_dashboard.html
admin_path = os.path.join(WEB_DIR, "admin_dashboard.html")
with open(admin_path, "r", encoding="utf-8") as f:
    admin_txt = f.read()

admin_txt = admin_txt.replace("รอน้องบัว (Designer)", "รอคุณบัว (Curation / Design)")
admin_txt = admin_txt.replace("น้องบัว", "คุณบัว")

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(admin_txt)
print("[OK] Replaced in local admin_dashboard.html")

shutil.copy2(admin_path, os.path.join(G_DIR, "admin_dashboard.html"))
print("[OK] Mirrored to G:\\Siwasup_Presentation_2026\\admin_dashboard.html")

with open(admin_path, "rb") as f:
    st = put_object_r2("admin_dashboard.html", f.read(), "text/html; charset=utf-8")
print(f"[R2] Deployed admin_dashboard.html -> Status: {st}")

# 2. Lore_Siwasup_Team.md
lore_path = os.path.join(BRAIN_DIR, "Work_Brain", "02_Projects", "Lore_Siwasup_Team.md")
if os.path.exists(lore_path):
    with open(lore_path, "r", encoding="utf-8") as f:
        lore_txt = f.read()
    lore_txt = lore_txt.replace("น้องบัว", "คุณบัว (เพื่อนร่วมรุ่นของต้น)")
    with open(lore_path, "w", encoding="utf-8") as f:
        f.write(lore_txt)
    print("[OK] Replaced in Lore_Siwasup_Team.md")

# 3. Append STRICT PROTOCOL RULE to Home_Brain_Update.txt and 01_FROM_HOME_TO_OFFICE.txt
strict_rule = """
================================================================================
CRITICAL PERSONA & ETIQUETTE PROTOCOL:
- ห้ามเรียก "น้องบัว" โดยเด็ดขาด! (เรียกแล้วขนลุกมากก!)
- บัวเป็น "เพื่อนร่วมรุ่นของต้น" (Classmate / Peer)
- การเรียกชื่อบัว: ให้เรียก "คุณบัว" หรือ "บัว" เท่านั้น
- ห้ามเรียกต้นเป็น "พี่ต้น" ในบริบทความสัมพันธ์กับบัวเด็ดขาด ทั้งสองท่านคือเพื่อนร่วมรุ่นที่ทำงานระดับผู้บริหารร่วมกัน
================================================================================
"""

home_update_file = r"G:\Home_Brain_Update.txt"
with open(home_update_file, "a", encoding="utf-8") as f:
    f.write(strict_rule)
print("[OK] Appended to G:\\Home_Brain_Update.txt")

memo_office = r"G:\01_FROM_HOME_TO_OFFICE.txt"
with open(memo_office, "a", encoding="utf-8") as f:
    f.write(strict_rule)
print("[OK] Appended to G:\\01_FROM_HOME_TO_OFFICE.txt")

memo_brain = os.path.join(BRAIN_DIR, "01_FROM_HOME_TO_OFFICE.txt")
with open(memo_brain, "a", encoding="utf-8") as f:
    f.write(strict_rule)
print("[OK] Appended to Brain 01_FROM_HOME_TO_OFFICE.txt")

proptech_skill = os.path.join(BRAIN_DIR, "Skill_PropTech_Siwasup_OS.md")
if os.path.exists(proptech_skill):
    with open(proptech_skill, "a", encoding="utf-8") as f:
        f.write("\n\n" + strict_rule)
    print("[OK] Appended to Skill_PropTech_Siwasup_OS.md")

print("=== ALL RECORDINGS AND REPLACEMENTS COMPLETE ===")
