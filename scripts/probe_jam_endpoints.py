import urllib.request, ssl, json

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.jjpropertythai.com',
    'Referer': 'https://www.jjpropertythai.com/'
}

base = "https://api.jjpropertythai.com/baanbaan"
candidates = [
    "/v1/assets",
    "/v1/asset",
    "/v1/asset/search",
    "/v1/properties",
    "/v1/web/assets",
    "/v1/web/asset",
    "/v1/search",
    "/assets",
    "/asset",
    "/properties",
    "/search"
]

for c in candidates:
    url = base + c
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=6) as r:
            print(f"[STATUS {r.status}] {url}")
            body = r.read().decode('utf-8', errors='ignore')
            print("  Body:", body[:200])
    except urllib.error.HTTPError as he:
        print(f"[HTTP {he.code}] {url}")
    except Exception as e:
        print(f"[ERR] {url} -> {e}")
