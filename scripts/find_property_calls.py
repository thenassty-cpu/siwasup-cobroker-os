import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}

html = urllib.request.urlopen('https://www.bam.co.th/th/search', context=ctx).read().decode('utf-8', errors='ignore')
scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html)

all_property_calls = set()

for s in scripts:
    url = f"https://www.bam.co.th{s}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            js = r.read().decode('utf-8', errors='ignore')
            # Look for properties endpoint
            matches = re.findall(r'([a-zA-Z0-9_\-\.\/]*properties[a-zA-Z0-9_\-\.\/\?=&]*)', js)
            for m in matches:
                if len(m) > 10 and ('api' in m or 'search' in m or '/' in m):
                    all_property_calls.add(m)
    except Exception:
        pass

print("Property occurrences:")
for p in sorted(all_property_calls)[:30]:
    print("  *", p)
