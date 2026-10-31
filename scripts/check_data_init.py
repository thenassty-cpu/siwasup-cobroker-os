import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", encoding="utf-8") as f:
    text = f.read()

idx = text.find("ALL_PROPERTIES_DATA")
while idx != -1:
    print("=== Match at", idx, "===")
    print(text[max(0, idx-150):idx+600])
    idx = text.find("ALL_PROPERTIES_DATA", idx+1)
