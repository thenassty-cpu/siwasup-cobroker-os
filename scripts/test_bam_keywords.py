import urllib.request, ssl, json

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-lang': 'th',
    'Origin': 'https://www.bam.co.th',
    'Referer': 'https://www.bam.co.th/th/search'
}

url = "https://bam-bo-api-prd.bam.co.th/api/v3/properties/search/list"

tests = [
    {"keyword": "บ้านเดี่ยว", "page": 1, "pageSize": 5},
    {"keyword": "ทาวน์เฮ้าส์", "page": 1, "pageSize": 5},
    {"keyword": "คอนโด", "page": 1, "pageSize": 5},
    {"keyword": "ที่ดิน", "page": 1, "pageSize": 5},
    {"keyword": "กรุงเทพ", "page": 1, "pageSize": 5},
    {"keyword": "นนทบุรี", "page": 1, "pageSize": 5},
    {"keyword": "ปทุมธานี", "page": 1, "pageSize": 5},
    {"minPrice": 1000000, "maxPrice": 3000000, "page": 1, "pageSize": 5}
]

for t in tests:
    req = urllib.request.Request(url, data=json.dumps(t).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            d = json.loads(r.read().decode('utf-8'))
            print(f"Query {t.get('keyword') or t} -> Total: {d['data']['total']}")
    except Exception as e:
        print(f"Query {t} -> Error: {e}")
