import re

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Header Badge to enlarge Golden Emblem to 38px while keeping it compact & uncrowded
old_header_badge_pattern = r'<!-- Official Golden Emblem Badge.*?<div id="tierBadge"[^>]+>.*?</div>\s*</div>'

new_header_badge = '''<!-- Official Golden Emblem Badge (Enlarged 38px Medallion without crowding) -->
        <div id="tierBadge" class="flex items-center gap-2 pl-1 pr-2.5 py-1 rounded-full bg-linear-to-r from-[#F9E7B9] via-[#E5B54F] to-[#D4A034] border border-[#B3801D]/70 shadow-sm shrink-0">
          <!-- Big Circular Emblem (36px on mobile, 40px on tablet) -->
          <img id="tierEmblemImg" 
               src="assets/badges/Golden__001_lion_web.png" 
               alt="Golden Emblem" 
               class="w-9 h-9 sm:w-10 sm:h-10 object-contain rounded-full bg-slate-900 border border-black shadow-xs shrink-0" 
               onerror="this.onerror=null; this.src='assets/badges/Golden__001_lion.png';" />
          <div class="leading-tight text-left min-w-0 pr-1">
            <span id="tierTitleText" class="block text-[10px] sm:text-[11px] font-extrabold text-slate-950 tracking-tight truncate">Senior Property Advisor</span>
            <span id="tierSubText" class="block text-[8.5px] font-semibold text-amber-950/80 tracking-wide uppercase">Official Partner</span>
          </div>
        </div>
      </div>'''

html = re.sub(old_header_badge_pattern, new_header_badge, html, flags=re.DOTALL)

# 2. Update Verified Checkmark on Avatar to 28px (w-7 h-7) matching Illustrator
old_avatar_badge_pattern = r'<!-- Verified Badge.*?<span class="absolute[^>]+>.*?</span>'
new_avatar_badge = '''<!-- Verified Badge (Enlarged 28px Vector Match from Illustrator, Zero Crowding) -->
          <span class="absolute -bottom-1 -right-1 w-7 h-7 sm:w-7.5 sm:h-7.5 rounded-full bg-[#3fb354] border-[2.5px] border-white flex items-center justify-center shadow-xs" title="ที่ปรึกษาที่ผ่านการรับรอง">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </span>'''

html = re.sub(old_avatar_badge_pattern, new_avatar_badge, html, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: agent_profile.html updated with enlarged 38px Golden Emblem and 28px Verified Badge!")
