import sys

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\modals.js', 'r', encoding='utf-8') as f:
    txt = f.read()

# 1. Inspect offer-modal
idx1 = txt.find('id="offer-modal"')
print('=== 1. OFFER MODAL (first 2500 chars) ===')
print(txt[idx1:idx1+2500])

# 2. Inspect consign-modal
idx2 = txt.find('id="consign-modal"')
print('=== 2. CONSIGN MODAL (first 2500 chars) ===')
print(txt[idx2:idx2+2500])

# 3. Inspect mgm-modal
idx3 = txt.find('id="mgm-modal"')
print('=== 3. MGM MODAL (first 2500 chars) ===')
print(txt[idx3:idx3+2500])

# 4. Inspect npa-key-dispatch-modal
idx4 = txt.find('id="npa-key-dispatch-modal"')
print('=== 4. KEY MODAL (first 2500 chars) ===')
print(txt[idx4:idx4+2500])
