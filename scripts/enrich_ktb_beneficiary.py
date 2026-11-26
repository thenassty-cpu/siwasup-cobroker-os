import json
import os
import shutil
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROPS_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.json")
BACKUP_PATH = os.path.join(BASE_DIR, "backups", "siwasup_all_properties_pre_ktb_lodge.json")

HEADERS_JSON = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://npa.krungthai.com",
    "Referer": "https://npa.krungthai.com/",
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


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


def fetch_ktb_detail(coll_grp_id, cate_no: int, is_speedy: int):
    payload = json.dumps({
        "speedDy": is_speedy if cate_no == 2 else 0,
        "collGrpId": str(coll_grp_id),
        "cateNo": int(cate_no or 0),
        "viewChannel": "BROWSER",
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://npa.krungthai.com/api/v1/product/searchSaleDetail",
        data=payload,
        headers=HEADERS_JSON,
        method="POST",
    )
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        res = json.loads(r.read().decode("utf-8", errors="ignore"))
    dr = res.get("dataResponse") if isinstance(res, dict) else res
    if isinstance(dr, list) and dr:
        it = dr[0]
        return {
            "lodge": str(it.get("lodge") or "").strip(),
            "assetTypeDetail": str(it.get("assetTypeDetail") or "").strip(),
        }
    return None


def main():
    os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
    shutil.copy2(PROPS_PATH, BACKUP_PATH)
    print(f"[Backup] Saved to {BACKUP_PATH}")

    with open(PROPS_PATH, "r", encoding="utf-8") as f:
        props = json.load(f)

    ktb_props = [p for p in props if p.get("bank_source") == "KTB"]
    target_codes = {str(p.get("code") or p.get("id", "").replace("KTB-", "")).strip() for p in ktb_props}
    print(f"[Target] {len(ktb_props)} KTB properties in siwasup_all_properties.json")

    first_items, paging = fetch_ktb_page(1)
    page_count = int(paging.get("pageCount") or 1)
    all_raw = list(first_items)
    if page_count > 1:
        with ThreadPoolExecutor(max_workers=10) as ex:
            futs = [ex.submit(fetch_ktb_page, pg) for pg in range(2, page_count + 1)]
            for fut in as_completed(futs):
                items, _ = fut.result()
                all_raw.extend(items)

    code_meta = {}
    for it in all_raw:
        cc = str(it.get("collCode") or "").strip()
        if cc in target_codes and it.get("collGrpId"):
            code_meta[cc] = (it["collGrpId"], int(it.get("cateNo") or 0), int(it.get("isSpeedy") or 0))
    print(f"[Matched] Found {len(code_meta)} / {len(target_codes)} live KTB IDs on npa.krungthai.com")

    details_by_code = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        fut_map = {ex.submit(fetch_ktb_detail, *meta): cc for cc, meta in code_meta.items()}
        for fut in as_completed(fut_map):
            cc = fut_map[fut]
            try:
                det = fut.result()
                if det:
                    details_by_code[cc] = det
            except Exception as e:
                print(f"[Warn] {cc}: {e}")

    print(f"[Fetched] Retrieved {len(details_by_code)} detail records")

    updated = 0
    for p in props:
        if p.get("bank_source") != "KTB":
            continue
        cc = str(p.get("code") or p.get("id", "").replace("KTB-", "")).strip()
        det = details_by_code.get(cc)
        if not det:
            continue

        lodge = det.get("lodge") or ""
        remark = det.get("assetTypeDetail") or ""
        specs = p.get("specs") if isinstance(p.get("specs"), dict) else {}

        if lodge:
            p["beneficiary"] = lodge
            specs["beneficiary"] = lodge
        if remark and remark != "-":
            p["remark"] = remark
            specs["remark"] = remark
        p["specs"] = specs

        desc = p.get("description") or ""
        lines = [ln for ln in desc.splitlines() if not ln.startswith("ผู้มีสิทธิประโยชน์:") and not ln.startswith("หมายเหตุ:")]
        if lodge:
            lines.append(f"ผู้มีสิทธิประโยชน์: {lodge}")
        if remark and remark != "-":
            lines.append(f"หมายเหตุ: {remark}")
        p["description"] = "\n".join(lines)
        updated += 1

    with open(PROPS_PATH, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=2)

    print(f"[Done] Updated {updated} KTB properties in {PROPS_PATH}")


if __name__ == "__main__":
    main()
