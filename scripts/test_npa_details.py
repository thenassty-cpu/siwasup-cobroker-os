import json
import urllib.request
import ssl
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl._create_unverified_context()

with open('live_allabout_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

npa_ids = [pid for pid, data in products.items() if data['category'] == 'ทรัพย์ NPA']
print(f"Total NPA products in live crawl: {len(npa_ids)}")

# Test fetch first 5
for pid in npa_ids[:5]:
    url = f"https://www.allabout-assets.com/product/{pid}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            raw = resp.read()
            html = raw.decode('utf-8', errors='ignore')
            title = re.search(r'<title>(.*?)</title>', html)
            h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html)
            price = re.search(r'([\d,]+(?:\.\d+)?)\s*บาท', html)
            print(f"ID: {pid} | Title: {title.group(1).strip() if title else 'None'} | Price: {price.group(0) if price else 'None'}")
    except Exception as e:
        print(f"Error {pid}: {e}")
