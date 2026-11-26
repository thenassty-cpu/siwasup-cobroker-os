# -*- coding: utf-8 -*-
"""
Crawler & Integrator for:
1. Krungthai NPA (KTB) - https://npa.krungthai.com
2. Alpha Capital AMC (ALPHA) - https://alphacapamc.com

Saves full nationwide master files to:
- data/ktb_property_master.json
- data/alpha_property_master.json

And merges Bangkok & Vicinity (6 provinces) into:
- siwasup_all_properties.json
- siwasup_all_properties.js
"""

import html as html_lib
import json
import os
import re
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==============================================================================
# ⚙️ CONFIGURATION TOGGLES (ปรับเปลี่ยนได้ทันทีหลังปรึกษาคุณกูล)
# ==============================================================================
ONLY_BKK_AND_VICINITY = True   # True = เอาขึ้นหน้าเว็บเฉพาะ 6 จังหวัด กทม.และปริมณฑล, False = ทั่วประเทศ
MERGE_ALPHA_INTO_KTB = False   # False = แยกป้าย KTB และ ALPHA, True = ยุบรวม ALPHA เข้าใน KTB

BKK_VICINITY_PROVINCES = (
    "กรุงเทพมหานคร",
    "นนทบุรี",
    "ปทุมธานี",
    "สมุทรปราการ",
    "สมุทรสาคร",
    "นครปฐม",
)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS_HTML = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "th-TH,th;q=0.9,en;q=0.8",
}

