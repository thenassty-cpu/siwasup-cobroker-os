import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.jjpropertythai.com/_nuxt/D-bi_m07.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

print("Script length:", len(js))
# Look for /api or /baanbaan or fetch/axios
calls = re.findall(r'["\']([^"\']*(?:baanbaan|asset|product|search|house)[^"\']*)["\']', js)
for c in set(calls):
    if len(c) < 100:
        print("Call/String:", c)
