import urllib.request, ssl, json

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json, text/plain, */*',
    'x-lang': 'th'
}

req = urllib.request.Request('https://bam-bo-api-prd.bam.co.th/api/v2/master-data/provinces', headers=headers)
data = json.loads(urllib.request.urlopen(req, context=ctx).read().decode('utf-8'))
print("Provinces response:", type(data['data']), list(data['data'].keys()) if isinstance(data['data'], dict) else len(data['data']))
if isinstance(data['data'], dict):
    for k, v in list(data['data'].items())[:3]:
        print(f"  {k}: {v}")
