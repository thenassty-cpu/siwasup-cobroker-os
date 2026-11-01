import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
url = 'https://www.bam.co.th/v2/_next/static/chunks/3695-8f515b908cba6363.js'
js = urllib.request.urlopen(url, context=ctx).read().decode('utf-8', errors='ignore')

idx = js.find('(1110)')
if idx != -1:
    print(js[idx-50:idx+300])
