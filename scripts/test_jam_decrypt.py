import urllib.request, ssl, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY = b"QWT9g38M6fwBzJcbCjRjIBqn97UBm1Cf"

ctx = ssl._create_unverified_context()
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'Origin': 'https://www.jjpropertythai.com',
    'Referer': 'https://www.jjpropertythai.com/'
}

url = "https://www.jjpropertythai.com/api/proxy/v1/assets"
req = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
    raw_json = json.loads(r.read().decode('utf-8'))
    enc_str = raw_json['_encrypted']
    parts = enc_str.split(':')
    
    iv = bytes.fromhex(parts[0])
    tag = bytes.fromhex(parts[1])
    ciphertext = bytes.fromhex(parts[2])
    
    # In AESGCM in python, ciphertext + tag is passed to decrypt(iv, data, associated_data=None)
    aesgcm = AESGCM(KEY)
    decrypted_bytes = aesgcm.decrypt(iv, ciphertext + tag, None)
    data = json.loads(decrypted_bytes.decode('utf-8'))
    
    print("[SUCCESS] Decrypted JAM Assets!")
    print("Response type:", type(data))
    if isinstance(data, dict):
        print("Keys:", list(data.keys()))
        items = data.get('data', data.get('assets', data.get('items', [])))
        print(f"Total items returned: {len(items) if isinstance(items, list) else items}")
        if isinstance(items, list) and items:
            p0 = items[0]
            print("Sample JAM Item 1:", json.dumps(p0, indent=2, ensure_ascii=False)[:400])
    elif isinstance(data, list):
        print("Items count:", len(data))
        if data:
            print("Sample JAM Item 1:", json.dumps(data[0], indent=2, ensure_ascii=False)[:400])
