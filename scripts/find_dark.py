with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", encoding="utf-8") as f:
    text = f.read()

import re
neutrals = set(re.findall(r'bg-neutral-[89]00|text-neutral-[89]00|border-neutral-[89]00|bg-black|bg-gray-[89]00', text))
print("Dark classes found in index.html:", neutrals)
