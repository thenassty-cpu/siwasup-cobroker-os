import os
import shutil
import json
from datetime import datetime, timedelta

REPO_ROOT = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
QUARANTINE_ROOT = r"D:\Recycle_Bin_90Days\Siwasup_OS_Cleansing_20261101"

os.makedirs(QUARANTINE_ROOT, exist_ok=True)

now = datetime.now()
expiry = now + timedelta(days=90)

manifest = {
    "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
    "retention_policy": "90_DAYS_QUARANTINE",
    "expire_at": expiry.strftime("%Y-%m-%d %H:%M:%S"),
    "reason": "Data Cleansing & Repository Streamlining approved by Khun Ton",
    "source_repo": REPO_ROOT,
    "files": []
}

# 1. Backups & Old Logs & PII
BACKUP_FILES = [
    "all_curation_properties.js.bak_20261030",
    "all_curation_properties.json.bak_20261030",
    "index.html.bak",
    "siwasup_all_properties.js.bak",
    "siwasup_all_properties.json.bak",
    "siwasup_viewing_flow_tester.html.bak_pre_slot",
    "scoring_debate_dashboard.html.bak",
    "siwasup_agents.js.PII_FULL_DO_NOT_DEPLOY"
]

# 2. Heavy Raw Data
RAW_DATA_FILES = [
    os.path.join("data", "homerun_all_properties_10k.json"),
    os.path.join("data", "r2_assets_manifest.json"),
    os.path.join("data", "gsb_all_properties.json")
]

# 3. Log files in data/
LOG_FILES = [
    os.path.join("data", "daemon_run.log"),
    os.path.join("data", "ghb_crawler.log"),
    os.path.join("data", "gsb_crawler.log"),
    os.path.join("data", "overnight_crawler.log"),
    os.path.join("data", "overnight_tasks_run.log")
]

# 4. One-off legacy scripts
LEGACY_SCRIPTS = [
    # inspect / find / check
    "inspect_index.py", "inspect_index_2.py", "inspect_modals.py", "inspect_modal_fields.py",
    "inspect_consign.py", "inspect_consign_2.py", "inspect_lines.py", "inspect_lines_2.py",
    "inspect_scb_bkk.py", "inspect_mgm.py", "inspect_top20.py", "inspect_tailwind.py",
    "find_actions.py", "find_dark.py", "find_hero_properties.py", "find_mgm.py", "find_render.py",
    "check_card_render.py", "check_data_init.py", "check_dropdowns.py", "check_load_props.py", "check_render_props.py",
    "show_header.py", "show_header_2.py", "show_render_details.py",
    # patch scripts already applied
    "patch_bank_filters.py", "patch_avatar_illustrator_match.py", "patch_enlarge_circular_emblems.py",
    "patch_daimond_logo_and_clean_name.py", "patch_complete_o3_metrics.py", "patch_o3_research_metrics.py",
    "patch_curator_and_slip.py", "patch_curator_js.py", "patch_curator_ui.py",
    "patch_modals_backdrop.py", "patch_web_fixes.py", "purge_nong_bua.py", "remove_bam_filter.py",
    "restore_100_original.py", "update_modals_and_fix_jumping.py", "fix_backdrop_and_scroll.py"
]

# 5. Redundant HTML / Old Proposals
REDUNDANT_HTML = [
    "scoring_summary_light.html",
    "Siwasup_Proposal_and_Web_Analysis.html",
    "Siwasup_Proposal_and_Web_Analysis.pdf"
]

