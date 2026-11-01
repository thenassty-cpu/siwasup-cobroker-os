import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen('https://www.jjpropertythai.com', context=ctx).read().decode('utf-8', errors='ignore')

scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html)
print(f"Total scripts on JAM portal: {len(scripts)}")

jam_apis = set()
for s in scripts:
    url = s if s.startswith('http') else f"https://www.jjpropertythai.com{s}"
    try:
        r = urllib.request.urlopen(url, context=ctx, timeout=8)
        js = r.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'["\'](/api/proxy/[^"\']+)["\']', js)
        jam_apis.update(matches)
        # Also look for property paths
        prop_matches = re.findall(r'["\']([^"\']*(?:property|asset|product)[^"\']*)["\']', js)
        for pm in prop_matches:
            if '/v1/' in pm or 'proxy' in pm:
                jam_apis.add(pm)
    except Exception:
        pass

print("Discovered JAM APIs:")
for a in sorted(jam_apis):
    print("  *", a)
