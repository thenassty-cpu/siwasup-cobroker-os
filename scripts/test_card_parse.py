import urllib.request
import ssl
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl._create_unverified_context()

url = "https://www.allabout-assets.com/category/260664?page=1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    raw = resp.read()
    html = raw.decode('utf-8', errors='ignore')

# Check structure of a product card
# Look for blocks containing /product/
cards = re.findall(r'<div[^>]*class=["\'][^"\']*product-item[^"\']*["\'][^>]*>([\s\S]*?)</div>\s*</div>', html)
print(f"Product item blocks found: {len(cards)}")
if not cards:
    # Alternative match
    items = re.findall(r'(<a[^>]*href=["\'][^"\']*/product/(\d+)["\'][^>]*>[\s\S]*?</a>[\s\S]*?(?:บาท|฿))', html)
    print(f"Alternative product blocks: {len(items)}")
    if items:
        print("Sample block 1:", items[0][0][:400])
