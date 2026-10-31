import os
import sys
import csv
import json
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
DATA_DIR = os.path.join(BASE_DIR, "data")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
sys.path.append(SCRIPTS_DIR)

from overnight_r2_crawler import put_object_r2

# ==============================================================================
# PART 1: BUILD UNIFIED siwasup_all_properties.js & .json
# (Bua's 43 Curated + Siwasup Clean Portfolio + Real NPA from SCB, SAM, GSB, TTB)
# ==============================================================================
print("=== [1/3] Building unified siwasup_all_properties.js & .json ===")

# 1.1 Load Bua's 43 CSV IDs
bua_csv_path = r"G:\data\bua_update_20261030.csv"
bua_status_map = {}
if os.path.exists(bua_csv_path):
    with open(bua_csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = str(row.get("ID") or "").strip()
            sold = str(row.get("SoldOut") or "").strip().upper()
            if pid:
                bua_status_map[pid] = sold
print(f"[*] Loaded {len(bua_status_map)} IDs from Bua's CSV.")

# 1.2 Load all_curation_properties.json (801 items) & original 119 backup
with open(os.path.join(BASE_DIR, "all_curation_properties.json"), "r", encoding="utf-8") as f:
    curation_801 = json.load(f)

curation_by_id = {str(p.get("id")): p for p in curation_801}

orig_bak_path = os.path.join(BASE_DIR, "siwasup_all_properties.json.bak")
if not os.path.exists(orig_bak_path):
    shutil.copy2(os.path.join(BASE_DIR, "siwasup_all_properties.json"), orig_bak_path)
with open(orig_bak_path, "r", encoding="utf-8") as f:
    orig_119 = json.load(f)

orig_by_id = {str(p.get("id")): p for p in orig_119}

def infer_cat(title):
    t = (title or "")
    if any(k in t for k in ["คอนโด", "ห้องชุด", "ลุมพินี", "เซ็นทริค"]):
        return "คอนโด"
    if any(k in t for k in ["ทาวน์โฮม", "ทาวน์เฮ้าส์", "ทาวน์เฮาส์"]):
        return "ทาวน์โฮม"
    if any(k in t for k in ["อาคารพาณิชย์", "ตึกแถว", "โฮมออฟฟิศ"]):
        return "อาคารพาณิชย์"
    if "ที่ดิน" in t:
        return "ที่ดิน"
    return "บ้านเดี่ยว"

final_properties = []
seen_ids = set()

# A) First: Add Bua's 43 curated properties at the very top!
for pid, sold_flag in bua_status_map.items():
    src = orig_by_id.get(pid) or curation_by_id.get(pid)
    if not src:
        continue
    item = dict(src)
    item["id"] = pid
    item["bank_source"] = "Siwasup"
    item["category"] = item.get("category") or infer_cat(item.get("title", ""))
    if sold_flag == "YES" or pid == "1100927":
        item["status"] = "sold_archive"
        item["is_image_soldout"] = True
        item["ribbon_text"] = "ขายแล้ว (บัวแจ้งตัดสต๊อก 30 ต.ค. 2569)"
    else:
        item["status"] = "available"
        item["is_image_soldout"] = False
        item["bua_verified"] = True
        if not item.get("title", "").startswith("✦"):
            item["description"] = f"[✓ บัวตรวจสถานะพร้อมขาย 30 ต.ค. 69] " + (item.get("description") or "")
    final_properties.append(item)
    seen_ids.add(pid)

# B) Second: Add remaining original 119 Siwasup properties
for op in orig_119:
    pid = str(op.get("id"))
    if pid in seen_ids:
        continue
    item = dict(op)
    item["bank_source"] = "Siwasup"
    final_properties.append(item)
    seen_ids.add(pid)

# C) Third: Add active curated Siwasup properties from all_curation_properties.json (non-soldout)
for cp in curation_801:
    pid = str(cp.get("id"))
    if pid in seen_ids:
        continue
    if cp.get("is_image_soldout") or cp.get("status") == "sold_archive":
        continue
    # Include up to 150 more clean Siwasup properties so Siwasup tab has ~280 listings
    if len(final_properties) >= 280:
        break
    item = dict(cp)
    item["bank_source"] = "Siwasup"
    item["status"] = "available"
    item["category"] = item.get("category") or infer_cat(item.get("title", ""))
    final_properties.append(item)
    seen_ids.add(pid)

print(f"[*] Siwasup portfolio count (including Bua's 43): {len(final_properties)}")

# D) Fourth: Add Real NPA Properties from catalog_index.json + r2_assets_manifest.json
with open(os.path.join(DATA_DIR, "catalog_index.json"), "r", encoding="utf-8") as f:
    cat_index = json.load(f)

with open(os.path.join(DATA_DIR, "r2_assets_manifest.json"), "r", encoding="utf-8") as f:
    r2_manifest = json.load(f)

TYPE_CODE_TO_TH = {
    "SDH": "บ้านเดี่ยว",
    "TH": "ทาวน์โฮม",
    "CD": "คอนโด",
    "LAND": "ที่ดิน",
    "COMM": "อาคารพาณิชย์",
    "CH": "อาคารพาณิชย์"
}

METRO_PROVS = {"Bangkok", "Nonthaburi", "Pathum Thani", "Samut Prakan", "Nakhon Pathom", "Samut Sakhon"}
BANK_QUOTAS = {"SAM": 200, "SCB": 200, "GSB": 150, "TTB": 150}
bank_added = {"SAM": 0, "SCB": 0, "GSB": 0, "TTB": 0}

# Sort catalog_index so Metro properties with images and reasonable prices (1M - 15M) come first
def npa_priority_key(p):
    is_metro = 0 if (p.get("pe") in METRO_PROVS or any(k in (p.get("p") or "") for k in ["กรุงเทพ", "นนทบุรี", "ปทุมธานี", "สมุทรปราการ"])) else 1
    pr = p.get("pr") or 0
    good_price = 0 if (800000 <= pr <= 15000000) else 1
    has_r2 = 0 if ("assets.siwasup.com" in str(p.get("thumb") or "")) else 1
    return (is_metro, has_r2, good_price, -(p.get("gc") or 0))

cat_sorted = sorted(cat_index, key=npa_priority_key)

for npa in cat_sorted:
    b = npa.get("b")
    if b not in BANK_QUOTAS or bank_added[b] >= BANK_QUOTAS[b]:
        continue
    thumb = npa.get("thumb") or ""
    if not thumb:
        continue
    code = str(npa.get("c") or npa.get("id"))
    if code in seen_ids:
        continue

    uuid = npa.get("id")
    cat_th = TYPE_CODE_TO_TH.get(npa.get("t"), npa.get("tn") or "บ้านเดี่ยว")
    if cat_th not in ["ทาวน์โฮม", "คอนโด", "บ้านเดี่ยว", "ที่ดิน", "อาคารพาณิชย์"]:
        cat_th = infer_cat(cat_th)

    prov_th = npa.get("p") or npa.get("pe") or "กรุงเทพมหานคร"
    dist_th = npa.get("d") or ""
    loc_str = f"{dist_th} • {prov_th}" if dist_th else prov_th

    pr_val = npa.get("pr") or 0
    price_str = f"{float(pr_val):,.0f} บาท" if pr_val else "สอบถามราคา"

    sqw = npa.get("sqw") or 0
    sqm = npa.get("sqm") or 0
    size_str = f"{sqw:g} ตร.ว." if sqw else (f"{sqm:g} ตร.ม." if sqm else "-")

    r2_entry = r2_manifest.get(uuid, {})
    gallery = r2_entry.get("gallery") or [thumb]
    if thumb not in gallery:
        gallery = [thumb] + gallery

    title_str = f"ทรัพย์ NPA {b}: {cat_th} โซน{dist_th} ({prov_th}) รหัส {code}"
    desc_str = (
        f"รหัสทรัพย์ {b}: {code} | ประเภท: {cat_th} | ทำเล: {loc_str} | "
        f"ขนาด: {size_str} | ทรัพย์รอการขาย (NPA) คัดพิเศษจาก {b} พร้อมยื่นข้อเสนอและนัดเปิดบ้านได้ทันที"
    )

    final_properties.append({
        "id": code,
        "code": code,
        "homerun_id": uuid,
        "title": title_str,
        "category": cat_th,
        "bank_source": b,
        "price": price_str,
        "location": loc_str,
        "size": size_str,
        "usable_area": f"{sqm:g} ตร.ม." if sqm else "-",
        "main_image": gallery[0],
        "gallery_count": len(gallery),
        "gallery": gallery[:8],
        "description": desc_str,
        "status": "available",
        "is_image_soldout": False
    })
    seen_ids.add(code)
    bank_added[b] += 1

print(f"[*] Added Real NPA Properties by Bank: {bank_added}")
print(f"[*] Total Unified Properties in Main Web: {len(final_properties)}")

# Write siwasup_all_properties.json and siwasup_all_properties.js
json_path = os.path.join(BASE_DIR, "siwasup_all_properties.json")
js_path = os.path.join(BASE_DIR, "siwasup_all_properties.js")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(final_properties, f, ensure_ascii=False, indent=2)

js_content = (
    "var ALL_PROPERTIES_DATA = "
    + json.dumps(final_properties, ensure_ascii=False, indent=2)
    + ";\n\nif (typeof window !== 'undefined') {\n"
    + "  window.SIWASUP_PROPERTIES = ALL_PROPERTIES_DATA;\n"
    + "  window.ALL_PROPERTIES_DATA = ALL_PROPERTIES_DATA;\n"
    + "}\n"
)
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"[*] Wrote siwasup_all_properties.js ({len(js_content):,} bytes)")
