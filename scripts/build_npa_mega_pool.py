import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATA_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
OUTPUT_FILE = os.path.join(DATA_DIR, "npa_mega_pool.json")

mega_pool = {}

# 1. Ingest BAM
bam_file = os.path.join(DATA_DIR, "bam_properties_golden_zone.json")
if os.path.exists(bam_file):
    with open(bam_file, 'r', encoding='utf-8') as f:
        bam_data = json.load(f)
        mega_pool.update(bam_data)
        print(f"[+] Loaded {len(bam_data)} BAM properties")

# 2. Ingest JAM
jam_file = os.path.join(DATA_DIR, "jam_properties_golden_zone.json")
if os.path.exists(jam_file):
    with open(jam_file, 'r', encoding='utf-8') as f:
        jam_data = json.load(f)
        mega_pool.update(jam_data)
        print(f"[+] Loaded {len(jam_data)} JAM properties")

# 3. Ingest GHB
ghb_file = os.path.join(DATA_DIR, "ghb_all_properties.json")
if os.path.exists(ghb_file):
    with open(ghb_file, 'r', encoding='utf-8') as f:
        ghb_data = json.load(f)
        if isinstance(ghb_data, list):
            for idx, p in enumerate(ghb_data):
                pid = p.get('property_id') or str(idx)
                k = f"GHB-{pid}"
                mega_pool[k] = {
                    "id": k,
                    "source": "GHB (ธอส.)",
                    "source_code": pid,
                    "title": p.get('title') or f"บ้าน ธอส. {pid}",
                    "property_type": p.get('property_type') or "บ้าน",
                    "price": p.get('price', 0),
                    "province": p.get('province'),
                    "district": p.get('district'),
                    "area_sqw": p.get('area_sqw'),
                    "images": [p.get('image')] if p.get('image') else [],
                    "commission_rate": "3.0%",
                    "url": f"https://www.ghbhomecenter.com/property-{pid}"
                }
        elif isinstance(ghb_data, dict):
            for pid, p in ghb_data.items():
                k = f"GHB-{pid}"
                mega_pool[k] = {
                    "id": k,
                    "source": "GHB (ธอส.)",
                    "source_code": pid,
                    "title": p.get('title') or f"บ้าน ธอส. {pid}",
                    "property_type": p.get('property_type') or "บ้าน",
                    "price": p.get('price', 0),
                    "province": p.get('province'),
                    "district": p.get('district'),
                    "area_sqw": p.get('area_sqw'),
                    "images": [p.get('image')] if p.get('image') else [],
                    "commission_rate": "3.0%",
                    "url": f"https://www.ghbhomecenter.com/property-{pid}"
                }
        print(f"[+] Loaded GHB properties")

print(f"\n[OK] Mega Pool compiled: {len(mega_pool)} total NPA properties ready for Siwasup Co-Broker OS!")

# Save to data directory
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(mega_pool, f, indent=2, ensure_ascii=False)

print(f"[SAVED] Saved to {OUTPUT_FILE}")
