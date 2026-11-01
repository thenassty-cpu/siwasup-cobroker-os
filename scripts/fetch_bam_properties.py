import urllib.request
import ssl
import json
import os
import sys
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATA_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
OUTPUT_FILE = os.path.join(DATA_DIR, "bam_properties_golden_zone.json")

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-lang': 'th',
    'Origin': 'https://www.bam.co.th',
    'Referer': 'https://www.bam.co.th/th/search'
}

url = "https://bam-bo-api-prd.bam.co.th/api/v3/properties/search/list"

# Golden Zone target keywords
TARGET_ZONES = ["กรุงเทพ", "นนทบุรี", "ปทุมธานี", "สมุทรปราการ"]

all_bam_properties = {}

print("=== STARTING BAM GOLDEN ZONE CRAWLER ===")

for zone in TARGET_ZONES:
    print(f"\n[*] Fetching zone: {zone}...")
    page = 1
    max_pages = 2  # Fetch top 100 per zone for initial high-value ingest
    
    while page <= max_pages:
        payload = {
            "keyword": zone,
            "page": page,
            "pageSize": 50
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                props = data.get('data', {}).get('properties', [])
                total_in_zone = data.get('data', {}).get('total', 0)
                
                print(f"  Page {page}/{max_pages}: Got {len(props)} properties (Total in zone: {total_in_zone})")
                
                for p in props:
                    pid = str(p.get('id') or p.get('marketCode'))
                    if pid and pid not in all_bam_properties:
                        # Extract price
                        real_price = None
                        for pr in p.get('prices', []):
                            if pr.get('amount'):
                                try:
                                    real_price = float(pr['amount'])
                                    break
                                except Exception:
                                    pass
                        
                        # Normalize to Siwasup Schema
                        normalized = {
                            "id": f"BAM-{pid}",
                            "source": "BAM",
                            "source_code": p.get('marketCode') or p.get('colNo'),
                            "title": p.get('projectName') or f"{p.get('propertyType')} {p.get('district') or ''}",
                            "property_type": p.get('propertyType') or "บ้าน",
                            "price": real_price or float(p.get('displayPrice', 0)),
                            "province": p.get('province'),
                            "district": p.get('city'),
                            "subdistrict": p.get('district'),
                            "latitude": float(p['latitude']) if p.get('latitude') else None,
                            "longitude": float(p['longitude']) if p.get('longitude') else None,
                            "bedrooms": p.get('bedroom'),
                            "bathrooms": p.get('bathroom'),
                            "area_sqw": p.get('wa'),
                            "area_sqm": p.get('areaMeter') or p.get('usabledArea'),
                            "images": p.get('images', []),
                            "renovation_status": p.get('renovationStatus'),
                            "is_shock_price": p.get('isShockPrice', False),
                            "commission_rate": "3.0%",
                            "url": f"https://www.bam.co.th/th/property/{p.get('marketCode')}"
                        }
                        all_bam_properties[normalized["id"]] = normalized
                
                if len(props) < 50:
                    break
                page += 1
                time.sleep(0.5)
        except Exception as e:
            print(f"  [ERR] Zone {zone} Page {page}: {e}")
            break

print(f"\n[OK] Finished BAM Golden Zone! Total unique properties extracted: {len(all_bam_properties)}")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(all_bam_properties, f, indent=2, ensure_ascii=False)

print(f"[SAVED] Saved to {OUTPUT_FILE}")
