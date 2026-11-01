import urllib.request, ssl, json

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.jjpropertythai.com',
    'Referer': 'https://www.jjpropertythai.com/'
}

candidates = [
    "https://www.jjpropertythai.com/api/proxy/v1/web/assets",
    "https://www.jjpropertythai.com/api/proxy/v1/assets",
    "https://www.baanbaanproperty.com/api/proxy/v1/web/assets"
]

for url in candidates:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            print(f"[STATUS {r.status}] {url}")
            data = r.read().decode('utf-8', errors='ignore')
            print("  Body:", data[:300])
    except urllib.error.HTTPError as he:
        print(f"[HTTP {he.code}] {url}")
    except Exception as e:
        print(f"[ERR] {url} -> {e}")
