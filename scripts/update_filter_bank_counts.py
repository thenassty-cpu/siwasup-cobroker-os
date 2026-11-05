import os
import re

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")

new_options = """                      <option value="all">ทุกสถาบัน / เจ้าของ (3,161 หลัง)</option>
                      <option value="PAMCO">PAMCO (1,312 หลัง)</option>
                      <option value="SAM">SAM (581 หลัง)</option>
                      <option value="SCB">SCB (568 หลัง)</option>
                      <option value="Siwasup">ศิวาทรัพย์ รีโนเวท (280 หลัง)</option>
                      <option value="TTB">TTB (267 หลัง)</option>
                      <option value="GSB">GSB (153 หลัง)</option>"""

for p in [CATALOG_PATH, INDEX_PATH]:
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace options inside select id="filter-bank"
    content = re.sub(
        r'(<select\s+id="filter-bank"[^>]*>)\s*[\s\S]*?(</select>)',
        r'\g<1>\n' + new_options + r'\n                    \g<2>',
        content
    )

    # Bump cache buster
    content = re.sub(r'v=20261106-\d+', 'v=20261106-0145', content)

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Updated filter-bank and cache buster in {p}")

# Bump sw.js
SW_PATH = os.path.join(REPO_DIR, "sw.js")
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw_c = f.read()
sw_c = re.sub(r"const CACHE_NAME = 'siwasup-os-v[^']+';", "const CACHE_NAME = 'siwasup-os-v20261106-0145';", sw_c)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw_c)
print("[OK] Bumped sw.js to v20261106-0145")
