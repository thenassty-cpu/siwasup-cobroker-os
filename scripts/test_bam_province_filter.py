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

candidates = [
    {"province_id": "10"},
    {"provinceId": "10"},
    {"provinceCode": "10"},
    {"provinceCodes": ["10"]},
    {"province_ids": ["10"]},
    {"provinceIds": ["10"]},
    {"locations": [{"provinceId": "10"}]},
    {"locations": [{"province_id": "10"}]}
]

for c in candidates:
    payload = {"page": 1, "pageSize": 5, **c}
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            d = json.loads(r.read().decode('utf-8'))
            print(f"Candidate {c} -> Matched: {d['data']['total']}")
    except Exception as e:
        print(f"Candidate {c} -> Error: {e}")
