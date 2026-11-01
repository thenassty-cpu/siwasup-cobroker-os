import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen('https://www.bam.co.th/th/search', context=ctx).read().decode('utf-8', errors='ignore')

f_pushes = re.findall(r'self\.__next_f\.push\(\[1,\s*"(.*?)"\]\)', html)
all_text = "".join(f_pushes).replace('\\"', '"').replace('\\\\', '\\')

for m in re.finditer(r'propertyCode', all_text):
    start = max(0, m.start() - 100)
    end = min(len(all_text), m.end() + 250)
    print("--- PROPERTY CONTEXT ---")
    print(all_text[start:end])
