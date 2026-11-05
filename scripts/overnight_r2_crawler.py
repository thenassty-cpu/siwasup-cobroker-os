import urllib.request
import ssl
import json
import hashlib
import hmac
from datetime import datetime
import os
import sys
import time

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# R2 Credentials
ACCESS_KEY = "21ea6725b31de7a08eb4e15c89181c56"
SECRET_KEY = "ec0b53061b1ca77e0f87b534194dd247949ed82679a591d5eda9752fa14f784a"
ACCOUNT_ID = "b2f4f44870ea14a9a5114dfb6163b48c"
BUCKET = "siwasup-npa-assets"
ENDPOINT = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
CDN_BASE = "https://assets.siwasup.com"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://homerunplatform.com',
    'Referer': 'https://homerunplatform.com/'
}

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def put_object_r2(object_key, data_bytes, content_type="image/jpeg"):
    now = datetime.utcnow()
    amz_date = now.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = now.strftime('%Y%m%d')
    region = "auto"
    service = "s3"
    
    host = f"{ACCOUNT_ID}.r2.cloudflarestorage.com"
    payload_hash = hashlib.sha256(data_bytes).hexdigest()
    
    canonical_uri = f"/{BUCKET}/{object_key}"
    canonical_querystring = ""
    canonical_headers = f"content-type:{content_type}\nhost:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
    signed_headers = "content-type;host;x-amz-content-sha256;x-amz-date"
    
    canonical_request = f"PUT\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    
    signing_key = get_signature_key(SECRET_KEY, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    authorization_header = f"{algorithm} Credential={ACCESS_KEY}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    
    url = f"{ENDPOINT}/{BUCKET}/{object_key}"
    req = urllib.request.Request(url, data=data_bytes, method="PUT")
    req.add_header('Host', host)
    req.add_header('Content-Type', content_type)
    req.add_header('x-amz-date', amz_date)
    req.add_header('x-amz-content-sha256', payload_hash)
    req.add_header('Authorization', authorization_header)
    
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        return resp.status

def log_msg(msg, log_fp=None):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    if log_fp:
        try:
            with open(log_fp, 'a', encoding='utf-8') as f:
                f.write(line + "\n")
        except Exception:
            pass

# ==============================================================================
# PAMCO PULL — ดูดพอร์ต 1,312 แปลง (ตัดรหัส D ออก) พร้อม status + GPS
# Backend: https://property-api-prod.pamco.co.th
# Media:   https://media.pamco.co.th/
# ==============================================================================

PAMCO_API_BASE  = "https://property-api-prod.pamco.co.th"
PAMCO_MEDIA_BASE = "https://media.pamco.co.th"
PAMCO_PAGE_SIZE  = 10    # server คืน 10 items ต่อหน้าเสมอ (ignore pageSize param)
PAMCO_EXCLUDE_D_PREFIX = True   # ตัดทรัพย์รหัส D (idMarket starts with D) ออกตามคำสั่งกูล
PAMCO_STALE_DAYS       = 14    # ทรัพย์ที่ไม่เจอบน server นานกว่านี้ → auto-hide

PAMCO_HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, */*',
    'Origin': 'https://property.pamco.co.th',
    'Referer': 'https://property.pamco.co.th/assets/results',
}

def _pamco_fetch_page(page: int) -> tuple[list, int]:
    """
    ดึงข้อมูล PAMCO หน้าเดียว
    คืน (items_list, total_count)
    """
    url = f"{PAMCO_API_BASE}/property-new/display?page={page}&pageSize={PAMCO_PAGE_SIZE}"
    req = urllib.request.Request(url, headers=PAMCO_HDRS)
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        raw = r.read().decode('utf-8', errors='ignore')
    d = json.loads(raw)
    if isinstance(d, list):
        return d, len(d)
    items = d.get('list', [])
    total = d.get('total', len(items))
    return items, total


def _pamco_to_record(item: dict) -> dict:
    """
    Normalize PAMCO item → canonical property_master record
    Fields ตรงกับ format ของ homerun pool เพื่อ merge ได้
    """
    market_id = item.get('idMarket', '')    # รหัสทรัพย์ เช่น B13703
    thumb_paths = item.get('thumbnail', [])
    thumb_url = (
        f"{PAMCO_MEDIA_BASE}/{thumb_paths[0]}" if thumb_paths else ""
    )

    price_raw = ""
    lowprice = item.get('lowprice', [])
    if lowprice and isinstance(lowprice[0], dict):
        price_raw = lowprice[0].get('lowprice', '') or ''

    try:
        price_num = int(str(price_raw).replace(',', ''))
    except (ValueError, TypeError):
        price_num = 0

    detail_code = str(item.get('idDetail', ''))
    return {
        "id":           f"PAMCO-{market_id}",
        "code":         market_id,
        "source":       "PAMCO",
        "bank_pool":    "PAMCO",
        "title":        item.get('npaProductTitle', ''),
        "category":     item.get('detail', {}).get('detail', '') if isinstance(item.get('detail'), dict) else '',
        "detail_code":  detail_code,          # "4" = rหัส D → ต้องกรอง
        "price":        price_num,
        "province":     item.get('provinceNameTh', ''),
        "district":     item.get('districtNameTh', ''),
        "sub_district": item.get('subDistrictNameTh', ''),
        "latitude":     item.get('npaProductLatitude', ''),
        "longitude":    item.get('npaProductLongitude', ''),
        "area_sqw":     item.get('npaProductArea', ''),
        "usable_sqm":   item.get('useableArea', ''),
        "landid":       item.get('landid', ''),
        "houseid":      item.get('houseid', ''),
        "street":       item.get('street', ''),
        "soi":          item.get('soi', ''),
        "hgroup":       item.get('hgroup', ''),
        "telAO":        item.get('telAO') or '',
        "slug":         item.get('slug', ''),
        "thumbnail":    thumb_url,
        "media_base":   PAMCO_MEDIA_BASE,
        "thumbnail_path": thumb_paths[0] if thumb_paths else '',
        "status":       "available" if item.get('checker') else "unavailable",
        "last_seen":    datetime.now().isoformat(),
    }


def run_pamco_pull(data_dir: str, log_file: str | None = None) -> dict:
    """
    ดูด PAMCO พอร์ตทั้งหมด → คืน dict keyed by record["id"]
    กรอง detail_code D (idDetail=4) ออกอัตโนมัติ
    """
    log_msg("[PAMCO] Starting pull from property-api-prod.pamco.co.th ...", log_file)

    all_records: dict[str, dict] = {}
    page = 1
    total_known = 9999  # อัปเดตหลังหน้าแรก

    while True:
        for attempt in range(3):
            try:
                items, total_count = _pamco_fetch_page(page)
                if page == 1:
                    total_known = total_count
                    log_msg(f"[PAMCO] Total on server: {total_known}", log_file)
                break
            except Exception as e:
                log_msg(f"[PAMCO] Page {page} attempt {attempt+1} error: {e}", log_file)
                time.sleep(2.0)
        else:
            log_msg(f"[PAMCO] Giving up on page {page} after 3 retries", log_file)
            break

        if not items:
            break

        kept = skipped = 0
        for item in items:
            rec = _pamco_to_record(item)
            # กรองรหัส D (ทรัพย์สิน ไม่ใช่ที่ดิน/บ้าน) ออกตามคำสั่งกูล
            if PAMCO_EXCLUDE_D_PREFIX and rec["code"].upper().startswith("D"):
                skipped += 1
                continue
            all_records[rec["id"]] = rec
            kept += 1

        log_msg(
            f"[PAMCO] Page {page}: {kept} kept, {skipped} skipped (D-code) "
            f"| running total: {len(all_records)}/{total_known}",
            log_file
        )

        # ถ้าได้ครบแล้วหรือไม่มีหน้าต่อไป
        fetched_so_far = (page - 1) * PAMCO_PAGE_SIZE + len(items)
        if fetched_so_far >= total_known or len(items) < PAMCO_PAGE_SIZE:
            break

        page += 1
        time.sleep(0.5)   # gentle pause

    log_msg(f"[PAMCO] Pull complete: {len(all_records)} properties (D-code excluded)", log_file)

    # ------------------------------------------------------------------
    # STALE GUARD
    # เปรียบ fresh pull กับ master file เดิม:
    #   - ทรัพย์ที่เจอใหม่ / เจออยู่ → status=available, last_seen=now
    #   - ทรัพย์ที่หายไปจาก server:
    #       * ถ้า hidden_since < STALE_DAYS → รักษาไว้ status=missing
    #       * ถ้า hidden_since >= STALE_DAYS → status=hidden (ซ่อนจากเว็บ)
    # ------------------------------------------------------------------
    out_path = os.path.join(data_dir, "pamco_property_master.json")

    prev_records: dict = {}
    if os.path.exists(out_path):
        try:
            with open(out_path, encoding='utf-8') as _f:
                prev_records = json.load(_f)
        except Exception:
            pass

    now_iso   = datetime.now().isoformat()
    now_dt    = datetime.now()
    stale_new = stale_hidden = stale_restored = 0

    # ทรัพย์ที่เคยมีแต่ไม่เจอในรอบนี้
    for pid, prev_rec in prev_records.items():
        if pid in all_records:
            # เจออยู่ → รีเซ็ต hidden_since ถ้ามี
            if prev_rec.get("status") in ("missing", "hidden"):
                all_records[pid]["status"] = "available"
                all_records[pid].pop("hidden_since", None)
                stale_restored += 1
            continue

        # ไม่เจอในรอบนี้ — ตรวจ hidden_since
        hidden_since_str = prev_rec.get("hidden_since")
        if hidden_since_str:
            try:
                hidden_since_dt = datetime.fromisoformat(hidden_since_str)
                days_missing = (now_dt - hidden_since_dt).days
            except ValueError:
                days_missing = 0
        else:
            # เพิ่งหายครั้งแรก
            hidden_since_str = now_iso
            days_missing     = 0

        if days_missing >= PAMCO_STALE_DAYS:
            prev_rec["status"]       = "hidden"
            prev_rec["hidden_since"] = hidden_since_str
            stale_hidden += 1
        else:
            prev_rec["status"]       = "missing"
            prev_rec["hidden_since"] = hidden_since_str
            stale_new += 1

        # คงไว้ใน master (status=missing/hidden) ไม่ลบออก
        all_records[pid] = prev_rec

    log_msg(
        f"[PAMCO] Stale Guard: "
        f"{stale_new} newly missing | "
        f"{stale_hidden} auto-hidden (>{PAMCO_STALE_DAYS}d) | "
        f"{stale_restored} restored",
        log_file
    )

    # สรุปยอด ก่อน save
    visible   = sum(1 for r in all_records.values() if r.get("status") != "hidden")
    hidden_ct = sum(1 for r in all_records.values() if r.get("status") == "hidden")
    missing_ct = sum(1 for r in all_records.values() if r.get("status") == "missing")
    log_msg(
        f"[PAMCO] Master total: {len(all_records)} "
        f"({visible} visible | {missing_ct} missing | {hidden_ct} hidden)",
        log_file
    )

    # บันทึกลงไฟล์
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)
    log_msg(f"[PAMCO] Saved → {out_path}", log_file)

    # อัปโหลด R2 สำหรับ webhook ดึงใช้
    if put_object_r2:
        try:
            data_bytes = json.dumps(all_records, ensure_ascii=False).encode('utf-8')
            put_object_r2("data/pamco_property_master.json", data_bytes, "application/json; charset=utf-8")
            log_msg("[PAMCO] Synced to Cloudflare R2: data/pamco_property_master.json", log_file)
        except Exception as e:
            log_msg(f"[PAMCO] R2 sync error: {e}", log_file)

    return all_records


def run_overnight_crawler():
    data_dir = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
    all_props_file = os.path.join(data_dir, "homerun_all_properties_10k.json")
    state_file = os.path.join(data_dir, "r2_images_sync_state.json")
    manifest_file = os.path.join(data_dir, "r2_assets_manifest.json")
    log_file = os.path.join(data_dir, "overnight_crawler.log")

    # ---- STEP 0: PAMCO pull (runs first, always) ----
    try:
        log_msg("=== STEP 0: PAMCO Property Pull ===", log_file)
        run_pamco_pull(data_dir, log_file)
    except Exception as e:
        log_msg(f"[PAMCO] Pull failed (non-fatal): {e}", log_file)
    
    if not os.path.exists(all_props_file):
        print("[-] Error: homerun_all_properties_10k.json not found!")
        return

    with open(all_props_file, 'r', encoding='utf-8') as f:
        all_items = json.load(f)

    log_msg(f"=== OVERNIGHT NPA IMAGE CRAWLER STARTED ===", log_file)
    log_msg(f"Total Master Properties: {len(all_items)} records", log_file)

    # Load State
    state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except Exception:
            state = {}

    # Migrate any existing SCB state
    old_scb_state_file = os.path.join(data_dir, "scb_images_sync_state.json")
    if os.path.exists(old_scb_state_file):
        try:
            with open(old_scb_state_file, 'r', encoding='utf-8') as f:
                old_scb = json.load(f)
                state.update(old_scb)
        except Exception:
            pass

    manifest = {}
    if os.path.exists(manifest_file):
        try:
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}

    old_manifest_file = os.path.join(data_dir, "scb_assets_manifest.json")
    if os.path.exists(old_manifest_file):
        try:
            with open(old_manifest_file, 'r', encoding='utf-8') as f:
                old_m = json.load(f)
                manifest.update(old_m)
        except Exception:
            pass

    log_msg(f"Already synced so far: {len(state)} properties", log_file)

    # Process pools in priority order: SCB -> SAM -> TTB
    pools = ['SCB', 'SAM', 'TTB']
    total_uploaded = 0
    start_time = time.time()

    for pool in pools:
        pool_items = [it for it in all_items if it.get('bank_pool') == pool]
        pending = [it for it in pool_items if it['id'] not in state]
        log_msg(f"\n--- Starting Pool [{pool}]: {len(pending)} pending / {len(pool_items)} total ---", log_file)
        
        for idx, item in enumerate(pending):
            p_id = item['id']
            code = item.get('code', 'N/A')
            title = str(item.get('title', 'Unknown'))
            pool_lower = pool.lower()
            
            # Fetch detail with media
            detail_url = f"https://homerun-platform-api-prod-645188686833.asia-southeast1.run.app/api/web/group-buy/{pool_lower}/properties/{p_id}?include=media"
            detail_data = {}
            for retry in range(3):
                try:
                    req = urllib.request.Request(detail_url, headers=HEADERS)
                    with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
                        if r.status == 200:
                            detail_data = json.loads(r.read().decode('utf-8')).get('data', {})
                            break
                except Exception:
                    time.sleep(1.0)

            thumb_url = detail_data.get('thumbnailUrl')
            gallery = detail_data.get('gallery', [])

            # Fix SAM URL if pointing to dead npa.sam.or.th subdomain
            if thumb_url and 'npa.sam.or.th' in thumb_url:
                thumb_url = thumb_url.replace('npa.sam.or.th', 'www.sam.or.th')

            prop_assets = {
                "id": p_id,
                "pool": pool,
                "code": code,
                "title": title,
                "price": item.get('price'),
                "thumbnail": None,
                "gallery": []
            }

            img_count = 0
            browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0'}

            # 1. Upload Thumbnail
            if thumb_url:
                try:
                    t_req = urllib.request.Request(thumb_url, headers=browser_header)
                    with urllib.request.urlopen(t_req, context=ctx, timeout=5) as r:
                        img_bytes = r.read()
                        if len(img_bytes) > 500:
                            ctype = r.headers.get('content-type', 'image/jpeg')
                            ext = "png" if "png" in ctype else "jpg"
                            r2_key = f"{pool_lower}/{p_id}/thumb.{ext}"
                            put_object_r2(r2_key, img_bytes, ctype)
                            prop_assets["thumbnail"] = f"{CDN_BASE}/{r2_key}"
                            img_count += 1
                            total_uploaded += 1
                except Exception:
                    pass

            # 2. Upload Gallery (up to 4 key images)
            for g_idx, g in enumerate(gallery[:4]):
                g_url = g.get('url')
                if g_url:
                    if 'npa.sam.or.th' in g_url:
                        g_url = g_url.replace('npa.sam.or.th', 'www.sam.or.th')
                    try:
                        g_req = urllib.request.Request(g_url, headers=browser_header)
                        with urllib.request.urlopen(g_req, context=ctx, timeout=5) as r:
                            img_bytes = r.read()
                            if len(img_bytes) > 500:
                                ctype = r.headers.get('content-type', 'image/jpeg')
                                ext = "png" if "png" in ctype else "jpg"
                                r2_key = f"{pool_lower}/{p_id}/gallery_{g_idx}.{ext}"
                                put_object_r2(r2_key, img_bytes, ctype)
                                prop_assets["gallery"].append(f"{CDN_BASE}/{r2_key}")
                                img_count += 1
                                total_uploaded += 1
                    except Exception:
                        pass
                time.sleep(0.12) # Gentle stealth pause between images

            # Save to state and manifest
            state[p_id] = {
                "pool": pool,
                "code": code,
                "synced_at": datetime.now().isoformat(),
                "images_count": img_count
            }
            manifest[p_id] = prop_assets

            if (idx + 1) % 10 == 0 or (idx + 1) == len(pending):
                log_msg(f"[{pool} {idx+1}/{len(pending)}] Total R2 Done: {len(state)}/10672 (Last: {code} -> {img_count} imgs)", log_file)

            # Checkpoint save state every 20 items
            if (idx + 1) % 20 == 0:
                with open(state_file, 'w', encoding='utf-8') as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                with open(manifest_file, 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, ensure_ascii=False, indent=2)

            # Stealth delay between properties (0.25s)
            time.sleep(0.25)

        # End of pool checkpoint save
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

    elapsed_h = (time.time() - start_time) / 3600
    log_msg(f"\n================ OVERNIGHT RUN COMPLETE ================", log_file)
    log_msg(f"Total Properties in R2: {len(state)}/10672", log_file)
    log_msg(f"Total Images Uploaded : {total_uploaded}", log_file)
    log_msg(f"Elapsed Time          : {elapsed_h:.2f} hours", log_file)
    log_msg(f"=========================================================", log_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Siwasup Overnight NPA Crawler")
    parser.add_argument("--pamco-only", action="store_true",
                        help="Run only the PAMCO pull step and exit")
    args = parser.parse_args()

    data_dir = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
    log_file = os.path.join(data_dir, "overnight_crawler.log")

    if args.pamco_only:
        run_pamco_pull(data_dir, log_file)
    else:
        run_overnight_crawler()
