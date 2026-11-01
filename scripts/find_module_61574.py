import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}

html = urllib.request.urlopen('https://www.bam.co.th/th/search', context=ctx).read().decode('utf-8', errors='ignore')
scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html)

for s in scripts:
    url = f"https://www.bam.co.th{s}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            js = r.read().decode('utf-8', errors='ignore')
            if '61574:' in js:
                print(f"[FOUND 61574] in {s}")
                idx = js.find('61574:')
                print(js[idx:idx+400])
    except Exception:
        pass
