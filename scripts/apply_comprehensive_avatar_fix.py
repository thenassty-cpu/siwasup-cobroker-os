import re

# ==============================================================
# 1. UPDATE agent_profile.html
# ==============================================================
profile_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(profile_path, "r", encoding="utf-8") as f:
    p_text = f.read()

# Replace lines 92-104 with clickable avatar and camera badge
old_avatar_markup = '''        <!-- Avatar Wrapper with 37px Rounded Corners -->
        <div class="relative shrink-0">
          <img id="agentAvatar" 
               src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80" 
               alt="Agent Profile" 
               class="w-[86px] h-[86px] sm:w-24 sm:h-24 squircle-37 object-cover bg-slate-100 border-2 border-[#E5B54F]/70 shadow-xs" />
          <!-- Verified Badge (Enlarged 28px Vector Match from Illustrator, Zero Crowding) -->
          <span class="absolute -bottom-1 -right-1 w-7 h-7 sm:w-7.5 sm:h-7.5 rounded-full bg-[#3fb354] border-[2.5px] border-white flex items-center justify-center shadow-xs" title="ที่ปรึกษาที่ผ่านการรับรอง">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </span>
        </div>'''

new_avatar_markup = '''        <!-- Avatar Wrapper with 37px Rounded Corners (Clickable Anywhere to Upload) -->
        <label for="customPhotoInput" class="relative shrink-0 cursor-pointer group block" title="แตะเพื่อเปลี่ยนรูปโปรไฟล์">
          <img id="agentAvatar" 
               src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80" 
               alt="Agent Profile" 
               class="w-[86px] h-[86px] sm:w-24 sm:h-24 squircle-37 object-cover bg-slate-100 border-2 border-amber-400 shadow-md transition group-hover:scale-105 group-hover:brightness-95" />
          <!-- Camera Overlay Badge on Avatar -->
          <span class="absolute -bottom-1 -left-1 w-7 h-7 sm:w-7.5 sm:h-7.5 rounded-full bg-slate-900 text-white flex items-center justify-center border-2 border-white shadow-md transition group-hover:scale-110 group-hover:bg-amber-500">
            <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
              <circle cx="12" cy="13" r="4"></circle>
            </svg>
          </span>
          <!-- Verified Badge -->
          <span class="absolute -bottom-1 -right-1 w-7 h-7 sm:w-7.5 sm:h-7.5 rounded-full bg-[#3fb354] border-[2.5px] border-white flex items-center justify-center shadow-xs" title="ที่ปรึกษาที่ผ่านการรับรอง">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </span>
        </label>'''

p_norm = p_text.replace("\r\n", "\n")
old_av_norm = old_avatar_markup.replace("\r\n", "\n")
if old_av_norm in p_norm:
    p_norm = p_norm.replace(old_av_norm, new_avatar_markup)
    print("1.1 Patched avatar wrapper in agent_profile.html")
else:
    print("Warning: old_avatar_markup not found in agent_profile.html")

# Add change photo button under title
old_title_line = '<p id="agentTitle" class="text-[11.5px] sm:text-xs text-slate-500 font-normal leading-relaxed truncate">ที่ปรึกษาด้านการซื้อ-ขายอสังหาริมทรัพย์มืออาชีพ</p>'
new_title_line = '''<p id="agentTitle" class="text-[11.5px] sm:text-xs text-slate-500 font-normal leading-relaxed truncate">ที่ปรึกษาด้านการซื้อ-ขายอสังหาริมทรัพย์มืออาชีพ</p>
          <button type="button" onclick="document.getElementById('customPhotoInput').click()" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 text-[10.5px] font-bold transition shadow-sm mt-1 active:scale-95">
            <svg class="w-3.5 h-3.5 text-amber-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
            <span>📷 แตะเปลี่ยนรูปโปรไฟล์</span>
          </button>'''

if old_title_line in p_norm:
    p_norm = p_norm.replace(old_title_line, new_title_line)
    print("1.2 Added change photo button in agent_profile.html")
else:
    print("Warning: old_title_line not found in agent_profile.html")

# Patch avatar source check in line 600
old_set_avatar = '      const avatarEl = document.getElementById("agentAvatar");\n      avatarEl.src = a.avatar;'
new_set_avatar = '''      const avatarEl = document.getElementById("agentAvatar");
      const savedCustomAvatar = localStorage.getItem("siwasup_avatar_" + a.name) || localStorage.getItem("siwasup_current_avatar");
      if (getParam("avatar")) {
        avatarEl.src = getParam("avatar");
      } else if (savedCustomAvatar) {
        avatarEl.src = savedCustomAvatar;
      } else {
        avatarEl.src = a.avatar;
      }'''

old_set_norm = old_set_avatar.replace("\r\n", "\n")
if old_set_norm in p_norm:
    p_norm = p_norm.replace(old_set_norm, new_set_avatar)
    print("1.3 Patched avatarEl.src resolution in agent_profile.html")
else:
    print("Warning: old_set_avatar not found in agent_profile.html")

with open(profile_path, "w", encoding="utf-8") as f:
    f.write(p_norm)


