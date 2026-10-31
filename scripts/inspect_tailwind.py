with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", encoding="utf-8") as f:
    text = f.read()

import re
idx = text.find('tailwind.config')
if idx != -1:
    print(text[idx:idx+800])
else:
    print("tailwind.config not found inline, checking <style>")
    idx2 = text.find('<style>')
    print(text[idx2:idx2+600])
