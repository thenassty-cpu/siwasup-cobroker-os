import http.server
import json
import urllib.request
import ssl
import hmac
import hashlib
import base64
import os
import sys
import threading
import time
import re
from datetime import datetime

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

# Session & Multi-Turn Memory Tracking
USER_LAST_SEEN = {}
USER_PROFILE_CACHE = {}
USER_CHAT_HISTORY = {}  # user_id -> list of {"user": ..., "bot": ...}
USER_SEARCH_CONTEXT = {}  # user_id -> {"types": [], "locs": [], "max_p": None, "unlimited": False, "updated_at": 0}
SESSION_TIMEOUT = 15 * 60

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
    "ราชพฤกษ์": ["Taling Chan", "Phasi Charoen", "Mueang Nonthaburi", "ตลิ่งชัน", "ภาษีเจริญ", "นนทบุรี"],
    "ธนบุรี": ["Thon Buri", "Bangkok Yai", "Khlong San", "ธนบุรี", "คลองสาน"],
    "คลองสาน": ["Khlong San", "Thon Buri", "คลองสาน", "ธนบุรี"],
    "ภาษีเจริญ": ["Phasi Charoen", "ภาษีเจริญ", "บางแค"],
    "บางแค": ["Bang Khae", "Phasi Charoen", "บางแค", "ภาษีเจริญ"],
    "บางบอน": ["Bang Bon", "บางบอน", "บางขุนเทียน"],
    "หนองแขม": ["Nong Khaem", "Bang Khae", "หนองแขม", "บางแค"],
    "ตลิ่งชัน": ["Taling Chan", "ตลิ่งชัน"],
    "ทวีวัฒนา": ["Thawi Watthana", "ทวีวัฒนา"],
    "พระราม 2": ["Bang Khun Thian", "Chom Thong", "พระราม 2", "ท่าข้าม", "บางขุนเทียน"],

    # โซนตะวันออก & เหนือ & ปริมณฑล
    "บางนา": ["Bang Na", "Bang Phli", "Prawet", "Samut Prakan", "บางนา"],
    "บางพลี": ["Bang Phli", "Samut Prakan", "บางพลี"],
    "บางบ่อ": ["Bang Bo", "Samut Prakan", "บางบ่อ"],
    "บางเสาธง": ["Bang Sao Thong", "Samut Prakan", "บางเสาธง"],
    "ลาดกระบัง": ["Lat Krabang", "ลาดกระบัง"],
    "บางกะปิ": ["Bang Kapi", "บางกะปิ"],
    "รามอินทรา": ["Khan Na Yao", "Min Buri", "Bang Khen", "Khlong Sam Wa", "รามอินทรา", "บางชัน"],
    "บางชัน": ["Khlong Sam Wa", "Khan Na Yao", "บางชัน", "รามอินทรา"],
    "จตุจักร": ["Chatuchak", "จตุจักร"],
    "ดอนเมือง": ["Don Mueang", "ดอนเมือง"],
    "สายไหม": ["Sai Mai", "สายไหม"],
    "นนทบุรี": ["Nonthaburi", "Mueang Nonthaburi", "Bang Kruai", "Bang Yai", "Pak Kret", "นนทบุรี"],
    "บางใหญ่": ["Bang Yai", "Nonthaburi", "บางใหญ่"],
    "ปากเกร็ด": ["Pak Kret", "Nonthaburi", "ปากเกร็ด"],
    "สมุทรปราการ": ["Samut Prakan", "Mueang Samut Prakan", "สมุทรปราการ"],
    "ปทุมธานี": ["Pathum Thani", "Khlong Luang", "Thanyaburi", "Lam Luk Ka", "ปทุมธานี"],
    "ลำลูกกา": ["Lam Luk Ka", "Pathum Thani", "ลำลูกกา"],
    "ธัญบุรี": ["Thanyaburi", "Pathum Thani", "ธัญบุรี"],
    "คลองหลวง": ["Khlong Luang", "Pathum Thani", "คลองหลวง"],
    "เชียงใหม่": ["Chiang Mai", "Mueang Chiang Mai", "เชียงใหม่"],
    "พัทยา": ["Bang Lamung", "Chon Buri", "พัทยา"],
    "ชลบุรี": ["Chon Buri", "Mueang Chon Buri", "Si Racha", "ชลบุรี"]
}

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
    "ตึกแถว": ["COMM"]
}


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


