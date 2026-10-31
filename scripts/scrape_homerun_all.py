import urllib.request
import ssl
import json
import time
import os
import sys

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://homerunplatform.com',
    'Referer': 'https://homerunplatform.com/'
}

POOLS = [
    ('sam', 5100),
    ('scb', 4207),
    ('ttb', 1365)
]

output_dir = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "homerun_all_properties_10k.json")
stats_file = os.path.join(output_dir, "homerun_10k_stats.json")

print("[*] Starting Stealth Scrape for Homerun NPA Dataset (Healthy & Silent Mode)...")
all_properties = []
pool_stats = {}

start_time = time.time()

for pool, expected_total in POOLS:
    per_page = 100
    total_pages = (expected_total + per_page - 1) // per_page
    print(f"\n[+] Pool [{pool.upper()}]: Target {expected_total} items across {total_pages} pages...")
    pool_items = []
    
    for page in range(1, total_pages + 1):
        url = f"https://homerun-platform-api-prod-645188686833.asia-southeast1.run.app/api/web/group-buy/{pool}/properties?page={page}&perPage={per_page}"
        success = False
        for retry in range(3):
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode('utf-8'))
                        items = data.get('data', [])
                        # Tag bank source for easy filtering
                        for it in items:
                            it['bank_pool'] = pool.upper()
                        pool_items.extend(items)
                        success = True
                        break
            except Exception as e:
                time.sleep(1.0)
        
        if page % 10 == 0 or page == total_pages:
            print(f"   -> Page {page}/{total_pages} ({len(pool_items)} items fetched)")
        
        # Gentle 0.25s delay between requests (Healthy / Stealth / Anti-Trigger)
        time.sleep(0.25)
    
    pool_stats[pool.upper()] = len(pool_items)
    all_properties.extend(pool_items)

elapsed = time.time() - start_time
print(f"\n[✓] Fetch complete in {elapsed:.1f} seconds! Total records: {len(all_properties)}")

# Save master JSON
print(f"[*] Writing {len(all_properties)} records to: {output_file}...")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_properties, f, ensure_ascii=False, indent=2)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
print(f"[✓] File successfully written! Size: {file_size_mb:.2f} MB")

# Calculate Detailed Analytics
total_value = sum(float(it.get('price', 0) or 0) for it in all_properties)
provinces = {}
categories = {}
price_brackets = {
    "< 1M": 0,
    "1M - 3M": 0,
    "3M - 5M": 0,
    "5M - 10M": 0,
    "> 10M": 0
}

for it in all_properties:
    # Province
    p_name = "Unknown"
    prov = it.get('province')
    if isinstance(prov, dict):
        p_name = prov.get('nameTh') or prov.get('nameEn') or "Unknown"
    elif isinstance(prov, str):
        p_name = prov
    provinces[p_name] = provinces.get(p_name, 0) + 1
    
    # Category
    cat = it.get('propertyCategory') or it.get('propertyTypeKey') or "อื่นๆ"
    categories[cat] = categories.get(cat, 0) + 1
    
    # Price
    p = float(it.get('price', 0) or 0)
    if p < 1000000:
        price_brackets["< 1M"] += 1
    elif p < 3000000:
        price_brackets["1M - 3M"] += 1
    elif p < 5000000:
        price_brackets["3M - 5M"] += 1
    elif p < 10000000:
        price_brackets["5M - 10M"] += 1
    else:
        price_brackets["> 10M"] += 1

top_provinces = sorted(provinces.items(), key=lambda x: x[1], reverse=True)[:10]

summary = {
    "total_records": len(all_properties),
    "file_size_mb": round(file_size_mb, 2),
    "elapsed_seconds": round(elapsed, 1),
    "by_bank": pool_stats,
    "total_asset_value_thb": round(total_value, 2),
    "top_provinces": dict(top_provinces),
    "categories": categories,
    "price_brackets": price_brackets
}

with open(stats_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("\n================== SCRAPING REPORT ==================")
print(f"Total Properties Scraped : {len(all_properties):,}")
print(f"Total Value (GMV Pool)   : {total_value:,.2f} THB")
print(f"SAM                      : {pool_stats.get('SAM', 0):,}")
print(f"SCB                      : {pool_stats.get('SCB', 0):,}")
print(f"TTB                      : {pool_stats.get('TTB', 0):,}")
print(f"Top 5 Provinces          : {top_provinces[:5]}")
print("=====================================================")
