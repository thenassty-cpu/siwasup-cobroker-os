import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
url = 'https://www.jjpropertythai.com/_nuxt/D-bi_m07.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

idx = js.find('async function E4(')
if idx != -1:
    print("Function E4 & context before/after:")
    start = max(0, idx - 400)
    end = min(len(js), idx + 1000)
    print(js[start:end])
