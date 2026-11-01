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
payload = {"page": 1, "pageSize": 100}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("Page 1 with pageSize 100:")
    print("Returned properties:", len(data['data']['properties']))
    print("Total in system:", data['data']['total'])
