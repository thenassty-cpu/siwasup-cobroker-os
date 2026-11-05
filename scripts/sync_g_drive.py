# -*- coding: utf-8 -*-
import os
import shutil
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

src_brain = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates"
dst_twin = r"G:\Twin_Brain"
os.makedirs(dst_twin, exist_ok=True)

# 1. Sync all modular brain files to G:\Twin_Brain
for f in os.listdir(src_brain):
    s = os.path.join(src_brain, f)
    d = os.path.join(dst_twin, f)
    if os.path.isfile(s):
        shutil.copy2(s, d)

# 2. Update G:\Home_Brain_Update.txt
home_brain_txt = r"G:\Home_Brain_Update.txt"
update_note = """
================================================================================
Update Date: 2026-11-05 11:10:00 (Home PC - hai -> Flash Drive G:)
Topic: Zero-Day Incident Resolution, Anti-Downgrade Defense, and A2G804 Catalog Assets
================================================================================
1. Zero-Day Post-Mortem and Defense:
   - Fixed Render Cold Start + Client Overwrite cascade on Siwasup OS.
   - Hardened with Anti-Downgrade Safeguard, LINE Real-time Auto-Healer, and GitHub Actions Keep-Alive Heartbeat (07:00-21:00 ICT).
   - Roster locked with 13 members (Khun Bua: Pamornmas Tantulathukul, Poppy: 063-073-3022, etc.).

2. FBT Production and Catalog Reference (A2G804):
   - Located existing production patterns for A2G804 (Jacket and Pants Tracksuit):
     * G:\\#Malee\\2569\\Jacket_BlueGold_Ref_A2G804_Folder\\Jacket_BlueGold_Ref_A2G804.ai
     * G:\\17-4-69\\จุฬา_A2G804_Folder\\จุฬา_A2G804.ai
     * G:\\4-2-68\\Tracksuit_ทีมชาติA2G804_ดำ-ทอง-ขาว_Folder\\Tracksuit_ทีมชาติA2G804_ดำ-ทอง-ขาว.ai
   - P'Malee can adapt this existing pattern for SWU Elementary to bypass new pattern grading and meet tight factory deadlines!
"""

with open(home_brain_txt, "a", encoding="utf-8") as f:
    f.write(update_note.strip() + "\n\n")

# 3. Update G:\01_FROM_HOME_TO_OFFICE.txt
shutil.copy2(os.path.join(src_brain, "01_FROM_HOME_TO_OFFICE.txt"), r"G:\01_FROM_HOME_TO_OFFICE.txt")

# 4. Update G:\ACTIVE_SESSION_STATE.json
shutil.copy2(r"C:\Users\ITss-Advice\.gemini\antigravity\ACTIVE_SESSION_STATE.json", r"G:\ACTIVE_SESSION_STATE.json")

print("[SUCCESS] Twin Brain sync to G: completed successfully!")
