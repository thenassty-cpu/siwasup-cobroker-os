"""Quick unit test for deed OCR additions — runs without network."""
import sys
import os
import base64

# point to project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

os.environ.setdefault("LINE_ACCESS_TOKEN", "test_token")
os.environ.setdefault("GEMINI_API_KEY",    "test_key")

# stub urlopen so no network calls go out during import
import urllib.request as _ur

class _FakeResp:
    status = 200
    def read(self):
        return b'{"conversations":[]}'
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass

_ur.urlopen = lambda *a, **k: _FakeResp()

import line_gemini_webhook as wh

# ------------------------------------------------------------------
# 1. GEO lookup loaded?
# ------------------------------------------------------------------
prov_count = len(wh._GEO_LOOKUP_PROV)
amp_count  = len(wh._GEO_LOOKUP_AMP)
assert prov_count >= 77, f"Expected ≥77 provinces, got {prov_count}"
assert amp_count  >= 500, f"Expected ≥500 amphurs, got {amp_count}"
print(f"[OK] GEO: {prov_count} provinces, {amp_count} amphurs")

# ------------------------------------------------------------------
# 2. deeplink token สูตร Base64(pcode,acode,deed_no)
# ------------------------------------------------------------------
tok = wh._build_deeplink_token("กระบี่", "เมืองกระบี่", "52696")
expected = base64.b64encode(b"81,01,52696").decode()
assert tok == expected, f"Token mismatch: got {tok!r}, expected {expected!r}"
print(f"[OK] deeplink token: {tok}")

# กรุงเทพ เขตพระนคร
tok2 = wh._build_deeplink_token("กรุงเทพมหานคร", "พระนคร", "12345")
pcode2 = wh._GEO_LOOKUP_PROV.get("กรุงเทพมหานคร")
acode2 = wh._GEO_LOOKUP_AMP.get("กรุงเทพมหานคร:พระนคร")
assert tok2 is not None, "Bangkok deeplink failed"
expected2 = base64.b64encode(f"{pcode2},{acode2},12345".encode()).decode()
assert tok2 == expected2, f"BKK token mismatch: {tok2} vs {expected2}"
print(f"[OK] Bangkok deeplink: {tok2}")

# จังหวัดที่ไม่มีในฐาน → คืน None (ไม่ crash)
tok_bad = wh._build_deeplink_token("มาร์ส", "ดาวอังคาร", "99999")
assert tok_bad is None, "Expected None for unknown province"
print("[OK] Unknown province → None (no crash)")

# ------------------------------------------------------------------
# 3. OCR prompt คือ string ไม่ว่าง
# ------------------------------------------------------------------
assert isinstance(wh.DEED_OCR_PROMPT, str) and len(wh.DEED_OCR_PROMPT) > 50
print("[OK] DEED_OCR_PROMPT defined")

# ------------------------------------------------------------------
# 4. build_deed_flex_card — structure ถูกต้อง
# ------------------------------------------------------------------
ocr = {
    "province":       "กระบี่",
    "amphur":         "เมืองกระบี่",
    "deed_no":        "52696",
    "land_area_sqw":  "32.5",
    "parcel_no":      "15",
    "confidence":     "high",
}
dl = f"https://landsmaps.dol.go.th/?qrcodeToken={tok}"
card = wh.build_deed_flex_card(ocr, dl, tok)

assert card["type"] == "flex"
assert card["contents"]["type"] == "bubble"
assert "โฉนดที่ดิน" in card["altText"]
assert "กระบี่" in card["altText"]
assert "52696" in card["altText"]

# header / body / footer present
c = card["contents"]
assert "header" in c and "body" in c and "footer" in c
print(f'[OK] Flex card: altText="{card["altText"]}"')

# ตรวจ footer มีปุ่ม LandsMaps
btns = c["footer"]["contents"]
assert any("LandsMaps" in (b.get("action", {}).get("label", "")) for b in btns), \
    "No LandsMaps button in footer"
print("[OK] Footer has LandsMaps button")

# ------------------------------------------------------------------
# 5. area rai-ngan-wa calculation
# ------------------------------------------------------------------
# 32.5 ตร.ว. = 0 ไร่ 0 งาน 32.5 วา
body_texts = [
    item.get("contents", [{}])[-1].get("text", "")
    for item in c["body"]["contents"]
    if item.get("layout") == "horizontal"
]
area_row = next((t for t in body_texts if "ตร.ว." in t), None)
assert area_row is not None, "No area row in body"
assert "0 ไร่" in area_row, f"Expected rai conversion in: {area_row!r}"
print(f"[OK] Area row: {area_row!r}")

print()
print("=" * 50)
print("  ALL DEED OCR UNIT TESTS PASSED ✅")
print("=" * 50)
