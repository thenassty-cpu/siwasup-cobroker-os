import urllib.request
import ssl
import re
import json
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl._create_unverified_context()

BASE_URL = "https://www.allabout-assets.com"

CATEGORIES = [
    ("single_house", "บ้านเดี่ยว", 2),
    ("townhome", "ทาวน์โฮม", 2),
    ("condominium", "คอนโด", 2),
    ("land", "ที่ดิน", 2),
    ("commercial_building", "อาคารพาณิชย์", 2),
    ("260664", "ทรัพย์ NPA", 29)
]

def fetch_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
                raw = resp.read()
                try:
                    return raw.decode('utf-8')
                except UnicodeDecodeError:
                    return raw.decode('tis-620', errors='ignore')
        except Exception:
            time.sleep(1)
    return ""

def parse_cards_from_html(html, category_name):
    # Regex to match <li> or product container
    # <li class="product-item ..."> ... </li>
    items = []
    # Pattern for product link
    pattern = r'<li[^>]*class=["\'][^"\']*product-item[^"\']*["\'][^>]*>([\s\S]*?)</li>'
    matches = re.findall(pattern, html)
    if not matches:
        # Fallback to general block
        pattern2 = r'(<div[^>]*class=["\'][^"\']*image-wrapper[^"\']*["\'][^>]*>[\s\S]*?<div[^>]*class=["\'][^"\']*product-name[^"\']*["\'][^>]*>[\s\S]*?</div>[\s\S]*?<div[^>]*class=["\'][^"\']*product-price[^"\']*["\'][^>]*>[\s\S]*?</div>)'
        matches = re.findall(pattern2, html)
        
    for block in matches:
        # Find ID
        pid_m = re.search(r'/product/([a-zA-Z0-9_\-]+)', block)
        if not pid_m:
            continue
        pid = pid_m.group(1)
        
        # Find Title
        title = ""
        title_m = re.search(r'<div[^>]*class=["\'][^"\']*product-name[^"\']*["\'][^>]*>([\s\S]*?)</div>', block)
        if title_m:
            title = re.sub(r'<[^>]+>', ' ', title_m.group(1)).strip()
            title = re.sub(r'\s+', ' ', title)
            
        # Find Price
        price = ""
        price_m = re.search(r'<div[^>]*class=["\'][^"\']*product-price[^"\']*["\'][^>]*>([\s\S]*?)</div>', block)
        if price_m:
            price_text = re.sub(r'<[^>]+>', ' ', price_m.group(1)).strip()
            price_match = re.search(r'([\d,]+(?:\.\d+)?)\s*(?:บาท|฿)', price_text)
            if price_match:
                price = f"{price_match.group(1)} บาท"
            else:
                price = price_text
                
        # Find Image
        img_url = ""
        img_m = re.search(r'(?:data-src|src)=["\'](https?://[^"\']+)["\']', block)
        if img_m:
            img_url = img_m.group(1)
            
        # Find Label (e.g. ใหม่ล่าสุด, แนะนำ)
        label = ""
        label_m = re.search(r'<div[^>]*class=["\'][^"\']*product-label[^"\']*["\'][^>]*>([\s\S]*?)</div>', block)
        if label_m:
            label = re.sub(r'<[^>]+>', '', label_m.group(1)).strip()
            
        items.append({
            "id": pid,
            "title": title or f"ทรัพย์ #{pid}",
            "category": category_name,
            "price": price or "ติดต่อสอบถาม",
            "main_image": img_url,
            "label": label,
            "url": f"https://www.allabout-assets.com/product/{pid}"
        })
    return items