# ==============================================================
# 2. UPDATE agent_registration.html
# ==============================================================
reg_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_registration.html"
with open(reg_path, "r", encoding="utf-8") as f:
    reg_text = f.read()

reg_norm = reg_text.replace("\r\n", "\n")

# Insert photo upload section before Full Name
old_name_field = '''        <!-- 2. Full Name -->
        <div class="space-y-1">
          <label class="text-xs font-bold text-slate-300 flex items-center gap-1.5">
            <i data-lucide="user" class="w-3.5 h-3.5 text-amber-400"></i>
            <span>ชื่อ - นามสกุลจริง (สำหรับแสดงบนนามบัตรทางการ) *</span>
          </label>'''

photo_upload_markup = '''        <!-- 1.5 Photo Upload & Avatar Picker -->
        <div class="space-y-2 p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800">
          <label class="text-xs font-bold text-amber-400 flex items-center justify-between">
            <span class="flex items-center gap-1.5">
              <i data-lucide="camera" class="w-3.5 h-3.5"></i>
              <span>รูปถ่ายโปรไฟล์ทางการ (Profile Picture) *</span>
            </span>
            <span class="text-[10px] text-slate-400">อัปโหลดรูปจริง หรือเลือกอวตาร</span>
          </label>

          <div class="flex items-center gap-3.5">
            <!-- Current Photo Preview & Click to Upload -->
            <label for="regPhotoFile" class="relative cursor-pointer shrink-0 group block" title="แตะเพื่อเลือกรูปจากมือถือ">
              <img id="regPhotoPreview" 
                   src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80" 
                   alt="Profile Preview" 
                   class="w-16 h-16 rounded-2xl object-cover border-2 border-amber-400 shadow-lg group-hover:brightness-90 transition">
              <span class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center border border-white shadow-sm group-hover:bg-amber-500 transition">
                <i data-lucide="upload" class="w-3 h-3"></i>
              </span>
            </label>
            <input type="file" id="regPhotoFile" accept="image/*" class="hidden" onchange="handleRegPhotoUpload(event)">

            <div class="space-y-1.5 flex-1 min-w-0">
              <button type="button" onclick="document.getElementById('regPhotoFile').click()" class="w-full py-1.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-bold flex items-center justify-center gap-1.5 transition active:scale-98">
                <i data-lucide="image" class="w-3.5 h-3.5 text-amber-400"></i>
                <span>📁 แตะเลือกรูปจากมือถือ (ถ่าย/อัลบั้ม)</span>
              </button>

              <!-- Quick Presets -->
              <div class="flex items-center gap-1.5 overflow-x-auto pb-0.5">
                <span class="text-[9px] text-slate-500 shrink-0">หรือเลือก:</span>
                <button type="button" onclick="selectPresetAvatar('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80')" class="w-6 h-6 rounded-full overflow-hidden border border-slate-700 hover:border-amber-400 shrink-0" title="หญิง ทางการ">
                  <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&auto=format&fit=crop&q=80" class="w-full h-full object-cover">
                </button>
                <button type="button" onclick="selectPresetAvatar('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80')" class="w-6 h-6 rounded-full overflow-hidden border border-slate-700 hover:border-amber-400 shrink-0" title="ชาย สูท">
                  <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80" class="w-full h-full object-cover">
                </button>
                <button type="button" onclick="selectPresetAvatar('https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&auto=format&fit=crop&q=80')" class="w-6 h-6 rounded-full overflow-hidden border border-slate-700 hover:border-amber-400 shrink-0" title="หญิง แคชชวล">
                  <img src="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=100&auto=format&fit=crop&q=80" class="w-full h-full object-cover">
                </button>
                <button type="button" onclick="selectPresetAvatar('https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80')" class="w-6 h-6 rounded-full overflow-hidden border border-slate-700 hover:border-amber-400 shrink-0" title="ชาย แคชชวล">
                  <img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80" class="w-full h-full object-cover">
                </button>
              </div>
            </div>
          </div>
        </div>

''' + old_name_field

old_name_norm = old_name_field.replace("\r\n", "\n")
if old_name_norm in reg_norm:
    reg_norm = reg_norm.replace(old_name_norm, photo_upload_markup)
    print("2.1 Added photo upload section to agent_registration.html")
else:
    print("Warning: old_name_field not found in agent_registration.html")

# Add photo upload handlers in javascript
js_photo_helpers = '''
    let selectedAvatarUrl = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80";

    function selectPresetAvatar(url) {
      selectedAvatarUrl = url;
      document.getElementById('regPhotoPreview').src = url;
    }

    function handleRegPhotoUpload(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          // Resize/compress to 400x400 canvas for fast upload & storage
          const img = new Image();
          img.onload = function() {
            const canvas = document.createElement('canvas');
            const maxDim = 400;
            let width = img.width;
            let height = img.height;
            if (width > height) {
              if (width > maxDim) {
                height *= maxDim / width;
                width = maxDim;
              }
            } else {
              if (height > maxDim) {
                width *= maxDim / height;
                height = maxDim;
              }
            }
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.85);

            selectedAvatarUrl = compressedDataUrl;
            document.getElementById('regPhotoPreview').src = compressedDataUrl;
            try {
              localStorage.setItem('siwasup_current_avatar', compressedDataUrl);
            } catch(err) {}
          };
          img.src = evt.target.result;
        };
        reader.readAsDataURL(file);
      }
    }
'''

