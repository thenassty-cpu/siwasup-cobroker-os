# -*- coding: utf-8 -*-
"""
Cross-match Allabout 671 Blue Ribbon NPA properties with 15,117 Bank Master properties.
Matching strategies:
1. Exact Price match + Location/Project keyword match
2. Project name regex extraction + Price proximity
"""
import json
import re

with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\all_curation_properties.json', 'r', encoding='utf-8') as f:
    allabout_props = json.load(f)

with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data\catalog_index.json', 'r', encoding='utf-8') as f:
    bank_props = json.load(f)

print(f"Loaded {len(allabout_props)} Allabout items and {len(bank_props)} Bank items.")

# Index bank items by rounded price and bank
# Bank items have: 'c' (code), 'b' (bank), 'tn' (type name), 'pr' (price), 'thumb'
price_bank_map = {}
for bp in bank_props:
    pr = int(bp.get('pr', 0))
    if pr > 0:
        if pr not in price_bank_map:
            price_bank_map[pr] = []
        price_bank_map[pr].append(bp)

print(f"Indexed {len(price_bank_map)} unique price points in Bank Vault.")

npa_allabout = [p for p in allabout_props if p.get('ribbon') == 'blue']
print(f"Total Allabout NPA (Blue Ribbon) to audit: {len(npa_allabout)}")

exact_price_matches = 0
found_details = []

for ap in npa_allabout:
    pr_str = ap.get('price', '')
    pr_digits = re.sub(r'[^\d.]', '', pr_str)
    try:
        pr_val = int(float(pr_digits))
    except:
        pr_val = 0

    title = ap.get('title', '')
    
    # Check exact price matches
    candidates = price_bank_map.get(pr_val, [])
    if candidates:
        exact_price_matches += 1
        found_details.append({
            'allabout_id': ap.get('id'),
            'allabout_title': title,
            'price': pr_val,
            'candidates_count': len(candidates),
            'bank_matched': candidates[0].get('b'),
            'bank_code': candidates[0].get('c')
        })

print(f"\n--- MATCH AUDIT PREVIEW ---")
print(f"Exact Price Matches found: {exact_price_matches} / {len(npa_allabout)} ({exact_price_matches/len(npa_allabout)*100:.1f}%)")
print(f"First 5 matched samples:")
for item in found_details[:5]:
    print(f"  • [{item['bank_matched']}] Code: {item['bank_code']} | Price: {item['price']:,} THB | Title: {item['allabout_title'][:40]}")
