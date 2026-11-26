import json
import os
import re
import shutil
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROPS_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.json")
BACKUP_PATH = os.path.join(BASE_DIR, "backups", "siwasup_all_properties_pre_kbank.json")
KBANK_MASTER_PATH = os.path.join(BASE_DIR, "data", "kbank_property_master.json")
CATALOG_INDEX_PATH = os.path.join(BASE_DIR, "data", "catalog_index.json")

BKK_VICINITY = [
    "กรุงเทพมหานคร",
    "นนทบุรี",
    "ปทุมธานี",
    "สมุทรปราการ",
    "สมุทรสาคร",
    "นครปฐม",
]

IMG_PREFIX = "https://pfsapp.kasikornbank.com/pfs-frontend-api/property-images"


def normalize_category(raw_type: str, title: str = "") -> str:
    s = f"{raw_type} {title}".lower()
    if "ทาวน์" in s:
        return "ทาวน์โฮม"
    if "คอนโด" in s or "ห้องชุด" in s:
        return "คอนโด"
    if "ที่ดิน" in s and "สิ่งปลูกสร้าง" not in s and "บ้าน" not in s:
        return "ที่ดิน"
    if "พาณิชย์" in s or "ตึกแถว" in s or "สำนักงาน" in s or "โรงงาน" in s or "โกดัง" in s:
        return "อาคารพาณิชย์"
    if "บ้าน" in s:
        return "บ้านเดี่ยว"
    return "บ้านเดี่ยว"


def map_type_code(cat: str) -> str:
    if cat == "ทาวน์โฮม":
        return "TH"
    if cat == "คอนโด":
        return "CD"
    if cat == "ที่ดิน":
        return "LAND"
    if cat == "อาคารพาณิชย์":
        return "COMM"
    return "SDH"


def format_area(it: dict) -> str:
    rai = int(it.get("Rai") or 0)
    ngan = int(it.get("Ngan") or 0)
    sqw = float(it.get("SquareArea") or 0)
    total_sqw = rai * 400 + ngan * 100 + sqw
    if total_sqw > 0:
        return f"{total_sqw:g} ตร.ว."
    av = str(it.get("AreaValue") or it.get("Area") or "").strip()
    return av if av else "-"


