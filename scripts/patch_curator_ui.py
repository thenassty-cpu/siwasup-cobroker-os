import re

html_path = 'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/property_curator.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update script tag to load all_curation_properties.js
html = html.replace(
    '<script src="siwasup_all_properties.js"></script>',
    '<script src="all_curation_properties.js?v=20261029-full801"></script>\n  <script src="siwasup_all_properties.js?v=20261029-fallback"></script>'
)

# 2. Add visual Guidance Banners (Caption นำทาง) before or inside CONTROLS
guidance_banner_html = """
  <!-- 🧭 GUIDANCE CAPTIONS & ACTION LEGEND (แผงนำทางสำหรับบัว) -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-1 w-full">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5">
      
      <!-- Card 1: 🔴 8 แปลงทบทวนด่วน -->
      <div onclick="setGroupFilter('flagged_red')" class="cursor-pointer bg-gradient-to-br from-rose-50 to-red-50/60 border-2 border-rose-300 hover:border-rose-500 rounded-2xl p-3.5 shadow-sm hover:shadow-md transition-all group">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-rose-500 animate-ping"></span>
            <span class="font-bold text-rose-900 text-xs sm:text-sm">🔴 8 แปลงที่เว็บเดิมถอดออกแล้ว</span>
          </div>
          <span id="badge-count-red" class="bg-rose-500 text-white text-[11px] font-bold px-2 py-0.5 rounded-full">8</span>
        </div>
        <p class="text-[11px] text-rose-800 leading-relaxed mt-1">
          <strong>ช่วยเช็กด่วน:</strong> ทรัพย์ชุดนี้ไม่อยู่ในหน้าเว็บปัจจุบันแล้ว ถ้าหลังไหน<strong>ยังอยู่/ยังมีกุญแจ</strong> ให้กดหัวใจ ❤️ ดึงกลับมา ถ้าขายแล้วไม่ต้องเลือก
        </p>
        <div class="mt-2 text-[10px] text-rose-600 font-bold flex items-center gap-1 group-hover:translate-x-1 transition-transform">
          <span>คลิกเพื่อตรวจเช็ก 8 แปลงนี้</span>
          <i data-lucide="arrow-right" class="w-3 h-3"></i>
        </div>
      </div>

      <!-- Card 2: 🟢 12 แปลงของเข้าใหม่ -->
      <div onclick="setGroupFilter('new_green')" class="cursor-pointer bg-gradient-to-br from-emerald-50 to-teal-50/60 border-2 border-emerald-300 hover:border-emerald-500 rounded-2xl p-3.5 shadow-sm hover:shadow-md transition-all group">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            <span class="font-bold text-emerald-950 text-xs sm:text-sm">🟢 12 แปลงของเข้าใหม่ล่าสุด</span>
          </div>
          <span id="badge-count-green" class="bg-emerald-600 text-white text-[11px] font-bold px-2 py-0.5 rounded-full">12</span>
        </div>
        <p class="text-[11px] text-emerald-800 leading-relaxed mt-1">
          <strong>ของใหม่สดๆ:</strong> ทรัพย์ที่เพิ่งนำมาลงบนหน้าแรก allabout กดหัวใจ ❤️ เพื่อคัดเลือกเข้าพอร์ตเว็บใหม่ได้เลยครับ
        </p>
        <div class="mt-2 text-[10px] text-emerald-700 font-bold flex items-center gap-1 group-hover:translate-x-1 transition-transform">
          <span>คลิกเพื่อดูของเข้าใหม่</span>
          <i data-lucide="arrow-right" class="w-3 h-3"></i>
        </div>
      </div>

      <!-- Card 3: 💎 ทรัพย์เด่น NPA (671 แปลง) -->
      <div onclick="setGroupFilter('npa_vault')" class="cursor-pointer bg-gradient-to-br from-indigo-50 to-blue-50/60 border-2 border-indigo-200 hover:border-indigo-400 rounded-2xl p-3.5 shadow-sm hover:shadow-md transition-all group">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
            <span class="font-bold text-indigo-950 text-xs sm:text-sm">💎 ทรัพย์เด่น NPA ธนาคาร</span>
          </div>
          <span id="badge-count-npa" class="bg-indigo-600 text-white text-[11px] font-bold px-2 py-0.5 rounded-full">671</span>
        </div>
        <p class="text-[11px] text-indigo-800 leading-relaxed mt-1">
          <strong>คลัง NPA แบงก์:</strong> ทรัพย์ NPA ที่ทีมคัดไว้ เตรียมนำไปเช็กสต๊อกตรงกับธนาคารเพื่อดึงขึ้นเป็น Spotlight Hero
        </p>
        <div class="mt-2 text-[10px] text-indigo-700 font-bold flex items-center gap-1 group-hover:translate-x-1 transition-transform">
          <span>คลิกเปิดคลัง NPA (671 แปลง)</span>
          <i data-lucide="arrow-right" class="w-3 h-3"></i>
        </div>
      </div>

    </div>
  </section>
"""

# Insert guidance banner right above CONTROLS & FILTER BAR
if '<!-- CONTROLS & FILTER BAR -->' in html:
    html = html.replace('<!-- CONTROLS & FILTER BAR -->', guidance_banner_html + '\n  <!-- CONTROLS & FILTER BAR -->')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Guidance captions injected into property_curator.html successfully.")
