import urllib.request, ssl, json

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.bam.co.th/th/search'
}

endpoints = [
    'https://bam-els-sync-api-prd.bam.co.th/api/properties/search',
    'https://bam-els-sync-api-prd.bam.co.th/properties/search',
    'https://bam-els-sync-api-prd.bam.co.th/search',
    'https://bam-els-sync-api-prd.bam.co.th/api/search',
    'https://bam-bo-api-prd.bam.co.th/api/properties',
    'https://bam-bo-api-prd.bam.co.th/api/search',
    'https://www.bam.co.th/api/search',
    'https://www.bam.co.th/api/properties'
]

for ep in endpoints:
    try:
        req = urllib.request.Request(ep, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=6) as r:
            print(f"[OK] {ep} -> Status: {r.status}")
            data = r.read()[:200]
            print("  Body:", data)
    except urllib.error.HTTPError as he:
        print(f"[HTTP {he.code}] {ep}")
    except Exception as e:
        print(f"[ERR] {ep} -> {e}")
