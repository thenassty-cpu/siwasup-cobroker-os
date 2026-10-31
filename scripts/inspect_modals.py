import re

with open('C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/modals.js', 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r'<div[^>]*id="([^"]+)"[^>]*>'
for m in re.finditer(pattern, c):
    tag = m.group(0)
    if 'modal-backdrop' in tag:
        is_hidden = 'hidden' in tag
        print(f"ID: {m.group(1)} | Hidden: {is_hidden}")
