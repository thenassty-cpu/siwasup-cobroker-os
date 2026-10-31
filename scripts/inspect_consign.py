import sys

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\modals.js', 'r', encoding='utf-8') as f:
    txt = f.read()

idx = txt.find('id="consign-modal"')
print(txt[idx:idx+3500])
