import re

with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\modals.js', 'r', encoding='utf-8') as f:
    txt = f.read()

for m in re.finditer(r'id=[\'"]([^\'"]*(?:mgm|referral|share|profile)[^\'"]*)[\'"]', txt, re.IGNORECASE):
    print(m.group(0), 'at', m.start())
