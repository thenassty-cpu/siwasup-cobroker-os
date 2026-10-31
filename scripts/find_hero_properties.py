import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data\catalog_index.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Filter sweet spot: 1.2M - 2.9M, TH/SDH/CD in BKK/Samut Prakan/Nonthaburi/Pathum Thani
candidates = []
for p in items:
    price = p.get('pr', 0)
    bank = p.get('b', '')
    prov = p.get('p', '')
    thumb = p.get('thumb', '')
    if 1200000 <= price <= 2900000 and any(k in prov for k in ['กรุงเทพ', 'สมุทรปราการ', 'นนทบุรี', 'ปทุมธานี']) and thumb:
        candidates.append(p)

print(f"Total sweet spot candidates: {len(candidates)}")

by_bank = {}
for p in candidates:
    b = p.get('b')
    if b not in by_bank:
        by_bank[b] = []
    if len(by_bank[b]) < 2:
        by_bank[b].append(p)

print("\n--- HERO PROPERTIES (TOP PICKS FOR AGENT TESTING) ---")
for b in ['SCB', 'GSB', 'SAM', 'TTB']:
    plist = by_bank.get(b, [])
    print(f"\n【 แบงก์ {b} 】")
    for p in plist:
        print(f"• รหัส {p['c']} | {p['tn']} | {p['p']} ({p['d']}) | ฿{p['pr']:,} | รูป: {p['thumb']}")
