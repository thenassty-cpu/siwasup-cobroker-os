import urllib.request
import ssl
import re
import json

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://www.bam.co.th/v2/_next/static/chunks/app/%5Blocale%5D/(common)/search/page-99b0005933752ea0.js', headers=headers)
with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
    code = r.read().decode('utf-8', errors='ignore')
    print(f"JS Length: {len(code)}")
    # Find all API endpoints, URLs, or fetch calls
    matches = re.findall(r'["\'](/api/[^"\']+|https?://[^"\']+)["\']', code)
    print("Found matching strings:")
    for m in set(matches):
        if any(w in m.lower() for w in ['property', 'asset', 'search', 'bam', 'graphql', 'npa']):
            print("  ->", m)