def main():
    print("=== STARTING FAST PARSING OF ALL CATEGORY PAGES ===")
    all_tasks = []
    for cat_slug, cat_name, max_pages in CATEGORIES:
        for p in range(1, max_pages + 1):
            url = f"{BASE_URL}/category/{cat_slug}?page={p}" if p > 1 else f"{BASE_URL}/category/{cat_slug}"
            all_tasks.append((url, cat_name, p))
            
    print(f"Total pages to crawl: {len(all_tasks)}")
    
    scraped_products = {}
    
    def process_task(task):
        url, cat_name, p = task
        html = fetch_page(url)
        if not html:
            return []
        return parse_cards_from_html(html, cat_name)

    with ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(process_task, all_tasks)
        for r in results:
            for item in r:
                pid = item["id"]
                if pid not in scraped_products:
                    scraped_products[pid] = item
                else:
                    # Update label if found on another page
                    if item["label"] and not scraped_products[pid].get("label"):
                        scraped_products[pid]["label"] = item["label"]

    print(f"\n[OK] Scraped total unique products from category cards: {len(scraped_products)}")
    
    # Also load previous 119 dataset to carry over descriptions, sizes, galleries if available
    local_path = 'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/siwasup_all_properties.json'
    with open(local_path, 'r', encoding='utf-8') as f:
        local_119 = json.load(f)
    local_dict = {p['id']: p for p in local_119}
    
    FLAGGED_8_REMOVED = ['1069562', '1183447', '1332905', '1330893', '1313075', '1239881', '1252172', '1325872']
    
    final_list = []
    
    # 1. First add the 8 FLAGGED RED properties on top so Bua sees them immediately!
    print(f"\n[*] Processing 8 FLAGGED properties (Red Ribbon)...")
    for pid in FLAGGED_8_REMOVED:
        if pid in local_dict:
            p = dict(local_dict[pid])
        elif pid in scraped_products:
            p = dict(scraped_products[pid])
        else:
            p = {"id": pid, "title": f"ทรัพย์ #{pid}", "category": "บ้านเดี่ยว", "price": "ติดต่อสอบถาม"}
            
        p["ribbon"] = "red"
        p["ribbon_text"] = "แจ้งเตือน: เว็บเดิมถอดออกแล้ว"
        p["flag_reason"] = "ทรัพย์นี้ไม่อยู่ในหมวดหมู่หน้าเว็บปัจจุบันแล้ว กรุณาเช็กว่าขายหรือยัง หากยังอยู่และขายได้ให้กดหัวใจ ❤️ เพื่อดึงกลับมา"
        p["group"] = "flagged_red"
        final_list.append(p)
        print(f"  + Added Red Ribbon: #{pid} - {p.get('title')[:40]}")
        
    # 2. Add GREEN RIBBON properties (New In / ใหม่ล่าสุด)
    # Products with label 'ใหม่ล่าสุด' or newly added
    print(f"\n[*] Processing GREEN RIBBON properties (New In)...")
    green_count = 0
    for pid, p in scraped_products.items():
        if pid in FLAGGED_8_REMOVED:
            continue
            
        is_new = (p.get("label") == "ใหม่ล่าสุด" or pid in ["1254541", "1254199", "1253183", "1336545", "1336482", "1334412", "1334351", "1336448", "1336234", "1336233", "1336218", "1336102"])
        if is_new:
            item = dict(p)
            # Enrich with local details if existing
            if pid in local_dict:
                for k, v in local_dict[pid].items():
                    if k not in item or not item[k]:
                        item[k] = v
            item["ribbon"] = "green"
            item["ribbon_text"] = "ใหม่ล่าสุด (New In)"
            item["flag_reason"] = "ทรัพย์ที่เพิ่งนำมาลงในเว็บ allabout กดหัวใจ ❤️ เพื่อเลือกเข้าพอร์ตเว็บใหม่"
            item["group"] = "new_green"
            final_list.append(item)
            green_count += 1
            
    print(f"  + Added Green Ribbon: {green_count} properties")
    
    # 3. Add General properties (Regular active properties)
    general_count = 0
    for pid, p in scraped_products.items():
        if pid in FLAGGED_8_REMOVED or any(x['id'] == pid for x in final_list):
            continue
        if p.get("category") != "ทรัพย์ NPA":
            item = dict(p)
            if pid in local_dict:
                for k, v in local_dict[pid].items():
                    if k not in item or not item[k]:
                        item[k] = v
            item["ribbon"] = "gray"
            item["ribbon_text"] = "เปิดขายปกติ"
            item["group"] = "general"
            final_list.append(item)
            general_count += 1
            
    print(f"  + Added General properties: {general_count} properties")
    
    # 4. Add NPA properties (677 items)
    npa_count = 0
    for pid, p in scraped_products.items():
        if pid in FLAGGED_8_REMOVED or any(x['id'] == pid for x in final_list):
            continue
        if p.get("category") == "ทรัพย์ NPA":
            item = dict(p)
            if pid in local_dict:
                for k, v in local_dict[pid].items():
                    if k not in item or not item[k]:
                        item[k] = v
            item["ribbon"] = "blue"
            item["ribbon_text"] = "ทรัพย์ NPA ธนาคาร"
            item["group"] = "npa_vault"
            final_list.append(item)
            npa_count += 1
            
    print(f"  + Added NPA Vault properties: {npa_count} properties")
    print(f"\nTOTAL CURATION LIST READY: {len(final_list)} properties")
    
    # Save to JSON and JS
    json_path = 'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/all_curation_properties.json'
    js_path = 'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/all_curation_properties.js'
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
        
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write("var ALL_CURATION_DATA = " + json.dumps(final_list, ensure_ascii=False, indent=2) + ";\n")
        
    print(f"[OK] Saved {json_path} and {js_path}!")

if __name__ == '__main__':
    main()
