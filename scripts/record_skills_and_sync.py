import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

skill_file = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates\Skill_PropTech_Siwasup_OS.md"
home_update_file = r"G:\Home_Brain_Update.txt"
status_file = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates\00_PROJECT_STATUS.md"

# 2. Append to G:\Home_Brain_Update.txt (Twin Brain Sync)
twin_brain_content = """
================================================================================
Update Date: 2026-10-29 23:25:00 (Home PC - hai)
Topic: PropTech Telemetry, Executive Psychology (Lion vs Eagle), 30/70 Strategy & Modal Fixes
================================================================================
1. Web & CSS Modal Freeze / Vanishing Background Fix:
   - NEVER use `position: fixed; top: -scrollY; width: 100%; height: 100%;` on `body.modal-open`. It causes the document body to jump out of viewport, turning background into a solid flat grey slate.
   - ALWAYS use `body.modal-open { overflow: hidden !important; overscroll-behavior: contain !important; }` to lock scroll without shifting or hiding background content.
   - Backdrop: Use luxury frosted bokeh glass `rgba(15, 23, 42, 0.45)` with `backdrop-filter: blur(6px)`.
   - Add `onerror="this.onerror=null; this.src='...'"` on modal images to prevent freezes from expired SSL (e.g. readyplanet).
   - Removed all outbound 'ดูหน้าเว็บเดิม' links from modals to eliminate friction.

2. PropTech Market Demand Intelligence:
   - Debounced Search Keyword Telemetry (1s debounce) to capture agent search intent.
   - Zero-Result Demand Gap Alert: Flags keywords with 0 matches to identify missing inventory immediately.
   - Dwell Time Tracking: (closeTime - openTime) / 1000 sec.
     * Quick Bounce (<3s): bad cover / overpriced.
     * High-Intent Hot Dwell (>15-30s+): triggers hot lead alert to agent LINE.

3. The 30/70 Inventory Strategy (Overcoming the 'Same Old Stuff' Fatigue for Sales Commander):
   - 30% Curated Legacy Gold: 5-8 verified active properties from original site.
   - 70% Fresh Blood 2026: Fresh listings from 10,000+ SAM / GSB / SCB master vaults tagged with `✦ Fresh Bank NPA 2026` to excite agents.

4. 3-Color Ribbon Protocol for Asset Curation (801 properties total):
   - Red Ribbon: 8 properties removed from live categories (review required).
   - Green Ribbon: 12 new-in properties from homepage.
   - Blue Ribbon: 671 bank NPA items to curate down to Top 20 for Alpha team.

5. Executive Psychology:
   - Lion (Gool): Wants to see the prey, revenue, hierarchy, one-click power, prestige.
   - Eagle (Ton): Wants to see the macro flow, data moat, horizon risks, and leverage.
"""

if os.path.exists(home_update_file):
    with open(home_update_file, 'a', encoding='utf-8') as f:
        f.write(twin_brain_content)
    print(f"[OK] Appended to {home_update_file}")

# 3. Update 00_PROJECT_STATUS.md
status_entry = """
### Update 2026-10-29 (Siwasup OS - 801 Properties Live Audit, Modal Freeze Fixes & Demand Telemetry)
- **Live 100% Match Crawl (allabout-assets.com)**:
  - 801 unique properties mapped across all categories (Single House 25, Townhome 30, Condo 23, Land 14, Commercial 30, NPA 677).
  - 3-Color Ribbon Curation Protocol deployed to `https://assets.siwasup.com/property_curator.html`:
    - 🔴 Red: 8 properties removed from original web (verification needed).
    - 🟢 Green: 12 New-In properties recently added to homepage.
    - 💎 Blue: 671 Bank NPA properties targeted to curate down to Top 20 Hero Deals for Gool's Alpha Agents.
- **Frontend & Modal Architecture Hardened**:
  - Solved vanishing grey background bug by replacing `position: fixed` on body with `overflow: hidden; overscroll-behavior: contain`.
  - Luxury Frosted Bokeh Glass backdrop (`rgba(15, 23, 42, 0.45)`, `blur(6px)`).
  - Removed 'ดูหน้าเว็บเดิม' button from all modals; added `onerror` fallback against Readyplanet expired SSL.
- **Twin Brain & Skill Documentation**:
  - Appended Section 13 to `Skill_PropTech_Siwasup_OS.md` and synced to `G:\Home_Brain_Update.txt`.
"""

with open(status_file, 'a', encoding='utf-8') as f:
    f.write(status_entry)
print(f"[OK] Appended to {status_file}")

print("=== ALL SKILLS AND BRAIN UPDATES RECORDED SUCCESSFULLY ===")