def normalize_kbank_item(it: dict) -> dict | None:
    if it.get("IsSoldOut"):
        return None
    pid = str(it.get("PropertyID") or "").strip()
    pcode = str(it.get("PropertyIDFormat") or pid).strip()
    if not pid:
        return None

    raw_type = re.sub(r"^\d+\s*", "", str(it.get("PropertyTypeName") or "")).strip()
    prov = str(it.get("ProvinceName") or "").strip()
    amp = str(it.get("AmphurName") or "").strip()
    tam = str(it.get("TambonName") or "").strip()
    village = str(it.get("VillageTH") or "").strip()
    road = str(it.get("RoadTH") or "").strip()
    soi = str(it.get("SoiTH") or "").strip()

    cat = normalize_category(raw_type, village)
    if village:
        title = f"{raw_type or cat} {village} ({amp} {prov}) รหัส {pcode}".strip()
    else:
        title = f"ทรัพย์ NPA กสิกร: {raw_type or cat} โซน{amp} ({prov}) รหัส {pcode}".strip()

    sell_p = int(float(it.get("SellPrice") or 0))
    promo_p = int(float(it.get("PromotionPrice") or 0))
    if sell_p <= 0:
        return None

    size_str = format_area(it)
    usable = float(it.get("UseableArea") or 0)
    usable_str = f"{usable:g} ตร.ม." if usable > 0 else "-"

    media = it.get("PropertyMediaes") or []
    gallery = []
    for m in media:
        mt = str(m.get("MediaType") or "")
        mp = str(m.get("MediaPath") or "")
        if mp and "IMAGE-PC" in mt:
            gallery.append(f"{IMG_PREFIX}{mp}")
    if not gallery:
        for m in media:
            mt = str(m.get("MediaType") or "")
            mp = str(m.get("MediaPath") or "")
            if mp and "IMAGE-" in mt:
                gallery.append(f"{IMG_PREFIX}{mp}")
    if not gallery:
        return None

    try:
        lat = float(it.get("Latitude") or 0)
        lng = float(it.get("Longtitude") or 0)
    except (TypeError, ValueError):
        lat, lng = 0.0, 0.0

    maint_status = str(it.get("PMMaintenanceStatus") or "").strip()
    addr_parts = [x for x in [
        f"ถ.{road}" if road else "",
        f"ซ.{soi}" if soi else "",
        f"ต.{tam}" if tam else "",
        f"อ.{amp}" if amp else "",
        prov,
    ] if x]
    addr_full = " ".join(addr_parts)

    desc_lines = [
        f"ประเภททรัพย์: {raw_type or cat}",
        f"ทำเลที่ตั้ง: {addr_full}",
        f"เนื้อที่ดิน: {size_str}",
    ]
    if village:
        desc_lines.insert(1, f"ชื่อโครงการ / หมู่บ้าน: {village}")
    if usable_str != "-":
        desc_lines.append(f"พื้นที่ใช้สอย: {usable_str}")
    if maint_status:
        desc_lines.append(f"หมายเหตุ: {maint_status}")

    specs = {
        "address_full": addr_full,
    }
    if village:
        specs["project_name"] = village
    if maint_status:
        specs["remark"] = maint_status

    prop = {
        "id": f"KBANK-{pid}",
        "code": pcode,
        "title": title,
        "category": cat,
        "bank_source": "KBANK",
        "province": prov,
        "province_th": prov,
        "district_th": amp,
        "subdistrict_th": tam,
        "location": f"{amp} • {prov}".strip(" •"),
        "size": size_str,
        "usable_area": usable_str,
        "bedrooms": int(it.get("Bedroom") or 0),
        "bathrooms": int(it.get("Bathroom") or 0),
        "main_image": gallery[0],
        "gallery_count": len(gallery),
        "gallery": gallery[:8],
        "description": "\n".join(desc_lines),
        "specs": specs,
        "status": "booked" if it.get("IsReserve") else "available",
        "search_keywords": f"KBANK กสิกร {pcode} {village} {addr_full} {raw_type}".strip(),
    }

    if promo_p > 0 and promo_p < sell_p:
        prop["original_price"] = f"{sell_p:,} บาท"
        prop["special_price"] = f"{promo_p:,} บาท"
        prop["price"] = f"{promo_p:,} บาท"
        prop["_eff_price"] = promo_p
    else:
        prop["price"] = f"{sell_p:,} บาท"
        prop["_eff_price"] = sell_p

    if maint_status:
        prop["remark"] = maint_status
    if lat and lng:
        prop["lat"] = lat
        prop["lng"] = lng
        prop["latitude"] = lat
        prop["longitude"] = lng

    return prop


