import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
url = 'https://www.jjpropertythai.com/_nuxt/D-bi_m07.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

idx = js.find('_encrypted')
if idx != -1:
    print("Found _encrypted in D-bi_m07.js:")
    start = max(0, idx - 150)
    end = min(len(js), idx + 350)
    print(js[start:end])
else:
    print("_encrypted not found in this chunk. Searching for crypto, aes, decrypt...")
    matches = re.findall(r'(\w*decrypt\w*|\w*crypto\w*|\w*aes\w*)', js, re.IGNORECASE)
    print("Crypto keywords found:", set(matches[:20]))
