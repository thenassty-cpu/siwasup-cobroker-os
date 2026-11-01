import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.bam.co.th/v2/_next/static/chunks/1110-fa7108d2177031fe.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

# Look for 61574 definition or Hm
idx = js.find('61574:')
if idx != -1:
    print("Found 61574 in current chunk:")
    print(js[idx:idx+500])
else:
    print("61574 not in this chunk. Searching for .Hm or v3:")
    matches = re.findall(r'(\w+\.Hm[^;]{1,100})', js)
    for m in matches:
        print("  ->", m)
