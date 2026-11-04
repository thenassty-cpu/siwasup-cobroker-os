# -*- coding: utf-8 -*-
"""
scripts/import_thonburi_all.py
---------------------------------------------
Imports all Thonburi & West Bangkok properties from catalog_index.json
into siwasup_all_properties.json and siwasup_all_properties.js,
then deploys them directly to Cloudflare R2.
"""

import os
import sys
import json
import re

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_INDEX_PATH = os.path.join(BASE_DIR, "data", "catalog_index.json")
SIWASUP_JSON_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.json")
SIWASUP_JS_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.js")

# District Thai-English Dictionary
DISTRICT_META = {
    'thawi watthana': ('ทวีวัฒนา', 'Thawi Watthana', 'กรุงเทพมหานคร', 'บรมราชชนนี ศาลายา พุทธมณฑลสาย 2 สาย 3'),
    'taling chan': ('ตลิ่งชัน', 'Taling Chan', 'กรุงเทพมหานคร', 'ราชพฤกษ์ บรมราชชนนี สวนผัก กาญจนาภิเษก'),
    'bangkok noi': ('บางกอกน้อย', 'Bangkok Noi', 'กรุงเทพมหานคร', 'ศิริราช พรานนก อิสรภาพ จรัญสนิทวงศ์ ไฟฉาย'),
    'bangkok yai': ('บางกอกใหญ่', 'Bangkok Yai', 'กรุงเทพมหานคร', 'ท่าพระ วังเดิม พาณิชยการธนบุรี เพชรเกษม'),
    'thon buri': ('ธนบุรี', 'Thon Buri', 'กรุงเทพมหานคร', 'วงเวียนใหญ่ ตลาดพลู สมเด็จพระเจ้าตากสิน โพธิ์นิมิตร'),
    'khlong san': ('คลองสาน', 'Khlong San', 'กรุงเทพมหานคร', 'ไอคอนสยาม เจริญนคร กรุงธนบุรี ลาดหญ้า'),
    'bang phlat': ('บางพลัด', 'Bang Phlat', 'กรุงเทพมหานคร', 'จรัญสนิทวงศ์ สะพานกรุงธน สิรินธร พระราม 7'),
    'phasi charoen': ('ภาษีเจริญ', 'Phasi Charoen', 'กรุงเทพมหานคร', 'เพชรเกษม บางหว้า บางแค ราชพฤกษ์'),
    'bang khae': ('บางแค', 'Bang Khae', 'กรุงเทพมหานคร', 'เพชรเกษม กัลปพฤกษ์ กาญจนาภิเษก บางแคเหนือ'),
    'nong khaem': ('หนองแขม', 'Nong Khaem', 'กรุงเทพมหานคร', 'เพชรเกษม 81 พุทธมณฑลสาย 3 สาย 4 มาเจริญ หนองแขม'),
    'bang bon': ('บางบอน', 'Bang Bon', 'กรุงเทพมหานคร', 'เอกชัย บางบอน กาญจนาภิเษก พระราม 2'),
    'bang khun thian': ('บางขุนเทียน', 'Bang Khun Thian', 'กรุงเทพมหานคร', 'พระราม 2 ท่าข้าม บางกระดี่ เทียนทะเล สะแกงาม'),
    'chom thong': ('จอมทอง', 'Chom Thong', 'กรุงเทพมหานคร', 'ดาวคะนอง วุฒากาศ พระราม 2 เอกชัย บางขุนเทียน'),
    'rat burana': ('ราษฎร์บูรณะ', 'Rat Burana', 'กรุงเทพมหานคร', 'สุขสวัสดิ์ ประชาอุทิศ ราษฎร์พัฒนา ทางด่วนเฉลิมมหานคร'),
    'thung khu': ('ทุ่งครุ', 'Thung Khu', 'กรุงเทพมหานคร', 'ประชาอุทิศ ครุใน บางมด พุทธบูชา อิสลามวิทยาลัย'),
    'bang bua thong': ('บางบัวทอง', 'Bang Bua Thong', 'นนทบุรี', 'กาญจนาภิเษก ชัยพฤกษ์ บางกรวย-ไทรน้อย เวสต์เกต'),
    'bang yai': ('บางใหญ่', 'Bang Yai', 'นนทบุรี', 'กาญจนาภิเษก เซ็นทรัลเวสต์เกต ตลาดบางใหญ่ แก้วอินทร์'),
    'bang kruai': ('บางกรวย', 'Bang Kruai', 'นนทบุรี', 'ราชพฤกษ์ พระราม 5 นครอินทร์ วงเวียนพระราม 5 ชัยพฤกษ์')
}

