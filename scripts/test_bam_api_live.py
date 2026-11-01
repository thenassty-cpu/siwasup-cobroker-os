import urllib.request, ssl, json

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'x-lang': 'th',
    'Accept-Language': 'th-TH,th;q=0.9',
    'Origin': 'https://www.bam.co.th',
    'Referer': 'https://www.bam.co.th/th/search'
}

url = "https://bam-bo-api-prd.bam.co.th/api/v3/properties/search/list"
payload = {"page": 1, "pageSize": 5}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("TOTAL BAM PROPERTIES IN SYSTEM:", data['data']['total'])
    print("Page Size:", data['data']['pageSize'])
    p0 = data['data']['properties'][0]
    print("Keys of Property Object:", list(p0.keys()))
    print("ID:", p0.get('id'), "| MarketCode:", p0.get('marketCode'), "| ColNo:", p0.get('colNo'))
    print("Project:", p0.get('projectName'), "| Type:", p0.get('propertyType'))
    print("Coords:", p0.get('latitude'), p0.get('longitude'))
    print("Prices:", p0.get('prices'))
    print("Address/Location:", p0.get('address'), p0.get('location'), p0.get('province'))
    print("Images:", p0.get('images') or p0.get('thumbnail') or p0.get('coverImage'))
