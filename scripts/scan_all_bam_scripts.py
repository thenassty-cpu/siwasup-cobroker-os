import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}

html = urllib.request.urlopen('https://www.bam.co.th/th/search', context=ctx).read().decode('utf-8', errors='ignore')
scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html)

print(f"Scanning {len(scripts)} scripts for API endpoints...")
found_endpoints = set()

for s in scripts:
    url = f"https://www.bam.co.th{s}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            js = r.read().decode('utf-8', errors='ignore')
            # Look for api paths
            matches = re.findall(r'["\'](/api/[^"\']+|https?://bam-[^"\']+)["\']', js)
            for m in matches:
                found_endpoints.add(m)
            # Also look for axios/fetch templates like `...${...}...`
            template_matches = re.findall(r'`([^`]*(?:search|propert|asset)[^`]*)`', js)
            for tm in template_matches:
                if '/' in tm and len(tm) < 100:
                    found_endpoints.add(tm)
    except Exception as e:
        pass

print("Discovered Endpoints/Templates:")
for ep in sorted(found_endpoints):
    print("  *", ep)
