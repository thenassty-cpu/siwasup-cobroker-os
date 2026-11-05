import os
import re

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")
MODALS_PATH = os.path.join(REPO_DIR, "modals.js")

# 1. Update modals.js: Boost modal backdrops to z-[9999] so they are always on top
with open(MODALS_PATH, "r", encoding="utf-8") as f:
    modals_content = f.read()

# Replace fixed inset-0 z-50 or z-[100] with z-[9999]
modals_content = re.sub(r'class="([^"]*?)fixed inset-0 z-(?:50|\[100\]|\[110\])([^"]*?)"', r'class="\1fixed inset-0 z-[9999]\2"', modals_content)
modals_content = re.sub(r'class="([^"]*?)fixed inset-0 z-50([^"]*?)"', r'class="\1fixed inset-0 z-[9999]\2"', modals_content)

with open(MODALS_PATH, "w", encoding="utf-8") as f:
    f.write(modals_content)
print("[OK] Updated modals.js to z-[9999]!")

# 2. Update catalog.html and index.html
def isolate_cards(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Add 'isolate' to property-card container
    content = content.replace(
        'class="bg-white rounded-[22px] border ${isSelected ? \'border-[#C2A460] ring-2 ring-[#C2A460]\' : \'border-slate-200/80\'} shadow-xs hover:shadow-lg transition-all duration-300 overflow-hidden flex flex-col justify-between group relative"',
        'class="bg-white rounded-[22px] border ${isSelected ? \'border-[#C2A460] ring-2 ring-[#C2A460]\' : \'border-slate-200/80\'} shadow-xs hover:shadow-lg transition-all duration-300 overflow-hidden flex flex-col justify-between group relative isolate"'
    )

    # Lower card button z-indices from 1050/1060 down to 20/30 (since leaflet pane is 1)
    content = content.replace('z-[1050]', 'z-20')
    content = content.replace('z-[1060]', 'z-30')

    # Ensure CSS rules for Leaflet inside card
    css_fix = """
    /* Leaflet Z-Index Containment inside Cards */
    .card-mini-map-container .leaflet-pane {
      z-index: 1 !important;
    }
    .card-mini-map-container .leaflet-top,
    .card-mini-map-container .leaflet-bottom {
      z-index: 2 !important;
    }
    .card-mini-map-container .leaflet-tile-pane {
      z-index: 1 !important;
    }
    .card-mini-map-container .leaflet-marker-pane {
      z-index: 5 !important;
    }
    """
    if "/* Leaflet Z-Index Containment inside Cards */" not in content:
        content = content.replace("</style>", css_fix + "\n  </style>")

    # Bump cache buster
    content = re.sub(r'v=20261106-\d+', 'v=20261106-0200', content)
    content = re.sub(r'v=20261104-realscan', 'v=20261106-0200', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Isolated cards and fixed z-indexes in {file_path}")

isolate_cards(CATALOG_PATH)
isolate_cards(INDEX_PATH)

# Bump sw.js
SW_PATH = os.path.join(REPO_DIR, "sw.js")
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw_c = f.read()
sw_c = re.sub(r"const CACHE_NAME = 'siwasup-os-v[^']+';", "const CACHE_NAME = 'siwasup-os-v20261106-0200';", sw_c)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw_c)
print("[OK] Bumped sw.js to v20261106-0200")
