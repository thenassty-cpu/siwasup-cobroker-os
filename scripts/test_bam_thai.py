import urllib.request, ssl, json, sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'x-lang': 'th',
    'Accept-Language': 'th-TH,th;q=0.9',
    'Origin': 'https://www.bam.co.th',
    'Referer': 'https://www.bam.co.th/th/search'
}

url = "https://bam-bo-api-prd.bam.co.th/api/v3/properties/search/list"
payload = {"page": 1, "pageSize": 3}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
    raw = resp.read()
    data = json.loads(raw.decode('utf-8'))
    for p in data['data']['properties']:
        print(f"[{p.get('marketCode')}] {p.get('projectName')} | {p.get('propertyType')} | ราคา: {p.get('displayPrice'):,} บาท | {p.get('city')}, {p.get('province')}")
        print(f"  พิกัด: {p.get('latitude')}, {p.get('longitude')} | ภาพ: {len(p.get('images', []))} รูป")
