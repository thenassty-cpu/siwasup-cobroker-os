import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen('https://www.jjpropertythai.com/Search', context=ctx).read().decode('utf-8', errors='ignore')

scripts = re.findall(r'src=["\']([^"\']*_nuxt[^"\']*)["\']', html)
print(f"Scripts on /Search: {len(scripts)}")
for s in scripts:
    print(" ", s)
