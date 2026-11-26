import json
import os
import re
import shutil
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROPS_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.json")
BACKUP_PATH = os.path.join(BASE_DIR, "backups", "siwasup_all_properties_pre_ttb_promo.json")
CATALOG_INDEX_PATH = os.path.join(BASE_DIR, "data", "catalog_index.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://property.pamco.co.th",
    "Referer": "https://property.pamco.co.th/",
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def parse_price_int(val) -> int:
    if isinstance(val, (int, float)):
        return int(val)
    s = str(val or "").replace(",", "")
    m = re.search(r"(\d+)(?:\.\d+)?", s)
    return int(m.group(1)) if m else 0


def fetch_pamco_page(page: int, limit: int = 100):
    url = f"https://property-api-prod.pamco.co.th/property-new/display?page={page}&limit={limit}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
    shutil.copy2(PROPS_PATH, BACKUP_PATH)
    print(f"[Backup] Saved to {BACKUP_PATH}")

    first = fetch_pamco_page(1, 100)
    total = int(first.get("total") or 0)
    items = list(first.get("list") or [])
    total_pages = (total + 99) // 100
    print(f"[PAMCO/TTB API] Total={total}, pages={total_pages}")

    if total_pages > 1:
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = [ex.submit(fetch_pamco_page, pg, 100) for pg in range(2, total_pages + 1)]
            for fut in as_completed(futs):
                res = fut.result()
                items.extend(res.get("list") or [])

    by_code = {}
    for it in items:
        slug = str(it.get("slug") or "").strip().upper()
        if slug:
            by_code[slug] = it

    print(f"[Indexed] {len(by_code)} unique PAMCO/TTB codes")

    today_iso = date.today().isoformat()
    with open(PROPS_PATH, "r", encoding="utf-8") as f:
        props = json.load(f)

    promo_updated = 0
    for p in props:
        if p.get("bank_source") not in ("TTB", "PAMCO"):
            continue
        code = str(p.get("code") or p.get("id") or "").replace("PAMCO_", "").strip().upper()
        it = by_code.get(code)
        if not it:
            continue

        # Normal price from lowprice
        normal_p = 0
        lp_list = it.get("lowprice") or []
        if isinstance(lp_list, list) and lp_list:
            normal_p = parse_price_int(lp_list[0].get("lowprice"))
        if not normal_p:
            normal_p = parse_price_int(p.get("price"))

        # Promo price from idEvent
        ev_list = it.get("idEvent") or []
        promo_p = 0
        start_dt = ""
        end_dt = ""
        if isinstance(ev_list, list) and ev_list:
            for ev in ev_list:
                if ev.get("active") and ev.get("activePrice"):
                    cand = parse_price_int(ev.get("priceSp1"))
                    s_dt = str(ev.get("startDate") or "")[:10]
                    e_dt = str(ev.get("endDate") or "")[:10]
                    if cand > 0 and (not e_dt or e_dt >= today_iso):
                        promo_p = cand
                        start_dt = s_dt
                        end_dt = e_dt
                        break

        if promo_p > 0 and normal_p > promo_p:
            p["original_price"] = f"{normal_p:,} บาท"
            p["special_price"] = f"{promo_p:,} บาท"
            p["price"] = f"{promo_p:,} บาท"
            if start_dt:
                p["promo_start_date"] = start_dt
            if end_dt:
                p["promo_end_date"] = end_dt
            promo_updated += 1

    with open(PROPS_PATH, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=2)
    print(f"[Done] Updated {promo_updated} TTB/PAMCO properties with active promo prices in {PROPS_PATH}")

    # Also sync catalog_index.json for TTB items
    if os.path.exists(CATALOG_INDEX_PATH):
        with open(CATALOG_INDEX_PATH, "r", encoding="utf-8") as f:
            cat = json.load(f)
        cat_updated = 0
        for c in cat:
            if c.get("b") != "TTB":
                continue
            code = str(c.get("c") or "").strip().upper()
            it = by_code.get(code)
            if not it:
                continue
            ev_list = it.get("idEvent") or []
            if isinstance(ev_list, list) and ev_list:
                for ev in ev_list:
                    if ev.get("active") and ev.get("activePrice"):
                        cand = parse_price_int(ev.get("priceSp1"))
                        e_dt = str(ev.get("endDate") or "")[:10]
                        if cand > 0 and (not e_dt or e_dt >= today_iso):
                            c["pr"] = cand
                            cat_updated += 1
                            break
        with open(CATALOG_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(cat, f, ensure_ascii=False)
        print(f"[Done] Synced {cat_updated} TTB promo prices in {CATALOG_INDEX_PATH}")


if __name__ == "__main__":
    main()