def safe_move(rel_path, target_subfolder):
    src = os.path.join(REPO_ROOT, rel_path)
    if not os.path.exists(src):
        return
    
    dest_dir = os.path.join(QUARANTINE_ROOT, target_subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    filename = os.path.basename(rel_path)
    dest = os.path.join(dest_dir, filename)
    
    size_bytes = os.path.getsize(src)
    try:
        shutil.move(src, dest)
        manifest["files"].append({
            "rel_path": rel_path,
            "quarantine_dest": os.path.relpath(dest, QUARANTINE_ROOT),
            "size_bytes": size_bytes,
            "moved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"[MOVED] {rel_path} -> {dest_dir} ({size_bytes / 1024:.1f} KB)")
    except Exception as e:
        print(f"[SKIP/LOCKED] {rel_path}: {e}")

print("=== STARTING DATA CLEANSING TO D:\\ RECYCLE BIN (90 DAYS) ===")

# Process Group 1
for f in BACKUP_FILES:
    safe_move(f, "01_Backups_and_PII")

# Process Group 2
for f in RAW_DATA_FILES:
    safe_move(f, "02_Heavy_RawData")

# Process Group 3
for f in LOG_FILES:
    safe_move(f, "01_Backups_and_PII")

# Process Group 4 (Scripts in scripts/)
for s in LEGACY_SCRIPTS:
    safe_move(os.path.join("scripts", s), "03_Legacy_Patch_Scripts")

# Process Group 5
for h in REDUNDANT_HTML:
    safe_move(h, "04_Old_Presentations_and_Drafts")

# Save Manifest
manifest_path = os.path.join(QUARANTINE_ROOT, "RESTORE_MANIFEST.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# Create 1-Click Restore Script
restore_script_content = f'''# 1-CLICK RESTORE SCRIPT FOR SIWASUP CO-BROKER OS
# Run this script if you need to restore any quarantined files back to the repo.
import os, json, shutil

REPO_ROOT = r"{REPO_ROOT}"
QUARANTINE_ROOT = r"{QUARANTINE_ROOT}"
MANIFEST_PATH = os.path.join(QUARANTINE_ROOT, "RESTORE_MANIFEST.json")

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print(f"[*] Restoring {{len(manifest['files'])}} files back to {{REPO_ROOT}}...")
for item in manifest["files"]:
    src = os.path.join(QUARANTINE_ROOT, item["quarantine_dest"])
    dst = os.path.join(REPO_ROOT, item["rel_path"])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"[RESTORED] {{item['rel_path']}}")

print("[OK] All files successfully restored!")
'''

with open(os.path.join(QUARANTINE_ROOT, "RESTORE_ALL.py"), "w", encoding="utf-8") as f:
    f.write(restore_script_content)

# Create README with 90-Day Policy Note
readme_content = f'''# 🗑️ ถังพักข้อมูล 90 วัน (Recycle Bin & Data Cleansing Quarantine)

* **ที่มา:** โครงการ Siwasup Co-Broker OS
* **วันที่ดำเนินการ:** {now.strftime('%d/%m/%Y %H:%M:%S')}
* **วันครบกำหนด 90 วัน (พิจารณาลบถาวร):** {expiry.strftime('%d/%m/%Y')}
* **ผู้ดูแลระบบ / ผู้อนุมัติ:** คุณต้น (NASSTY) & hai (Home AI)

---

## 📂 โครงสร้างโฟลเดอร์:
* `01_Backups_and_PII/` - ไฟล์สำรอง `.bak`, Log เก่า และไฟล์ข้อมูลเดิมที่มี PII เพื่อลดความเสี่ยง PDPA
* `02_Heavy_RawData/` - ข้อมูลดิบขนาดใหญ่ (เช่น 10k homerun 21.4MB, manifest 7.5MB)
* `03_Legacy_Patch_Scripts/` - สคริปต์ One-Off 40+ ไฟล์ที่ใช้งานเสร็จสิ้นแล้ว
* `04_Old_Presentations_and_Drafts/` - สไลด์พรีเซนต์เวอร์ชันแรกและหน้า HTML ทดลองธีม

## 🔄 วิธีกู้คืนไฟล์กลับ Repository:
หากต้องการดึงไฟล์ทั้งหมดกลับเข้าโปรเจกต์เดิม เพียงรัน:
```powershell
python D:\\Recycle_Bin_90Days\\Siwasup_OS_Cleansing_20261101\\RESTORE_ALL.py
```
'''

with open(os.path.join(QUARANTINE_ROOT, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

total_moved = len(manifest["files"])
total_bytes = sum(item["size_bytes"] for item in manifest["files"])
print(f"\n=== CLEANSING COMPLETED ===")
print(f"Total files moved: {total_moved}")
print(f"Total space freed: {total_bytes / (1024 * 1024):.2f} MB")
print(f"Quarantine location: {QUARANTINE_ROOT}")
print(f"Expires on: {expiry.strftime('%Y-%m-%d')} (90 Days)")
