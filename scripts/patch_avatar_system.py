import re

# ==========================================
# 1. PATCH agent_profile.html
# ==========================================
profile_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(profile_path, "r", encoding="utf-8") as f:
    p_content = f.read()

# Replace avatar wrapper to be clickable with camera icon overlay & text button
old_avatar_block = '''        <!-- Avatar Wrapper with 37px Rounded Corners -->
        <div class="relative shrink-0">
          <img id="agentAvatar"
               src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80"
               alt="Agent Profile"
               class="w-[86px] h-[86px] sm:w-24 sm:h-24 squircle-37 object-cover bg-slate-100 border border-slate-200 shadow-sm">
          <!-- Verified Badge (Enlarged 28px Vector Match from Illustrator, Zero Crowding) -->
          <span class="absolute -bottom-1 -right-1 w-7 h-7 sm:w-7.5 sm:h-7.5 rounded-full bg-[#3fb351] flex items-center justify-center border-2 border-white shadow-sm">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </span>
        </div>'''

new_avatar_block = '''        <!-- Avatar Wrapper with 37px Rounded Corners (Clickable to Upload Anywhere) -->
        <label for="customPhotoInput" class="relative shrink-0 cursor-pointer group block" title="แตะเพื่อเปลี่ยนรูปโปรไฟล์">
          <img id="agentAvatar"
               src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80"
               alt="Agent Profile"
               class="w-[86px] h-[86px] sm:w-24 sm:h-24 squircle-37 object-cover bg-slate-100 border-2 border-amber-400/80 shadow-md transition group-hover:scale-[1.02] group-hover:brightness-95">
          <!-- Camera Overlay Badge on Avatar -->
          <span class="absolute -bottom-1 -left-1 w-7 h-7 sm:w-7.5 sm:h-7.5 rounded-full bg-slate-900 text-white flex items-center justify-center border-2 border-white shadow-md transition group-hover:scale-110 group-hover:bg-amber-500">
            <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
              <circle cx="12" cy="13" r="4"></circle>
            </svg>
          </span>
          <!-- Verified Badge -->
          <span class="absolute -bottom-1 -right-1 w-7 h-7 sm:w-7.5 sm:h-7.5 rounded-full bg-[#3fb351] flex items-center justify-center border-2 border-white shadow-sm">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </span>
        </label>'''

p_content_norm = p_content.replace("\r\n", "\n")
old_av_norm = old_avatar_block.replace("\r\n", "\n")
if old_av_norm in p_content_norm:
    p_content_norm = p_content_norm.replace(old_av_norm, new_avatar_block)
    print("Patched avatar wrapper in agent_profile.html")
else:
    print("Warning: old_avatar_block not found in agent_profile.html")

# Add change photo button next to name/title
old_title_p = '<p id="agentTitle" class="text-[11.5px] sm:text-xs text-slate-500 font-normal leading-relaxed"></p>'
new_title_p = '''<p id="agentTitle" class="text-[11.5px] sm:text-xs text-slate-500 font-normal leading-relaxed"></p>
          <button type="button" onclick="document.getElementById('customPhotoInput').click()" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 text-[10.5px] font-bold transition shadow-sm mt-1 active:scale-95">
            <svg class="w-3.5 h-3.5 text-amber-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
            <span>แตะเปลี่ยนรูปโปรไฟล์</span>
          </button>'''

if old_title_p in p_content_norm:
    p_content_norm = p_content_norm.replace(old_title_p, new_title_p)
    print("Added change photo button under title in agent_profile.html")
else:
    print("Warning: old_title_p not found in agent_profile.html")

# Update handleCustomPhoto to persist in localStorage and update modal
old_handle = '''    function handleCustomPhoto(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          document.getElementById("agentAvatar").src = evt.target.result;
          confirmPhoto();
          showToast("อัปโหลดรูปใหม่สำเร็จแล้ว");
        };
        reader.readAsDataURL(file);
      }
    }'''

new_handle = '''    function handleCustomPhoto(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          const dataUrl = evt.target.result;
          const avatarEl = document.getElementById("agentAvatar");
          if (avatarEl) avatarEl.src = dataUrl;
          const modalAvatar = document.getElementById("modalAvatar");
          if (modalAvatar) modalAvatar.src = dataUrl;

          // Save to localStorage
          const agentName = (document.getElementById("agentName").innerText || "").trim();
          try {
            if (agentName) localStorage.setItem("siwasup_avatar_" + agentName, dataUrl);
            localStorage.setItem("siwasup_current_avatar", dataUrl);
          } catch(err) {
            console.warn("Storage quota:", err);
          }
          if (typeof confirmPhoto === 'function') confirmPhoto();
          showToast("✓ เปลี่ยนรูปโปรไฟล์ใหม่เรียบร้อยแล้ว");
        };
        reader.readAsDataURL(file);
      }
    }'''

old_handle_norm = old_handle.replace("\r\n", "\n")
if old_handle_norm in p_content_norm:
    p_content_norm = p_content_norm.replace(old_handle_norm, new_handle)
    print("Patched handleCustomPhoto in agent_profile.html")
else:
    print("Warning: old_handle not found in agent_profile.html")

# Check for saved custom avatar on initial render
old_avatar_set = '''      // Avatar Override if passed
      if (getParam("avatar")) {
        a.avatar = getParam("avatar");
      }'''

new_avatar_set = '''      // Avatar Override if passed or in localStorage
      const savedCustomAvatar = localStorage.getItem("siwasup_avatar_" + a.name) || localStorage.getItem("siwasup_current_avatar");
      if (getParam("avatar")) {
        a.avatar = getParam("avatar");
      } else if (savedCustomAvatar) {
        a.avatar = savedCustomAvatar;
      }'''

old_av_set_norm = old_avatar_set.replace("\r\n", "\n")
if old_av_set_norm in p_content_norm:
    p_content_norm = p_content_norm.replace(old_av_set_norm, new_avatar_set)
    print("Patched avatar initialization in agent_profile.html")
else:
    print("Warning: old_avatar_set not found in agent_profile.html")

with open(profile_path, "w", encoding="utf-8") as f:
    f.write(p_content_norm)

print("Finished patching agent_profile.html!")
