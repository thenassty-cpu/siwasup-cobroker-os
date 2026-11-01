import urllib.request, ssl, re, json

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

url = 'https://www.jjpropertythai.com'
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        title = re.search(r'<title>(.*?)</title>', html)
        print(f"[OK] JJPropertyThai (JAM) loaded! Title: {title.group(1).strip() if title else 'No title'}")
        
        # Check for APIs or script endpoints
        apis = re.findall(r'["\'](/api/[^"\']+|https?://[^"\']+/api/[^"\']+)["\']', html)
        print(f"APIs found: {len(apis)}")
        for a in apis[:10]:
            print("  API:", a)
except Exception as e:
    print(f"[ERR] Error: {e}")
