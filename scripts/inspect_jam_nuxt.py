import urllib.request, ssl, re, json

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen('https://www.jjpropertythai.com', context=ctx).read().decode('utf-8', errors='ignore')

m = re.search(r'<script id="__NUXT_DATA__"[^>]*>(.*?)</script>', html)
if m:
    print("Found __NUXT_DATA__!")
    raw = m.group(1)
    data = json.loads(raw)
    print(f"Nuxt data elements: {len(data)}")
    # Find property strings, prices, codes
    for idx, item in enumerate(data[:100]):
        if isinstance(item, str) and any(k in item for k in ['/product/', 'Baan', 'JAM', 'ราคา', 'บ้าน']):
            print(f"[{idx}] {item}")
else:
    print("No __NUXT_DATA__. Checking other scripts...")
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    print(f"Total inline scripts: {len(scripts)}")
    for i, s in enumerate(scripts):
        if 'window.' in s or 'json' in s.lower() or 'property' in s.lower():
            print(f"Script {i} length: {len(s)} | Preview: {s[:200]}")
