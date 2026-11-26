import json
import os
import re
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PATH = os.path.join(BASE_DIR, "siwasup_all_properties.json")
CUR_PATH = os.path.join(BASE_DIR, "all_curation_properties.json")
BACKUP_PATH = os.path.join(BASE_DIR, "backups", "siwasup_all_properties_pre_curation_sync.json")


def parse_price_int(val) -> int:
    if isinstance(val, (int, float)):
        return int(val)
    s = str(val or "").replace(",", "")
    m = re.search(r"(\d+)(?:\.\d+)?", s)
    return int(m.group(1)) if m else 0


def main():
    if not os.environ.get("CI"):
        os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
        shutil.copy2(MAIN_PATH, BACKUP_PATH)
        print(f"[Backup] Saved to {BACKUP_PATH}")

    with open(MAIN_PATH, "r", encoding="utf-8") as f:
        main_props = json.load(f)
    with open(CUR_PATH, "r", encoding="utf-8") as f:
        cur_by_id = {str(c.get("id")): c for c in json.load(f)}

    fixed_bad = 0
    fixed_promo = 0
    for p in main_props:
        pid = str(p.get("id"))
        c = cur_by_id.get(pid)
        if not c:
            continue
        p1 = parse_price_int(p.get("price"))
        p2 = parse_price_int(c.get("price"))
        if not p1 or not p2 or p1 == p2:
            continue

        if (p1 < 500_000 and p2 >= 500_000) or (p1 < 500_000 and p2 < 500_000):
            p["price"] = f"{p2:,} บาท"
            p.pop("original_price", None)
            p.pop("special_price", None)
            p.pop("promo_start_date", None)
            p.pop("promo_end_date", None)
            fixed_bad += 1
            print(f"  [Fix Price] {pid}: {p1:,} -> {p2:,}")
        elif p1 > p2 and p2 >= 500_000:
            p["original_price"] = f"{p1:,} บาท"
            p["special_price"] = f"{p2:,} บาท"
            p["price"] = f"{p2:,} บาท"
            p.pop("promo_start_date", None)
            p.pop("promo_end_date", None)
            fixed_promo += 1
            print(f"  [Promo Sync] {pid}: orig={p1:,} -> spec={p2:,}")

    with open(MAIN_PATH, "w", encoding="utf-8") as f:
        json.dump(main_props, f, ensure_ascii=False, indent=2)
    print(f"[Done] Fixed bad/rent prices={fixed_bad}, synced promo prices={fixed_promo}")


if __name__ == "__main__":
    main()
