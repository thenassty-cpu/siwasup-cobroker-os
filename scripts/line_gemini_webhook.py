import http.server
import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import hmac
import hashlib
import base64
import os
import sys
import threading
import time
import re
import difflib
from datetime import datetime, timezone, timedelta

TH_TZ = timezone(timedelta(hours=7))


def bkk_now() -> datetime:
    """Return current datetime in Asia/Bangkok (UTC+7)."""
    return datetime.now(TH_TZ)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.environ.get("BASE_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DATA_DIR = os.path.join(BASE_DIR, "data")
sys.path.append(SCRIPTS_DIR)

try:
    from overnight_r2_crawler import put_object_r2
except Exception as e:
    print(f"[Warn] Could not import put_object_r2: {e}")
    put_object_r2 = None

PORT = int(os.environ.get("PORT", 5005))
HOST = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"

# LINE & Gemini Credentials (Dynamic config & Cloud env var support)
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
_cfg = {}
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as _cf:
            _cfg = json.load(_cf)
    except Exception:
        pass

LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET") or _cfg.get("line_oa", {}).get("channel_secret", "")
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN") or _cfg.get("line_oa", {}).get("channel_access_token", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or _cfg.get("gemini_api", {}).get("api_key", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
ADMIN_EXPORT_SECRET = os.environ.get("ADMIN_EXPORT_SECRET", "SiwasupAdmin2026_SecureKey_99")
_R2_CHAT_VAULT_KEY = "_vault/chat_logs_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_chat_logs_vault_v2", hashlib.sha256).hexdigest()[:32] + ".json"

# ---------------------------------------------------------------------------
# LandsMaps GEO lookup: province code + amphur code  (ใช้สร้าง deeplink token)
# Parse ตรงจากไฟล์ thai_landmap_geo.js ที่มีอยู่แล้วในโปรเจกต์
# ---------------------------------------------------------------------------
_GEO_LOOKUP_PROV: dict[str, str] = {}   # ชื่อจังหวัด → code เช่น "กระบี่" → "81"
_GEO_LOOKUP_AMP:  dict[str, str] = {}   # "จังหวัด:อำเภอ" → code เช่น "กระบี่:เมืองกระบี่" → "01"

def _load_geo_lookup():
    """
    thai_landmap_geo.js structure:
      { "provinces": [{code, name}, ...],
        "districts": { "<prov_code>": [{code, name}, ...], ... } }
    """
    geo_js = os.path.join(BASE_DIR, "thai_landmap_geo.js")
    if not os.path.exists(geo_js):
        return
    try:
        raw = open(geo_js, encoding="utf-8").read()
        raw = re.sub(r'^window\.THAI_LANDMAP_GEO\s*=\s*', '', raw.strip())
        raw = re.sub(r';?\s*$', '', raw)
        geo = json.loads(raw)

        # province code ← ชื่อจังหวัด
        pcode_by_name: dict[str, str] = {}
        for prov in geo.get("provinces", []):
            pname = prov.get("name", "")
            pcode = str(prov.get("code", ""))
            if pname and pcode:
                _GEO_LOOKUP_PROV[pname] = pcode
                pcode_by_name[pname] = pcode

        # amphur code ← "จังหวัด:อำเภอ"
        # districts keyed by province_code (string int like "10", "81")
        districts: dict = geo.get("districts", {})
        for pname, pcode in pcode_by_name.items():
            amp_list = districts.get(pcode) or districts.get(int(pcode), [])
            for amp in amp_list:
                aname = amp.get("name", "")
                acode = amp.get("code", "")
                if aname and acode:
                    _GEO_LOOKUP_AMP[f"{pname}:{aname}"] = acode

        print(f"[GEO] Loaded {len(_GEO_LOOKUP_PROV)} provinces, {len(_GEO_LOOKUP_AMP)} amphurs")
    except Exception as e:
        print(f"[GEO] Load error: {e}")

_load_geo_lookup()

# ---------------------------------------------------------------------------
# Nationwide Thai Geo Centroids (77 Provinces, 924 Districts, 7,436 Subdistricts)
# Used for Greedy Longest-Match parsing ("คานหามอยุธยา") & Haversine Nearest Fallback
# ---------------------------------------------------------------------------
_THAI_GEO = {"provinces": {}, "districts": [], "subdistricts": []}
_THAI_PROV_NAMES: list[str] = []
_THAI_DIST_NAMES: list[str] = []
_THAI_SUB_NAMES: list[str] = []

_THAI_PROV_ALIASES = {
    "กทม": "กรุงเทพมหานคร", "กรุงเทพฯ": "กรุงเทพมหานคร", "กรุงเทพ": "กรุงเทพมหานคร",
    "อยุธยา": "พระนครศรีอยุธยา", "โคราช": "นครราชสีมา", "นครศรี": "นครศรีธรรมราช",
    "สุราษฎร์": "สุราษฎร์ธานี", "อุบล": "อุบลราชธานี", "อุดร": "อุดรธานี",
    "พิษณุโลก": "พิษณุโลก", "แปดริ้ว": "ฉะเชิงเทรา", "เมืองชล": "ชลบุรี",
    "ปากน้ำ": "สมุทรปราการ", "นนท์": "นนทบุรี", "ปทุม": "ปทุมธานี",
    "ประจวบ": "ประจวบคีรีขันธ์", "กาญจน์": "กาญจนบุรี", "เพชรบุรี": "เพชรบุรี",
    "ราชบุรี": "ราชบุรี", "สุพรรณ": "สุพรรณบุรี", "สมุทรสาคร": "สมุทรสาคร",
    "มหาชัย": "สมุทรสาคร", "พัทยา": "ชลบุรี", "หัวหิน": "ประจวบคีรีขันธ์",
    "หาดใหญ่": "สงขลา", "รังสิต": "ปทุมธานี", "ศาลายา": "นครปฐม",
}
_THAI_SPECIAL_ZONE_COORDS = {
    "โรจนะ": ("พระนครศรีอยุธยา", "อุทัย", 14.3266, 100.6596),
    "นวนคร": ("ปทุมธานี", "คลองหลวง", 14.1135, 100.6145),
    "ไฮเทค": ("พระนครศรีอยุธยา", "บางปะอิน", 14.1983, 100.6122),
    "บางกะดี": ("ปทุมธานี", "เมืองปทุมธานี", 13.9806, 100.5539),
    "อมตะนคร": ("ชลบุรี", "เมืองชลบุรี", 13.4281, 101.0267),
    "อมตะซิตี้": ("ระยอง", "ปลวกแดง", 12.9972, 101.1489),
    "อีสเทิร์นซีบอร์ด": ("ระยอง", "ปลวกแดง", 13.0278, 101.1981),
    "แหลมฉบัง": ("ชลบุรี", "ศรีราชา", 13.0819, 100.9169),
    "มาบตาพุด": ("ระยอง", "เมืองระยอง", 12.7161, 101.1486),
    "นิคมบางปู": ("สมุทรปราการ", "เมืองสมุทรปราการ", 13.5411, 100.6428),
    "บางปู": ("สมุทรปราการ", "เมืองสมุทรปราการ", 13.5411, 100.6428),
    "เมกาบางนา": ("สมุทรปราการ", "บางพลี", 13.6464, 100.6803),
    "ฟิวเจอร์": ("ปทุมธานี", "ธัญบุรี", 13.9888, 100.6184),
    "เซียร์รังสิต": ("ปทุมธานี", "ลำลูกกา", 13.9619, 100.6222),
    "ธรรมศาสตร์": ("ปทุมธานี", "คลองหลวง", 14.0734, 100.6015),
    "รังสิต": ("ปทุมธานี", "ธัญบุรี", 13.9888, 100.6184),
    "ศาลายา": ("นครปฐม", "พุทธมณฑล", 13.8022, 100.3219),
    "เวสต์เกต": ("นนทบุรี", "บางใหญ่", 13.8772, 100.4114),
    "เมืองทอง": ("นนทบุรี", "ปากเกร็ด", 13.9122, 100.5486),
    "แจ้งวัฒนะ": ("นนทบุรี", "ปากเกร็ด", 13.9039, 100.5300),
    "เลียบด่วน": ("กรุงเทพมหานคร", "ลาดพร้าว", 13.8167, 100.6194),
    "เกษตรนวมินทร์": ("กรุงเทพมหานคร", "ลาดพร้าว", 13.8344, 100.6144),
    "พระราม 2": ("กรุงเทพมหานคร", "บางขุนเทียน", 13.6625, 100.4342),
    "ประชาอุทิศ": ("กรุงเทพมหานคร", "ทุ่งครุ", 13.6433, 100.4964),
    "ทุ่งครุ": ("กรุงเทพมหานคร", "ทุ่งครุ", 13.6472, 100.4958),
    "พุทธบูชา": ("กรุงเทพมหานคร", "ทุ่งครุ", 13.6531, 100.4836),
    "ราษฎร์บูรณะ": ("กรุงเทพมหานคร", "ราษฎร์บูรณะ", 13.6822, 100.5056),
    "สุขสวัสดิ์": ("กรุงเทพมหานคร", "ราษฎร์บูรณะ", 13.6714, 100.5117),
    "พระประแดง": ("สมุทรปราการ", "พระประแดง", 13.6586, 100.5336),
    "พระราม 9": ("กรุงเทพมหานคร", "ห้วยขวาง", 13.7536, 100.5819),
    "ทองหล่อ": ("กรุงเทพมหานคร", "วัฒนา", 13.7308, 100.5825),
    "เอกมัย": ("กรุงเทพมหานคร", "วัฒนา", 13.7269, 100.5858),
    "อารีย์": ("กรุงเทพมหานคร", "พญาไท", 13.7797, 100.5447),
    "อ่อนนุช": ("กรุงเทพมหานคร", "สวนหลวง", 13.7086, 100.6056),
    "แบริ่ง": ("สมุทรปราการ", "เมืองสมุทรปราการ", 13.6611, 100.6019),
    "ศิริราช": ("กรุงเทพมหานคร", "บางกอกน้อย", 13.7592, 100.4856),
    "ปิ่นเกล้า": ("กรุงเทพมหานคร", "บางพลัด", 13.7764, 100.4783),
    "พัทยา": ("ชลบุรี", "บางละมุง", 12.9236, 100.8825),
    "หัวหิน": ("ประจวบคีรีขันธ์", "หัวหิน", 12.5684, 99.9577),
    "หาดใหญ่": ("สงขลา", "หาดใหญ่", 7.0086, 100.4747),
    "มหาชัย": ("สมุทรสาคร", "เมืองสมุทรสาคร", 13.5475, 100.2747),
}

def _load_thai_geo_centroids():
    global _THAI_GEO, _THAI_PROV_NAMES, _THAI_DIST_NAMES, _THAI_SUB_NAMES
    geo_path = os.path.join(BASE_DIR, "data", "thai_geo_centroids.json")
    if not os.path.exists(geo_path):
        print("[GEO-CENTROIDS] File not found:", geo_path)
        return
    try:
        with open(geo_path, "r", encoding="utf-8") as f:
            _THAI_GEO = json.load(f)
        _THAI_PROV_NAMES = sorted(
            set(list(_THAI_GEO.get("provinces", {}).keys()) + list(_THAI_PROV_ALIASES.keys())),
            key=len, reverse=True
        )
        _THAI_DIST_NAMES = sorted({d["d"] for d in _THAI_GEO.get("districts", []) if len(d.get("d", "")) >= 2}, key=len, reverse=True)
        _THAI_SUB_NAMES = sorted({s["t"] for s in _THAI_GEO.get("subdistricts", []) if len(s.get("t", "")) >= 3}, key=len, reverse=True)
        print(f"[GEO-CENTROIDS] Loaded {len(_THAI_GEO.get('provinces', {}))} provs, {len(_THAI_GEO.get('districts', []))} dists, {len(_THAI_GEO.get('subdistricts', []))} subs")
    except Exception as e:
        print(f"[GEO-CENTROIDS] Load error: {e}")

_load_thai_geo_centroids()


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    import math
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


_SHORT_AMBIGUOUS_PROVS = {"เลย", "ตาก", "ตราด", "น่าน", "ตรัง", "แพร่", "นนท์"}

def _extract_thai_geo(text: str) -> dict | None:
    """
    Extract Thai province / district / subdistrict (even concatenated like 'คานหามอยุธยา')
    using Greedy Longest-Match against 77 provinces, 924 districts, 7,436 subdistricts.
    """
    if not text or not _THAI_GEO.get("subdistricts"):
        return None
    raw_text = str(text)
    has_geo_prefix = bool(re.search(r'(?:จังหวัด|จ\.|อำเภอ|อ\.|เขต|ตำบล|ต\.|แขวง|โซน|แถว|ย่าน)', raw_text))
    clean = re.sub(r'(?:ตำบล|ต\.|แขวง|อำเภอ|อ\.|เขต|จังหวัด|จ\.)', ' ', raw_text)
    clean = re.sub(r'\s+', ' ', clean).strip()

    # Check special famous zones first
    for zk, (zp, zd, zlat, zlng) in _THAI_SPECIAL_ZONE_COORDS.items():
        if zk in clean:
            return {"province": zp, "district": zd, "subdistrict": "", "lat": zlat, "lng": zlng, "ambiguous": []}

    matched_prov = ""
    rem = clean
    for pn in _THAI_PROV_NAMES:
        if pn in rem:
            if pn in _SHORT_AMBIGUOUS_PROVS:
                # Guard against common Thai words like "ขอลิงก์บ้านเลย" or "จัดมาเลย"
                if pn == "เลย" and not has_geo_prefix and not re.search(r'(?:^|\s)เลย(?:\s|$)', clean):
                    continue
                if pn != "เลย" and not has_geo_prefix and not re.search(rf'(?:^|\s){re.escape(pn)}(?:\s|$)', clean):
                    continue
            matched_prov = _THAI_PROV_ALIASES.get(pn, pn)
            rem = rem.replace(pn, " ", 1).strip()
            break

    matched_dist = ""
    dist_pool = [d for d in _THAI_GEO.get("districts", []) if not matched_prov or d["p"] == matched_prov]
    dist_names = sorted({d["d"] for d in dist_pool if len(d.get("d", "")) >= 2}, key=len, reverse=True)
    for dn in dist_names:
        if dn in rem:
            matched_dist = dn
            rem = rem.replace(dn, " ", 1).strip()
            if not matched_prov:
                cand_p = [d["p"] for d in dist_pool if d["d"] == dn]
                if len(set(cand_p)) == 1:
                    matched_prov = cand_p[0]
            break

    matched_sub = ""
    ambiguous = []
    sub_pool = [
        s for s in _THAI_GEO.get("subdistricts", [])
        if (not matched_prov or s["p"] == matched_prov) and (not matched_dist or s["d"] == matched_dist)
    ]
    sub_names = sorted({s["t"] for s in sub_pool if len(s.get("t", "")) >= 3}, key=len, reverse=True)
    for sn in sub_names:
        if sn in rem:
            hits = [s for s in sub_pool if s["t"] == sn]
            matched_sub = sn
            if len(hits) == 1:
                matched_prov = hits[0]["p"]
                matched_dist = hits[0]["d"]
                return {"province": matched_prov, "district": matched_dist, "subdistrict": matched_sub, "lat": hits[0]["lat"], "lng": hits[0]["lng"], "ambiguous": []}
            else:
                ambiguous = hits
                if not matched_prov:
                    return {"province": "", "district": "", "subdistrict": matched_sub, "lat": hits[0]["lat"], "lng": hits[0]["lng"], "ambiguous": hits}
                return {"province": matched_prov, "district": hits[0]["d"], "subdistrict": matched_sub, "lat": hits[0]["lat"], "lng": hits[0]["lng"], "ambiguous": hits}

    if matched_dist and matched_prov:
        d_hit = next((d for d in _THAI_GEO.get("districts", []) if d["p"] == matched_prov and d["d"] == matched_dist), None)
        if d_hit:
            return {"province": matched_prov, "district": matched_dist, "subdistrict": "", "lat": d_hit["lat"], "lng": d_hit["lng"], "ambiguous": []}
    if matched_prov:
        p_hit = _THAI_GEO.get("provinces", {}).get(matched_prov)
        if p_hit:
            return {"province": matched_prov, "district": "", "subdistrict": "", "lat": p_hit["lat"], "lng": p_hit["lng"], "ambiguous": []}
    return None


def _detect_conflicting_zones(text: str, threshold_km: float = 20.0) -> list[str]:
    """Detect 2+ distinct zones/districts/provinces in one query that are > threshold_km apart."""
    if not text or not _THAI_GEO.get("districts"):
        return []
    raw_text = str(text)
    has_geo_prefix = bool(re.search(r'(?:จังหวัด|จ\.|อำเภอ|อ\.|เขต|ตำบล|ต\.|แขวง|โซน|แถว|ย่าน)', raw_text))
    clean = re.sub(r'(?:ตำบล|ต\.|แขวง|อำเภอ|อ\.|เขต|จังหวัด|จ\.)', ' ', raw_text)
    clean = re.sub(r'\s+', ' ', clean).strip()

    hits = []  # list of (label, lat, lng)
    rem = clean

    for zk, (zp, zd, zlat, zlng) in sorted(_THAI_SPECIAL_ZONE_COORDS.items(), key=lambda x: len(x[0]), reverse=True):
        if zk in rem:
            hits.append((zk, zlat, zlng))
            rem = rem.replace(zk, " ", 1)

    for pn in _THAI_PROV_NAMES:
        if pn in rem:
            if pn in _SHORT_AMBIGUOUS_PROVS and not has_geo_prefix and not re.search(rf'(?:^|\s){re.escape(pn)}(?:\s|$)', clean):
                continue
            canon_p = _THAI_PROV_ALIASES.get(pn, pn)
            p_hit = _THAI_GEO.get("provinces", {}).get(canon_p)
            if p_hit:
                hits.append((canon_p, p_hit["lat"], p_hit["lng"]))
                rem = rem.replace(pn, " ", 1)

    # Check unique/major districts (len >= 3) in remaining text
    dist_by_name = {}
    for d in _THAI_GEO.get("districts", []):
        dn = d.get("d", "")
        if len(dn) >= 3 and not dn.startswith("เมือง"):
            dist_by_name.setdefault(dn, []).append(d)
    for dn in sorted(dist_by_name.keys(), key=len, reverse=True):
        if dn in rem and len(dist_by_name[dn]) == 1:
            d0 = dist_by_name[dn][0]
            hits.append((dn, d0["lat"], d0["lng"]))
            rem = rem.replace(dn, " ", 1)

    if len(hits) < 2:
        return []

    # Check if any pair is > threshold_km apart
    for i in range(len(hits)):
        for j in range(i + 1, len(hits)):
            if _haversine_km(hits[i][1], hits[i][2], hits[j][1], hits[j][2]) > threshold_km:
                seen = []
                for lbl, _, _ in hits:
                    if lbl not in seen:
                        seen.append(lbl)
                return seen[:3]
    return []


def _parse_prop_lat_lng(sp: dict):
    for lk, gk in (("latitude", "longitude"), ("lat", "lng")):
        try:
            la = float(sp.get(lk) or 0)
            ln = float(sp.get(gk) or 0)
            if la != 0.0 and ln != 0.0:
                return (la, ln)
        except (TypeError, ValueError):
            continue
    return None


def _parse_prop_price_int(raw_price) -> int:
    """Parse property price string/number to integer baht, ignoring decimals (e.g. '10,500,000.00 บาท' -> 10500000)."""
    if isinstance(raw_price, (int, float)):
        return int(raw_price)
    s = str(raw_price or "").replace(",", "")
    m_unit = re.search(r'(\d+(?:\.\d+)?)\s*(ล้าน|แสน)', s)
    if m_unit:
        mult = 1_000_000 if m_unit.group(2) == "ล้าน" else 100_000
        return int(float(m_unit.group(1)) * mult)
    m = re.search(r'(\d+)(?:\.\d+)?', s)
    return int(m.group(1)) if m else 0


def _format_prop_price_text(raw_price) -> str:
    """Format property price for display/Gemini/Flex, returning 'กรุณาสอบถาม' when price <= 0."""
    pr = _parse_prop_price_int(raw_price)
    return f"{pr:,} บาท" if pr > 0 else "กรุณาสอบถาม"


def _find_nearest_siwasup_props(target_lat: float, target_lng: float, allowed_cats: list = None, max_p: int = None, limit: int = 5) -> list[dict]:
    """Cross-Province Haversine Radius Search: Tier 1 (0-5 km), Tier 2 (5-15 km), or nearest >15 km."""
    scored = []
    for sp in SIWASUP_PROPS:
        if sp.get("status") in ("sold_archive", "transferred") or sp.get("is_image_soldout"):
            continue
        sp_cat = sp.get("category") or ""
        if allowed_cats and not any(ac in sp_cat for ac in allowed_cats):
            continue
        pr = _parse_prop_price_int(sp.get("price"))
        if max_p and (pr <= 0 or pr > max_p):
            continue
        coords = _parse_prop_lat_lng(sp)
        if not coords:
            continue
        dist_km = _haversine_km(target_lat, target_lng, coords[0], coords[1])
        scored.append((dist_km, sp, pr))
    scored.sort(key=lambda x: x[0])
    out = []
    for dist_km, sp, pr in scored[:limit]:
        loc_parts = [x.strip() for x in (sp.get("location") or "").split("•") if x.strip()]
        dist_name = sp.get("district_th") or (loc_parts[0] if loc_parts else "")
        prov_name = sp.get("province_th") or (loc_parts[-1] if loc_parts else "")
        tier = 1 if dist_km <= 5.0 else (2 if dist_km <= 15.0 else 3)
        out.append({
            "code": str(sp.get("id")),
            "bank": sp.get("bank_source") or "Siwasup",
            "type": sp.get("category") or "บ้านเดี่ยว",
            "district": dist_name,
            "subdistrict": sp.get("subdistrict_th") or "",
            "province": prov_name,
            "price": _format_prop_price_text(pr),
            "land_sqw": (sp.get("size") or "-").replace(" ตร.ว.", ""),
            "living_sqm": (sp.get("usable_area") or "-").replace(" ตร.ม.", ""),
            "distance_km": round(dist_km, 1),
            "tier": tier,
            "status": "พร้อมเปิดให้เข้าชม"
        })
    return out

# Session & Multi-Turn Memory Tracking
USER_LAST_SEEN = {}
USER_PROFILE_CACHE = {}
USER_CHAT_HISTORY = {}  # user_id -> list of {"user": ..., "bot": ...}
USER_SEARCH_CONTEXT = {}  # user_id -> {"types": [], "locs": [], "max_p": None, "unlimited": False, "updated_at": 0}
SESSION_TIMEOUT = 15 * 60
_MSG_DEBOUNCE_LOCK = threading.Lock()
_MSG_DEBOUNCE_BUF = {}  # uid -> {"texts": [...], "token": ..., "continuous": bool, "timer": Timer}

CHAT_LOG_PATH = os.path.join(DATA_DIR, "line_chat_logs.json")
LOG_LOCK = threading.Lock()

# 1. Load Both Siwasup Curated Portfolio (801 items) AND NPA Catalog (15,117 items)
SIWASUP_PROPS = []
for fname in ["all_curation_properties.json", "siwasup_all_properties.json"]:
    fpath = os.path.join(BASE_DIR, fname)
    if os.path.exists(fpath):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                items = json.load(f)
                existing_ids = {str(x.get("id")) for x in SIWASUP_PROPS}
                for it in items:
                    if str(it.get("id")) not in existing_ids:
                        SIWASUP_PROPS.append(it)
                        existing_ids.add(str(it.get("id")))
        except Exception as e:
            print(f"[-] Error loading {fname}: {e}")

CATALOG_PATH = os.path.join(DATA_DIR, "catalog_index.json")
CATALOG = []
if os.path.exists(CATALOG_PATH):
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            CATALOG = json.load(f)
        print(f"[*] Loaded {len(SIWASUP_PROPS)} Siwasup listings + {len(CATALOG)} NPA properties into search memory.")
    except Exception as e:
        print(f"[-] Error loading catalog: {e}")

LOC_MAP = {
    # โซนตะวันออก & มีนบุรี & กรุงเทพฯ ตะวันออก (เน้นย้ำความแม่นยำ 100%)
    "มีนบุรี": ["Min Buri", "มีนบุรี", "Khlong Sam Wa", "คลองสามวา"],
    "คลองสามวา": ["Khlong Sam Wa", "คลองสามวา", "Min Buri", "มีนบุรี"],
    "หนองจอก": ["Nong Chok", "หนองจอก", "Min Buri", "มีนบุรี"],
    "คันนายาว": ["Khan Na Yao", "Khanna Yao", "คันนายาว", "รามอินทรา"],
    "รามอินทรา": ["Khan Na Yao", "Min Buri", "Bang Khen", "Khlong Sam Wa", "รามอินทรา", "บางชัน"],
    "บางชัน": ["Khlong Sam Wa", "Khan Na Yao", "บางชัน", "รามอินทรา"],
    "ลาดกระบัง": ["Lat Krabang", "ลาดกระบัง", "สุวรรณภูมิ"],
    "สะพานสูง": ["Saphan Sung", "สะพานสูง"],
    "บึงกุ่ม": ["Bung Kum", "บึงกุ่ม", "นวมินทร์"],
    "นวมินทร์": ["Bung Kum", "Lat Phrao", "นวมินทร์"],
    "บางกะปิ": ["Bang Kapi", "บางกะปิ", "เสรีไทย"],
    "เสรีไทย": ["Bang Kapi", "Bung Kum", "เสรีไทย"],
    "ประเวศ": ["Prawet", "ประเวศ", "ศรีนครินทร์", "สวนหลวง"],
    "สวนหลวง": ["Suan Luang", "สวนหลวง", "พัฒนาการ"],
    "พัฒนาการ": ["Suan Luang", "Prawet", "พัฒนาการ"],
    "บางนา": ["Bang Na", "Bang Phli", "Prawet", "บางนา"],
    "อุดมสุข": ["Bang Na", "Phra Khanong", "อุดมสุข"],
    "พระโขนง": ["Phra Khanong", "พระโขนง", "อ่อนนุช"],
    "อ่อนนุช": ["Phra Khanong", "Suan Luang", "Prawet", "อ่อนนุช"],

    # โซนเหนือ & ดอนเมือง & หลักสี่ & พหลโยธิน
    "ดอนเมือง": ["Don Mueang", "ดอนเมือง"],
    "หลักสี่": ["Lak Si", "หลักสี่", "แจ้งวัฒนะ"],
    "สายไหม": ["Sai Mai", "สายไหม", "สุขาภิบาล 5", "วัชรพล"],
    "วัชรพล": ["Sai Mai", "Bang Khen", "วัชรพล"],
    "บางเขน": ["Bang Khen", "บางเขน", "รามอินทรา", "หลักสี่"],
    "จตุจักร": ["Chatuchak", "จตุจักร", "พหลโยธิน", "รัชโยธิน"],
    "รัชโยธิน": ["Chatuchak", "จตุจักร", "รัชโยธิน", "พหลโยธิน", "รัชวิภา"],
    "พหลโยธิน": ["Chatuchak", "จตุจักร", "พหลโยธิน", "รัชโยธิน"],
    "รัชดา": ["Din Daeng", "Huai Khwang", "Chatuchak", "รัชดา", "รัชดาภิเษก"],
    "รัชดาภิเษก": ["Din Daeng", "Huai Khwang", "Chatuchak", "รัชดา", "รัชดาภิเษก"],
    "ลาดพร้าว": ["Lat Phrao", "ลาดพร้าว", "โชคชัย 4"],
    "วังทองหลาง": ["Wang Thong Lang", "วังทองหลาง", "ทาวน์อินทาวน์"],
    "ห้วยขวาง": ["Huai Khwang", "ห้วยขวาง", "รัชดา", "พระราม 9"],
    "ดินแดง": ["Din Daeng", "ดินแดง"],
    "พญาไท": ["Phaya Thai", "พญาไท", "อารีย์", "สะพานควาย"],
    "อารีย์": ["Phaya Thai", "อารีย์"],
    "ราชเทวี": ["Rat Thewi", "ราชเทวี", "ประตูน้ำ"],
    "ปทุมวัน": ["Pathum Wan", "ปทุมวัน", "สยาม"],
    "บางซื่อ": ["Bang Su", "บางซื่อ", "เตาปูน", "วงศ์สว่าง"],
    "เตาปูน": ["Bang Su", "เตาปูน"],
    "ดุสิต": ["Dusit", "ดุสิต", "ศรีย่าน", "สามเสน"],
    "พระนคร": ["Phra Nakhon", "พระนคร", "เกาะรัตนโกสินทร์"],
    "สัมพันธวงศ์": ["Samphanthawong", "สัมพันธวงศ์", "เยาวราช"],
    "ป้อมปราบ": ["Pom Prap", "ป้อมปราบศัตรูพ่าย"],

    # โซนสุขุมวิท & เมืองชั้นใน & พระราม 3-4
    "วัฒนา": ["Watthana", "วัฒนา", "สุขุมวิท", "ทองหล่อ", "เอกมัย", "พร้อมพงษ์"],
    "ทองหล่อ": ["Watthana", "ทองหล่อ", "สุขุมวิท 55"],
    "เอกมัย": ["Watthana", "เอกมัย", "สุขุมวิท 63"],
    "คลองเตย": ["Khlong Toei", "คลองเตย", "พระราม 4"],
    "สาทร": ["Sa Thon", "สาทร", "Sathon", "สีลม"],
    "สีลม": ["Bang Rak", "สีลม", "Bangrak"],
    "บางรัก": ["Bang Rak", "บางรัก", "สีลม"],
    "ยานนาวา": ["Yannawa", "ยานนาวา", "พระราม 3", "ช่องนนทรี"],
    "พระราม 3": ["Yannawa", "Bang Kho Laem", "พระราม 3"],
    "บางคอแหลม": ["Bang Kho Laem", "บางคอแหลม", "เจริญกรุง"],
    "เจริญกรุง": ["Bang Kho Laem", "Bang Rak", "Khlong San", "เจริญกรุง"],

    # ฝั่งธนบุรี & ศิริราช & โซนตะวันตก (เดินทางเชื่อมต่อศิริราชได้สะดวกรวดเร็ว)
    "ศิริราช": ["Bangkok Noi", "Bang Phlat", "Taling Chan", "Thon Buri", "บางกอกน้อย", "บางพลัด", "ตลิ่งชัน", "ธนบุรี"],
    "พรานนก": ["Bangkok Noi", "Bang Phlat", "Taling Chan", "บางกอกน้อย", "บางพลัด", "ตลิ่งชัน"],
    "บางกอกน้อย": ["Bangkok Noi", "Bang Phlat", "Taling Chan", "บางกอกน้อย", "บางพลัด", "ตลิ่งชัน"],
    "บางกอกใหญ่": ["Bangkok Yai", "Thon Buri", "บางกอกใหญ่", "ธนบุรี"],
    "บางขุนนนท์": ["Bangkok Noi", "Taling Chan", "Bang Phlat", "บางกอกน้อย", "ตลิ่งชัน", "บางพลัด"],
    "ไฟฉาย": ["Bangkok Noi", "Taling Chan", "บางกอกน้อย", "ตลิ่งชัน"],
    "จรัญ": ["Bang Phlat", "Bangkok Noi", "บางพลัด", "บางกอกน้อย"],
    "จรัญสนิทวงศ์": ["Bang Phlat", "Bangkok Noi", "บางพลัด", "บางกอกน้อย"],
    "บางพลัด": ["Bang Phlat", "บางพลัด", "บางกอกน้อย"],
    "ปิ่นเกล้า": ["Bangkok Noi", "Bang Phlat", "Taling Chan", "บางกอกน้อย", "บางพลัด", "ตลิ่งชัน"],
    "บรมราชชนนี": ["Taling Chan", "Thawi Watthana", "Bang Phlat", "ตลิ่งชัน", "ทวีวัฒนา", "บางพลัด"],
    "พุทธมณฑล": ["Taling Chan", "Thawi Watthana", "ตลิ่งชัน", "ทวีวัฒนา"],
    "พุทธมณฑลสาย 1": ["Taling Chan", "Phasi Charoen", "ตลิ่งชัน", "ภาษีเจริญ"],
    "พุทธมณฑลสาย 2": ["Thawi Watthana", "Bang Khae", "ทวีวัฒนา", "บางแค"],
    "พุทธมณฑลสาย 3": ["Thawi Watthana", "Nong Khaem", "ทวีวัฒนา", "หนองแขม"],
    "พุทธมณฑลสาย 4": ["Nong Khaem", "Sam Phran", "กระทุ่มแบน"],
    "ราชพฤกษ์": ["ราชพฤกษ์", "Ratchaphruek", "Mueang Nonthaburi", "Bang Kruai", "Pak Kret", "Taling Chan", "เมืองนนทบุรี", "บางกรวย", "ปากเกร็ด", "ตลิ่งชัน"],
    "ราชพฤษ": ["ราชพฤกษ์", "Ratchaphruek", "Mueang Nonthaburi", "Bang Kruai", "Pak Kret", "Taling Chan", "เมืองนนทบุรี", "บางกรวย", "ปากเกร็ด", "ตลิ่งชัน"],
    "ราชพฤษ์": ["ราชพฤกษ์", "Ratchaphruek", "Mueang Nonthaburi", "Bang Kruai", "Pak Kret", "Taling Chan", "เมืองนนทบุรี", "บางกรวย", "ปากเกร็ด", "ตลิ่งชัน"],
    "ราชพฤก": ["ราชพฤกษ์", "Ratchaphruek", "Mueang Nonthaburi", "Bang Kruai", "Pak Kret", "Taling Chan", "เมืองนนทบุรี", "บางกรวย", "ปากเกร็ด", "ตลิ่งชัน"],
    "รัตนาธิเบศร์": ["รัตนาธิเบศร์", "Rattanathibet", "Mueang Nonthaburi", "Bang Yai", "Bang Bua Thong", "เมืองนนทบุรี", "บางใหญ่", "บางบัวทอง"],
    "รัตนาธิเบศ": ["รัตนาธิเบศร์", "Rattanathibet", "Mueang Nonthaburi", "Bang Yai", "Bang Bua Thong", "เมืองนนทบุรี", "บางใหญ่", "บางบัวทอง"],
    "รัตนาทิเบศ": ["รัตนาธิเบศร์", "Rattanathibet", "Mueang Nonthaburi", "Bang Yai", "Bang Bua Thong", "เมืองนนทบุรี", "บางใหญ่", "บางบัวทอง"],
    "รัตนาทิเบส": ["รัตนาธิเบศร์", "Rattanathibet", "Mueang Nonthaburi", "Bang Yai", "Bang Bua Thong", "เมืองนนทบุรี", "บางใหญ่", "บางบัวทอง"],
    "ชัยพฤกษ์": ["ชัยพฤกษ์", "Pak Kret", "Bang Bua Thong", "ปากเกร็ด", "บางบัวทอง"],
    "แจ้งวัฒนะ": ["แจ้งวัฒนะ", "Chaeng Watthana", "Pak Kret", "Lak Si", "ปากเกร็ด", "หลักสี่"],
    "งามวงศ์วาน": ["งามวงศ์วาน", "Ngam Wong Wan", "Mueang Nonthaburi", "Lak Si", "เมืองนนทบุรี", "หลักสี่"],
    "ติวานนท์": ["ติวานนท์", "Tiwanon", "Mueang Nonthaburi", "Pak Kret", "เมืองนนทบุรี", "ปากเกร็ด"],
    "กาญจนาภิเษก": ["กาญจนาภิเษก", "Bang Yai", "Bang Bua Thong", "Bang Kruai", "Taling Chan", "Bang Khae", "บางใหญ่", "บางบัวทอง", "บางกรวย", "ตลิ่งชัน"],
    "กัลปพฤกษ์": ["กัลปพฤกษ์", "Phasi Charoen", "Bang Khae", "Bang Bon", "Chom Thong", "ภาษีเจริญ", "บางแค", "บางบอน", "จอมทอง"],
    "ศรีนครินทร์": ["ศรีนครินทร์", "Srinakarin", "Prawet", "Suan Luang", "Mueang Samut Prakan", "Bang Phli", "ประเวศ", "สวนหลวง"],
    "ศรีนคริน": ["ศรีนครินทร์", "Srinakarin", "Prawet", "Suan Luang", "Mueang Samut Prakan", "ประเวศ", "สวนหลวง"],
    "เทพารักษ์": ["เทพารักษ์", "Theparak", "Mueang Samut Prakan", "Bang Phli", "บางพลี"],
    "เพชรเกษม": ["เพชรเกษม", "Phasi Charoen", "Bang Khae", "Nong Khaem", "ภาษีเจริญ", "บางแค", "หนองแขม"],
    "สุขสวัสดิ์": ["สุขสวัสดิ์", "Rat Burana", "Phra Pradaeng", "Thung Khu", "ราษฎร์บูรณะ", "พระประแดง", "ทุ่งครุ"],
    "สุขุมวิท": ["สุขุมวิท", "Sukhumvit", "Watthana", "Khlong Toei", "Phra Khanong", "Bang Na", "วัฒนา", "คลองเตย", "พระโขนง", "บางนา"],
    "พระราม 9": ["พระราม 9", "Rama 9", "Huai Khwang", "Suan Luang", "ห้วยขวาง", "สวนหลวง"],
    "ไทรน้อย": ["ไทรน้อย", "Sai Noi"],
    "ศาลายา": ["ศาลายา", "Phutthamonthon", "Salaya", "พุทธมณฑล"],
    "หทัยราษฎร์": ["หทัยราษฎร์", "Khlong Sam Wa", "Min Buri", "คลองสามวา", "มีนบุรี"],
    "นิมิตใหม่": ["นิมิตใหม่", "Khlong Sam Wa", "Min Buri", "คลองสามวา", "มีนบุรี"],
    "คู้บอน": ["คู้บอน", "Khan Na Yao", "Khlong Sam Wa", "คันนายาว", "คลองสามวา"],
    "แสมดำ": ["แสมดำ", "Bang Khun Thian", "บางขุนเทียน", "พระราม 2"],
    "ธนบุรี": ["Thon Buri", "Bangkok Yai", "Khlong San", "ธนบุรี", "คลองสาน"],
    "คลองสาน": ["Khlong San", "Thon Buri", "คลองสาน", "ธนบุรี"],
    "ภาษีเจริญ": ["Phasi Charoen", "ภาษีเจริญ", "บางแค"],
    "บางแค": ["Bang Khae", "Phasi Charoen", "บางแค", "ภาษีเจริญ"],
    "บางบอน": ["Bang Bon", "บางบอน", "บางขุนเทียน"],
    "หนองแขม": ["Nong Khaem", "Bang Khae", "หนองแขม", "บางแค"],
    "ตลิ่งชัน": ["Taling Chan", "ตลิ่งชัน"],
    "ทวีวัฒนา": ["Thawi Watthana", "ทวีวัฒนา"],
    "พระราม 2": ["Bang Khun Thian", "Chom Thong", "พระราม 2", "ท่าข้าม", "บางขุนเทียน"],
    "ท่าข้าม": ["Bang Khun Thian", "ท่าข้าม", "พระราม 2"],
    "บางขุนเทียน": ["Bang Khun Thian", "บางขุนเทียน", "พระราม 2", "ท่าข้าม"],
    "จอมทอง": ["Chom Thong", "จอมทอง", "ดาวคะนอง"],
    "ราษฎร์บูรณะ": ["Rat Burana", "ราษฎร์บูรณะ", "สุขสวัสดิ์"],
    "ทุ่งครุ": ["Thung Khu", "ทุ่งครุ", "ประชาอุทิศ"],
    "ประชาอุทิศ": ["Thung Khu", "Rat Burana", "ประชาอุทิศ"],

    # โซนปริมณฑล & นนทบุรี & ปทุมธานี & สมุทรปราการ
    "นนทบุรี": ["Nonthaburi", "Mueang Nonthaburi", "Bang Kruai", "Bang Yai", "Pak Kret", "นนทบุรี"],
    "บางใหญ่": ["Bang Yai", "Nonthaburi", "บางใหญ่"],
    "บางกรวย": ["Bang Kruai", "Nonthaburi", "บางกรวย"],
    "บางบัวทอง": ["Bang Bua Thong", "Nonthaburi", "บางบัวทอง"],
    "ปากเกร็ด": ["Pak Kret", "Nonthaburi", "ปากเกร็ด"],
    "เมืองทอง": ["Pak Kret", "Nonthaburi", "ปากเกร็ด", "เมืองทอง"],
    "สมุทรปราการ": ["Samut Prakan", "Mueang Samut Prakan", "สมุทรปราการ"],
    "บางพลี": ["Bang Phli", "Samut Prakan", "บางพลี"],
    "บางบ่อ": ["Bang Bo", "Samut Prakan", "บางบ่อ"],
    "บางเสาธง": ["Bang Sao Thong", "Samut Prakan", "บางเสาธง"],
    "ปทุมธานี": ["Pathum Thani", "Khlong Luang", "Thanyaburi", "Lam Luk Ka", "ปทุมธานี"],
    "ลำลูกกา": ["ลำลูกกา", "Lam Luk Ka"],
    "ธัญบุรี": ["ธัญบุรี", "Thanyaburi"],
    "รังสิต": ["รังสิต", "Rangsit", "Thanyaburi", "Khlong Luang"],
    "คลองหลวง": ["คลองหลวง", "Khlong Luang"],
    "สมุทรสาคร": ["Samut Sakhon", "Mueang Samut Sakhon", "Krathum Baen", "สมุทรสาคร"],
    "มหาชัย": ["Mueang Samut Sakhon", "Samut Sakhon", "มหาชัย", "สมุทรสาคร"],
    "กระทุ่มแบน": ["Krathum Baen", "Samut Sakhon", "กระทุ่มแบน"],
    "นครปฐม": ["Nakhon Pathom", "Mueang Nakhon Pathom", "Sam Phran", "Phutthamonthon", "นครปฐม"],
    "เชียงใหม่": ["Chiang Mai", "Mueang Chiang Mai", "เชียงใหม่"],
    "พัทยา": ["Bang Lamung", "Chon Buri", "พัทยา"],
    "ศรีราชา": ["Si Racha", "Chon Buri", "ศรีราชา"],
    "บางแสน": ["Mueang Chon Buri", "Chon Buri", "บางแสน", "แสนสุข"],
    "ชลบุรี": ["Chon Buri", "Mueang Chon Buri", "Si Racha", "ชลบุรี"]
}

_LOC_KEYS_SORTED = sorted(LOC_MAP.keys(), key=len, reverse=True)
_GEO_INDEX_LOCK = threading.Lock()

TYPE_MAP = {
    "ทาวน์โฮม": ["TH"],
    "ทาวน์เฮ้าส์": ["TH"],
    "ทาวน์เฮาส์": ["TH"],
    "ทวาน์โฮม": ["TH"],
    "บ้านเดี่ยว": ["SDH"],
    "บ้านแฝด": ["SDH"],
    "คอนโด": ["CD"],
    "ห้องชุด": ["CD"],
    "ที่ดิน": ["LAND"],
    "อาคารพาณิชย์": ["COMM"],
    "ตึกแถว": ["COMM"],
    "อพาร์ทเม้นท์": ["COMM"],
    "อพาร์ทเมนท์": ["COMM"],
    "อพาร์ตเมนต์": ["COMM"],
    "หอพัก": ["COMM"],
    "apartment": ["COMM"],
    "โรงแรม": ["COMM"],
    "รีสอร์ท": ["COMM"],
    "hotel": ["COMM"],
    "สำนักงาน": ["COMM"],
    "ออฟฟิศ": ["COMM"],
    "โฮมออฟฟิศ": ["COMM"],
    "office": ["COMM"],
    "โกดัง": ["COMM"],
    "โรงงาน": ["COMM"],
}

SUB_TYPE_SYNONYMS = [
    ["อพาร์ทเม้นท์", "อพาร์ทเมนท์", "อพาร์ตเมนต์", "หอพัก", "apartment"],
    ["โรงแรม", "รีสอร์ท", "hotel", "resort"],
    ["สำนักงาน", "ออฟฟิศ", "โฮมออฟฟิศ", "office"],
    ["โกดัง", "โรงงาน", "คลังสินค้า"],
]


def _build_prefiltered_catalog_url(ctx: dict, agent_ref: str = "SW001") -> str:
    """Build a pre-filtered client catalog URL matching the user's search context."""
    from urllib.parse import urlencode
    params = {"view": "client", "ref": agent_ref or "SW001"}
    types = (ctx or {}).get("types") or []
    sub_kws = (ctx or {}).get("sub_kws") or []
    locs = (ctx or {}).get("locs") or []
    max_p = (ctx or {}).get("max_p")
    cat_map = {"SDH": "บ้านเดี่ยว", "TH": "ทาวน์โฮม", "CD": "คอนโด", "LAND": "ที่ดิน", "COMM": "อาคารพาณิชย์"}
    if types:
        if len(set(types) & {"SDH", "TH"}) == 2:
            params["cat"] = "บ้าน"
        elif types[0] in cat_map:
            params["cat"] = cat_map[types[0]]
    q_parts = []
    if sub_kws:
        q_parts.append(sub_kws[0])
    if locs:
        q_parts.append(locs[0])
    if q_parts:
        params["q"] = " ".join(q_parts)
    if max_p:
        params["budget"] = str(int(max_p))
    return "https://assets.siwasup.com/catalog.html?" + urlencode(params)


def get_line_profile(user_id):
    if not user_id or user_id == "anon":
        return {"displayName": "ผู้ใช้งานทั่วไป", "pictureUrl": ""}
    if user_id in USER_PROFILE_CACHE:
        return USER_PROFILE_CACHE[user_id]
    url = f"https://api.line.me/v2/bot/profile/{user_id}"
    headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            prof = {
                "displayName": data.get("displayName", "สมาชิก LINE"),
                "pictureUrl": data.get("pictureUrl", ""),
                "statusMessage": data.get("statusMessage", "")
            }
            USER_PROFILE_CACHE[user_id] = prof
            return prof
    except Exception as e:
        print(f"[Profile Lookup Warn]: {e}")
        return {"displayName": f"User ({user_id[-6:]})", "pictureUrl": ""}


def clean_phone_str(phone):
    return re.sub(r'[^0-9]', '', str(phone or ''))

def auto_heal_member_line_profile(user_id, prof=None, text_content=""):
    """
    Zero-Day Defense and Seamless LINE Profile Auto-Healer:
    Whenever a wiped or returning member interacts with LINE OA or logs in via LINE Login,
    automatically matches them by LINE UID, Name/Nickname keywords, or typed phone number,
    pulls their authentic LINE pictureUrl and displayName, updates R2 Vault, and prevents future wipeouts.
    """
    if not user_id or user_id in ('anon', 'system'):
        return None

    if prof is None:
        prof = get_line_profile(user_id)
    if not prof:
        return None

    display_name = prof.get('displayName', '')
    picture_url = prof.get('pictureUrl', '') or prof.get('picture', '')

    # Extract any 9-10 digit Thai mobile phone number from message text
    extracted_phones = []
    if text_content:
        phones_found = re.findall(r'(?:0[689]\d{8}|0[689]\d[-\s]?\d{3}[-\s]?\d{4})', text_content)
        for ph in phones_found:
            clean_p = clean_phone_str(ph)
            if len(clean_p) == 10:
                extracted_phones.append(clean_p)

    store = load_lobby_data()
    approved = store.get('approved', [])
    matched_member = None

    # 1. Match by bound lineUserId
    for m in approved:
        if m.get('lineUserId') == user_id:
            matched_member = m
            break

    # 2. Match by extracted phone number (ONLY unbound seats - prevent takeover!)
    if not matched_member and extracted_phones:
        for m in approved:
            if m.get('lineUserId'):
                continue
            m_phone = clean_phone_str(m.get('phone', ''))
            if m_phone and m_phone in extracted_phones:
                matched_member = m
                break

    # 3. Match by smart name/nickname heuristics (ONLY unbound seats & distinctive tokens)
    if not matched_member and display_name:
        name_lower = display_name.lower().replace(' ', '')
        keywords_map = [
            # Strict Distinctive Tokens: Prevent loose substring collisions & account takeover
            ('app_office_001', ['varinthorn', 'วรินทร', 'กูลจีรัง', 'sw001 jeab', 'jeab v@r']),
            ('app_office_002', ['ตันฑุลทุกุล', 'ภมรมาศ', 'pamornmas']),
            ('app_office_003', ['ว่องสุวรรณวาร', 'วรวลัญช์', 'vorawalun']),
            ('app_admin_001',  ['สุภาพร by ศิวาทรัพย์']),
            ('app_admin_002',  ['ณัฐสุดา พรพริ้ง']),
            ('app_office_004', ['nassty', 'thenassty']),
            ('app_agent_001',  ['เขมิกา ศิวาทรัพย์']),
            ('app_agent_002',  ['ประกายเกียรติกุล']),
            ('app_agent_003',  ['อนัญญา(กัญ)', 'อนัญญา สาททอง']),
            ('app_agent_004',  ['สิทธิชัย มฤคพานิช', 'มฤคพานิช', 'มกุลพานิช']),
            ('app_agent_005',  ['พัชญ์ณิภา เอื้อปัญญากุล', 'เอื้อประโยชน์กิจ']),
            ('app_agent_006',  ['นภมกร วรพัทธ์กุล', 'วรพัทธ์ภูดิท']),
            ('app_agent_007',  ['jaidee asset', 'jaidee0902', 'สุหทัย ปานทอง']),
        ]
        for mem_id, kws in keywords_map:
            if any(k.lower().replace(' ', '') in name_lower for k in kws):
                target = next((m for m in approved if m.get('id') == mem_id), None)
                if target and not target.get('lineUserId'):
                    matched_member = target
                    break

    if matched_member:
        changed = False
        if not matched_member.get('lineUserId'):
            matched_member['lineUserId'] = user_id
            changed = True
        elif matched_member.get('lineUserId') != user_id:
            return None

        cur_avatar = str(matched_member.get('avatar', ''))
        # Replace if picture_url is new or replaces unsplash mockup
        if picture_url and (picture_url != cur_avatar or 'unsplash.com' in cur_avatar or not cur_avatar):
            matched_member['avatar'] = picture_url
            changed = True

        matched_member['last_active_at'] = int(time.time())
        matched_member['line_display_name'] = display_name

        if changed:
            now_str = bkk_now().strftime('%Y-%m-%d %H:%M:%S')
            log_msg = f"[{now_str}] 🛡️✨ [ZERO-DAY AUTO-HEAL] กู้คืนรูปโปรไฟล์ LINE อัตโนมัติ: {matched_member.get('nickname', '')} ({matched_member.get('name', '')}) -> ผูก LINE และเชื่อมรูปภาพสำเร็จ 100%"
            store.setdefault('audit_log', []).insert(0, log_msg)
            save_lobby_data(store)
            print(f"[Auto-Heal Triggered] {log_msg}")

        return matched_member

    return None



def load_chat_logs():
    store = None
    if os.path.exists(CHAT_LOG_PATH):
        try:
            with open(CHAT_LOG_PATH, "r", encoding="utf-8") as f:
                store = json.load(f)
        except Exception:
            pass

    # Always check R2 backup to ensure we have the most up-to-date conversation logs
    try:
        req = urllib.request.Request("https://assets.siwasup.com/" + _R2_CHAT_VAULT_KEY + "?t=" + str(int(time.time())), headers={"User-Agent": "SiwasupSync/1.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            if r.status == 200:
                r2_store = json.loads(r.read().decode("utf-8"))
                r2_convs = r2_store.get("conversations", [])
                if not store or not store.get("conversations"):
                    store = r2_store
                elif r2_convs:
                    local_convs = store.get("conversations", [])
                    known_ids = {c.get("id") or (c.get("timestamp", "") + "_" + c.get("user_text", "")): c for c in local_convs}
                    merged = False
                    for rc in r2_convs:
                        rk = rc.get("id") or (rc.get("timestamp", "") + "_" + rc.get("user_text", ""))
                        if rk and rk not in known_ids:
                            known_ids[rk] = rc
                            merged = True
                    if merged or len(r2_convs) > len(local_convs):
                        all_items = list(known_ids.values())
                        all_items.sort(key=lambda x: str(x.get("timestamp", "")), reverse=True)
                        store["conversations"] = all_items
                        store["total_logged"] = len(all_items)
                        try:
                            with open(CHAT_LOG_PATH, "w", encoding="utf-8") as fw:
                                json.dump(store, fw, ensure_ascii=False, indent=2)
                        except Exception:
                            pass
    except Exception as _e:
        pass

    if store and isinstance(store.get("conversations"), list):
        return store

    return {
        "bot_name": "Siwasupagent (@813nyyia)",
        "updated_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_logged": 0,
        "historical_summary": {
            "2026-10-29_replies_sent": 18,
            "followers_count": 2,
            "note": "ข้อความ 18 รายการแรกวันที่ 29 ต.ค. 2569 บันทึกผ่านทาง Terminal ก่อนเปิดระบบบันทึกสด วันที่ 31 ต.ค. 2569 เป็นต้นไป ทุกข้อความจะถูกบันทึกสดเรียลไทม์แบบ Real-Time 100%"
        },
        "conversations": []
    }


_CHAT_SYNC_STATUS_LOCK = threading.Lock()
_CHAT_R2_UPLOAD_LOCK = threading.Lock()
_CHAT_SYNC_SEQ = 0
_CHAT_SHUTTING_DOWN = False
_CHAT_R2_SYNC_STATUS = {
    "last_sync_ok": None,
    "last_sync_time": None,
    "last_sync_error": None,
    "last_http_status": None,
}


def _write_chat_log_atomic(data_bytes: bytes):
    tmp_path = CHAT_LOG_PATH + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(data_bytes)
    os.replace(tmp_path, CHAT_LOG_PATH)


def append_chat_log(entry):
    global _CHAT_SYNC_SEQ
    with LOG_LOCK:
        store = load_chat_logs()
        store["conversations"].insert(0, entry)
        store["conversations"] = store["conversations"][:500]
        store["total_logged"] = len(store["conversations"])
        store["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            _write_chat_log_atomic(data_bytes)
        except Exception as e:
            print(f"[Log Save Error]: {e}")

        _CHAT_SYNC_SEQ += 1
        my_seq = _CHAT_SYNC_SEQ
        total_logged = store["total_logged"]

        # Persistent Cloud Backup: Sync to Cloudflare R2 asynchronously (ordered + retry) so logs survive Render restarts
        if put_object_r2:
            def sync_r2():
                with _CHAT_R2_UPLOAD_LOCK:
                    if _CHAT_SHUTTING_DOWN or my_seq < _CHAT_SYNC_SEQ:
                        return
                    last_err = None
                    last_status = None
                    for attempt in range(2):
                        if _CHAT_SHUTTING_DOWN or my_seq < _CHAT_SYNC_SEQ:
                            return
                        try:
                            status_code = put_object_r2(_R2_CHAT_VAULT_KEY, data_bytes, "application/json; charset=utf-8")
                            last_status = int(status_code) if status_code is not None else None
                            if last_status is not None and 200 <= last_status < 300:
                                with _CHAT_SYNC_STATUS_LOCK:
                                    _CHAT_R2_SYNC_STATUS["last_http_status"] = last_status
                                    _CHAT_R2_SYNC_STATUS["last_sync_ok"] = True
                                    _CHAT_R2_SYNC_STATUS["last_sync_time"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                                    _CHAT_R2_SYNC_STATUS["last_sync_error"] = None
                                print(f"[R2 Chat Sync OK] total={total_logged} status={last_status}")
                                return
                            last_err = f"HTTP {last_status}"
                        except urllib.error.HTTPError as he:
                            last_status = getattr(he, "code", None)
                            last_err = f"HTTPError {last_status}"
                        except Exception as ex:
                            last_status = None
                            last_err = type(ex).__name__
                        if attempt == 0:
                            time.sleep(1.5)
                    with _CHAT_SYNC_STATUS_LOCK:
                        _CHAT_R2_SYNC_STATUS["last_http_status"] = last_status
                        _CHAT_R2_SYNC_STATUS["last_sync_ok"] = False
                        _CHAT_R2_SYNC_STATUS["last_sync_time"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                        _CHAT_R2_SYNC_STATUS["last_sync_error"] = last_err
                    print(f"[R2 Sync Log Error]: {last_err}")
            threading.Thread(target=sync_r2, daemon=True).start()


WORKFLOW_KEYWORDS = [
    "จองคิวเพิ่มได้อีกกี่", "จองได้กี่ที่", "จองคิวเพิ่มได้กี่", "แจ้งใคร", "รับกุญแจ", "ส่งคืนกุญแจ",
    "กุญแจรับที่ไหน", "เปิดบ้านได้กี่รอบ", "รอบละกี่ชั่วโมง", "otp", "ตู้ smart keybox",
    "พี่ลิลลี่", "นัดเปิดบ้านยังไง", "กฎการเปิดบ้าน", "ขอกุญแจยังไง"
]

SEARCH_ACTION_KEYWORDS = [
    "มัดรวม", "สาดมา", "เอามา", "จัดมา", "ส่งมา", "ขอบ้าน", "ขอคอนโด", "ขอทาวน์",
    "ใกล้ที่สุด", "มีอะไรบ้าง", "เหลืออะไร", "มีเหลือไหม", "ลิสต์มา", "ดูหน่อย",
    "แนะนำหน่อย", "หา", "มีบ้าน", "มีคอนโด", "มีทาวน์", "ไม่อั้น", "ทุ่มเพิ่ม",
    "งบเปิด", "ไม่จำกัด", "คอนโดล่ะ", "บ้านล่ะ", "ทาวน์โฮมล่ะ", "มีไหม", "แถวนี้มี",
    "ย่านนี้", "พอไหว", "เปิดดีล", "ปิดดีล", "ขอแค่ใกล้", "ลูกค้าอยากได้", "สาดมาเลย"
]


def parse_price(text):
    # Only parse explicit price mentions (e.g. "3 ล้าน", "งบ 2,500,000", "ราคา 1.8 ล้าน", "ไม่เกิน 4 ล้าน", "5 m")
    # Never treat a property ID like "รหัสทรัพย์ 1090965" as a price!
    cleaned = re.sub(r'รหัส(?:ทรัพย์)?\s*#?[A-Za-z0-9\-]+', '', text)
    m_m = re.search(r'([0-9\.]+)\s*(?:ล้าน|m\b)', cleaned, re.IGNORECASE)
    if m_m:
        try:
            return int(float(m_m.group(1)) * 1000000)
        except Exception:
            pass
    m_k = re.search(r'([0-9\.]+)\s*(?:แสน|k\b)', cleaned, re.IGNORECASE)
    if m_k:
        try:
            return int(float(m_k.group(1)) * 100000)
        except Exception:
            pass
    m_explicit = re.search(r'(?:งบ|ราคา|ไม่เกิน)\s*([0-9,]{5,10})', cleaned)
    if m_explicit:
        try:
            return int(m_explicit.group(1).replace(',', ''))
        except Exception:
            pass
    return None


def search_properties(query, user_id=None):
    q_low = query.lower().strip()

    # Guard against conflicting distant zones in one query (e.g. "ขอบ้าน ทุ่งครุ มีนบุรี")
    conflicts = _detect_conflicting_zones(query, threshold_km=20.0)
    if len(conflicts) >= 2:
        return [], "GEO_CONFLICT_CONFIRM:" + "|".join(conflicts)

    # Detect requested quantity (e.g. "ขอ 5", "ขอไป 5", "ขอ 5 หลัง", "มี 4 ที่มั้ย")
    target_count = 5  # default 5 results (expandable up to 10)
    m_count = re.search(r'(?:ขอไป|ขอ|เอา|ดู|สัก|ส่งมา|มี)\s*(\d{1,2})\s*(?:หลัง|ที่|แปลง|รายการ|ห้อง|แห่ง)?(?!\s*(?:ล้าน|บาท))', query)
    if m_count:
        try:
            req_c = int(m_count.group(1))
            if 1 <= req_c <= 10:
                target_count = req_c
        except Exception:
            pass
    else:
        m_count2 = re.search(r'(\d{1,2})\s*(?:หลัง|ที่|แปลง|รายการ|ห้อง|แห่ง)(?!\s*(?:ล้าน|บาท))', query)
        if m_count2:
            try:
                req_c = int(m_count2.group(1))
                if 1 <= req_c <= 10:
                    target_count = req_c
            except Exception:
                pass

    # 1. Exact Property Code Search in Siwasup Portfolio (e.g., 1090965) AND NPA Catalog
    for sp in SIWASUP_PROPS:
        sid = str(sp.get("id") or "").strip()
        if sid and len(sid) >= 5 and sid.lower() in q_low:
            return [{
                "code": sid,
                "bank": sp.get("bank_source") or "Siwasup",
                "title": sp.get("title"),
                "type": sp.get("category") or "บ้าน",
                "location": sp.get("location") or "กรุงเทพฯ และปริมณฑล",
                "price": _format_prop_price_text(sp.get("price")),
                "status": "ขายแล้ว/ตัดสต๊อก" if (sp.get("status") == "sold_archive" or sp.get("is_image_soldout")) else "พร้อมเปิดให้เข้าชม",
                "description": (sp.get("description") or "")[:300]
            }], "EXACT_SIWASUP_CODE"

    for p in CATALOG:
        code = str(p.get('c') or '')
        if code and len(code) >= 5 and code.lower() in q_low:
            return [{
                "code": code,
                "bank": p.get('b'),
                "type": p.get('tn', 'บ้าน'),
                "district": p.get('d'),
                "province": p.get('p'),
                "price": _format_prop_price_text(p.get('pr')),
                "land_sqw": p.get('sqw'),
                "living_sqm": p.get('sqm'),
                "status": "พร้อมเปิดให้เข้าชม"
            }], "EXACT_NPA_CODE"

    # 2. Project / Title Keyword Match in Siwasup Portfolio (Smart Substring & Brand Parsing)
    known_project_brands = [
        "ซิกเนเจอร์", "มัณฑนา", "พาทิโอ", "ลุมพินี", "lumpini", "เพลส",
        "ศุภาลัย", "ยูดีไลท์", "ชวนชื่น", "พฤกษา", "เซ็นทริค",
        "ไอดีโอ", "แอสปาย", "ดีคอนโด", "พลัมคอนโด"
    ]
    detected_brand_kws = [k for k in known_project_brands if k.lower() in q_low]
    stop_words = ["เป๊ะนะครับ", "เป็น", "ทวาน์โฮม", "ทาวน์โฮม", "บ้านเดี่ยว", "คอนโด", "ช่วยตรวจสอบให้หน่อย", "อยากนัดเปิดบ้าน", "ใกล้สถานีรถไฟฟ้า"]
    raw_split = [w for w in re.split(r'\s+', query) if len(w) >= 3 and w not in stop_words and not w.startswith("ช่วย") and not w.startswith("อยาก")]
    all_search_kws = list(set(raw_split + detected_brand_kws))

    if detected_brand_kws or any(k in query for k in ["ซิกเนเจอร์", "มัณฑนา", "พาทิโอ", "ลุมพินี", "ชวนชื่น", "พฤกษา", "เซ็นทริค"]):
        matched_siwa = []
        for sp in SIWASUP_PROPS:
            title_desc = ((sp.get("title") or "") + " " + (sp.get("description") or "") + " " + (sp.get("location") or "")).lower()
            score = sum(1 for kw in all_search_kws if kw.lower() in title_desc)
            if score >= 1 and (not detected_brand_kws or any(dk.lower() in title_desc for dk in detected_brand_kws)):
                matched_siwa.append((score, sp))
        if matched_siwa:
            matched_siwa.sort(key=lambda x: x[0], reverse=True)
            out = []
            for _, sp in matched_siwa[:3]:
                out.append({
                    "code": str(sp.get("id")),
                    "bank": sp.get("bank_source") or "Siwasup",
                    "title": sp.get("title"),
                    "type": sp.get("category") or "คอนโด",
                    "location": sp.get("location") or "กรุงเทพฯ",
                    "price": _format_prop_price_text(sp.get("price")),
                    "status": "ขายแล้ว/ตัดสต็อก" if (sp.get("status") == "sold_archive" or sp.get("is_image_soldout")) else "พร้อมเปิดให้เข้าชม"
                })
            if user_id:
                USER_SEARCH_CONTEXT.setdefault(user_id, {})["last_matched"] = out
            return out, "PROJECT_NAME_MATCH"

    # 3. Check if this is purely a workflow/process/booking question
    if any(w in q_low for w in WORKFLOW_KEYWORDS):
        return [], "WORKFLOW_QUESTION"

    # 4. Multi-Turn Search Context Management (30-min TTL expiry)
    uid = user_id or "default"
    existing_ctx = USER_SEARCH_CONTEXT.get(uid)
    if existing_ctx and (time.time() - existing_ctx.get("updated_at", 0) > 1800):
        USER_SEARCH_CONTEXT.pop(uid, None)
    ctx = USER_SEARCH_CONTEXT.setdefault(uid, {
        "types": [],
        "sub_kws": [],
        "locs": [],
        "max_p": None,
        "unlimited": False,
        "updated_at": time.time()
    })

    # If this turn is simply "มีไหม", "มีหรือเปล่า", "มีห้องไหม" and we recently matched a project:
    if any(q_low == trigger or q_low.startswith(trigger) for trigger in ["มีไหม", "มีมั้ย", "มีหรือเปล่า", "มีมั่งไหม", "ขอดูหน่อย", "ส่งมาดู"]) and ctx.get("last_matched"):
        return ctx["last_matched"], "MULTI_TURN_PROJECT_FOLLOWUP"

    # Clean query for type check (strip viewing verbs)
    q_for_type = re.sub(r'(?:เปิดบ้าน|ชมบ้าน|ดูบ้าน|กุญแจบ้าน|เข้าบ้าน|ล็อกบ้าน|หน้าบ้าน)', '', query)

    # Detect new types in current message (Strict type discrimination + Commercial Sub-Type Synonyms)
    new_types = []
    detected_sub_kws = []
    for syn_group in SUB_TYPE_SYNONYMS:
        if any(sk in q_for_type.lower() for sk in syn_group):
            detected_sub_kws = syn_group
            new_types.extend(["COMM"])
            break
    if not new_types and any(k in q_for_type for k in ["บ้านเดี่ยว", "บ้านแฝด"]):
        new_types.extend(["SDH"])
    elif not new_types and any(k in q_for_type for k in ["ทาวน์โฮม", "ทาวน์เฮ้าส์", "ทาวน์เฮาส์", "ทวาน์โฮม"]):
        new_types.extend(["TH"])
    elif not new_types and any(k in q_for_type for k in ["คอนโด", "ห้องชุด", "condo"]):
        new_types.extend(["CD"])
    elif not new_types and any(k in q_for_type for k in ["ที่ดิน", "แปลงที่ดิน"]):
        new_types.extend(["LAND"])
    elif not new_types and any(k in q_for_type for k in ["อาคารพาณิชย์", "ตึกแถว"]):
        new_types.extend(["COMM"])
    elif not new_types and "บ้าน" in q_for_type:
        # General "บ้าน" = residential ground houses (SDH, TH) - strictly excludes Condo, Land, or Commercial!
        new_types.extend(["SDH", "TH"])
    elif not new_types:
        for k, v in TYPE_MAP.items():
            if k in q_for_type.lower():
                new_types.extend(v)
    if new_types:
        ctx["types"] = list(set(new_types))
        ctx["sub_kws"] = detected_sub_kws

    # Detect new locations in current message (precomputed longest LOC_MAP keys first + all districts/provinces + fuzzy typo match)
    new_locs = []
    for k in _LOC_KEYS_SORTED:
        if k in query:
            new_locs.extend(LOC_MAP[k])

    # Thread-safe lazy auto-index of district/province names from CATALOG + SIWASUP_PROPS
    if not hasattr(search_properties, "_geo_terms"):
        with _GEO_INDEX_LOCK:
            if not hasattr(search_properties, "_geo_terms"):
                geo_map = {}
                for cp in CATALOG:
                    for fld in ("d", "p", "pe"):
                        val = str(cp.get(fld) or "").strip()
                        if len(val) >= 4:
                            geo_map.setdefault(val.lower(), val)
                for sp in SIWASUP_PROPS:
                    loc_s = str(sp.get("location") or "").strip()
                    for part in re.split(r"[•,/|\s]+", loc_s):
                        part = part.strip()
                        if len(part) >= 4 and not part.isdigit():
                            geo_map.setdefault(part.lower(), part)
                search_properties._geo_terms = geo_map
                search_properties._all_candidates = list(LOC_MAP.keys()) + list(geo_map.values())
    geo_terms = search_properties._geo_terms
    all_candidates = search_properties._all_candidates

    # Direct match against known district/province names (len >= 4 avoids short false positives)
    for gk, gval in geo_terms.items():
        if gk in q_low and gval not in new_locs:
            new_locs.append(gval)

    # Dynamic regex matcher for terms like โซน..., แถว..., เขต..., ย่าน..., อำเภอ... + fuzzy typo matching
    zone_matches = re.findall(r'(?:โซน|แถว|เขต|ย่าน|อำเภอ|ทำเล)\s*([ก-๙a-zA-Z0-9\-\.]+)', query)
    for zm in zone_matches:
        for sub_zm in re.split(r'[\-\s]+', zm.strip()):
            zm_clean = sub_zm.strip()
            if len(zm_clean) < 3 or zm_clean in ["บ้าน", "คอนโด", "ที่ดิน", "ไหน", "นี้", "ราคา", "งบ"]:
                continue
            matched_sub = False
            for k in _LOC_KEYS_SORTED:
                if k in zm_clean or zm_clean in k:
                    new_locs.extend(LOC_MAP[k])
                    matched_sub = True
            if not matched_sub:
                for cp in CATALOG:
                    d_val = str(cp.get('d', ''))
                    p_val = str(cp.get('p', ''))
                    if zm_clean.lower() in d_val.lower() or zm_clean in p_val:
                        if d_val and d_val not in new_locs:
                            new_locs.append(d_val)
                        if zm_clean not in new_locs:
                            new_locs.append(zm_clean)
                        matched_sub = True
                        break
            if not matched_sub:
                close = difflib.get_close_matches(zm_clean, all_candidates, n=2, cutoff=0.75)
                for c_hit in close:
                    if c_hit in LOC_MAP:
                        new_locs.extend(LOC_MAP[c_hit])
                    elif c_hit not in new_locs:
                        new_locs.append(c_hit)

    # Nationwide Thai Geo extraction (handles 'คานหามอยุธยา', 'โคราช', etc. before TOO_VAGUE check)
    if not new_locs:
        _q_geo = _extract_thai_geo(query)
        if _q_geo:
            for _gk in ("subdistrict", "district", "province"):
                _gv = _q_geo.get(_gk)
                if _gv and _gv not in new_locs:
                    new_locs.append(_gv)

    # Fallback fuzzy check on standalone Thai/Eng tokens if still no location matched
    if not new_locs:
        tokens_chk = [t for t in re.findall(r'[ก-๙a-zA-Z]{4,24}', query) if t not in ("อยากได้", "ต้องการ", "แนะนำ", "มัดรวม", "ส่งมา", "บ้านเดี่ยว", "ทาวน์โฮม", "ทาวน์เฮ้าส์", "คอนโด", "ที่ดิน", "ราคา", "ไม่เกิน")]
        for tok in tokens_chk[:6]:
            close = difflib.get_close_matches(tok, all_candidates, n=1, cutoff=0.80)
            for c_hit in close:
                if c_hit in LOC_MAP:
                    new_locs.extend(LOC_MAP[c_hit])
                elif c_hit not in new_locs:
                    new_locs.append(c_hit)

    if new_locs:
        ctx["locs"] = list(dict.fromkeys(new_locs))
    elif zone_matches:
        ctx["locs"] = []

    # Detect budget changes
    if any(w in q_low for w in ["ไม่อั้น", "ทุ่มเพิ่ม", "งบเปิด", "ไม่จำกัด", "เท่าไหร่ก็ได้", "กี่บาทก็ได้", "แพงแค่ไหน"]):
        ctx["unlimited"] = True
        ctx["max_p"] = None
    else:
        parsed_p = parse_price(query)
        if parsed_p:
            ctx["max_p"] = parsed_p
            ctx["unlimited"] = False

    ctx["updated_at"] = time.time()

    # Determine if this turn is asking to search or view properties
    has_trigger = any(w in q_low for w in SEARCH_ACTION_KEYWORDS) or bool(m_count) or bool(m_count2) or any(w in q_low for w in ['ขอไป', 'ขอเพิ่ม', 'เอาอีก', 'ส่งมาอีก'])
    has_type = bool(new_types)
    has_loc = bool(new_locs)
    has_price = bool(parse_price(query)) or ctx["unlimited"]

    if not (has_trigger or has_type or has_loc or has_price):
        return [], "NOT_PROPERTY_SEARCH"

    # Search Catalog using effective Context
    eff_types = ctx["types"]
    eff_locs = ctx["locs"]
    eff_max_p = ctx["max_p"]
    eff_unlimited = ctx["unlimited"]

    # When query is too vague (e.g. only says 'อยากได้บ้าน', 'หาบ้าน', 'สนใจคอนโด')
    # without specifying ANY location, price, or explicit dump command:
    # Ask clarifying questions first instead of randomly dumping 3 properties!
    explicit_dump = any(k in q_low for k in ["ทั้งหมด", "สาดมา", "เอามาเลย", "อะไรก็ได้", "จัดมา", "ลิสต์มา", "ดูหน่อย"])
    if eff_types and not eff_locs and not eff_max_p and not eff_unlimited and not explicit_dump:
        return [], "TOO_VAGUE_NEEDS_MORE_INFO" 

    eff_sub_kws = ctx.get("sub_kws") or []
    results = []
    for p in CATALOG:
        if eff_types and p.get('t') not in eff_types:
            continue
        if eff_sub_kws:
            p_text = f"{p.get('tn', '')} {p.get('n', '')}".lower()
            if not any(sk in p_text for sk in eff_sub_kws):
                continue
        pr = p.get('pr', 0)
        if eff_max_p and pr > eff_max_p:
            continue
        if not eff_max_p and not eff_unlimited:
            # Default realistic residential budget (1M - 12M)
            if pr < 1000000 or pr > 12000000:
                continue
        if eff_locs:
            d = p.get('d', '')
            pe = p.get('pe', '')
            p_th = p.get('p', '')
            if not any(loc.lower() in d.lower() or loc.lower() in pe.lower() or loc in p_th for loc in eff_locs):
                continue
        else:
            if p.get('pe') not in {'Bangkok', 'Nonthaburi', 'Pathum Thani', 'Samut Prakan'}:
                continue
        results.append(p)

    # Automatic geographic expansion ONLY when explicitly searching Siriraj / inner-Thonburi core
    if len(results) < target_count and eff_locs and any(w in str(eff_locs) for w in ['Bangkok Noi', 'Bang Phlat', 'Thon Buri']) and 'Nonthaburi' not in str(eff_locs):
        west_expand = ['Taling Chan', 'Bangkok Noi', 'Bang Phlat', 'Thawi Watthana', 'Phasi Charoen', 'Thon Buri']
        existing_cat_codes = {p.get('c') for p in results}
        for p in CATALOG:
            if len(results) >= target_count * 2:
                break
            if p.get('c') in existing_cat_codes:
                continue
            if eff_types and p.get('t') not in eff_types:
                continue
            if eff_sub_kws:
                p_text = f"{p.get('tn', '')} {p.get('n', '')}".lower()
                if not any(sk in p_text for sk in eff_sub_kws):
                    continue
            pr = p.get('pr', 0)
            if eff_max_p and pr > eff_max_p:
                continue
            if not eff_max_p and not eff_unlimited:
                if pr < 800000 or pr > 15000000:
                    continue
            d = p.get('d', '')
            if any(loc.lower() in d.lower() for loc in west_expand):
                results.append(p)
                existing_cat_codes.add(p.get('c'))

    # Prioritize web catalog properties (SIWASUP_PROPS = 995 items with real photos on catalog.html) first!
    web_results = []
    cat_type_map = {"SDH": ["บ้านเดี่ยว", "บ้านแฝด"], "TH": ["ทาวน์โฮม", "ทาวน์เฮ้าส์"], "CD": ["คอนโด", "ห้องชุด"], "LAND": ["ที่ดิน"], "COMM": ["อาคารพาณิชย์", "ตึกแถว", "โฮมออฟฟิศ"]}
    allowed_cats = []
    for t_code in eff_types:
        allowed_cats.extend(cat_type_map.get(t_code, []))

    for sp in SIWASUP_PROPS:
        if sp.get("status") in ("sold_archive", "transferred") or sp.get("is_image_soldout"):
            continue
        sp_cat = sp.get("category") or ""
        if allowed_cats and not any(ac in sp_cat for ac in allowed_cats):
            if not eff_sub_kws:
                continue
        if eff_sub_kws:
            sp_text = f"{sp_cat} {sp.get('title') or ''} {sp.get('description') or ''} {sp.get('search_keywords') or ''}".lower()
            if not any(sk in sp_text for sk in eff_sub_kws):
                continue
        pr = _parse_prop_price_int(sp.get("price"))
        if eff_max_p and (pr <= 0 or pr > eff_max_p):
            continue
        if not eff_max_p and not eff_unlimited:
            if pr < 800000 or pr > 15000000:
                continue
        haystack = " ".join([
            str(sp.get("title") or ""),
            str(sp.get("description") or ""),
            str(sp.get("location") or ""),
            str(sp.get("subdistrict_th") or ""),
            str(sp.get("district_th") or ""),
            str(sp.get("province_th") or ""),
            str(sp.get("search_keywords") or "")
        ]).lower()
        if eff_locs:
            if not any(loc.lower() in haystack for loc in eff_locs):
                continue
        web_results.append({
            "c": str(sp.get("id")),
            "b": sp.get("bank_source") or "Siwasup",
            "tn": sp.get("category") or "บ้านเดี่ยว",
            "d": sp.get("district_th") or (sp.get("location") or sp.get("title") or "กรุงเทพฯ").split("•")[0].strip(),
            "p": sp.get("province_th") or (sp.get("location") or "กรุงเทพมหานคร").split("•")[-1].strip(),
            "pr": pr,
            "sqw": (sp.get("size") or "-").replace(" ตร.ว.", ""),
            "sqm": (sp.get("usable_area") or "-").replace(" ตร.ม.", ""),
            "_web": True
        })

    # Nationwide Geo + Haversine Nearest Fallback when standard keyword search returns empty
    if not web_results and not results:
        geo_hit = _extract_thai_geo(query)
        if geo_hit and geo_hit.get("lat") and geo_hit.get("lng"):
            nearest = _find_nearest_siwasup_props(
                geo_hit["lat"], geo_hit["lng"],
                allowed_cats=allowed_cats or None,
                max_p=eff_max_p,
                limit=target_count
            )
            if nearest:
                return nearest, "NEAREST_GEO_FALLBACK"

    # Sorting (Web catalog properties with photos always come first!)
    if eff_unlimited:
        web_results.sort(key=lambda x: x.get('pr', 0), reverse=True)
        results.sort(key=lambda x: x.get('pr', 0), reverse=True)
    elif eff_max_p:
        web_results.sort(key=lambda x: abs((x.get('pr') or 0) - eff_max_p))
        results.sort(key=lambda x: abs((x.get('pr') or 0) - eff_max_p))
    else:
        web_results.sort(key=lambda x: abs((x.get('pr') or 0) - 4000000))
        results.sort(key=lambda x: abs((x.get('pr') or 0) - 4000000))

    seen_codes = {x.get('c') for x in web_results}
    results = web_results + [r for r in results if r.get('c') not in seen_codes]

    if not results:
        return [], "EMPTY_SEARCH_RESULT"

    out_list = []
    for p in results[:target_count]:
        out_list.append({
            "code": p.get('c'),
            "bank": p.get('b'),
            "type": p.get('tn', 'บ้าน'),
            "district": p.get('d'),
            "province": p.get('p'),
            "price": _format_prop_price_text(p.get('pr')),
            "land_sqw": p.get('sqw'),
            "living_sqm": p.get('sqm'),
            "status": "พร้อมเปิดให้เข้าชม"
        })

    search_mode = "SMART_CONTEXT_MATCH" if (has_trigger and not has_loc) else "FILTER_MATCH"
    return out_list, search_mode


SYSTEM_INSTRUCTION = """คุณคือ "น้องศิวา" (Siwasup AI) ผู้ช่วยอัจฉริยะประจำ LINE Official Account ของ บริษัท ศิวาทรัพย์ แอสเซท จำกัด (Siwasup Asset Co-Broker Hub)
บุคลิก: ฉลาด รอบคอบ สุภาพ เป็นกันเอง และตอบตรงคำถาม (ลงท้ายด้วย "ครับ" เสมอ)

กฎเหล็กสำคัญที่สุด (ห้ามมึนและห้ามยัดเยียดขายของไม่ตรงคำถาม!):
1. **ห้ามแนะนำทรัพย์ที่ไม่เกี่ยวข้องเด็ดขาด:** หากผู้ใช้กำลังถามเรื่อง "วิธีเปิดบ้าน", "กฎการจองคิว", "จองเพิ่มได้อีกกี่ที่", หรือ "แจ้งนัดหมาย" ให้ตอบเฉพาะเรื่องที่ผู้ใช้ถามเท่านั้น **ห้ามหยิบบ้านแปลงอื่นมาขายพ่วงท้ายคำตอบเด็ดขาด** ยกเว้นผู้ใช้พิมพ์ขอให้ค้นหาทรัพย์!
2. **จดจำบริบทบทสนทนาก่อนหน้า (Conversation History):** หากผู้ใช้แจ้งรหัสทรัพย์ (เช่น #1090965 ทาวน์โฮม ซิกเนเจอร์ รามอินทรา 109), วันนัด, รอบเวลา, หรือชื่อลูกค้า (เช่น คุณองอาจ) ไว้ในข้อความก่อนหน้า ให้จำและสรุปทวนรายการนั้นให้ครบถ้วนถูกต้อง
3. **แยกแยะกฎคิวเปิดบ้านให้แม่นยำ:**
   - **ต่อบ้าน 1 หลัง:** เปิดรับเข้าชมสูงสุด **วันละ 2 รอบ** (รอบเช้า `09:00 - 12:30 น.` และ รอบบ่าย `13:30 - 17:00 น.`) เพื่อให้ตัวแทนมีเวลาพาลูกค้าชมบ้านและถ่ายคอนเทนต์ได้เต็มที่ 3.5 ชม.
   - **กรณีตัวแทน 1 คนอยากจองเปิดบ้าน "หลังอื่นเพิ่มเติม":**
     * หากเป็น **คนละวันกัน** สามารถจองนัดเปิดบ้านหลังอื่นเพิ่มเติมได้ตามปกติ
     * หากเป็น **วันเดียวกัน** ตัวแทน 1 คนสามารถจองได้สูงสุด **2 หลัง (บ้านหลังที่ 1 รอบเช้า 09:00-12:30 น. และบ้านหลังที่ 2 รอบบ่าย 13:30-17:00 น.)** เพราะเวลาแต่ละรอบไม่ชนกัน
     * แต่ห้ามจองเปิดบ้าน 2 หลังในรอบเวลาเดียวกัน (เช่น รอบเช้าพร้อมกัน 2 หลัง) และห้ามจองกั๊กคิวโดยไม่มีชื่อลูกค้าผู้ซื้อจริง
4. **การรับและส่งคืนกุญแจ:**
   - วันจันทร์ - เสาร์ (เวลาทำการ): รับ-คืนได้ที่ออฟฟิศท่าข้าม 12 (พี่ลิลลี่) หรือเรียก Messenger จัดส่ง
   - นอกเวลาทำการ / วันอาทิตย์ / ส่งไม้ต่อเช้า-บ่าย: ใช้ **Smart Keybox รุ่นห่วงคล้องพกพา (รหัส OTP)** ที่พี่ลิลลี่ควบคุมรหัสจากออฟฟิศ
5. **กฎการทักทาย:** ถ้าคุยต่อเนื่อง ห้ามพูด "สวัสดีครับ" ซ้ำ ให้เข้าเรื่องทันที
6. **ความตรงประเด็นเรื่องประเภททรัพย์:** หากผู้ใช้ขอ "บ้าน" (เช่น ขอบ้านแถวบางแค, หาบ้าน) ให้แนะนำเฉพาะ บ้านเดี่ยว, บ้านแฝด หรือทาวน์โฮม/ทาวน์เฮ้าส์ เท่านั้น **ห้ามใส่คอนโดหรือที่ดินมาเด็ดขาด** เว้นแต่ผู้ใช้จะระบุคำว่า "คอนโด" หรือ "ห้องชุด" โดยตรง
7. **การสอบถามเพื่อคัดกรองความต้องการ (Qualifying Leads):** หากผู้ใช้บอกความต้องการลอยๆ แบบกว้างมาก (เช่น "อยากได้บ้าน", "หาบ้าน", "สนใจคอนโด", "มีบ้านไหม") โดยที่ยังไม่ได้ระบุทำเลหรือช่วงราคา **อย่าเพิ่งรีบสุ่มทรัพย์มาแนะนำ** ให้ตอบรับอย่างกระตือรือร้นและสุภาพ แล้วสอบถามข้อมูลเพิ่มเติมสั้นๆ (เช่น สะดวกโซน/ทำเลไหนเป็นพิเศษ และมีงบประมาณในใจประมาณเท่าไหร่) เพื่อคัดแปลงที่ตรงใจที่สุดให้ครับ
8. กฎการจัดรูปแบบข้อความใน LINE (ห้ามใช้ Markdown): ห้ามใส่เครื่องหมาย ** หรือ __ หรือ ` ในคำตอบเด็ดขาด เพราะ LINE ไม่แปลงเป็นตัวหนา ให้ใช้การขึ้นบรรทัดใหม่ อิโมจิ หรือสัญลักษณ์ • / - แทนเพื่อให้อ่านง่ายบนมือถือครับ"""


def ask_gemini(user_id, user_text, is_continuous=False, retries=2):
    matched_props, search_mode = search_properties(user_text, user_id=user_id)
    if str(search_mode).startswith("GEO_CONFLICT_CONFIRM:"):
        zones = search_mode.split(":", 1)[1].split("|")
        z_str = " กับ ".join(zones[:2]) if len(zones) == 2 else ", ".join(zones)
        msg = (
            f"📍 เห็นระบุมา {len(zones)} โซนที่อยู่คนละฝั่งกัน ({z_str}) — "
            f"อยากให้คัดเน้นโซนไหนก่อน หรือให้ส่งแยกทีละโซนดีครับ?"
        )
        return msg, [], "GEO_CONFLICT_CONFIRM", []
    history = USER_CHAT_HISTORY.get(user_id, [])

    prompt_parts = []
    if history:
        prompt_parts.append("[ประวัติการสนทนาก่อนหน้ากับผู้ใช้คนนี้ (ใช้เพื่อจำรหัสทรัพย์ ชื่อลูกค้า และนัดหมาย)]:")
        for turn in history[-6:]:
            prompt_parts.append(f"- ผู้ใช้: {turn['user']}")
            prompt_parts.append(f"- น้องศิวา: {turn['bot']}")
        prompt_parts.append("")

    prompt_parts.append(f"ข้อความล่าสุดจากผู้ใช้: {user_text}")
    if is_continuous:
        prompt_parts.append("[สถานะ: กำลังคุยต่อเนื่อง ห้ามสวัสดีซ้ำเด็ดขาด]")

    if search_mode == "EMPTY_SEARCH_RESULT":
        prefiltered_url = _build_prefiltered_catalog_url(USER_SEARCH_CONTEXT.get(user_id, {}))
        msg = (
            "ขออภัยครับ น้องศิวาค้นหาในระบบแล้วยังไม่พบทรัพย์ที่ตรงกับเงื่อนไขนี้ในขณะนี้ครับ\n\n"
            "ลองปรับทำเล ขยายงบประมาณ หรือดูทรัพย์ทั้งหมดบนเว็บ Catalog ได้ที่ลิงก์นี้ครับ:\n"
            f"👉 {prefiltered_url}"
        )
        return msg, [], "EMPTY_SEARCH_RESULT", []

    if matched_props:
        prefiltered_url = _build_prefiltered_catalog_url(USER_SEARCH_CONTEXT.get(user_id, {}))
        prompt_parts.append(
            f"\n[ข้อมูลทรัพย์จริงที่ระบบดึงมาให้ตอบ ({search_mode}) ทั้งหมด {len(matched_props)} หลัง]:\n"
            + json.dumps(matched_props, ensure_ascii=False, indent=2)
            + f"\nคำสั่งสำคัญ: ผู้ใช้ขอดูทรัพย์ ให้ตอบแนะนำข้อมูลทรัพย์จริงครบทั้ง {len(matched_props)} หลัง อย่าตัดทิ้งหรือสรุปย่อ ระบุรหัสทรัพย์ ราคา และทำเลให้ครบถ้วนทุกแปลง และแนบลิงก์ดูทั้งหมดที่ตรงเงื่อนไข: {prefiltered_url}"
        )
    elif search_mode == "TOO_VAGUE_NEEDS_MORE_INFO":
        ctx_types = USER_SEARCH_CONTEXT.get(user_id, {}).get("types", [])
        type_str = "บ้าน" if any(t in ctx_types for t in ["SDH", "TH"]) else ("คอนโด" if "CD" in ctx_types else "อสังหาฯ")
        prompt_parts.append(
            f"\n[คำสั่งสำคัญ]: ผู้ใช้แจ้งความต้องการเบื้องต้นว่าสนใจ '{type_str}' แต่ยังไม่ได้ระบุทำเลหรือช่วงราคาที่ต้องการ "
            "ห้ามสุ่มหยิบทรัพย์มาแนะนำในตอนนี้เด็ดขาด! ให้ตอบรับอย่างยินดี สุภาพ เป็นกันเอง แล้วสอบถามข้อมูลเพิ่มเติมสั้นๆ 1-2 ข้อ "
            "(เช่น สะดวกเป็นทำเลหรือโซนไหนเป็นพิเศษ และมีงบประมาณในใจประมาณเท่าไหร่) เพื่อให้น้องศิวาช่วยคัดแปลงที่ตรงใจและเดินทางสะดวกที่สุดให้ครับ"
        )
    else:
        prompt_parts.append(
            "\n[คำสั่งควบคุม]: ข้อความนี้ไม่ใช่การค้นหาทรัพย์ใหม่ ห้ามแต่งชื่อทรัพย์อื่นหรือยัดเยียดแนะนำบ้านแปลงอื่นที่ไม่เกี่ยวกับคำถามเด็ดขาด ให้ตอบคำถามหรือรับเรื่องนัดหมายตามประวัติการคุยด้านบนอย่างชัดเจนและกระชับ"
        )

    prompt_content = "\n".join(prompt_parts)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt_content}]
            }
        ],
        "generationConfig": {
            "temperature": 0.25,
            "maxOutputTokens": 450
        }
    }

    data_bytes = json.dumps(payload).encode('utf-8')

    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                candidates = data.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        reply = parts[0].get('text', '').strip()
                        if reply:
                            # Save to user memory
                            history.append({"user": user_text, "bot": reply})
                            USER_CHAT_HISTORY[user_id] = history[-8:]
                            return reply, [p.get('code') for p in matched_props], search_mode, matched_props
        except Exception as e:
            print(f"[Gemini Error Attempt {attempt+1}]: {e}")
            time.sleep(1)

    return (
        "รับทราบครับ! สามารถตรวจสอบรูปจริงและรายละเอียดแปลงทั้งหมดได้ที่ Web Catalog https://assets.siwasup.com/catalog.html ได้เลยครับ",
        [p.get('code') for p in matched_props],
        search_mode,
        matched_props
    )



def find_property_by_id_or_code(pid):
    pid_clean = str(pid).strip().lower()
    for p in SIWASUP_PROPS:
        if str(p.get("id", "")).strip().lower() == pid_clean or str(p.get("code", "")).strip().lower() == pid_clean:
            return p
    for p in CATALOG:
        if str(p.get("c", "")).strip().lower() == pid_clean:
            return {
                "id": p.get("c"),
                "code": p.get("c"),
                "title": f"ทรัพย์ NPA {p.get('b', '')}: {p.get('tn', 'บ้าน')} โซน {p.get('d', '')}",
                "category": p.get("tn", "บ้าน"),
                "bank_source": p.get("b", "NPA"),
                "price": _format_prop_price_text(p.get('pr')),
                "location": f"{p.get('d', '')} • {p.get('p', 'กทม.')}",
                "size": f"{p.get('sqw', '')} ตร.ว." if p.get('sqw') else "",
                "usable_area": f"{p.get('sqm', '')} ตร.ม." if p.get('sqm') else "",
                "main_image": p.get("img") or "https://assets.siwasup.com/fallback_property.jpg"
            }
    return None


# ==============================================================================
# DEED OCR — รับรูปโฉนดจาก LINE → Gemini Vision → Flex Card + LandsMaps link
# ==============================================================================

def download_line_image(message_id: str) -> bytes | None:
    """ดึงไบนารีรูปภาพจาก LINE Content API"""
    url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"},
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception as e:
        print(f"[LINE Image DL Error]: {e}")
        return None


def _build_deeplink_token(province: str, amphur: str, deed_no: str) -> str | None:
    """Base64(ProvinceCode,AmphurCode,DeedNo) ตาม LandsMaps spec"""
    pcode = _GEO_LOOKUP_PROV.get(province, "")
    acode = _GEO_LOOKUP_AMP.get(f"{province}:{amphur}", "")
    if not pcode or not acode or not deed_no:
        return None
    raw = f"{pcode},{acode},{deed_no}"
    return base64.b64encode(raw.encode("utf-8")).decode("utf-8")


DEED_OCR_PROMPT = """คุณเป็นระบบ OCR อ่านหน้าโฉนดที่ดินของไทย (น.ส.4 / โฉนดที่ดิน / น.ส.3ก)
ให้ค้นหาและคืนค่าต่อไปนี้ ในรูปแบบ JSON เท่านั้น ไม่มีข้อความนำ ไม่มี markdown:
{
  "province": "ชื่อจังหวัดภาษาไทย เช่น กรุงเทพมหานคร",
  "amphur": "ชื่ออำเภอ/เขต ภาษาไทย เช่น เมืองกระบี่",
  "deed_no": "เลขที่โฉนด ตัวเลขล้วน เช่น 52696",
  "land_area_sqw": "เนื้อที่เป็นตารางวา เช่น 32.5 (ตัวเลขล้วน)",
  "parcel_no": "เลขที่ดิน ถ้ามี",
  "confidence": "high|medium|low"
}
ถ้าอ่านค่าไหนไม่ได้ให้ใส่ "" สำหรับ string หรือ null สำหรับตัวเลข
ห้ามเดาหรือแต่งข้อมูล"""


def ocr_deed_with_gemini(image_bytes: bytes) -> dict:
    """
    ส่งรูปไปยัง Gemini Vision API แล้วรับ JSON ข้อมูลโฉนด
    คืน dict พร้อม key: province, amphur, deed_no, land_area_sqw, parcel_no, confidence
    """
    if not GEMINI_API_KEY:
        return {}

    img_b64 = base64.b64encode(image_bytes).decode("utf-8")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"text": DEED_OCR_PROMPT},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_b64
                    }
                }
            ]
        }],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 256
        }
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
                .strip()
            )
            # strip markdown fences ถ้า Gemini ใส่มา
            raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
            raw_text = re.sub(r"\s*```$", "", raw_text)
            return json.loads(raw_text)
    except Exception as e:
        print(f"[Deed OCR Error]: {e}")
        return {}


ZONING_EMOJI = {
    "ย.1": "🟡 ที่อยู่อาศัยหนาแน่นน้อย",
    "ย.2": "🟡 ที่อยู่อาศัยหนาแน่นปานกลาง",
    "ย.3": "🟡 ที่อยู่อาศัยหนาแน่นมาก",
    "ย.4": "🟡 ที่อยู่อาศัยหนาแน่นมากพิเศษ",
    "พ.1": "🟠 พาณิชยกรรม",
    "พ.2": "🟠 พาณิชยกรรม",
    "พ.3": "🟠 พาณิชยกรรมหนาแน่น",
    "อ.1": "🔵 อุตสาหกรรม รง.4 ✅",
    "อ.2": "🔵 อุตสาหกรรม รง.4 ✅",
    "อ.3": "🔴 อุตสาหกรรมรวม",
    "ก.1": "🟢 เกษตรกรรม",
    "ก.2": "🟢 ชนบทและเกษตรกรรม",
    "ก.3": "🟢 อนุรักษ์ชนบท/เกษตรกรรม",
}


def build_deed_flex_card(ocr: dict, deeplink_url: str, qr_token: str) -> dict:
    """สร้าง LINE Flex Message Bubble สำหรับผลวิเคราะห์โฉนด"""
    province   = ocr.get("province", "") or "—"
    amphur     = ocr.get("amphur", "")   or "—"
    deed_no    = ocr.get("deed_no", "")  or "—"
    area_sqw   = ocr.get("land_area_sqw", "") or "—"
    confidence = ocr.get("confidence", "low")
    parcel_no  = ocr.get("parcel_no", "")

    conf_color = {"high": "#10B981", "medium": "#F59E0B", "low": "#EF4444"}.get(confidence, "#6B7280")
    conf_label = {"high": "✅ อ่านชัด", "medium": "⚠️ ตรวจสอบด้วย", "low": "❌ ภาพไม่ชัด"}.get(confidence, "?")

    area_rai   = ""
    try:
        sqw = float(str(area_sqw).replace(",", ""))
        rai  = int(sqw // 400)
        ngan = int((sqw % 400) // 100)
        rem  = round(sqw % 100, 1)
        area_rai = f"{rai} ไร่ {ngan} งาน {rem} วา"
    except Exception:
        pass

    contents = [
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "📍 จังหวัด", "size": "xs", "color": "#94A3B8", "flex": 3},
                {"type": "text", "text": province, "size": "xs", "color": "#F8FAFC", "weight": "bold", "flex": 5, "align": "end"}
            ]
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "🏘️ อำเภอ/เขต", "size": "xs", "color": "#94A3B8", "flex": 3},
                {"type": "text", "text": amphur, "size": "xs", "color": "#F8FAFC", "weight": "bold", "flex": 5, "align": "end"}
            ]
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "📄 เลขโฉนด", "size": "xs", "color": "#94A3B8", "flex": 3},
                {"type": "text", "text": deed_no, "size": "xs", "color": "#34D399", "weight": "bold", "flex": 5, "align": "end"}
            ]
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "📐 เนื้อที่", "size": "xs", "color": "#94A3B8", "flex": 3},
                {
                    "type": "text",
                    "text": f"{area_sqw} ตร.ว.{(' ≈ ' + area_rai) if area_rai else ''}",
                    "size": "xs",
                    "color": "#F8FAFC",
                    "flex": 5,
                    "align": "end",
                    "wrap": True
                }
            ]
        },
        {
            "type": "separator",
            "margin": "sm",
            "color": "#1E293B"
        },
        {
            "type": "box",
            "layout": "horizontal",
            "margin": "sm",
            "contents": [
                {"type": "text", "text": "ความแม่นยำ OCR", "size": "xxs", "color": "#64748B", "flex": 4},
                {"type": "text", "text": conf_label, "size": "xxs", "color": conf_color, "weight": "bold", "flex": 4, "align": "end"}
            ]
        },
    ]

    if parcel_no:
        contents.insert(3, {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": "🔢 เลขที่ดิน", "size": "xs", "color": "#94A3B8", "flex": 3},
                {"type": "text", "text": parcel_no, "size": "xs", "color": "#F8FAFC", "flex": 5, "align": "end"}
            ]
        })

    footer_buttons = []
    if deeplink_url:
        footer_buttons.append({
            "type": "button",
            "style": "primary",
            "color": "#059669",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": "🗺️ เปิดแผนที่โฉนด LandsMaps",
                "uri": deeplink_url
            }
        })

    share_text = f"โฉนดที่ดิน {province} อ.{amphur} เลขที่ {deed_no}\n📐 เนื้อที่ {area_sqw} ตร.ว.\n🗺️ ดูแผนที่: {deeplink_url or 'N/A'}"
    footer_buttons.append({
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
            "type": "uri",
            "label": "📋 เช็กรายละเอียดเพิ่ม",
            "uri": f"https://assets.siwasup.com/landmap_share.html"
        }
    })

    return {
        "type": "flex",
        "altText": f"📄 โฉนดที่ดิน {province} อ.{amphur} เลขที่ {deed_no} | {area_sqw} ตร.ว.",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "14px",
                "backgroundColor": "#0F172A",
                "contents": [
                    {
                        "type": "text",
                        "text": "📑 ผลวิเคราะห์โฉนดที่ดิน",
                        "size": "sm",
                        "weight": "bold",
                        "color": "#34D399"
                    },
                    {
                        "type": "text",
                        "text": "LandsMaps • กรมที่ดิน • ศิวาทรัพย์ AI",
                        "size": "xxs",
                        "color": "#64748B",
                        "margin": "xs"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "paddingAll": "14px",
                "backgroundColor": "#1E293B",
                "contents": contents
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "paddingAll": "12px",
                "paddingTop": "0px",
                "backgroundColor": "#1E293B",
                "contents": footer_buttons
            }
        }
    }



def parse_deed_text_query(text: str) -> dict | None:
    """
    ตรวจจับและสกัดข้อมูลโฉนดจากข้อความพิมพ์ของผู้ใช้ (ท่าที่ 2: พิมพ์ข้อความ)
    คืนค่า dict: {'deed_no': ..., 'province': ..., 'amphur': ...} หรือ None ถ้าไม่ใช่การค้นหาโฉนด
    """
    if not text:
        return None
    text_clean = text.strip()

    # คำหลักที่บ่งบอกว่าต้องการเช็คหรือค้นหาโฉนด
    has_deed_kw = any(k in text_clean for k in ['โฉนด', 'แปลงที่ดิน', 'รูปแปลง', 'เช็คที่ดิน', 'เลขที่ดิน'])

    # ค้นหาตัวเลข 3-8 หลัก
    num_match = re.search(r'(?:โฉนด(?:\s*เลขที่)?\s*)?(\b\d{3,8}\b)', text_clean)
    deed_no = num_match.group(1) if num_match else ''

    if not has_deed_kw and not (deed_no and len(deed_no) >= 4 and any(p in text_clean for p in _GEO_LOOKUP_PROV)):
        return None

    # สกัดจังหวัด
    matched_prov = ''
    for p in sorted(_GEO_LOOKUP_PROV.keys(), key=len, reverse=True):
        if p in text_clean:
            matched_prov = p
            break

    # สกัดอำเภอ
    matched_amp = ''
    if matched_prov:
        for k in _GEO_LOOKUP_AMP.keys():
            if k.startswith(f"{matched_prov}:"):
                amp_name = k.split(":", 1)[1]
                amp_clean = amp_name.replace("อำเภอ", "").replace("เขต", "").replace("อ.", "").strip()
                if amp_clean in text_clean or (amp_clean.startswith("เมือง") and ("เมือง" in text_clean or "อ.เมือง" in text_clean)):
                    matched_amp = amp_name
                    break
    else:
        # กรณีไม่ได้พิมพ์ชื่อจังหวัดตรงๆ ลองหาจากชื่ออำเภอ
        for k in _GEO_LOOKUP_AMP.keys():
            prov_name, amp_name = k.split(":", 1)
            amp_clean = amp_name.replace("อำเภอ", "").replace("เขต", "").replace("อ.", "").strip()
            if len(amp_clean) >= 3 and amp_clean in text_clean:
                matched_prov = prov_name
                matched_amp = amp_name
                break

    return {
        "deed_no": deed_no,
        "province": matched_prov,
        "amphur": matched_amp
    }


def handle_deed_image(message_id: str, reply_token: str, user_id: str, user_name: str):
    """
    Main pipeline: LINE image → download → Gemini OCR → LandsMaps deeplink → Flex reply
    รันบน background thread เพื่อไม่ให้ block webhook response
    """
    t0 = time.time()
    # 1. ตอบรับทันทีว่ากำลังอ่าน
    quick_reply_text = f"⏳ กำลังอ่านโฉนด AI อยู่ครับ คุณ{user_name}... รอแป๊บเดียวนะครับ! 🔍"
    reply_line(reply_token, quick_reply_text)

    # 2. Download รูปจาก LINE
    image_bytes = download_line_image(message_id)
    if not image_bytes:
        return  # reply token หมดอายุแล้วถ้าถึงจุดนี้ ไม่มีทางส่งซ้ำได้

    # 3. OCR ด้วย Gemini Vision
    ocr = ocr_deed_with_gemini(image_bytes)

    if not ocr or not ocr.get("deed_no"):
        # รูปอ่านไม่ออก — push ข้อความแนะนำแทน
        _push_line_message(
            user_id,
            "ขออภัยครับ น้องศิวาอ่านโฉนดจากรูปนี้ไม่ชัดเจนครับ 🙏\n"
            "ลองถ่ายรูปใหม่ให้:\n"
            "• ภาพคมชัด ไม่เบลอ\n"
            "• เห็นเลขโฉนด จังหวัด และอำเภอครบ\n"
            "• ถ่ายตรง ไม่เอียง\n\n"
            "หรือกรอกเองที่ 👉 https://assets.siwasup.com/landmap_share.html"
        )
        return

    # 4. สร้าง LandsMaps deeplink token
    province = ocr.get("province", "")
    amphur   = ocr.get("amphur", "")
    deed_no  = ocr.get("deed_no", "")
    qr_token    = _build_deeplink_token(province, amphur, deed_no)
    deeplink_url = (
        f"https://landsmaps.dol.go.th/?qrcodeToken={qr_token}"
        if qr_token else ""
    )

    # 5. สร้าง Flex Card
    flex_card = build_deed_flex_card(ocr, deeplink_url, qr_token or "")

    # 6. Push Flex Card (reply token หมดอายุแล้วตอนนี้ ต้องใช้ push API)
    latency_ms = int((time.time() - t0) * 1000)
    print(f"[Deed OCR Done] {province} อ.{amphur} โฉนด#{deed_no} | {latency_ms}ms | token={'ok' if qr_token else 'no_geo'}")

    # Push flex ผ่าน push API (reply token หมดอายุหลังจาก quick reply แรก)
    _push_flex_message_raw(flex_card, user_id)
    append_chat_log({
        "id": f"LOG_{int(time.time()*1000)}",
        "timestamp": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_name": user_name,
        "user_pic": "",
        "user_id_tail": "deed_ocr",
        "event_type": "deed_ocr",
        "user_text": f"[รูปโฉนด] {province} อ.{amphur} เลขที่ {deed_no}",
        "ai_reply": f"Flex Card: {province} อ.{amphur} #{deed_no} | {ocr.get('land_area_sqw','')} ตร.ว.",
        "matched_codes": [],
        "search_mode": "DEED_OCR",
        "latency_ms": latency_ms
    })


def strip_line_markdown(text: str) -> str:
    """Remove Markdown bold/code tokens (** / __ / `) that LINE Text messages render literally."""
    if not text:
        return text
    cleaned = str(text)
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned, flags=re.DOTALL)
    cleaned = cleaned.replace("**", "")
    cleaned = re.sub(r"__(.*?)__", r"\1", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    cleaned = re.sub(r"(?m)^\s*#{1,6}\s+", "", cleaned)
    return cleaned


def _push_line_message(user_id: str, text: str):
    """Push ข้อความ text ไปยัง user โดยตรง (ไม่ใช้ reply token)"""
    url = "https://api.line.me/v2/bot/message/push"
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": strip_line_markdown(text)}]
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[LINE Push OK]: {resp.status}")
    except Exception as e:
        print(f"[LINE Push Error]: {e}")


def _push_flex_message_raw(flex_msg: dict, user_id: str):
    """Push Flex message ไปยัง user_id โดยตรง"""
    url = "https://api.line.me/v2/bot/message/push"
    payload = {
        "to": user_id,
        "messages": [flex_msg]
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[LINE Push Flex OK]: {resp.status}")
    except Exception as e:
        print(f"[LINE Push Flex Error]: {e}")


def _mask_client_prop_code(raw_id: str) -> str:
    return re.sub(r"^(?:ALPHA|KTB|KBANK|BAM|PAMCO|SAM|SCB|TTB|GSB|GHB|BBL)[-_]", "SW-", str(raw_id or "").strip(), flags=re.IGNORECASE)


def build_property_flex_bubble(prop, client_name="คุณลูกค้า", agent_ref="SW000"):
    pid = str(prop.get("id") or prop.get("code") or "")
    masked_pid = _mask_client_prop_code(pid)
    title = str(prop.get("title") or "ทรัพย์คัดสรรพิเศษ ศิวาทรัพย์")
    price = _format_prop_price_text(prop.get("price"))
    category = str(prop.get("category") or "อสังหาริมทรัพย์")
    location = str(prop.get("location") or "กรุงเทพมหานครและปริมณฑล")
    size_str = str(prop.get("size") or prop.get("usable_area") or "")
    
    img_url = prop.get("main_image") or "https://assets.siwasup.com/fallback_property.jpg"
    if not img_url.startswith("http"):
        img_url = "https://assets.siwasup.com/fallback_property.jpg"

    detail_url = f"https://assets.siwasup.com/catalog.html?id={masked_pid}&property={masked_pid}&ref={agent_ref}&view=client&src=flex_carousel#prop-{masked_pid}"

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "hero": {
            "type": "image",
            "url": img_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": detail_url
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "paddingAll": "14px",
            "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"รหัส {masked_pid}",
                            "size": "xxs",
                            "color": "#8C734B",
                            "weight": "bold",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": category,
                            "size": "xxs",
                            "color": "#666666",
                            "align": "end"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "sm",
                    "wrap": True,
                    "maxLines": 2,
                    "color": "#1D1D1D"
                },
                {
                    "type": "text",
                    "text": price,
                    "weight": "bold",
                    "size": "md",
                    "color": "#8B0000"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "xs",
                    "margin": "xs",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"📍 {location}",
                            "size": "xxs",
                            "color": "#777777",
                            "maxLines": 1,
                            "wrap": True
                        }
                    ] + ([{
                        "type": "text",
                        "text": f"📐 ขนาด: {size_str}",
                        "size": "xxs",
                        "color": "#777777"
                    }] if size_str else [])
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "paddingAll": "12px",
            "paddingTop": "0px",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#1D1D1D",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "ดูรูปจริง & สเปกเต็ม",
                        "uri": detail_url
                    }
                }
            ]
        }
    }
    return bubble


def build_property_flex_carousel(props, client_name="คุณลูกค้า", agent_ref="SW000", view_all_url=""):
    max_items = 9 if view_all_url else 10
    bubbles = [build_property_flex_bubble(p, client_name, agent_ref) for p in props[:max_items] if p]
    if not bubbles:
        return None
    if view_all_url and len(bubbles) < 10:
        bubbles.append({
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "justifyContent": "center",
                "alignItems": "center",
                "spacing": "md",
                "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": "🔎 ดูทรัพย์ทั้งหมดที่ตรงเงื่อนไข", "weight": "bold", "size": "md", "color": "#111111", "wrap": True, "align": "center"},
                    {"type": "text", "text": "เปิดหน้าเว็บ Catalog แบบกรองให้แล้ว พร้อมรูปภาพและแผนที่ครบทุกหลัง", "size": "xs", "color": "#666666", "wrap": True, "align": "center"},
                    {"type": "button", "style": "primary", "color": "#990000", "action": {"type": "uri", "label": "ดูทั้งหมดบน Catalog", "uri": view_all_url}}
                ]
            }
        })
    return {
        "type": "flex",
        "altText": f"🏠 คัดสรรทรัพย์พิเศษ {len(props[:max_items])} หลัง สำหรับ {client_name} (ศิวาทรัพย์ Co-Broker)",
        "contents": {
            "type": "carousel",
            "contents": bubbles
        }
    }

def reply_line(reply_token, reply_text, flex_message=None):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    messages = [
        {
            "type": "text",
            "text": strip_line_markdown(reply_text)
        }
    ]
    if flex_message and isinstance(flex_message, dict) and flex_message.get("type") == "flex":
        messages.append(flex_message)

    payload = {
        "replyToken": reply_token,
        "messages": messages[:5]
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[LINE Reply OK]: Status {resp.status}")
            return True
    except Exception as e:
        print(f"[LINE Reply Error]: {e}")
        return False


LOBBY_PATH = os.path.join(DATA_DIR, "lobby_applicants.json")
LOBBY_LOCK = threading.Lock()

_R2_LOBBY_VAULT_KEY = "_vault/lobby_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_lobby_vault_v2", hashlib.sha256).hexdigest()[:32] + ".json"
_R2_LOBBY_SNAP_PREFIX = hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_lobby_snap_v1", hashlib.sha256).hexdigest()[:24]
_R2_LOBBY_SNAP_INDEX_KEY = f"_vault/lobby_snap_idx_{_R2_LOBBY_SNAP_PREFIX}.json"
_R2_LOBBY_RESTORED = False
_R2_LOBBY_SNAP_LOCK = threading.Lock()

def _fetch_r2_json(key, timeout=12):
    url = f"https://assets.siwasup.com/{key}?t={int(time.time())}"
    req = urllib.request.Request(url, headers={"User-Agent": "SiwasupRenderVault/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if r.status == 200:
            return json.loads(r.read().decode("utf-8"))
    return None

def _ensure_approved_member_codes(store: dict) -> bool:
    """Backfill missing SA/SW codes on approved members (e.g. SA001 Bua, SA002 Lily, SA004+ staff)."""
    if not isinstance(store, dict):
        return False
    changed = False
    for m in store.get("approved", []):
        if str(m.get("code") or "").strip():
            continue
        mid = str(m.get("id") or "").strip()
        phone = re.sub(r'\D', '', str(m.get("phone") or ""))
        name_low = str(m.get("name") or "").lower()
        if mid == "app_office_004":
            m["code"] = "SA000"
            changed = True
        elif mid == "app_office_001":
            m["code"] = "SW001"
            changed = True
        elif mid == "SW-APP-252" or phone == "0853365703" or "ภมรมาศ" in name_low:
            m["code"] = "SA001"
            changed = True
        elif mid == "SW-APP-866" or phone == "0925836565" or "ลิลลี่" in str(m.get("nickname") or ""):
            m["code"] = "SA002"
            changed = True
        else:
            perms = m.get("permissions") or {}
            is_staff = (
                m.get("affiliation") == "office"
                or any(bool(perms.get(k)) for k in ("standardAdmin", "keyboxAdmin", "executiveAuthority", "systemAdmin", "catalogCurator"))
            )
            m["code"] = _next_admin_sa_code(store) if is_staff else _next_agent_sw_code(store)
            changed = True
    return changed


def load_lobby_data():
    global _R2_LOBBY_RESTORED
    if not _R2_LOBBY_RESTORED and os.environ.get("PORT"):
        for r2_key in (_R2_LOBBY_VAULT_KEY, "data/lobby_applicants.json"):
            try:
                cloud_store = _fetch_r2_json(r2_key, timeout=12)
                if isinstance(cloud_store, dict) and ("approved" in cloud_store or "pending" in cloud_store):
                    backfilled = _ensure_approved_member_codes(cloud_store)
                    with open(LOBBY_PATH, "w", encoding="utf-8") as f:
                        json.dump(cloud_store, f, ensure_ascii=False, indent=2)
                    _R2_LOBBY_RESTORED = True
                    if backfilled:
                        try:
                            save_lobby_data(cloud_store, create_snapshot=False)
                        except Exception:
                            pass
                    print(f"[Vault] Restored lobby_applicants from R2 ({r2_key}: {len(cloud_store.get('approved', []))} approved, {len(cloud_store.get('pending', []))} pending)")
                    return cloud_store
            except Exception as e:
                print(f"[Vault] R2 restore attempt ({r2_key}) note: {e}")
    if os.path.exists(LOBBY_PATH):
        try:
            with open(LOBBY_PATH, "r", encoding="utf-8") as f:
                local_store = json.load(f)
            _ensure_approved_member_codes(local_store)
            return local_store
        except Exception as e:
            print(f"[Warn] Failed to read lobby_applicants.json: {e}")
    return {"updated_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"), "pending": [], "approved": []}

def _upload_lobby_snapshot_r2(snapshot_bytes, approved_cnt, pending_cnt, reason):
    if not put_object_r2:
        return
    with _R2_LOBBY_SNAP_LOCK:
        try:
            ts_id = bkk_now().strftime("%Y%m%d_%H%M%S")
            snap_key = f"_vault/lobby_snap_{_R2_LOBBY_SNAP_PREFIX}_{ts_id}.json"
            put_object_r2(snap_key, snapshot_bytes, "application/json")
            idx_list = []
            try:
                cur = _fetch_r2_json(_R2_LOBBY_SNAP_INDEX_KEY, timeout=8)
                if isinstance(cur, list):
                    idx_list = cur
            except Exception:
                pass
            idx_list.insert(0, {
                "key": snap_key,
                "ts": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
                "reason": reason or "auto",
                "approved": approved_cnt,
                "pending": pending_cnt,
            })
            # Deduplicate by key and keep latest 30 snapshots
            seen = set()
            deduped = []
            for item in idx_list:
                k = item.get("key")
                if k and k not in seen:
                    seen.add(k)
                    deduped.append(item)
                if len(deduped) >= 30:
                    break
            put_object_r2(_R2_LOBBY_SNAP_INDEX_KEY, json.dumps(deduped, ensure_ascii=False, indent=2).encode("utf-8"), "application/json")
        except Exception as _se:
            print(f"[R2 Snapshot Warn]: {_se}")

def save_lobby_data(store, allow_truncate=False, create_snapshot=False, snapshot_reason=""):
    with LOBBY_LOCK:
        # Zero-Day Anti-Downgrade Safeguard: Prevent accidental roster truncation/wipeout
        if not allow_truncate and os.path.exists(LOBBY_PATH):
            try:
                with open(LOBBY_PATH, "r", encoding="utf-8") as _chk_f:
                    _existing = json.load(_chk_f)
                    _existing_count = len(_existing.get("approved", []))
                    _new_count = len(store.get("approved", []))
                    if (_existing_count > 3 and _new_count <= 1) or (_existing_count >= 2 and _new_count < _existing_count):
                        print(f"[CRITICAL SAFEGUARD] Blocked attempted roster downgrade! Existing: {_existing_count}, Incoming: {_new_count}")
                        return
            except Exception as _chk_e:
                pass

        store["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            with open(LOBBY_PATH, "wb") as f:
                f.write(data_bytes)
        except Exception as e:
            print(f"[Error] Failed to save lobby local: {e}")
        # Never overwrite R2 from an un-restored Render worker unless explicitly forced
        if os.environ.get("PORT") and not _R2_LOBBY_RESTORED and not allow_truncate:
            print("[Vault] Skipped R2 lobby write because initial R2 restore has not succeeded yet.")
            return
        if put_object_r2:
            try:
                put_object_r2(_R2_LOBBY_VAULT_KEY, data_bytes, "application/json")
                put_object_r2("data/lobby_applicants.json", data_bytes, "application/json; charset=utf-8")
                if create_snapshot:
                    threading.Thread(
                        target=_upload_lobby_snapshot_r2,
                        args=(data_bytes, len(store.get("approved", [])), len(store.get("pending", [])), snapshot_reason),
                        daemon=True,
                    ).start()
            except Exception as e:
                print(f"[R2 Vault Sync Error]: {e}")


# ==============================================================================
# LINE LOGIN + SERVER-SIDE SESSIONS (replaces phone/PIN login)
# ==============================================================================
import secrets

SESSION_SECRET = (os.environ.get("SESSION_SECRET") or secrets.token_hex(32)).encode()
LINE_LOGIN_CHANNEL_ID = os.environ.get("LINE_LOGIN_CHANNEL_ID", "")
LINE_LOGIN_CHANNEL_SECRET = os.environ.get("LINE_LOGIN_CHANNEL_SECRET", "")
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "https://siwasup-cobroker-os.onrender.com").rstrip("/")
SUPER_ADMIN_LINE_USER_IDS = {x.strip() for x in os.environ.get("SUPER_ADMIN_LINE_USER_IDS", "").split(",") if x.strip()}
FRONTEND_URLS = {
    "register": "https://assets.siwasup.com/agent_registration.html",
    "login": "https://assets.siwasup.com/agent_registration.html?mode=login",
    "admin": "https://assets.siwasup.com/admin_lobby_manager.html",
    "exec": "https://assets.siwasup.com/gool_executive_dashboard.html",
    "consignment": "https://assets.siwasup.com/admin_consignment.html",
    "contracts": "https://assets.siwasup.com/exclusive_contracts.html",
    "content": "https://assets.siwasup.com/admin_content_hub.html",
    "catalog": "https://assets.siwasup.com/catalog.html",
    "seller": "https://assets.siwasup.com/catalog.html?view=seller",
}
ADMIN_PERM_KEYS = ("standardAdmin", "executiveAuthority", "keyboxAdmin", "systemAdmin")
SESSION_TTL = 12 * 3600


def _b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _b64u_dec(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def make_token(payload, ttl):
    body = dict(payload)
    body["exp"] = int(time.time()) + ttl
    raw = _b64u(json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    sig = _b64u(hmac.new(SESSION_SECRET, raw.encode(), hashlib.sha256).digest())
    return raw + "." + sig


def verify_token(tok):
    try:
        raw, sig = tok.split(".", 1)
        expect = _b64u(hmac.new(SESSION_SECRET, raw.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expect):
            return None
        body = json.loads(_b64u_dec(raw).decode("utf-8"))
        if body.get("exp", 0) < time.time():
            return None
        return body
    except Exception:
        return None


def is_super_tech_root(m):
    if not isinstance(m, dict):
        return False
    if m.get("id") == "app_office_004" or m.get("is_tech"):
        return True
    uid = m.get("lineUserId")
    if uid and uid in SUPER_ADMIN_LINE_USER_IDS:
        return True
    return False


def ensure_super_tech_seat(store, uid, name="", picture=""):
    """Self-healing guarantee: SUPER_ADMIN_LINE_USER_IDS always has an active full-power seat."""
    if not uid or uid not in SUPER_ADMIN_LINE_USER_IDS:
        return False
    changed = False
    seat = next((a for a in store.get("approved", []) if a.get("lineUserId") == uid or a.get("id") == "app_office_004"), None)
    if not seat:
        seat = {
            "id": "app_office_004",
            "code": "SA000",
            "name": "[NASSTY]",
            "nickname": "NASSTY",
            "phone": "0815555555",
            "line_id": "nassty_ton",
            "zone": "สำนักงานใหญ่",
            "role": "💻 Tech Architect & Senior Advisor",
            "title": "Senior Technology Architect",
            "role_code": "TECH_ARCHITECT",
            "status": "approved",
            "avatar": picture or "https://sprofile.line-scdn.net/0h28p75zAZbRddTkF0fXETaC0ebn1-PzQFdX8neWkaMS9gfH9EcnhweTtIMyc0d3gWdyAkImxOMXNRXRpxQxiRI1p-MCZgfSlGdSAj8g",
            "lineUserId": uid,
            "badges": ["⚙️ Technical Admin", "💰 เคาะราคา", "🛡️ Standard Admin"],
            "permissions": {
                "standardAdmin": True,
                "editPrice": True,
                "keyboxAdmin": True,
                "leadInspector": True,
                "executiveAuthority": True,
                "catalogCurator": True,
                "systemAdmin": True,
            },
            "is_tech": True,
            "approved_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        store.setdefault("approved", []).insert(0, seat)
        changed = True
    else:
        if seat.get("code") != "SA000":
            seat["code"] = "SA000"
            changed = True
        if seat.get("name") != "[NASSTY]":
            seat["name"] = "[NASSTY]"
            changed = True
        if seat.get("nickname") != "NASSTY":
            seat["nickname"] = "NASSTY"
            changed = True
        if seat.get("lineUserId") != uid:
            seat["lineUserId"] = uid
            changed = True
        perms = seat.setdefault("permissions", {})
        for k in ("standardAdmin", "executiveAuthority", "systemAdmin"):
            if not perms.get(k):
                perms[k] = True
                changed = True
        seat["is_tech"] = True
    if changed:
        save_lobby_data(store)
    return changed

def is_admin_member(m):
    perms = m.get("permissions") or {}
    return any(perms.get(k) for k in ADMIN_PERM_KEYS)


def sanitize_member(m):
    """Never expose legacy PINs or raw LINE user ids to clients."""
    if not isinstance(m, dict):
        return m
    out = {k: v for k, v in m.items() if k not in ("pin", "lineUserId")}
    out["lineLinked"] = bool(m.get("lineUserId"))
    return out


def sanitize_store_for_admin(store):
    out = dict(store)
    out["approved"] = [sanitize_member(a) for a in store.get("approved", [])]
    out["pending"] = [sanitize_member(a) for a in store.get("pending", [])]
    hist = []
    for rb in store.get("rollback_history", []):
        rb2 = dict(rb)
        if isinstance(rb2.get("member"), dict):
            rb2["member"] = sanitize_member(rb2["member"])
        hist.append(rb2)
    out["rollback_history"] = hist
    return out


def _http_post_form(url, data):
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(data).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))



CONTRACTS_PATH = os.path.join(DATA_DIR, "exclusive_contracts.json")
CONTRACTS_LOCK = threading.RLock()
_R2_CONTRACTS_VAULT_KEY = "_vault/contracts_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_contracts_vault_v1", hashlib.sha256).hexdigest()[:32] + ".json"

def load_contracts_data():
    if os.path.exists(CONTRACTS_PATH):
        try:
            with open(CONTRACTS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warn] Failed to read exclusive_contracts.json: {e}")
    return {"updated_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"), "contracts": []}

def save_contracts_data(store):
    with CONTRACTS_LOCK:
        store["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            with open(CONTRACTS_PATH, "wb") as f:
                f.write(data_bytes)
        except Exception as e:
            print(f"[Error] Failed to save contracts local: {e}")
        if put_object_r2 and os.environ.get("PORT"):
            threading.Thread(target=lambda: put_object_r2(_R2_CONTRACTS_VAULT_KEY, data_bytes, "application/json"), daemon=True).start()


# ==============================================================================
# LISTING INTAKE VAULT (Phase 1: Consignment & Digital Contract Intake)
# ==============================================================================
LISTING_INTAKE_PATH = os.path.join(DATA_DIR, "listing_intake.json")
LISTING_INTAKE_LOCK = threading.RLock()
_R2_INTAKE_VAULT_KEY = "_vault/listing_intake_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_listing_intake_vault_v1", hashlib.sha256).hexdigest()[:32] + ".json"
_R2_INTAKE_RESTORED = False
_INTAKE_MEM_CACHE = None
_R2_INTAKE_UPLOAD_LOCK = threading.Lock()
_LATEST_INTAKE_BYTES = None
_INTAKE_IP_WINDOW = {}
_INTAKE_RATE_LOCK = threading.Lock()


def _default_intake_store():
    return {
        "updated_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
        "intakes": [],
    }


def _check_intake_ip_rate(client_ip: str) -> bool:
    if not client_ip:
        return True
    now = time.time()
    with _INTAKE_RATE_LOCK:
        cutoff = now - 600.0
        recent = [ts for ts in _INTAKE_IP_WINDOW.get(client_ip, []) if ts > cutoff]
        if len(recent) >= 6:
            _INTAKE_IP_WINDOW[client_ip] = recent
            return False
        recent.append(now)
        _INTAKE_IP_WINDOW[client_ip] = recent
        return True


def load_intake_data():
    global _R2_INTAKE_RESTORED, _INTAKE_MEM_CACHE
    with LISTING_INTAKE_LOCK:
        if not _R2_INTAKE_RESTORED and os.environ.get("PORT"):
            try:
                url = f"https://assets.siwasup.com/{_R2_INTAKE_VAULT_KEY}?t={int(time.time())}"
                req = urllib.request.Request(url, headers={"User-Agent": "SiwasupRenderVault/1.0"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    if r.status == 200:
                        cloud_store = json.loads(r.read().decode("utf-8"))
                        if isinstance(cloud_store, dict) and isinstance(cloud_store.get("intakes"), list):
                            os.makedirs(os.path.dirname(LISTING_INTAKE_PATH), exist_ok=True)
                            tmp_path = LISTING_INTAKE_PATH + ".tmp"
                            with open(tmp_path, "w", encoding="utf-8") as f:
                                json.dump(cloud_store, f, ensure_ascii=False, indent=2)
                            os.replace(tmp_path, LISTING_INTAKE_PATH)
                            _INTAKE_MEM_CACHE = json.loads(json.dumps(cloud_store))
                            _R2_INTAKE_RESTORED = True
                            print(f"[Vault] Restored listing_intake from R2 ({len(cloud_store.get('intakes', []))} items)")
                            return cloud_store
            except urllib.error.HTTPError as he:
                if he.code == 404:
                    _R2_INTAKE_RESTORED = True
                print(f"[Vault] Listing intake initial R2 restore HTTP {he.code}")
            except Exception as e:
                print(f"[Vault] Listing intake initial R2 restore note (will retry): {e}")
        if os.path.exists(LISTING_INTAKE_PATH):
            try:
                with open(LISTING_INTAKE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and isinstance(data.get("intakes"), list):
                        _INTAKE_MEM_CACHE = json.loads(json.dumps(data))
                        return data
            except Exception as e:
                print(f"[Warn] Failed to read listing_intake.json: {e}")
        if _INTAKE_MEM_CACHE is not None:
            return json.loads(json.dumps(_INTAKE_MEM_CACHE))
        return _default_intake_store()


def _sequential_r2_intake_upload():
    global _LATEST_INTAKE_BYTES
    with _R2_INTAKE_UPLOAD_LOCK:
        with LISTING_INTAKE_LOCK:
            payload_bytes = _LATEST_INTAKE_BYTES
        if payload_bytes and put_object_r2:
            try:
                put_object_r2(_R2_INTAKE_VAULT_KEY, payload_bytes, "application/json; charset=utf-8")
            except Exception as e:
                print(f"[R2 Listing Intake Sync Warn]: {e}")


def save_intake_data(store):
    global _INTAKE_MEM_CACHE, _LATEST_INTAKE_BYTES
    with LISTING_INTAKE_LOCK:
        prev_count = len((_INTAKE_MEM_CACHE or {}).get("intakes", []))
        new_count = len(store.get("intakes", []))
        if prev_count > 3 and new_count == 0:
            print(f"[CRITICAL SAFEGUARD] Blocked attempted listing_intake wipeout! Existing: {prev_count}, Incoming: {new_count}")
            return
        store["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        _INTAKE_MEM_CACHE = json.loads(json.dumps(store))
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            os.makedirs(os.path.dirname(LISTING_INTAKE_PATH), exist_ok=True)
            tmp_path = LISTING_INTAKE_PATH + ".tmp"
            with open(tmp_path, "wb") as f:
                f.write(data_bytes)
            os.replace(tmp_path, LISTING_INTAKE_PATH)
        except Exception as e:
            print(f"[Error] Failed to save listing_intake local: {e}")
        if put_object_r2 and os.environ.get("PORT"):
            _LATEST_INTAKE_BYTES = data_bytes
            threading.Thread(target=_sequential_r2_intake_upload, daemon=True).start()


# ==============================================================================
# CONSIGNMENT DEMO VAULT (Shared Sandbox for Founders & Bua - Isolated from Catalog)
# ==============================================================================
CONSIGNMENT_DEMO_PATH = os.path.join(DATA_DIR, "consignment_demo_vault.json")
CONSIGNMENT_DEMO_LOCK = threading.RLock()
_R2_CONSIGNMENT_VAULT_KEY = "_vault/consignment_demo_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_consignment_demo_v1", hashlib.sha256).hexdigest()[:32] + ".json"
_R2_CONSIGNMENT_RESTORED = False
_CONSIGNMENT_MEM_CACHE = None
_R2_CONSIGNMENT_UPLOAD_LOCK = threading.Lock()
_LATEST_CONSIGNMENT_BYTES = None


def _is_consignment_founder(member: dict) -> bool:
    if not isinstance(member, dict):
        return False
    mid = str(member.get("id") or "").strip().lower()
    code = str(member.get("code") or "").strip().upper()
    if mid in ("app_office_001", "app_office_002", "app_office_004") or code in ("SW001", "SW002", "SA000", "SA001"):
        return True
    perms = member.get("permissions") or {}
    if bool(perms.get("executiveAuthority") or perms.get("systemAdmin") or member.get("is_leader")):
        return True
    return clean_phone_str(member.get("phone") or "") == "0853365703"


def _is_gool_approver(member: dict) -> bool:
    """Only Gool (SW001) or systemAdmin may approve new agent-submitted consignment properties."""
    if not isinstance(member, dict):
        return False
    mid = str(member.get("id") or "").strip().lower()
    code = str(member.get("code") or "").strip().upper()
    perms = member.get("permissions") or {}
    return mid == "app_office_001" or code == "SW001" or bool(perms.get("systemAdmin"))


_BUG_REPORT_LOCK = threading.RLock()
_R2_BUG_REPORTS_KEY = "_vault/bug_reports_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_bug_reports_v1", hashlib.sha256).hexdigest()[:32] + ".json"
_BUG_REPORTS_MEM = None


def _load_bug_reports() -> list:
    global _BUG_REPORTS_MEM
    with _BUG_REPORT_LOCK:
        if isinstance(_BUG_REPORTS_MEM, list):
            return _BUG_REPORTS_MEM
        try:
            data = _fetch_r2_json(_R2_BUG_REPORTS_KEY, timeout=8)
            if isinstance(data, list):
                _BUG_REPORTS_MEM = data
                return _BUG_REPORTS_MEM
        except Exception:
            pass
        _BUG_REPORTS_MEM = []
        return _BUG_REPORTS_MEM


def _save_bug_reports(items: list):
    global _BUG_REPORTS_MEM
    with _BUG_REPORT_LOCK:
        trimmed = list(items)[:200]
        _BUG_REPORTS_MEM = trimmed
        if put_object_r2 is not None:
            raw = json.dumps(trimmed, ensure_ascii=False).encode("utf-8")
            threading.Thread(target=put_object_r2, args=(_R2_BUG_REPORTS_KEY, raw, "application/json; charset=utf-8"), daemon=True).start()


_DAILY_STATS_LOCK = threading.RLock()
_R2_DAILY_STATS_KEY = "_vault/daily_active_stats_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_daily_stats_v1", hashlib.sha256).hexdigest()[:32] + ".json"
_DAILY_STATS_MEM = None
_DAILY_STATS_LAST_R2_TS = 0


def _load_daily_stats() -> dict:
    global _DAILY_STATS_MEM
    with _DAILY_STATS_LOCK:
        if isinstance(_DAILY_STATS_MEM, dict):
            return _DAILY_STATS_MEM
        try:
            data = _fetch_r2_json(_R2_DAILY_STATS_KEY, timeout=8)
            if isinstance(data, dict):
                _DAILY_STATS_MEM = data
                return _DAILY_STATS_MEM
        except Exception:
            pass
        _DAILY_STATS_MEM = {}
        return _DAILY_STATS_MEM


def _record_daily_active(mem: dict, store: dict):
    global _DAILY_STATS_LAST_R2_TS
    if not isinstance(mem, dict):
        return
    with _DAILY_STATS_LOCK:
        stats = _load_daily_stats()
        day_key = bkk_now().strftime("%Y-%m-%d")
        day_rec = stats.setdefault(day_key, {"unique_members": [], "total_hits": 0, "peak_online": 0})
        day_rec["total_hits"] = int(day_rec.get("total_hits") or 0) + 1
        label = f"{mem.get('nickname') or mem.get('name') or mem.get('code') or 'ทีมงาน'} ({mem.get('code') or '-'})"
        if label not in day_rec["unique_members"]:
            day_rec["unique_members"].append(label)
        now_ts = int(time.time())
        approved = (store or {}).get("approved") or []
        cur_online = sum(1 for a in approved if int(a.get("last_active_at") or 0) >= (now_ts - 300))
        if cur_online > int(day_rec.get("peak_online") or 0):
            day_rec["peak_online"] = cur_online
        # Keep only last 60 days
        keys_sorted = sorted(stats.keys(), reverse=True)
        for old_k in keys_sorted[60:]:
            stats.pop(old_k, None)
        # Debounce R2 upload (max once per 60s)
        if put_object_r2 is not None and (now_ts - _DAILY_STATS_LAST_R2_TS) >= 60:
            _DAILY_STATS_LAST_R2_TS = now_ts
            raw = json.dumps(stats, ensure_ascii=False).encode("utf-8")
            threading.Thread(target=put_object_r2, args=(_R2_DAILY_STATS_KEY, raw, "application/json; charset=utf-8"), daemon=True).start()


def _is_bua_publisher(member: dict) -> bool:
    """Only Bua (SA001) or systemAdmin may publish Sandbox consignment properties to Public."""
    if not isinstance(member, dict):
        return False
    mid = str(member.get("id") or "").strip().lower()
    code = str(member.get("code") or "").strip().upper()
    perms = member.get("permissions") or {}
    return (
        mid == "app_office_002"
        or code in ("SA001", "SW002")
        or clean_phone_str(member.get("phone") or "") == "0853365703"
        or bool(perms.get("systemAdmin"))
    )


def _consignment_role(member: dict) -> str:
    if _is_consignment_founder(member):
        return "founder"
    perms = (member or {}).get("permissions") or {}
    if bool(perms.get("standardAdmin") or perms.get("keyboxAdmin")):
        return "staff"
    return "agent"


def _is_consignment_owner(prop: dict, member: dict) -> bool:
    if not isinstance(prop, dict) or not isinstance(member, dict):
        return False
    mid = str(member.get("id") or "").strip().lower()
    code = str(member.get("code") or "").strip().upper()
    sub_id = str(prop.get("submitted_by_id") or "").strip().lower()
    sub_code = str(prop.get("submitted_by_code") or "").strip().upper()
    ass_code = str(prop.get("assigned_agent_code") or "").strip().upper()
    return (bool(mid) and sub_id == mid) or (bool(code) and (sub_code == code or ass_code == code))


def _is_contract_verified(prop: dict) -> bool:
    """Catalog Publish Guard: only verified non-expired properties may enter catalog."""
    if not isinstance(prop, dict):
        return False
    if str(prop.get("status") or "").strip() == "expired":
        return False
    if not bool(prop.get("contract_verified")):
        return False
    ctype = str(prop.get("consignment_type") or "open_contract").strip()
    if ctype == "no_contract":
        return True
    has_files = bool(prop.get("contract_files")) or bool(prop.get("linked_contract_id"))
    if not has_files:
        return False
    exp_str = str(prop.get("contract_expiry") or "").strip()
    if exp_str:
        try:
            exp_dt = datetime.strptime(exp_str[:10], "%Y-%m-%d").date()
            if exp_dt < bkk_now().date():
                return False
        except Exception:
            pass
    return True


def _default_consignment_store():
    seed_path = os.path.join(DATA_DIR, "consignment_seed_test.json")
    if os.path.exists(seed_path):
        try:
            with open(seed_path, "r", encoding="utf-8") as f:
                seed_data = json.load(f)
                if isinstance(seed_data, dict) and isinstance(seed_data.get("properties"), list):
                    return {
                        "updated_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_by": "seed_init",
                        "properties": seed_data["properties"],
                    }
        except Exception as e:
            print(f"[Consignment Seed Read Error]: {e}")
    return {
        "updated_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_by": "empty_init",
        "properties": [],
    }


def load_consignment_data():
    global _R2_CONSIGNMENT_RESTORED, _CONSIGNMENT_MEM_CACHE
    with CONSIGNMENT_DEMO_LOCK:
        if not _R2_CONSIGNMENT_RESTORED and os.environ.get("PORT"):
            try:
                url = f"https://assets.siwasup.com/{_R2_CONSIGNMENT_VAULT_KEY}?t={int(time.time())}"
                req = urllib.request.Request(url, headers={"User-Agent": "SiwasupRenderVault/1.0"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    if r.status == 200:
                        cloud_store = json.loads(r.read().decode("utf-8"))
                        if isinstance(cloud_store, dict) and isinstance(cloud_store.get("properties"), list):
                            os.makedirs(os.path.dirname(CONSIGNMENT_DEMO_PATH), exist_ok=True)
                            tmp_path = CONSIGNMENT_DEMO_PATH + ".tmp"
                            with open(tmp_path, "w", encoding="utf-8") as f:
                                json.dump(cloud_store, f, ensure_ascii=False, indent=2)
                            os.replace(tmp_path, CONSIGNMENT_DEMO_PATH)
                            _CONSIGNMENT_MEM_CACHE = json.loads(json.dumps(cloud_store))
                            _R2_CONSIGNMENT_RESTORED = True
                            print(f"[Vault] Restored consignment_demo from R2 ({len(cloud_store.get('properties', []))} items)")
                            return cloud_store
            except urllib.error.HTTPError as he:
                if he.code == 404:
                    _R2_CONSIGNMENT_RESTORED = True
                print(f"[Vault] Consignment demo initial R2 restore HTTP {he.code}")
            except Exception as e:
                print(f"[Vault] Consignment demo initial R2 restore note: {e}")
        if os.path.exists(CONSIGNMENT_DEMO_PATH):
            try:
                with open(CONSIGNMENT_DEMO_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and isinstance(data.get("properties"), list):
                        _CONSIGNMENT_MEM_CACHE = json.loads(json.dumps(data))
                        return data
            except Exception as e:
                print(f"[Warn] Failed to read consignment_demo_vault.json: {e}")
        if _CONSIGNMENT_MEM_CACHE is not None:
            return json.loads(json.dumps(_CONSIGNMENT_MEM_CACHE))
        seed = _default_consignment_store()
        _CONSIGNMENT_MEM_CACHE = json.loads(json.dumps(seed))
        return seed


def _sequential_r2_consignment_upload():
    global _LATEST_CONSIGNMENT_BYTES
    with _R2_CONSIGNMENT_UPLOAD_LOCK:
        with CONSIGNMENT_DEMO_LOCK:
            payload_bytes = _LATEST_CONSIGNMENT_BYTES
        if payload_bytes and put_object_r2:
            try:
                put_object_r2(_R2_CONSIGNMENT_VAULT_KEY, payload_bytes, "application/json; charset=utf-8")
            except Exception as e:
                print(f"[R2 Consignment Demo Sync Warn]: {e}")


def save_consignment_data(store):
    global _CONSIGNMENT_MEM_CACHE, _LATEST_CONSIGNMENT_BYTES
    with CONSIGNMENT_DEMO_LOCK:
        prev_count = len((_CONSIGNMENT_MEM_CACHE or {}).get("properties", []))
        new_count = len(store.get("properties", []))
        if prev_count > 3 and new_count == 0:
            print(f"[CRITICAL SAFEGUARD] Blocked attempted consignment_demo wipeout! Existing: {prev_count}, Incoming: {new_count}")
            return
        store["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        _CONSIGNMENT_MEM_CACHE = json.loads(json.dumps(store))
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            os.makedirs(os.path.dirname(CONSIGNMENT_DEMO_PATH), exist_ok=True)
            tmp_path = CONSIGNMENT_DEMO_PATH + ".tmp"
            with open(tmp_path, "wb") as f:
                f.write(data_bytes)
            os.replace(tmp_path, CONSIGNMENT_DEMO_PATH)
        except Exception as e:
            print(f"[Error] Failed to save consignment_demo local: {e}")
        if put_object_r2 and os.environ.get("PORT"):
            _LATEST_CONSIGNMENT_BYTES = data_bytes
            threading.Thread(target=_sequential_r2_consignment_upload, daemon=True).start()


# ==============================================================================
# SELLER (PROPERTY OWNER) AUTH VAULT — Isolated from Co-Broker Lobby
# ==============================================================================
SELLERS_PATH = os.path.join(DATA_DIR, "sellers_vault.json")
SELLERS_LOCK = threading.RLock()
_R2_SELLERS_VAULT_KEY = "_vault/sellers_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_sellers_vault_v1", hashlib.sha256).hexdigest()[:32] + ".json"
_R2_SELLERS_RESTORED = False
_SELLERS_MEM_CACHE = None


def load_sellers_data():
    global _R2_SELLERS_RESTORED, _SELLERS_MEM_CACHE
    with SELLERS_LOCK:
        if not _R2_SELLERS_RESTORED and os.environ.get("PORT"):
            try:
                url = f"https://assets.siwasup.com/{_R2_SELLERS_VAULT_KEY}?t={int(time.time())}"
                req = urllib.request.Request(url, headers={"User-Agent": "SiwasupRenderVault/1.0"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    if r.status == 200:
                        cloud_store = json.loads(r.read().decode("utf-8"))
                        if isinstance(cloud_store, dict) and isinstance(cloud_store.get("sellers"), list):
                            os.makedirs(os.path.dirname(SELLERS_PATH), exist_ok=True)
                            tmp_path = SELLERS_PATH + ".tmp"
                            with open(tmp_path, "w", encoding="utf-8") as f:
                                json.dump(cloud_store, f, ensure_ascii=False, indent=2)
                            os.replace(tmp_path, SELLERS_PATH)
                            _SELLERS_MEM_CACHE = json.loads(json.dumps(cloud_store))
                            _R2_SELLERS_RESTORED = True
                            return cloud_store
            except urllib.error.HTTPError as he:
                if he.code == 404:
                    _R2_SELLERS_RESTORED = True
            except Exception as e:
                print(f"[Vault] Sellers R2 restore note: {e}")
        if os.path.exists(SELLERS_PATH):
            try:
                with open(SELLERS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and isinstance(data.get("sellers"), list):
                        _SELLERS_MEM_CACHE = json.loads(json.dumps(data))
                        return data
            except Exception as e:
                print(f"[Warn] Failed to read sellers_vault.json: {e}")
        if _SELLERS_MEM_CACHE is not None:
            return json.loads(json.dumps(_SELLERS_MEM_CACHE))
        return {"updated_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"), "sellers": []}


def save_sellers_data(store):
    global _SELLERS_MEM_CACHE
    with SELLERS_LOCK:
        store["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        _SELLERS_MEM_CACHE = json.loads(json.dumps(store))
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            os.makedirs(os.path.dirname(SELLERS_PATH), exist_ok=True)
            tmp_path = SELLERS_PATH + ".tmp"
            with open(tmp_path, "wb") as f:
                f.write(data_bytes)
            os.replace(tmp_path, SELLERS_PATH)
        except Exception as e:
            print(f"[Error] Failed to save sellers_vault local: {e}")
        if put_object_r2 and os.environ.get("PORT"):
            threading.Thread(target=lambda: put_object_r2(_R2_SELLERS_VAULT_KEY, data_bytes, "application/json; charset=utf-8"), daemon=True).start()


def upsert_seller_account(line_user_id: str, name: str = "", picture: str = "", phone: str = "") -> dict:
    with SELLERS_LOCK:
        store = load_sellers_data()
        sellers = store.setdefault("sellers", [])
        now_str = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        seller = next((x for x in sellers if x.get("lineUserId") == line_user_id), None)
        if not seller:
            seller = {
                "id": f"SLR-{int(time.time()*1000)%1000000:06d}",
                "role": "seller",
                "lineUserId": line_user_id,
                "name": name,
                "picture": picture,
                "phone": phone,
                "created_at": now_str,
                "last_active_at": now_str,
            }
            sellers.insert(0, seller)
        else:
            if name:
                seller["name"] = name
            if picture:
                seller["picture"] = picture
            if phone:
                seller["phone"] = phone
            seller["last_active_at"] = now_str
        save_sellers_data(store)
        return seller


def _sanitize_intake_for_seller(it: dict) -> dict:
    return {
        "id": it.get("id", ""),
        "swc_code": it.get("swc_code", ""),
        "type": it.get("type", ""),
        "title": it.get("title", ""),
        "price": it.get("price", ""),
        "size": it.get("size", ""),
        "contract_mode": it.get("contract_mode", ""),
        "status": it.get("status", "pending_review"),
        "review_note": it.get("review_note", "") if it.get("status") == "need_revision" else "",
        "created_at": it.get("created_at", ""),
        "updated_at": it.get("updated_at", ""),
    }


def _sanitize_contract_for_seller(c: dict) -> dict:
    return {
        "id": c.get("id", ""),
        "swc_code": c.get("swc_code", ""),
        "contract_type": c.get("contract_type", ""),
        "contract_mode": c.get("contract_mode", ""),
        "project_name": c.get("project_name") or c.get("property_title") or c.get("title") or "",
        "sale_price": c.get("sale_price") or c.get("price") or "",
        "area": c.get("area") or c.get("size") or "",
        "deed_no": c.get("deed_no", ""),
        "expires_at": c.get("expires_at", ""),
        "saved_at": c.get("saved_at", ""),
        "status": c.get("status", "active"),
    }


# ==============================================================================
# CLIENT VIEW TRACKING, HYBRID AVATAR LINK (&t=) & DEVICE VISITOR TRUST (vid)
# ==============================================================================
CLIENT_TRACKING_PATH = os.path.join(DATA_DIR, "client_tracking.json")
CLIENT_TRACKING_LOCK = threading.RLock()
_R2_CLIENT_TRACKING_VAULT_KEY = "_vault/client_tracking_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_client_tracking_vault_v1", hashlib.sha256).hexdigest()[:32] + ".json"
_R2_CLIENT_TRACKING_RESTORED = False
_CLIENT_TRACKING_MEM_CACHE = None
_R2_CLIENT_TRACKING_UPLOAD_LOCK = threading.Lock()
_LATEST_CLIENT_TRACKING_BYTES = None
_TAG_SECRET_SEED = (os.environ.get("ADMIN_EXPORT_SECRET") or LINE_CHANNEL_SECRET or ADMIN_EXPORT_SECRET) + "_client_tag_mask_v2"
_TAG_MASK_KEY = hashlib.sha256(_TAG_SECRET_SEED.encode("utf-8")).digest()
_CLIENT_ALERT_COOLDOWN = {}
_AGENT_ALERT_RATE = {}
_TRACK_IP_WINDOW = {}
_CLIENT_ALERT_LOCK = threading.Lock()
_MAX_TRACKED_VISITORS = 2000


def _default_client_tracking_store():
    return {
        "updated_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
        "visitors": {},
        "events": [],
        "merge_log": []
    }


def _clone_store(store):
    return json.loads(json.dumps(store, ensure_ascii=False))


def load_client_tracking_data():
    global _R2_CLIENT_TRACKING_RESTORED, _CLIENT_TRACKING_MEM_CACHE
    with CLIENT_TRACKING_LOCK:
        if not _R2_CLIENT_TRACKING_RESTORED and os.environ.get("PORT"):
            try:
                url = f"https://assets.siwasup.com/{_R2_CLIENT_TRACKING_VAULT_KEY}?t={int(time.time())}"
                req = urllib.request.Request(url, headers={"User-Agent": "SiwasupRenderVault/1.0"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    if r.status == 200:
                        cloud_store = json.loads(r.read().decode("utf-8"))
                        if isinstance(cloud_store, dict) and "visitors" in cloud_store:
                            os.makedirs(os.path.dirname(CLIENT_TRACKING_PATH), exist_ok=True)
                            tmp_path = CLIENT_TRACKING_PATH + ".tmp"
                            with open(tmp_path, "w", encoding="utf-8") as f:
                                json.dump(cloud_store, f, ensure_ascii=False, indent=2)
                            os.replace(tmp_path, CLIENT_TRACKING_PATH)
                            _CLIENT_TRACKING_MEM_CACHE = cloud_store
                            _R2_CLIENT_TRACKING_RESTORED = True
                            print(f"[Vault] Restored client_tracking from R2 ({len(cloud_store.get('visitors', {}))} visitors)")
                            return _clone_store(cloud_store)
            except urllib.error.HTTPError as he:
                if he.code == 404:
                    _R2_CLIENT_TRACKING_RESTORED = True
                print(f"[Vault] Client tracking initial R2 restore HTTP {he.code}")
            except Exception as e:
                print(f"[Vault] Client tracking initial R2 restore note (will retry): {e}")
        if os.path.exists(CLIENT_TRACKING_PATH):
            try:
                with open(CLIENT_TRACKING_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "visitors" in data:
                        _CLIENT_TRACKING_MEM_CACHE = data
                        return _clone_store(data)
            except Exception as e:
                print(f"[Warn] Failed to read client_tracking.json: {e}")
        if _CLIENT_TRACKING_MEM_CACHE is not None:
            return _clone_store(_CLIENT_TRACKING_MEM_CACHE)
        return _default_client_tracking_store()


def _sequential_r2_tracking_upload():
    global _LATEST_CLIENT_TRACKING_BYTES
    with _R2_CLIENT_TRACKING_UPLOAD_LOCK:
        with CLIENT_TRACKING_LOCK:
            payload_bytes = _LATEST_CLIENT_TRACKING_BYTES
        if payload_bytes and put_object_r2:
            try:
                put_object_r2(_R2_CLIENT_TRACKING_VAULT_KEY, payload_bytes, "application/json; charset=utf-8")
            except Exception as e:
                print(f"[R2 Client Tracking Sync Warn]: {e}")


def save_client_tracking_data(store):
    global _CLIENT_TRACKING_MEM_CACHE, _LATEST_CLIENT_TRACKING_BYTES
    with CLIENT_TRACKING_LOCK:
        prev_count = len((_CLIENT_TRACKING_MEM_CACHE or {}).get("visitors", {}))
        new_count = len(store.get("visitors", {}))
        if prev_count > 3 and new_count == 0:
            print(f"[CRITICAL SAFEGUARD] Blocked attempted client_tracking wipeout! Existing: {prev_count}, Incoming: {new_count}")
            return
        store["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        _CLIENT_TRACKING_MEM_CACHE = _clone_store(store)
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            os.makedirs(os.path.dirname(CLIENT_TRACKING_PATH), exist_ok=True)
            tmp_path = CLIENT_TRACKING_PATH + ".tmp"
            with open(tmp_path, "wb") as f:
                f.write(data_bytes)
            os.replace(tmp_path, CLIENT_TRACKING_PATH)
        except Exception as e:
            print(f"[Error] Failed to save client_tracking local: {e}")
        _LATEST_CLIENT_TRACKING_BYTES = data_bytes
        if put_object_r2 and os.environ.get("PORT") and _R2_CLIENT_TRACKING_RESTORED:
            threading.Thread(target=_sequential_r2_tracking_upload, daemon=True).start()


def _derive_tag_keystream(nonce: bytes, length: int) -> bytes:
    chunks = []
    blk = 0
    total = 0
    while total < length:
        digest = hashlib.sha256(_TAG_MASK_KEY + nonce + blk.to_bytes(2, "big")).digest()
        chunks.append(digest)
        total += len(digest)
        blk += 1
    return b"".join(chunks)[:length]


def encode_client_tag(avatar_name: str, agent_note: str = "") -> str:
    """Short 8-char URL-safe token backed by client_tracking_data (with legacy HMAC fallback in decode)."""
    av = re.sub(r"[\t\r\n]+", " ", str(avatar_name or "")).strip()[:25]
    note = re.sub(r"[\t\r\n]+", " ", str(agent_note or "")).strip()[:60]
    if not av:
        return ""
    try:
        with CLIENT_TRACKING_LOCK:
            store = load_client_tracking_data()
            st = store.setdefault("short_tags", {})
            for k_ex, v_ex in st.items():
                if isinstance(v_ex, dict) and v_ex.get("name") == av and v_ex.get("note", "") == note:
                    return k_ex
            alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
            short_code = "S" + "".join(secrets.choice(alphabet) for _ in range(7))
            while short_code in st:
                short_code = "S" + "".join(secrets.choice(alphabet) for _ in range(7))
            st[short_code] = {"name": av, "note": note, "ts": int(time.time())}
            if len(st) > 5000:
                oldest_keys = sorted(st.keys(), key=lambda k: st[k].get("ts", 0))[:len(st) - 5000]
                for ok in oldest_keys:
                    st.pop(ok, None)
            save_client_tracking_data(store)
        return short_code
    except Exception:
        raw_str = f"{av}\t{note}" if note else av
        raw_bytes = raw_str.encode("utf-8")
        nonce = secrets.token_bytes(4)
        stream = _derive_tag_keystream(nonce, len(raw_bytes))
        cipher = bytes(b ^ s for b, s in zip(raw_bytes, stream))
        mac = hmac.new(_TAG_MASK_KEY, nonce + cipher, hashlib.sha256).digest()[:6]
        return base64.urlsafe_b64encode(nonce + mac + cipher).decode("ascii").rstrip("=")


def decode_client_tag(token: str):
    """Resolve Short Token from client_tracking_data or verify legacy HMAC &t= token."""
    tok = str(token or "").strip()
    if not tok or len(tok) > 300:
        return ("", "")
    if re.match(r"^S[A-Za-z0-9]{7}$", tok):
        with CLIENT_TRACKING_LOCK:
            store = load_client_tracking_data()
            entry = (store.get("short_tags") or {}).get(tok)
            if isinstance(entry, dict):
                return (str(entry.get("name") or "").strip()[:25], str(entry.get("note") or "").strip()[:60])
    try:
        padded = tok + ("=" * (-len(tok) % 4))
        blob = base64.urlsafe_b64decode(padded.encode("ascii"))
        if len(blob) < 11:
            return ("", "")
        nonce, mac, cipher = blob[:4], blob[4:10], blob[10:]
        expect_mac = hmac.new(_TAG_MASK_KEY, nonce + cipher, hashlib.sha256).digest()[:6]
        if not hmac.compare_digest(mac, expect_mac):
            return ("", "")
        stream = _derive_tag_keystream(nonce, len(cipher))
        raw_bytes = bytes(b ^ s for b, s in zip(cipher, stream))
        decoded = raw_bytes.decode("utf-8")
        if any(ord(ch) < 32 and ch != "\t" for ch in decoded):
            return ("", "")
        if "\t" in decoded:
            av, note = decoded.split("\t", 1)
        else:
            av, note = decoded, ""
        return (av.strip()[:25], note.strip()[:60])
    except Exception:
        return ("", "")


def parse_agent_link_input(raw_input: str):
    """Parse '<avatar_name> [private note...] [optional_prop_id]' safely (supports 'ส่งให้คุณ5ที' -> '5')."""
    s = str(raw_input or "").strip()
    if not s:
        return ("", "", "")
    # Handle natural Thai phrases like "3หลังส่งให้คุณ5ที" or "ส่งให้คุณAหน่อย"
    m_khun = re.search(r'(?:ส่งให้|ให้)?คุณ\s*([0-9]+|[ก-๙a-zA-Z0-9_]+)', s)
    if m_khun and not s.startswith("คุณ"):
        raw_name = m_khun.group(1)
        # Strip trailing polite particles glued to numbers/names like "5ที", "5หน่อย", "5ครับ"
        raw_name = re.sub(r'(?:ที|หน่อย|ด้วย|ครับ|ค่ะ|นะ)$', '', raw_name).strip() or m_khun.group(1)
        prefix_note = s[:m_khun.start()].strip()
        return (raw_name[:25], prefix_note[:60], "")
    tokens = s.split()
    if not tokens:
        return ("", "", "")
    prop_id = ""
    if len(tokens) >= 2:
        last_tok = tokens[-1].strip()
        if find_property_by_id_or_code(last_tok):
            prop_id = last_tok
            tokens.pop()
    avatar_name = re.sub(r'(?:ที|หน่อย|ด้วย|ครับ|ค่ะ|นะ)$', '', tokens[0]).strip() if re.match(r'^(?:คุณ)?\d+(?:ที|หน่อย|ด้วย|ครับ|ค่ะ|นะ)$', tokens[0]) else tokens[0]
    avatar_name = avatar_name[:25]
    agent_note = " ".join(tokens[1:])[:60] if len(tokens) > 1 else ""
    return (avatar_name, agent_note, prop_id)


_LOBBY_OP_LOCK = threading.Lock()


def _is_lobby_approver(member: dict) -> bool:
    """Only Bua (SA001), Lily (SA002), Gool (SW001), and Ton (SA000) may approve/reject Lobby registrations."""
    if not isinstance(member, dict):
        return False
    mid = str(member.get("id") or "").strip().lower()
    code = str(member.get("code") or member.get("agent_ref") or "").strip().upper()
    perms = member.get("permissions") or {}
    if mid in ("app_office_001", "app_office_002", "app_office_003", "app_office_004"):
        return True
    if code in ("SW001", "SA000", "SA001", "SA002"):
        return True
    if bool(perms.get("executiveAuthority") or perms.get("systemAdmin")):
        return True
    return False


def _next_agent_sw_code(store: dict) -> str:
    """Assign next sequential SW128+ code for new sales agents (runs after legacy 02-127)."""
    max_num = 127
    for m in (store or {}).get("approved", []):
        c = str(m.get("code") or m.get("agent_ref") or "").strip().upper()
        m_sw = re.match(r"^SW(\d{3,})$", c)
        if m_sw:
            n = int(m_sw.group(1))
            if n < 9000 and n > max_num:
                max_num = n
    return f"SW{max_num + 1}"


def _next_admin_sa_code(store: dict) -> str:
    """Assign next available SA003+ code for newly approved admin/staff members."""
    used_nums = {0, 1, 2}  # Reserved: SA000 (Tech/Ton), SA001 (Bua), SA002 (Lily)
    for m in (store or {}).get("approved", []):
        c = str(m.get("code") or m.get("agent_ref") or "").strip().upper()
        m_sa = re.match(r"^SA(\d{3,})$", c)
        if m_sa:
            used_nums.add(int(m_sa.group(1)))
    nxt = 3
    while nxt in used_nums:
        nxt += 1
    return f"SA{nxt:03d}"


def resolve_agent_ref_for_member(member):
    if not isinstance(member, dict):
        return "SW000"
    mid = str(member.get("id", "")).strip()
    nick_u = str(member.get("nickname", "")).strip().upper()
    if mid == "app_office_001" or nick_u == "SW001" or nick_u.startswith("SW001 "):
        return "SW001"
    if mid == "app_office_004" or nick_u in ("NASSTY", "[NASSTY]"):
        return "SA000"
    if mid == "app_office_002":
        return str(member.get("agent_ref") or member.get("code") or "SA001").strip()
    if mid == "app_office_003":
        return str(member.get("agent_ref") or member.get("code") or "SA002").strip()
    explicit = str(member.get("agent_ref") or member.get("code") or "").strip()
    return explicit if explicit else "SW000"


def find_agent_line_uid(agent_ref: str) -> str:
    ref_clean = str(agent_ref or "").strip().upper()
    if not ref_clean:
        return ""
    store = load_lobby_data()
    approved = store.get("approved", [])
    for m in approved:
        uid = m.get("lineUserId", "")
        if not uid:
            continue
        m_ref = resolve_agent_ref_for_member(m).upper()
        if m_ref == ref_clean:
            return uid
        if ref_clean in (str(m.get("id", "")).upper(), str(m.get("nickname", "")).upper(), str(m.get("line_id", "")).upper()):
            return uid
    if ref_clean == "SW001":
        ceo = next((m for m in approved if m.get("id") == "app_office_001"), None)
        if ceo and ceo.get("lineUserId"):
            return ceo["lineUserId"]
    return ""


def build_client_catalog_link(avatar_name: str, agent_note: str = "", agent_ref: str = "SW001", prop_id: str = ""):
    tok = encode_client_tag(avatar_name, agent_note)
    url = f"https://assets.siwasup.com/catalog.html?ref={urllib.parse.quote(agent_ref)}&view=client&t={tok}"
    if prop_id:
        url += f"&id={urllib.parse.quote(str(prop_id).strip())}"
    return (url, tok)


def resolve_catalog_link_request(text_raw: str, matched_member: dict, is_admin: bool = False):
    """Detect requests for an agent's client catalog link (e.g. 'ส่งลิงก์บ้านของตัวแทน 001 มาให้ที')."""
    t = str(text_raw or "").strip()
    tl = t.lower()
    if not any(w in tl for w in ("ลิงก์", "ลิงค์", "link")):
        return None
    if any(w in tl for w in ("สมัคร", "ลงทะเบียน", "นามบัตร", "login", "เข้าสู่ระบบ")):
        return None
    # Detect explicit request for Internal Agent View (showing bank names/codes) vs Client View
    if any(w in tl for w in ("มุม agent", "มุมตัวแทน", "ฝั่งตัวแทน", "ฝั่งเอเจน", "สำหรับ agent", "สำหรับตัวแทน", "ธนาคารไหน", "ทรัพย์ธนาคาร", "ดูในระบบ")) or re.match(r'^(?:สร้าง|ขอ|ส่ง)?(?:ลิงก์|ลิงค์|ลิ้งก์|ลิ้งค์)\s*(?:ตัวแทน|เอเจนต์?|agent)\s*$', tl):
        return None
    has_direct_catalog_phrase = any(
        w in tl for w in (
            "ลิงก์บ้าน", "ลิงค์บ้าน", "ลิงก์ทรัพย์", "ลิงค์ทรัพย์",
            "ลิงก์แคตตาล็อก", "ลิงค์แคตตาล็อก", "ลิงก์แค็ตตาล็อก", "ลิงค์แค็ตตาล็อก",
            "ลิงก์ขายบ้าน", "ลิงค์ขายบ้าน", "ลิงก์ของฉัน", "ลิงค์ของฉัน", "ลิงก์ส่วนตัว", "ลิงค์ส่วนตัว",
            "แปะกลุ่ม", "กลุ่มสาธารณะ", "โพสต์กลุ่ม", "ลิงก์สาธารณะ", "ลิงค์สาธารณะ", "ลิงก์กลุ่ม", "ลิงค์กลุ่ม", "ทุกโซน"
        )
    )
    starts_with_catalog_req = bool(re.match(
        r'^(?:สร้าง|ขอ|ส่ง)?(?:ลิงก์|ลิงค์|ลิ้งก์|ลิ้งค์)\s*(?:บ้าน|ทรัพย์|แคตตาล็อก|แค็ตตาล็อก|catalog|ขายบ้าน|ของฉัน|ส่วนตัว|ของตัวแทน|ตัวแทน|แปะกลุ่ม|กลุ่ม|สาธารณะ|โพสต์|ทุกโซน)',
        tl
    ))
    has_agent_code = bool(re.search(r'(?:ตัวแทน|เอเจนต์?|แอดมิน|รหัส)\s*(?:s[wa])?\d{3}\b', tl, re.IGNORECASE))
    if not (has_direct_catalog_phrase or starts_with_catalog_req or has_agent_code):
        return None

    # Do NOT hijack queries that specify a location, budget, or specific search filter
    # e.g. "ขอลิงก์บ้าน คานหามอยุธยา" should run geo search + filtered link instead of generic link!
    if not has_agent_code and not any(w in tl for w in ("ของฉัน", "ส่วนตัว", "แปะกลุ่ม", "กลุ่มสาธารณะ", "โพสต์กลุ่ม", "ลิงก์สาธารณะ", "ลิงก์กลุ่ม", "ทุกโซน")):
        if _extract_thai_geo(tl) or parse_price(tl):
            return None
        stripped_generic = re.sub(r'^(?:สร้าง|ขอ|ส่ง)?(?:ลิงก์|ลิงค์|ลิ้งก์|ลิ้งค์)\s*(?:บ้าน|ทรัพย์|แคตตาล็อก|แค็ตตาล็อก|catalog|ขายบ้าน)?\s*', '', tl).strip()
        if len(stripped_generic) >= 3:
            return None

    ag_ref = resolve_agent_ref_for_member(matched_member)
    if is_admin:
        m_code = re.search(r'\b(s[wa]\d{3}|\d{3})\b', tl, re.IGNORECASE)
        if m_code:
            raw_code = m_code.group(1).upper()
            ag_ref = raw_code if raw_code.startswith(("SW", "SA")) else f"SW{raw_code}"
    url = f"https://assets.siwasup.com/catalog.html?ref={urllib.parse.quote(ag_ref)}&view=client"
    return (ag_ref, url)


def compute_visitor_trust(vis: dict):
    if vis.get("confirmed"):
        return (100, "✅ ยืนยันตัวตนสมบูรณ์ (100%)")
    has_name = bool(str(vis.get("primary_name") or "").strip())
    open_count = int(vis.get("open_count") or 0)
    prop_clicks = len(vis.get("viewed_properties") or [])
    if has_name and (open_count >= 2 or prop_clicks >= 2):
        return (75, "🔥 ความแม่นยำสูง - เข้าชมซ้ำ (75%)")
    if has_name:
        return (50, "🏷️ ผูกชื่อ Avatar กับเครื่องแล้ว (50%)")
    return (25, "🌱 ผู้เข้าชมลิงก์รวม (25%)")


def _resolve_root_visitor(visitors: dict, vid: str):
    cur = vid
    seen = set()
    while cur in visitors and visitors[cur].get("merged_into"):
        nxt = visitors[cur].get("merged_into")
        if not nxt or nxt in seen or nxt not in visitors:
            break
        seen.add(cur)
        cur = nxt
    return cur


def get_consolidated_visitor(visitors: dict, vid: str, ref_filter: str = ""):
    """Aggregate opens, property clicks, names, notes_by_ref, refs, and trust score across root + merged aliases."""
    root_id = _resolve_root_visitor(visitors, vid)
    root_vis = visitors.get(root_id, {})
    cons = dict(root_vis)
    cons["vid"] = root_id
    aliases = []
    all_props = list(root_vis.get("viewed_properties") or [])
    total_opens = int(root_vis.get("open_count") or 0)
    total_clicks = int(root_vis.get("click_count") or 0)
    confirmed = bool(root_vis.get("confirmed"))
    shared_warn = bool(root_vis.get("shared_link_warning"))
    last_seen = str(root_vis.get("last_seen_at") or "")
    primary_name = str(root_vis.get("primary_name") or "").strip()
    all_names = [n for n in (root_vis.get("name_history") or []) if n]
    if primary_name and primary_name not in all_names:
        all_names.insert(0, primary_name)
    all_refs = list(root_vis.get("refs") or [])
    ref_set_u = {str(r).upper() for r in all_refs if r}
    merged_notes_by_ref = {str(k).upper(): v for k, v in (root_vis.get("notes_by_ref") or {}).items() if v}
    if root_vis.get("agent_note") and not root_vis.get("notes_by_ref"):
        for r_item in all_refs:
            rk_u = str(r_item).upper()
            if rk_u and rk_u not in merged_notes_by_ref:
                merged_notes_by_ref[rk_u] = root_vis["agent_note"]

    alias_items = [
        (v_key, v_obj)
        for v_key, v_obj in visitors.items()
        if v_key != root_id and _resolve_root_visitor(visitors, v_key) == root_id
    ]
    alias_items.sort(key=lambda kv: str(kv[1].get("last_seen_at") or ""), reverse=True)

    for v_key, v_obj in alias_items:
        aliases.append(v_key)
        total_opens += int(v_obj.get("open_count") or 0)
        total_clicks += int(v_obj.get("click_count") or 0)
        confirmed = confirmed or bool(v_obj.get("confirmed"))
        shared_warn = shared_warn or bool(v_obj.get("shared_link_warning"))
        for pid in (v_obj.get("viewed_properties") or []):
            if pid not in all_props:
                all_props.append(pid)
        if str(v_obj.get("last_seen_at") or "") > last_seen:
            last_seen = str(v_obj.get("last_seen_at") or "")
        a_pname = str(v_obj.get("primary_name") or "").strip()
        if not primary_name and a_pname:
            primary_name = a_pname
        for nm in (v_obj.get("name_history") or ([a_pname] if a_pname else [])):
            if nm and nm not in all_names:
                all_names.append(nm)
        for rf in (v_obj.get("refs") or []):
            rf_u = str(rf).upper()
            if rf and rf_u not in ref_set_u:
                ref_set_u.add(rf_u)
                all_refs.append(rf)
        for rk, rv in (v_obj.get("notes_by_ref") or {}).items():
            rk_u = str(rk).upper()
            if rk_u and rv and rk_u not in merged_notes_by_ref:
                merged_notes_by_ref[rk_u] = rv
        if v_obj.get("agent_note") and not v_obj.get("notes_by_ref"):
            for r_item in (v_obj.get("refs") or []):
                rk_u = str(r_item).upper()
                if rk_u and rk_u not in merged_notes_by_ref:
                    merged_notes_by_ref[rk_u] = v_obj["agent_note"]

    cons["primary_name"] = primary_name
    cons["name_history"] = all_names
    cons["refs"] = all_refs
    cons["notes_by_ref"] = merged_notes_by_ref
    cons["open_count"] = total_opens
    cons["click_count"] = total_clicks
    cons["viewed_properties"] = all_props
    cons["confirmed"] = confirmed
    cons["shared_link_warning"] = shared_warn or (len(all_names) >= 2)
    cons["last_seen_at"] = last_seen
    cons["_aliases"] = sorted(aliases)
    if ref_filter:
        cons["agent_note"] = merged_notes_by_ref.get(ref_filter.upper(), "")
    else:
        cons["agent_note"] = cons.get("agent_note") or next(iter(merged_notes_by_ref.values()), "")
    score, label = compute_visitor_trust(cons)
    cons["trust_score"] = score
    cons["trust_label"] = label
    return cons


def merge_visitor_ids(master_vid: str, alias_vid: str, actor_name: str = "", agent_ref: str = "", is_admin: bool = True):
    m_id = str(master_vid or "").strip().upper()
    a_id = str(alias_vid or "").strip().upper()
    with CLIENT_TRACKING_LOCK:
        store = load_client_tracking_data()
        visitors = store.setdefault("visitors", {})
        if m_id not in visitors:
            return (False, f"ไม่พบรหัสเครื่องหลัก {m_id} ในระบบ")
        if a_id not in visitors:
            return (False, f"ไม่พบรหัสเครื่องพ่วง {a_id} ในระบบ")
        m_root = _resolve_root_visitor(visitors, m_id)
        if m_root == a_id:
            return (False, "ไม่สามารถรวมรหัสเครื่องเดียวกันได้")
        if not is_admin and agent_ref:
            ref_u = agent_ref.upper()
            for check_id in (m_id, m_root, a_id):
                if ref_u not in [r.upper() for r in (visitors[check_id].get("refs") or [])]:
                    return (False, "สิทธิ์เฉพาะเจ้าของลูกค้าหรือผู้บริหารเท่านั้น")
        m_lock = visitors[m_root].get("lock") or {}
        a_lock = visitors[a_id].get("lock") or {}
        now_dt = bkk_now()
        _sync_lock_expiry(visitors[m_root], now_dt)
        _sync_lock_expiry(visitors[a_id], now_dt)
        if a_lock.get("status") == "booked" and m_lock.get("status") != "booked":
            visitors[m_root]["lock"] = dict(a_lock)
        elif m_lock.get("status") in ("active", "conflict_pending") and a_lock.get("status") in ("active", "conflict_pending"):
            o1 = str(m_lock.get("owner_ref") or "").upper()
            o2 = str(a_lock.get("owner_ref") or "").upper()
            if o1 and o2 and o1 != o2:
                cands = list(dict.fromkeys([o1, o2] + list(m_lock.get("conflict_candidates") or [])))
                m_lock["status"] = "conflict_pending"
                m_lock["conflict_candidates"] = cands
                visitors[m_root]["lock"] = m_lock
        visitors[a_id]["merged_into"] = m_root
        for k, v in visitors.items():
            if k != a_id and v.get("merged_into") == a_id:
                v["merged_into"] = m_root
        store.setdefault("merge_log", []).insert(0, {
            "action": "MERGE",
            "master_vid": m_root,
            "alias_vid": a_id,
            "actor": actor_name,
            "timestamp": bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        })
        store["merge_log"] = store["merge_log"][:200]
        save_client_tracking_data(store)
        m_name = visitors[m_root].get("primary_name") or m_root
        return (True, f"รวม #{a_id} เข้ากับ #{m_root} ({m_name}) เรียบร้อย (สามารถพิมพ์ 'แยก {a_id}' เพื่อยกเลิกได้ตลอดเวลา)")


def unmerge_visitor_id(alias_vid: str, actor_name: str = "", agent_ref: str = "", is_admin: bool = True):
    a_id = str(alias_vid or "").strip().upper()
    with CLIENT_TRACKING_LOCK:
        store = load_client_tracking_data()
        visitors = store.setdefault("visitors", {})
        if a_id not in visitors:
            return (False, f"ไม่พบรหัสเครื่อง {a_id} ในระบบ")
        if not is_admin and agent_ref:
            ref_u = agent_ref.upper()
            if ref_u not in [r.upper() for r in (visitors[a_id].get("refs") or [])]:
                return (False, "สิทธิ์เฉพาะเจ้าของลูกค้าหรือผู้บริหารเท่านั้น")
        prev_master = visitors[a_id].get("merged_into")
        if not prev_master:
            return (False, f"รหัส #{a_id} ไม่ได้ถูกพ่วงรวมกับรหัสใดอยู่แล้ว")
        visitors[a_id]["merged_into"] = None
        store.setdefault("merge_log", []).insert(0, {
            "action": "UNMERGE",
            "prev_master_vid": prev_master,
            "alias_vid": a_id,
            "actor": actor_name,
            "timestamp": bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        })
        store["merge_log"] = store["merge_log"][:200]
        save_client_tracking_data(store)
        return (True, f"แยก #{a_id} ออกจาก #{prev_master} คืนสถานะอิสระ 100% แล้ว")


def confirm_visitor_identity(vid: str, actor_name: str = "", agent_ref: str = "", is_admin: bool = True):
    v_id = str(vid or "").strip().upper()
    with CLIENT_TRACKING_LOCK:
        store = load_client_tracking_data()
        visitors = store.setdefault("visitors", {})
        if v_id not in visitors:
            return (False, f"ไม่พบรหัสเครื่อง {v_id} ในระบบ")
        root_id = _resolve_root_visitor(visitors, v_id)
        vis = visitors[root_id]
        if not is_admin and agent_ref:
            ref_u = agent_ref.upper()
            if ref_u not in [r.upper() for r in (vis.get("refs") or [])]:
                return (False, "สิทธิ์เฉพาะเจ้าของลูกค้าหรือผู้บริหารเท่านั้น")
        vis["confirmed"] = True
        cons = get_consolidated_visitor(visitors, root_id)
        vis["trust_score"] = cons["trust_score"]
        vis["trust_label"] = cons["trust_label"]
        vis["confirmed_by"] = actor_name
        vis["confirmed_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        save_client_tracking_data(store)
        name = vis.get("primary_name") or root_id
        return (True, f"ยืนยันตัวตน #{root_id} ({name}) สมบูรณ์แล้ว — Trust Score: {cons['trust_score']}%")


def _check_track_ip_rate(client_ip: str) -> bool:
    if not client_ip:
        return True
    now_ts = time.time()
    with _CLIENT_ALERT_LOCK:
        hist = [t for t in _TRACK_IP_WINDOW.get(client_ip, []) if now_ts - t < 60]
        if len(hist) >= 40:
            _TRACK_IP_WINDOW[client_ip] = hist
            return False
        hist.append(now_ts)
        _TRACK_IP_WINDOW[client_ip] = hist
        if len(_TRACK_IP_WINDOW) > 1000:
            stale_ips = [ip for ip, ts_list in _TRACK_IP_WINDOW.items() if not ts_list or now_ts - ts_list[-1] > 120]
            for ip in stale_ips:
                del _TRACK_IP_WINDOW[ip]
    return True


def _should_send_client_alert(raw_vid: str, event_type: str, property_id: str = "", ref: str = "SW001") -> bool:
    cooldown = 300 if event_type == "property_click" else 900
    key = (raw_vid, event_type, property_id if event_type == "property_click" else "")
    ref_key = str(ref or "SW001").strip().upper()
    now_ts = time.time()
    with _CLIENT_ALERT_LOCK:
        last_ts = _CLIENT_ALERT_COOLDOWN.get(key, 0)
        if now_ts - last_ts < cooldown:
            return False
        ref_hist = [t for t in _AGENT_ALERT_RATE.get(ref_key, []) if now_ts - t < 60]
        if len(ref_hist) >= 5:
            _AGENT_ALERT_RATE[ref_key] = ref_hist
            return False
        _CLIENT_ALERT_COOLDOWN[key] = now_ts
        ref_hist.append(now_ts)
        _AGENT_ALERT_RATE[ref_key] = ref_hist
        if len(_CLIENT_ALERT_COOLDOWN) > 2000:
            cutoff = now_ts - 3600
            stale = [k for k, v in _CLIENT_ALERT_COOLDOWN.items() if v < cutoff]
            for k in stale:
                del _CLIENT_ALERT_COOLDOWN[k]
    return True


def _prune_old_visitors(visitors: dict):
    if len(visitors) <= _MAX_TRACKED_VISITORS:
        return
    referenced_roots = {v.get("merged_into") for v in visitors.values() if v.get("merged_into")}
    candidates = [
        (v.get("last_seen_at", ""), k)
        for k, v in visitors.items()
        if not v.get("confirmed") and not v.get("merged_into") and k not in referenced_roots
    ]
    candidates.sort()
    overflow = len(visitors) - _MAX_TRACKED_VISITORS
    for _, k in candidates[:overflow]:
        visitors.pop(k, None)


def _parse_bkk_dt(s: str):
    try:
        return datetime.strptime(str(s or "").strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=TH_TZ)
    except Exception:
        return None


def _sync_lock_expiry(vis: dict, now_dt=None) -> bool:
    """Lazy expiry: if active/conflict_pending lock is past expires_at, mark expired and clear owner_ref."""
    if not isinstance(vis, dict):
        return False
    lk = vis.get("lock")
    if not isinstance(lk, dict):
        return False
    st = str(lk.get("status") or "")
    if st == "booked":
        return False
    if st in ("active", "conflict_pending"):
        exp_dt = _parse_bkk_dt(lk.get("expires_at"))
        now_dt = now_dt or bkk_now()
        if exp_dt and now_dt >= exp_dt:
            lk["status"] = "expired"
            lk["owner_ref"] = ""
            lk["conflict_candidates"] = []
            return True
    return False


def _apply_lock_on_visit(visitors: dict, root_vid: str, ref: str, is_identified: bool, now_dt=None):
    """Apply 15-day Customer Lock rule on identified visit."""
    vis = visitors.get(root_vid)
    if not isinstance(vis, dict):
        return {}
    now_dt = now_dt or bkk_now()
    _sync_lock_expiry(vis, now_dt)
    ref_u = str(ref or "").strip().upper()
    if not is_identified or not ref_u or ref_u == "SW000":
        return vis.get("lock") or {}
    lk = vis.get("lock")
    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    exp_str = (now_dt + timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")
    if not isinstance(lk, dict) or lk.get("status") in (None, "", "expired"):
        vis["lock"] = {
            "owner_ref": ref_u,
            "locked_at": now_str,
            "expires_at": exp_str,
            "extended_days": 0,
            "extended_by": "",
            "extend_reason": "",
            "status": "active",
            "booked_property_id": "",
            "booked_at": "",
            "conflict_candidates": [],
            "chosen_by_client_at": "",
            "history": [{"action": "LOCK_15D", "ref": ref_u, "at": now_str}],
        }
        return vis["lock"]
    if lk.get("status") == "booked":
        return lk
    owner_u = str(lk.get("owner_ref") or "").strip().upper()
    hq_admin_refs = {"SW000", "SW001", "SA000", "SA001", "SA002"}
    if owner_u and owner_u != ref_u:
        if owner_u in hq_admin_refs and ref_u in hq_admin_refs:
            return lk
        cands = list(dict.fromkeys([owner_u] + [str(c).upper() for c in (lk.get("conflict_candidates") or []) if c] + [ref_u]))
        lk["status"] = "conflict_pending"
        lk["conflict_candidates"] = cands
        lk.setdefault("history", []).append({"action": "CONFLICT", "ref": ref_u, "at": now_str})
    return lk


def _format_lock_badge(vis: dict, now_dt=None) -> str:
    lk = (vis or {}).get("lock")
    if not isinstance(lk, dict) or not lk.get("status"):
        return ""
    now_dt = now_dt or bkk_now()
    _sync_lock_expiry(vis, now_dt)
    st = lk.get("status")
    owner = lk.get("owner_ref") or "-"
    if st == "booked":
        pid = lk.get("booked_property_id") or "-"
        return f" | 🏠 จองแล้ว [{pid}] (ล็อกถาวร: {owner})"
    if st == "conflict_pending":
        cands = ", ".join(lk.get("conflict_candidates") or [])
        return f" | ⚠️ ชนกัน ({cands}) รอลูกค้าเลือก"
    if st == "active":
        exp_dt = _parse_bkk_dt(lk.get("expires_at"))
        days_left = max(0, (exp_dt - now_dt).days) if exp_dt else 15
        return f" | 🔒 ล็อก [{owner}] เหลือ {days_left} วัน"
    if st == "expired":
        return " | 🔓 ล็อกหมดอายุแล้ว"
    return ""


def record_client_tracking_event(payload: dict) -> dict:
    raw_vid = re.sub(r"[^A-Z0-9\-]", "", str(payload.get("vid") or "").strip().upper())[:24]
    tag_token = str(payload.get("t") or "").strip()
    ref = re.sub(r"[^A-Za-z0-9_\-]", "", str(payload.get("ref") or "SW001").strip())[:24] or "SW001"
    event_type = str(payload.get("event") or "catalog_open").strip()[:32]
    if event_type not in ("catalog_open", "property_click"):
        event_type = "catalog_open"
    property_id = re.sub(r"[^A-Za-z0-9_\-]", "", str(payload.get("property_id") or "").strip())[:40]
    property_title = re.sub(r"[\r\n\t]+", " ", str(payload.get("property_title") or "")).strip()[:120]
    if property_id:
        official_prop = find_property_by_id_or_code(property_id)
        if official_prop and official_prop.get("title"):
            property_title = re.sub(r"[\r\n\t]+", " ", str(official_prop.get("title"))).strip()[:120]
    ua_type = re.sub(r"[\r\n\t]+", " ", str(payload.get("ua_type") or "mobile")).strip()[:20] or "mobile"

    if not raw_vid or not raw_vid.startswith("V-") or len(raw_vid) < 6:
        raw_vid = "V-" + hashlib.sha256(f"{ua_type}:{ref}:{tag_token}".encode("utf-8")).hexdigest()[:6].upper()

    # Strictly accept cryptographically authenticated &t= tokens only (no unsigned legacy_c spoofing)
    avatar_name, agent_note = decode_client_tag(tag_token)

    now_str = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
    now_hm = bkk_now().strftime("%H:%M")

    with CLIENT_TRACKING_LOCK:
        store = load_client_tracking_data()
        visitors = store.setdefault("visitors", {})
        vis = visitors.setdefault(raw_vid, {
            "vid": raw_vid,
            "primary_name": "",
            "agent_note": "",
            "notes_by_ref": {},
            "name_history": [],
            "notes_history": [],
            "refs": [],
            "viewed_properties": [],
            "open_count": 0,
            "click_count": 0,
            "first_seen_at": now_str,
            "last_seen_at": now_str,
            "ua_type": ua_type,
            "trust_score": 25,
            "trust_label": "🌱 ผู้เข้าชมลิงก์รวม (25%)",
            "confirmed": False,
            "shared_link_warning": False,
            "merged_into": None
        })

        if avatar_name:
            vis["primary_name"] = avatar_name
            nh = vis.setdefault("name_history", [])
            if avatar_name not in nh:
                nh.append(avatar_name)
            if len(nh) >= 2:
                vis["shared_link_warning"] = True
        if agent_note:
            vis["agent_note"] = agent_note
            vis.setdefault("notes_by_ref", {})[ref.upper()] = agent_note
            noh = vis.setdefault("notes_history", [])
            if agent_note not in noh:
                noh.append(agent_note)
        if ref and ref not in vis.setdefault("refs", []):
            vis["refs"].append(ref)

        if event_type == "property_click":
            vis["click_count"] = int(vis.get("click_count") or 0) + 1
            if property_id and property_id not in vis.setdefault("viewed_properties", []):
                vis["viewed_properties"].append(property_id)
        else:
            vis["open_count"] = int(vis.get("open_count") or 0) + 1

        vis["last_seen_at"] = now_str
        vis["ua_type"] = ua_type
        score, label = compute_visitor_trust(vis)
        vis["trust_score"] = score
        vis["trust_label"] = label

        events = store.setdefault("events", [])
        events.insert(0, {
            "raw_vid": raw_vid,
            "avatar_name": avatar_name,
            "agent_note": agent_note,
            "ref": ref,
            "event": event_type,
            "property_id": property_id,
            "property_title": property_title,
            "ua_type": ua_type,
            "timestamp": now_str,
            "ts": int(time.time())
        })
        store["events"] = events[:5000]
        _prune_old_visitors(visitors)
        cons_vis = get_consolidated_visitor(visitors, raw_vid, ref_filter=ref)
        root_vid = cons_vis.get("vid", raw_vid)
        eff_name = str(cons_vis.get("primary_name") or "").strip()
        is_identified = bool(str(avatar_name or "").strip()) or bool(eff_name) or bool(cons_vis.get("confirmed"))
        lock_info = _apply_lock_on_visit(visitors, root_vid, ref, is_identified, bkk_now())
        save_client_tracking_data(store)

    eff_score = cons_vis.get("trust_score", score)
    eff_label = cons_vis.get("trust_label", label)

    # Async LINE Push Notification to owning agent (identified leads only; raw traffic is logged without push)
    if is_identified and _should_send_client_alert(raw_vid, event_type, property_id, ref=ref):
        target_uid = find_agent_line_uid(ref)
        if target_uid and LINE_ACCESS_TOKEN:
            eff_note = cons_vis.get("agent_note") or ""
            disp_name = (eff_name if eff_name.startswith("คุณ") else f"คุณ{eff_name}") if eff_name else "ลูกค้า (ลิงก์รวมไม่ระบุชื่อ)"
            merged_tag = f" (พ่วงจาก #{raw_vid})" if root_vid != raw_vid else ""
            warn_line = "\n⚠️ หมายเหตุ: เครื่องนี้เคยเปิดจากหลายชื่อ (อาจส่งลิงก์ต่อ หรือพิมพ์แก้ไขชื่อ)" if cons_vis.get("shared_link_warning") else ""
            note_line = f"\n📝 โน้ต: {eff_note}" if eff_note else ""
            if event_type == "property_click" and property_id:
                alert_text = (
                    f"🏠 ลูกค้ากำลังเปิดดูรายละเอียดบ้าน!\n"
                    f"👤 {disp_name} [#{root_vid}]{merged_tag}{note_line}\n"
                    f"📌 [{property_id}] {property_title}\n"
                    f"🛡️ {eff_label}\n"
                    f"📱 {ua_type} • เวลา {now_hm} น.{warn_line}"
                )
            else:
                alert_text = (
                    f"🔔 ลูกค้าเปิดดูแคตตาล็อกแล้วค่ะ!\n"
                    f"👤 {disp_name} [#{root_vid}]{merged_tag}{note_line}\n"
                    f"🛡️ {eff_label}\n"
                    f"📱 {ua_type} • เวลา {now_hm} น.{warn_line}"
                )
            threading.Thread(target=_push_line_message, args=(target_uid, alert_text), daemon=True).start()

    # Never expose agent_note or historical backend names in public tracking response
    return {
        "status": "ok",
        "vid": raw_vid,
        "root_vid": root_vid,
        "avatar_name": avatar_name,
        "trust_score": eff_score,
        "lock_status": (lock_info or {}).get("status", ""),
        "lock_owner": (lock_info or {}).get("owner_ref", ""),
        "conflict_candidates": (lock_info or {}).get("conflict_candidates", []) if (lock_info or {}).get("status") == "conflict_pending" else []
    }


def format_client_tracking_report(agent_ref: str = "", target_query: str = "", is_admin: bool = False) -> str:
    q = str(target_query or "").strip()
    ref_u = str(agent_ref or "").strip().upper()
    q_clean = re.sub(r"\s+", " ", q).lower()

    queried_ref = ""
    if q_clean in ("กูล", "คุณกูล", "เจี๊ยบ", "คุณเจี๊ยบ", "gool", "jeab", "sw001", "sw001 jeab"):
        queried_ref = "SW001"
    elif q_clean in ("ต้น", "พี่ต้น", "คุณต้น", "ton", "nassty", "[nassty]", "sa000"):
        queried_ref = "SA000"
    elif re.match(r"^s[wa]\d{3,}$", q_clean):
        queried_ref = q_clean.upper()

    if queried_ref and not is_admin and queried_ref.upper() != ref_u:
        return "🔒 คำสั่งตรวจสอบลูกค้าของสายงานอื่น สงวนสิทธิ์เฉพาะผู้บริหารและแอดมินเท่านั้นค่ะ"

    eff_ref_filter = queried_ref if queried_ref else ("" if is_admin else ref_u)

    with CLIENT_TRACKING_LOCK:
        store = load_client_tracking_data()
        visitors = store.get("visitors", {})

        roots = {}
        for vid, vis in visitors.items():
            if not is_admin and ref_u and ref_u not in [r.upper() for r in (vis.get("refs") or [])]:
                continue
            root_id = _resolve_root_visitor(visitors, vid)
            if root_id not in roots:
                cons = get_consolidated_visitor(visitors, root_id, ref_filter=eff_ref_filter)
                if not is_admin and ref_u:
                    cons_refs = [r.upper() for r in (cons.get("refs") or [])]
                    if ref_u not in cons_refs:
                        continue
                roots[root_id] = cons

    items = list(roots.values())
    items.sort(key=lambda x: x.get("last_seen_at", ""), reverse=True)

    if queried_ref:
        q_ref_u = queried_ref.upper()
        items = [
            it for it in items
            if q_ref_u in [str(r).upper() for r in (it.get("refs") or [])]
        ]
    elif q:
        q_low = q.lower()
        items = [
            it for it in items
            if q_low in str(it.get("vid", "")).lower()
            or q_low in str(it.get("primary_name", "")).lower()
            or q_low in str(it.get("agent_note", "")).lower()
            or any(q_low in str(a).lower() for a in it.get("_aliases", []))
            or any(q_low in str(n).lower() for n in (it.get("name_history") or []))
            or any(q_low in str(r).lower() for r in (it.get("refs") or []))
        ]

    if not items:
        if queried_ref:
            return f"🔍 ยังไม่พบประวัติลูกค้าของสายงาน '{queried_ref}' ที่กดเปิดลิงก์ในระบบค่ะ"
        if q:
            return f"🔍 ยังไม่พบประวัติการเข้าดูของ '{q}' ค่ะ (อาจยังไม่ได้กดเปิดลิงก์)"
        return (
            "📊 ยังไม่มีลูกค้ากดเปิดลิงก์ในระบบค่ะ\n\n"
            "💡 วิธีสร้างลิงก์ส่งลูกค้า:\n"
            "พิมพ์: ลิงก์ ตั้ม\n"
            "หรือ: ลิงก์ ตั้ม งบ4ล้าน"
        )

    header_scope = f" [สายงาน: {queried_ref}]" if queried_ref else ""
    lines = [f"📊 รายงานลูกค้าเข้าดูแคตตาล็อก{header_scope} ({len(items)} เครื่องล่าสุด):"]
    for idx, it in enumerate(items[:8], 1):
        vid = it.get("vid", "")
        pname = it.get("primary_name") or "ผู้เข้าชมลิงก์รวม"
        disp = pname if (pname.startswith("คุณ") or pname == "ผู้เข้าชมลิงก์รวม") else f"คุณ{pname}"
        note = f" ({it.get('agent_note')})" if it.get("agent_note") else ""
        score = it.get("trust_score", 25)
        opens = it.get("open_count", 0)
        clicks = it.get("click_count", 0)
        last_seen = str(it.get("last_seen_at") or "")[5:16]
        props = it.get("viewed_properties", [])
        prop_txt = f" | ดูบ้าน: {', '.join(props[:3])}" if props else ""
        alias_txt = f" [พ่วง: {','.join(it['_aliases'])}]" if it.get("_aliases") else ""
        warn_txt = " ⚠️หลายชื่อ" if it.get("shared_link_warning") else ""
        lock_txt = _format_lock_badge(it)
        lines.append(f"{idx}. {disp}{note} [#{vid}]{alias_txt}\n   🛡️ Trust {score}% | เปิด {opens} ครั้ง | ดูบ้าน {clicks} ครั้ง | ล่าสุด {last_seen}{prop_txt}{warn_txt}{lock_txt}")

    lines.append("\n💡 คำสั่งเสริม:\n• ลิงก์ [ชื่อ] [โน้ต] — สร้างลิงก์เฉพาะคน\n• ยืนยัน V-XXXX — อัป Trust เป็น 100%\n• รวม V-XXXX V-YYYY / แยก V-YYYY")
    return "\n".join(lines)


# ==============================================================================
# CONTENT HUB STORE (Poppy & Admins - Public vs Agent Audience)
# ==============================================================================
CONTENT_HUB_PATH = os.path.join(DATA_DIR, "content_hub.json")
CONTENT_HUB_LOCK = threading.RLock()
_R2_CONTENT_VAULT_KEY = "_vault/content_hub_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_content_hub_v1", hashlib.sha256).hexdigest()[:32] + ".json"
_R2_CONTENT_RESTORED = False
_R2_CONTENT_RESTORE_FAILED = False
_CONTENT_MEM_CACHE = None
_CONTENT_R2_UPLOAD_LOCK = threading.Lock()
_CONTENT_R2_PENDING_BYTES = None
_CONTENT_R2_WORKER_ACTIVE = False


def _is_content_editor(member: dict) -> bool:
    if not isinstance(member, dict):
        return False
    perms = member.get("permissions") or {}
    return bool(perms.get("contentEditor") or perms.get("standardAdmin") or perms.get("executiveAuthority") or perms.get("systemAdmin")) or _is_lobby_approver(member)


def _sequential_r2_content_upload():
    global _CONTENT_R2_WORKER_ACTIVE, _CONTENT_R2_PENDING_BYTES
    while True:
        with _CONTENT_R2_UPLOAD_LOCK:
            data_bytes = _CONTENT_R2_PENDING_BYTES
            _CONTENT_R2_PENDING_BYTES = None
            if data_bytes is None:
                _CONTENT_R2_WORKER_ACTIVE = False
                return
        try:
            if put_object_r2:
                put_object_r2(_R2_CONTENT_VAULT_KEY, data_bytes, "application/json; charset=utf-8")
        except Exception as e:
            print(f"[Content Hub R2 Save Warn]: {e}")


def load_content_data():
    global _R2_CONTENT_RESTORED, _R2_CONTENT_RESTORE_FAILED, _CONTENT_MEM_CACHE
    with CONTENT_HUB_LOCK:
        if _CONTENT_MEM_CACHE is not None and len(_CONTENT_MEM_CACHE.get("items", [])) > 0:
            return json.loads(json.dumps(_CONTENT_MEM_CACHE))
        if not _R2_CONTENT_RESTORED:
            try:
                parsed = _fetch_r2_json(_R2_CONTENT_VAULT_KEY, timeout=8)
                if isinstance(parsed, dict) and isinstance(parsed.get("items"), list):
                    _CONTENT_MEM_CACHE = parsed
                    _R2_CONTENT_RESTORED = True
                    _R2_CONTENT_RESTORE_FAILED = False
                    return json.loads(json.dumps(_CONTENT_MEM_CACHE))
                if parsed is None:
                    _R2_CONTENT_RESTORED = True
                    _R2_CONTENT_RESTORE_FAILED = False
            except urllib.error.HTTPError as he:
                if he.code == 404:
                    _R2_CONTENT_RESTORED = True
                    _R2_CONTENT_RESTORE_FAILED = False
                else:
                    print(f"[Content Hub R2 Load Warn]: HTTP {he.code} {he}")
                    _R2_CONTENT_RESTORE_FAILED = True
            except Exception as e:
                print(f"[Content Hub R2 Load Warn]: {e}")
                _R2_CONTENT_RESTORE_FAILED = True
        if _CONTENT_MEM_CACHE is not None:
            return json.loads(json.dumps(_CONTENT_MEM_CACHE))
        if os.path.exists(CONTENT_HUB_PATH):
            try:
                with open(CONTENT_HUB_PATH, "r", encoding="utf-8") as f:
                    parsed = json.load(f)
                    if isinstance(parsed, dict) and isinstance(parsed.get("items"), list):
                        _CONTENT_MEM_CACHE = parsed
                        return json.loads(json.dumps(_CONTENT_MEM_CACHE))
            except Exception:
                pass
        _CONTENT_MEM_CACHE = {"items": [], "updated_at": ""}
        return json.loads(json.dumps(_CONTENT_MEM_CACHE))


def save_content_data(store: dict):
    global _CONTENT_MEM_CACHE
    with CONTENT_HUB_LOCK:
        store["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
        _CONTENT_MEM_CACHE = json.loads(json.dumps(store))
        data_bytes = json.dumps(_CONTENT_MEM_CACHE, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            tmp_path = CONTENT_HUB_PATH + ".tmp"
            with open(tmp_path, "wb") as f:
                f.write(data_bytes)
            os.replace(tmp_path, CONTENT_HUB_PATH)
        except Exception as e:
            print(f"[Content Hub Local Save Warn]: {e}")
        if put_object_r2:
            if _R2_CONTENT_RESTORE_FAILED:
                print("[Content Hub R2 Skip]: Skipping R2 overwrite because initial R2 restore failed")
                return
            try:
                put_object_r2(_R2_CONTENT_VAULT_KEY, data_bytes, "application/json; charset=utf-8")
            except Exception as e:
                print(f"[Content Hub R2 Save Warn]: {e}")


_THAI_TAMBONS_CACHE = None


def _load_thai_tambons():
    global _THAI_TAMBONS_CACHE
    if _THAI_TAMBONS_CACHE is not None:
        return _THAI_TAMBONS_CACHE
    path = os.path.join(DATA_DIR, "thai_tambons.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            _THAI_TAMBONS_CACHE = json.load(f)
    except Exception as e:
        print(f"[Thai Tambons Load Error]: {e}")
        _THAI_TAMBONS_CACHE = {}
    return _THAI_TAMBONS_CACHE


def _strip_thai_admin_prefix(text: str) -> str:
    s = re.sub(r"\s+", "", (text or "").strip())
    s = re.sub(r"^(?:ตำบล|ต\.|แขวง|อำเภอ|อ\.|เขต|จังหวัด|จ\.)", "", s)
    return s


def _thai_consonant_skeleton(text: str) -> str:
    s = _strip_thai_admin_prefix(text)
    return re.sub(r"[\u0e30-\u0e3a\u0e40-\u0e4e]", "", s)


def _recheck_thai_location(subdistrict: str, district: str, province: str) -> tuple[str, str, str, str]:
    """Cross-check OCR (subdistrict, district, province) against official Thai geography."""
    import difflib
    geo = _load_thai_tambons()
    if not geo:
        return subdistrict, district, province, ""

    p_clean = _strip_thai_admin_prefix(province)
    if p_clean in ("กรุงเทพ", "กทม", "กทม.", "กรุงเทพฯ"):
        p_clean = "กรุงเทพมหานคร"
    if p_clean not in geo:
        p_matches = difflib.get_close_matches(p_clean, list(geo.keys()), n=1, cutoff=0.75)
        if p_matches:
            p_clean = p_matches[0]
        else:
            return subdistrict, district, province, ""

    dmap = geo[p_clean]
    d_clean = _strip_thai_admin_prefix(district)
    if d_clean not in dmap:
        d_matches = difflib.get_close_matches(d_clean, list(dmap.keys()), n=1, cutoff=0.75)
        if d_matches:
            d_clean = d_matches[0]

    s_clean = _strip_thai_admin_prefix(subdistrict)
    if not s_clean:
        return subdistrict, d_clean or district, p_clean, ""

    # Tier 1: Search within matched district
    if d_clean in dmap:
        subs = dmap[d_clean]
        if s_clean in subs:
            return s_clean, d_clean, p_clean, ""
        s_skel = _thai_consonant_skeleton(s_clean)
        skel_hits = [sub for sub in subs if _thai_consonant_skeleton(sub) == s_skel]
        if len(skel_hits) == 1:
            return skel_hits[0], d_clean, p_clean, ""
        if skel_hits:
            best = max(skel_hits, key=lambda x: difflib.SequenceMatcher(None, s_clean, x).ratio())
            return best, d_clean, p_clean, ""
        close = difflib.get_close_matches(s_clean, subs, n=1, cutoff=0.72)
        if close:
            return close[0], d_clean, p_clean, ""

    # Tier 2: Province-wide fallback (handles old deeds whose subdistrict moved to a newer district)
    s_skel = _thai_consonant_skeleton(s_clean)
    exact_prov_hits = []
    skel_prov_hits = []
    for dist_name, subs in dmap.items():
        if s_clean in subs:
            exact_prov_hits.append((s_clean, dist_name))
        for sub in subs:
            if s_skel and _thai_consonant_skeleton(sub) == s_skel:
                skel_prov_hits.append((sub, dist_name))

    if len(exact_prov_hits) == 1:
        sub_m, dist_m = exact_prov_hits[0]
        note = f"ปัจจุบัน อ.{dist_m}" if d_clean and dist_m != d_clean else ""
        return sub_m, d_clean or dist_m, p_clean, note

    if skel_prov_hits:
        best_sub, best_dist = max(
            skel_prov_hits,
            key=lambda item: difflib.SequenceMatcher(None, s_clean, item[0]).ratio(),
        )
        if difflib.SequenceMatcher(None, s_clean, best_sub).ratio() >= 0.65:
            note = f"ปัจจุบัน อ.{best_dist}" if d_clean and best_dist != d_clean else ""
            return best_sub, d_clean or best_dist, p_clean, note

    return subdistrict, d_clean or district, p_clean, ""


_THAI_TO_ARABIC_TRANS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")


def _thai_digits_to_arabic(text: str) -> str:
    return (text or "").translate(_THAI_TO_ARABIC_TRANS)


def _normalize_rawang(raw: str) -> str:
    """Normalize Thai title deed UTM map sheet (ระวาง), converting Thai digits and fixing Roman numerals."""
    s = re.sub(r"\s+", " ", _thai_digits_to_arabic(raw or "").strip())
    if not s:
        return ""
    m = re.search(r"(\d{4})\s*([IVXil1|!]+)\s*(\d{4})(\s*-\s*\d{1,2})?", s, re.I)
    if not m:
        return s
    p1, mid, p2, tail = m.groups()
    mid_clean = mid.upper().replace("L", "I").replace("|", "I").replace("!", "I")
    roman_map = {
        "1": "I", "I": "I",
        "11": "II", "II": "II",
        "111": "III", "III": "III",
        "1V": "IV", "IV": "IV", "4": "IV",
    }
    roman = roman_map.get(mid_clean, mid.upper())
    tail_clean = re.sub(r"\s+", " ", tail or "").strip()
    return f"{p1} {roman} {p2}" + (f" {tail_clean}" if tail_clean else "")


def _validate_thai_id_checksum(id_number: str) -> dict:
    """Validate 13-digit Thai National ID using modulus-11 checksum."""
    digits = re.sub(r"\D", "", str(id_number or ""))
    if not digits:
        return {"valid": False, "digits": "", "reason": "empty"}
    if len(digits) != 13:
        return {"valid": False, "digits": digits, "reason": "ต้องมีครบ 13 หลัก"}
    total = sum(int(digits[i]) * (13 - i) for i in range(12))
    check = (11 - (total % 11)) % 10
    ok = (check == int(digits[12]))
    return {
        "valid": ok,
        "digits": digits,
        "reason": "เลขบัตรถูกต้องตามสูตร 13 หลัก" if ok else "Checksum ไม่ผ่าน (อาจอ่านผิดบางหลัก)"
    }


def _validate_rawang_utm(rawang: str) -> dict:
    """Validate Thai Land Department UTM map sheet format: <4-digit> <I|II|III|IV> <4-digit> [- 1..16]."""
    norm = _normalize_rawang(rawang)
    if not norm:
        return {"valid": False, "normalized": "", "reason": "empty"}
    m = re.match(r"^(\d{4})\s+(I|II|III|IV)\s+(\d{4})(?:\s*-\s*(\d{1,2}))?$", norm)
    if not m:
        return {
            "valid": False,
            "normalized": norm,
            "reason": "รูปแบบไม่ตรงมาตรฐาน UTM (<4หลัก> <I-IV> <4หลัก>)"
        }
    g1, roman, g2, sub = m.groups()
    col, row = int(g1[:2]), int(g1[2:])
    if not (43 <= col <= 62 and 20 <= row <= 55):
        return {
            "valid": False,
            "normalized": norm,
            "reason": f"รหัสโซน {g1} อยู่นอกพิกัดกริดประเทศไทย"
        }
    if sub is not None and not (1 <= int(sub) <= 16):
        return {
            "valid": False,
            "normalized": norm,
            "reason": f"เลขระวางย่อย (-{sub}) ต้องอยู่ระหว่าง 1-16"
        }
    return {"valid": True, "normalized": norm, "reason": "รูปแบบระวาง UTM ถูกต้อง"}


def extract_contract_ocr(image_base64, doc_type="id_card", mime_type="image/jpeg"):
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]
    
    if doc_type == "id_card":
        prompt = """คุณคือ AI ผู้ช่วยตรวจสอบและสกัดข้อมูลจาก 'บัตรประจำตัวประชาชนไทย' (Thai National ID Card) สำหรับร่างสัญญาแต่งตั้งตัวแทนขายอสังหาริมทรัพย์
จงอ่านและสกัดข้อมูลจากภาพอย่างละเอียด ถูกต้อง 100% ตอบกลับเฉพาะ JSON ที่มีโครงสร้างดังนี้เท่านั้น:
{
  "doc_type": "id_card",
  "id_number": "เลขประจำตัวประชาชน 13 หลัก (เฉพาะตัวเลข)",
  "prefix_th": "คำนำหน้า (นาย / นาง / นางสาว)",
  "first_name_th": "ชื่อภาษาไทย",
  "last_name_th": "นามสกุลภาษาไทย",
  "full_name_th": "ชื่อ-สกุลเต็มภาษาไทยพร้อมคำนำหน้า",
  "full_name_en": "Full Name in English",
  "birth_date_th": "วันเดือนปีเกิด พ.ศ.",
  "address_no": "บ้านเลขที่",
  "moo": "หมู่ที่",
  "soi": "ตรอก/ซอย",
  "road": "ถนน",
  "subdistrict": "ตำบล/แขวง",
  "district": "อำเภอ/เขต",
  "province": "จังหวัด",
  "full_address": "ที่อยู่เต็มตามบัตรประชาชน"
}
หากมองไม่เห็นฟิลด์ใด ให้ใส่เป็นสตริงว่าง "" ห้ามเดาข้อมูล"""
    elif doc_type == "title_deed":
        prompt = """คุณคือ AI ผู้ช่วยตรวจสอบและสกัดข้อมูลจาก 'โฉนดที่ดินไทย (น.ส. 4 จ.)' สำหรับร่างสัญญาแต่งตั้งตัวแทนขายอสังหาริมทรัพย์
คำแนะนำสำคัญในการอ่านโฉนดไทย:
1. ตัวเลขในโฉนดเก่ามักเขียนด้วย "เลขไทยลายมือ" (๐ ๑ ๒ ๓ ๔ ๕ ๖ ๗ ๘ ๙) ต้องแปลงเป็นเลขอารบิก (0-9) ทุกช่อง ห้ามส่งเลขไทยกลับมาใน JSON โดยเฉพาะ "โฉนดที่ดิน เลขที่" มุมขวาบน และ "หน้าสำรวจ" มุมซ้ายบน
2. "ระวาง" มีรูปแบบมาตรฐานคือ <เลข 4 หลัก> <เลขโรมัน I, II, III หรือ IV> <เลข 4 หลัก> เช่น 5140 I 1446 หรือ 5340 III 8824 (ห้ามมีตัวอักษรไทยปน ระวังเลขเขียนมือ 8 กับ 6, 2 กับ 1)
3. "เนื้อที่ดิน" ให้อ่านทั้งตัวเลขไทยและ "คำอ่านภาษาไทยในวงเล็บ" ใต้บรรทัด เช่น (ยี่สิบห้าไร่สองงานหกสิบสามตารางวา) เพื่อยืนยันความถูกต้อง 100% ก่อนตอบ
4. "ข้อความที่ถูกขีดฆ่า หรืออยู่ในวงเล็บ" (เช่น (บ้านโพธน์) ซับสมอทอด, (หนองไผ่) บึงสามพัน, ๓๗ ๑๑๕, ๑๒๗/๕ ๔๒๐๗): ให้ตัดค่าเก่าที่ขีดฆ่า/อยู่ในวงเล็บทิ้ง แล้วเลือกอ่านเฉพาะ "ค่าใหม่ที่เขียนแก้ไว้ข้างๆ หรือด้านหลัง" เสมอ!

ตอบกลับเฉพาะ JSON ที่มีโครงสร้างดังนี้เท่านั้น:
{
  "doc_type": "title_deed",
  "deed_number": "โฉนดที่ดินเลขที่ (เลขอารบิก)",
  "land_number": "เลขที่ดิน (เลขอารบิก)",
  "survey_page": "หน้าสำรวจ (เลขอารบิก)",
  "rawang": "ระวาง เช่น 5340 III 8824",
  "subdistrict": "ตำบล/แขวง (ไม่ต้องใส่คำว่า ตำบล/แขวง)",
  "district": "อำเภอ/เขต (ไม่ต้องใส่คำว่า อำเภอ/เขต)",
  "province": "จังหวัด (ไม่ต้องใส่คำว่า จังหวัด)",
  "area_rai": "จำนวนไร่ (ตัวเลขอารบิก)",
  "area_ngan": "จำนวนงาน (ตัวเลขอารบิก)",
  "area_sqw": "จำนวนตารางวา (ตัวเลขอารบิก)",
  "area_total_sqw": "คำนวณพื้นที่รวมเป็นตารางวา (ตัวเลขล้วน เช่น 10263)",
  "owner_name": "ชื่อผู้ถือกรรมสิทธิ์ / ผู้ถือกรรมสิทธิ์เดิม"
}
หากมองไม่เห็นฟิลด์ใด ให้ใส่เป็นสตริงว่าง "" ห้ามเดาข้อมูล"""
    else:
        prompt = """สกัดข้อมูลสำคัญจากเอกสารอสังหาริมทรัพย์ไทยในภาพนี้ ตอบกลับเป็น JSON ที่ระบุประเภทเอกสารและข้อมูลสำคัญ"""

    models_to_try = (
        ["gemini-flash-latest", "gemini-flash-lite-latest"]
        if doc_type == "title_deed"
        else ["gemini-flash-lite-latest", "gemini-flash-latest"]
    )
    for m in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_base64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.1
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                candidates = data.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        raw_json = parts[0].get('text', '').strip()
                        parsed = json.loads(raw_json)
                        if isinstance(parsed, dict):
                            if doc_type == "title_deed":
                                for nf in ("deed_number", "land_number", "survey_page", "rawang", "area_rai", "area_ngan", "area_sqw"):
                                    if parsed.get(nf) is not None:
                                        parsed[nf] = _thai_digits_to_arabic(str(parsed[nf])).strip()
                                if parsed.get("rawang"):
                                    parsed["rawang"] = _normalize_rawang(str(parsed["rawang"]))
                                try:
                                    r_v = float(str(parsed.get("area_rai") or 0).replace(",", "") or 0)
                                    n_v = float(str(parsed.get("area_ngan") or 0).replace(",", "") or 0)
                                    w_v = float(str(parsed.get("area_sqw") or 0).replace(",", "") or 0)
                                    if r_v or n_v or w_v:
                                        tot = r_v * 400 + n_v * 100 + w_v
                                        parsed["area_total_sqw"] = str(int(tot)) if tot.is_integer() else f"{tot:.1f}"
                                except Exception:
                                    pass
                            sub_m, dist_m, prov_m, loc_note = _recheck_thai_location(
                                str(parsed.get("subdistrict") or ""),
                                str(parsed.get("district") or ""),
                                str(parsed.get("province") or ""),
                            )
                            if sub_m:
                                parsed["subdistrict"] = sub_m
                            if dist_m:
                                parsed["district"] = dist_m
                            if prov_m:
                                parsed["province"] = prov_m
                            if loc_note:
                                parsed["location_note"] = loc_note
                            geo = _load_thai_tambons()
                            prov_key = str(parsed.get("province") or "")
                            sub_key = str(parsed.get("subdistrict") or "")
                            loc_verified = bool(
                                geo and prov_key in geo and any(sub_key in subs for subs in geo[prov_key].values())
                            )
                            validation = {"location_verified": loc_verified}
                            if doc_type == "id_card":
                                validation["id_checksum"] = _validate_thai_id_checksum(str(parsed.get("id_number") or ""))
                            elif doc_type == "title_deed":
                                validation["rawang_check"] = _validate_rawang_utm(str(parsed.get("rawang") or ""))
                            parsed["validation"] = validation
                        return parsed
        except Exception as e:
            print(f"[OCR Error on {m}]: {e}")
            continue

    raise RuntimeError("Failed to extract OCR data with Gemini Vision API")


class WebhookHandler(http.server.BaseHTTPRequestHandler):



    def _send_json(self, code, obj):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(obj, ensure_ascii=False).encode('utf-8'))

    def _redirect(self, url, set_cookie=None):
        self.send_response(302)
        self.send_header('Location', url)
        if set_cookie:
            self.send_header('Set-Cookie', set_cookie)
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()

    def _session(self):
        auth = self.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            return verify_token(auth[7:].strip())
        return None

    def _require(self, level):
        """Return the acting approved member, or send 401/403 and return None."""
        s = self._session()
        if not s or not s.get("sub"):
            self._send_json(401, {"error": "กรุณาเข้าสู่ระบบด้วย LINE"})
            return None
        store = load_lobby_data()
        ensure_super_tech_seat(store, s.get("sub"), s.get("name", ""), s.get("picture", ""))
        m = next((a for a in store.get("approved", []) if a.get("lineUserId") == s.get("sub")), None)
        if not m:
            self._send_json(401, {"error": "บัญชี LINE นี้ยังไม่ได้รับอนุมัติเป็นสมาชิก"})
            return None
        perms = m.get("permissions") or {}
        if level == "member":
            ok = True
        elif level == "lobby_approver":
            ok = _is_lobby_approver(m)
        elif level == "exec":
            ok = bool(perms.get("executiveAuthority") or perms.get("systemAdmin"))
        else:
            ok = is_admin_member(m)
        if not ok:
            self._send_json(403, {"error": "บัญชีนี้ไม่มีสิทธิ์ดำเนินการ"})
            return None
        return m

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Line-Signature, Authorization')
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        # Health & Keep-Alive Heartbeat Endpoint (Wake up Nong Siwa)
        if path in ("/health", "/api/health", "/ping"):
            store = load_lobby_data()
            approved_count = len(store.get("approved", []))
            chat_total = 0
            chat_latest_ts = None
            try:
                if os.path.exists(CHAT_LOG_PATH):
                    with open(CHAT_LOG_PATH, "r", encoding="utf-8") as cf:
                        c_data = json.load(cf)
                        if isinstance(c_data, dict):
                            c_list = c_data.get("conversations")
                            if isinstance(c_list, list):
                                chat_total = len(c_list)
                                if c_list and isinstance(c_list[0], dict):
                                    chat_latest_ts = c_list[0].get("timestamp")
            except Exception:
                pass
            with _CHAT_SYNC_STATUS_LOCK:
                sync_status_snap = dict(_CHAT_R2_SYNC_STATUS)
            self._send_json(200, {
                "status": "healthy",
                "service": "Siwasup Co-Broker Webhook v2",
                "server_time": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
                "approved_members": approved_count,
                "r2_sync": bool(put_object_r2),
                "chat_logs": {
                    "total": chat_total,
                    "latest_timestamp": chat_latest_ts,
                    "r2_sync_status": sync_status_snap,
                },
                "anti_downgrade": "ACTIVE",
                "message": "Nong Siwa is wide awake and ready to serve!"
            })
            return
        if path == "/api/contracts/list":
            acting = self._require("member")
            if not acting:
                return
            agent_ref = query.get("agent_ref", [""])[0]
            store = load_contracts_data()
            contracts = store.get("contracts", [])
            if not is_admin_member(acting):
                my_refs = {str(acting.get("code") or "").strip(), str(acting.get("id") or "").strip(), str(acting.get("lineUserId") or "").strip()}
                my_refs.discard("")
                contracts = [
                    c for c in contracts
                    if (c.get("agent_ref") in my_refs or c.get("agent_id") in my_refs or c.get("submitted_by_ref") in my_refs or c.get("submitted_by_line_id") in my_refs)
                ]
            elif agent_ref:
                contracts = [c for c in contracts if c.get("agent_ref") == agent_ref or c.get("agent_id") == agent_ref or c.get("submitted_by_ref") == agent_ref]
            self._send_json(200, {"status": "success", "count": len(contracts), "contracts": contracts})
            return
        if path == "/api/consignment/list":
            acting = self._require("member")
            if not acting:
                return
            role = _consignment_role(acting)
            store = load_consignment_data()
            props = store.get("properties", [])
            if role == "agent":
                props = [p for p in props if _is_consignment_owner(p, acting)]
            self._send_json(200, {
                "status": "success",
                "role": role,
                "updated_at": store.get("updated_at", ""),
                "updated_by": store.get("updated_by", ""),
                "count": len(props),
                "properties": props,
            })
            return

        if path == "/api/content/list":
            aud = str(query.get("audience", ["public"])[0] or "public").strip().lower()
            if aud not in ("public", "agent", "all"):
                aud = "public"
            if aud == "agent":
                acting = self._require("member")
                if not acting:
                    return
                perms = acting.get("permissions") or {}
                rc = str(acting.get("role_code") or "").upper()
                if perms.get("vipClient") or perms.get("sellerClient") or rc in ("VIP_CLIENT", "SELLER"):
                    self._send_json(403, {"error": "เฉพาะตัวแทนและทีมงานเท่านั้น"})
                    return
            elif aud == "all":
                acting = self._require("member")
                if not acting or not _is_content_editor(acting):
                    if acting:
                        self._send_json(403, {"error": "เฉพาะผู้ดูแลคอนเทนต์ (Poppy / Admin) เท่านั้น"})
                    return
            store = load_content_data()
            items = list(store.get("items", []))
            if aud == "public":
                items = [
                    it for it in items
                    if it.get("status") == "published"
                    and (
                        it.get("audience") == "both"
                        or (it.get("audience") == "public" and it.get("category") in ("just_sold", "howto", "article", "news"))
                    )
                ]
            elif aud == "agent":
                items = [
                    it for it in items
                    if it.get("status") == "published"
                    and (
                        it.get("audience") == "both"
                        or (it.get("audience") == "agent" and it.get("category") in ("top_agent", "announcement", "meeting"))
                    )
                ]
            items.sort(key=lambda x: (1 if x.get("pinned") else 0, str(x.get("published_at") or x.get("updated_at") or "")), reverse=True)
            self._send_json(200, {"status": "success", "count": len(items), "items": items})
            return

        if path == "/api/consignment/catalog":
            acting = self._require("member")
            if not acting:
                return
            store = load_consignment_data()
            out = []
            for p in store.get("properties", []):
                if p.get("status") == "available" and _is_contract_verified(p):
                    safe_p = {
                        k: v for k, v in p.items()
                        if k not in ("contract_files", "internal_note", "owner_phone", "owner_id_card", "deed_no", "land_no", "survey_page", "survey_no", "house_no")
                    }
                    out.append(safe_p)
            self._send_json(200, {
                "status": "success",
                "count": len(out),
                "properties": out,
            })
            return

        if path == "/api/consignment/contract-file":
            acting = self._require("member")
            if not acting:
                return
            role = _consignment_role(acting)
            r2_key = str(query.get("key", [""])[0] or "").strip()
            m_key = re.match(r"^_vault/consignment_contracts/([A-Za-z0-9_-]+)_[a-f0-9]+\.(pdf|jpg|png|webp)$", r2_key)
            if not m_key:
                self._send_json(400, {"error": "Invalid contract file key"})
                return
            pid_from_key = m_key.group(1)
            ext_from_key = m_key.group(2)
            if role == "agent":
                store = load_consignment_data()
                target_prop = next((x for x in store.get("properties", []) if str(x.get("id") or "").strip() == pid_from_key), None)
                if not target_prop or not _is_consignment_owner(target_prop, acting):
                    self._send_json(403, {"error": "ไม่มีสิทธิ์เข้าถึงเอกสารสัญญาของผู้อื่น"})
                    return
            ctype_map = {
                "pdf": "application/pdf",
                "jpg": "image/jpeg",
                "png": "image/png",
                "webp": "image/webp",
            }
            try:
                url = f"https://assets.siwasup.com/{r2_key}"
                req = urllib.request.Request(url, headers={"User-Agent": "SiwasupContractProxy/1.0"})
                with urllib.request.urlopen(req, timeout=12) as r:
                    file_bytes = r.read()
                self.send_response(200)
                self.send_header("Content-Type", ctype_map.get(ext_from_key, "application/octet-stream"))
                self.send_header("Content-Length", str(len(file_bytes)))
                self.send_header("Cache-Control", "private, no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                self.wfile.write(file_bytes)
            except urllib.error.HTTPError as he:
                self._send_json(he.code if he.code in (403, 404) else 502, {"error": f"Contract file fetch HTTP {he.code}"})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if path == "/api/intake/list":
            acting = self._require("member")
            if not acting:
                return
            status_filter = query.get("status", [""])[0].strip()
            store = load_intake_data()
            intakes = store.get("intakes", [])
            if not is_admin_member(acting):
                my_refs = {str(acting.get("code") or "").strip(), str(acting.get("id") or "").strip(), str(acting.get("lineUserId") or "").strip()}
                my_refs.discard("")
                intakes = [
                    it for it in intakes
                    if (it.get("submitted_by_ref") in my_refs or it.get("submitted_by_line_id") in my_refs)
                ]
            if status_filter:
                intakes = [it for it in intakes if it.get("status") == status_filter]
            pending_count = sum(1 for it in intakes if it.get("status") == "pending_review")
            self._send_json(200, {
                "status": "success",
                "count": len(intakes),
                "pending_count": pending_count,
                "is_admin": is_admin_member(acting),
                "intakes": intakes,
            })
            return

        if path == "/api/track/summary":
            secret = query.get("secret", [""])[0]
            client_ip = self.client_address[0] if hasattr(self, 'client_address') else ''
            forwarded_for = self.headers.get("X-Forwarded-For", "").strip()
            is_local = (client_ip in ("127.0.0.1", "localhost", "::1")) and (not os.environ.get("PORT")) and (not forwarded_for)
            configured_secret = os.environ.get("ADMIN_EXPORT_SECRET", "").strip()
            is_secret_ok = bool(secret and configured_secret and hmac.compare_digest(secret, configured_secret))
            acting = None
            is_admin_req = False
            if is_local or is_secret_ok:
                is_admin_req = True
            else:
                s = self._session()
                if not s or not s.get("sub"):
                    self._send_json(401, {"error": "Unauthorized"})
                    return
                lobby = load_lobby_data()
                acting = next((a for a in lobby.get("approved", []) if a.get("lineUserId") == s.get("sub")), None)
                if not acting:
                    self._send_json(403, {"error": "Forbidden"})
                    return
                is_admin_req = is_admin_member(acting)
            req_ref = query.get("ref", [""])[0].strip()
            if not is_admin_req and acting:
                req_ref = resolve_agent_ref_for_member(acting)
            req_vid = query.get("vid", [""])[0].strip().upper()
            with CLIENT_TRACKING_LOCK:
                store = load_client_tracking_data()
                visitors = store.get("visitors", {})
                events = store.get("events", [])
                updated_at = store.get("updated_at")
                now_bkk = bkk_now()
                lock_changed = False
                for v in visitors.values():
                    if _sync_lock_expiry(v, now_bkk):
                        lock_changed = True
                if lock_changed:
                    save_client_tracking_data(store)
            if not is_admin_req and req_ref:
                ref_u = req_ref.upper()
                vis_list = []
                for v in visitors.values():
                    if ref_u in [r.upper() for r in (v.get("refs") or [])]:
                        v_safe = dict(v)
                        v_safe["agent_note"] = (v.get("notes_by_ref") or {}).get(ref_u, "")
                        v_safe.pop("notes_history", None)
                        v_safe.pop("notes_by_ref", None)
                        vis_list.append(v_safe)
                ev_list = [e for e in events if str(e.get("ref", "")).upper() == ref_u]
            else:
                vis_list = list(visitors.values())
                if req_ref:
                    ref_u = req_ref.upper()
                    vis_list = [v for v in vis_list if ref_u in [r.upper() for r in (v.get("refs") or [])]]
                    ev_list = [e for e in events if str(e.get("ref", "")).upper() == ref_u]
                else:
                    ev_list = events
            if req_vid:
                group_root = _resolve_root_visitor(visitors, req_vid) if req_vid in visitors else req_vid
                group_vids = {
                    k for k in visitors
                    if k == group_root or _resolve_root_visitor(visitors, k) == group_root
                }
                if not group_vids:
                    group_vids = {req_vid}
                vis_list = [v for v in vis_list if v.get("vid") in group_vids]
                ev_list = [e for e in ev_list if e.get("raw_vid") in group_vids]
            vis_list.sort(key=lambda x: x.get("last_seen_at", ""), reverse=True)
            self._send_json(200, {
                "status": "success",
                "updated_at": updated_at,
                "visitor_count": len(vis_list),
                "visitors": vis_list[:200],
                "events": ev_list[:200]
            })
            return

        if path == "/api/bundle/flex":
            bundle_raw = query.get("bundle", [""])[0]
            client_name = query.get("for", ["คุณลูกค้า"])[0]
            agent_ref = query.get("ref", ["SW000"])[0]
            
            bids = [b.strip() for b in bundle_raw.split(",") if b.strip()]
            props = []
            for bid in bids:
                found = find_property_by_id_or_code(bid)
                if found:
                    props.append(found)
            
            flex = build_property_flex_carousel(props, client_name=client_name, agent_ref=agent_ref)
            if flex:
                self._send_json(200, {"status": "success", "count": len(props), "flex": flex})
            else:
                self._send_json(404, {"error": "No properties found for given bundle IDs", "bundle": bids})
            return

        if path == "/api/presence/heartbeat":
            s = self._session()
            if s and s.get("sub"):
                sub = s["sub"]
                store = load_lobby_data()
                mem = next((a for a in store.get("approved", []) if a.get("lineUserId") == sub), None)
                if mem:
                    mem["last_active_at"] = int(time.time())
                    save_lobby_data(store)
            self._send_json(200, {"ok": True, "now": int(time.time())})
            return

        if path == "/api/lobby/snapshots":
            acting = self._require("admin")
            if not acting:
                return
            snaps = []
            try:
                cur = _fetch_r2_json(_R2_LOBBY_SNAP_INDEX_KEY, timeout=8)
                if isinstance(cur, list):
                    snaps = cur
            except Exception:
                pass
            self._send_json(200, {"status": "success", "snapshots": snaps})
            return

        if path == "/api/lobby/list":
            acting = self._require("admin")
            if not acting:
                return
            store = load_lobby_data()
            # Mark acting member as online
            acting_id = acting.get("id")
            for a in store.get("approved", []):
                if a.get("id") == acting_id:
                    a["last_active_at"] = int(time.time())
                    break
            self._send_json(200, sanitize_store_for_admin(store))
            return

        if path == "/api/lobby/status":
            self._send_json(410, {"error": "deprecated: use /api/auth/me"})
            return

        if path == "/api/agent/public-card":
            ref_q = (query.get("ref", [""])[0] or "").strip().upper()
            if not ref_q:
                self._send_json(200, {"found": False})
                return
            store = load_lobby_data()
            hit = next(
                (a for a in store.get("approved", [])
                 if str(a.get("code") or "").strip().upper() == ref_q
                 or str(a.get("id") or "").strip().upper() == ref_q),
                None,
            )
            perms = (hit.get("permissions") or {}) if hit else {}
            rc = str((hit or {}).get("role_code") or "").upper()
            if not hit or perms.get("vipClient") or perms.get("sellerClient") or rc in ("VIP_CLIENT", "SELLER"):
                self._send_json(200, {"found": False})
                return
            self._send_json(200, {
                "found": True,
                "agent": {
                    "code": hit.get("code") or hit.get("id") or ref_q,
                    "name": hit.get("name") or "",
                    "nickname": hit.get("nickname") or "",
                    "phone": hit.get("phone") or "",
                    "line_id": hit.get("line_id") or hit.get("lineId") or "",
                    "avatar": hit.get("avatar") or hit.get("picture") or "",
                },
            })
            return

        if path == "/api/bug-report/list":
            acting = self._require("admin")
            if not acting:
                return
            self._send_json(200, {"status": "ok", "reports": _load_bug_reports()})
            return

        if path == "/api/stats/daily-active":
            acting = self._require("admin")
            if not acting:
                return
            stats = _load_daily_stats()
            days = [{"date": k, **stats[k]} for k in sorted(stats.keys(), reverse=True)[:30]]
            self._send_json(200, {"status": "ok", "days": days})
            return

        if path == "/api/auth/me":
            s = self._session()
            if not s or not s.get("sub"):
                self._send_json(401, {"error": "no session"})
                return
            sub = s["sub"]
            store = load_lobby_data()
            ensure_super_tech_seat(store, sub, s.get("name", ""), s.get("picture", ""))
            line_info = {"userId": sub, "name": s.get("name", ""), "picture": s.get("picture", "")}
            mem = next((a for a in store.get("approved", []) if a.get("lineUserId") == sub), None)
            if mem:
                mem["last_active_at"] = int(time.time())
                _record_daily_active(mem, store)
                save_lobby_data(store)
                is_adm = is_admin_member(mem)
                me_payload = {
                    "status": "approved",
                    "member": sanitize_member(mem),
                    "isAdmin": is_adm,
                    "line": line_info,
                }
                if is_adm:
                    me_payload["lobbyPendingCount"] = len(store.get("pending", []))
                self._send_json(200, me_payload)
                return
            pend = next((a for a in store.get("pending", []) if a.get("lineUserId") == sub), None)
            if pend:
                self._send_json(200, {"status": "pending", "applicant": sanitize_member(pend), "line": line_info})
                return
            sellers_store = load_sellers_data()
            seller = next((x for x in sellers_store.get("sellers", []) if x.get("lineUserId") == sub), None)
            if seller:
                self._send_json(200, {
                    "status": "seller",
                    "seller": {
                        "id": seller.get("id"),
                        "role": "seller",
                        "name": seller.get("name", s.get("name", "")),
                        "picture": seller.get("picture", s.get("picture", "")),
                        "phone": seller.get("phone", ""),
                    },
                    "line": line_info,
                })
                return
            revoked_rb = next(
                (
                    rb for rb in store.get("rollback_history", [])
                    if rb.get("action") == "REVOKE"
                    and isinstance(rb.get("member"), dict)
                    and rb["member"].get("lineUserId") == sub
                ),
                None,
            )
            guest_payload = {"status": "guest", "line": line_info}
            if revoked_rb:
                guest_payload["revoked"] = True
                guest_payload["revokedAt"] = revoked_rb.get("timestamp", "")
            self._send_json(200, guest_payload)
            return

        if path == "/api/seller/my-listings":
            s = self._session()
            if not s or not s.get("sub"):
                self._send_json(401, {"error": "กรุณาเข้าสู่ระบบด้วย LINE"})
                return
            sub = s["sub"]
            sellers_store = load_sellers_data()
            seller = next((x for x in sellers_store.get("sellers", []) if x.get("lineUserId") == sub), None)
            seller_phone = (seller or {}).get("phone", "").strip()

            with LISTING_INTAKE_LOCK:
                intake_store = load_intake_data()
                my_intakes = [
                    _sanitize_intake_for_seller(it)
                    for it in intake_store.get("intakes", [])
                    if it.get("seller_line_id") == sub
                    or it.get("submitted_by_line_id") == sub
                    or (seller_phone and it.get("phone", "").strip() == seller_phone)
                ]
            with CONTRACTS_LOCK:
                contract_store = load_contracts_data()
                my_contracts = [
                    _sanitize_contract_for_seller(c)
                    for c in contract_store.get("contracts", [])
                    if c.get("seller_line_id") == sub
                    or (seller_phone and (c.get("seller_phone") or c.get("phone") or "").strip() == seller_phone)
                ]
            self._send_json(200, {
                "status": "success",
                "role": "seller",
                "intakes": my_intakes,
                "contracts": my_contracts,
            })
            return

        if path == "/api/auth/line/start":
            if not LINE_LOGIN_CHANNEL_ID or not LINE_LOGIN_CHANNEL_SECRET:
                self._send_json(503, {"error": "LINE Login ยังไม่ได้ตั้งค่าบนเซิร์ฟเวอร์"})
                return
            ret = query.get("return", ["register"])[0]
            if ret not in FRONTEND_URLS:
                ret = "register"
            nonce = secrets.token_urlsafe(16)
            state = make_token({"n": nonce, "r": ret}, 600)
            params = urllib.parse.urlencode({
                "response_type": "code",
                "client_id": LINE_LOGIN_CHANNEL_ID,
                "redirect_uri": PUBLIC_BASE_URL + "/api/auth/line/callback",
                "state": state,
                "scope": "profile openid",
                "nonce": nonce,
            })
            self._redirect(
                "https://access.line.me/oauth2/v2.1/authorize?" + params,
                "line_state=" + nonce + "; HttpOnly; Secure; SameSite=Lax; Path=/api/auth/line; Max-Age=600",
            )
            return

        if path == "/api/auth/line/callback":
            clear_cookie = "line_state=; HttpOnly; Secure; SameSite=Lax; Path=/api/auth/line; Max-Age=0"
            code = query.get("code", [""])[0]
            st = verify_token(query.get("state", [""])[0])
            cm = re.search(r"line_state=([^;]+)", self.headers.get("Cookie", ""))
            if not code or not st or not cm or not hmac.compare_digest(cm.group(1), st.get("n", "")):
                self._redirect(FRONTEND_URLS["register"] + "#auth_error=state", clear_cookie)
                return
            try:
                tok = _http_post_form("https://api.line.me/oauth2/v2.1/token", {
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": PUBLIC_BASE_URL + "/api/auth/line/callback",
                    "client_id": LINE_LOGIN_CHANNEL_ID,
                    "client_secret": LINE_LOGIN_CHANNEL_SECRET,
                })
                prof = _http_post_form("https://api.line.me/oauth2/v2.1/verify", {
                    "id_token": tok["id_token"],
                    "client_id": LINE_LOGIN_CHANNEL_ID,
                    "nonce": st.get("n", ""),
                })
                sub = prof["sub"]
                name = prof.get("name", "")
                picture = prof.get("picture", "")
            except Exception as e:
                print(f"[LINE Login] token/verify failed: {e}")
                self._redirect(FRONTEND_URLS[st.get("r", "register")] + "#auth_error=line", clear_cookie)
                return

            # Bootstrap: designated super admin LINE ids get linked to the Tech Architect seat
            store = load_lobby_data()
            if sub in SUPER_ADMIN_LINE_USER_IDS and not any(a.get("lineUserId") == sub for a in store.get("approved", [])):
                seat = next((a for a in store.get("approved", []) if a.get("id") == "app_office_004" and not a.get("lineUserId")), None)
                if seat:
                    seat["lineUserId"] = sub
                    store.setdefault("audit_log", []).insert(0, f"[{bkk_now().strftime('%Y-%m-%d %H:%M:%S')}] 🔗 ผูก LINE ผู้ดูแลระบบสูงสุด: {seat.get('name')}")
                    save_lobby_data(store)

            # Zero-Day Defense Auto-Heal on LINE Login OAuth callback
            try:
                auto_heal_member_line_profile(sub, {"displayName": name, "pictureUrl": picture})
            except Exception as _cb_e:
                print(f"[LINE Login Auto-Heal Warn]: {_cb_e}")
            if st.get("r") == "seller":
                try:
                    upsert_seller_account(sub, name=name, picture=picture)
                except Exception as _sl_e:
                    print(f"[Seller Upsert Warn]: {_sl_e}")
            session = make_token({"sub": sub, "name": name, "picture": picture}, SESSION_TTL)
            self._redirect(FRONTEND_URLS[st.get("r", "register")] + "#session=" + session, clear_cookie)
            return

        if path in ["/logs", "/api/export-logs"]:
            secret = query.get("secret", [""])[0]
            client_ip = self.client_address[0] if hasattr(self, 'client_address') else ''
            forwarded_for = (self.headers.get("X-Forwarded-For") or "").strip()
            is_local = (client_ip in ["127.0.0.1", "localhost", "::1"]) and (not os.environ.get("PORT")) and (not forwarded_for)
            configured_secret = os.environ.get("ADMIN_EXPORT_SECRET", "").strip()
            is_secret_ok = bool(secret and configured_secret and hmac.compare_digest(secret, configured_secret))
            is_sess_admin = False
            if not (is_local or is_secret_ok):
                s = self._session()
                if s and s.get("sub"):
                    lobby = load_lobby_data()
                    acting = next((a for a in lobby.get("approved", []) if a.get("lineUserId") == s.get("sub")), None)
                    if acting and is_admin_member(acting):
                        is_sess_admin = True

            # Security verification
            if not (is_local or is_secret_ok or is_sess_admin):
                self.send_response(401)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unauthorized. Invalid admin secret."}, ensure_ascii=False).encode('utf-8'))
                return

            store = load_chat_logs()
            convs = store.get("conversations", [])

            # Filter by Days (e.g. 7, 30)
            days_str = query.get("days", ["all"])[0]
            if days_str.isdigit():
                max_days = int(days_str)
                now_ts = time.time()
                cutoff_ts = now_ts - (max_days * 86400)
                filtered = []
                for c in convs:
                    try:
                        c_dt = datetime.strptime(c.get("timestamp", ""), "%Y-%m-%d %H:%M:%S").replace(tzinfo=TH_TZ)
                        if c_dt.timestamp() >= cutoff_ts:
                            filtered.append(c)
                    except Exception:
                        filtered.append(c)
                convs = filtered

            # Filter by Category
            cat = query.get("category", ["all"])[0].lower()
            if cat == "property":
                convs = [c for c in convs if c.get("matched_codes") or "บ้าน" in c.get("user_text", "") or "คอนโด" in c.get("user_text", "")]
            elif cat == "workflow":
                convs = [c for c in convs if any(w in c.get("user_text", "") for w in ["เปิดบ้าน", "กุญแจ", "จองคิว", "otp", "keybox"])]

            # Filter by PII Masking (Mask phone numbers for PDPA safety)
            mask_pii = query.get("mask_pii", ["true"])[0].lower() in ["true", "1", "yes"]
            if mask_pii:
                masked_convs = []
                for c in convs:
                    c_copy = dict(c)
                    # Mask 10-digit phone in user text or ai reply
                    for field in ["user_text", "ai_reply"]:
                        val = c_copy.get(field, "")
                        val = re.sub(r'\b(0\d{2})[-.\s]?(\d{3,4})[-.\s]?(\d{4})\b', r'\1-XXX-\3', val)
                        c_copy[field] = val
                    masked_convs.append(c_copy)
                convs = masked_convs

            export_data = {
                "bot_name": store.get("bot_name", "Siwasupagent"),
                "export_time": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_exported": len(convs),
                "filter_criteria": {
                    "days": days_str,
                    "category": cat,
                    "pii_masked": mask_pii
                },
                "conversations": convs
            }

            body = json.dumps(export_data, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"<h1>Siwasup Line-Gemini Webhook v2 (Smart Context & Exact Property Match) is Running!</h1>")

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        ADMIN_POST_LEVELS = {
            "/api/lobby/approve": "lobby_approver",
            "/api/lobby/reject": "lobby_approver",
            "/api/lobby/revoke": "admin",
            "/api/lobby/rollback": "admin",
            "/api/lobby/backup": "admin",
            "/api/lobby/snapshots/restore": "admin",
            "/api/lobby/update-permissions": "exec",
        }
        acting_member = None
        if path in ADMIN_POST_LEVELS:
            acting_member = self._require(ADMIN_POST_LEVELS[path])
            if not acting_member:
                return

        if path == "/api/track/view":
            try:
                client_ip = (
                    (self.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
                    or (self.client_address[0] if hasattr(self, "client_address") and self.client_address else "")
                )
                if not _check_track_ip_rate(client_ip):
                    self._send_json(429, {"status": "rate_limited", "error": "Too many tracking requests"})
                    return
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length <= 0 or content_length > 16384:
                    self._send_json(400, {"error": "Invalid payload size"})
                    return
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                if not isinstance(payload, dict):
                    self._send_json(400, {"error": "Invalid JSON object"})
                    return
                res = record_client_tracking_event(payload)
                self._send_json(200, res)
            except Exception as e:
                self._send_json(400, {"status": "error", "message": str(e)})
            return

        if path == "/api/track/tag":
            try:
                client_ip = (
                    (self.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
                    or (self.client_address[0] if hasattr(self, "client_address") and self.client_address else "")
                )
                if not _check_track_ip_rate(client_ip):
                    self._send_json(429, {"status": "rate_limited", "error": "Too many tracking requests"})
                    return
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length <= 0 or content_length > 4096:
                    self._send_json(400, {"error": "Invalid payload size"})
                    return
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                if not isinstance(payload, dict):
                    self._send_json(400, {"error": "Invalid JSON object"})
                    return
                avatar_name = re.sub(r"[\t\r\n]+", " ", str(payload.get("avatar_name") or payload.get("name") or "")).strip()[:25]
                agent_note = re.sub(r"[\t\r\n]+", " ", str(payload.get("agent_note") or payload.get("note") or "")).strip()[:60]
                if not avatar_name:
                    self._send_json(400, {"status": "error", "error": "Missing avatar_name"})
                    return
                tok = encode_client_tag(avatar_name, agent_note)
                self._send_json(200, {"status": "ok", "t": tok, "avatar_name": avatar_name})
            except Exception as e:
                self._send_json(400, {"status": "error", "message": str(e)})
            return

        if path == "/api/track/choose-agent":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length <= 0 or content_length > 4096:
                    self._send_json(400, {"error": "Invalid payload size"})
                    return
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                raw_vid = re.sub(r"[^A-Z0-9\-]", "", str(payload.get("vid") or "").strip().upper())[:24]
                chosen_ref = re.sub(r"[^A-Za-z0-9_\-]", "", str(payload.get("chosen_ref") or "").strip().upper())[:24]
                if not raw_vid or not chosen_ref:
                    self._send_json(400, {"error": "Missing vid or chosen_ref"})
                    return
                with CLIENT_TRACKING_LOCK:
                    store = load_client_tracking_data()
                    visitors = store.setdefault("visitors", {})
                    if raw_vid not in visitors:
                        self._send_json(404, {"error": "Visitor not found"})
                        return
                    root_vid = _resolve_root_visitor(visitors, raw_vid)
                    vis = visitors[root_vid]
                    _sync_lock_expiry(vis, bkk_now())
                    lk = vis.get("lock") or {}
                    if lk.get("status") == "booked":
                        self._send_json(409, {"error": "ลูกค้าจองบ้านแล้ว ไม่สามารถเปลี่ยนเซลล์ผู้ดูแลได้"})
                        return
                    cands = [str(c).upper() for c in (lk.get("conflict_candidates") or [])]
                    if chosen_ref not in cands:
                        self._send_json(400, {"error": "ตัวแทนที่เลือกไม่อยู่ในรายการที่ชนกัน"})
                        return
                    now_str = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                    lk["owner_ref"] = chosen_ref
                    lk["status"] = "active"
                    lk["conflict_candidates"] = []
                    lk["chosen_by_client_at"] = now_str
                    lk.setdefault("history", []).append({"action": "CLIENT_CHOSE", "ref": chosen_ref, "at": now_str})
                    vis["lock"] = lk
                    save_client_tracking_data(store)
                self._send_json(200, {"status": "ok", "root_vid": root_vid, "owner_ref": chosen_ref, "lock": lk})
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        if path == "/api/track/lock-booking":
            acting = self._require("admin")
            if not acting:
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                raw_vid = re.sub(r"[^A-Z0-9\-]", "", str(payload.get("vid") or "").strip().upper())[:24]
                prop_id = re.sub(r"[^A-Za-z0-9_\-]", "", str(payload.get("property_id") or "").strip())[:40]
                owner_ref = re.sub(r"[^A-Za-z0-9_\-]", "", str(payload.get("owner_ref") or "").strip().upper())[:24]
                if not raw_vid:
                    self._send_json(400, {"error": "Missing vid"})
                    return
                with CLIENT_TRACKING_LOCK:
                    store = load_client_tracking_data()
                    visitors = store.setdefault("visitors", {})
                    if raw_vid not in visitors:
                        self._send_json(404, {"error": "Visitor not found"})
                        return
                    root_vid = _resolve_root_visitor(visitors, raw_vid)
                    vis = visitors[root_vid]
                    lk = vis.setdefault("lock", {})
                    if lk.get("status") == "booked":
                        self._send_json(409, {"error": "เคสนี้จองแล้ว ไม่สามารถเปลี่ยนเซลล์ผู้ดูแลได้"})
                        return
                    now_str = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                    eff_owner = owner_ref or str(lk.get("owner_ref") or (vis.get("refs") or ["SW001"])[0]).upper()
                    lk["owner_ref"] = eff_owner
                    lk["status"] = "booked"
                    lk["booked_property_id"] = prop_id
                    lk["booked_at"] = now_str
                    lk["conflict_candidates"] = []
                    lk.setdefault("history", []).append({"action": "BOOKED", "ref": eff_owner, "property_id": prop_id, "by": acting.get("name", ""), "at": now_str})
                    save_client_tracking_data(store)
                self._send_json(200, {"status": "ok", "root_vid": root_vid, "lock": lk})
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        if path == "/api/track/extend-lock":
            acting = self._require("admin")
            if not acting:
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                raw_vid = re.sub(r"[^A-Z0-9\-]", "", str(payload.get("vid") or "").strip().upper())[:24]
                extra_days = int(payload.get("extra_days") or 15)
                extra_days = max(1, min(30, extra_days))
                reason = str(payload.get("reason") or "").strip()[:150]
                if not raw_vid or not reason:
                    self._send_json(400, {"error": "กรุณาระบุรหัสเครื่อง (vid) และเหตุผลในการต่ออายุล็อก"})
                    return
                with CLIENT_TRACKING_LOCK:
                    store = load_client_tracking_data()
                    visitors = store.setdefault("visitors", {})
                    if raw_vid not in visitors:
                        self._send_json(404, {"error": "Visitor not found"})
                        return
                    root_vid = _resolve_root_visitor(visitors, raw_vid)
                    vis = visitors[root_vid]
                    now_dt = bkk_now()
                    _sync_lock_expiry(vis, now_dt)
                    lk = vis.setdefault("lock", {})
                    if lk.get("status") == "booked":
                        self._send_json(200, {"status": "ok", "note": "เคสนี้จองแล้ว (ล็อกถาวร)", "lock": lk})
                        return
                    base_dt = _parse_bkk_dt(lk.get("expires_at"))
                    if not base_dt or base_dt < now_dt:
                        base_dt = now_dt
                    new_exp = (base_dt + timedelta(days=extra_days)).strftime("%Y-%m-%d %H:%M:%S")
                    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
                    lk["expires_at"] = new_exp
                    lk["extended_days"] = int(lk.get("extended_days") or 0) + extra_days
                    lk["extended_by"] = str(acting.get("nickname") or acting.get("name") or acting.get("code") or "")
                    lk["extend_reason"] = reason
                    if not lk.get("owner_ref") and vis.get("refs"):
                        lk["owner_ref"] = str(vis["refs"][-1]).upper()
                    lk["status"] = "active"
                    lk.setdefault("history", []).append({"action": "ADMIN_EXTEND", "days": extra_days, "reason": reason, "by": lk["extended_by"], "at": now_str})
                    save_client_tracking_data(store)
                self._send_json(200, {"status": "ok", "root_vid": root_vid, "lock": lk})
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return

        if path == "/api/content/save":
            acting = self._require("member")
            if not acting:
                return
            if not _is_content_editor(acting):
                self._send_json(403, {"error": "เฉพาะผู้ดูแลคอนเทนต์ (Poppy / Admin) เท่านั้น"})
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length <= 0 or content_length > 512 * 1024:
                    self._send_json(400, {"error": "Invalid payload size"})
                    return
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                action = str(payload.get("action") or "upsert").strip()
                actor_name = str(acting.get("nickname") or acting.get("name") or acting.get("code") or "Poppy").strip()
                with CONTENT_HUB_LOCK:
                    store = load_content_data()
                    items = list(store.get("items", []))
                    cid = re.sub(r"[^A-Za-z0-9_-]", "", str(payload.get("id") or "").strip())
                    if action in ("delete", "trash", "restore"):
                        if not cid:
                            self._send_json(400, {"error": "กรุณาระบุรหัสคอนเทนต์ที่ต้องการดำเนินการ"})
                            return
                        if action == "trash":
                            found = None
                            for it in items:
                                if it.get("id") == cid:
                                    it["prev_status"] = it.get("status") if it.get("status") != "trash" else it.get("prev_status", "draft")
                                    it["status"] = "trash"
                                    it["trashed_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                                    it["trashed_by"] = actor_name
                                    found = it
                                    break
                            if not found:
                                self._send_json(404, {"error": "ไม่พบคอนเทนต์ที่ต้องการย้ายลงถังขยะ"})
                                return
                            store["items"] = items
                            save_content_data(store)
                            self._send_json(200, {"status": "success", "trashed": cid, "item": found})
                            return
                        if action == "restore":
                            found = None
                            for it in items:
                                if it.get("id") == cid:
                                    it["status"] = it.pop("prev_status", "draft") or "draft"
                                    it.pop("trashed_at", None)
                                    it.pop("trashed_by", None)
                                    it["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                                    it["updated_by"] = actor_name
                                    found = it
                                    break
                            if not found:
                                self._send_json(404, {"error": "ไม่พบคอนเทนต์ในถังขยะ"})
                                return
                            store["items"] = items
                            save_content_data(store)
                            self._send_json(200, {"status": "success", "restored": cid, "item": found})
                            return
                        store["items"] = [it for it in items if it.get("id") != cid]
                        save_content_data(store)
                        self._send_json(200, {"status": "success", "deleted": cid})
                        return
                    cover_image = str(payload.get("cover_image") or "").strip()[:500]
                    if cover_image and not re.match(r"^https?://", cover_image, re.IGNORECASE):
                        self._send_json(400, {"error": "URL รูปภาพต้องขึ้นต้นด้วย http:// หรือ https://"})
                        return
                    title = str(payload.get("title") or "").strip()[:160]
                    if not title:
                        self._send_json(400, {"error": "กรุณาระบุหัวข้อคอนเทนต์"})
                        return
                    aud = str(payload.get("audience") or "public").strip().lower()
                    if aud not in ("public", "agent", "both"):
                        aud = "public"
                    cat = str(payload.get("category") or "article").strip().lower()
                    if cat not in ("just_sold", "howto", "article", "news", "top_agent", "announcement", "meeting"):
                        cat = "article" if aud == "public" else "announcement"
                    st = str(payload.get("status") or "published").strip().lower()
                    if st not in ("draft", "published", "archived"):
                        st = "published"
                    now_str = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                    if not cid:
                        cid = f"CNT-{bkk_now().strftime('%Y%m%d')}-{secrets.token_hex(2).upper()}"
                    existing = next((it for it in items if it.get("id") == cid), None)
                    item_obj = {
                        "id": cid,
                        "audience": aud,
                        "category": cat,
                        "title": title,
                        "summary": str(payload.get("summary") or "").strip()[:300],
                        "body": str(payload.get("body") or "").strip()[:10000],
                        "cover_image": cover_image,
                        "status": st,
                        "pinned": bool(payload.get("pinned")),
                        "published_at": (existing.get("published_at") if existing else "") or (now_str if st == "published" else ""),
                        "author_name": (existing.get("author_name") if existing else "") or actor_name,
                        "updated_at": now_str,
                        "updated_by": actor_name,
                    }
                    items = [it for it in items if it.get("id") != cid]
                    items.insert(0, item_obj)
                    store["items"] = items[:500]
                    save_content_data(store)
                self._send_json(200, {"status": "success", "item": item_obj})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if path == "/api/content/upload-image":
            acting = self._require("member")
            if not acting:
                return
            if not _is_content_editor(acting):
                self._send_json(403, {"error": "เฉพาะผู้ดูแลคอนเทนต์ (Poppy / Admin) เท่านั้น"})
                return
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0 or content_length > 12 * 1024 * 1024:
                self._send_json(400, {"error": "ไฟล์ใหญ่เกินกำหนด (สูงสุด 8MB)"})
                return
            try:
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                data_url = str(payload.get("data_url") or "")
                if ";base64," not in data_url:
                    self._send_json(400, {"error": "รูปแบบไฟล์ไม่ถูกต้อง"})
                    return
                raw_b64 = data_url.split(";base64,", 1)[1]
                file_bytes = base64.b64decode(raw_b64, validate=True)
                if len(file_bytes) == 0 or len(file_bytes) > 8 * 1024 * 1024:
                    self._send_json(400, {"error": "ขนาดไฟล์ต้องไม่เกิน 8MB"})
                    return
                ext, ctype = None, None
                if file_bytes.startswith(b"\xff\xd8\xff"):
                    ext, ctype = "jpg", "image/jpeg"
                elif file_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                    ext, ctype = "png", "image/png"
                elif file_bytes[:4] == b"RIFF" and file_bytes[8:12] == b"WEBP":
                    ext, ctype = "webp", "image/webp"
                if not ext:
                    self._send_json(400, {"error": "รองรับเฉพาะไฟล์ JPG, PNG, WebP เท่านั้น"})
                    return
                if not put_object_r2:
                    self._send_json(500, {"error": "R2 storage not available"})
                    return
                r2_key = f"content_uploads/cnt_{int(time.time())}_{secrets.token_hex(4)}.{ext}"
                status_r2 = put_object_r2(r2_key, file_bytes, ctype)
                if status_r2 not in (200, 201, 204):
                    self._send_json(502, {"error": f"R2 upload failed ({status_r2})"})
                    return
                self._send_json(200, {"status": "success", "url": f"https://assets.siwasup.com/{r2_key}"})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if path == "/api/ocr/contract":
            acting = self._require("member")
            if not acting:
                return
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0 or content_length > 10 * 1024 * 1024:
                self._send_json(400, {"error": "Invalid payload size"})
                return
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                doc_type = payload.get("doc_type", "id_card")
                img_b64 = payload.get("image_base64", "")
                mime_type = payload.get("mime_type", "image/jpeg")
                if not img_b64:
                    self._send_json(400, {"error": "Missing image_base64 parameter"})
                    return
                ocr_result = extract_contract_ocr(img_b64, doc_type=doc_type, mime_type=mime_type)
                self._send_json(200, {
                    "status": "success",
                    "doc_type": doc_type,
                    "data": ocr_result
                })
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/contracts/save":
            acting = self._require("member")
            if not acting:
                return
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0 or content_length > 2 * 1024 * 1024:
                self._send_json(400, {"error": "Invalid payload size"})
                return
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                with CONTRACTS_LOCK:
                    store = load_contracts_data()
                    contracts = store.setdefault("contracts", [])
                    cid = payload.get("id") or f"SW-CNT-{int(time.time()*1000)%1000000}"
                    existing = next((c for c in contracts if c.get("id") == cid), None)
                    if existing and not is_admin_member(acting):
                        my_refs = {str(acting.get("code") or "").strip(), str(acting.get("id") or "").strip(), str(acting.get("lineUserId") or "").strip()}
                        my_refs.discard("")
                        is_owner = (
                            existing.get("submitted_by_line_id") == acting.get("lineUserId")
                            or existing.get("submitted_by_ref") in my_refs
                            or existing.get("agent_ref") in my_refs
                            or existing.get("agent_id") in my_refs
                        )
                        if not is_owner:
                            self._send_json(403, {"error": "ไม่มีสิทธิ์แก้ไขสัญญาของตัวแทนท่านอื่น"})
                            return
                    payload["id"] = cid
                    payload["saved_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                    payload["submitted_by_ref"] = acting.get("code") or acting.get("id") or ""
                    payload["submitted_by_name"] = acting.get("nickname") or acting.get("name") or ""
                    payload["submitted_by_line_id"] = acting.get("lineUserId") or ""
                    # Expiry calculation (from contract_date + contract_days, default 90 days)
                    days = max(1, int(payload.get("contract_days") or 90))
                    base_dt = bkk_now()
                    cdate_str = str(payload.get("contract_date") or "").strip()
                    if cdate_str:
                        try:
                            base_dt = datetime.strptime(cdate_str[:10], "%Y-%m-%d").replace(tzinfo=TH_TZ)
                        except Exception:
                            pass
                    payload["expires_at"] = (base_dt + timedelta(days=days)).strftime("%Y-%m-%d")

                    # Replace or prepend
                    contracts = [c for c in contracts if c.get("id") != cid]
                    contracts.insert(0, payload)
                    store["contracts"] = contracts
                    save_contracts_data(store)

                # Two-way sync back to Consignment Vault (outside CONTRACTS_LOCK to prevent nested locks)
                linked_pid = str(payload.get("property_id") or "").strip()
                if linked_pid:
                    role = _consignment_role(acting)
                    actor_name = str(acting.get("nickname") or acting.get("name") or acting.get("code") or "").strip()
                    with CONSIGNMENT_DEMO_LOCK:
                        cstore = load_consignment_data()
                        cprops = list(cstore.get("properties", []))
                        tprop = next((x for x in cprops if str(x.get("id") or "").strip() == linked_pid), None)
                        if tprop and (role in ("founder", "staff") or _is_consignment_owner(tprop, acting)):
                            ctype = "exclusive_contract" if str(payload.get("contract_type") or "") == "exclusive" else "open_contract"
                            tprop["consignment_type"] = ctype
                            tprop["contract_expiry"] = payload["expires_at"]
                            if role == "founder":
                                tprop["contract_verified"] = True
                            tprop["linked_contract_id"] = cid
                            for f_key in ("owner_phone", "deed_no", "land_no", "survey_page", "survey_no", "project_name", "house_no", "subdistrict", "district"):
                                if payload.get(f_key) is not None and str(payload.get(f_key)).strip():
                                    tprop[f_key] = str(payload.get(f_key)).strip()
                            if payload.get("survey_no") and not tprop.get("survey_page"):
                                tprop["survey_page"] = str(payload.get("survey_no")).strip()
                            tprop["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                            tprop["updated_by"] = actor_name
                            cstore["properties"] = cprops
                            cstore["updated_by"] = actor_name
                            save_consignment_data(cstore)
                self._send_json(200, {"status": "success", "contract": payload})
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/consignment/save":
            acting = self._require("member")
            if not acting:
                return
            role = _consignment_role(acting)
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0 or content_length > 5 * 1024 * 1024:
                self._send_json(400, {"error": "Invalid payload size (max 5MB)"})
                return
            try:
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                action = str(payload.get("action") or "save_all").strip()
                actor_name = str(acting.get("nickname") or acting.get("name") or acting.get("code") or "").strip()
                actor_id = str(acting.get("id") or "").strip()
                actor_code = str(acting.get("code") or "").strip().upper()
                with CONSIGNMENT_DEMO_LOCK:
                    if action == "upsert_property":
                        prop = payload.get("property")
                        is_new = bool(payload.get("is_new"))
                        if not isinstance(prop, dict) or (not is_new and not str(prop.get("id") or "").strip()):
                            self._send_json(400, {"error": "Missing property object or id"})
                            return
                        store = load_consignment_data()
                        props = list(store.get("properties", []))
                        if is_new:
                            max_num = 2600
                            for x in props:
                                m = re.match(r"^SWC-(\d+)$", str(x.get("id") or "").strip(), re.IGNORECASE)
                                if m:
                                    n = int(m.group(1))
                                    if n > max_num:
                                        max_num = n
                            pid = f"SWC-{max_num + 1}"
                            prop["id"] = pid
                            existing_idx = None
                            existing = None
                        else:
                            pid = str(prop.get("id")).strip()
                            existing_idx = next((i for i, x in enumerate(props) if str(x.get("id") or "").strip() == pid), None)
                            existing = props[existing_idx] if existing_idx is not None else None
                        if not prop.get("office_post_commission"):
                            prop["office_post_commission"] = 1
                        if role == "agent":
                            if existing is not None and not _is_consignment_owner(existing, acting):
                                self._send_json(403, {"error": "ไม่มีสิทธิ์แก้ไขทรัพย์ของผู้อื่น"})
                                return
                            prop["submitted_by_id"] = existing.get("submitted_by_id") if existing else actor_id
                            prop["submitted_by_code"] = existing.get("submitted_by_code") if existing else actor_code
                            prop["submitted_by_name"] = existing.get("submitted_by_name") if existing else actor_name
                            prop["assigned_agent_code"] = existing.get("assigned_agent_code", "") if existing else actor_code
                            prop["assigned_agent_name"] = existing.get("assigned_agent_name", "") if existing else actor_name
                            if is_new or (existing and existing.get("status") == "pending_gool_approval"):
                                prop["status"] = "pending_gool_approval"
                            elif str(prop.get("status") or "") not in ("pending_photos", "ready_for_review", "pending_gool_approval"):
                                prop["status"] = "pending_photos" if not (prop.get("images") or []) else "ready_for_review"
                        elif role == "staff":
                            if existing and existing.get("status") == "pending_gool_approval" and str(prop.get("status") or "") != "pending_gool_approval":
                                prop["status"] = "pending_gool_approval"
                            elif str(prop.get("status") or "") == "available" and (not existing or existing.get("status") != "available"):
                                prop["status"] = "ready_for_review"
                        elif role == "founder":
                            prev_status = existing.get("status") if existing else ""
                            next_status = str(prop.get("status") or "")
                            if prev_status == "pending_gool_approval" and next_status != "pending_gool_approval" and not _is_gool_approver(acting):
                                self._send_json(403, {"error": "เฉพาะคุณกูล (SW001) เท่านั้นที่อนุมัติบ้านใหม่จากเซลล์ได้"})
                                return
                            if next_status == "available" and prev_status != "available" and not _is_bua_publisher(acting):
                                self._send_json(403, {"error": "เฉพาะคุณบัว (SA001) เท่านั้นที่กดปล่อยบ้านออก Public ได้"})
                                return
                        if role != "founder":
                            prop["contract_verified"] = bool(existing.get("contract_verified")) if existing else False
                        prop["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                        prop["updated_by"] = actor_name
                        if existing_idx is not None:
                            props[existing_idx] = prop
                        else:
                            props.insert(0, prop)
                        store["properties"] = props
                        store["updated_by"] = actor_name
                        save_consignment_data(store)
                        visible_count = len([p for p in props if _is_consignment_owner(p, acting)]) if role == "agent" else len(props)
                        self._send_json(200, {
                            "status": "success",
                            "updated_at": store.get("updated_at", ""),
                            "updated_by": store.get("updated_by", ""),
                            "count": visible_count,
                            "property": prop,
                        })
                        return

                    if role != "founder":
                        self._send_json(403, {"error": "คำสั่งนี้จำกัดเฉพาะผู้บริหาร"})
                        return
                    if action == "reset_seed":
                        store = _default_consignment_store()
                        store["updated_by"] = f"reset:{actor_name}"
                        save_consignment_data(store)
                    else:
                        props = payload.get("properties")
                        if not isinstance(props, list):
                            self._send_json(400, {"error": "Missing properties list"})
                            return
                        store = load_consignment_data()
                        store["properties"] = props
                        store["updated_by"] = actor_name
                        save_consignment_data(store)
                self._send_json(200, {
                    "status": "success",
                    "updated_at": store.get("updated_at", ""),
                    "updated_by": store.get("updated_by", ""),
                    "count": len(store.get("properties", [])),
                    "properties": store.get("properties", []) if action == "reset_seed" else None,
                })
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/consignment/upload":
            acting = self._require("member")
            if not acting:
                return
            role = _consignment_role(acting)
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0 or content_length > 12 * 1024 * 1024:
                self._send_json(400, {"error": "ไฟล์ใหญ่เกินกำหนด (สูงสุด 8MB)"})
                return
            try:
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                pid = re.sub(r"[^A-Za-z0-9_-]", "", str(payload.get("property_id") or "").strip())
                kind = str(payload.get("kind") or "image").strip().lower()
                data_url = str(payload.get("data_url") or "")
                if not pid or kind not in ("image", "contract") or ";base64," not in data_url:
                    self._send_json(400, {"error": "ข้อมูลไฟล์ไม่ถูกต้อง"})
                    return
                if role == "agent":
                    store = load_consignment_data()
                    existing = next((x for x in store.get("properties", []) if str(x.get("id") or "").strip() == pid), None)
                    if existing is not None and not _is_consignment_owner(existing, acting):
                        self._send_json(403, {"error": "ไม่มีสิทธิ์อัปโหลดไฟล์เข้าทรัพย์ของผู้อื่น"})
                        return
                raw_b64 = data_url.split(";base64,", 1)[1]
                file_bytes = base64.b64decode(raw_b64, validate=True)
                if len(file_bytes) == 0 or len(file_bytes) > 8 * 1024 * 1024:
                    self._send_json(400, {"error": "ขนาดไฟล์ต้องไม่เกิน 8MB"})
                    return
                # Verify real magic bytes (anti-spoof)
                ext = None
                ctype = None
                if file_bytes.startswith(b"\xff\xd8\xff"):
                    ext, ctype = "jpg", "image/jpeg"
                elif file_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
                    ext, ctype = "png", "image/png"
                elif len(file_bytes) >= 12 and file_bytes[:4] == b"RIFF" and file_bytes[8:12] == b"WEBP":
                    ext, ctype = "webp", "image/webp"
                elif kind == "contract" and file_bytes.startswith(b"%PDF"):
                    ext, ctype = "pdf", "application/pdf"
                if not ext:
                    self._send_json(400, {"error": "รองรับเฉพาะไฟล์ JPG, PNG, WebP (และ PDF สำหรับสัญญา)"})
                    return
                if not put_object_r2:
                    self._send_json(503, {"error": "R2 storage not configured"})
                    return
                rand_hex = secrets.token_hex(8)
                if kind == "contract":
                    r2_key = f"_vault/consignment_contracts/{pid}_{rand_hex}.{ext}"
                    out_url = f"{PUBLIC_BASE_URL}/api/consignment/contract-file?key={urllib.parse.quote(r2_key)}"
                else:
                    r2_key = f"consignment_uploads/{pid}_{rand_hex}.{ext}"
                    out_url = f"https://assets.siwasup.com/{r2_key}"
                st = put_object_r2(r2_key, file_bytes, ctype)
                if int(st) not in (200, 201):
                    self._send_json(502, {"error": f"R2 upload failed ({st})"})
                    return
                self._send_json(200, {
                    "status": "success",
                    "url": out_url,
                    "r2_key": r2_key,
                    "content_type": ctype,
                    "size": len(file_bytes),
                })
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/intake/submit":
            try:
                client_ip = (
                    (self.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
                    or (self.client_address[0] if hasattr(self, "client_address") and self.client_address else "")
                )
                if not _check_intake_ip_rate(client_ip):
                    self._send_json(429, {"status": "rate_limited", "error": "ส่งข้อมูลถี่เกินไป กรุณารอสักครู่แล้วลองใหม่"})
                    return
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length <= 0 or content_length > 16384:
                    self._send_json(400, {"error": "Invalid payload size"})
                    return
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                if not isinstance(payload, dict):
                    self._send_json(400, {"error": "Invalid JSON object"})
                    return
                # Honeypot check
                if str(payload.get("_hp_website") or "").strip():
                    self._send_json(200, {"status": "success", "intake_id": "INTAKE-OK"})
                    return

                prop_type = str(payload.get("type") or "").strip()[:40]
                title = str(payload.get("title") or "").strip()[:200]
                price_raw = str(payload.get("price") or "").replace(",", "").strip()
                size = str(payload.get("size") or "-").strip()[:60]
                owner_name = str(payload.get("owner_name") or "").strip()[:100]
                phone = str(payload.get("phone") or "").strip()[:40]
                contract_mode = str(payload.get("contract_mode") or "unsure").strip()[:40]
                note = str(payload.get("note") or "").strip()[:500]
                if not title or not owner_name or not phone:
                    self._send_json(400, {"error": "กรุณากรอกข้อมูลทรัพย์ ชื่อ และเบอร์โทรศัพท์ให้ครบถ้วน"})
                    return
                try:
                    price_num = int(float(price_raw)) if price_raw else 0
                except Exception:
                    price_num = 0

                submitted_by_ref = str(payload.get("agent_ref") or "").strip()[:40]
                submitted_by_name = ""
                submitted_by_line_id = ""
                s = self._session()
                if s and s.get("sub"):
                    lobby = load_lobby_data()
                    mem = next((a for a in lobby.get("approved", []) if a.get("lineUserId") == s.get("sub")), None)
                    if mem:
                        submitted_by_ref = mem.get("code") or mem.get("id") or submitted_by_ref
                        submitted_by_name = mem.get("nickname") or mem.get("name") or ""
                        submitted_by_line_id = mem.get("lineUserId") or ""

                now_dt = bkk_now()
                intake_id = f"INTAKE-{now_dt.strftime('%Y%m%d')}-{int(time.time()*1000)%10000:04d}"
                item = {
                    "id": intake_id,
                    "type": prop_type or "บ้าน",
                    "title": title,
                    "price": f"{price_num:,}" if price_num > 0 else price_raw,
                    "price_num": price_num,
                    "size": size or "-",
                    "owner_name": owner_name,
                    "phone": phone,
                    "contract_mode": contract_mode,
                    "note": note,
                    "source": "agent_intake" if submitted_by_line_id else "public_consign",
                    "submitted_by_ref": submitted_by_ref,
                    "submitted_by_name": submitted_by_name,
                    "submitted_by_line_id": submitted_by_line_id,
                    "status": "pending_review",
                    "swc_code": "",
                    "review_note": "",
                    "created_at": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
                }

                with LISTING_INTAKE_LOCK:
                    store = load_intake_data()
                    intakes = store.setdefault("intakes", [])
                    intakes.insert(0, item)
                    save_intake_data(store)
                self._send_json(200, {"status": "success", "intake": item})
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/intake/review":
            acting = self._require("admin")
            if not acting:
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length <= 0 or content_length > 16384:
                    self._send_json(400, {"error": "Invalid payload size"})
                    return
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                intake_id = str(payload.get("id") or "").strip()
                action = str(payload.get("action") or "").strip()
                review_note = str(payload.get("review_note") or "").strip()[:500]
                if not intake_id or action not in ("approve", "need_revision", "reject", "archive"):
                    self._send_json(400, {"error": "Invalid id or action"})
                    return

                with LISTING_INTAKE_LOCK:
                    store = load_intake_data()
                    intakes = store.get("intakes", [])
                    target = next((it for it in intakes if it.get("id") == intake_id), None)
                    if not target:
                        self._send_json(404, {"error": "ไม่พบรายการฝากขายนี้"})
                        return

                    now_str = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                    if action == "approve":
                        target["status"] = "approved"
                        if not target.get("swc_code"):
                            seq = sum(1 for it in intakes if it.get("swc_code")) + 1
                            target["swc_code"] = f"SWC-{bkk_now().strftime('%y%m')}-{seq:03d}"
                    elif action == "need_revision":
                        target["status"] = "need_revision"
                    elif action == "reject":
                        target["status"] = "rejected"
                    elif action == "archive":
                        target["status"] = "archived"

                    target["review_note"] = review_note
                    target["reviewed_by"] = acting.get("nickname") or acting.get("name") or acting.get("code") or "Admin"
                    target["reviewed_at"] = now_str
                    target["updated_at"] = now_str
                    save_intake_data(store)
                self._send_json(200, {"status": "success", "intake": target})
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/seller/bind":
            acting = self._require("admin")
            if not acting:
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length <= 0 or content_length > 4096:
                    self._send_json(400, {"error": "Invalid payload size"})
                    return
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                seller_line_id = str(payload.get("seller_line_id") or "").strip()[:80]
                seller_phone = str(payload.get("seller_phone") or "").strip()[:40]
                intake_id = str(payload.get("intake_id") or "").strip()[:80]
                contract_id = str(payload.get("contract_id") or "").strip()[:80]
                if not seller_line_id:
                    self._send_json(400, {"error": "Missing seller_line_id"})
                    return
                upsert_seller_account(seller_line_id, name=str(payload.get("seller_name") or "").strip()[:100], phone=seller_phone)
                updated = []
                if intake_id:
                    with LISTING_INTAKE_LOCK:
                        istore = load_intake_data()
                        it = next((x for x in istore.get("intakes", []) if x.get("id") == intake_id), None)
                        if it:
                            it["seller_line_id"] = seller_line_id
                            it["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                            save_intake_data(istore)
                            updated.append(intake_id)
                if contract_id:
                    with CONTRACTS_LOCK:
                        cstore = load_contracts_data()
                        ct = next((x for x in cstore.get("contracts", []) if x.get("id") == contract_id), None)
                        if ct:
                            ct["seller_line_id"] = seller_line_id
                            save_contracts_data(cstore)
                            updated.append(contract_id)
                self._send_json(200, {"status": "success", "seller_line_id": seller_line_id, "bound_ids": updated})
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/lobby/register":
            s = self._session()
            if not s or not s.get("sub"):
                self._send_json(401, {"error": "กรุณาเชื่อมบัญชี LINE ก่อนลงทะเบียน"})
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                uid = s["sub"]
                store = load_lobby_data()
                if any(a.get("lineUserId") == uid for a in store.get("approved", [])):
                    self._send_json(409, {"error": "บัญชี LINE นี้เป็นสมาชิกอยู่แล้ว"})
                    return
                allowed = ("id", "name", "nickname", "phone", "line_id", "zone", "affiliation", "affiliation_label", "avatar", "submitted_at", "is_legacy_agent", "legacy_code", "legacy_match_status", "sales_scope")
                safe = {k: payload.get(k) for k in allowed if payload.get(k) is not None}
                safe["lineUserId"] = uid
                safe["lineDisplayName"] = s.get("name", "")
                if s.get("picture") and (not safe.get("avatar") or "unsplash.com" in str(safe.get("avatar", ""))):
                    safe["avatar"] = s.get("picture")
                safe["status"] = "pending"
                if not safe.get("id"):
                    safe["id"] = f"SW-APP-{int(time.time()) % 100000}"
                store["pending"] = [p for p in store.get("pending", []) if p.get("lineUserId") != uid]
                store["pending"].insert(0, safe)
                save_lobby_data(store, create_snapshot=True, snapshot_reason=f"register:{safe.get('name', uid)}")
                try:
                    admin_uids = {
                        a.get("lineUserId") for a in store.get("approved", [])
                        if _is_lobby_approver(a) and a.get("lineUserId")
                    } | {u for u in SUPER_ADMIN_LINE_USER_IDS if u}
                    pending_total = len(store.get("pending", []))
                    if LINE_ACCESS_TOKEN and admin_uids:
                        _app_snap = dict(safe)
                        def _notify_lobby_admins():
                            _name = _app_snap.get("name") or _app_snap.get("lineDisplayName") or "-"
                            _nick = _app_snap.get("nickname") or "-"
                            _phone = _app_snap.get("phone") or "-"
                            _line_id = _app_snap.get("line_id") or "-"
                            _zone = _app_snap.get("zone") or "-"
                            _aff = _app_snap.get("affiliation_label") or _app_snap.get("affiliation") or "-"
                            _leg = f"\n🏷️ รหัสเดิมที่แจ้ง: {_app_snap.get('legacy_code')} ({_app_snap.get('legacy_match_status')})" if _app_snap.get("is_legacy_agent") else ""
                            _msg = (
                                "🏛️ [แจ้งเตือน Lobby] มีผู้สมัครตัวแทนใหม่รอการอนุมัติ!\n"
                                f"👤 ชื่อ: {_name} (ชื่อเล่น: {_nick})\n"
                                f"📱 โทร: {_phone} | LINE: {_line_id}\n"
                                f"📍 โซน: {_zone}\n"
                                f"🏢 สังกัด: {_aff}{_leg}\n"
                                f"⏳ คิวรอใน Lobby ทั้งหมด: {pending_total} ท่าน\n"
                                "👉 กดตรวจสอบและอนุมัติ (บัว / พี่ลิลลี่):\n"
                                "https://assets.siwasup.com/admin_lobby_manager.html"
                            )
                            for auid in admin_uids:
                                _push_line_message(auid, _msg)
                        threading.Thread(target=_notify_lobby_admins, daemon=True).start()
                except Exception as _ne:
                    print(f"[Warn] Lobby admin notify failed: {_ne}")
                self._send_json(200, {"status": "success", "applicant": sanitize_member(safe)})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if path == "/api/lobby/approve":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                app_id = payload.get("applicantId")
                with _LOBBY_OP_LOCK:
                    store = load_lobby_data()
                    target_idx = -1
                    for idx, p in enumerate(store.get("pending", [])):
                        if p.get("id") == app_id:
                            target_idx = idx
                            break
                    if target_idx == -1:
                        self._send_json(404, {"error": "Applicant not found"})
                        return
                    applicant = store["pending"][target_idx]
                    _digits = lambda v: re.sub(r"\D", "", v or "")
                    existing = next((a for a in store.get("approved", []) if not a.get("lineUserId") and _digits(a.get("phone")) and _digits(a.get("phone")) == _digits(applicant.get("phone"))), None)
                    if existing and applicant.get("lineUserId"):
                        store["pending"].pop(target_idx)
                        existing["lineUserId"] = applicant["lineUserId"]
                        if applicant.get("avatar") and not existing.get("avatar"):
                            existing["avatar"] = applicant["avatar"]
                        store.setdefault("audit_log", []).insert(0, f"[{bkk_now().strftime('%Y-%m-%d %H:%M:%S')}] 🔗 ผูก LINE เข้ากับสมาชิกเดิม: {existing.get('name')}")
                        save_lobby_data(store)
                        self._send_json(200, {"status": "success", "approved": sanitize_member(existing), "linked": True})
                        return
                    perms_req = dict(payload.get("permissions", {}) or {})
                    sales_scope = str(payload.get("salesScope") or perms_req.get("salesScope") or applicant.get("sales_scope") or "both").strip()
                    if sales_scope not in ("npa_only", "consign_only", "both"):
                        sales_scope = "both"
                    perms_req["salesScope"] = sales_scope
                    is_admin_role = any(bool(perms_req.get(k)) for k in ("standardAdmin", "keyboxAdmin", "executiveAuthority", "systemAdmin"))
                    assigned_code = str(payload.get("code") or applicant.get("code") or "").strip().upper()
                    if not assigned_code:
                        if is_admin_role:
                            assigned_code = _next_admin_sa_code(store)
                        elif applicant.get("is_legacy_agent") and applicant.get("legacy_code") and applicant.get("legacy_match_status") in ("matched_verified", "matched_need_phone_confirm", "matched_phone_diff"):
                            assigned_code = str(applicant.get("legacy_code")).strip().upper()
                        else:
                            assigned_code = _next_agent_sw_code(store)
                    # Prevent duplicate code takeover
                    dup_holder = next((a for a in store.get("approved", []) if str(a.get("code") or "").strip().upper() == assigned_code and a.get("lineUserId") and a.get("lineUserId") != applicant.get("lineUserId")), None)
                    if dup_holder:
                        self._send_json(409, {"error": f"รหัส {assigned_code} ถูกใช้งานแล้วโดย {dup_holder.get('name', '-')}"})
                        return
                    store["pending"].pop(target_idx)
                    approved_item = {
                        "id": applicant.get("id"),
                        "code": assigned_code,
                        "name": applicant.get("name"),
                        "nickname": applicant.get("nickname"),
                        "phone": applicant.get("phone"),
                        "line_id": applicant.get("line_id"),
                        "zone": applicant.get("zone"),
                        "affiliation": applicant.get("affiliation", ""),
                        "is_legacy_agent": bool(applicant.get("is_legacy_agent")),
                        "legacy_match_status": applicant.get("legacy_match_status", ""),
                        "submitted_at": applicant.get("submitted_at", ""),
                        "avatar": applicant.get("avatar", ""),
                        "lineUserId": applicant.get("lineUserId"),
                        "role": payload.get("role", "Co-Broker Partner"),
                        "role_code": payload.get("role_code", ""),
                        "title": payload.get("title", ""),
                        "badges": payload.get("badges", []),
                        "permissions": perms_req,
                        "approved_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    store.setdefault("approved", []).insert(0, approved_item)
                    audit_entry = f"[{approved_item['approved_at']}] 🟢 อนุมัติสิทธิ์: {approved_item.get('name')} ({assigned_code} • {sales_scope})"
                    store.setdefault("audit_log", []).insert(0, audit_entry)
                    store["audit_log"] = store["audit_log"][:100]
                    save_lobby_data(store, create_snapshot=True, snapshot_reason=f"approve:{approved_item.get('name', app_id)}")
                    self._send_json(200, {"status": "success", "approved": sanitize_member(approved_item)})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if path == "/api/lobby/reject":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                app_id = payload.get("applicantId")
                store = load_lobby_data()
                store["pending"] = [p for p in store.get("pending", []) if p.get("id") != app_id]
                save_lobby_data(store, create_snapshot=True, snapshot_reason=f"reject:{app_id}")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/update-permissions":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                app_id = payload.get("applicantId")
                phone = payload.get("phone")
                store = load_lobby_data()
                target_idx = -1
                for idx, a in enumerate(store.get("approved", [])):
                    if (app_id and a.get("id") == app_id) or (phone and a.get("phone") == phone):
                        target_idx = idx
                        break
                if target_idx != -1:
                    m = store["approved"][target_idx]
                    if is_super_tech_root(m):
                        if not acting_member or not is_super_tech_root(acting_member):
                            self._send_json(403, {"error": "🔒 บัญชีสถาปัตยกรรมระบบสูงสุด (Super Tech Root) ได้รับการคุ้มครอง ห้ามผู้อื่นแก้ไขสิทธิ์"})
                            return
                        if "permissions" in payload and isinstance(payload["permissions"], dict):
                            payload["permissions"]["systemAdmin"] = True
                            payload["permissions"]["standardAdmin"] = True
                            payload["permissions"]["executiveAuthority"] = True
                    old_role = m.get("role")
                    if "role" in payload: m["role"] = payload["role"]
                    if "role_code" in payload: m["role_code"] = payload["role_code"]
                    if "title" in payload: m["title"] = payload["title"]
                    if "zone" in payload and payload["zone"]: m["zone"] = payload["zone"]
                    if "badges" in payload: m["badges"] = payload["badges"]
                    if "permissions" in payload: m["permissions"] = payload["permissions"]
                    perms_now = m.get("permissions") or {}
                    if not str(m.get("code") or "").strip() and any(bool(perms_now.get(k)) for k in ("standardAdmin", "keyboxAdmin", "executiveAuthority", "systemAdmin")):
                        m["code"] = _next_admin_sa_code(store)
                    m["updated_at"] = bkk_now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    audit_entry = f"[{m['updated_at']}] ⚙️ ปรับสิทธิ์: {m.get('name')} เป็น {m.get('role')} ({len(m.get('badges', []))} สิทธิ์)"
                    store.setdefault("audit_log", []).insert(0, audit_entry)
                    store["audit_log"] = store["audit_log"][:100]
                    save_lobby_data(store, create_snapshot=True, snapshot_reason=f"update_perms:{m.get('name', app_id)}")
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "member": sanitize_member(m)}, ensure_ascii=False).encode('utf-8'))
                    return
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Member not found in approved list"}).encode('utf-8'))
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/revoke":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                app_id = payload.get("applicantId")
                reason = payload.get("reason", "Revoked by admin")
                if acting_member and acting_member.get("id") == app_id:
                    self._send_json(400, {"error": "ไม่สามารถคัดตัวเองออกจากระบบได้"})
                    return
                store = load_lobby_data()
                target_member = next((a for a in store.get("approved", []) if a.get("id") == app_id), None)
                if target_member and is_super_tech_root(target_member):
                    self._send_json(403, {"error": "🔒 บัญชีสถาปัตยกรรมระบบสูงสุด (Super Tech Root) ถูกล็อกถาวร ไม่สามารถคัดออกได้"})
                    return
                target_idx = -1
                for idx, a in enumerate(store.get("approved", [])):
                    if a.get("id") == app_id:
                        target_idx = idx
                        break
                if target_idx != -1:
                    revoked_member = store["approved"].pop(target_idx)
                    rollback_id = payload.get("rollbackId") or f"rb_{int(time.time()*1000)}"
                    rollback_record = {
                        "rollback_id": rollback_id,
                        "action": "REVOKE",
                        "member": revoked_member,
                        "timestamp": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
                        "reason": reason
                    }
                    store.setdefault("rollback_history", []).insert(0, rollback_record)
                    store["rollback_history"] = store["rollback_history"][:50]
                    audit_entry = f"[{rollback_record['timestamp']}] คัดออก/เพิกถอนสิทธิ์: {revoked_member.get('name')} ({revoked_member.get('role')})"
                    store.setdefault("audit_log", []).insert(0, audit_entry)
                    store["audit_log"] = store["audit_log"][:100]
                    save_lobby_data(store, allow_truncate=True, create_snapshot=True, snapshot_reason=f"revoke:{revoked_member.get('name', app_id)}")
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "revoked": sanitize_member(revoked_member), "rollback_id": rollback_id}, ensure_ascii=False).encode('utf-8'))
                    return
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Member not found in approved list"}).encode('utf-8'))
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/rollback":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                rollback_id = payload.get("rollbackId")
                store = load_lobby_data()
                rb_list = store.get("rollback_history", [])
                target_idx = -1
                if rollback_id:
                    for idx, rb in enumerate(rb_list):
                        if rb.get("rollback_id") == rollback_id:
                            target_idx = idx
                            break
                elif rb_list:
                    target_idx = 0
                
                if target_idx != -1:
                    rb_item = rb_list.pop(target_idx)
                    if rb_item.get("action") == "REVOKE":
                        restored_member = rb_item.get("member")
                        store.setdefault("approved", []).insert(0, restored_member)
                        audit_entry = f"[{bkk_now().strftime('%Y-%m-%d %H:%M:%S')}] ↩️ Rollback คืนสิทธิ์: {restored_member.get('name')}"
                        store.setdefault("audit_log", []).insert(0, audit_entry)
                        save_lobby_data(store)
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json; charset=utf-8')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "success", "restored": sanitize_member(restored_member)}, ensure_ascii=False).encode('utf-8'))
                        return
                self.send_response(404)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No rollback record found"}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/snapshots/restore":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                snap_key = str(payload.get("key") or "").strip()
                expected_prefix = f"_vault/lobby_snap_{_R2_LOBBY_SNAP_PREFIX}_"
                if not snap_key.startswith(expected_prefix) or not snap_key.endswith(".json"):
                    self._send_json(400, {"error": "Invalid snapshot key"})
                    return
                snap_data = _fetch_r2_json(snap_key, timeout=12)
                if not isinstance(snap_data, dict) or ("approved" not in snap_data and "pending" not in snap_data):
                    self._send_json(404, {"error": "Snapshot not found or invalid"})
                    return
                snap_data.setdefault("audit_log", []).insert(0, f"[{bkk_now().strftime('%Y-%m-%d %H:%M:%S')}] ⏪ กู้คืนข้อมูล Lobby จาก Snapshot: {snap_key}")
                snap_data["audit_log"] = snap_data["audit_log"][:100]
                save_lobby_data(snap_data, allow_truncate=True, create_snapshot=True, snapshot_reason=f"restore:{snap_key}")
                self._send_json(200, {"status": "success", "approved": len(snap_data.get("approved", [])), "pending": len(snap_data.get("pending", []))})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if path == "/api/bug-report":
            s = self._session()
            if not s or not s.get("sub"):
                self._send_json(401, {"error": "login required"})
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 800_000:
                    self._send_json(413, {"error": "Payload too large"})
                    return
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                msg = str(payload.get("message") or "").strip()[:1000]
                if not msg:
                    self._send_json(400, {"error": "message is required"})
                    return
                shot = str(payload.get("screenshot_data_url") or "")
                if shot and (not shot.startswith("data:image/") or len(shot) > 600_000):
                    shot = ""
                store = load_lobby_data()
                mem = next((a for a in store.get("approved", []) if a.get("lineUserId") == s["sub"]), None)
                if not mem:
                    self._send_json(403, {"error": "approved member required"})
                    return
                rid = f"BUG-{bkk_now().strftime('%m%d%H%M%S')}-{uuid.uuid4().hex[:4].upper()}"
                rec = {
                    "id": rid,
                    "reporter_name": mem.get("nickname") or mem.get("name") or s.get("name") or "ทีมงาน",
                    "reporter_code": mem.get("code") or mem.get("id") or "",
                    "message": msg,
                    "screenshot_data_url": shot,
                    "page_url": str(payload.get("page_url") or "")[:400],
                    "mode": str(payload.get("mode") or "")[:30],
                    "prop_id": str(payload.get("prop_id") or "")[:60],
                    "viewport": str(payload.get("viewport") or "")[:30],
                    "status": "open",
                    "created_at": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                reports = _load_bug_reports()
                reports.insert(0, rec)
                _save_bug_reports(reports)
                self._send_json(200, {"status": "ok", "id": rid})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if path == "/api/bug-report/resolve":
            acting = self._require("admin")
            if not acting:
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
                rid = str(payload.get("id") or "").strip()
                new_status = "open" if payload.get("status") == "open" else "resolved"
                reports = _load_bug_reports()
                for r in reports:
                    if r.get("id") == rid:
                        r["status"] = new_status
                        r["resolved_by"] = acting.get("nickname") or acting.get("code") or "Admin"
                        break
                _save_bug_reports(reports)
                self._send_json(200, {"status": "ok"})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if path == "/api/lobby/backup":
            try:
                store = load_lobby_data()
                backup_name = f"lobby_backup_{bkk_now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_dir = os.path.join(os.path.dirname(LOBBY_PATH), "backups")
                os.makedirs(backup_dir, exist_ok=True)
                backup_file = os.path.join(backup_dir, backup_name)
                with open(backup_file, "w", encoding="utf-8") as bf:
                    json.dump(store, bf, ensure_ascii=False, indent=2)
                audit_entry = f"[{bkk_now().strftime('%Y-%m-%d %H:%M:%S')}] 💾 สำรองข้อมูลสถานะ: {backup_name}"
                store.setdefault("audit_log", []).insert(0, audit_entry)
                save_lobby_data(store, create_snapshot=True, snapshot_reason=f"manual:{backup_name}")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "backup_file": backup_name}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        signature = self.headers.get('X-Line-Signature')
        if signature:
            hash_val = hmac.new(
                LINE_CHANNEL_SECRET.encode('utf-8'),
                body,
                hashlib.sha256
            ).digest()
            calc_sig = base64.b64encode(hash_val).decode('utf-8')
            if signature != calc_sig:
                print("[Warn] Invalid LINE signature!")

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

        try:
            payload = json.loads(body.decode('utf-8'))
            events = payload.get('events', [])
            for event in events:
                ev_type = event.get('type')
                user_id = event.get('source', {}).get('userId', 'anon')

                if ev_type == 'follow':
                    reply_token = event.get('replyToken')
                    def process_follow(uid, rtoken):
                        prof = get_line_profile(uid)
                        # Zero-Day Defense Auto-Heal: Auto-link and pull authentic profile picture
                        try:
                            auto_heal_member_line_profile(uid, prof, "")
                        except Exception as _ahe:
                            print(f"[Auto-Heal Hook Warn]: {_ahe}")
                        user_name = prof.get("displayName", "ท่าน")
                        welcome_msg = (
                            f"สวัสดีครับคุณ {user_name}! ยินดีต้อนรับสู่ ศิวาทรัพย์ แอสเซท (Siwasup Co-Broker OS) ครับ 🏠✨\n\n"
                            "น้องศิวาเป็น AI ผู้ช่วยค้นหาทรัพย์และประสานงานนำชมบ้าน พร้อมทำงาน 24 ชั่วโมงครับ\n\n"
                            "🔑 หากท่านเป็นสมาชิกที่ยืนยันตัวตนแล้ว สามารถเข้าสู่ระบบได้ที่:\n"
                            "👉 https://assets.siwasup.com/agent_registration.html?mode=login\n\n"
                            "🏢 หากสนใจสมัครเป็นตัวแทนร่วมขาย (Co-Broker) บริษัทเปิดรับสมัครแบบ Walk-in พบทีมผู้บริหารที่สำนักงานท่าข้าม 12 เท่านั้นครับ\n\n"
                            "💡 หรือพิมพ์ค้นหาบ้านได้ทันที เช่น:\n"
                            "• 'บ้านเดี่ยว นนทบุรี งบ 4 ล้าน'\n"
                            "• 'ค้นหาทรัพย์ 1090965'"
                        )
                        if rtoken:
                            reply_line(rtoken, welcome_msg)
                        append_chat_log({
                            "id": f"LOG_{int(time.time()*1000)}",
                            "timestamp": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
                            "user_name": prof.get("displayName"),
                            "user_pic": prof.get("pictureUrl"),
                            "user_id_tail": uid[-6:] if uid else "anon",
                            "event_type": "follow",
                            "user_text": "[แอดเพื่อนเข้าสู่ระบบ LINE OA]",
                            "ai_reply": welcome_msg,
                            "matched_codes": [],
                            "search_mode": "FOLLOW_EVENT",
                            "latency_ms": 0
                        })
                    threading.Thread(target=process_follow, args=(user_id, reply_token), daemon=True).start()

                elif ev_type == 'message':
                    msg = event.get('message', {})
                    msg_type = msg.get('type', 'unknown')
                    user_text = msg.get('text', f"[{msg_type.upper()} MESSAGE]")
                    reply_token = event.get('replyToken')

                    now = time.time()
                    last_time = USER_LAST_SEEN.get(user_id, 0)
                    is_continuous = (now - last_time) < SESSION_TIMEOUT
                    USER_LAST_SEEN[user_id] = now

                    def process_msg(token, uid, text, mtype, continuous):
                        t0 = time.time()
                        try:
                            prof = get_line_profile(uid)
                            print(f"[User Message from {prof.get('displayName')}]: {text}")
                            matched_member = None
                            try:
                                matched_member = auto_heal_member_line_profile(uid, prof, text if mtype == 'text' else "")
                            except Exception as _ahe:
                                print(f"[Auto-Heal Msg Warn]: {_ahe}")
                            if not matched_member and uid in SUPER_ADMIN_LINE_USER_IDS:
                                lobby_s = load_lobby_data()
                                ensure_super_tech_seat(lobby_s, uid, prof.get("displayName", ""), prof.get("pictureUrl", ""))
                                matched_member = next((a for a in lobby_s.get("approved", []) if a.get("lineUserId") == uid), None)
                            if mtype == 'image':
                                # ---- รูปโฉนด: OCR + LandsMaps Flex Card ----
                                handle_deed_image(
                                    message_id=msg.get("id", ""),
                                    reply_token=token,
                                    user_id=uid,
                                    user_name=prof.get("displayName", "คุณเอเจนต์")
                                )
                                return
                            elif mtype == 'text':
                                text_clean = text.strip().lower()
                                text_raw = text.strip()
                                m_link = re.match(r'^(?:สร้าง|ขอ|ส่ง)?(?:ลิงก์|ลิงค์|ลิ้งก์|ลิ้งค์|ลิ้ง|ลิง|link)\s*(.+)$', text_raw, re.IGNORECASE)
                                m_check = re.match(r'^(?:เช็ก|เช็ค|ตรวจ)ลูกค้า(?:\s+(.+))?$|^(?:เช็ก|เช็ค|ตรวจ)\s+(v-[a-z0-9]+)$', text_raw, re.IGNORECASE)
                                m_merge = re.match(r'^(?:รวม|merge)\s+(v-[a-z0-9]+)\s+(v-[a-z0-9]+)$', text_raw, re.IGNORECASE)
                                m_unmerge = re.match(r'^(?:แยก|ยกเลิกรวม|unmerge)\s+(v-[a-z0-9]+)$', text_raw, re.IGNORECASE)
                                m_confirm = re.match(r'^(?:ยืนยัน|confirm)\s+(v-[a-z0-9]+)$', text_raw, re.IGNORECASE)
                                _is_adm_member = bool(matched_member and (is_admin_member(matched_member) or uid in SUPER_ADMIN_LINE_USER_IDS))
                                catalog_link_res = resolve_catalog_link_request(text_raw, matched_member, is_admin=_is_adm_member) if matched_member else None
                                _onboarding_strict_kw = ['สมัคร', 'ลงทะเบียน', 'login', 'เข้าสู่ระบบ', 'ขอนามบัตร', 'นามบัตร', 'โปรไฟล์', 'profile', 'วิธีสมัคร', 'ลิงก์สมัคร']
                                _onboarding_public_kw = _onboarding_strict_kw + ['เอเจนต์', 'เอเจน', 'ตัวแทน', 'ร่วมงาน', 'ขอเข้ากลุ่ม', 'เข้ากลุ่ม', 'นายหน้า', 'co-broker', 'cobroker', 'ขอลิงก์', 'ขอลิงค์', 'อยากเป็นเอเจนต์']
                                is_onboarding_link_req = any(k in text_clean for k in (_onboarding_strict_kw if matched_member else _onboarding_public_kw))
                                _is_agent_view_req = any(w in text_clean for w in (
                                    "มุม agent", "มุมตัวแทน", "ฝั่งตัวแทน", "ฝั่งเอเจน", "สำหรับ agent", "สำหรับตัวแทน",
                                    "ธนาคารไหน", "ทรัพย์ธนาคาร", "ดูในระบบ", "เข้าสู่ระบบตัวแทน"
                                )) or bool(re.match(r'^(?:สร้าง|ขอ|ส่ง)?(?:ลิงก์|ลิงค์|ลิ้งก์|ลิ้งค์)\s*(?:ตัวแทน|เอเจนต์?|agent)\s*$', text_clean))
                                is_prop_or_cmd_link = False
                                _link_geo_hit = None
                                if m_link:
                                    _raw_link_arg = m_link.group(1).strip()
                                    _raw_link_lower = _raw_link_arg.lower()
                                    _first_tok = _raw_link_arg.split()[0].lstrip('#').strip() if _raw_link_arg.split() else ''
                                    _is_explicit_client_name = _raw_link_arg.startswith("คุณ") or (bool(re.search(r'(?:ส่งให้|ให้)คุณ\s*[ก-๙a-zA-Z0-9]+', _raw_link_arg)) and not _extract_thai_geo(_raw_link_arg))
                                    _link_geo_hit = None if _is_explicit_client_name else _extract_thai_geo(_raw_link_arg)
                                    if _is_agent_view_req:
                                        is_prop_or_cmd_link = True
                                    elif any(_raw_link_lower.startswith(p) for p in ('โฉนด', 'บ้าน', 'ทาวน์โฮม', 'ทาวน์เฮ้าส์', 'คอนโด', 'ที่ดิน', 'อาคาร', 'ข้อมูล', 'ทรัพย์', 'สมัคร', 'ลงทะเบียน', 'นามบัตร', 'สำหรับ', 'ตัวแทน', 'เอเจน')):
                                        is_prop_or_cmd_link = True
                                    elif not _is_explicit_client_name and any(kw in _raw_link_lower for kw in ('โซน', 'แถว', 'ย่าน', 'ทำเล', 'หลัง', 'แปลง', 'ไม่เกิน', 'งบ', 'ล้าน')):
                                        is_prop_or_cmd_link = True
                                    elif _link_geo_hit:
                                        is_prop_or_cmd_link = True
                                    elif ('/' not in _raw_link_arg and '|' not in _raw_link_arg) and _first_tok and find_property_by_id_or_code(_first_tok):
                                        is_prop_or_cmd_link = True
                                deed_q = parse_deed_text_query(text)
                                if deed_q:
                                    deed_no = deed_q.get('deed_no', '')
                                    prov = deed_q.get('province', '')
                                    amp = deed_q.get('amphur', '')
                                    if deed_no and prov and amp:
                                        qr_tok = _build_deeplink_token(prov, amp, deed_no)
                                        dlink = f'https://landsmaps.dol.go.th/?qrcodeToken={qr_tok}' if qr_tok else ''
                                        flex_card = build_deed_flex_card({
                                            'province': prov,
                                            'amphur': amp,
                                            'deed_no': deed_no,
                                            'land_area_sqw': '',
                                            'confidence': 'high',
                                            'notes': 'ค้นหาผ่านข้อความพิมพ์ตรง'
                                        }, dlink, qr_tok or '')
                                        ai_reply = f'🗺️ น้องศิวาปักหมุดแปลงที่ดิน โฉนดเลขที่ {deed_no} อ.{amp} จ.{prov} ให้เรียบร้อยครับ! กดเปิดดูบน LandsMaps ได้เลยครับ ✨'
                                        matched_codes, search_mode, matched_props, flex_carousel = [], 'DEED_TEXT_QUERY', [], flex_card
                                    elif deed_no:
                                        ai_reply = f'🗺️ น้องศิวาตรวจพบเลขที่โฉนด #{deed_no} แล้วครับ!\n\nเนื่องจากระบบกรมที่ดิน (LandsMaps) ต้องใช้ชื่อจังหวัดและอำเภอในการปักหมุดรูปแปลง\n\n👉 รบกวนพิมพ์ระบุ จังหวัด และ อำเภอ เพิ่มเติมได้เลยครับ\nตัวอย่างเช่น: โฉนด {deed_no} ชลบุรี อ.เมือง'
                                        matched_codes, search_mode, matched_props, flex_carousel = [], 'DEED_PROMPT_GEO', [], None
                                    else:
                                        ai_reply = '🗺️ หากต้องการค้นหาแปลงที่ดิน กรุณาระบุเลขที่โฉนด พร้อมจังหวัดและอำเภอครับ\nตัวอย่าง: โฉนด 52696 ชลบุรี อ.เมือง'
                                        matched_codes, search_mode, matched_props, flex_carousel = [], 'DEED_PROMPT_GEO', [], None
                                elif _is_agent_view_req:
                                    ai_reply = (
                                        "🔐 ลิงก์เข้าใช้งาน **มุมมองตัวแทน / หลังบ้าน (Agent View)** เพื่อดูข้อมูลธนาคารเจ้าของทรัพย์, รหัสแบงก์ และค่าคอมมิชชัน:\n\n"
                                        "1️⃣ **หน้าแคตตาล็อกมุมมองตัวแทน:**\n"
                                        "https://assets.siwasup.com/catalog.html\n\n"
                                        "2️⃣ **ศูนย์รวมเครื่องมือตัวแทน (Launchpad):**\n"
                                        "https://assets.siwasup.com/launchpad.html\n\n"
                                        "💡 **วิธีเปิดมุมมอง Agent:** กดเข้าลิงก์ด้านบน แล้วกดปุ่ม **เข้าสู่ระบบ (LINE Login)** ด้วยบัญชีที่อนุมัติแล้ว ระบบจะปลดล็อกชื่อธนาคารและรหัสทรัพย์ให้เห็นทันทีครับ\n"
                                        "(ส่วนลิงก์ที่มี `&view=client` จะเป็นมุมมองลูกค้าที่ซ่อนชื่อธนาคารไว้ครับ)"
                                    )
                                    matched_codes, search_mode, matched_props, flex_carousel = [], 'AGENT_VIEW_PORTAL_LINK', [], None
                                elif catalog_link_res:
                                    ag_ref, catalog_url = catalog_link_res
                                    ai_reply = (
                                        f"🏠 ลิงก์แคตตาล็อกบ้านของตัวแทน **{ag_ref}** (มุมมองลูกค้า ซ่อนรหัสแบงก์/ค่าคอม) พร้อมส่งต่อแล้วค่ะ:\n\n"
                                        f"{catalog_url}\n\n"
                                        f"💡 หากต้องการสร้างลิงก์เฉพาะเจาะจงรายลูกค้า (เพื่อแจ้งเตือนชื่อและ Trust Score เมื่อลูกค้าเปิดดู) ให้พิมพ์:\n"
                                        f"`ลิงก์ ชื่อลูกค้า`"
                                    )
                                    matched_codes, search_mode, matched_props, flex_carousel = [], 'AGENT_CATALOG_LINK', [], None
                                elif matched_member and m_link and is_prop_or_cmd_link and _link_geo_hit:
                                    ag_ref = resolve_agent_ref_for_member(matched_member)
                                    conflicts = _detect_conflicting_zones(text_raw, threshold_km=20.0)
                                    ambig = _link_geo_hit.get("ambiguous") or []
                                    if len(conflicts) >= 2:
                                        z_str = " กับ ".join(conflicts[:2]) if len(conflicts) == 2 else ", ".join(conflicts)
                                        ai_reply = (
                                            f"📍 เห็นระบุมา {len(conflicts)} โซนที่อยู่คนละฝั่งกัน ({z_str}) — "
                                            f"อยากให้คัดเน้นโซนไหนก่อน หรือให้ส่งแยกทีละโซนดีครับ?"
                                        )
                                        matched_codes, search_mode, matched_props, flex_carousel = [], 'GEO_CONFLICT_CONFIRM', [], None
                                    # Mandatory Parameter / Ambiguity Gate: if tambon matches multiple provinces without province specified, ask first!
                                    elif ambig and not _link_geo_hit.get("province"):
                                        prov_choices = list(dict.fromkeys(a["p"] for a in ambig))[:5]
                                        sub_name = _link_geo_hit.get("subdistrict") or ""
                                        ai_reply = (
                                            f"📍 พบชื่อตำบล/แขวง **\"{sub_name}\"** ซ้ำกันหลายจังหวัดครับ รบกวนระบุจังหวัดที่ต้องการเพิ่มเติมสักนิดนะครับ:\n"
                                            + "\n".join(f"• {p}" for p in prov_choices)
                                            + f"\n\nตัวอย่าง: `ขอลิงก์บ้าน {sub_name} {prov_choices[0]}`"
                                        )
                                        matched_codes, search_mode, matched_props, flex_carousel = [], 'GEO_AMBIGUOUS_CONFIRM', [], None
                                    else:
                                        req_cat = ""
                                        allowed_cats = []
                                        if any(w in text_clean for w in ("บ้านเดี่ยว", "บ้านแฝด")):
                                            req_cat, allowed_cats = "บ้านเดี่ยว", ["บ้านเดี่ยว", "บ้านแฝด"]
                                        elif any(w in text_clean for w in ("ทาวน์โฮม", "ทาวน์เฮ้าส์")):
                                            req_cat, allowed_cats = "ทาวน์โฮม", ["ทาวน์โฮม", "ทาวน์เฮ้าส์"]
                                        elif "คอนโด" in text_clean or "ห้องชุด" in text_clean:
                                            req_cat, allowed_cats = "คอนโด", ["คอนโด", "ห้องชุด"]
                                        elif "ที่ดิน" in text_clean:
                                            req_cat, allowed_cats = "ที่ดิน", ["ที่ดิน"]
                                        elif "อาคารพาณิชย์" in text_clean or "ตึกแถว" in text_clean:
                                            req_cat, allowed_cats = "อาคารพาณิชย์", ["อาคารพาณิชย์", "ตึกแถว", "โฮมออฟฟิศ"]
                                        elif "บ้าน" in text_clean:
                                            req_cat, allowed_cats = "บ้าน", ["บ้านเดี่ยว", "บ้านแฝด", "ทาวน์โฮม", "ทาวน์เฮ้าส์"]

                                        req_budget = parse_price(text_raw)
                                        m_req_cnt = re.search(r'(\d{1,2})\s*(?:หลัง|ที่|แปลง|รายการ|ห้อง)', text_raw)
                                        req_limit = min(max(int(m_req_cnt.group(1)), 1), 10) if m_req_cnt else 5
                                        g_prov = _link_geo_hit.get("province") or ""
                                        g_dist = _link_geo_hit.get("district") or ""
                                        g_sub = _link_geo_hit.get("subdistrict") or ""
                                        g_lat = _link_geo_hit.get("lat")
                                        g_lng = _link_geo_hit.get("lng")

                                        # Cross-Province Haversine Radius Search (Tier 1: 0-5km, Tier 2: 5-15km, no province lock)
                                        ranked = _find_nearest_siwasup_props(g_lat, g_lng, allowed_cats=allowed_cats or None, max_p=req_budget, limit=req_limit) if (g_lat and g_lng) else []
                                        tier1 = [p for p in ranked if p.get("tier") == 1]
                                        tier2 = [p for p in ranked if p.get("tier") == 2]
                                        show_props = (tier1 + tier2)[:req_limit] if (tier1 or tier2) else ranked[:min(req_limit, 3)]

                                        q_params = [("ref", ag_ref), ("view", "client")]
                                        if req_cat:
                                            q_params.append(("cat", req_cat))
                                        if show_props:
                                            link_prov = show_props[0].get("province") or g_prov
                                            if link_prov:
                                                q_params.append(("province", link_prov))
                                        elif g_prov:
                                            q_params.append(("province", g_prov))
                                        filtered_url = "https://assets.siwasup.com/catalog.html?" + urllib.parse.urlencode(q_params)

                                        area_label = " ".join(x for x in [
                                            f"ต.{g_sub}" if g_sub else "",
                                            f"อ.{g_dist}" if g_dist else "",
                                            f"จ.{g_prov}" if g_prov else ""
                                        ] if x) or "พื้นที่ที่ระบุ"

                                        lines = []
                                        if tier1 and tier2:
                                            lines.append(f"🏠 พิกัด {area_label}: พบในระยะเป้าหมาย (0–5 กม.) {len(tier1)} หลัง และโซนใกล้เคียง (5–15 กม.) อีก {len(tier2)} หลังครับ:")
                                        elif tier1:
                                            lines.append(f"🏠 พิกัด {area_label}: พบในระยะเป้าหมาย (0–5 กม.) จำนวน {len(tier1)} หลังครับ:")
                                        elif tier2:
                                            lines.append(f"📍 โซน {area_label} (0–5 กม.) ยังไม่มี{req_cat or 'ทรัพย์'}ว่าง — น้องศิวาคัดโซนใกล้เคียง (5–15 กม.) ที่ใกล้ที่สุด {len(tier2)} หลังมาให้ครับ:")
                                        elif show_props:
                                            lines.append(f"📍 โซน {area_label} (0–15 กม.) ยังไม่มี{req_cat or 'ทรัพย์'}ว่าง — น้องศิวาคัดแปลงที่ใกล้ที่สุดในระบบมาให้แทนครับ:")
                                        else:
                                            lines.append(f"🏠 ลิงก์แคตตาล็อกโซน {area_label} (มุมมองลูกค้า) พร้อมส่งต่อครับ:")

                                        for idx_p, hp in enumerate(show_props, 1):
                                            lines.append(f"{idx_p}. {hp['code']} | {hp['type']} | {hp['district']} {hp['province']} — {hp['price']} (ห่าง ~{hp['distance_km']} กม.)")
                                        lines.append(f"\n🔗 ลิงก์แคตตาล็อกมุมมองลูกค้า:\n{filtered_url}")
                                        ai_reply = "\n".join(lines)
                                        matched_codes = [p["code"] for p in show_props]
                                        search_mode = "GEO_RADIUS_TIER1_2" if (tier1 or tier2) else "GEO_RADIUS_FALLBACK"
                                        matched_props = show_props
                                        full_flex_props = [fp for fp in (find_property_by_id_or_code(c) for c in matched_codes) if fp]
                                        flex_carousel = build_property_flex_carousel(full_flex_props, client_name=prof.get("displayName", "คุณลูกค้า"), agent_ref=ag_ref) if full_flex_props else None
                                elif matched_member and m_link and not is_onboarding_link_req and not is_prop_or_cmd_link:
                                    raw_arg = m_link.group(1).strip()
                                    av_name, ag_note, prop_id = parse_agent_link_input(raw_arg)
                                    if not av_name:
                                        ai_reply = "⚠️ กรุณาระบุชื่อเรียก (Avatar) ลูกค้าด้วยค่ะ เช่น: `ลิงก์ คุณA / งบ 3 ล้าน`"
                                    else:
                                        ag_ref = resolve_agent_ref_for_member(matched_member)
                                        client_url, _ = build_client_catalog_link(av_name, ag_note, agent_ref=ag_ref, prop_id=prop_id)
                                        disp_av = av_name if av_name.startswith("คุณ") else f"คุณ{av_name}"
                                        note_info = f"\n📝 โน้ตหลังบ้าน (ลูกค้าไม่เห็น): {ag_note}" if ag_note else ""
                                        prop_info = f"\n📌 ล็อกเปิดบ้านรหัส: {prop_id}" if prop_id else ""
                                        zone_ask_hint = ""
                                        if not prop_id and re.search(r'\d+\s*(?:หลัง|ห้อง|แปลง)', f"{ag_note} {raw_arg}") and not _extract_thai_geo(f"{ag_note} {raw_arg}"):
                                            zone_ask_hint = f"\n\n💡 เห็นระบุจำนวนไว้แต่ยังไม่ได้ระบุทำเล — อยากเจาะจงโซนไหนหรืองบประมาณเท่าไหร่ บอกน้องศิวาช่วยคัดส่งให้ {disp_av} เพิ่มเติมได้เลยนะครับ (เช่น 'บ้าน โซนบางแค งบ 3 ล้าน')"
                                        ai_reply = (
                                            f"🔗 ลิงก์เฉพาะสำหรับ {disp_av} พร้อมส่งต่อให้ลูกค้าแล้วค่ะ!\n"
                                            f"(ลิงก์นี้ซ่อนชื่อเป็นรหัสปลอดภัย ลูกค้าไม่เห็นโน้ตหลังบ้าน){note_info}{prop_info}\n\n"
                                            f"👇 กดค้าง/ส่งต่อข้อความด้านล่างให้ลูกค้าได้เลยค่ะ:\n"
                                            f"คัดสรรบ้านสวยและทรัพย์คุณภาพไว้ให้ {disp_av} เลือกชมแล้วนะคะ คลิกดูทั้งหมดได้ที่นี่เลยค่ะ 👇\n"
                                            f"{client_url}\n\n"
                                            f"🔔 ทันทีที่ลูกค้ากดเปิดดู น้องศิวาจะแจ้งเตือนกลับมาในแชทนี้ทันทีค่ะ{zone_ask_hint}"
                                        )
                                    matched_codes, search_mode, matched_props, flex_carousel = [], 'CLIENT_LINK_GEN', [], None
                                elif matched_member and m_check:
                                    ag_ref = resolve_agent_ref_for_member(matched_member)
                                    is_adm = _is_adm_member
                                    q_target = (m_check.group(1) or m_check.group(2) or "").strip()
                                    ai_reply = format_client_tracking_report(agent_ref=ag_ref, target_query=q_target, is_admin=is_adm)
                                    matched_codes, search_mode, matched_props, flex_carousel = [], 'CLIENT_TRACK_REPORT', [], None
                                elif matched_member and m_merge:
                                    ag_ref = resolve_agent_ref_for_member(matched_member)
                                    is_adm = _is_adm_member
                                    ok, msg_res = merge_visitor_ids(m_merge.group(1), m_merge.group(2), actor_name=matched_member.get('name', ''), agent_ref=ag_ref, is_admin=is_adm)
                                    ai_reply = ("✅ " if ok else "⚠️ ") + msg_res
                                    matched_codes, search_mode, matched_props, flex_carousel = [], 'CLIENT_MERGE', [], None
                                elif matched_member and m_unmerge:
                                    ag_ref = resolve_agent_ref_for_member(matched_member)
                                    is_adm = _is_adm_member
                                    ok, msg_res = unmerge_visitor_id(m_unmerge.group(1), actor_name=matched_member.get('name', ''), agent_ref=ag_ref, is_admin=is_adm)
                                    ai_reply = ("✅ " if ok else "⚠️ ") + msg_res
                                    matched_codes, search_mode, matched_props, flex_carousel = [], 'CLIENT_UNMERGE', [], None
                                elif matched_member and m_confirm:
                                    ag_ref = resolve_agent_ref_for_member(matched_member)
                                    is_adm = _is_adm_member
                                    ok, msg_res = confirm_visitor_identity(m_confirm.group(1), actor_name=matched_member.get('name', ''), agent_ref=ag_ref, is_admin=is_adm)
                                    ai_reply = ("✅ " if ok else "⚠️ ") + msg_res
                                    matched_codes, search_mode, matched_props, flex_carousel = [], 'CLIENT_CONFIRM', [], None
                                elif is_onboarding_link_req:
                                    if matched_member:
                                        ai_reply = (
                                            f"สวัสดีครับคุณ {prof.get('displayName', '')}! ท่านสามารถเข้าสู่ระบบหรือเปิดดูนามบัตรดิจิทัลทางการได้ที่นี่ครับ:\n\n"
                                            "👉 https://assets.siwasup.com/agent_registration.html?mode=login"
                                        )
                                    else:
                                        ai_reply = (
                                            f"สวัสดีครับคุณ {prof.get('displayName', '')}! การสมัครเป็นตัวแทนร่วมขาย (Co-Broker) กับศิวาทรัพย์ แอสเซท "
                                            "เปิดรับสมัครแบบ Walk-in เข้ามาพบทีมผู้บริหารและเซ็นสัญญาที่สำนักงานท่าข้าม 12 เท่านั้นครับ\n\n"
                                            "📍 สามารถนัดหมายวันเวลาเข้ามาสมัครได้ในแชทนี้ หรือติดต่อคุณบัว / พี่ลิลลี่ได้เลยครับ ✨"
                                        )
                                    matched_codes, search_mode, matched_props, flex_carousel = [], "ONBOARDING_REGISTRATION", [], None
                                else:
                                    ai_reply, matched_codes, search_mode, matched_props = ask_gemini(uid, text, is_continuous=continuous)
                                    flex_carousel = None
                                    if matched_props:
                                        full_props = []
                                        for mp in matched_props:
                                            found = find_property_by_id_or_code(mp.get("code"))
                                            if found:
                                                full_props.append(found)
                                        if full_props:
                                            req_agent_ref = resolve_agent_ref_for_member(matched_member) if matched_member else "SW000"
                                            prefiltered_url = _build_prefiltered_catalog_url(USER_SEARCH_CONTEXT.get(uid, {}), agent_ref=req_agent_ref)
                                            flex_carousel = build_property_flex_carousel(full_props, client_name=prof.get("displayName", "คุณลูกค้า"), agent_ref=req_agent_ref, view_all_url=prefiltered_url)
                            else:
                                ai_reply = "น้องศิวาได้รับไฟล์/สติกเกอร์เรียบร้อยครับ หากต้องการค้นหาทรัพย์ พิมพ์รหัสทรัพย์หรือทำเล เช่น '1090965' หรือ 'บ้านเดี่ยว นนทบุรี งบ 4 ล้าน' ได้เลยครับ!"
                                matched_codes, search_mode, matched_props, flex_carousel = [], "NON_TEXT", [], None

                            latency_ms = int((time.time() - t0) * 1000)
                            if token:
                                reply_line(token, ai_reply, flex_message=flex_carousel)

                            append_chat_log({
                                "id": f"LOG_{int(time.time()*1000)}",
                                "timestamp": bkk_now().strftime("%Y-%m-%d %H:%M:%S"),
                                "user_name": prof.get("displayName"),
                                "user_pic": prof.get("pictureUrl"),
                                "user_id_tail": uid[-6:] if uid else "anon",
                                "event_type": "message",
                                "user_text": text,
                                "ai_reply": ai_reply,
                                "matched_codes": matched_codes,
                                "search_mode": search_mode,
                                "latency_ms": latency_ms
                            })
                        except Exception as th_err:
                            print(f"[Thread Error]: {th_err}")

                    if msg_type == 'text' and user_id:
                        def _flush_debounced_msg(target_uid):
                            with _MSG_DEBOUNCE_LOCK:
                                entry = _MSG_DEBOUNCE_BUF.pop(target_uid, None)
                            if entry:
                                combined_text = " ".join(entry["texts"]).strip()
                                process_msg(entry["token"], target_uid, combined_text, "text", entry["continuous"])

                        with _MSG_DEBOUNCE_LOCK:
                            buf = _MSG_DEBOUNCE_BUF.get(user_id)
                            if buf and buf.get("timer"):
                                buf["timer"].cancel()
                                buf["texts"].append(user_text)
                                buf["token"] = reply_token
                                buf["continuous"] = is_continuous
                            else:
                                buf = {"texts": [user_text], "token": reply_token, "continuous": is_continuous, "timer": None}
                                _MSG_DEBOUNCE_BUF[user_id] = buf
                            t_obj = threading.Timer(1.6, _flush_debounced_msg, args=(user_id,))
                            t_obj.daemon = True
                            buf["timer"] = t_obj
                            t_obj.start()
                    else:
                        threading.Thread(
                            target=process_msg,
                            args=(reply_token, user_id, user_text, msg_type, is_continuous),
                            daemon=True
                        ).start()
        except Exception as e:
            print(f"[Webhook Error]: {e}")


import signal

def handle_render_shutdown(signum, frame):
    global _CHAT_SHUTTING_DOWN
    _CHAT_SHUTTING_DOWN = True
    print(f"[*] Received shutdown signal ({signum}) from Render. Flushing all data to Cloudflare R2 before sleep...")
    try:
        if put_object_r2:
            with LOG_LOCK:
                store = load_chat_logs()
                data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
                put_object_r2(_R2_CHAT_VAULT_KEY, data_bytes, "application/json; charset=utf-8")
                print("[+] Chat logs successfully flushed to Cloudflare R2 before sleep!")
            with CONTRACTS_LOCK:
                c_store = load_contracts_data()
                c_bytes = json.dumps(c_store, ensure_ascii=False, indent=2).encode("utf-8")
                put_object_r2(_R2_CONTRACTS_VAULT_KEY, c_bytes, "application/json")
                print("[+] Exclusive contracts vault flushed to Cloudflare R2 before sleep!")
            with LOBBY_LOCK:
                if put_object_r2 and _R2_LOBBY_RESTORED:
                    l_store = load_lobby_data()
                    l_bytes = json.dumps(l_store, ensure_ascii=False, indent=2).encode("utf-8")
                    put_object_r2(_R2_LOBBY_VAULT_KEY, l_bytes, "application/json")
                    put_object_r2("data/lobby_applicants.json", l_bytes, "application/json; charset=utf-8")
                    print("[+] Lobby applicants vault flushed to Cloudflare R2 before sleep!")
                else:
                    print("[~] Skipped lobby R2 flush (not restored from R2 yet).")
            with CLIENT_TRACKING_LOCK:
                ct_store = load_client_tracking_data()
                if put_object_r2 and _R2_CLIENT_TRACKING_RESTORED and len(ct_store.get("visitors", {})) > 0:
                    ct_bytes = json.dumps(ct_store, ensure_ascii=False, indent=2).encode("utf-8")
                    put_object_r2(_R2_CLIENT_TRACKING_VAULT_KEY, ct_bytes, "application/json; charset=utf-8")
                    print("[+] Client tracking vault flushed to Cloudflare R2 before sleep!")
                else:
                    print("[~] Skipped client tracking R2 flush (not restored or empty store).")
            with CONTENT_HUB_LOCK:
                ch_store = load_content_data()
                if put_object_r2 and _R2_CONTENT_RESTORED and not _R2_CONTENT_RESTORE_FAILED:
                    ch_bytes = json.dumps(ch_store, ensure_ascii=False, indent=2).encode("utf-8")
                    put_object_r2(_R2_CONTENT_VAULT_KEY, ch_bytes, "application/json; charset=utf-8")
                    print("[+] Content hub vault flushed to Cloudflare R2 before sleep!")
    except Exception as e:
        print(f"[-] Error during pre-sleep flush: {e}")
    sys.exit(0)

try:
    signal.signal(signal.SIGTERM, handle_render_shutdown)
    signal.signal(signal.SIGINT, handle_render_shutdown)
except Exception:
    pass


def run_server():
    if not os.path.exists(CHAT_LOG_PATH):
        store = load_chat_logs()
        with open(CHAT_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False, indent=2)
    server = http.server.ThreadingHTTPServer((HOST, PORT), WebhookHandler)
    print(f"[*] LINE-Gemini Webhook Server v2 running on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
