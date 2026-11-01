import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
url = 'https://www.jjpropertythai.com/_nuxt/D-bi_m07.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

for m in re.finditer(r'apiBaseUrl', js):
    start = max(0, m.start() - 150)
    end = min(len(js), m.end() + 250)
    print("--- API BASE URL CONTEXT ---")
    print(js[start:end])
