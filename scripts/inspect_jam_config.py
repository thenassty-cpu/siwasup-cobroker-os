import urllib.request, ssl, re, json

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen('https://www.jjpropertythai.com', context=ctx).read().decode('utf-8', errors='ignore')

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for s in scripts:
    if 'apiBaseUrl' in s:
        print("=== CONFIG SCRIPT ===")
        print(s)
