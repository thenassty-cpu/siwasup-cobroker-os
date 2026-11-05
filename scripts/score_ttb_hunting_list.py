"""
TTB Pre-Foreclosure Hunting List — Lead Scoring Script
=======================================================
Input : E:/TON/#Siwasub/document/ttb_pre_foreclosure_hunting_list.csv
Output: E:/TON/#Siwasub/document/ttb_hunting_scored.csv

Scoring weights (100 pts total)
  40 pts — ราคาต่อ ตร.ม. ต่ำ (ยิ่งถูกยิ่งสูง → เจ้าของหลังชนฝาจริง)
  25 pts — ทำเลสภาพคล่อง (กทม.+ปริมณฑล > หัวเมือง > ต่างจังหวัด)
  20 pts — ประเภททรัพย์ที่ขายเร็ว (บ้านเดี่ยว/ทาวน์โฮม > คอนโด > ที่ดิน)
  15 pts — ขนาดพื้นที่ใช้สอย (ไม่เล็กเกินไป ไม่ใหญ่เกินไป — sweet spot 80-250 ตร.ม.)
"""

import csv
import math
import sys
import os

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------
INPUT_CSV  = r"E:\TON\#Siwasub\document\ttb_pre_foreclosure_hunting_list.csv"
OUTPUT_CSV = r"E:\TON\#Siwasub\document\ttb_hunting_scored.csv"

