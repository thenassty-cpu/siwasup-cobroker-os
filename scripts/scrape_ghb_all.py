import urllib.request
import ssl
import re
import json
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
OUTPUT_FILE = os.path.join(DATA_DIR, "ghb_all_properties.json")
STATE_FILE = os.path.join(DATA_DIR, "ghb_crawler_state.json")
LOG_FILE = os.path.join(DATA_DIR, "ghb_crawler.log")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'th,en-US;q=0.9,en;q=0.8'
}

CARD_PATTERN = re.compile(
    r'<a href="https://www\.ghbhomecenter\.com/property-([0-9]+)"[^>]*>.*?<img src="([^"]+)"'
    r'.*?<div class="link-property-detail"[^>]*>.*?'
    r'<div class="text-propertyprice">.*?<div[^>]*>([0-9,]+)\s*บาท</div>'
    r'.*?<div class="text-header-titletype">.*?<div>(.*?)</div>'
    r'.*?<div class="text-location">.*?</i>\s*(.*?)\s*</div>'
    r'.*?<div class="text-area">.*?</i>\s*(.*?)\s*</div>'
    r'.*?รหัสทรัพย์:\s*<span[^>]*>(.*?)</span>',
    re.DOTALL
)

def log_msg(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
    except Exception:
        pass

def fetch_page(page_num, retries=3):
    url = f"https://ghbhomecenter.com/search?page={page_num}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
                if resp.status == 200:
                    return resp.read().decode('utf-8', errors='ignore')
        except Exception as e:
            time.sleep(1.0 * (attempt + 1))
    return None

def run_crawler(max_pages=None):
    os.makedirs(DATA_DIR, exist_ok=True)
    log_msg("=== STARTING GHB (ธอส.) NPA CRAWLER ===")

    # Load existing state & data
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

    # Probe page 1 to detect total pages and items
    p1_html = fetch_page(1)
    if not p1_html:
        log_msg("[-] Failed to fetch Page 1. Aborting.")
        return

    total_items_match = re.search(r'([0-9,]+)\s*รายการ', p1_html)
    total_items_str = total_items_match.group(1).replace(',', '') if total_items_match else "31792"
    total_items = int(total_items_str)
    
    # Extract highest page number
    page_numbers = [int(p) for p in re.findall(r'rel=[\'"]([0-9]+)[\'"]', p1_html) if int(p) < 5000]
    total_pages = max(page_numbers) if page_numbers else (total_items // 20 + 1)
    
    if max_pages and max_pages < total_pages:
        total_pages = max_pages

    log_msg(f"Total GHB Database Target: {total_items:,} items across ~{total_pages} pages")

    start_page = last_page + 1
    start_time = time.time()
    pages_processed = 0

    for page in range(start_page, total_pages + 1):
        html = fetch_page(page)
        if not html:
            log_msg(f"[!] Warning: Could not fetch page {page}, skipping...")
            continue

        matches = CARD_PATTERN.findall(html)
        if not matches:
            # Check if there are no more items or layout changed
            if "ไม่พบข้อมูล" in html or "No data" in html:
                log_msg(f"Reached end of listings at page {page}")
                break

        page_new = 0
        for m in matches:
            pid, img, price_str, title_str, loc_str, area_str, code_str = m
            clean_price = int(price_str.replace(',', '')) if price_str else 0
            
            # Parse location: "ตำบล, อำเภอ, จังหวัด"
            loc_parts = [x.strip() for x in loc_str.split(',') if x.strip()]
            province = loc_parts[-1] if loc_parts else ""
            district = loc_parts[-2] if len(loc_parts) >= 2 else ""
            subdistrict = loc_parts[-3] if len(loc_parts) >= 3 else ""

            prop_data = {
                "id": f"GHB_{pid}",
                "ghb_id": pid,
                "code": code_str.strip(),
                "bank_pool": "GHB",
                "bank_name": "ธอส.",
                "title": title_str.strip(),
                "price": clean_price,
                "province": province,
                "district": district,
                "subdistrict": subdistrict,
                "location_raw": loc_str.strip(),
                "area_raw": area_str.strip(),
                "thumbnail_url": img.strip(),
                "detail_url": f"https://www.ghbhomecenter.com/property-{pid}",
                "crawled_at": datetime.now().isoformat()
            }

            if pid not in properties_map:
                page_new += 1
            properties_map[pid] = prop_data

        pages_processed += 1

        # Log progress every 5 pages
        if page % 5 == 0 or page == total_pages:
            elapsed = time.time() - start_time
            ppm = (pages_processed / (elapsed / 60)) if elapsed > 0 else 0
            pct = (page / total_pages) * 100
            log_msg(f"[Page {page}/{total_pages} ({pct:.1f}%)] Total Properties: {len(properties_map):,} (Speed: {ppm:.1f} pages/min)")

            # Checkpoint save
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(properties_map.values()), f, ensure_ascii=False, indent=2)
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    "last_page": page,
                    "total_pages": total_pages,
                    "total_collected": len(properties_map),
                    "updated_at": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)

        # Gentle delay between pages
        time.sleep(0.3)

    log_msg(f"=== GHB CRAWL FINISHED: Collected {len(properties_map):,} properties ===")

if __name__ == "__main__":
    max_p = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run_crawler(max_pages=max_p)
