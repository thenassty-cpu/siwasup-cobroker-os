import json
import os
import sys

DATA_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
HOMERUN_FILE = os.path.join(DATA_DIR, "homerun_all_properties_10k.json")
GSB_FILE = os.path.join(DATA_DIR, "gsb_all_properties.json")
MANIFEST_FILE = os.path.join(DATA_DIR, "r2_assets_manifest.json")
SYNC_STATE_FILE = os.path.join(DATA_DIR, "r2_images_sync_state.json")
OUTPUT_JSON = os.path.join(DATA_DIR, "catalog_index.json")

with open(os.path.join(DATA_DIR, "provinces_clean.json"), "r", encoding="utf-8") as f:
    PROVINCE_MAP = json.load(f)

# Reverse mapping: Thai province -> English province
TH_TO_EN_PROVINCE = {th: en for en, th in PROVINCE_MAP.items()}

with open(os.path.join(DATA_DIR, "types_clean.json"), "r", encoding="utf-8") as f:
    TYPE_MAP = json.load(f)

def map_gsb_type(raw_type):
    t = raw_type or ""
    if any(k in t for k in ['คอนโด', 'ห้องชุด', 'อาคารชุด']):
        return 'CD', 'คอนโด'
    elif 'ทาวน์' in t:
        return 'TH', 'ทาวน์เฮ้าส์'
    elif 'ที่ดินเปล่า' in t or (t == 'ที่ดิน'):
        return 'LD', 'ที่ดินเปล่า'
    elif any(k in t for k in ['พาณิชย์', 'ตึกแถว']):
        return 'CH', 'อาคารพาณิชย์'
    elif 'บ้านแฝด' in t:
        return 'TWH', 'บ้านแฝด'
    elif 'บ้าน' in t or 'สิ่งปลูกสร้าง' in t:
        return 'SDH', 'บ้านเดี่ยว'
    return 'SDH', t or 'อสังหาริมทรัพย์'

def build_index():
    print("[*] Loading Homerun data...")
    with open(HOMERUN_FILE, 'r', encoding='utf-8') as f:
        props = json.load(f)

    manifest = {}
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

    sync_state = {}
    if os.path.exists(SYNC_STATE_FILE):
        with open(SYNC_STATE_FILE, 'r', encoding='utf-8') as f:
            sync_state = json.load(f)

    print(f"[*] Processing {len(props)} Homerun properties...")
    catalog = []
    
    for p in props:
        pid = p.get('id')
        code = p.get('code') or 'N/A'
        bank = p.get('bank_pool') or 'SCB'
        t_key = p.get('propertyTypeKey') or 'SDH'
        t_name = TYPE_MAP.get(t_key, 'อสังหาริมทรัพย์')
        
        prov_obj = p.get('province') or {}
        prov_en = prov_obj.get('nameEn') or 'Bangkok'
        prov_th = PROVINCE_MAP.get(prov_en, prov_en)
        
        dist_obj = p.get('district') or {}
        dist_en = dist_obj.get('nameEn') or ''
        
        price = p.get('price') or 0
        living = p.get('livingSpace') or 0
        land = p.get('landSpace') or 0
        bed = p.get('bedCount') or 0
        bath = p.get('bathCount') or 0

        # Thumbnail determination
        m_item = manifest.get(pid)
        sync_item = sync_state.get(pid)
        
        if m_item and m_item.get('thumbnail'):
            thumb = m_item['thumbnail']
            gallery_count = len(m_item.get('gallery', []))
        elif sync_item and sync_item.get('images_count', 0) > 0:
            thumb_ext = 'png' if bank == 'SCB' else 'jpg'
            thumb = f"https://assets.siwasup.com/{bank.lower()}/{pid}/thumb.{thumb_ext}"
            gallery_count = sync_item.get('images_count', 1)
        else:
            thumb = f"https://assets.siwasup.com/{bank.lower()}/{pid}/thumb.jpg"
            gallery_count = 0

        catalog.append({
            "id": pid,
            "c": code,
            "b": bank,
            "t": t_key,
            "tn": t_name,
            "p": prov_th,
            "pe": prov_en,
            "d": dist_en,
            "pr": int(price),
            "sqm": round(float(living), 1) if living else 0,
            "sqw": round(float(land), 1) if land else 0,
            "bed": int(bed) if bed else 0,
            "bath": int(bath) if bath else 0,
            "thumb": thumb,
            "gc": gallery_count
        })

    # Ingest GSB
    if os.path.exists(GSB_FILE):
        print("[*] Loading GSB (ธนาคารออมสิน) data...")
        with open(GSB_FILE, 'r', encoding='utf-8') as gf:
            gsb_items = json.load(gf)
        
        print(f"[*] Processing {len(gsb_items)} GSB properties...")
        for gp in gsb_items:
            gid = gp.get('id')
            gcode = gp.get('code') or gid
            bank = "GSB"
            raw_t = gp.get('type_name')
            t_key, t_name = map_gsb_type(raw_t)
            
            prov_th = gp.get('province') or "กรุงเทพมหานคร"
            prov_en = TH_TO_EN_PROVINCE.get(prov_th, prov_th)
            dist_th = gp.get('district') or ""
            
            price = gp.get('price') or gp.get('original_price') or 0
            living = gp.get('area_sqm') or 0
            
            # Area calculation
            rai = gp.get('area_rai') or 0
            ngan = gp.get('area_ngan') or 0
            wa = gp.get('area_sqw') or 0
            total_sqw = (rai * 400) + (ngan * 100) + wa
            
            thumb = gp.get('thumbnail_url') or ""
            
            catalog.append({
                "id": gid,
                "c": gcode,
                "b": bank,
                "t": t_key,
                "tn": t_name,
                "p": prov_th,
                "pe": prov_en,
                "d": dist_th,
                "pr": int(price),
                "sqm": round(float(living), 1) if living else 0,
                "sqw": round(float(total_sqw), 1) if total_sqw else 0,
                "bed": 0,
                "bath": 0,
                "thumb": thumb,
                "gc": 1 if thumb else 0
            })

    # Save compact json
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, separators=(',', ':'))

    size_mb = os.path.getsize(OUTPUT_JSON) / 1024 / 1024
    print(f"[OK] Generated {OUTPUT_JSON} with {len(catalog):,} properties ({size_mb:.2f} MB)")

if __name__ == "__main__":
    build_index()
