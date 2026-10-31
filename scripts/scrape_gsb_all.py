import urllib.request
import ssl
import json
import re
import os
import sys
import time
from datetime import datetime

# UTF-8 stdout
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATA_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
OUTPUT_FILE = os.path.join(DATA_DIR, "gsb_all_properties.json")
STATE_FILE = os.path.join(DATA_DIR, "gsb_crawler_state.json")
LOG_FILE = os.path.join(DATA_DIR, "gsb_crawler.log")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'th,en-US;q=0.9,en;q=0.8'
}

def log_msg(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
    except Exception:
        pass

def fetch_page(page_num, page_size=100, retries=3):
    url = f"https://npa-assets.gsb.or.th/asset/npa/all?page={page_num}&page_size={page_size}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                if resp.status == 200:
                    html = resp.read().decode('utf-8', errors='ignore')
                    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
                    if m:
                        d = json.loads(m.group(1))
                        list_obj = d.get('props', {}).get('pageProps', {}).get('list', {})
                        data_obj = list_obj.get('data', {})
                        rows = data_obj.get('rows', [])
                        total_count = list_obj.get('asset_count', 4446)
                        return rows, total_count
        except Exception as e:
            time.sleep(1.5 * (attempt + 1))
    return None, 0

def run_crawler():
    os.makedirs(DATA_DIR, exist_ok=True)
    log_msg("=== STARTING GSB (ธนาคารออมสิน) NPA CRAWLER ===")

    properties_map = {}
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                props_list = json.load(f)
                properties_map = {p['id']: p for p in props_list}
            log_msg(f"Loaded existing data: {len(properties_map)} properties")
        except Exception as e:
            log_msg(f"Warning: could not read existing data ({e})")

    last_page = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                st = json.load(f)
                last_page = st.get('last_page', 0)
            log_msg(f"Resuming from page {last_page + 1}")
        except Exception:
            last_page = 0

    # Probe Page 1
    sample_rows, total_items = fetch_page(1, page_size=100)
    if sample_rows is None:
        log_msg("[-] Failed to fetch Page 1. Aborting.")
        return

    page_size = 100
    total_pages = (total_items + page_size - 1) // page_size
    log_msg(f"Total GSB Target: {total_items:,} items across {total_pages} pages (batch size {page_size})")

    start_page = last_page + 1
    start_time = time.time()

    for page in range(start_page, total_pages + 1):
        rows, _ = fetch_page(page, page_size=page_size)
        if rows is None:
            log_msg(f"[!] Warning: Could not fetch page {page}, retrying next run...")
            continue

        if not rows:
            log_msg(f"No rows on page {page}, crawl complete.")
            break

        for item in rows:
            asset_id = str(item.get('asset_id', ''))
            code = item.get('asset_group_id_npa') or item.get('asset_group_id') or f"GSB_{asset_id}"
            image_id = item.get('image_id', '')
            asset_type_id = item.get('asset_type_id', 342)
            
            img_url = f"https://npa-assets.gsb.or.th/apipr/npa/image?id={image_id}&asset_type_id={asset_type_id}" if image_id else None
            detail_url = f"https://npa-assets.gsb.or.th/asset/npa/detail/{item.get('asset_group_id')}"

            # Standard clean format
            prop_data = {
                "id": f"GSB_{asset_id}",
                "gsb_id": asset_id,
                "code": code,
                "bank_pool": "GSB",
                "bank_name": "ธนาคารออมสิน",
                "title": item.get('asset_name') or item.get('village_head') or item.get('asset_type_desc') or "ทรัพย์สินรอการขาย ออมสิน",
                "type_name": item.get('asset_type_desc') or "อสังหาริมทรัพย์",
                "price": int(item.get('xprice') or item.get('current_offer_price') or item.get('group_sell_price') or 0),
                "original_price": int(item.get('current_offer_price') or item.get('group_sell_price') or 0),
                "promo_price": int(item.get('xprice') or 0) if item.get('xtype') == 'promotion' else None,
                "province": item.get('province_name') or "",
                "district": item.get('district_name') or "",
                "subdistrict": item.get('sub_district_name') or "",
                "area_rai": item.get('sum_rai', 0),
                "area_ngan": item.get('sum_ngan', 0),
                "area_sqw": item.get('sum_square_wa', 0),
                "area_sqm": item.get('square_meter'),
                "area_raw": item.get('rai_ngan_wa') or "",
                "deed_info": item.get('deed_info') or "",
                "thumbnail_url": img_url,
                "detail_url": detail_url,
                "crawled_at": datetime.now().isoformat()
            }

            properties_map[prop_data['id']] = prop_data

        elapsed = time.time() - start_time
        pct = (len(properties_map) / total_items) * 100
        log_msg(f"[Page {page}/{total_pages} ({pct:.1f}%)] Ingested: {len(properties_map):,} / {total_items:,} properties")

        # Checkpoint save after every page
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(properties_map.values()), f, ensure_ascii=False, indent=2)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "last_page": page,
                "total_pages": total_pages,
                "total_collected": len(properties_map),
                "updated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

        time.sleep(0.5)  # Gentle delay

    total_time = (time.time() - start_time) / 60
    log_msg(f"=== GSB CRAWL FINISHED: Successfully captured {len(properties_map):,} properties in {total_time:.2f} mins ===")

if __name__ == "__main__":
    run_crawler()
