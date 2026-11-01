import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.bam.co.th/v2/_next/static/chunks/app/%5Blocale%5D/(common)/search/page-99b0005933752ea0.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

# Look for Yf (which is searchList)
for m in re.finditer(r'\bYf\b', js):
    start = max(0, m.start() - 150)
    end = min(len(js), m.end() + 250)
    print("--- Yf CALL CONTEXT ---")
    print(js[start:end])
