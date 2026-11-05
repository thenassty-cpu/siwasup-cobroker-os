import os
import re

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")

def apply_fresh_map_and_zindex_fix(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add CSS rules to control Leaflet z-index inside cards
    css_fix = """
    /* Leaflet Z-Index Containment inside Cards */
    .card-mini-map-container .leaflet-pane {
      z-index: 10 !important;
    }
    .card-mini-map-container .leaflet-top,
    .card-mini-map-container .leaflet-bottom {
      z-index: 20 !important;
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

    # 2. Fix Card Image Area: Ensure z-[1050] on category badge, share/heart buttons, and z-[1060] on media toggle
    old_card_area_pattern = re.compile(
        r'<!-- Image Area \(Homerun 4:3 Ratio with Toggle Map/Photo\) -->[\s\S]*?<!-- Bottom-Left: New Pill Badge',
        re.DOTALL
    )

    new_card_area = """<!-- Image Area (Homerun 4:3 Ratio with Toggle Map/Photo) -->
            <div class="relative aspect-[4/3] bg-slate-100 overflow-hidden" id="card-media-box-${p.id}">
              
              <!-- Layer 1: Image -->
              <div id="card-img-layer-${p.id}" class="w-full h-full relative cursor-pointer" onclick="openPropertyDetailModal('${p.id}')">
                <img src="${img}" alt="${safeTitleAttr}" 
                     onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600';"
                     class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ${isBooked || isTransferred ? 'contrast-105 opacity-85' : ''}">
              </div>

              <!-- Layer 2: Embedded Mini Map (Instant Flip in Card with Fresh Color) -->
              <div id="card-map-layer-${p.id}" class="w-full h-full hidden relative bg-slate-100 card-mini-map-container">
                <div id="card-mini-map-${p.id}" class="w-full h-full"></div>
                <button type="button" onclick="event.stopPropagation(); openPropertyMapDirect('${p.id}')" class="absolute bottom-2.5 right-2.5 z-[1050] bg-neutral-900/90 hover:bg-neutral-950 text-white text-[10px] font-bold px-2.5 py-1 rounded-full shadow-md flex items-center gap-1 transition active:scale-95 border border-white/20" title="เปิด Google Maps นำทางจริง">
                  <span>นำทาง Google Maps ↗</span>
                </button>
              </div>

              <!-- Top-Left: Category Badge (High Z-Index so it stays above map) -->
              <div class="absolute top-3 left-3 capsule-bokeh text-[11px] font-medium px-3 py-1 flex items-center gap-1.5 shadow-sm z-[1050] pointer-events-auto">
                <i data-lucide="${getCategoryIcon(p.category)}" class="w-3.5 h-3.5 stroke-[1.5]"></i>
                <span>${p.category || 'ทาวน์โฮม'}</span>
              </div>

              <!-- Top-Right: Glass Action Buttons (High Z-Index) -->
              <div class="absolute top-3 right-3 flex items-center gap-1.5 z-[1050] pointer-events-auto" onclick="event.stopPropagation()">
                <button onclick="openSmartShare('${p.id}', '${safeTitleAttr}')" class="w-8 h-8 rounded-full capsule-bokeh hover:bg-slate-900/60 flex items-center justify-center transition-all shadow-sm active:scale-90" title="แชร์">
                  <i data-lucide="share-2" class="w-3.5 h-3.5 stroke-[1.5]"></i>
                </button>
                <button onclick="toggleFavorite('${p.id}')" class="w-8 h-8 rounded-full ${isFav ? 'bg-rose-600 text-white border border-rose-400' : 'capsule-bokeh hover:bg-slate-900/60'} flex items-center justify-center transition-all shadow-sm active:scale-90" title="บันทึกที่ชอบ">
                  <i data-lucide="heart" class="w-3.5 h-3.5 ${isFav ? 'fill-white stroke-none' : 'stroke-[1.5]'}"></i>
                </button>
              </div>

              <!-- Floating Media Toggle [รูป | แผนที่] High Z-Index & Clickable Always -->
              <div class="absolute top-2.5 left-1/2 -translate-x-1/2 flex items-center bg-slate-900/75 backdrop-blur-md rounded-full p-0.5 border border-white/30 z-[1060] shadow-lg pointer-events-auto" onclick="event.stopPropagation()">
                <button type="button" id="toggle-btn-img-${p.id}" onclick="toggleCardMedia('${p.id}', 'img')" class="px-2.5 py-0.5 rounded-full text-[10px] font-bold text-slate-900 bg-white shadow-xs transition-all flex items-center gap-1 cursor-pointer">
                  <i data-lucide="image" class="w-3 h-3"></i>
                  <span>รูป</span>
                </button>
                <button type="button" id="toggle-btn-map-${p.id}" onclick="toggleCardMedia('${p.id}', 'map')" class="px-2.5 py-0.5 rounded-full text-[10px] font-medium text-white/90 hover:text-white transition-all flex items-center gap-1 cursor-pointer">
                  <i data-lucide="map-pin" class="w-3 h-3"></i>
                  <span>แผนที่</span>
                </button>
              </div>

              <!-- Bottom-Left: New Pill Badge"""

    content = old_card_area_pattern.sub(new_card_area, content)

    # 3. Replace Tile Layer with Fresh Google Maps Tiles in both big map and mini map
    # Old Esri tile url:
    esri_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    google_tile_snippet = """L.tileLayer('https://mt{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
          subdomains: ['0', '1', '2', '3'],
          maxZoom: 20
        })"""

    # In initOrUpdateLeafletMap
    content = content.replace(f"L.tileLayer('{esri_url}', {{\n          maxZoom: 19\n        }})", google_tile_snippet)
    content = content.replace(f"L.tileLayer('{esri_url}', {{\n              maxZoom: 19\n            }})", google_tile_snippet)

    # 4. Bump Cache Version
    content = re.sub(r'v=20261106-\d+', 'v=20261106-0155', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Applied Fresh Google Map & Z-Index Fix to {file_path}")

apply_fresh_map_and_zindex_fix(CATALOG_PATH)
apply_fresh_map_and_zindex_fix(INDEX_PATH)

# Bump sw.js
SW_PATH = os.path.join(REPO_DIR, "sw.js")
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw_c = f.read()
sw_c = re.sub(r"const CACHE_NAME = 'siwasup-os-v[^']+';", "const CACHE_NAME = 'siwasup-os-v20261106-0155';", sw_c)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw_c)
print("[OK] Bumped sw.js to v20261106-0155")