HEADERS_JSON = {
    "User-Agent": HEADERS_HTML["User-Agent"],
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def map_zone_keywords(location_str, title_str=""):
    """Enrich search_keywords so properties match the 10 BKK/Vicinity zones in #filter-location."""
    combined = f"{location_str} {title_str}"
    zones = []
    if any(k in combined for k in ("บางขุนเทียน", "ท่าข้าม", "พระราม 2", "พระราม2", "จอมทอง", "ทุ่งครุ", "ราษฎร์บูรณะ", "บางบอน", "สมุทรสาคร", "กระทุ่มแบน", "มหาชัย")):
        zones.append("พระราม 2 ท่าข้าม บางขุนเทียน")
    if any(k in combined for k in ("บางแค", "เพชรเกษม", "ท่าพระ", "ภาษีเจริญ", "ตลิ่งชัน", "ทวีวัฒนา", "หนองแขม", "บางกอกน้อย", "บางกอกใหญ่", "ธนบุรี", "คลองสาน", "บางพลัด", "นครปฐม", "สามพราน", "พุทธมณฑล", "ศาลายา")):
        zones.append("ท่าพระ ฝั่งธน บางแค เพชรเกษม")
    if any(k in combined for k in ("รามอินทรา", "สายไหม", "บางเขน", "มีนบุรี", "คลองสามวา", "คันนายาว", "ลาดพร้าว", "บึงกุ่ม", "หนองจอก")):
        zones.append("รามอินทรา สายไหม บางเขน มีนบุรี")
    if any(k in combined for k in ("ลาดพร้าว", "บางกะปิ", "นวมินทร์", "รามคำแหง", "สะพานสูง", "วังทองหลาง", "สวนหลวง")):
        zones.append("ลาดพร้าว บางกะปิ นวมินทร์ รามคำแหง")
    if any(k in combined for k in ("รัชดา", "พระราม 9", "ห้วยขวาง", "ดินแดง", "พญาไท", "ราชเทวี", "วัฒนา", "คลองเตย", "สาทร", "บางรัก", "ปทุมวัน", "ยานนาวา", "บางคอแหลม")):
        zones.append("พระราม 9 รัชดา ห้วยขวาง")
    if any(k in combined for k in ("วิภาวดี", "จตุจักร", "ดอนเมือง", "แจ้งวัฒนะ", "หลักสี่", "บางซื่อ", "สายไหม")):
        zones.append("วิภาวดี จตุจักร ดอนเมือง แจ้งวัฒนะ")
    if any(k in combined for k in ("บางนา", "ศรีนครินทร์", "สมุทรปราการ", "เมืองสมุทรปราการ", "บางพลี", "พระประแดง", "พระสมุทรเจดีย์", "บางบ่อ", "สำโรง", "เทพารักษ์", "พระโขนง")):
        zones.append("บางนา ศรีนครินทร์ สมุทรปราการ")
    if any(k in combined for k in ("ลาดกระบัง", "อ่อนนุช", "สุวรรณภูมิ", "ประเวศ", "สวนหลวง", "ร่มเกล้า")):
        zones.append("ลาดกระบัง อ่อนนุช สุวรรณภูมิ")
    if any(k in combined for k in ("นนทบุรี", "บางใหญ่", "บางบัวทอง", "ปากเกร็ด", "บางกรวย", "ไทรน้อย", "เมืองนนทบุรี", "รัตนาธิเบศร์", "ราชพฤกษ์")):
        zones.append("บางใหญ่ บางบัวทอง นนทบุรี")
    if any(k in combined for k in ("ปทุมธานี", "รังสิต", "ลำลูกกา", "คลองหลวง", "ธัญบุรี", "เมืองปทุมธานี", "ลาดหลุมแก้ว", "สามโคก", "พหลโยธิน")):
        zones.append("รังสิต ลำลูกกา คลองหลวง ปทุมธานี")
    return " ".join(zones)


def sanitize_no_phone_or_contact(text):
    """Strip any bank officer names, phone numbers, or contact prompts from descriptions."""
    if not text:
        return ""
    s = str(text)
    # Remove Thai mobile & landline numbers (e.g. 084-924-9966, 02-xxx-xxxx)
    s = re.sub(r"\b0[2689]\d[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b", "", s)
    # Remove lines mentioning สนใจติดต่อ / ติดต่อพนักงาน / โทร.
    clean_lines = []
    for line in s.splitlines():
        if any(bad in line for bad in ("สนใจติดต่อ", "ติดต่อพนักงาน", "ติดต่อเจ้าหน้าที่ธนาคาร", "เบอร์โทร")):
            continue
        clean_lines.append(line.strip())
    return "\n".join([l for l in clean_lines if l])


def normalize_category(raw_cat, title=""):
    s = f"{raw_cat} {title}"
    if any(k in s for k in ("ทาวน์เฮ้าส์", "ทาวน์โฮม", "Townhouse", "Townhome")):
        return "ทาวน์โฮม"
    if any(k in s for k in ("คอนโด", "ห้องชุด", "Condo", "อพาร์ทเมนท์")):
        return "คอนโด"
    if any(k in s for k in ("อาคารพาณิชย์", "ตึกแถว", "โฮมออฟฟิศ", "สำนักงาน")):
        return "อาคารพาณิชย์"
    if any(k in s for k in ("ที่ดินเปล่า", "ที่ดิน")):
        return "ที่ดินเปล่า"
    return "บ้านเดี่ยว"


def format_ktb_area(area_str, sum_area_num=None):
    if not area_str and not sum_area_num:
        return "-"
    s = str(area_str or "").strip()
    m = re.match(r"^(\d+)-(\d+)-([0-9.]+)$", s)
    if m:
        rai, ngan, wah = int(m.group(1)), int(m.group(2)), float(m.group(3))
        if rai == 0 and ngan == 0:
            return f"{wah:g} ตร.ว."
        total_wah = rai * 400 + ngan * 100 + wah
        if rai > 0:
            return f"{rai} ไร่ {ngan} งาน {wah:g} ตร.ว. ({total_wah:g} ตร.ว.)"
        return f"{total_wah:g} ตร.ว."
    if sum_area_num:
        return f"{float(sum_area_num):g} ตร.ว."
    return s


# ==============================================================================
# 1. CRAWL KRUNGTHAI NPA (KTB)
# ==============================================================================
def fetch_ktb_page(page_num):
    payload = json.dumps(
        {"paging": {"currentPage": page_num, "rowsPerPage": 100, "totalRows": 0}}
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://npa.krungthai.com/api/v1/product/searchAll",
        data=payload,
        headers=HEADERS_JSON,
        method="POST",
    )
    with urllib.request.urlopen(req, context=ctx, timeout=25) as r:
        res = json.loads(r.read().decode("utf-8", errors="ignore"))
    return res.get("dataResponse", []), res.get("paging", {})


def crawl_all_ktb():
    print("[KTB] Fetching page 1...")
    first_items, paging = fetch_ktb_page(1)
    page_count = int(paging.get("pageCount") or 1)
    total_rows = int(paging.get("totalRows") or len(first_items))
    print(f"[KTB] Total rows={total_rows}, pages={page_count}")

    raw_items = list(first_items)
    if page_count > 1:
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = {ex.submit(fetch_ktb_page, p): p for p in range(2, page_count + 1)}
            for fut in as_completed(futures):
                try:
                    items, _ = fut.result()
                    raw_items.extend(items)
                except Exception as e:
                    print(f"[KTB] Error on page {futures[fut]}: {e}")

    normalized = []
    seen_ids = set()
    for it in raw_items:
        coll_code = str(it.get("collCode") or it.get("collGrpId") or "").strip()
        if not coll_code:
            continue
        prop_id = f"KTB-{coll_code}"
        if prop_id in seen_ids:
            continue
        seen_ids.add(prop_id)

        prov_raw = (it.get("shrProvinceName") or "").strip()
        prov_clean = prov_raw.replace("จังหวัด", "").strip()
        amphur = (it.get("shrAmphurName") or "").replace("อำเภอ", "อ.").replace("เขต", "เขต").strip()
        tambon = (it.get("shrTambonName") or "").replace("ตำบล", "ต.").replace("แขวง", "แขวง").strip()
        is_bkk = any(b in prov_clean for b in BKK_VICINITY_PROVINCES)

        raw_cat = (it.get("collCateName") or "ทรัพย์สินรอการขาย").strip()
        proj_name = (it.get("propertyName") or "").strip()
        cat = normalize_category(raw_cat, proj_name)

        loc_display = f"{amphur} • {prov_clean}".strip(" •")
        if proj_name:
            title = f"{raw_cat} {proj_name} ({amphur} {prov_clean}) รหัส {coll_code}"
        else:
            title = f"ทรัพย์ NPA KTB: {raw_cat} โซน{amphur} ({prov_clean}) รหัส {coll_code}"

        price_str = str(it.get("price") or it.get("nmlPrice") or "ติดต่อเจ้าหน้าที่").strip()
        size_str = format_ktb_area(it.get("area") or it.get("calSumAreaCollGrpId"), it.get("sumAreaNum"))

        floor_val = it.get("floor")
        usable_str = "-"
        if floor_val:
            try:
                f_num = float(floor_val)
                if f_num > 0:
                    usable_str = f"อาคาร {int(f_num) if f_num.is_integer() else f_num} ชั้น"
            except Exception:
                pass

        bed_val = it.get("bedroomNum")
        bath_val = it.get("bathroomNum")
        bed_str = f"{bed_val} ห้องนอน" if bed_val else "-"
        bath_str = f"{bath_val} ห้องน้ำ" if bath_val else "-"

        # Gallery images from listImg
        gallery = []
        list_img = it.get("listImg") or []
        if isinstance(list_img, list):
            for img_obj in sorted(list_img, key=lambda x: x.get("seqNo") or 999):
                fn = (img_obj.get("fileName") or "").strip()
                if fn:
                    url = f"https://npa.krungthai.com/image/product/{fn}"
                    if url not in gallery:
                        gallery.append(url)
        thumb_fn = (it.get("fileName") or "").strip()
        if not gallery and thumb_fn:
            gallery.append(f"https://npa.krungthai.com/image/product/{thumb_fn}")
        if not gallery:
            gallery.append("https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600")

        lat = None
        lng = None
        try:
            if it.get("lat") and it.get("lon"):
                lat = float(it["lat"])
                lng = float(it["lon"])
        except Exception:
            pass

        house_no = str(it.get("addr") or "").strip()
        deed_raw = str(it.get("collMonoCodeAll") or it.get("collMonoCode") or "").strip()
        deed_str = f"โฉนดเลขที่: {deed_raw}" if deed_raw else ""
        road = str(it.get("road") or "").strip()
        addr_parts = [p for p in [tambon, amphur, prov_clean] if p]
        if road:
            addr_parts.insert(0, f"ถ.{road}")
        address_full = " ".join(addr_parts)

        near_parts = []
        for nk, nl in [("nearHospitalName", "รพ."), ("nearSchoolName", "รร."), ("nearShopName", "ห้าง/แหล่งชุมชน")]:
            if it.get(nk):
                near_parts.append(f"{nl}: {it[nk]}")

        desc_lines = [
            f"ประเภททรัพย์: {raw_cat}",
            f"ทำเลที่ตั้ง: {address_full or loc_display}",
            f"เนื้อที่ดิน: {size_str}",
        ]
        if proj_name:
            desc_lines.insert(1, f"ชื่อโครงการ / หมู่บ้าน: {proj_name}")
        if usable_str != "-":
            desc_lines.append(f"ลักษณะอาคาร: {usable_str}")
        if near_parts:
            desc_lines.append("สถานที่ใกล้เคียง: " + " | ".join(near_parts))

        specs_obj = {}
        if proj_name:
            specs_obj["project_name"] = proj_name
        if house_no:
            specs_obj["house_no"] = house_no
        if deed_str:
            specs_obj["deed_no"] = deed_str
        if address_full:
            specs_obj["address_full"] = address_full

        zone_kw = map_zone_keywords(f"{address_full} {loc_display}", title)
        search_kw = f"KTB กรุงไทย {coll_code} {proj_name} {address_full} {raw_cat} {zone_kw}".strip()

        prop = {
            "id": prop_id,
            "code": coll_code,
            "title": title,
            "category": cat,
            "bank_source": "KTB",
            "sub_source": "KTB",
            "province": prov_clean,
            "is_bkk_vicinity": is_bkk,
            "price": price_str,
            "size": size_str,
            "usable_area": usable_str,
            "bedrooms": bed_str,
            "bathrooms": bath_str,
            "location": loc_display,
            "status": "New",
            "main_image": gallery[0],
            "gallery": gallery,
            "description": sanitize_no_phone_or_contact("\n".join(desc_lines)),
            "specs": specs_obj,
            "search_keywords": search_kw,
        }
        if lat and lng:
            prop["lat"] = lat
            prop["lng"] = lng

        normalized.append(prop)

    print(f"[KTB] Normalized {len(normalized)} properties (BKK & Vicinity: {sum(1 for x in normalized if x['is_bkk_vicinity'])})")
    return normalized


# ==============================================================================
# 2. CRAWL ALPHA CAPITAL AMC (ALPHA)
# ==============================================================================
def parse_alpha_cards_from_html(html_text):
    # Split by <div class="property-item
    parts = re.split(r'<div class="property-item\b[^>]*>', html_text)[1:]
    items = []
    for part in parts:
        # Cut at footer or comparison section if last card on page
        part = part.split('<div class="compare-popup')[0].split("<footer")[0]

        m_link = re.search(r'href=["\'](https://alphacapamc\.com/property/([^"\'/]+)/)["\']', part)
        if not m_link:
            continue
        link, slug = m_link.group(1), m_link.group(2)

        # Gallery images from swiper-slide
        imgs = re.findall(r'src=["\'](https://alphacapamc\.com/wp-content/uploads/[^"\']+)["\']', part)
        gallery = []
        for u in imgs:
            if "Share-Alpha-cap" in u:
                continue
            # Prefer full size or 1200x800
            clean_u = re.sub(r"-\d+x\d+(?=\.(?:jpg|jpeg|png|webp)$)", "", u, flags=re.I)
            if u not in gallery:
                gallery.append(u)

        cates = [
            html_lib.unescape(c.strip())
            for c in re.findall(r'<p class="propertyItem-cate">\s*(.*?)\s*</p>', part, flags=re.S)
        ]
        raw_cat = cates[0] if len(cates) > 0 else "ทรัพย์สินรอการขาย"
        code = cates[1] if len(cates) > 1 else slug.upper()
        loc_raw = cates[2] if len(cates) > 2 else ""

        m_title = re.search(r'<p class="propertyItem-title">\s*(.*?)\s*</p>', part, flags=re.S)
        raw_title = html_lib.unescape(m_title.group(1).strip()) if m_title else f"{raw_cat} {code}"

        m_map = re.search(r"google\.com/maps/place/([0-9.]+),([0-9.]+)", part)
        lat = float(m_map.group(1)) if m_map else None
        lng = float(m_map.group(2)) if m_map else None

        m_usable = re.search(r"พื้นที่ใช้สอย:\s*</span>\s*([^<]+)</p>", part)
        usable_str = m_usable.group(1).strip() if m_usable else "-"

        m_size = re.search(r"เนื้อที่:\s*</span>\s*([^<]+)</p>", part)
        size_str = m_size.group(1).strip() if m_size else "-"

        m_price = re.search(r'<p class="price[^>]*>\s*<span[^>]*>\s*([0-9,]+)\s*</span>', part)
        price_str = m_price.group(1).strip() if m_price else "ติดต่อเจ้าหน้าที่"

        m_prov = re.search(r"จ\.([ก-๙]+)", loc_raw)
        prov_clean = m_prov.group(1).strip() if m_prov else loc_raw
        is_bkk = any(b in prov_clean for b in BKK_VICINITY_PROVINCES)

        loc_display = re.sub(r"\s+", " ", loc_raw).replace("จ.", "• ").strip()
        cat = normalize_category(raw_cat, raw_title)

        # Extract floor count if mentioned in title
        m_fl = re.search(r"(\d+)\s*ชั้น", raw_title)
        if usable_str == "-" and m_fl:
            usable_str = f"อาคาร {m_fl.group(1)} ชั้น"

        if not gallery:
            gallery = ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=600"]

        title = f"{raw_title} ({loc_raw}) รหัส {code}" if code not in raw_title else f"{raw_title} ({loc_raw})"

        desc_lines = [
            f"ชื่อทรัพย์ / โครงการ: {raw_title}",
            f"ประเภททรัพย์: {raw_cat}",
            f"ทำเลที่ตั้ง: {loc_raw}",
            f"เนื้อที่ดิน: {size_str}",
        ]
        if usable_str != "-":
            desc_lines.append(f"พื้นที่ใช้สอย: {usable_str}")

        specs_obj = {
            "project_name": raw_title,
            "address_full": loc_raw,
        }

        zone_kw = map_zone_keywords(loc_raw, raw_title)
        search_kw = f"ALPHA อัลฟ่า กรุงไทย {code} {raw_title} {loc_raw} {raw_cat} {zone_kw}".strip()

        prop = {
            "id": f"ALPHA-{code}",
            "code": code,
            "slug": slug,
            "title": title,
            "category": cat,
            "bank_source": "KTB" if MERGE_ALPHA_INTO_KTB else "ALPHA",
            "sub_source": "ALPHA",
            "province": prov_clean,
            "is_bkk_vicinity": is_bkk,
            "price": price_str,
            "size": size_str,
            "usable_area": usable_str,
            "bedrooms": "-",
            "bathrooms": "-",
            "location": loc_display or prov_clean,
            "status": "New",
            "main_image": gallery[0],
            "gallery": gallery,
            "description": sanitize_no_phone_or_contact("\n".join(desc_lines)),
            "specs": specs_obj,
            "search_keywords": search_kw,
        }
        if lat and lng:
            prop["lat"] = lat
            prop["lng"] = lng
        items.append(prop)
    return items


def fetch_alpha_archive_page(p):
    url = "https://alphacapamc.com/property/" if p == 1 else f"https://alphacapamc.com/property/page/{p}/"
    req = urllib.request.Request(url, headers=HEADERS_HTML)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
            html_text = r.read().decode("utf-8", errors="ignore")
        return parse_alpha_cards_from_html(html_text)
    except Exception:
        return []


def enrich_alpha_bkk_detail(prop):
    """Fetch detail page for BKK & Vicinity Alpha properties to grab full gallery + deed number."""
    slug = prop.get("slug")
    if not slug:
        return prop
    url = f"https://alphacapamc.com/property/{slug}/"
    req = urllib.request.Request(url, headers=HEADERS_HTML)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            html_text = r.read().decode("utf-8", errors="ignore")
        main_part = html_text.split("ทรัพย์อื่นๆที่น่าสนใจ")[0]

        # Extract all 1200x800 or full-res gallery images from main section
        imgs = re.findall(
            r'https://alphacapamc\.com/wp-content/uploads/[^"\'\s>]+?\.(?:jpg|jpeg|png|webp)',
            main_part,
            flags=re.I,
        )
        by_base = {}
        order = []
        for u in imgs:
            if any(skip in u for skip in ("Share-Alpha-cap", "site-logo", "footer-bg", "-300x", "-150x", "-600x", "-768x", "img-7_compressed")):
                continue
            base = re.sub(r"-\d+x\d+(?=\.[a-z]+$)", "", u, flags=re.I)
            if base not in by_base:
                by_base[base] = u
                order.append(base)
            elif "1200x" in u:
                by_base[base] = u
        full_gallery = [by_base[b] for b in order]
        if full_gallery:
            prop["gallery"] = full_gallery
            prop["main_image"] = full_gallery[0]

        # Extract deed_no and extra detail text
        clean_txt = re.sub(r"<[^>]+>", "\n", main_part)
        m_deed = re.search(r"เอกสารสิทธิ์\s*:\s*\n*\s*([^\n\r]+)", clean_txt)
        if m_deed:
            deed_val = re.sub(r"\s+", " ", m_deed.group(1)).strip()
            if deed_val:
                prop["specs"]["deed_no"] = deed_val

        m_desc = re.search(r"รายละเอียดทรัพย์\s*:\s*\n*\s*([^\n\r]+)", clean_txt)
        if m_desc:
            d_val = sanitize_no_phone_or_contact(re.sub(r"\s+", " ", m_desc.group(1)).strip())
            if d_val and d_val not in prop["description"]:
                prop["description"] += f"\nจุดเด่น / การเดินทาง: {d_val}"
    except Exception:
        pass
    return prop


def crawl_all_alpha():
    print("[ALPHA] Scanning archive pages 1..148 in parallel...")
    all_alpha = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        futures = {ex.submit(fetch_alpha_archive_page, p): p for p in range(1, 148)}
        for fut in as_completed(futures):
            for item in fut.result():
                all_alpha[item["id"]] = item

    props = list(all_alpha.values())
    bkk_props = [p for p in props if p["is_bkk_vicinity"]]
    print(f"[ALPHA] Found {len(props)} total properties (BKK & Vicinity: {len(bkk_props)})")

    print(f"[ALPHA] Enriching deep gallery & deed specs for {len(bkk_props)} BKK & Vicinity properties...")
    with ThreadPoolExecutor(max_workers=20) as ex:
        list(ex.map(enrich_alpha_bkk_detail, bkk_props))

    # Remove temporary slug field
    for p in props:
        p.pop("slug", None)
    return props


def main():
    ktb_all = crawl_all_ktb()
    alpha_all = crawl_all_alpha()

    # 1. Save full nationwide master files in data/
    ktb_master_path = os.path.join(DATA_DIR, "ktb_property_master.json")
    alpha_master_path = os.path.join(DATA_DIR, "alpha_property_master.json")
    with open(ktb_master_path, "w", encoding="utf-8") as f:
        json.dump(ktb_all, f, ensure_ascii=False, indent=2)
    with open(alpha_master_path, "w", encoding="utf-8") as f:
        json.dump(alpha_all, f, ensure_ascii=False, indent=2)
    print(f"[SAVED] Master files: KTB ({len(ktb_all)}), ALPHA ({len(alpha_all)})")

    # 2. Filter for active website dataset (BKK & Vicinity 6 provinces per ONLY_BKK_AND_VICINITY)
    ktb_active = [p for p in ktb_all if (p["is_bkk_vicinity"] or not ONLY_BKK_AND_VICINITY)]
    alpha_active = [p for p in alpha_all if (p["is_bkk_vicinity"] or not ONLY_BKK_AND_VICINITY)]

    # 3. Merge into siwasup_all_properties.json & .js
    main_json_path = os.path.join(ROOT_DIR, "siwasup_all_properties.json")
    main_js_path = os.path.join(ROOT_DIR, "siwasup_all_properties.js")
    with open(main_json_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    # Remove any previous KTB or ALPHA records before appending fresh ones
    base_props = [
        p for p in existing if str(p.get("bank_source", "")).upper() not in ("KTB", "ALPHA")
    ]
    merged = base_props + ktb_active + alpha_active

    with open(main_json_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, separators=(",", ":"))

    js_payload = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    js_content = (
        f"const ALL_PROPERTIES_DATA = {js_payload};\n"
        f"window.SIWASUP_ALL_PROPERTIES = ALL_PROPERTIES_DATA;\n"
        f"window.SIWASUP_PROPERTIES = ALL_PROPERTIES_DATA;\n"
    )
    with open(main_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(
        f"[MERGED] Base: {len(base_props)} + KTB (BKK): {len(ktb_active)} + ALPHA (BKK): {len(alpha_active)} = Total: {len(merged)} properties!"
    )


if __name__ == "__main__":
    main()