# ---------------------------------------------------------------------------
# helper: parse price string "4,140,000 บาท" → float
# ---------------------------------------------------------------------------
def parse_price(raw: str) -> float:
    cleaned = raw.replace(",", "").replace("บาท", "").replace(" ", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

# ---------------------------------------------------------------------------
# helper: parse area string "32.6 ตร.ว." → float (ตร.ว.)
# ---------------------------------------------------------------------------
def parse_sqw(raw: str) -> float:
    cleaned = raw.replace("ตร.ว.", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

# ---------------------------------------------------------------------------
# helper: parse usable_area "347.5 ตร.ม." → float
# ---------------------------------------------------------------------------
def parse_sqm(raw: str) -> float:
    cleaned = raw.replace("ตร.ม.", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

# ---------------------------------------------------------------------------
# 40 pts — ราคาต่อ ตร.ม.
# ทรัพย์ถูกกว่าได้คะแนนมากกว่า; normalize แบบ inverse percentile
# ---------------------------------------------------------------------------
def score_price_per_sqm(price_per_sqm: float, all_ppsqm: list) -> float:
    if price_per_sqm <= 0:
        return 0.0
    valid = [v for v in all_ppsqm if v > 0]
    if not valid:
        return 0.0
    rank = sum(1 for v in valid if v > price_per_sqm)  # กี่คนที่แพงกว่า
    percentile = rank / len(valid)                       # 1.0 = ถูกสุด
    return round(percentile * 40, 2)

# ---------------------------------------------------------------------------
# 25 pts — ทำเลสภาพคล่อง
# ---------------------------------------------------------------------------
LIQUIDITY_TIERS = {
    # tier 1 — กทม. + ปริมณฑลหลัก (25 pts)
    "tier1": {
        "กรุงเทพมหานคร", "Bangkok",
        "นนทบุรี", "Nonthaburi",
        "ปทุมธานี", "Pathum Thani",
        "สมุทรปราการ", "Samut Prakan",
    },
    # tier 2 — หัวเมืองใหญ่ (18 pts)
    "tier2": {
        "เชียงใหม่", "Chiang Mai",
        "ชลบุรี", "Chon Buri",
        "ระยอง", "Rayong",
        "ภูเก็ต", "Phuket",
        "ขอนแก่น", "Khon Kaen",
        "นครราชสีมา", "Nakhon Ratchasima",
        "สมุทรสาคร", "Samut Sakhon",
    },
}

def score_liquidity(location: str) -> float:
    for prov in LIQUIDITY_TIERS["tier1"]:
        if prov in location:
            return 25.0
    for prov in LIQUIDITY_TIERS["tier2"]:
        if prov in location:
            return 18.0
    return 10.0  # tier 3 — จังหวัดอื่น

def tier_label(location: str) -> str:
    for prov in LIQUIDITY_TIERS["tier1"]:
        if prov in location:
            return "🔴 กทม./ปริมณฑล"
    for prov in LIQUIDITY_TIERS["tier2"]:
        if prov in location:
            return "🟡 หัวเมืองใหญ่"
    return "⚪ จังหวัดอื่น"

# ---------------------------------------------------------------------------
# 20 pts — ประเภททรัพย์
# ---------------------------------------------------------------------------
TYPE_SCORE = {
    "บ้านเดี่ยว":   20.0,
    "ทาวน์โฮม":     18.0,
    "ทาวน์เฮ้าส์":  18.0,
    "คอนโดมิเนียม": 14.0,
    "คอนโด":        14.0,
    "อาคารพาณิชย์": 12.0,
    "ที่ดิน":        8.0,
    "โรงงาน":        8.0,
    "อื่นๆ":          8.0,
}

def score_type(category: str) -> float:
    for key, pts in TYPE_SCORE.items():
        if key in category:
            return pts
    return 8.0

# ---------------------------------------------------------------------------
# 15 pts — ขนาด usable_area sweet spot 80–250 ตร.ม.
# นอก sweet spot ลดแบบ linear ทั้งสองทาง
# ---------------------------------------------------------------------------
def score_usable(sqm: float) -> float:
    if sqm <= 0:
        return 5.0
    if 80 <= sqm <= 250:
        return 15.0
    if sqm < 80:
        # ยิ่งเล็กยิ่งน้อย; 0 ตร.ม. → 0 pts
        return round(max(0, (sqm / 80) * 15), 2)
    # sqm > 250 — ยิ่งใหญ่ยิ่งขายยาก; 500+ → 5 pts
    decay = max(0, 1 - (sqm - 250) / 500)
    return round(max(5, decay * 15), 2)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    if not os.path.exists(INPUT_CSV):
        print(f"[ERROR] ไม่พบไฟล์ input: {INPUT_CSV}")
        sys.exit(1)

    rows = []
    with open(INPUT_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    print(f"[+] โหลดข้อมูล {len(rows)} แปลง")

    # คำนวณ price_per_sqm ก่อน (ต้องใช้ทุก row เพื่อ percentile)
    for row in rows:
        price  = parse_price(row.get("price", ""))
        sqm    = parse_sqm(row.get("usable_area", ""))
        row["_price"]  = price
        row["_sqm"]    = sqm
        row["_sqw"]    = parse_sqw(row.get("size", ""))
        row["_ppsqm"]  = (price / sqm) if sqm > 0 else 0.0

    all_ppsqm = [r["_ppsqm"] for r in rows]

    # คำนวณคะแนน
    for row in rows:
        s_price    = score_price_per_sqm(row["_ppsqm"], all_ppsqm)
        s_liquidity = score_liquidity(row.get("location", ""))
        s_type     = score_type(row.get("category", ""))
        s_usable   = score_usable(row["_sqm"])
        total      = s_price + s_liquidity + s_type + s_usable

        row["score_total"]     = round(total, 1)
        row["score_price"]     = s_price
        row["score_liquidity"] = s_liquidity
        row["score_type"]      = s_type
        row["score_usable"]    = s_usable
        row["tier"]            = tier_label(row.get("location", ""))
        row["price_per_sqm"]   = (
            f"{row['_ppsqm']:,.0f}" if row["_ppsqm"] > 0 else "-"
        )
        row["priority"] = (
            "🔥 ล่าก่อน" if total >= 70
            else "✅ ล่าได้"  if total >= 50
            else "⏸ รอก่อน"
        )

    # เรียงลำดับ score สูงสุดก่อน
    rows.sort(key=lambda r: r["score_total"], reverse=True)

    # กำหนด rank
    for i, row in enumerate(rows, 1):
        row["rank"] = i

    # OUTPUT COLUMNS
    out_fields = [
        "rank",
        "priority",
        "score_total",
        "id",
        "category",
        "location",
        "tier",
        "price",
        "price_per_sqm",
        "size",
        "usable_area",
        "score_price",
        "score_liquidity",
        "score_type",
        "score_usable",
        "title",
        "main_image",
    ]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"[✓] บันทึก {len(rows)} แปลง → {OUTPUT_CSV}")

    # สรุปผล
    fire  = sum(1 for r in rows if r["priority"] == "🔥 ล่าก่อน")
    ok    = sum(1 for r in rows if r["priority"] == "✅ ล่าได้")
    wait  = sum(1 for r in rows if r["priority"] == "⏸ รอก่อน")
    top5  = rows[:5]

    print(f"\n{'='*60}")
    print(f"  🔥 ล่าก่อน  : {fire:>3} แปลง  (score ≥ 70)")
    print(f"  ✅ ล่าได้   : {ok:>3} แปลง  (score 50–69)")
    print(f"  ⏸ รอก่อน  : {wait:>3} แปลง  (score < 50)")
    print(f"{'='*60}")
    print(f"\n  TOP 5 เป้าหมายวันนี้:")
    for r in top5:
        print(
            f"  #{r['rank']:>3}  [{r['score_total']:>5.1f} pts]  "
            f"{r['tier']}  {r['id']}  "
            f"{r['category']}  {r['price']}  "
            f"({r['location'].split('•')[-1].strip()})"
        )
    print()

if __name__ == "__main__":
    main()
