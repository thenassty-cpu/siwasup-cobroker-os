import urllib.request, ssl, json

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

for test_filter in [
    {"keyword": "สายไหม", "page": 1, "pageSize": 5},
    {"provinces": ["กรุงเทพมหานคร"], "page": 1, "pageSize": 5},
    {"propertyTypes": ["บ้านเดี่ยว"], "page": 1, "pageSize": 5}
]:
    try:
        req = urllib.request.Request(url, data=json.dumps(test_filter).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f"Filter {test_filter} -> Total matched: {data['data']['total']}")
    except Exception as e:
        print(f"Filter {test_filter} -> Error: {e}")