# Insert js_photo_helpers before submitToLobby
old_submit_fn = 'function submitToLobby() {'
new_submit_fn = js_photo_helpers + '\n    function submitToLobby() {'

if old_submit_fn in reg_norm:
    reg_norm = reg_norm.replace(old_submit_fn, new_submit_fn, 1)
    print("2.2 Added js_photo_helpers in agent_registration.html")
else:
    print("Warning: old_submit_fn not found in agent_registration.html")

# Update currentApplicant in submitToLobby to include avatar
old_app_obj = '''      currentApplicant = {
        id: appId,
        name: name,
        nickname: nickname || name,
        phone: phone,
        line_id: lineId || "ไม่ระบุ",
        zone: zone,
        affiliation: affiliation,
        affiliation_label: affiliation === 'office' ? "🏢 พนักงาน/ทีมงานออฟฟิศ" : "🤝 Co-Broker พันธมิตรภายนอก",
        status: "pending",
        submitted_at: "เมื่อสักครู่"
      };'''

new_app_obj = '''      currentApplicant = {
        id: appId,
        name: name,
        nickname: nickname || name,
        phone: phone,
        line_id: lineId || "ไม่ระบุ",
        zone: zone,
        affiliation: affiliation,
        affiliation_label: affiliation === 'office' ? "🏢 พนักงาน/ทีมงานออฟฟิศ" : "🤝 Co-Broker พันธมิตรภายนอก",
        avatar: selectedAvatarUrl,
        status: "pending",
        submitted_at: "เมื่อสักครู่"
      };
      try {
        localStorage.setItem("siwasup_avatar_" + name, selectedAvatarUrl);
        localStorage.setItem("siwasup_current_avatar", selectedAvatarUrl);
      } catch(e) {}'''

old_app_norm = old_app_obj.replace("\r\n", "\n")
if old_app_norm in reg_norm:
    reg_norm = reg_norm.replace(old_app_norm, new_app_obj)
    print("2.3 Added avatar field to currentApplicant in agent_registration.html")
else:
    print("Warning: old_app_obj not found in agent_registration.html")

# Update card link in handleApplicantApproved to pass avatar
old_card_url = "const cardUrl = `https://assets.siwasup.com/agent_profile.html?name=${encodeURIComponent(approvedData.name)}&phone=${encodeURIComponent(approvedData.phone)}&zone=${encodeURIComponent(approvedData.zone)}&title=${encodeURIComponent(approvedData.title || '')}&mode=client`;"
new_card_url = "const cardUrl = `https://assets.siwasup.com/agent_profile.html?name=${encodeURIComponent(approvedData.name)}&phone=${encodeURIComponent(approvedData.phone)}&zone=${encodeURIComponent(approvedData.zone)}&title=${encodeURIComponent(approvedData.title || '')}&mode=client&avatar=${encodeURIComponent(approvedData.avatar || selectedAvatarUrl)}`;"

if old_card_url in reg_norm:
    reg_norm = reg_norm.replace(old_card_url, new_card_url)
    print("2.4 Updated cardUrl in handleApplicantApproved")
else:
    print("Warning: old_card_url not found in agent_registration.html")

with open(reg_path, "w", encoding="utf-8") as f:
    f.write(reg_norm)


# ==============================================================
# 3. UPDATE scripts/line_gemini_webhook.py (Expand Keyword Listeners)
# ==============================================================
webhook_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"
with open(webhook_path, "r", encoding="utf-8") as f:
    w_text = f.read()

w_norm = w_text.replace("\r\n", "\n")

old_kw = "if any(k in text_clean for k in ['สมัคร', 'ลงทะเบียน', 'login', 'เข้าสู่ระบบ', 'ขอนามบัตร', 'นามบัตร']):"
new_kw = "if any(k in text_clean for k in ['สมัคร', 'ลงทะเบียน', 'login', 'เข้าสู่ระบบ', 'ขอนามบัตร', 'นามบัตร', 'เอเจนต์', 'เอเจน', 'ตัวแทน', 'ร่วมงาน', 'ขอเข้ากลุ่ม', 'เข้ากลุ่ม', 'นายหน้า', 'co-broker', 'cobroker', 'ขอลิงก์', 'ขอลิงค์', 'วิธีสมัคร', 'อยากเป็นเอเจนต์']):"

if old_kw in w_norm:
    w_norm = w_norm.replace(old_kw, new_kw)
    print("3.1 Expanded keyword listeners in webhook")
else:
    print("Warning: old_kw not found in line_gemini_webhook.py")

with open(webhook_path, "w", encoding="utf-8") as f:
    f.write(w_norm)

print("\n[SUCCESS] Comprehensive Avatar & LINE OA fixes applied!")
