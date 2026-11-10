# -*- coding: utf-8 -*-
import os
import sys
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
RAW_DIR = r"D:\Recycle_Bin_90Days\Siwasup_OS_Cleansing_20261101\02_Heavy_RawData"

PROPS_JSON_PATH = os.path.join(REPO_DIR, "siwasup_all_properties.json")
PROPS_JS_PATH = os.path.join(REPO_DIR, "siwasup_all_properties.js")
CAT_INDEX_PATH = os.path.join(REPO_DIR, "data", "catalog_index.json")
SYNC_STATE_PATH = os.path.join(REPO_DIR, "data", "r2_images_sync_state.json")
PAMCO_MASTER_PATH = os.path.join(REPO_DIR, "data", "pamco_property_master.json")

HOMERUN_10K_PATH = os.path.join(RAW_DIR, "homerun_all_properties_10k.json")
R2_MANIFEST_PATH = os.path.join(RAW_DIR, "r2_assets_manifest.json")
GSB_RAW_PATH = os.path.join(RAW_DIR, "gsb_all_properties.json")

JUNK_IMG_KEYWORDS = ['social-ig', 'social-tiktok', 'social-youtube', 'pinext', 'facebook', 'line-icon']

def is_valid_gallery_url(u):
    if not u or not isinstance(u, str):
        return False
    ul = u.strip().lower()
    if not ul.startswith('http'):
        return False
    for kw in JUNK_IMG_KEYWORDS:
        if kw in ul:
            return False
    return True

def parse_thai_content_specs(text):
    if not text:
        return {}
    specs = {}
    m_deed = re.search(r'(?:ประเภทเอกสารสิทธิ์\s*/\s*เลขที่|โฉนดที่ดิน)\s*[:：]\s*([^\n\r]+)', text)
    if m_deed:
        val = m_deed.group(1).strip()
        if not val.startswith('โฉนด'):
            val = f"โฉนดที่ดิน: {val}"
        specs['deed_no'] = val

    m_loc = re.search(r'ที่ตั้ง\s*[:：]\s*([^\n\r]+)', text)
    if m_loc:
        addr = m_loc.group(1).strip()
        specs['address_full'] = addr
        m_proj = re.search(r'(?:หมู่บ้าน/โครงการ|โครงการ|หมู่บ้าน)\s+(.+?)(?:\s+เลขที่|\s+ถนน|\s+ซอย|\s+แขวง|\s+ตำบล|$)', addr)
        if m_proj:
            specs['project_name'] = m_proj.group(1).strip()
        m_hno = re.search(r'เลขที่\s+([^\s]+)', addr)
        if m_hno:
            specs['house_no'] = m_hno.group(1).strip()
        m_rd = re.search(r'ถนน\s+([^\s]+)', addr)
        if m_rd and m_rd.group(1).strip() != '-':
            specs['street'] = m_rd.group(1).strip()

    if 'project_name' not in specs:
        m_proj2 = re.search(r'โครงการ\s+([^\n\r]+?)(?:\s+ตั้งอยู่|\s+เลขที่|\s+ถนน|\n|$)', text)
        if m_proj2 and len(m_proj2.group(1).strip()) < 60:
            specs['project_name'] = m_proj2.group(1).strip()

    m_dim = re.search(r'หน้ากว้างติดถนน\s*[:：]\s*([^\n\r]+)', text)
    if m_dim:
        specs['dimensions'] = m_dim.group(1).strip()

    m_fl = re.search(r'(?:ทาวน์เฮ้าส์|ทาวน์โฮม|บ้านเดี่ยว|บ้านแฝด|อาคารพาณิชย์|ตึกแถว)\s*(\d+\s*ชั้น)', text)
    if m_fl:
        specs['floors'] = m_fl.group(1).strip()

    m_fee = re.search(r'ค่าส่วนกลาง[^\n\r]*?ประมาณ\s*([\d,]+(?:\.\d+)?\s*บาท\s*/\s*(?:ปี|เดือน|ตร\.ว\.))', text)
    if m_fee:
        specs['common_fee'] = m_fee.group(1).strip()

    return specs

