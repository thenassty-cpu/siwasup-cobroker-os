import urllib.request
import ssl
import re
import json
import time
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl._create_unverified_context()

BASE_URL = "https://www.allabout-assets.com"

CATEGORIES = {
    "single_house": {"name": "บ้านเดี่ยว", "url": f"{BASE_URL}/category/single_house"},
    "townhome": {"name": "ทาวน์โฮม", "url": f"{BASE_URL}/category/townhome"},
    "condominium": {"name": "คอนโด", "url": f"{BASE_URL}/category/condominium"},
    "land": {"name": "ที่ดิน", "url": f"{BASE_URL}/category/land"},
    "commercial_building": {"name": "อาคารพาณิชย์", "url": f"{BASE_URL}/category/commercial_building"},
    "npa": {"name": "ทรัพย์ NPA", "url": f"{BASE_URL}/category/260664"}
}

def fetch_html(url, retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
                raw = resp.read()
                # Try utf-8 first
                try:
                    return raw.decode('utf-8')
                except UnicodeDecodeError:
                    return raw.decode('tis-620', errors='ignore')
        except Exception as e:
            if attempt == retries - 1:
                print(f"Error fetching {url}: {e}")
                return ""
            time.sleep(1)
    return ""

def get_product_ids_from_category(cat_key, cat_info):
    url_base = cat_info["url"]
    name = cat_info["name"]
    page = 1
    found_products = {}
    
    print(f"[*] Crawling category: {name} ({cat_key})...")
    
    while True:
        url = f"{url_base}?page={page}" if page > 1 else url_base
        html = fetch_html(url)
        if not html:
            break
            
        # Match product links
        # Looking for /product/<id>
        matches = re.findall(r'href=["\'](?:https?://www\.allabout-assets\.com)?/product/([a-zA-Z0-9_\-]+)["\']', html)
        if not matches:
            break
            
        unique_matches = list(dict.fromkeys(matches))
        new_in_page = 0
        for pid in unique_matches:
            if pid not in found_products:
                found_products[pid] = {
                    "id": pid,
                    "category": name,
                    "cat_key": cat_key,
                    "page": page
                }
                new_in_page += 1
                
        print(f"  Page {page}: found {len(unique_matches)} links ({new_in_page} new, total: {len(found_products)})")
        
        if new_in_page == 0:
            # No new products found on this page, end of pagination
            break
            
        page += 1
        # Safety break for huge pagination
        if page > 40:
            break
            
        time.sleep(0.3)
        
    return found_products

def main():
    print("=== STARTING FULL RE-CRAWL OF ALLABOUT-ASSETS ===")
    all_live_products = {}
    cat_summary = {}
    
    for cat_key, cat_info in CATEGORIES.items():
        prods = get_product_ids_from_category(cat_key, cat_info)
        cat_summary[cat_info["name"]] = len(prods)
        for pid, data in prods.items():
            if pid not in all_live_products:
                all_live_products[pid] = data
            else:
                # Product exists in multiple categories (e.g. NPA + Single House)
                all_live_products[pid]["other_categories"] = all_live_products[pid].get("other_categories", []) + [cat_info["name"]]
                
    print("\n=== LIVE CRAWL SUMMARY ===")
    total_unique = len(all_live_products)
    for cat_name, count in cat_summary.items():
        print(f"- {cat_name}: {count} รายการ")
    print(f"TOTAL UNIQUE PROPERTIES LIVE: {total_unique}")
    
    # Save live audit
    with open('live_allabout_products.json', 'w', encoding='utf-8') as f:
        json.dump(all_live_products, f, ensure_ascii=False, indent=2)
        
    # Now compare with our current siwasup_all_properties.json
    local_path = 'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/siwasup_all_properties.json'
    with open(local_path, 'r', encoding='utf-8') as f:
        local_props = json.load(f)
        
    local_ids = set(str(p['id']) for p in local_props)
    live_ids = set(all_live_products.keys())
    
    in_both = local_ids.intersection(live_ids)
    in_live_only = live_ids - local_ids
    in_local_only = local_ids - live_ids
    
    print("\n=== COMPARISON WITH LOCAL DATASET (119 PROPS) ===")
    print(f"Matched in both: {len(in_both)}")
    print(f"New on Live site (MISSING from local): {len(in_live_only)}")
    print(f"In local but disappeared from Live: {len(in_local_only)}")
    
    if in_local_only:
        print("\nIDs in local but not found in current categories:", list(in_local_only)[:10])
        
    print("\nSample of NEW items on live site:")
    for pid in list(in_live_only)[:10]:
        print(f"- ID: {pid} ({all_live_products[pid]['category']})")

if __name__ == '__main__':
    main()
