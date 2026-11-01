import urllib.request
import ssl
import re
import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'th-TH,th;q=0.9,en;q=0.8'
}

print("[*] Probing BAM Search page: https://www.bam.co.th/th/search ...")
try:
    req = urllib.request.Request('https://www.bam.co.th/th/search', headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
        raw = r.read()
        try:
            html = raw.decode('tis-620')
        except Exception:
            html = raw.decode('utf-8', errors='ignore')
        
        print(f"[OK] BAM /th/search loaded: {len(html)} chars")
        # Look for API calls, fetch, axios, or ajax in HTML
        apis = re.findall(r'[\'"](/api/[^\'"]+|https?://[^\'"]+/api/[^\'"]+)[\'"]', html)
        scripts = re.findall(r'src=[\'"]([^\'"]+\.js[^\'"]*)[\'"]', html)
        forms = re.findall(r'<form[^>]*action=[\'"]([^\'"]*)[\'"]', html)
        
        print(f"APIs found in page: {len(apis)}")
        for a in apis[:10]:
            print("  API:", a)
            
        print(f"Forms found: {forms}")
        
        print("Scripts on search page:")
        for s in scripts:
            if any(k in s.lower() for k in ['search', 'property', 'main', 'app', 'bundle']):
                print("  Script:", s)
except Exception as e:
    print(f"[ERR] Error: {e}")
