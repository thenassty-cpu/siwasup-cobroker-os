import os
import re

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")

def add_card_map_toggle(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Card Image Area to include Toggle and Map Layer
    old_image_area_regex = re.compile(
        r'<!-- Image Area \(Homerun 4:3 Ratio\) -->\s*<div class="relative aspect-\[4/3\] bg-slate-100 overflow-hidden cursor-pointer" onclick="openPropertyDetailModal\(\'\$\{p\.id\}\'\)">\s*<img src="\$\{img\}" alt="\$\{safeTitleAttr\}"\s*onerror="this\.onerror=null; this\.src=\'https://images\.unsplash\.com/photo-1600596542815-ffad4c1539a9\?w=600\';"\s*class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 \$\{isBooked \|\| isTransferred \? \'contrast-105 opacity-85\' : \'\'\}">',
        re.DOTALL
    )

    new_image_area = """<!-- Image Area (Homerun 4:3 Ratio with Toggle Map/Photo) -->
            <div class="relative aspect-[4/3] bg-slate-100 overflow-hidden" id="card-media-box-${p.id}">
              
              <!-- Layer 1: Image -->
              <div id="card-img-layer-${p.id}" class="w-full h-full relative cursor-pointer" onclick="openPropertyDetailModal('${p.id}')">
                <img src="${img}" alt="${safeTitleAttr}" 
                     onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600';"
                     class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ${isBooked || isTransferred ? 'contrast-105 opacity-85' : ''}">
              </div>

              <!-- Layer 2: Embedded Mini Map (Instant Flip in Card) -->
              <div id="card-map-layer-${p.id}" class="w-full h-full hidden relative bg-slate-200">
                <div id="card-mini-map-${p.id}" class="w-full h-full"></div>
                <button type="button" onclick="event.stopPropagation(); openPropertyMapDirect('${p.id}')" class="absolute bottom-2.5 right-2.5 z-[400] bg-neutral-900/90 hover:bg-neutral-950 text-white text-[10px] font-bold px-2.5 py-1 rounded-full shadow-md flex items-center gap-1 transition active:scale-95 border border-white/20" title="เปิด Google Maps นำทางจริง">
                  <span>นำทาง Google Maps ↗</span>
                </button>
              </div>

              <!-- Floating Media Toggle [รูป | แผนที่] Homerun Capsule Style -->
              <div class="absolute top-2.5 left-1/2 -translate-x-1/2 flex items-center bg-slate-900/65 backdrop-blur-md rounded-full p-0.5 border border-white/25 z-20 shadow-md" onclick="event.stopPropagation()">
                <button type="button" id="toggle-btn-img-${p.id}" onclick="toggleCardMedia('${p.id}', 'img')" class="px-2.5 py-0.5 rounded-full text-[10px] font-bold text-slate-900 bg-white shadow-xs transition-all flex items-center gap-1">
                  <i data-lucide="image" class="w-3 h-3"></i>
                  <span>รูป</span>
                </button>
                <button type="button" id="toggle-btn-map-${p.id}" onclick="toggleCardMedia('${p.id}', 'map')" class="px-2.5 py-0.5 rounded-full text-[10px] font-medium text-white/90 hover:text-white transition-all flex items-center gap-1">
                  <i data-lucide="map-pin" class="w-3 h-3"></i>
                  <span>แผนที่</span>
                </button>
              </div>"""

    content = old_image_area_regex.sub(new_image_area, content)

    # 2. Add toggleCardMedia javascript logic
    toggle_script = """
    // ==========================================
    // IN-CARD TOGGLE: PHOTO vs MINI MAP
    // ==========================================
    const activeMiniMaps = {};

    function toggleCardMedia(propId, mode) {
      const imgLayer = document.getElementById(`card-img-layer-${propId}`);
      const mapLayer = document.getElementById(`card-map-layer-${propId}`);
      const btnImg = document.getElementById(`toggle-btn-img-${propId}`);
      const btnMap = document.getElementById(`toggle-btn-map-${propId}`);

      if (!imgLayer || !mapLayer || !btnImg || !btnMap) return;

      if (mode === 'map') {
        imgLayer.classList.add('hidden');
        mapLayer.classList.remove('hidden');

        btnMap.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold text-slate-900 bg-white shadow-xs transition-all flex items-center gap-1";
        btnImg.className = "px-2.5 py-0.5 rounded-full text-[10px] font-medium text-white/90 hover:text-white transition-all flex items-center gap-1";

        // Initialize Mini Leaflet Map if not already created
        if (!activeMiniMaps[propId]) {
          const p = (window.allProperties || []).find(x => String(x.id) === String(propId));
          if (p && typeof getPropertyCoords === 'function') {
            const coords = getPropertyCoords(p);
            const zoomLevel = coords.isExact ? 15 : 13;
            
            const miniMap = L.map(`card-mini-map-${propId}`, {
              zoomControl: false,
              attributionControl: false
            }).setView([coords.lat, coords.lng], zoomLevel);

            L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
              maxZoom: 19
            }).addTo(miniMap);

            const pinColor = coords.isExact ? '#ED1C24' : '#F59E0B';
            const miniPinIcon = L.divIcon({
              html: `<div style="background-color: ${pinColor}; width: 24px; height: 24px; border-radius: 50%; border: 2.5px solid #FFFFFF; box-shadow: 0 3px 10px rgba(0,0,0,0.35); display: flex; align-items: center; justify-content: center; color: #FFF; font-size: 11px; font-weight: bold;">${coords.isExact ? '📍' : '⭕'}</div>`,
              className: 'custom-siwasup-mini-pin',
              iconSize: [24, 24],
              iconAnchor: [12, 12]
            });

            L.marker([coords.lat, coords.lng], { icon: miniPinIcon }).addTo(miniMap);
            activeMiniMaps[propId] = miniMap;
          }
        }

        setTimeout(() => {
          if (activeMiniMaps[propId]) {
            activeMiniMaps[propId].invalidateSize();
          }
        }, 60);

      } else {
        mapLayer.classList.add('hidden');
        imgLayer.classList.remove('hidden');

        btnImg.className = "px-2.5 py-0.5 rounded-full text-[10px] font-bold text-slate-900 bg-white shadow-xs transition-all flex items-center gap-1";
        btnMap.className = "px-2.5 py-0.5 rounded-full text-[10px] font-medium text-white/90 hover:text-white transition-all flex items-center gap-1";
      }

      if (window.lucide) { lucide.createIcons(); }
    }
    """

    if "function toggleCardMedia" not in content:
        content = content.replace("</script>\n\n</body>", toggle_script + "\n  </script>\n\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Added In-Card Map/Photo Toggle to {file_path}")

add_card_map_toggle(CATALOG_PATH)
add_card_map_toggle(INDEX_PATH)
