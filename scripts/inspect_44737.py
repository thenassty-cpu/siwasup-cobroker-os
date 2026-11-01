import urllib.request, ssl

ctx = ssl._create_unverified_context()
url = 'https://www.bam.co.th/v2/_next/static/chunks/1110-fa7108d2177031fe.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

idx = js.find('44737:')
if idx != -1:
    print(js[idx:idx+1200])
