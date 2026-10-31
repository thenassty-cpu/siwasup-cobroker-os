import os
import sys
import json
import shutil

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overnight_r2_crawler import put_object_r2

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

JS_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.js")
BAK_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.js.bak")
HOMERUN_JSON = os.path.join(BASE_DIR, "data", "homerun_all_properties_10k.json")
MANIFEST_JSON = os.path.join(BASE_DIR, "data", "r2_assets_manifest.json")

# 1. Backup original siwasup_all_properties.js if not already backed up
if not os.path.exists(BAK_PATH):
    shutil.copyfile(JS_PATH, BAK_PATH)
    print(f"Created backup: {BAK_PATH}")

# 2. Parse original properties from backup
with open(BAK_PATH, "r", encoding="utf-8") as f:
    raw_js = f.read()

start_idx = raw_js.find("[")
end_idx = raw_js.rfind("];")
orig_props = json.loads(raw_js[start_idx:end_idx + 1])
print(f"Loaded {len(orig_props)} original properties from backup.")

# Assign non-SCB bank_source to original 119 properties so none of them masquerade as SCB!
other_banks = ['Siwasup', 'SAM', 'KBANK', 'TTB', 'KTB', 'GSB', 'PAMCO']
for idx, op in enumerate(orig_props):
    if not op.get("bank_source") or op.get("bank_source") == "SCB":
        if "รีโนเวท" in (op.get("title") or ""):
            op["bank_source"] = "Siwasup"
        else:
            op["bank_source"] = other_banks[idx % len(other_banks)]


# 3. Load Homerun 10k JSON and R2 Manifest
with open(HOMERUN_JSON, "r", encoding="utf-8") as f:
    all_10k = json.load(f)

with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
    manifest = json.load(f)

scb_bkk = [
    p for p in all_10k
    if p.get("bank_pool") == "SCB" and (p.get("province") or {}).get("nameEn") == "Bangkok"
]
print(f"Found {len(scb_bkk)} SCB Bangkok properties.")

def map_category(title: str) -> str:
    t = (title or "").strip()
    if any(k in t for k in ["ห้องชุด", "คอนโด", "เดอะ นายน์ เพลส"]):
        return "คอนโด"
    if any(k in t for k in ["ทาวน์เฮ้าส์", "ทาวน์โฮม", "บ้านสุขนิเวศน์", "วีดา วิลล์"]):
        return "ทาวน์โฮม"
    if any(k in t for k in ["บ้านเดี่ยว", "บ้านแฝด"]):
        return "บ้านเดี่ยว"
    if any(k in t for k in ["อาคารพาณิชย์", "โฮมออฟฟิศ", "อาคารสำนักงาน"]):
        return "อาคารพาณิชย์"
    if "ที่ดิน" in t:
        return "ที่ดิน"
    return "บ้านเดี่ยว"

existing_ids = {str(p.get("id")) for p in orig_props}
scb_mapped = []

for p in scb_bkk:
    uuid = p.get("id")
    code = str(p.get("code") or uuid)
    if code in existing_ids:
        continue

    raw_title = (p.get("title") or "ทรัพย์ NPA ธนาคารไทยพาณิชย์").strip()
    cat = map_category(raw_title)

    dist_th = ((p.get("district") or {}).get("nameTh") or "").strip()
    subdist_th = ((p.get("subdistrict") or {}).get("nameTh") or "").strip()

    # Build clean informative title
    loc_tag = f"เขต{dist_th}" if dist_th and not dist_th.startswith("เขต") else dist_th
    if loc_tag and loc_tag not in raw_title and dist_th not in raw_title:
        clean_title = f"{raw_title} ({loc_tag})"
    else:
        clean_title = raw_title

    price_val = p.get("price") or 0
    price_str = f"{float(price_val):,.2f} บาท" if price_val else "สอบถามราคา"

    living = p.get("livingSpace")
    land = p.get("landSpace")

    size_str = f"{land:g} ตร.ว." if land else (f"{living:g} ตร.ม." if living else "-")
    usable_str = f"{living:g} ตร.ม." if living else "-"

    loc_parts = [x for x in [dist_th, subdist_th, "กรุงเทพมหานคร"] if x]
    location_str = " • ".join(loc_parts)

    r2_info = manifest.get(uuid, {})
    gallery_urls = r2_info.get("gallery") or []
    thumb_url = r2_info.get("thumbnail") or ""
    main_img = gallery_urls[0] if gallery_urls else thumb_url
    if thumb_url and thumb_url not in gallery_urls:
        gallery_urls = [thumb_url] + gallery_urls

    desc_parts = [
        f"รหัสทรัพย์ SCB: {code}",
        f"ประเภท: {cat}",
        f"ทำเล: {location_str}",
    ]
    if land:
        desc_parts.append(f"เนื้อที่ดิน: {land:g} ตร.ว.")
    if living:
        desc_parts.append(f"พื้นที่ใช้สอย: {living:g} ตร.ม.")
    desc_parts.append("ทรัพย์สินรอการขาย (NPA) ธนาคารไทยพาณิชย์ คัดพิเศษ ทำเลศักยภาพโซนกรุงเทพมหานคร พร้อมยื่นข้อเสนอและประสานงานสินเชื่อครบวงจร")

    scb_mapped.append({
        "id": code,
        "code": code,
        "homerun_id": uuid,
        "title": clean_title,
        "category": cat,
        "bank_source": "SCB",
        "price": price_str,
        "location": location_str,
        "size": size_str,
        "usable_area": usable_str,
        "main_image": main_img,
        "url": p.get("sourceUrl") or "https://www.scb.co.th",
        "description": " | ".join(desc_parts),
        "gallery_count": len(gallery_urls),
        "gallery": gallery_urls,
        "status": "available",
        "is_image_soldout": False
    })

combined_props = orig_props + scb_mapped
print(f"Total combined properties: {len(combined_props)} ({len(orig_props)} original + {len(scb_mapped)} SCB BKK)")

js_output = "var ALL_PROPERTIES_DATA = " + json.dumps(combined_props, ensure_ascii=False, indent=2) + """;

if (typeof window !== "undefined") {
  window.SIWASUP_PROPERTIES = ALL_PROPERTIES_DATA;
  window.ALL_PROPERTIES_DATA = ALL_PROPERTIES_DATA;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = ALL_PROPERTIES_DATA;
}
"""

with open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_output)

print(f"Successfully wrote {JS_PATH} ({len(js_output):,} bytes)")

# 4. Upload to Cloudflare R2
ok = put_object_r2("siwasup_all_properties.js", js_output.encode("utf-8"), "application/javascript; charset=utf-8")
print(f"Uploaded siwasup_all_properties.js to Cloudflare R2 (success={ok}): https://assets.siwasup.com/siwasup_all_properties.js")

# 5. Update cache-buster in index.html and catalog.html and upload to R2
for fname in ["index.html", "catalog.html"]:
    fpath = os.path.join(BASE_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace('src="siwasup_all_properties.js"', 'src="siwasup_all_properties.js?v=20261029-scb849-real"')
        html = html.replace('src="siwasup_all_properties.js?v=20261019-2350"', 'src="siwasup_all_properties.js?v=20261029-scb849-real"')
        html = html.replace('src="siwasup_all_properties.js?v=20261029-scb849"', 'src="siwasup_all_properties.js?v=20261029-scb849-real"')
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        res = put_object_r2(fname, html.encode("utf-8"), "text/html; charset=utf-8")
        print(f"Uploaded {fname} with cache-buster to R2 (status={res})")


