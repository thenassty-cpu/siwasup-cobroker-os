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
BACKUP_PATH = os.path.join(BASE_DIR, "backups", "siwasup_all_properties_pre_ktb_gsb_promo.json")
CATALOG_INDEX_PATH = os.path.join(BASE_DIR, "data", "catalog_index.json")

HEADERS_JSON = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://npa.krungthai.com",
    "Referer": "https://npa.krungthai.com/",
}
HEADERS_HTML = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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


def fetch_ktb_page(page_num: int):
    payload = json.dumps({"paging": {"currentPage": page_num, "rowsPerPage": 100, "totalRows": 0}}).encode("utf-8")
    req = urllib.request.Request(
        "https://npa.krungthai.com/api/v1/product/searchAll",
        data=payload,
        headers=HEADERS_JSON,
        method="POST",
    )
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        res = json.loads(r.read().decode("utf-8", errors="ignore"))
    return res.get("dataResponse", []), res.get("paging", {})


def fetch_gsb_page(page_num: int, page_size: int = 100):
    url = f"https://npa-assets.gsb.or.th/asset/npa/all?page={page_num}&page_size={page_size}"
    req = urllib.request.Request(url, headers=HEADERS_HTML)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        html = r.read().decode("utf-8", errors="ignore")
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    if not m:
        return [], 0
    d = json.loads(m.group(1))
    list_obj = d.get("props", {}).get("pageProps", {}).get("list", {})
    rows = list_obj.get("data", {}).get("rows", [])
    total = int(list_obj.get("asset_count") or 0)
    return rows, total


def main():
    if not os.environ.get("CI"):
        os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
        shutil.copy2(PROPS_PATH, BACKUP_PATH)
        print(f"[Backup] Saved to {BACKUP_PATH}")

    today_iso = date.today().isoformat()

    # 1. Fetch KTB
    ktb_first, ktb_paging = fetch_ktb_page(1)
    ktb_pages = int(ktb_paging.get("pageCount") or 1)
    ktb_raw = list(ktb_first)
    if ktb_pages > 1:
        with ThreadPoolExecutor(max_workers=10) as ex:
            for fut in as_completed([ex.submit(fetch_ktb_page, pg) for pg in range(2, ktb_pages + 1)]):
                items, _ = fut.result()
                ktb_raw.extend(items)
    ktb_by_code = {}
    for it in ktb_raw:
        cc = str(it.get("collCode") or "").strip().upper()
        if cc:
            ktb_by_code[cc] = it
    print(f"[KTB] Fetched {len(ktb_by_code)} unique codes across {ktb_pages} pages")

    # 2. Fetch GSB
    gsb_first, gsb_total = fetch_gsb_page(1, 100)
    gsb_pages = (gsb_total + 99) // 100 if gsb_total else 1
    gsb_raw = list(gsb_first)
    if gsb_pages > 1:
        with ThreadPoolExecutor(max_workers=8) as ex:
            for fut in as_completed([ex.submit(fetch_gsb_page, pg, 100) for pg in range(2, gsb_pages + 1)]):
                try:
                    rows, _ = fut.result()
                    gsb_raw.extend(rows)
                except Exception as e:
                    print(f"[GSB Warn] {e}")
    gsb_by_code = {}
    for it in gsb_raw:
        for key in (
            str(it.get("asset_group_id_npa") or "").strip().upper(),
            str(it.get("asset_group_id") or "").strip().upper(),
            f"GSB_{it.get('asset_id')}" if it.get("asset_id") else "",
        ):
            if key:
                gsb_by_code[key] = it
    print(f"[GSB] Fetched {len(gsb_raw)} rows ({len(gsb_by_code)} lookup keys) across {gsb_pages} pages")

    # 3. Update siwasup_all_properties.json
    with open(PROPS_PATH, "r", encoding="utf-8") as f:
        props = json.load(f)

    ktb_updated = 0
    gsb_updated = 0
    for p in props:
        bank = p.get("bank_source")
        code = str(p.get("code") or p.get("id") or "").replace("KTB-", "").strip().upper()

        if bank == "KTB":
            it = ktb_by_code.get(code)
            if not it:
                continue
            cur_p = parse_price_int(it.get("price"))
            nml_p = parse_price_int(it.get("nmlPrice"))
            start_dt = str(it.get("priceStrDt") or "")[:10]
            end_dt = str(it.get("priceEndDt") or "")[:10]
            if cur_p > 0 and nml_p > cur_p and (not end_dt or end_dt >= today_iso):
                p["original_price"] = f"{nml_p:,} บาท"
                p["special_price"] = f"{cur_p:,} บาท"
                p["price"] = f"{cur_p:,} บาท"
                if start_dt:
                    p["promo_start_date"] = start_dt
                if end_dt:
                    p["promo_end_date"] = end_dt
                ktb_updated += 1
            elif p.get("special_price") and (nml_p > 0 or cur_p > 0):
                rev_p = nml_p or cur_p
                p["price"] = f"{rev_p:,} บาท"
                p.pop("original_price", None)
                p.pop("special_price", None)
                p.pop("promo_start_date", None)
                p.pop("promo_end_date", None)

        elif bank == "GSB":
            it = gsb_by_code.get(code) or gsb_by_code.get(str(p.get("id") or "").strip().upper())
            if not it:
                continue
            promo_p = parse_price_int(it.get("xprice"))
            orig_p = parse_price_int(it.get("current_offer_price") or it.get("group_sell_price"))
            end_dt = str(it.get("end_date") or "")[:10]
            if end_dt == "None":
                end_dt = ""
            if promo_p > 0 and orig_p > promo_p and (not end_dt or end_dt >= today_iso):
                p["original_price"] = f"{orig_p:,} บาท"
                p["special_price"] = f"{promo_p:,} บาท"
                p["price"] = f"{promo_p:,} บาท"
                if end_dt:
                    p["promo_end_date"] = end_dt
                gsb_updated += 1
            elif p.get("special_price") and orig_p > 0:
                p["price"] = f"{orig_p:,} บาท"
                p.pop("original_price", None)
                p.pop("special_price", None)
                p.pop("promo_start_date", None)
                p.pop("promo_end_date", None)

    with open(PROPS_PATH, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=2)
    print(f"[Done] Updated KTB={ktb_updated}, GSB={gsb_updated} promo properties in {PROPS_PATH}")

    # 4. Sync catalog_index.json for KTB & GSB
    if os.path.exists(CATALOG_INDEX_PATH):
        with open(CATALOG_INDEX_PATH, "r", encoding="utf-8") as f:
            cat = json.load(f)
        cat_gsb = 0
        cat_ktb = 0
        for c in cat:
            b = c.get("b")
            code = str(c.get("c") or "").strip().upper()
            if b == "GSB":
                it = gsb_by_code.get(code) or gsb_by_code.get(str(c.get("id") or "").strip().upper())
                if it:
                    promo_p = parse_price_int(it.get("xprice"))
                    orig_p = parse_price_int(it.get("current_offer_price") or it.get("group_sell_price"))
                    if promo_p > 0 and orig_p > promo_p:
                        c["pr"] = promo_p
                        cat_gsb += 1
            elif b == "KTB":
                it = ktb_by_code.get(code)
                if it:
                    cur_p = parse_price_int(it.get("price"))
                    if cur_p > 0:
                        c["pr"] = cur_p
                        cat_ktb += 1
        with open(CATALOG_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(cat, f, ensure_ascii=False)
        print(f"[Done] Synced catalog_index.json: GSB={cat_gsb}, KTB={cat_ktb}")


if __name__ == "__main__":
    main()