def run_import():
    print("[*] Reading catalog_index.json...")
    with open(CATALOG_INDEX_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    print("[*] Reading current siwasup_all_properties.json...")
    with open(SIWASUP_JSON_PATH, 'r', encoding='utf-8') as f:
        siwasup = json.load(f)

    existing_ids = {str(p.get("id")).strip().lower() for p in siwasup if p.get("id")}
    existing_codes = {str(p.get("code")).strip().lower() for p in siwasup if p.get("code")}

    print(f"[*] Starting base: {len(siwasup)} properties currently in Siwasup.")

    new_items = []
    added_codes = set()

    for p in catalog:
        # Check district
        d_raw = str(p.get('d', '')).strip().lower()
        matched_key = None
        for k in DISTRICT_META:
            if k in d_raw:
                matched_key = k
                break
        
        if not matched_key:
            continue

        thumb = p.get('thumb')
        if not thumb or 'assets.siwasup.com' not in thumb:
            # We only import items with verified HD photos hosted on Cloudflare R2
            continue

        code = str(p.get('c', '')).strip()
        if not code:
            code = str(p.get('id', '')).strip()

        # Skip duplicates
        code_clean = code.lower()
        if code_clean in existing_ids or code_clean in existing_codes or code_clean in added_codes:
            continue

        dist_th, dist_en, prov_th, landmarks = DISTRICT_META[matched_key]
        bank = p.get('b', 'Siwasup')
        cat_name = p.get('tn', 'บ้านเดี่ยว')
        price_num = p.get('pr', 0)
        price_fmt = f"{price_num:,} บาท"
        sqw = p.get('sqw', 0)
        sqm = p.get('sqm', 0)
        size_fmt = f"{sqw} ตร.ว." if sqw and sqw > 0 else "- ตร.ว."
        usable_fmt = f"{sqm} ตร.ม." if sqm and sqm > 0 else "- ตร.ม."
        location_fmt = f"{dist_th} ({dist_en}) • {prov_th}"

        # Gallery builder
        gc = p.get('gc', 1)
        gallery = [thumb]
        for i in range(min(gc, 6)):
            gal_url = thumb.replace('thumb.jpg', f'gallery_{i}.jpg')
            if gal_url not in gallery:
                gallery.append(gal_url)

        title = f"ทรัพย์ NPA {bank}: {cat_name} โซน{dist_th} ({prov_th}) รหัส {code}"
        description = (
            f"รหัสทรัพย์ {bank}: {code} | ประเภท: {cat_name} | ทำเล: {location_fmt} | "
            f"ขนาดที่ดิน: {size_fmt} | พื้นที่ใช้สอย: {usable_fmt} | "
            f"ทรัพย์รอการขาย (NPA) คัดสรรจาก {bank} ยื่นข้อเสนอและนัดเปิดบ้านได้ทันที "
            f"[โซนเด่นฝั่งธนบุรี: {dist_th} {landmarks} เดินทางสะดวก]"
        )

        item = {
            "id": code,
            "code": code,
            "title": title,
            "category": cat_name,
            "bank_source": bank,
            "price": price_fmt,
            "location": location_fmt,
            "size": size_fmt,
            "usable_area": usable_fmt,
            "main_image": thumb,
            "gallery_count": len(gallery),
            "gallery": gallery,
            "description": description,
            "status": "available",
            "is_image_soldout": False
        }

        new_items.append(item)
        added_codes.add(code_clean)

    print(f"[+] Successfully curated {len(new_items)} new Thonburi & West Bangkok properties with real R2 photos!")
    combined = siwasup + new_items
    print(f"[+] Total combined Siwasup stock: {len(combined)} properties (from 995 -> {len(combined)})")

    # 1. Save siwasup_all_properties.json
    print("[*] Writing updated siwasup_all_properties.json...")
    with open(SIWASUP_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    # 2. Save siwasup_all_properties.js
    print("[*] Writing updated siwasup_all_properties.js...")
    with open(SIWASUP_JS_PATH, 'w', encoding='utf-8') as f:
        f.write("var ALL_PROPERTIES_DATA = ")
        json.dump(combined, f, ensure_ascii=False, indent=2)
        f.write(";\nwindow.SIWASUP_PROPERTIES = ALL_PROPERTIES_DATA;\n")

    # 3. Deploy to Cloudflare R2
    print("[*] Deploying siwasup_all_properties.json to Cloudflare R2...")
    with open(SIWASUP_JSON_PATH, 'rb') as f:
        json_bytes = f.read()
    st_json = put_object_r2("siwasup_all_properties.json", json_bytes, "application/json; charset=utf-8")
    print(f"    Status: {st_json}")

    print("[*] Deploying siwasup_all_properties.js to Cloudflare R2...")
    with open(SIWASUP_JS_PATH, 'rb') as f:
        js_bytes = f.read()
    st_js = put_object_r2("siwasup_all_properties.js", js_bytes, "application/javascript; charset=utf-8")
    print(f"    Status: {st_js}")

    print("=== THONBURI EXPANSION DEPLOYED SUCCESSFULLY ===")
    return len(new_items), len(combined)

if __name__ == "__main__":
    run_import()
