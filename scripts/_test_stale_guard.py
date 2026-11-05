"""
Unit test สำหรับ Stale Guard logic ใน run_pamco_pull
ทดสอบแบบ offline — ไม่ต้องเรียก network จริง
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

os.environ.setdefault("LINE_ACCESS_TOKEN", "test")
os.environ.setdefault("GEMINI_API_KEY", "test")

import urllib.request as _ur

class _FakeResp:
    status = 200
    def read(self):
        return b'{"conversations":[]}'
    def __enter__(self): return self
    def __exit__(self, *a): pass

_ur.urlopen = lambda *a, **k: _FakeResp()

import overnight_r2_crawler as cr

# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------
def _make_rec(code: str, status: str = "available", hidden_since: str = None) -> dict:
    r = {
        "id": f"PAMCO-{code}", "code": code, "source": "PAMCO", "bank_pool": "PAMCO",
        "title": f"ทรัพย์ {code}", "category": "ทาวน์โฮม", "detail_code": "2",
        "price": 2000000, "province": "กรุงเทพมหานคร", "district": "บางนา",
        "sub_district": "บางนา", "latitude": "13.6", "longitude": "100.5",
        "area_sqw": "30", "usable_sqm": "120", "landid": f"ฉ.{code}",
        "houseid": "1/1", "street": "สุขุมวิท", "soi": "101", "hgroup": "X",
        "telAO": "08-0000-0000", "slug": code.lower(),
        "thumbnail": "https://media.pamco.co.th/x.jpg",
        "media_base": "https://media.pamco.co.th",
        "thumbnail_path": "x.jpg", "status": status,
        "last_seen": datetime.now().isoformat(),
    }
    if hidden_since:
        r["hidden_since"] = hidden_since
    return r


def run_stale_guard_on(prev: dict, fresh_codes: list[str]) -> dict:
    """
    จำลอง Stale Guard loop จาก run_pamco_pull โดยไม่ต้อง pull จริง
    fresh_codes = รหัสที่ server ส่งมาในรอบนี้
    """
    all_records = {f"PAMCO-{c}": _make_rec(c) for c in fresh_codes}
    now_iso = datetime.now().isoformat()
    now_dt  = datetime.now()

    stale_new = stale_hidden = stale_restored = 0
    for pid, prev_rec in prev.items():
        if pid in all_records:
            if prev_rec.get("status") in ("missing", "hidden"):
                all_records[pid]["status"] = "available"
                all_records[pid].pop("hidden_since", None)
                stale_restored += 1
            continue

        hidden_since_str = prev_rec.get("hidden_since")
        if hidden_since_str:
            try:
                days_missing = (now_dt - datetime.fromisoformat(hidden_since_str)).days
            except ValueError:
                days_missing = 0
        else:
            hidden_since_str = now_iso
            days_missing = 0

        if days_missing >= cr.PAMCO_STALE_DAYS:
            prev_rec["status"]       = "hidden"
            prev_rec["hidden_since"] = hidden_since_str
            stale_hidden += 1
        else:
            prev_rec["status"]       = "missing"
            prev_rec["hidden_since"] = hidden_since_str
            stale_new += 1

        all_records[pid] = prev_rec

    return all_records, stale_new, stale_hidden, stale_restored


# ------------------------------------------------------------------
# TEST 1: ทรัพย์ที่เจออยู่ → status ไม่เปลี่ยน
# ------------------------------------------------------------------
prev = {"PAMCO-B001": _make_rec("B001", "available")}
result, new, hidden, restored = run_stale_guard_on(prev, ["B001"])
assert result["PAMCO-B001"]["status"] == "available", "Should stay available"
assert new == 0 and hidden == 0 and restored == 0
print("[OK] ทรัพย์ที่เจออยู่ → available ไม่เปลี่ยน")

# ------------------------------------------------------------------
# TEST 2: ทรัพย์ที่หายครั้งแรก → status=missing, hidden_since=now
# ------------------------------------------------------------------
prev = {"PAMCO-B002": _make_rec("B002", "available")}
result, new, hidden, restored = run_stale_guard_on(prev, [])  # ไม่เจอ B002
rec = result["PAMCO-B002"]
assert rec["status"] == "missing", f"Expected missing, got {rec['status']}"
assert "hidden_since" in rec
assert new == 1 and hidden == 0
print("[OK] ทรัพย์หายครั้งแรก → missing + hidden_since ถูก set")

# ------------------------------------------------------------------
# TEST 3: ทรัพย์ที่ missing < 14 วัน → ยังคง missing
# ------------------------------------------------------------------
five_days_ago = (datetime.now() - timedelta(days=5)).isoformat()
prev = {"PAMCO-B003": _make_rec("B003", "missing", hidden_since=five_days_ago)}
result, new, hidden, restored = run_stale_guard_on(prev, [])
rec = result["PAMCO-B003"]
assert rec["status"] == "missing", f"Expected still missing, got {rec['status']}"
assert new == 1 and hidden == 0
print("[OK] missing < 14 วัน → ยังคง missing")

# ------------------------------------------------------------------
# TEST 4: ทรัพย์ที่ missing >= 14 วัน → auto-hidden
# ------------------------------------------------------------------
fifteen_days_ago = (datetime.now() - timedelta(days=15)).isoformat()
prev = {"PAMCO-B004": _make_rec("B004", "missing", hidden_since=fifteen_days_ago)}
result, new, hidden, restored = run_stale_guard_on(prev, [])
rec = result["PAMCO-B004"]
assert rec["status"] == "hidden", f"Expected hidden, got {rec['status']}"
assert new == 0 and hidden == 1
print("[OK] missing >= 14 วัน → auto-hidden ✅")

# ------------------------------------------------------------------
# TEST 5: ทรัพย์ที่เคย missing แต่กลับมา → restored, ไม่มี hidden_since
# ------------------------------------------------------------------
prev = {"PAMCO-B005": _make_rec("B005", "missing", hidden_since=five_days_ago)}
result, new, hidden, restored = run_stale_guard_on(prev, ["B005"])
rec = result["PAMCO-B005"]
assert rec["status"] == "available", f"Expected available, got {rec['status']}"
assert "hidden_since" not in rec
assert restored == 1
print("[OK] ทรัพย์ที่เคย missing กลับมา → restored + hidden_since cleared ✅")

# ------------------------------------------------------------------
# TEST 6: ทรัพย์ที่เคย hidden กลับมา → ก็ restore ได้
# ------------------------------------------------------------------
prev = {"PAMCO-B006": _make_rec("B006", "hidden", hidden_since=fifteen_days_ago)}
result, new, hidden, restored = run_stale_guard_on(prev, ["B006"])
rec = result["PAMCO-B006"]
assert rec["status"] == "available"
assert "hidden_since" not in rec
assert restored == 1
print("[OK] ทรัพย์ที่เคย hidden กลับมา → restored ✅")

# ------------------------------------------------------------------
# TEST 7: Mix scenario (ตรงกับ real-world วันคืนถัดไป)
# ------------------------------------------------------------------
prev = {
    "PAMCO-B010": _make_rec("B010", "available"),             # เจออยู่
    "PAMCO-B011": _make_rec("B011", "available"),             # หายครั้งแรก
    "PAMCO-B012": _make_rec("B012", "missing",
                             hidden_since=(datetime.now()-timedelta(days=5)).isoformat()),  # missing 5d
    "PAMCO-B013": _make_rec("B013", "missing",
                             hidden_since=(datetime.now()-timedelta(days=15)).isoformat()), # missing 15d → hidden
    "PAMCO-B014": _make_rec("B014", "hidden",
                             hidden_since=(datetime.now()-timedelta(days=20)).isoformat()), # hidden กลับมา
}
fresh = ["B010", "B014"]   # B011,B012,B013 หาย; B014 กลับมา
result, new, hidden_c, rest = run_stale_guard_on(prev, fresh)

assert result["PAMCO-B010"]["status"] == "available"
assert result["PAMCO-B011"]["status"] == "missing"
assert result["PAMCO-B012"]["status"] == "missing"
assert result["PAMCO-B013"]["status"] == "hidden"
assert result["PAMCO-B014"]["status"] == "available"
assert new == 2        # B011 (ครั้งแรก) + B012 (ยังอยู่ใน window)
assert hidden_c == 1   # B013
assert rest == 1       # B014
print("[OK] Mix scenario → ผลถูกทุกตัว ✅")

# ------------------------------------------------------------------
# TEST 8: ตรวจสอบ PAMCO_STALE_DAYS config ถูกต้อง
# ------------------------------------------------------------------
assert cr.PAMCO_STALE_DAYS == 14, f"Expected 14, got {cr.PAMCO_STALE_DAYS}"
print("[OK] PAMCO_STALE_DAYS = 14 วัน ✅")

print()
print("=" * 55)
print("  ALL STALE GUARD UNIT TESTS PASSED ✅")
print("=" * 55)
