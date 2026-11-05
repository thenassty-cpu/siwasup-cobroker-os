import os

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")

for p in [CATALOG_PATH, INDEX_PATH]:
    with open(p, "rb") as f:
        data = f.read()
    text = data.decode("utf-8", errors="ignore")
    text = text.replace("<span>ٻ</span>", "<span>รูป</span>")
    text = text.replace("<span>Ἱ</span>", "<span>แผนที่</span>")
    text = text.replace("<span></span>", "<span>แชร์</span>")
    with open(p, "wb") as f:
        f.write(text.encode("utf-8"))
    print(f"[OK] Cleaned Thai characters in {p}")
