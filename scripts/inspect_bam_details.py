import re
import urllib.request, ssl

ctx = ssl._create_unverified_context()
r = urllib.request.urlopen('https://www.bam.co.th/v2/_next/static/chunks/app/%5Blocale%5D/(common)/search/page-99b0005933752ea0.js', context=ctx)
code = r.read().decode('utf-8', errors='ignore')

# Search for service calls
matches = re.findall(r'(\w+\(\s*["\'](?:els|bam|amc|web-cms)["\']\)[^;]{1,150})', code)
for m in matches:
    print("Call:", m)

# Search for url paths like /api/v1 or /search or /property
urls = re.findall(r'["\'](/[^"\']+)["\']', code)
for u in set(urls):
    if any(k in u for k in ['search', 'property', 'asset', 'estate']):
        print("URL found:", u)
