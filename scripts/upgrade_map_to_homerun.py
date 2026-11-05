import os
import re

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")

def update_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Leaflet MarkerCluster CSS & JS if not present
    cluster_tags = """  <!-- Leaflet Map & MarkerCluster (Homerun Style) -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>"""

    # Replace existing leaflet include
    content = re.sub(r'<!-- Leaflet Map CSS & JS -->.*?<script src="https://unpkg\.com/leaflet@1\.9\.4/dist/leaflet\.js"></script>', cluster_tags, content, flags=re.DOTALL)

    # 2. Add Homerun Cluster CSS
    cluster_style = """
    /* Homerun Platform Cluster Badge Style */
    .homerun-cluster-wrap {
      background: transparent !important;
      border: none !important;
    }
    .homerun-cluster-pill {
      background: #FFFFFF;
      color: #0F172A;
      font-family: 'Prompt', -apple-system, sans-serif;
      font-weight: 700;
      font-size: 12px;
      padding: 6px 14px;
      border-radius: 9999px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16), 0 1px 3px rgba(0, 0, 0, 0.08);
      border: 1px solid rgba(0, 0, 0, 0.06);
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
      position: relative;
    }
    .homerun-cluster-pill:hover {
      transform: scale(1.08);
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.22);
      color: #ED1C24;
    }
    .homerun-cluster-pill::after {
      content: '';
      position: absolute;
      bottom: -5px;
      left: 50%;
      transform: translateX(-50%);
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-top: 5px solid #FFFFFF;
    }
    .leaflet-popup-content-wrapper {
      border-radius: 18px !important;
      padding: 4px !important;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.2) !important;
    }
    .leaflet-popup-content {
      margin: 8px !important;
      line-height: 1.4 !important;
    }
    """

    if "/* Homerun Platform Cluster Badge Style */" not in content:
        content = content.replace("</style>", cluster_style + "\n  </style>")

    # 3. Update single property location click & button to open Google Maps or single modal
    old_loc = '<span>${p.location || \'กรุงเทพฯ และปริมณฑล\'}</span>'
    new_loc = '<span class="hover:underline hover:text-rose-600 transition" onclick="event.stopPropagation(); openPropertyMapDirect(\'${p.id}\')" title="คลิกเปิดแผนที่/นำทาง">${p.location || \'กรุงเทพฯ และปริมณฑล\'} 📍</span>'
    content = content.replace(old_loc, new_loc)

    # 4. Replace Leaflet Map script and HTML container with Homerun UI
    old_map_container = """            <div id="siwasup-map-container" class="w-full h-[620px] rounded-2xl border border-neutral-200/90 shadow-sm relative overflow-hidden z-0"></div>"""
    new_map_container = """            <div class="relative w-full h-[620px] rounded-2xl border border-neutral-200/90 shadow-sm overflow-hidden z-0">
              <!-- Floating Filters Homerun Style (Left Top) -->
              <div class="absolute top-4 left-4 z-[400] flex flex-col gap-2">
                <button type="button" onclick="filterMapCategory('all')" id="map-btn-all" class="px-3.5 py-1.5 rounded-full bg-white text-neutral-800 hover:bg-neutral-50 shadow-md border border-neutral-200/80 flex items-center gap-1.5 text-xs font-bold transition active:scale-95">
                  <span class="w-2.5 h-2.5 rounded-full bg-rose-600"></span>
                  <span>ทั้งหมด</span>
                </button>
                <button type="button" onclick="filterMapCategory('horizontal')" id="map-btn-horizontal" class="px-3.5 py-1.5 rounded-full bg-white text-neutral-800 hover:bg-neutral-50 shadow-md border border-neutral-200/80 flex items-center gap-1.5 text-xs font-bold transition active:scale-95">
                  <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
                  <span>แนวราบ (บ้าน/ที่ดิน)</span>
                </button>
                <button type="button" onclick="filterMapCategory('vertical')" id="map-btn-vertical" class="px-3.5 py-1.5 rounded-full bg-white text-neutral-800 hover:bg-neutral-50 shadow-md border border-neutral-200/80 flex items-center gap-1.5 text-xs font-bold transition active:scale-95">
                  <span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                  <span>แนวสูง (คอนโด)</span>
                </button>
              </div>

              <!-- Map Container -->
              <div id="siwasup-map-container" class="w-full h-full"></div>
            </div>"""

    content = content.replace(old_map_container, new_map_container)

    # 5. Replace initOrUpdateLeafletMap implementation
    map_impl_pattern = re.compile(r'function initOrUpdateLeafletMap\(props\) \{.*?\n    \}', re.DOTALL)
    
    new_map_impl = """    let currentMapCatFilter = 'all'; // 'all' | 'horizontal' | 'vertical'
    let siwasupMarkerCluster = null;

    function filterMapCategory(cat) {
      currentMapCatFilter = cat;
      ['all', 'horizontal', 'vertical'].forEach(k => {
        const btn = document.getElementById(`map-btn-${k}`);
        if (btn) {
          if (k === cat) {
            btn.classList.add('ring-2', 'ring-rose-500', 'bg-rose-50');
          } else {
            btn.classList.remove('ring-2', 'ring-rose-500', 'bg-rose-50');
          }
        }
      });
      if (window.lastMapProperties) {
        initOrUpdateLeafletMap(window.lastMapProperties);
      }
    }

    function openPropertyMapDirect(propId) {
      const p = (window.allProperties || []).find(x => String(x.id) === String(propId));
      if (!p) return;
      const coords = getPropertyCoords(p);
      if (coords && coords.isExact) {
        window.open(`https://www.google.com/maps/search/?api=1&query=${coords.lat},${coords.lng}`, '_blank');
      } else {
        const q = encodeURIComponent(`${p.title || ''} ${p.location || ''} ${coords.district || ''}`);
        window.open(`https://www.google.com/maps/search/?api=1&query=${q}`, '_blank');
      }
    }

    function initOrUpdateLeafletMap(props) {
      window.lastMapProperties = props;
      setTimeout(() => {
        const mapDiv = document.getElementById('siwasup-map-container');
        if (!mapDiv) return;

        if (siwasupLeafletMap) {
          siwasupLeafletMap.remove();
          siwasupLeafletMap = null;
          siwasupMarkerCluster = null;
        }

        // Center on Thailand
        siwasupLeafletMap = L.map('siwasup-map-container', {
          zoomControl: true,
          attributionControl: false
        }).setView([13.7563, 100.5018], 8);

        // High Quality Map Tiles without Watermark (Esri World Street Map)
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
          maxZoom: 19
        }).addTo(siwasupLeafletMap);

        // Homerun-style Cluster Group
        siwasupMarkerCluster = L.markerClusterGroup({
          maxClusterRadius: 75,
          spiderfyOnMaxZoom: true,
          showCoverageOnHover: false,
          zoomToBoundsOnClick: true,
          iconCreateFunction: function(cluster) {
            const count = cluster.getChildCount();
            const countLabel = count >= 1000 ? '999+ ตำแหน่ง' : `${count.toLocaleString()} ตำแหน่ง`;
            return L.divIcon({
              html: `<div class="homerun-cluster-pill"><span>${countLabel}</span></div>`,
              className: 'homerun-cluster-wrap',
              iconSize: [100, 36],
              iconAnchor: [50, 36]
            });
          }
        });

        const bounds = [];
        let exactCount = 0;
        let approxCount = 0;

        // Apply Category Filter (horizontal vs vertical)
        const filteredProps = props.filter(p => {
          if (currentMapCatFilter === 'all') return true;
          const cat = (p.category || '').toLowerCase();
          const isCondo = cat.includes('คอนโด') || cat.includes('condo');
          if (currentMapCatFilter === 'vertical') return isCondo;
          if (currentMapCatFilter === 'horizontal') return !isCondo;
          return true;
        });

        filteredProps.forEach(p => {
          const coords = getPropertyCoords(p);
          if (!coords) return;
          bounds.push([coords.lat, coords.lng]);

          if (coords.isExact) exactCount++;
          else approxCount++;

          const markerColor = coords.isExact ? '#ED1C24' : '#F59E0B';
          const pinHtml = `
            <div style="background-color: ${markerColor}; width: 28px; height: 28px; border-radius: 50%; border: 2.5px solid #FFFFFF; box-shadow: 0 4px 12px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: #FFF; font-size: 13px; font-weight: bold;">
              ${coords.isExact ? '📍' : '⭕'}
            </div>
          `;
          const customIcon = L.divIcon({
            html: pinHtml,
            className: 'custom-siwasup-pin',
            iconSize: [28, 28],
            iconAnchor: [14, 14],
            popupAnchor: [0, -14]
          });

          const pTitle = (p.title || p.name || 'ทรัพย์พร้อมอยู่').replace(/'/g, '');
          const pPrice = p.price ? (typeof p.price === 'number' ? p.price.toLocaleString() + ' บาท' : p.price) : 'ติดต่อสอบถาม';
          const pImg = p.main_image || p.thumbnail || 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400';
          const badgeText = coords.isExact ? '📍 พิกัดตรงเป๊ะ' : `⭕ โซน${coords.district || 'โดยประมาณ'}`;

          const popupContent = `
            <div style="font-family: 'Prompt', sans-serif; width: 230px; padding: 4px;">
              <img src="${pImg}" style="width: 100%; height: 115px; object-fit: cover; border-radius: 12px; margin-bottom: 8px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-size: 10px; padding: 2px 7px; border-radius: 6px; background-color: ${coords.isExact ? '#FEF2F2' : '#FFFBEB'}; color: ${coords.isExact ? '#DC2626' : '#D97706'}; font-weight: bold;">
                  ${badgeText}
                </span>
                <span style="font-size: 11px; font-weight: 700; color: #0F172A;">${p.category || 'บ้าน'}</span>
              </div>
              <h4 style="font-size: 12px; font-weight: bold; color: #1E293B; margin: 0 0 4px 0; line-height: 1.35; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                ${pTitle}
              </h4>
              <div style="font-size: 15px; font-weight: 800; color: #ED1C24; margin-bottom: 8px;">
                ${pPrice}
              </div>
              <div style="display: flex; gap: 4px;">
                <button onclick="openPropertyDetailModal('${p.id}')" style="flex: 1; background: #0F172A; color: white; border: none; border-radius: 8px; padding: 7px 0; font-size: 11px; font-weight: bold; cursor: pointer;">
                  ดูรายละเอียด ➔
                </button>
                <button onclick="openPropertyMapDirect('${p.id}')" style="background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; border-radius: 8px; padding: 7px 10px; font-size: 11px; font-weight: bold; cursor: pointer;" title="เปิด Google Maps นำทาง">
                  นำทาง ↗
                </button>
              </div>
            </div>
          `;

          const m = L.marker([coords.lat, coords.lng], { icon: customIcon });
          m.bindPopup(popupContent);
          siwasupMarkerCluster.addLayer(m);
        });

        siwasupLeafletMap.addLayer(siwasupMarkerCluster);

        if (bounds.length > 0) {
          siwasupLeafletMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 13 });
        }

        const counterEl = document.getElementById('map-badge-counter');
        if (counterEl) {
          counterEl.innerText = `แสดง ${bounds.length.toLocaleString()} แปลง (${exactCount.toLocaleString()} GPS ตรง, ${approxCount.toLocaleString()} โซนย่าน)`;
        }
      }, 100);
    }"""

    content = map_impl_pattern.sub(new_map_impl, content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Updated {file_path} to Homerun Map UI!")

update_file(CATALOG_PATH)
update_file(INDEX_PATH)
