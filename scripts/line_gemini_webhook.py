import http.server
import json
import urllib.request
import urllib.parse
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
ADMIN_EXPORT_SECRET = os.environ.get("ADMIN_EXPORT_SECRET", "SiwasupAdmin2026_SecureKey_99")

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
    store = None
    if os.path.exists(CHAT_LOG_PATH):
        try:
            with open(CHAT_LOG_PATH, "r", encoding="utf-8") as f:
                store = json.load(f)
        except Exception:
            pass
    # If local file missing or empty, attempt restoring from R2 backup
    if not store or not store.get("conversations"):
        try:
            req = urllib.request.Request("https://assets.siwasup.com/data/line_chat_logs.json?t=" + str(int(time.time())), headers={"User-Agent": "SiwasupSync/1.0"})
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    store = json.loads(r.read().decode("utf-8"))
        except Exception:
            pass

    if store and isinstance(store.get("conversations"), list):
        return store

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

        # Persistent Cloud Backup: Sync to Cloudflare R2 asynchronously so logs survive Render restarts
        if put_object_r2:
            def sync_r2():
                try:
                    put_object_r2("data/line_chat_logs.json", data_bytes, "application/json; charset=utf-8")
                except Exception as ex:
                    print(f"[R2 Sync Log Warn]: {ex}")
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

    # Detect requested quantity (e.g. "ขอ 5", "ขอไป 5", "ขอ 5 หลัง", "มี 4 ที่มั้ย")
    target_count = 3  # default fallback
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

    # Automatic geographic expansion if results < target_count in western/Bangkok area
    if len(results) < target_count and eff_locs and any(w in str(eff_locs) for w in ['Bangkok Noi', 'Taling Chan', 'Bang Phlat', 'Thon Buri', 'Bang Khae']):
        west_expand = ['Taling Chan', 'Bangkok Noi', 'Bang Phlat', 'Thawi Watthana', 'Phasi Charoen', 'Bang Khae', 'Thon Buri', 'Nonthaburi']
        existing_cat_codes = {p.get('c') for p in results}
        for p in CATALOG:
            if len(results) >= target_count * 2:
                break
            if p.get('c') in existing_cat_codes:
                continue
            if eff_types and p.get('t') not in eff_types:
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
            continue
        pr_str = re.sub(r'[^0-9]', '', str(sp.get("price") or "0"))
        pr = int(pr_str) if pr_str.isdigit() else 0
        if eff_max_p and pr > eff_max_p:
            continue
        if not eff_max_p and not eff_unlimited:
            if pr < 800000 or pr > 15000000:
                continue
        haystack = ((sp.get("title") or "") + " " + (sp.get("description") or "") + " " + (sp.get("location") or "") + " " + (sp.get("search_keywords") or "")).lower()
        if eff_locs:
            if not any(loc.lower() in haystack for loc in eff_locs):
                continue
        web_results.append({
            "c": str(sp.get("id")),
            "b": sp.get("bank_source") or "Siwasup",
            "tn": sp.get("category") or "บ้านเดี่ยว",
            "d": (sp.get("location") or sp.get("title") or "กรุงเทพฯ").split("•")[0].strip(),
            "p": (sp.get("location") or "กรุงเทพมหานคร").split("•")[-1].strip(),
            "pr": pr,
            "sqw": (sp.get("size") or "-").replace(" ตร.ว.", ""),
            "sqm": (sp.get("usable_area") or "-").replace(" ตร.ม.", ""),
            "_web": True
        })

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

    out_list = []
    for p in results[:target_count]:
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
6. **ความตรงประเด็นเรื่องประเภททรัพย์:** หากผู้ใช้ขอ "บ้าน" (เช่น ขอบ้านแถวบางแค, หาบ้าน) ให้แนะนำเฉพาะ บ้านเดี่ยว, บ้านแฝด หรือทาวน์โฮม/ทาวน์เฮ้าส์ เท่านั้น **ห้ามใส่คอนโดหรือที่ดินมาเด็ดขาด** เว้นแต่ผู้ใช้จะระบุคำว่า "คอนโด" หรือ "ห้องชุด" โดยตรง
7. **การสอบถามเพื่อคัดกรองความต้องการ (Qualifying Leads):** หากผู้ใช้บอกความต้องการลอยๆ แบบกว้างมาก (เช่น "อยากได้บ้าน", "หาบ้าน", "สนใจคอนโด", "มีบ้านไหม") โดยที่ยังไม่ได้ระบุทำเลหรือช่วงราคา **อย่าเพิ่งรีบสุ่มทรัพย์มาแนะนำ** ให้ตอบรับอย่างกระตือรือร้นและสุภาพ แล้วสอบถามข้อมูลเพิ่มเติมสั้นๆ (เช่น สะดวกโซน/ทำเลไหนเป็นพิเศษ และมีงบประมาณในใจประมาณเท่าไหร่) เพื่อคัดแปลงที่ตรงใจที่สุดให้ครับ"""


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
            f"\n[ข้อมูลทรัพย์จริงที่ระบบดึงมาให้ตอบ ({search_mode}) ทั้งหมด {len(matched_props)} หลัง]:\n"
            + json.dumps(matched_props, ensure_ascii=False, indent=2)
            + f"\nคำสั่งสำคัญ: ผู้ใช้ขอดูทรัพย์ ให้ตอบแนะนำข้อมูลทรัพย์จริงครบทั้ง {len(matched_props)} หลัง อย่าตัดทิ้งหรือสรุปย่อ ระบุรหัสทรัพย์ ราคา และทำเลให้ครบถ้วนทุกแปลง และแนะนำให้คลิกดูรูปรายละเอียด https://assets.siwasup.com/catalog.html หรือจองเปิดบ้านได้"
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
                "price": f"{p.get('pr', 0):,} บาท" if isinstance(p.get('pr'), (int, float)) else str(p.get('pr', '')),
                "location": f"{p.get('d', '')} • {p.get('p', 'กทม.')}",
                "size": f"{p.get('sqw', '')} ตร.ว." if p.get('sqw') else "",
                "usable_area": f"{p.get('sqm', '')} ตร.ม." if p.get('sqm') else "",
                "main_image": p.get("img") or "https://assets.siwasup.com/fallback_property.jpg"
            }
    return None


def build_property_flex_bubble(prop, client_name="คุณลูกค้า", agent_ref="TON"):
    pid = str(prop.get("id") or prop.get("code") or "")
    title = str(prop.get("title") or "ทรัพย์คัดสรรพิเศษ ศิวาทรัพย์")
    price = str(prop.get("price") or "กรุณาสอบถาม")
    category = str(prop.get("category") or "อสังหาริมทรัพย์")
    location = str(prop.get("location") or "กรุงเทพมหานครและปริมณฑล")
    size_str = str(prop.get("size") or prop.get("usable_area") or "")
    
    img_url = prop.get("main_image") or "https://assets.siwasup.com/fallback_property.jpg"
    if not img_url.startswith("http"):
        img_url = "https://assets.siwasup.com/fallback_property.jpg"

    detail_url = f"https://assets.siwasup.com/catalog.html?id={pid}&property={pid}&ref={agent_ref}&src=flex_carousel#prop-{pid}"

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
                            "text": f"รหัส {pid}",
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


def build_property_flex_carousel(props, client_name="คุณลูกค้า", agent_ref="TON"):
    bubbles = [build_property_flex_bubble(p, client_name, agent_ref) for p in props[:10] if p]
    if not bubbles:
        return None
    return {
        "type": "flex",
        "altText": f"🏠 คัดสรรทรัพย์พิเศษ {len(bubbles)} หลัง สำหรับ {client_name} (ศิวาทรัพย์ Co-Broker)",
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
            "text": reply_text
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
_R2_LOBBY_RESTORED = False

def load_lobby_data():
    global _R2_LOBBY_RESTORED
    if not _R2_LOBBY_RESTORED and os.environ.get("PORT"):
        _R2_LOBBY_RESTORED = True
        try:
            url = f"https://assets.siwasup.com/{_R2_LOBBY_VAULT_KEY}?t={int(time.time())}"
            req = urllib.request.Request(url, headers={"User-Agent": "SiwasupRenderVault/1.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                if r.status == 200:
                    cloud_store = json.loads(r.read().decode("utf-8"))
                    if isinstance(cloud_store, dict) and ("approved" in cloud_store or "pending" in cloud_store):
                        with open(LOBBY_PATH, "w", encoding="utf-8") as f:
                            json.dump(cloud_store, f, ensure_ascii=False, indent=2)
                        print(f"[Vault] Restored lobby_applicants from R2 ({len(cloud_store.get('approved', []))} approved)")
                        return cloud_store
        except Exception as e:
            print(f"[Vault] Initial R2 restore note: {e}")
    if os.path.exists(LOBBY_PATH):
        try:
            with open(LOBBY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warn] Failed to read lobby_applicants.json: {e}")
    return {"updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pending": [], "approved": []}

def save_lobby_data(store):
    with LOBBY_LOCK:
        store["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            with open(LOBBY_PATH, "wb") as f:
                f.write(data_bytes)
        except Exception as e:
            print(f"[Error] Failed to save lobby local: {e}")
        if put_object_r2 and os.environ.get("PORT"):
            threading.Thread(target=lambda: put_object_r2(_R2_LOBBY_VAULT_KEY, data_bytes, "application/json"), daemon=True).start()


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
    "admin": "https://assets.siwasup.com/admin_lobby_manager.html",
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
            "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        store.setdefault("approved", []).insert(0, seat)
        changed = True
    else:
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
CONTRACTS_LOCK = threading.Lock()
_R2_CONTRACTS_VAULT_KEY = "_vault/contracts_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_contracts_vault_v1", hashlib.sha256).hexdigest()[:32] + ".json"

def load_contracts_data():
    if os.path.exists(CONTRACTS_PATH):
        try:
            with open(CONTRACTS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warn] Failed to read exclusive_contracts.json: {e}")
    return {"updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "contracts": []}

def save_contracts_data(store):
    with CONTRACTS_LOCK:
        store["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            with open(CONTRACTS_PATH, "wb") as f:
                f.write(data_bytes)
        except Exception as e:
            print(f"[Error] Failed to save contracts local: {e}")
        if put_object_r2 and os.environ.get("PORT"):
            threading.Thread(target=lambda: put_object_r2(_R2_CONTRACTS_VAULT_KEY, data_bytes, "application/json"), daemon=True).start()


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
จงอ่านและสกัดข้อมูลจากภาพอย่างละเอียด ถูกต้อง 100% ตอบกลับเฉพาะ JSON ที่มีโครงสร้างดังนี้เท่านั้น:
{
  "doc_type": "title_deed",
  "deed_number": "โฉนดที่ดินเลขที่",
  "land_number": "เลขที่ดิน",
  "survey_page": "หน้าสำรวจ",
  "rawang": "ระวาง",
  "subdistrict": "ตำบล/แขวง",
  "district": "อำเภอ/เขต",
  "province": "จังหวัด",
  "area_rai": "จำนวนไร่ (ตัวเลข)",
  "area_ngan": "จำนวนงาน (ตัวเลข)",
  "area_sqw": "จำนวนตารางวา (ตัวเลข)",
  "area_total_sqw": "คำนวณพื้นที่รวมเป็นตารางวา เช่น 1 ไร่ 2 งาน 50 วา = 650 ตร.ว.",
  "owner_name": "ชื่อผู้ถือกรรมสิทธิ์ / ผู้ถือกรรมสิทธิ์เดิม"
}
หากมองไม่เห็นฟิลด์ใด ให้ใส่เป็นสตริงว่าง "" ห้ามเดาข้อมูล"""
    else:
        prompt = """สกัดข้อมูลสำคัญจากเอกสารอสังหาริมทรัพย์ไทยในภาพนี้ ตอบกลับเป็น JSON ที่ระบุประเภทเอกสารและข้อมูลสำคัญ"""

    models_to_try = ["gemini-flash-lite-latest", "gemini-flash-latest"]
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
                        return json.loads(raw_json)
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
        if level == "exec":
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
        if path == "/api/contracts/list":
            agent_ref = query.get("agent_ref", [""])[0]
            store = load_contracts_data()
            contracts = store.get("contracts", [])
            if agent_ref:
                contracts = [c for c in contracts if c.get("agent_ref") == agent_ref or c.get("agent_id") == agent_ref]
            self._send_json(200, {"status": "success", "count": len(contracts), "contracts": contracts})
            return

        if path == "/api/bundle/flex":
            bundle_raw = query.get("bundle", [""])[0]
            client_name = query.get("for", ["คุณลูกค้า"])[0]
            agent_ref = query.get("ref", ["TON"])[0]
            
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
                mem = next((a for a in store.get("approved", []) if a.get("lineUserId") == sub or a.get("id") == "app_office_004"), None)
                if mem:
                    mem["last_active_at"] = int(time.time())
                    save_lobby_data(store)
            self._send_json(200, {"ok": True, "now": int(time.time())})
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
                save_lobby_data(store)
                self._send_json(200, {"status": "approved", "member": sanitize_member(mem), "isAdmin": is_admin_member(mem), "line": line_info})
                return
            pend = next((a for a in store.get("pending", []) if a.get("lineUserId") == sub), None)
            if pend:
                self._send_json(200, {"status": "pending", "applicant": sanitize_member(pend), "line": line_info})
                return
            self._send_json(200, {"status": "guest", "line": line_info})
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
            if not code or not st or (cm and not hmac.compare_digest(cm.group(1), st.get("n", ""))):
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
                    store.setdefault("audit_log", []).insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔗 ผูก LINE ผู้ดูแลระบบสูงสุด: {seat.get('name')}")
                    save_lobby_data(store)

            for m in store.get("approved", []):
                if m.get("lineUserId") == sub and picture and (not m.get("avatar") or "unsplash.com" in str(m.get("avatar", ""))):
                    m["avatar"] = picture
                    save_lobby_data(store)
                    break
            session = make_token({"sub": sub, "name": name, "picture": picture}, SESSION_TTL)
            self._redirect(FRONTEND_URLS[st.get("r", "register")] + "#session=" + session, clear_cookie)
            return

        if path in ["/logs", "/api/export-logs"]:
            secret = query.get("secret", [""])[0]
            client_ip = self.client_address[0] if hasattr(self, 'client_address') else ''
            is_local = client_ip in ["127.0.0.1", "localhost", "::1"]

            # Security verification
            if not is_local and secret != ADMIN_EXPORT_SECRET:
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
                        c_dt = datetime.strptime(c.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
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
                "export_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            "/api/lobby/approve": "admin",
            "/api/lobby/reject": "admin",
            "/api/lobby/revoke": "admin",
            "/api/lobby/rollback": "admin",
            "/api/lobby/backup": "admin",
            "/api/lobby/update-permissions": "exec",
        }
        acting_member = None
        if path in ADMIN_POST_LEVELS:
            acting_member = self._require(ADMIN_POST_LEVELS[path])
            if not acting_member:
                return

        if path == "/api/ocr/contract":
            content_length = int(self.headers.get('Content-Length', 0))
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
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                store = load_contracts_data()
                cid = payload.get("id") or f"SW-CNT-{int(time.time()*1000)%1000000}"
                payload["id"] = cid
                payload["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Expiry calculation (default 90 days if not set)
                days = int(payload.get("contract_days") or 90)
                exp_ts = time.time() + (days * 86400)
                payload["expires_at"] = datetime.fromtimestamp(exp_ts).strftime("%Y-%m-%d")
                
                # Replace or prepend
                contracts = store.setdefault("contracts", [])
                contracts = [c for c in contracts if c.get("id") != cid]
                contracts.insert(0, payload)
                store["contracts"] = contracts
                save_contracts_data(store)
                self._send_json(200, {"status": "success", "contract": payload})
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
                allowed = ("id", "name", "nickname", "phone", "line_id", "zone", "affiliation", "affiliation_label", "avatar", "submitted_at")
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
                save_lobby_data(store)
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
                store = load_lobby_data()
                target_idx = -1
                for idx, p in enumerate(store.get("pending", [])):
                    if p.get("id") == app_id:
                        target_idx = idx
                        break
                if target_idx != -1:
                    applicant = store["pending"].pop(target_idx)
                    _digits = lambda v: re.sub(r"\D", "", v or "")
                    existing = next((a for a in store.get("approved", []) if not a.get("lineUserId") and _digits(a.get("phone")) and _digits(a.get("phone")) == _digits(applicant.get("phone"))), None)
                    if existing and applicant.get("lineUserId"):
                        existing["lineUserId"] = applicant["lineUserId"]
                        if applicant.get("avatar") and not existing.get("avatar"):
                            existing["avatar"] = applicant["avatar"]
                        store.setdefault("audit_log", []).insert(0, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔗 ผูก LINE เข้ากับสมาชิกเดิม: {existing.get('name')}")
                        save_lobby_data(store)
                        self._send_json(200, {"status": "success", "approved": sanitize_member(existing), "linked": True})
                        return
                    approved_item = {
                        "id": applicant.get("id"),
                        "name": applicant.get("name"),
                        "nickname": applicant.get("nickname"),
                        "phone": applicant.get("phone"),
                        "line_id": applicant.get("line_id"),
                        "zone": applicant.get("zone"),
                        "avatar": applicant.get("avatar", ""),
                        "lineUserId": applicant.get("lineUserId"),
                        "role": payload.get("role", "Co-Broker Partner"),
                        "title": payload.get("title", ""),
                        "badges": payload.get("badges", []),
                        "permissions": payload.get("permissions", {}),
                        "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    store.setdefault("approved", []).insert(0, approved_item)
                    audit_entry = f"[{approved_item['approved_at']}] 🟢 อนุมัติสิทธิ์: {approved_item.get('name')} ({approved_item.get('role')})"
                    store.setdefault("audit_log", []).insert(0, audit_entry)
                    store["audit_log"] = store["audit_log"][:100]
                    save_lobby_data(store)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "approved": sanitize_member(approved_item)}, ensure_ascii=False).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Applicant not found"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/reject":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                app_id = payload.get("applicantId")
                store = load_lobby_data()
                store["pending"] = [p for p in store.get("pending", []) if p.get("id") != app_id]
                save_lobby_data(store)
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
                    if "title" in payload: m["title"] = payload["title"]
                    if "badges" in payload: m["badges"] = payload["badges"]
                    if "permissions" in payload: m["permissions"] = payload["permissions"]
                    m["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    audit_entry = f"[{m['updated_at']}] ⚙️ ปรับสิทธิ์: {m.get('name')} เป็น {m.get('role')} ({len(m.get('badges', []))} สิทธิ์)"
                    store.setdefault("audit_log", []).insert(0, audit_entry)
                    store["audit_log"] = store["audit_log"][:100]
                    save_lobby_data(store)
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
                target_member = next((a for a in store.get("approved", []) if a.get("id") == app_id), None)
                if target_member and is_super_tech_root(target_member):
                    self._send_json(403, {"error": "🔒 บัญชีสถาปัตยกรรมระบบสูงสุด (Super Tech Root) ถูกล็อกถาวร ไม่สามารถคัดออกได้"})
                    return
                store = load_lobby_data()
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
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "reason": reason
                    }
                    store.setdefault("rollback_history", []).insert(0, rollback_record)
                    store["rollback_history"] = store["rollback_history"][:50]
                    audit_entry = f"[{rollback_record['timestamp']}] คัดออก/เพิกถอนสิทธิ์: {revoked_member.get('name')} ({revoked_member.get('role')})"
                    store.setdefault("audit_log", []).insert(0, audit_entry)
                    store["audit_log"] = store["audit_log"][:100]
                    save_lobby_data(store)
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
                        audit_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ↩️ Rollback คืนสิทธิ์: {restored_member.get('name')}"
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

        if path == "/api/lobby/backup":
            try:
                store = load_lobby_data()
                backup_name = f"lobby_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_dir = os.path.join(os.path.dirname(LOBBY_PATH), "backups")
                os.makedirs(backup_dir, exist_ok=True)
                backup_file = os.path.join(backup_dir, backup_name)
                with open(backup_file, "w", encoding="utf-8") as bf:
                    json.dump(store, bf, ensure_ascii=False, indent=2)
                audit_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 💾 สำรองข้อมูลสถานะ: {backup_name}"
                store.setdefault("audit_log", []).insert(0, audit_entry)
                save_lobby_data(store)
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
                        user_name = prof.get("displayName", "ท่าน")
                        welcome_msg = (
                            f"สวัสดีครับคุณ {user_name}! ยินดีต้อนรับสู่ Siwasup Co-Broker OS ครับ 🏠✨\n\n"
                            "น้องศิวาเป็น AI ผู้ช่วยค้นหาทรัพย์และประสานงานนำชมบ้าน พร้อมทำงาน 24 ชั่วโมงครับ\n\n"
                            "📋 สำหรับทีมงานออฟฟิศและตัวแทนพันธมิตร เพื่อเริ่มต้นใช้งานและรับ 'นามบัตรดิจิทัลทางการ' "
                            "กรุณาลงทะเบียนเข้าสู่ระบบที่นี่ได้เลยครับ:\n"
                            "👉 https://assets.siwasup.com/agent_registration.html\n\n"
                            "💡 หรือพิมพ์ค้นหาบ้านได้ทันที เช่น:\n"
                            "• 'บ้านเดี่ยว นนทบุรี งบ 4 ล้าน'\n"
                            "• 'ค้นหาทรัพย์ 1090965'\n"
                            "• พิมพ์ 'นามบัตร' หรือ 'ลงทะเบียน' เพื่อเปิดดูหรือสร้างนามบัตรของคุณได้ตลอดเวลาครับ"
                        )
                        if rtoken:
                            reply_line(rtoken, welcome_msg)
                        append_chat_log({
                            "id": f"LOG_{int(time.time()*1000)}",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
                            if mtype == 'text':
                                text_clean = text.strip().lower()
                                if any(k in text_clean for k in ['สมัคร', 'ลงทะเบียน', 'login', 'เข้าสู่ระบบ', 'ขอนามบัตร', 'นามบัตร', 'โปรไฟล์', 'profile', 'เอเจนต์', 'เอเจน', 'ตัวแทน', 'ร่วมงาน', 'ขอเข้ากลุ่ม', 'เข้ากลุ่ม', 'นายหน้า', 'co-broker', 'cobroker', 'ขอลิงก์', 'ขอลิงค์', 'วิธีสมัคร', 'อยากเป็นเอเจนต์', 'ลิงก์สมัคร']):
                                    ai_reply = (
                                        f"สวัสดีครับคุณ {prof.get('displayName', '')}! สำหรับการลงทะเบียนทีมงานออฟฟิศ หรือรับนามบัตรดิจิทัลทางการของ Siwasup Co-Broker OS:\n\n"
                                        "👉 คลิกที่นี่เพื่อลงทะเบียน/เข้าสู่ระบบได้ทันทีครับ:\n"
                                        "https://assets.siwasup.com/agent_registration.html\n\n"
                                        "เมื่อลงทะเบียนเสร็จ ท่านจะได้นามบัตรเฉพาะตัวพร้อมลิงก์และ QR Code ส่งต่อให้ลูกค้าดูได้ทันทีครับ ✨"
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
                                            flex_carousel = build_property_flex_carousel(full_props, client_name=prof.get("displayName", "คุณลูกค้า"))
                            else:
                                ai_reply = "น้องศิวาได้รับไฟล์/สติกเกอร์เรียบร้อยครับ หากต้องการค้นหาทรัพย์ พิมพ์รหัสทรัพย์หรือทำเล เช่น '1090965' หรือ 'บ้านเดี่ยว นนทบุรี งบ 4 ล้าน' ได้เลยครับ!"
                                matched_codes, search_mode, matched_props, flex_carousel = [], "NON_TEXT", [], None

                            latency_ms = int((time.time() - t0) * 1000)
                            if token:
                                reply_line(token, ai_reply, flex_message=flex_carousel)

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