def main():
    if not os.environ.get("CI"):
        os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
        shutil.copy2(PROPS_PATH, BACKUP_PATH)
        print(f"[Backup] Saved to {BACKUP_PATH}")

    raw_items = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome", headless=False, args=["--window-position=-2000,-2000"])
        ctx = browser.new_context(locale="th-TH")
        page = ctx.new_page()
        with page.expect_response(lambda r: "GetProperties" in r.url, timeout=30000):
            page.goto(
                "https://www.kasikornbank.com/th/propertyforsale/search/pages/index.aspx",
                wait_until="domcontentloaded",
                timeout=30000,
            )

        # Fetch 40 pages (2,000 newest properties) without Provinces filter (Provinces expects numeric IDs)
        res_js = page.evaluate(
            """async () => {
                const fetchPage = async (pg) => {
                    const r = await fetch('/Custom/KWEB2020/NPA2023Backend13.aspx/GetProperties', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest'},
                        body: JSON.stringify({filter: {CurrentPageIndex: pg, PageSize: 50, Ordering: 'New'}})
                    });
                    if (!r.ok) return {items: [], total: 0};
                    const outer = await r.json();
                    const d = typeof outer.d === 'string' ? JSON.parse(outer.d) : (outer.d || {});
                    const data = d.Data || {};
                    return {items: data.Items || [], total: data.TotalRows || 0};
                };
                const first = await fetchPage(1);
                const total = first.total || 0;
                const maxPages = Math.min(Math.ceil(total / 50), 40);
                let all = [...first.items];
                for (let pg = 2; pg <= maxPages; pg += 4) {
                    const batch = [];
                    for (let k = pg; k < pg + 4 && k <= maxPages; k++) {
                        batch.push(fetchPage(k));
                    }
                    const results = await Promise.all(batch);
                    for (const res of results) all.push(...res.items);
                }
                return {total, fetched: all.length, items: all};
            }"""
        )
        print(f"[KBANK] Total={res_js['total']}, Fetched={res_js['fetched']}")
        raw_items = res_js["items"]
        browser.close()

    normalized = []
    seen = set()
    for it in raw_items:
        p = normalize_kbank_item(it)
        if p and p["id"] not in seen:
            seen.add(p["id"])
            normalized.append(p)

    with open(KBANK_MASTER_PATH, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
    print(f"[KBANK Master] Saved {len(normalized)} normalized items to {KBANK_MASTER_PATH}")

    # Select top 500 available items for main web catalog (prioritize BKK+Vicinity first)
    bkk_avail = [p for p in normalized if p.get("status") == "available" and any(bv in p.get("province_th", "") for bv in BKK_VICINITY)]
    other_avail = [p for p in normalized if p.get("status") == "available" and p not in bkk_avail]
    for_catalog = (bkk_avail + other_avail)[:500]
    for p in normalized:
        p.pop("_eff_price", None)

    with open(PROPS_PATH, "r", encoding="utf-8") as f:
        main_props = json.load(f)

    # Remove any old KBANK entries before merging fresh ones
    main_props = [p for p in main_props if p.get("bank_source") != "KBANK"]
    main_props.extend(for_catalog)

    with open(PROPS_PATH, "w", encoding="utf-8") as f:
        json.dump(main_props, f, ensure_ascii=False, indent=2)
    print(f"[Main Catalog] Added {len(for_catalog)} KBANK items -> Total={len(main_props)}")

    # Sync to data/catalog_index.json for LINE bot
    if os.path.exists(CATALOG_INDEX_PATH):
        with open(CATALOG_INDEX_PATH, "r", encoding="utf-8") as f:
            cat_idx = json.load(f)
        cat_idx = [c for c in cat_idx if c.get("b") != "KBANK"]
        for p in normalized:
            pr_num = int(re.sub(r"[^0-9]", "", p["price"].split(".")[0]) or 0)
            m_sqw = re.search(r"(\d+(?:\.\d+)?)", p["size"])
            m_sqm = re.search(r"(\d+(?:\.\d+)?)", p["usable_area"])
            sqw_num = float(m_sqw.group(1)) if m_sqw else 0
            sqm_num = float(m_sqm.group(1)) if m_sqm else 0
            cat_idx.append({
                "id": p["id"],
                "c": p["code"],
                "b": "KBANK",
                "t": map_type_code(p["category"]),
                "tn": p["category"],
                "p": p["province_th"],
                "pe": p["province_th"],
                "d": p["district_th"],
                "pr": pr_num,
                "sqm": sqm_num,
                "sqw": sqw_num,
                "bed": p["bedrooms"],
                "bath": p["bathrooms"],
                "thumb": p["main_image"],
                "gc": p["gallery_count"],
            })
        with open(CATALOG_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(cat_idx, f, ensure_ascii=False)
        print(f"[Catalog Index] Synced {len(normalized)} KBANK items -> Total={len(cat_idx)}")


if __name__ == "__main__":
    main()