def main():
    print("[*] Loading datasets...")
    with open(PROPS_JSON_PATH, "r", encoding="utf-8") as f:
        props = json.load(f)

    cat_index = json.load(open(CAT_INDEX_PATH, "r", encoding="utf-8")) if os.path.exists(CAT_INDEX_PATH) else []
    sync_state = json.load(open(SYNC_STATE_PATH, "r", encoding="utf-8")) if os.path.exists(SYNC_STATE_PATH) else {}
    pamco_master = json.load(open(PAMCO_MASTER_PATH, "r", encoding="utf-8")) if os.path.exists(PAMCO_MASTER_PATH) else {}
    homerun_10k = json.load(open(HOMERUN_10K_PATH, "r", encoding="utf-8")) if os.path.exists(HOMERUN_10K_PATH) else []
    r2_manifest = json.load(open(R2_MANIFEST_PATH, "r", encoding="utf-8")) if os.path.exists(R2_MANIFEST_PATH) else {}
    gsb_raw = json.load(open(GSB_RAW_PATH, "r", encoding="utf-8")) if os.path.exists(GSB_RAW_PATH) else []

    # Build lookup maps
    hr_by_bank_code = {}
    hr_by_code = {}
    for h in homerun_10k:
        b = str(h.get("bank_pool") or h.get("sourceKey") or "").upper()
        c = str(h.get("code") or "").strip().upper()
        if b and c:
            hr_by_bank_code[(b, c)] = h
        if c:
            hr_by_code[c] = h

    cat_by_bank_code = {}
    for cx in cat_index:
        b = str(cx.get("b") or "").upper()
        c = str(cx.get("c") or "").strip().upper()
        if b and c:
            cat_by_bank_code[(b, c)] = cx

    sync_by_bank_code = {}
    for uuid, sv in sync_state.items():
        b = str(sv.get("pool") or "").upper()
        c = str(sv.get("code") or "").strip().upper()
        if b and c:
            sync_by_bank_code[(b, c)] = (uuid, sv)

    gsb_by_code = {}
    for gp in gsb_raw:
        c = str(gp.get("code") or "").strip().upper()
        gid = str(gp.get("id") or "").strip().upper()
        if c:
            gsb_by_code[c] = gp
        if gid:
            gsb_by_code[gid] = gp

    pamco_by_code = {}
    if isinstance(pamco_master, dict):
        for k, v in pamco_master.items():
            pamco_by_code[str(k).upper()] = v
            c = str(v.get("code") or "").strip().upper()
            if c:
                pamco_by_code[c] = v
                pamco_by_code[f"PAMCO_{c}"] = v
                pamco_by_code[f"PAMCO-{c}"] = v

    print(f"[*] Enriching {len(props)} properties...")
    fixed_uuid_count = 0
    pamco_enriched_count = 0
    gsb_enriched_count = 0
    hr_enriched_count = 0

    # First pass: local enrichment
    for idx, p in enumerate(props):
        bank = str(p.get("bank_source") or "").strip()
        bank_up = bank.upper()
        code = str(p.get("code") or p.get("id") or "").strip()
        code_up = code.upper()

        # 1. Clean existing gallery of junk social icons
        raw_gal = p.get("gallery") or []
        clean_gal = [g for g in raw_gal if is_valid_gallery_url(g)]

        # 2. Enrich PAMCO
        if bank_up == "PAMCO" or code_up.startswith("PAMCO_"):
            pm = pamco_by_code.get(code_up) or pamco_by_code.get(code_up.replace("PAMCO_", ""))
            if pm:
                pamco_enriched_count += 1
                thumb = pm.get("thumbnail")
                if thumb:
                    p["main_image"] = thumb
                    clean_gal = [thumb]
                else:
                    clean_gal = []

                sqw = pm.get("area_sqw")
                sqm = pm.get("usable_sqm")
                try:
                    if sqw and float(sqw) > 0:
                        p["size"] = f"{float(sqw):g} ตร.ว."
                except Exception:
                    pass
                try:
                    if sqm and float(sqm) > 0:
                        p["usable_area"] = f"{float(sqm):g} ตร.ม."
                except Exception:
                    pass

                prov = (pm.get("province") or "").strip()
                dist = (pm.get("district") or "").strip()
                subd = (pm.get("sub_district") or "").strip()
                loc_parts = [x for x in [subd, dist, prov] if x]
                if loc_parts:
                    p["location"] = " • ".join(loc_parts)

                hgroup = (pm.get("hgroup") or "").strip()
                houseid = (pm.get("houseid") or "").strip()
                landid = (pm.get("landid") or "").strip()
                street = (pm.get("street") or "").strip()
                soi = (pm.get("soi") or "").strip()
                tel_ao = (pm.get("telAO") or "").strip()

                if hgroup and hgroup != "-":
                    p["project_name"] = hgroup
                if houseid and houseid != "-":
                    p["house_no"] = houseid
                if landid and landid != "-":
                    p["deed_no"] = f"โฉนด {landid}" if not landid.startswith("โฉนด") else landid
                if street and street != "-":
                    p["street"] = f"{street} {soi}".strip() if (soi and soi != "-") else street

                # Build rich description for PAMCO
                desc_lines = [
                    f"รหัสทรัพย์ PAMCO: {pm.get('code') or code} | ประเภท: {p.get('category', 'อสังหาฯ')}"
                ]
                if hgroup and hgroup != "-":
                    desc_lines.append(f"โครงการ/หมู่บ้าน: {hgroup}")
                addr_bits = [b for b in [f"บ้านเลขที่ {houseid}" if houseid else "", f"ซอย{soi}" if soi else "", f"ถนน{street}" if street else "", subd, dist, prov] if b and b != "-"]
                if addr_bits:
                    desc_lines.append(f"ที่ตั้ง: {' '.join(addr_bits)}")
                if landid and landid != "-":
                    desc_lines.append(f"เอกสารสิทธิ์: {landid}")
                desc_lines.append(f"ขนาดที่ดิน: {p.get('size', '-')} | พื้นที่ใช้สอย: {p.get('usable_area', '-')}")
                desc_lines.append("ทรัพย์รอการขาย (NPA) คัดพิเศษจาก บริหารสินทรัพย์ พรอสเพอริตี้ (PAMCO) พร้อมประสานงานนัดชมและยื่นข้อเสนอได้ทันที")
                p["description"] = "\n".join(desc_lines)

        # 3. Enrich GSB
        elif bank_up == "GSB":
            gp = gsb_by_code.get(code_up)
            if gp:
                gsb_enriched_count += 1
                real_thumb = gp.get("thumbnail_url")
                if real_thumb and ("/sam/" in str(p.get("main_image") or "") or not p.get("main_image")):
                    p["main_image"] = real_thumb
                    clean_gal = [real_thumb]
                    fixed_uuid_count += 1
                elif real_thumb and not clean_gal:
                    clean_gal = [real_thumb]

                if gp.get("deed_info"):
                    p["deed_no"] = gp["deed_info"]
                if gp.get("detail_url"):
                    p["source_url"] = gp["detail_url"]
                    p["url"] = gp["detail_url"]
                if gp.get("area_raw"):
                    p["dimensions"] = gp["area_raw"]
                prov = gp.get("province") or ""
                dist = gp.get("district") or ""
                subd = gp.get("subdistrict") or ""
                if subd and dist and prov:
                    p["location"] = f"{subd} • {dist} • {prov}"
                if gp.get("title") and gp.get("title") != "-":
                    p["project_name"] = gp.get("title")

        # 4. Enrich SAM / SCB / TTB from Homerun 10k + R2 Manifest + Catalog Index
        elif bank_up in ("SAM", "SCB", "TTB"):
            hr = hr_by_bank_code.get((bank_up, code_up)) or hr_by_code.get(code_up)
            cx = cat_by_bank_code.get((bank_up, code_up))
            sync_pair = sync_by_bank_code.get((bank_up, code_up))

            uuid = None
            if hr:
                uuid = hr.get("id")
            elif cx:
                uuid = cx.get("id")
            elif sync_pair:
                uuid = sync_pair[0]

            if uuid:
                p["homerun_id"] = uuid
                hr_enriched_count += 1

                # Check manifest & sync state for R2 gallery
                m_entry = r2_manifest.get(uuid, {})
                s_entry = sync_state.get(uuid, {})

                ext = "png" if (bank_up == "SCB" and str(m_entry.get("thumbnail") or "").endswith(".png")) else "jpg"
                real_thumb = m_entry.get("thumbnail") or (cx.get("thumb") if cx else None) or f"https://assets.siwasup.com/{bank_up.lower()}/{uuid}/thumb.{ext}"

                if p.get("main_image") != real_thumb and uuid not in str(p.get("main_image") or ""):
                    fixed_uuid_count += 1
                    p["main_image"] = real_thumb

                # Build unique R2 gallery (skip gallery_0 because gallery_0 is identical to thumb!)
                m_gal = m_entry.get("gallery") or []
                gal_list = [p["main_image"]]
                for g_url in m_gal:
                    if not is_valid_gallery_url(g_url):
                        continue
                    if "/gallery_0." in g_url or g_url == p["main_image"]:
                        continue
                    if g_url not in gal_list:
                        gal_list.append(g_url)

                # If sync_state says images_count > 1 and m_gal wasn't populated, build from images_count
                img_cnt = s_entry.get("images_count", 0)
                if len(gal_list) == 1 and img_cnt > 1:
                    for g_i in range(1, img_cnt):
                        g_url = f"https://assets.siwasup.com/{bank_up.lower()}/{uuid}/gallery_{g_i}.{ext}"
                        if g_url not in gal_list:
                            gal_list.append(g_url)

                # Special extra uploaded images for 3A1421 (gallery_4 to gallery_8)
                if code_up == "3A1421" and uuid == "59d88c66-35b2-4834-9c45-ae3c9b5b6115":
                    for g_i in range(1, 9):
                        g_url = f"https://assets.siwasup.com/sam/{uuid}/gallery_{g_i}.jpg"
                        if g_url not in gal_list:
                            gal_list.append(g_url)

                clean_gal = gal_list

            if hr:
                bed = hr.get("bedCount") or 0
                bath = hr.get("bathCount") or 0
                if bed and int(bed) > 0:
                    p["bedrooms"] = int(bed)
                if bath and int(bath) > 0:
                    p["bathrooms"] = int(bath)

                land_sp = hr.get("landSpace") or 0
                liv_sp = hr.get("livingSpace") or 0
                if land_sp and float(land_sp) > 0:
                    p["size"] = f"{float(land_sp):g} ตร.ว."
                if liv_sp and float(liv_sp) > 0:
                    p["usable_area"] = f"{float(liv_sp):g} ตร.ม."

                if hr.get("ppsqw"):
                    p["ppsqw"] = int(hr["ppsqw"])
                if hr.get("ppsqm"):
                    p["ppsqm"] = int(hr["ppsqm"])

                if hr.get("lat") and hr.get("lng"):
                    p["latitude"] = hr["lat"]
                    p["longitude"] = hr["lng"]

                src_url = hr.get("sourceUrl") or ""
                if src_url:
                    src_url = src_url.replace("://sam.or.th", "://www.sam.or.th").replace("://npa.sam.or.th", "://www.sam.or.th")
                    p["source_url"] = src_url
                    p["url"] = src_url

                raw_t = (hr.get("title") or "").strip()
                if raw_t and not raw_t.startswith("รหัสทรัพย์") and raw_t != code:
                    p["project_name"] = raw_t

                subd_th = (hr.get("subdistrict") or {}).get("nameTh") or ""
                dist_th = (hr.get("district") or {}).get("nameTh") or ""
                dist_en = (hr.get("district") or {}).get("nameEn") or ""
                prov_th = (hr.get("province") or {}).get("nameTh") or ""
                if subd_th and dist_th and prov_th:
                    p["subdistrict_th"] = subd_th
                    p["district_th"] = dist_th
                    p["province_th"] = prov_th

            elif cx:
                if cx.get("bed") and int(cx["bed"]) > 0:
                    p["bedrooms"] = int(cx["bed"])
                if cx.get("bath") and int(cx["bath"]) > 0:
                    p["bathrooms"] = int(cx["bath"])

        # Deduplicate clean_gal while preserving order
        seen_g = set()
        final_gal = []
        if p.get("main_image") and is_valid_gallery_url(p.get("main_image")):
            final_gal.append(p["main_image"])
            seen_g.add(p["main_image"])
        for g in clean_gal:
            if g not in seen_g:
                final_gal.append(g)
                seen_g.add(g)

        p["gallery"] = final_gal
        p["gallery_count"] = len(final_gal)

    print(f"[+] Pass 1 Complete: Fixed UUIDs={fixed_uuid_count}, Homerun={hr_enriched_count}, PAMCO={pamco_enriched_count}, GSB={gsb_enriched_count}")

    # Pass 2: Fetch deep content from Homerun API for the top 80 Homerun properties (so first pages have full project name, deed_no, dimensions, common_fee, full_content baked in!)
    hr_targets = []
    for p in props:
        if p.get("homerun_id") and p.get("bank_source") in ("SAM", "SCB", "TTB"):
            hr_targets.append(p)
        if len(hr_targets) >= 80:
            break

    print(f"[*] Fetching deep Thai specs from Homerun API for top {len(hr_targets)} properties...")

    def fetch_deep(prop):
        pool_l = prop["bank_source"].lower()
        hid = prop["homerun_id"]
        url = f"https://homerun-platform-api-prod-645188686833.asia-southeast1.run.app/api/web/group-buy/{pool_l}/properties/{hid}?include=media"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=8) as r:
                if r.status == 200:
                    d = json.loads(r.read().decode("utf-8")).get("data", {})
                    return prop, d
        except Exception:
            pass
        return prop, None

    deep_ok = 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(fetch_deep, pt) for pt in hr_targets]
        for fut in as_completed(futs):
            prop, d = fut.result()
            if not d:
                continue
            content = (d.get("content") or "").strip()
            if content:
                deep_ok += 1
                prop["full_content"] = content
                parsed = parse_thai_content_specs(content)
                for k, v in parsed.items():
                    if v and not prop.get(k):
                        prop[k] = v
                if parsed.get("floors") and (not prop.get("usable_area") or prop.get("usable_area") in ("-", "- ตร.ม.")):
                    prop["usable_area"] = f"{prop.get('category', 'ทาวน์โฮม')} {parsed['floors']}"
                # Update description with real content summary
                prop["description"] = content

            # Also check if TTB/SCB/SAM has extra gallery URLs on Supabase CDN when local R2 only had 1-2 images
            api_gal = d.get("gallery") or []
            if len(prop.get("gallery", [])) < len(api_gal) and prop.get("code") != "3A1421":
                # Keep R2 images first, then append any extra from api_gal (index >= len(r2))
                cur_gal = list(prop.get("gallery", []))
                # Note: api_gal[0] corresponds to thumb.jpg, api_gal[1] to gallery_1.jpg, etc.
                for g_idx, g_obj in enumerate(api_gal):
                    if g_idx >= len(cur_gal):
                        gu = g_obj.get("url")
                        if gu and is_valid_gallery_url(gu) and gu not in cur_gal:
                            cur_gal.append(gu)
                prop["gallery"] = cur_gal
                prop["gallery_count"] = len(cur_gal)

    print(f"[+] Deep API specs fetched for {deep_ok}/{len(hr_targets)} top properties!")

    # Save JSON & JS
    print("[*] Writing siwasup_all_properties.json and siwasup_all_properties.js...")
    with open(PROPS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=2)

    json_compact = json.dumps(props, ensure_ascii=False)
    js_out = (
        f"window.ALL_PROPERTIES_DATA = {json_compact};\n"
        f"window.SIWASUP_PROPERTIES = window.ALL_PROPERTIES_DATA;\n"
        f"window.SIWASUP_ALL_PROPERTIES = window.ALL_PROPERTIES_DATA;\n"
    )
    with open(PROPS_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_out)

    print("[✓] Saved enriched property files successfully!")

if __name__ == "__main__":
    main()
