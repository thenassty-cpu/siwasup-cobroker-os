with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", encoding="utf-8") as f:
    text = f.read()

import re
idx = text.find('function renderProperties')
if idx == -1:
    idx = text.find('render')
print(text[idx:idx+1000])
