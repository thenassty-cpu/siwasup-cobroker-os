# -*- coding: utf-8 -*-
import os, re

files = [
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\catalog.html",
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html"
]

banner_html = """    <!-- 🎯 Single Property Focus Landing Banner (ปรากฏเมื่อคลิกมาจาก LINE / Deep-link เฉพาะหลัง) -->
    <div id="single-property-focus-banner" class="hidden mx-3 sm:mx-6 mt-3 bg-[#faf8f5] text-neutral-800 p-3.5 sm:p-4 rounded-2xl shadow-xs text-xs border border-siwasup-gold/70 border-l-4 border-siwasup-gold animate-in fade-in duration-300">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-siwasup-gold/15 text-amber-800 flex items-center justify-center shrink-0">
            <i data-lucide="home" class="w-5 h-5 text-[#8C734B]"></i>
          </div>
          <div>
            <div class="flex items-center gap-2 font-bold text-sm text-neutral-900">
              <span id="single-focus-title">กำลังเปิดดูสเปกเต็มของทรัพย์นี้</span>
            </div>
            <p id="single-focus-subtitle" class="text-xs text-neutral-500 mt-0.5">
              คุณกำลังดูหน้าทรัพย์เฉพาะหลังที่เลือกมาจาก LINE สามารถดูรูปจริง สเปก และทำเลได้ครบถ้วน
            </p>
          </div>
        </div>
        <div class="flex items-center gap-2 shrink-0 self-end sm:self-auto">
          <button type="button" onclick="openPropertyDetailModal(window.activeSinglePropertyFocus)" class="px-3 py-1.5 rounded-xl bg-siwasup-gold text-neutral-950 font-bold hover:opacity-90 transition active:scale-95 shadow-2xs text-xs flex items-center gap-1.5">
            <i data-lucide="eye" class="w-3.5 h-3.5"></i>
            <span>เปิดสเปกเต็ม</span>
          </button>
          <button type="button" onclick="clearSinglePropertyFocus()" class="px-3 py-1.5 rounded-xl bg-white border border-neutral-300 hover:bg-neutral-100 text-neutral-700 font-semibold transition active:scale-95 text-xs">
            ดูทรัพย์ทั้งหมด (995 หลัง) &rarr;
          </button>
        </div>
      </div>
    </div>
"""

clear_focus_fn = """    function clearSinglePropertyFocus() {
      window.activeSinglePropertyFocus = null;
      activeBundleFilter = null;
      const b = document.getElementById('single-property-focus-banner');
      if (b) b.classList.add('hidden');
      renderProperties();
      if (typeof showToast === 'function') {
        showToast('ปลดล็อกแสดงทรัพย์ทั้งหมดในคลังเรียบร้อย');
      }
    }
"""

