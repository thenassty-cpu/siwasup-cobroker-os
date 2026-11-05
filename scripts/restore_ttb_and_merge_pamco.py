import json
import os

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
BACKUP_TTB_PATH = os.path.join(REPO_DIR, "data", "siwasup_all_properties_backup_with_ttb.json")
PAMCO_PATH = os.path.join(REPO_DIR, "data", "pamco_property_master.json")
ALL_PROP_JSON = os.path.join(REPO_DIR, "siwasup_all_properties.json")
ALL_PROP_JS = os.path.join(REPO_DIR, "siwasup_all_properties.js")

# 1. Load Backup base with TTB (1,849 items)
with open(BACKUP_TTB_PATH, "r", encoding="utf-8") as f:
    base_props = json.load(f)

print(f"Loaded base properties with TTB: {len(base_props)} items")

# 2. Load PAMCO properties (1,312 items)
with open(PAMCO_PATH, "r", encoding="utf-8") as f:
    pamco_raw = json.load(f)

if isinstance(pamco_raw, dict):
    pamco_props = list(pamco_raw.values())
else:
    pamco_props = pamco_raw

# Format PAMCO to master format
formatted_pamco = []
for p in pamco_props:
    pid = p.get("id") or p.get("code")
    pcode = p.get("code") or pid
    if not str(pid).startswith("PAMCO_"):
        pid = f"PAMCO_{pcode}"
    
    price_val = p.get("price") or "ติดต่อสอบถาม"
    if isinstance(price_val, (int, float)):
        price_str = f"{price_val:,.0f} บาท"
    else:
        price_str = str(price_val)
        if "บาท" not in price_str and price_str != "ติดต่อสอบถาม":
            price_str += " บาท"

    formatted_pamco.append({
        "id": str(pid),
        "code": str(pcode),
        "title": p.get("title") or f"ทรัพย์ PAMCO: {p.get('category', 'อสังหาฯ')} {p.get('location', '')}",
        "category": p.get("category") or "บ้านเดี่ยว",
        "bank_source": "PAMCO",
        "price": price_str,
        "location": p.get("location") or "กรุงเทพฯ และปริมณฑล",
        "size": p.get("size") or "-",
        "usable_area": p.get("usable_area") or "-",
        "main_image": p.get("main_image") or (p.get("gallery", [None])[0]),
        "gallery_count": len(p.get("gallery", [])),
        "gallery": p.get("gallery") or [p.get("main_image")],
        "description": p.get("description") or f"รหัสทรัพย์ PAMCO: {pcode}",
        "status": "available",
        "is_image_soldout": False,
        "latitude": p.get("latitude") or p.get("lat"),
        "longitude": p.get("longitude") or p.get("lng"),
        "search_keywords": f"{pcode} {p.get('title', '')} {p.get('category', '')} {p.get('location', '')} pamco".lower()
    })

print(f"Formatted PAMCO: {len(formatted_pamco)} items")

# Combine all: Base (including TTB) + PAMCO
merged_dict = {}
for p in base_props:
    merged_dict[str(p["id"])] = p

for p in formatted_pamco:
    merged_dict[str(p["id"])] = p

master_list = list(merged_dict.values())
print(f"Total Combined Master Properties: {len(master_list)} items")

# Bank counts breakdown
from collections import Counter
counts = Counter(p.get("bank_source") for p in master_list)
print("\n=== BANK BREAKDOWN IN RESTORED MASTER ===")
for b, c in counts.most_common():
    print(f"  {b}: {c}")

# Save JSON
with open(ALL_PROP_JSON, "w", encoding="utf-8") as f:
    json.dump(master_list, f, ensure_ascii=False, indent=2)

# Save JS bundle with aliases
json_str = json.dumps(master_list, ensure_ascii=False)
js_content = f"window.ALL_PROPERTIES_DATA = {json_str};\nwindow.SIWASUP_PROPERTIES = window.ALL_PROPERTIES_DATA;\nwindow.SIWASUP_ALL_PROPERTIES = window.ALL_PROPERTIES_DATA;\n"
with open(ALL_PROP_JS, "w", encoding="utf-8") as f:
    f.write(js_content)

print("\n[OK] Successfully generated siwasup_all_properties.json and .js with TTB restored!")
