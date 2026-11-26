import csv
import json
import os
import re
import shutil
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROPS_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.json")
BACKUP_PATH = os.path.join(BASE_DIR, "backups", "siwasup_all_properties_pre_geocode.json")
CENTROIDS_PATH = os.path.join(BASE_DIR, "data", "thai_geo_centroids.json")
LOG_JSON_PATH = os.path.join(BASE_DIR, "data", "geocode_audit_log.json")
LOG_CSV_PATH = os.path.join(BASE_DIR, "data", "geocode_audit_log.csv")


def clean_geo_name(s: str) -> str:
    s = str(s or "").strip()
    s = re.sub(r"^(?:จังหวัด|จ\.|อำเภอ|อ\.|เขต|ตำบล|ต\.|แขวง)\s*", "", s)
    return s.strip()


def has_valid_coords(p: dict) -> bool:
    try:
        lat = float(p.get("lat") or p.get("latitude") or 0)
        lng = float(p.get("lng") or p.get("longitude") or 0)
        return lat != 0.0 and lng != 0.0
    except (TypeError, ValueError):
        return False


def main():
    if not os.environ.get("CI"):
        os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
        shutil.copy2(PROPS_PATH, BACKUP_PATH)
        print(f"[Backup] Saved to {BACKUP_PATH}")

    with open(CENTROIDS_PATH, "r", encoding="utf-8") as f:
        geo = json.load(f)

    provinces = geo.get("provinces", {})
    districts = geo.get("districts", [])
    subdistricts = geo.get("subdistricts", [])

    # Sort longest names first to avoid partial match collisions
    prov_keys = sorted(provinces.keys(), key=len, reverse=True)
    districts_sorted = sorted(districts, key=lambda x: len(x.get("d", "")), reverse=True)
    subdistricts_sorted = sorted(subdistricts, key=lambda x: len(x.get("t", "")), reverse=True)

    with open(PROPS_PATH, "r", encoding="utf-8") as f:
        props = json.load(f)

    bkk_tz = timezone(timedelta(hours=7))
    now_str = datetime.now(bkk_tz).strftime("%Y-%m-%d %H:%M:%S+07:00")

    audit_log = []
    still_missing = []

    for p in props:
        if has_valid_coords(p):
            continue

        specs = p.get("specs") if isinstance(p.get("specs"), dict) else {}
        sub_raw = clean_geo_name(p.get("subdistrict_th") or "")
        dist_raw = clean_geo_name(p.get("district_th") or "")
        prov_raw = clean_geo_name(p.get("province_th") or p.get("province") or "")

        # Normalize Bangkok aliases
        if prov_raw in ("กทม", "กทม.", "กรุงเทพ", "กรุงเทพฯ"):
            prov_raw = "กรุงเทพมหานคร"

        haystack = " ".join([
            str(p.get("location") or ""),
            str(specs.get("address_full") or ""),
            str(p.get("title") or ""),
            str(p.get("description") or "")[:400],
        ])
        haystack_norm = haystack.replace("กรุงเทพฯ", "กรุงเทพมหานคร").replace("กทม.", "กรุงเทพมหานคร")

        # Detect province if not explicitly set
        matched_prov = prov_raw if prov_raw in provinces else ""
        if not matched_prov:
            for pk in prov_keys:
                if pk in haystack_norm:
                    matched_prov = pk
                    break

        lat, lng = None, None
        level, matched_name = "", ""

        # 1. Subdistrict match (only if explicit subdistrict or paired with district/province)
        if sub_raw:
            for sd in subdistricts_sorted:
                if sd["t"] == sub_raw and (not matched_prov or sd["p"] == matched_prov) and (not dist_raw or sd["d"] == dist_raw):
                    lat, lng = sd["lat"], sd["lng"]
                    level = "subdistrict"
                    matched_name = f"{sd['t']} / {sd['d']} / {sd['p']}"
                    break

        # 2. District match
        if lat is None:
            if dist_raw:
                for ds in districts_sorted:
                    if ds["d"] == dist_raw and (not matched_prov or ds["p"] == matched_prov):
                        lat, lng = ds["lat"], ds["lng"]
                        level = "district"
                        matched_name = f"{ds['d']} / {ds['p']}"
                        break
            if lat is None:
                haystack_dist = haystack_norm.replace("กรุงเทพมหานคร", "")
                for ds in districts_sorted:
                    d_name = ds["d"]
                    if len(d_name) < 3:
                        continue
                    # Avoid matching 'เมือง' alone without prefix unless 'อำเภอเมือง' / 'อ.เมือง'
                    if d_name.startswith("เมือง") and d_name not in haystack_dist:
                        continue
                    if (f"เขต{d_name}" in haystack_dist or f"อำเภอ{d_name}" in haystack_dist or f"อ.{d_name}" in haystack_dist or d_name in haystack_dist):
                        if not matched_prov or ds["p"] == matched_prov:
                            lat, lng = ds["lat"], ds["lng"]
                            level = "district"
                            matched_name = f"{ds['d']} / {ds['p']}"
                            break

        # 3. Province fallback
        if lat is None and matched_prov and matched_prov in provinces:
            lat = provinces[matched_prov]["lat"]
            lng = provinces[matched_prov]["lng"]
            level = "province"
            matched_name = matched_prov

        if lat is not None and lng is not None:
            p["lat"] = lat
            p["lng"] = lng
            p["latitude"] = lat
            p["longitude"] = lng
            p["coord_source"] = f"auto_centroid_{level}"
            audit_log.append({
                "id": p.get("id"),
                "code": p.get("code") or "",
                "bank_source": p.get("bank_source") or "",
                "title": (p.get("title") or "")[:80],
                "location": p.get("location") or "",
                "reason": "missing_lat_lng",
                "matched_level": level,
                "matched_name": matched_name,
                "lat": lat,
                "lng": lng,
                "updated_at": now_str,
            })
        else:
            still_missing.append({
                "id": p.get("id"),
                "bank_source": p.get("bank_source"),
                "location": p.get("location"),
                "title": (p.get("title") or "")[:60],
            })

    with open(PROPS_PATH, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=2)

    with open(LOG_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": now_str,
            "total_geocoded": len(audit_log),
            "still_missing_count": len(still_missing),
            "by_level": {
                lv: sum(1 for x in audit_log if x["matched_level"] == lv)
                for lv in ("subdistrict", "district", "province")
            },
            "records": audit_log,
            "still_missing": still_missing,
        }, f, ensure_ascii=False, indent=2)

    with open(LOG_CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "code", "bank_source", "matched_level", "matched_name", "lat", "lng", "location", "title", "reason", "updated_at"])
        w.writeheader()
        w.writerows(audit_log)

    print(f"[Done] Geocoded {len(audit_log)} properties (still missing: {len(still_missing)})")
    print(f"  By level: subdistrict={sum(1 for x in audit_log if x['matched_level']=='subdistrict')}, district={sum(1 for x in audit_log if x['matched_level']=='district')}, province={sum(1 for x in audit_log if x['matched_level']=='province')}")
    print(f"[Log] Saved JSON to {LOG_JSON_PATH} and CSV to {LOG_CSV_PATH}")


if __name__ == "__main__":
    main()