new_check_target = """    // 🎯 Instant Deep-Link Navigator (รองรับ ?id=, ?property=, ?code=, ?prop= และ #prop-...)
    function checkAndOpenTargetProperty(maxRetries = 40) {
      const params = new URLSearchParams(window.location.search);
      let targetId = params.get('id') || params.get('property') || params.get('code') || params.get('prop');
      
      // Fallback to URL Hash (#prop-B13559 or #B13559)
      if (!targetId && window.location.hash) {
        const cleanHash = window.location.hash.replace(/^#prop-/, '').replace(/^#/, '').trim();
        if (cleanHash && cleanHash.length > 2 && !cleanHash.startsWith('/')) {
          targetId = cleanHash;
        }
      }

      if (!targetId) return;
      targetId = targetId.trim();

      let attempts = 0;
      const pollTimer = setInterval(() => {
        attempts++;
        const list = (window.allProperties && window.allProperties.length > 0)
          ? window.allProperties
          : (window.SIWASUP_PROPERTIES || allProperties || []);

        const targetClean = targetId.toLowerCase();
        const found = list.find(item => {
          if (!item) return false;
          const itemId = String(item.id || '').trim().toLowerCase();
          const itemCode = String(item.code || '').trim().toLowerCase();
          const itemPropId = String(item.property_id || '').trim().toLowerCase();
          return itemId === targetClean || itemCode === targetClean || itemPropId === targetClean;
        });

        if (found) {
          clearInterval(pollTimer);
          window.activeSinglePropertyFocus = found.id || found.code;
          
          // ล็อกหน้าเว็บให้แสดงเฉพาะทรัพย์หลังนี้ ไม่ให้แสดงทรัพย์อื่น 995 หลังปนเปื้อน
          activeBundleFilter = [String(found.id || ''), String(found.code || ''), String(found.property_id || '')].filter(Boolean);
          
          const banner = document.getElementById('single-property-focus-banner');
          const titleEl = document.getElementById('single-focus-title');
          const subEl = document.getElementById('single-focus-subtitle');
          const displayTitle = typeof getDisplayTitle === 'function' ? getDisplayTitle(found) : (found.title || found.id);
          
          if (banner) {
            if (titleEl) titleEl.textContent = `กำลังดูข้อมูลทรัพย์: ${displayTitle}`;
            if (subEl) subEl.textContent = `รหัส #${found.id} • ${found.category || 'อสังหาฯ'} • ${found.location || ''} • ฿${formatPriceClean(found.price)}`;
            banner.classList.remove('hidden');
          }

          renderProperties();
          openPropertyDetailModal(found.id || found.code);
          
          if (typeof showToast === 'function') {
            showToast(`📍 กำลังเปิดสเปกเต็ม: ${displayTitle}`);
          }
          // เลื่อนหน้าจอไปยังการ์ดทรัพย์นั้นเบื้องหลัง
          setTimeout(() => {
            const cardEl = document.getElementById(`property-card-${found.id}`) || document.querySelector(`[data-prop-id="${found.id}"]`);
            if (cardEl) {
              cardEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
              cardEl.classList.add('ring-4', 'ring-[#8C734B]', 'transition-all');
              setTimeout(() => cardEl.classList.remove('ring-4', 'ring-[#8C734B]'), 3000);
            }
          }, 350);
        } else if (attempts >= maxRetries) {
          clearInterval(pollTimer);
          console.warn("Target property not found:", targetId);
        }
      }, 120);
    }
"""

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Insert banner after #vip-bundle-banner
    if 'id="single-property-focus-banner"' not in content:
        vip_closing = "      </div>\n    </div>\n\n    <!-- Trainee Agent Onboarding Challenge Banner"
        vip_closing_crlf = "      </div>\r\n    </div>\r\n\r\n    <!-- Trainee Agent Onboarding Challenge Banner"
        replacement_vip = "      </div>\n    </div>\n\n" + banner_html + "\n    <!-- Trainee Agent Onboarding Challenge Banner"
        replacement_vip_crlf = "      </div>\r\n    </div>\r\n\r\n" + banner_html.replace('\n', '\r\n') + "\r\n    <!-- Trainee Agent Onboarding Challenge Banner"
        
        if vip_closing_crlf in content:
            content = content.replace(vip_closing_crlf, replacement_vip_crlf, 1)
            print(f"[+] Inserted banner into {os.path.basename(fpath)} (CRLF)")
        elif vip_closing in content:
            content = content.replace(vip_closing, replacement_vip, 1)
            print(f"[+] Inserted banner into {os.path.basename(fpath)} (LF)")
        else:
            print(f"[-] Could not match vip_closing in {os.path.basename(fpath)}")

    # 2. Replace checkAndOpenTargetProperty
    old_check_pattern = r'    // 🎯 Instant Deep-Link Navigator.*?\n    function checkAndOpenTargetProperty\(.*?\}\n    \}'
    match = re.search(old_check_pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_check_target.rstrip() + "\n\n" + clear_focus_fn + content[match.end():]
        print(f"[+] Replaced checkAndOpenTargetProperty in {os.path.basename(fpath)}")
    else:
        print(f"[-] Could not find old checkAndOpenTargetProperty in {os.path.basename(fpath)}")

    # 3. Update modal open & close to use display = 'flex'
    old_modal_open = "modal.classList.remove('hidden');"
    new_modal_open = "modal.classList.remove('hidden');\n      modal.style.display = 'flex';\n      document.body.classList.add('modal-open');"
    # only replace inside openPropertyDetailModal
    if "modal.style.display = 'flex';" not in content and old_modal_open in content:
        content = content.replace(old_modal_open, new_modal_open, 1)
        print(f"[+] Added modal.style.display = 'flex' in {os.path.basename(fpath)}")

    old_modal_close = "function closePropertyDetailModal() {\n      const modal = document.getElementById('property-detail-modal');\n      if (modal) modal.classList.add('hidden');"
    new_modal_close = "function closePropertyDetailModal() {\n      const modal = document.getElementById('property-detail-modal');\n      if (modal) {\n        modal.classList.add('hidden');\n        modal.style.display = '';\n      }"
    
    old_modal_close_crlf = old_modal_close.replace('\n', '\r\n')
    new_modal_close_crlf = new_modal_close.replace('\n', '\r\n')
    if old_modal_close_crlf in content:
        content = content.replace(old_modal_close_crlf, new_modal_close_crlf, 1)
        print(f"[+] Updated closePropertyDetailModal in {os.path.basename(fpath)} (CRLF)")
    elif old_modal_close in content:
        content = content.replace(old_modal_close, new_modal_close, 1)
        print(f"[+] Updated closePropertyDetailModal in {os.path.basename(fpath)} (LF)")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

# Update sw.js version
sw_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\sw.js"
with open(sw_path, "r", encoding="utf-8") as f:
    sw_content = f.read()

sw_content = re.sub(r"const CACHE_NAME = 'siwasup-os-[^']+';", "const CACHE_NAME = 'siwasup-os-v20261104-2050';", sw_content)
with open(sw_path, "w", encoding="utf-8") as f:
    f.write(sw_content)
print("[+] Bumped sw.js to v20261104-2050")
