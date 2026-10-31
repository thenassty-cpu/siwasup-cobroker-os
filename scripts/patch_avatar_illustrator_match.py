import re

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update squircle-37 CSS to strict 37px
html = re.sub(
    r'\.squircle-37\s*\{[^}]+\}(\s*@media[^{]+\{[^}]+\})?',
    '''.squircle-37 {
      border-radius: 37px !important;
    }''',
    html
)

# 2. Update Verified Checkmark badge on main avatar
old_badge_pattern = r'<!-- Small Verified Checkmark -->\s*<span class="absolute[^>]+>.*?</span>'
new_badge = '''<!-- Verified Badge (Vector Match from Adobe Illustrator Corners: 37px) -->
          <span class="absolute -bottom-1 -right-1 w-6 h-6 sm:w-6.5 sm:h-6.5 rounded-full bg-[#3fb354] border-2 border-white flex items-center justify-center shadow-xs" title="ที่ปรึกษาที่ผ่านการรับรอง">
            <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </span>'''

html = re.sub(old_badge_pattern, new_badge, html, flags=re.DOTALL)

# 3. Update modal avatar in Preview Modal
old_modal_avatar_pattern = r'<img id="modalAvatar"[^>]+>'
new_modal_avatar = '''<div class="relative shrink-0">
            <img id="modalAvatar" src="" class="w-14 h-14 squircle-37 object-cover border border-slate-200 bg-white shrink-0" />
            <span class="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-[#3fb354] border border-white flex items-center justify-center shadow-2xs">
              <svg class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </span>
          </div>'''

html = re.sub(old_modal_avatar_pattern, new_modal_avatar, html)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: agent_profile.html updated with exact 37px squircle and Illustrator verified badge!")
