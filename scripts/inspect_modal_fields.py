import sys

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\modals.js', 'r', encoding='utf-8') as f:
    txt = f.read()

# 1. Offer price input area
idx1 = txt.find('id="offer-price"')
if idx1 == -1: idx1 = txt.find('homerun-offer-form')
print('=== 1. OFFER FORM DETAILS ===')
print(txt[idx1:idx1+2000])

# 2. Key dispatch form fields
idx2 = txt.find('id="npa-tab-req"')
print('=== 2. KEY TAB REQ DETAILS ===')
print(txt[idx2:idx2+2500])

# 3. Consign modal details
idx3 = txt.find('id="consign-modal"')
print('=== 3. CONSIGN MODAL DETAILS ===')
print(txt[idx3:idx3+2500])
