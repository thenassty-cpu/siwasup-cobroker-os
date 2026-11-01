import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.bam.co.th/v2/_next/static/chunks/app/%5Blocale%5D/(common)/search/page-99b0005933752ea0.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

# Look for payload structure or searchParams
matches = re.findall(r'(\{[^}]*(?:province|propertyType|minPrice|maxPrice|keyword)[^}]*\})', js)
for m in matches[:10]:
    print("Payload candidate:", m[:150])
