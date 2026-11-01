import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen('https://www.jjpropertythai.com', context=ctx).read().decode('utf-8', errors='ignore')

# Find all scripts in _nuxt
nuxt_scripts = re.findall(r'src=["\']([^"\']*_nuxt[^"\']*)["\']', html)
print(f"Found {len(nuxt_scripts)} Nuxt scripts:")

jam_endpoints = set()

for s in nuxt_scripts:
    url = f"https://www.jjpropertythai.com{s}"
    try:
        js = urllib.request.urlopen(url, context=ctx, timeout=8).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'["\'](/[a-zA-Z0-9_\-\./]+)["\']', js)
        for m in matches:
            if any(k in m.lower() for k in ['property', 'asset', 'product', 'house', 'search', 'list', 'filter']):
                jam_endpoints.add(m)
    except Exception:
        pass

print("Discovered endpoints in JAM Nuxt scripts:")
for ep in sorted(jam_endpoints):
    print("  *", ep)
