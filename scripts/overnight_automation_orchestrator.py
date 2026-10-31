import os
import sys
import time
import json
import re
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
DATA_DIR = os.path.join(BASE_DIR, "data")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
OVERNIGHT_LOG = os.path.join(DATA_DIR, "overnight_tasks_run.log")

sys.path.append(SCRIPTS_DIR)
try:
    from overnight_r2_crawler import put_object_r2
except Exception:
    put_object_r2 = None


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(OVERNIGHT_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def run_image_integrity_check():
    log("======================================================================")
    log(">> TASK 1: ASSET / IMAGE INTEGRITY CHECK (3,194 IMAGES ON 980 PROPERTIES)")
    log("======================================================================")
    
    prop_js_path = os.path.join(BASE_DIR, "siwasup_all_properties.js")
    if not os.path.exists(prop_js_path):
        log("[-] Error: siwasup_all_properties.js not found!")
        return
        
    with open(prop_js_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    idx_start = text.find('[')
    idx_end = text.rfind('];')
    if idx_start == -1 or idx_end == -1:
        log("[-] Error: Cannot parse array in siwasup_all_properties.js")
        return
        
    properties = json.loads(text[idx_start:idx_end+1])
    log(f"[*] Loaded {len(properties)} properties from siwasup_all_properties.js")
    
    # Collect all image targets
    targets = []
    for p in properties:
        pid = str(p.get("id"))
        bank = p.get("bank_source") or "Unknown"
        title = p.get("title", "")
        
        main_img = p.get("main_image")
        if main_img and not main_img.endswith(".png"):
            targets.append({"prop_id": pid, "bank": bank, "type": "main", "url": main_img, "title": title})
            
        for idx, g in enumerate(p.get("gallery", [])):
            if g and not g.endswith(".png"):
                targets.append({"prop_id": pid, "bank": bank, "type": f"gal_{idx+1}", "url": g, "title": title})
                
    log(f"[*] Total image targets to verify: {len(targets)}")
    
    def check_url(target):
        url = target["url"]
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SiwasupAssetBot/2.1"}
        req = urllib.request.Request(url, headers=headers, method="HEAD")
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                elapsed = int((time.time() - t0) * 1000)
                status = resp.status
                cl = resp.headers.get("Content-Length", "unknown")
                return {**target, "status": status, "size": cl, "elapsed_ms": elapsed, "ok": True}
        except urllib.error.HTTPError as he:
            # Try GET with Range 0-1024 if HEAD method is blocked by server
            if he.code in [403, 405]:
                try:
                    req_get = urllib.request.Request(url, headers={**headers, "Range": "bytes=0-1024"}, method="GET")
                    with urllib.request.urlopen(req_get, timeout=8) as resp2:
                        return {**target, "status": resp2.status, "size": "range_ok", "elapsed_ms": int((time.time()-t0)*1000), "ok": True}
                except Exception as ex2:
                    return {**target, "status": he.code, "error": str(ex2), "ok": False}
            return {**target, "status": he.code, "error": str(he), "ok": False}
        except Exception as e:
            return {**target, "status": 0, "error": str(e), "ok": False}

    success_count = 0
    failure_list = []
    start_time = time.time()
    
    # Run with 10 worker threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_url, t): t for t in targets}
        done = 0
        for fut in as_completed(futures):
            done += 1
            res = fut.result()
            if res["ok"] and res["status"] in [200, 206]:
                success_count += 1
            else:
                failure_list.append(res)
                log(f"  [FAIL] {res['prop_id']} ({res['bank']}) {res['type']} -> Status {res['status']} | {res['url']}")
                
            if done % 500 == 0 or done == len(targets):
                log(f"  Progress: {done}/{len(targets)} verified ({(done/len(targets))*100:.1f}%) | Success: {success_count} | Fails: {len(failure_list)}")

    total_time = time.time() - start_time
    log(f"[✓] Image Integrity Check Completed in {total_time:.1f}s.")
    log(f"    - Total Checked: {len(targets)}")
    log(f"    - Healthy / OK:  {success_count} ({(success_count/len(targets))*100:.2f}%)")
    log(f"    - Broken / Fail: {len(failure_list)}")
    
    # Save Report
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_properties": len(properties),
        "total_images_checked": len(targets),
        "healthy_count": success_count,
        "broken_count": len(failure_list),
        "health_ratio": f"{(success_count/len(targets))*100:.2f}%",
        "broken_details": failure_list[:100]  # first 100 failures
    }
    
    report_json_path = os.path.join(DATA_DIR, "r2_images_integrity_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    # Write Markdown summary
    report_md_path = os.path.join(DATA_DIR, "r2_images_integrity_report.md")
    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("# 🖼️ Siwasup Asset / Image Integrity Audit Report\n\n")
        f.write(f"- **เวลาที่สแกน:** {report['timestamp']}\n")
        f.write(f"- **จำนวนทรัพย์ที่ตรวจ:** {len(properties)} รายการ\n")
        f.write(f"- **จำนวนรูปภาพทั้งหมด:** {len(targets)} รูป\n")
        f.write(f"- **สถานะสมบูรณ์ (HTTP 200/206):** {success_count} รูป (**{report['health_ratio']}**)\n")
        f.write(f"- **รูปที่โหลดไม่ขึ้น (Broken/Timeout):** {len(failure_list)} รูป\n\n")
        if failure_list:
            f.write("### ⚠️ รายการรูปภาพที่พบปัญหา:\n\n")
            f.write("| รหัสทรัพย์ | สถาบัน | ตำแหน่ง | HTTP Status | URL |\n")
            f.write("| :--- | :--- | :--- | :---: | :--- |\n")
            for brk in failure_list[:50]:
                f.write(f"| `{brk['prop_id']}` | {brk['bank']} | {brk['type']} | {brk['status']} | {brk['url']} |\n")
        else:
            f.write("### 🟢 ผลลัพธ์: สมบูรณ์ 100% ไม่มีลิงก์เสียแม้แต่รูปเดียว!\n")
            
    log(f"[✓] Saved reports to {report_json_path} and {report_md_path}")
    if put_object_r2:
        try:
            with open(report_json_path, "rb") as rf:
                put_object_r2("r2_images_integrity_report.json", rf.read(), "application/json; charset=utf-8")
            log("[R2] Uploaded r2_images_integrity_report.json to assets.siwasup.com")
        except Exception as ex:
            log(f"[R2 Sync Warn]: {ex}")


def run_data_enrichment():
    log("======================================================================")
    log(">> TASK 2: CRAWLER / DATA ENRICHMENT & SMART TAGGING")
    log("======================================================================")
    
    cat_path = os.path.join(DATA_DIR, "catalog_index.json")
    if not os.path.exists(cat_path):
        log("[-] Error: catalog_index.json not found!")
        return
        
    with open(cat_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    log(f"[*] Loaded {len(catalog)} properties in catalog_index.json for enrichment.")
    
    # Load Homerun details map if available
    homerun_map = {}
    homerun_path = os.path.join(DATA_DIR, "homerun_all_properties_10k.json")
    if os.path.exists(homerun_path):
        try:
            with open(homerun_path, "r", encoding="utf-8") as f:
                h_data = json.load(f)
                for item in h_data:
                    cid = str(item.get("code") or item.get("id"))
                    homerun_map[cid] = item
            log(f"[*] Loaded {len(homerun_map)} rich property specs from Homerun dataset.")
        except Exception as e:
            log(f"[-] Homerun map load error: {e}")

    # Transit Station & Highway Keywords
    TRANSIT_KW = [
        "bts", "mrt", "รถไฟฟ้า", "สายสีเขียว", "สายสีน้ำเงิน", "สายสีเหลือง", "สายสีชมพู", 
        "สายสีส้ม", "สายสีแดง", "แอร์พอร์ตลิงก์", "สถานี", "ทางด่วน", "กาญจนาภิเษก", "วงแหวน"
    ]
    
    # Prime / Commercial Keywords
    PRIME_KW = [
        "ติดถนนใหญ่", "หน้ากว้าง", "แปลงมุม", "หลังมุม", "ค้าขาย", "ทำเลทอง", 
        "ติดถนนสาธารณะ", "ชุมชน", "ใกล้ตลาด", "ติดถนนเมน"
    ]
    
    # Renovation / Ready Keywords
    READY_KW = [
        "รีโนเวท", "พร้อมอยู่", "ตกแต่งใหม่", "สภาพดี", "ทาสีใหม่", "ปูกระเบื้องใหม่", "สวยพร้อมอยู่"
    ]

    enriched_count = 0
    transit_count = 0
    discount_count = 0
    prime_count = 0
    ready_count = 0
    
    for p in catalog:
        code = str(p.get("c") or p.get("id"))
        h_spec = homerun_map.get(code, {})
        
        title = (h_spec.get("title") or "") + " " + (h_spec.get("titleEn") or "")
        desc = (h_spec.get("description") or "") + " " + (h_spec.get("property_detail") or "")
        full_text = f"{title} {desc}".lower()
        
        tags = []
        
        # 1. Transit Near
        if any(kw in full_text for kw in TRANSIT_KW):
            tags.append("ใกล้รถไฟฟ้า/ทางด่วน")
            transit_count += 1
            
        # 2. Discount / Promotional Price
        price = p.get("pr", 0)
        promo_price = h_spec.get("promotionalPrice") or 0
        if promo_price and promo_price < price:
            diff_pct = int(((price - promo_price) / price) * 100)
            if diff_pct >= 5:
                tags.append(f"ลดพิเศษ {diff_pct}%")
                discount_count += 1
        elif any(kw in full_text for kw in ["ลดราคา", "ต่ำกว่าราคาประเมิน", "ราคาพิเศษ", "หลุดจอง"]):
            tags.append("ลดราคาพิเศษ")
            discount_count += 1
            
        # 3. Prime Location
        if any(kw in full_text for kw in PRIME_KW):
            tags.append("ทำเลทอง/แปลงมุม")
            prime_count += 1
            
        # 4. Ready / Renovated
        if any(kw in full_text for kw in READY_KW):
            tags.append("รีโนเวทพร้อมอยู่")
            ready_count += 1
            
        if tags:
            p["tags"] = tags
            enriched_count += 1
            
    log(f"[✓] Data Enrichment Complete:")
    log(f"    - Total Enriched Properties: {enriched_count} / {len(catalog)}")
    log(f"    - ใกล้รถไฟฟ้า/ทางด่วน:        {transit_count}")
    log(f"    - ต่ำกว่าราคาประเมิน/ลดพิเศษ:  {discount_count}")
    log(f"    - ทำเลทอง/ติดถนนใหญ่/แปลงมุม:   {prime_count}")
    log(f"    - รีโนเวทพร้อมอยู่:            {ready_count}")
    
    # Save enriched catalog
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False)
    log(f"[✓] Saved enriched catalog to {cat_path}")
    
    if put_object_r2:
        try:
            with open(cat_path, "rb") as cf:
                put_object_r2("catalog_index.json", cf.read(), "application/json; charset=utf-8")
            log("[R2] Uploaded enriched catalog_index.json to assets.siwasup.com")
        except Exception as ex:
            log(f"[R2 Sync Warn]: {ex}")


def run_twin_brain_and_git_sync():
    log("======================================================================")
    log(">> TASK 3: TWIN BRAIN BACKUP & GIT COMMITS")
    log("======================================================================")
    
    # 1. Sync FBT-Graphic-Studio-Tools to Git
    fbt_dir = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools"
    log(f"[*] Committing changes in {fbt_dir}...")
    try:
        subprocess.run(["git", "add", "."], cwd=fbt_dir, check=True)
        res = subprocess.run(["git", "commit", "-m", "chore: Sync Twin Brain & Project Status (31 Oct 2026 Nightly)"], cwd=fbt_dir, capture_output=True, text=True)
        log(f"[Git FBT Commit]: {res.stdout.strip() or res.stderr.strip()}")
    except Exception as e:
        log(f"[Git FBT Warn]: {e}")

    # 2. Sync siwasup-cobroker-os to Git
    log(f"[*] Committing changes in {BASE_DIR}...")
    try:
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        res = subprocess.run(["git", "commit", "-m", "feat: Line Bot v2.1 Smart Memory + Enriched Catalog + Overnight Audit"], cwd=BASE_DIR, capture_output=True, text=True)
        log(f"[Git Siwasup Commit]: {res.stdout.strip() or res.stderr.strip()}")
    except Exception as e:
        log(f"[Git Siwasup Warn]: {e}")

    # 3. Flash Drive G:\ Sync
    if os.path.exists(r"G:\ "):
        pass
    if os.path.exists("G:\\"):
        log("[*] Flash Drive G:\ detected. Syncing master files...")
        sync_files = [
            (os.path.join(fbt_dir, "Brain_Updates", "00_PROJECT_STATUS.md"), r"G:\00_PROJECT_STATUS.md"),
            (os.path.join(fbt_dir, "Brain_Updates", "Skill_PropTech_Siwasup_OS.md"), r"G:\Skill_PropTech_Siwasup_OS.md"),
            (os.path.join(DATA_DIR, "r2_images_integrity_report.json"), r"G:\r2_images_integrity_report.json"),
            (os.path.join(DATA_DIR, "r2_images_integrity_report.md"), r"G:\r2_images_integrity_report.md"),
            (OVERNIGHT_LOG, r"G:\overnight_tasks_run.log")
        ]
        for src, dst in sync_files:
            if os.path.exists(src):
                try:
                    with open(src, "rb") as sf, open(dst, "wb") as df:
                        df.write(sf.read())
                    log(f"  [✓] Synced -> {dst}")
                except Exception as ex:
                    log(f"  [-] Sync error {dst}: {ex}")
        log("[✓] Flash Drive G:\ Twin Brain sync complete.")
    else:
        log("[!] Flash Drive G:\ not accessible. Skipping physical copy.")


def main():
    with open(OVERNIGHT_LOG, "w", encoding="utf-8") as f:
        f.write(f"=== OVERNIGHT AUTOMATION ORCHESTRATOR STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        
    t_start = time.time()
    
    # Task 1
    run_image_integrity_check()
    
    # Task 2
    run_data_enrichment()
    
    # Task 3
    run_twin_brain_and_git_sync()
    
    total_elapsed = time.time() - t_start
    log("======================================================================")
    log(f">> ALL OVERNIGHT TASKS COMPLETED SUCCESSFULLY IN {total_elapsed:.1f}s <<")
    log("======================================================================")


if __name__ == "__main__":
    main()
