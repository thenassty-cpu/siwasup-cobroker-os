import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
url = 'https://www.bam.co.th/v2/_next/static/chunks/1110-fa7108d2177031fe.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

for m in re.finditer(r'\bp\.Yf\b', js):
    start = max(0, m.start() - 250)
    end = min(len(js), m.end() + 350)
    print("--- p.Yf USAGE ---")
    print(js[start:end])
