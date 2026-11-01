import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen('https://www.bam.co.th/th/search', context=ctx).read().decode('utf-8', errors='ignore')

# Find all script src
scripts = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html)
print(f"Total scripts on /th/search: {len(scripts)}")
for s in scripts:
    print(" ", s)
