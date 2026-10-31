import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines[180:320]):
    print(f"{i+180}: {l}", end="")
