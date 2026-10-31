import urllib.request
import ssl
import re

ctx = ssl._create_unverified_context()
url = 'https://www.allabout-assets.com/product/1336545'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        raw = resp.read()
        for enc in ['utf-8', 'tis-620', 'cp874']:
            try:
                html = raw.decode(enc)
                title = re.search(r'<title>(.*?)</title>', html)
                if title and 'บ้าน' in title.group(1):
                    print(f"Decoded successfully with {enc}!")
                    print("Title:", title.group(1))
                    break
            except Exception:
                pass
except Exception as e:
    print(f"Error: {e}")
