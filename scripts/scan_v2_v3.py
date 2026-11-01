import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}

html = urllib.request.urlopen('https://www.bam.co.th/th/search', context=ctx).read().decode('utf-8', errors='ignore')
scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html)

all_v2_v3 = set()

for s in scripts:
    url = f"https://www.bam.co.th{s}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            js = r.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'["\'](/api/v[23]/[^"\']+)["\']', js)
            all_v2_v3.update(matches)
    except Exception:
        pass

print("ALL /api/v2 and /api/v3 routes:")
for m in sorted(all_v2_v3):
    print("  *", m)
