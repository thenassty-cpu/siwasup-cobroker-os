"""Build data/consignment_seed_test.json from raw Google Sheet export and R2 WebP image index."""

import json
import os
import re
import time

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(ROOT_DIR, "data", "consignment_sheet_raw_20261119.json")
IMG_PATH = os.path.join(ROOT_DIR, "data", "consignment_images_index_20261119.json")
OUT_PATH = os.path.join(ROOT_DIR, "data", "consignment_seed_test.json")


def parse_price_baht(raw_price: str) -> tuple[int, str]:
    """Convert sheet price_million string to integer Baht and optional extra note."""
    text = (raw_price or "").strip()
    if not text:
        return 0, ""
    m = re.match(r"^([\d,]+(?:\.\d+)?)\s*(.*)$", text)
    if not m:
        return 0, text
    num = float(m.group(1).replace(",", ""))
    extra = m.group(2).strip()
    # Values >= 10,000 (e.g., 750,000) are already in Baht rather than millions
    baht = round(num) if num >= 10000 else round(num * 1_000_000)
    return baht, extra


def parse_int_safe(val: str) -> int:
    m = re.search(r"\d+", (val or "").replace(",", ""))
    return int(m.group(0)) if m else 0


def main():
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_props = json.load(f)["properties"]
    with open(IMG_PATH, "r", encoding="utf-8") as f:
        images_by_prop = json.load(f)["images_by_property"]

    out_props = []
    for r in raw_props:
        pid = r["id"]
        price_baht, price_note = parse_price_baht(r.get("price_million", ""))
        imgs = images_by_prop.get(pid, [])
        status = "available" if imgs else "pending_photos"

        district = (r.get("district") or "").strip()
        province = (r.get("province") or "").strip()
        zone = " • ".join(p for p in (district, province) if p) or (r.get("address") or "").strip()

        notes = []
        if r.get("commission"):
            notes.append(f"ค่าคอม: {r['commission']}")
        if r.get("condition"):
            notes.append(f"สภาพ: {r['condition']}")
        if price_note:
            notes.append(price_note)

        out_props.append({
            "id": pid,
            "title": r.get("title", ""),
            "property_type": r.get("property_type", ""),
            "price": price_baht,
            "zone": zone,
            "district": district,
            "province": province,
            "address": r.get("address", ""),
            "area_sqw": (r.get("land_area_sqw") or "").strip(),
            "usable_area_sqm": (r.get("usable_area_sqm") or "").strip(),
            "bedrooms": parse_int_safe(r.get("bedrooms", "")),
            "bathrooms": parse_int_safe(r.get("bathrooms", "")),
            "parking": parse_int_safe(r.get("parking", "")),
            "consignment_type": "open_contract",
            "contract_expiry": "",
            "status": status,
            "caretaker_name": r.get("caretaker") or "คุณบัว (ดูแลหลัก)",
            "assigned_agent_code": "",
            "assigned_agent_name": "",
            "internal_note": " • ".join(notes),
            "images": imgs,
            "contract_files": [],
        })

    payload = {
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(out_props),
        "properties": out_props,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    avail = sum(1 for p in out_props if p["status"] == "available")
    pend = sum(1 for p in out_props if p["status"] == "pending_photos")
    total_imgs = sum(len(p["images"]) for p in out_props)
    print(f"[+] Wrote {len(out_props)} properties (available={avail}, pending_photos={pend}, images={total_imgs}) -> {OUT_PATH}")


if __name__ == "__main__":
    main()
