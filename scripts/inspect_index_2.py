with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", encoding="utf-8") as f:
    text = f.read()

import re
tags = re.findall(r'<div[^>]*class="([^"]+)"', text)
print("Total divs:", len(tags))

# Find the property grid or catalog container in index.html
matches = [t for t in tags if 'grid' in t or 'property' in t or 'card' in t]
print("Grid/Card classes:", matches[:10])

# Find script data sources
scripts = re.findall(r'<script[^>]*src="([^"]+)"', text)
print("External scripts:", scripts)

# Check inline script variables
vars_found = re.findall(r'const ([a-zA-Z0-9_]+) =|let ([a-zA-Z0-9_]+) =|var ([a-zA-Z0-9_]+) =', text)
print("Vars:", [v for t in vars_found for v in t if v][:25])
