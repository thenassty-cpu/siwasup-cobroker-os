import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen('https://www.jjpropertythai.com', context=ctx).read().decode('utf-8', errors='ignore')
print("HTML Length:", len(html))
print("First 1500 chars of HTML:")
print(html[:1500])