def load_chat_logs():
    if os.path.exists(CHAT_LOG_PATH):
        try:
            with open(CHAT_LOG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "bot_name": "Siwasupagent (@813nyyia)",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_logged": 0,
        "historical_summary": {
            "2026-10-29_replies_sent": 18,
            "followers_count": 2,
            "note": "ข้อความ 18 รายการแรกเมื่อวันที่ 29 ต.ค. 2569 รันผ่านโหมด Terminal ก่อนเปิดระบบบันทึกไฟล์ ตั้งแต่วันที่ 31 ต.ค. 2569 เป็นต้นไป ทุกข้อความจะถูกบันทึกแสดงผลที่นี่แบบ Real-Time 100%"
        },
        "conversations": []
    }


def append_chat_log(entry):
    with LOG_LOCK:
        store = load_chat_logs()
        store["conversations"].insert(0, entry)
        store["conversations"] = store["conversations"][:500]
        store["total_logged"] = len(store["conversations"])
        store["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            with open(CHAT_LOG_PATH, "wb") as f:
                f.write(data_bytes)
        except Exception as e:
            print(f"[Log Save Error]: {e}")

    if put_object_r2:
        def sync_r2():
            try:
                put_object_r2("line_chat_logs.json", data_bytes, "application/json; charset=utf-8")
                print("[R2 Sync] Uploaded line_chat_logs.json to assets.siwasup.com")
            except Exception as ex:
                print(f"[R2 Sync Warn]: {ex}")
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
                "price": sp.get("price"),
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
                "price": f"{p.get('pr', 0):,} บาท",
                "land_sqw": p.get('sqw'),
                "living_sqm": p.get('sqm'),
                "status": "พร้อมเปิดให้เข้าชม"
            }], "EXACT_NPA_CODE"

    # 2. Project / Title Keyword Match in Siwasup Portfolio (e.g. "ซิกเนเจอร์ รามอินทรา 109")
    stop_words = ["เป๊ะนะครับ", "เป็น", "ทวาน์โฮม", "ทาวน์โฮม", "บ้านเดี่ยว", "คอนโด", "ช่วยตรวจสอบให้หน่อย", "อยากนัดเปิดบ้าน", "ใกล้สถานีรถไฟฟ้า"]
    project_keywords = [w for w in re.split(r'\s+', query) if len(w) >= 3 and w not in stop_words and not w.startswith("ช่วย") and not w.startswith("อยาก")]
    if any(k in query for k in ["ซิกเนเจอร์", "รามอินทรา 109", "มัณฑนา", "พาทิโอ", "ลุมพินี", "ชวนชื่น", "พฤกษา", "เซ็นทริค"]):
        matched_siwa = []
        for sp in SIWASUP_PROPS:
            title_desc = ((sp.get("title") or "") + " " + (sp.get("description") or "")).lower()
            score = sum(1 for kw in project_keywords if kw.lower() in title_desc)
            if score >= 2 or ("ซิกเนเจอร์" in q_low and "ซิกเนเจอร์" in title_desc):
                matched_siwa.append((score, sp))
        if matched_siwa:
            matched_siwa.sort(key=lambda x: x[0], reverse=True)
            out = []
            for _, sp in matched_siwa[:3]:
                out.append({
                    "code": str(sp.get("id")),
                    "bank": sp.get("bank_source") or "Siwasup",
                    "title": sp.get("title"),
                    "type": sp.get("category") or "ทาวน์โฮม",
                    "location": sp.get("location") or "กรุงเทพฯ",
                    "price": sp.get("price"),
                    "status": "ขายแล้ว/ตัดสต๊อก" if (sp.get("status") == "sold_archive" or sp.get("is_image_soldout")) else "พร้อมเปิดให้เข้าชม"
                })
            return out, "PROJECT_NAME_MATCH"

    # 3. Check if this is purely a workflow/process/booking question
    if any(w in q_low for w in WORKFLOW_KEYWORDS):
        return [], "WORKFLOW_QUESTION"

    # 4. Multi-Turn Search Context Management
    uid = user_id or "default"
    ctx = USER_SEARCH_CONTEXT.setdefault(uid, {
        "types": [],
        "locs": [],
        "max_p": None,
        "unlimited": False,
        "updated_at": time.time()
    })

    # Clean query for type check (strip viewing verbs)
    q_for_type = re.sub(r'(?:เปิดบ้าน|ชมบ้าน|ดูบ้าน|กุญแจบ้าน|เข้าบ้าน|ล็อกบ้าน|หน้าบ้าน)', '', query)

    # Detect new types in current message (Strict type discrimination)
    new_types = []
    if any(k in q_for_type for k in ["บ้านเดี่ยว", "บ้านแฝด"]):
        new_types.extend(["SDH"])
    elif any(k in q_for_type for k in ["ทาวน์โฮม", "ทาวน์เฮ้าส์", "ทาวน์เฮาส์", "ทวาน์โฮม"]):
        new_types.extend(["TH"])
    elif any(k in q_for_type for k in ["คอนโด", "ห้องชุด", "condo"]):
        new_types.extend(["CD"])
    elif any(k in q_for_type for k in ["ที่ดิน", "แปลงที่ดิน"]):
        new_types.extend(["LAND"])
    elif any(k in q_for_type for k in ["อาคารพาณิชย์", "ตึกแถว", "โฮมออฟฟิศ"]):
        new_types.extend(["COMM"])
    elif "บ้าน" in q_for_type:
        # General "บ้าน" = residential ground houses (SDH, TH) - strictly excludes Condo, Land, or Commercial!
        new_types.extend(["SDH", "TH"])
    else:
        for k, v in TYPE_MAP.items():
            if k in q_for_type:
                new_types.extend(v)
    if new_types:
        ctx["types"] = list(set(new_types))

    # Detect new locations in current message
    new_locs = []
    for k, v in LOC_MAP.items():
        if k in query:
            new_locs.extend(v)
    if new_locs:
        ctx["locs"] = list(set(new_locs))

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
    has_trigger = any(w in q_low for w in SEARCH_ACTION_KEYWORDS)
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

    results = []
    for p in CATALOG:
        if eff_types and p.get('t') not in eff_types:
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

    # Automatic geographic expansion if 0 results found in tight western/Siriraj area
    if not results and eff_locs and any(w in str(eff_locs) for w in ['Bangkok Noi', 'Taling Chan']):
        west_expand = ['Taling Chan', 'Bangkok Noi', 'Bang Phlat', 'Thawi Watthana', 'Phasi Charoen', 'Bang Khae', 'Thon Buri']
        for p in CATALOG:
            if eff_types and p.get('t') not in eff_types:
                continue
            pr = p.get('pr', 0)
            if eff_max_p and pr > eff_max_p:
                continue
            if not eff_max_p and not eff_unlimited:
                if pr < 1000000 or pr > 15000000:
                    continue
            d = p.get('d', '')
            if any(loc.lower() in d.lower() for loc in west_expand):
                results.append(p)

    # Sorting
    if eff_unlimited:
        results.sort(key=lambda x: x.get('pr', 0), reverse=True)
    elif eff_max_p:
        results.sort(key=lambda x: abs((x.get('pr') or 0) - eff_max_p))
    else:
        results.sort(key=lambda x: abs((x.get('pr') or 0) - 4000000))

    out_list = []
    for p in results[:3]:
        out_list.append({
            "code": p.get('c'),
            "bank": p.get('b'),
            "type": p.get('tn', 'บ้าน'),
            "district": p.get('d'),
            "province": p.get('p'),
            "price": f"{p.get('pr', 0):,} บาท",
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
6. **ความตรงประเด็นเรื่องประเภททรัพย์:** หากผู้ใช้ขอ "บ้าน" (เช่น ขอบ้านแถวบางแค, หาบ้าน) ให้แนะนำเฉพาะ บ้านเดี่ยว, บ้านแฝด หรือทาวน์โฮม/ทาวน์เฮ้าส์ เท่านั้น **ห้ามใส่คอนโดหรือที่ดินมาเด็ดขาด** เว้นแต่ผู้ใช้จะระบุคำว่า "คอนโด" หรือ "ห้องชุด" โดยตรง"""


def ask_gemini(user_id, user_text, is_continuous=False, retries=2):
    matched_props, search_mode = search_properties(user_text, user_id=user_id)
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

    if matched_props:
        prompt_parts.append(
            f"\n[ข้อมูลทรัพย์จริงในระบบที่ดึงมาให้ตอบ ({search_mode})]:\n"
            + json.dumps(matched_props, ensure_ascii=False, indent=2)
            + "\nคำสั่ง: ให้ตอบแนะนำข้อมูลทรัพย์จริงชุดนี้แก่ผู้ใช้ทันที โดยระบุรหัสทรัพย์ ธนาคาร ประเภท ทำเล และราคา ให้ชัดเจนทุกแปลง พร้อมแนะนำให้คลิกดูรูปและรายละเอียดเพิ่มเติมที่ https://assets.siwasup.com/catalog.html หรือแจ้งรหัสเพื่อจองคิวเปิดบ้านได้เลย"
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
                            return reply, [p.get('code') for p in matched_props], search_mode
        except Exception as e:
            print(f"[Gemini Error Attempt {attempt+1}]: {e}")
            time.sleep(1)

    return (
        "รับทราบครับ! สามารถตรวจสอบรูปจริงและรายละเอียดแปลงทั้งหมดได้ที่ Web Catalog https://assets.siwasup.com/catalog.html ได้เลยครับ",
        [p.get('code') for p in matched_props],
        search_mode
    )


def reply_line(reply_token, reply_text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": reply_text
            }
        ]
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


class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/logs"):
            store = load_chat_logs()
            body = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
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
                    def process_follow(uid):
                        prof = get_line_profile(uid)
                        append_chat_log({
                            "id": f"LOG_{int(time.time()*1000)}",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "user_name": prof.get("displayName"),
                            "user_pic": prof.get("pictureUrl"),
                            "user_id_tail": uid[-6:] if uid else "anon",
                            "event_type": "follow",
                            "user_text": "[แอดเพื่อนเข้าสู่ระบบ LINE OA]",
                            "ai_reply": "(ระบบส่งข้อความต้อนรับอัตโนมัติ)",
                            "matched_codes": [],
                            "search_mode": "FOLLOW_EVENT",
                            "latency_ms": 0
                        })
                    threading.Thread(target=process_follow, args=(user_id,), daemon=True).start()

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
                            if mtype == 'text':
                                ai_reply, matched_codes, search_mode = ask_gemini(uid, text, is_continuous=continuous)
                            else:
                                ai_reply = "น้องศิวาได้รับไฟล์/สติกเกอร์เรียบร้อยครับ หากต้องการค้นหาทรัพย์ พิมพ์รหัสทรัพย์หรือทำเล เช่น '1090965' หรือ 'บ้านเดี่ยว นนทบุรี งบ 4 ล้าน' ได้เลยครับ!"
                                matched_codes, search_mode = [], "NON_TEXT"

                            latency_ms = int((time.time() - t0) * 1000)
                            if token:
                                reply_line(token, ai_reply)

                            append_chat_log({
                                "id": f"LOG_{int(time.time()*1000)}",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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

                    threading.Thread(
                        target=process_msg,
                        args=(reply_token, user_id, user_text, msg_type, is_continuous),
                        daemon=True
                    ).start()
        except Exception as e:
            print(f"[Webhook Error]: {e}")


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
