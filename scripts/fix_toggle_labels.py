import os
import re

for path in [
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\catalog.html",
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html"
]:
    with open(path, "r", encoding="utf-8") as f:
        t = f.read()
    
    t = re.sub(r'(id="toggle-btn-img-\$\{p\.id\}"[^>]*>[\s\S]*?<span>)[\s\S]*?(</span>)', r'\g<1>รูป\g<2>', t)
    t = re.sub(r'(id="toggle-btn-map-\$\{p\.id\}"[^>]*>[\s\S]*?<span>)[\s\S]*?(</span>)', r'\g<1>แผนที่\g<2>', t)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(t)
    print("Fixed labels for:", path)
