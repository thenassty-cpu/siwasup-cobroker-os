import sys

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\crawler_dashboard.html', 'r', encoding='utf-8') as f:
    txt = f.read()

idx = 0
while True:
    idx = txt.find('actionItemsContainer', idx)
    if idx == -1: break
    print(f'Found actionItemsContainer at {idx}')
    print(txt[idx-50:idx+400])
    print('='*40)
    idx += len('actionItemsContainer')
