import re

with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", encoding="utf-8") as f:
    text = f.read()

print("File size:", len(text))
sections = re.findall(r'<section[^>]*id="([^"]+)"', text)
print("Sections:", sections)

# Check color palette used in index.html
colors = set(re.findall(r'#[0-9a-fA-F]{6}', text))
print("Sample hex colors:", list(colors)[:20])
