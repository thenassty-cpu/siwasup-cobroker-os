import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data\homerun_all_properties_10k.json', encoding='utf-8') as f:
    props = json.load(f)

scb_bkk = [p for p in props if p.get('bank_pool') == 'SCB' and (p.get('province') or {}).get('nameEn') == 'Bangkok']
print('SCB BKK count:', len(scb_bkk))
for p in scb_bkk[:5]:
    print(json.dumps(p, ensure_ascii=False, indent=2))
