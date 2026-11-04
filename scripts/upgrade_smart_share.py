# -*- coding: utf-8 -*-
"""
scripts/upgrade_smart_share.py
---------------------------------------------
Upgrades Smart Share Center from a simple URL-copy mockup
into a full-featured, functional multi-channel sharing suite:
- Direct LINE share (opens LINE with prefilled card text & link)
- LINE rich caption copy
- Direct Facebook share (opens FB sharer dialog)
- Facebook Marketplace sales post copy
- TikTok/Reels bio hook caption copy
- Native mobile system share (navigator.share)
- QR Code display
"""

import os
import re

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
MODALS_JS = os.path.join(BASE_DIR, "modals.js")
CATALOG_HTML = os.path.join(BASE_DIR, "catalog.html")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")

new_modal_share_ui = """            <!-- Native System Share Button (1-Click Share to All Apps) -->
            <button type="button" onclick="shareViaSystemNative()" class="w-full bg-gradient-to-r from-amber-600 to-[#8C734B] hover:from-amber-700 hover:to-[#735d3b] text-white font-bold py-2 px-3 rounded-xl shadow-xs text-xs flex items-center justify-center gap-2 active:scale-95 transition-all mb-1">
              <i data-lucide="share-2" class="w-3.5 h-3.5"></i>
              <span>📲 แชร์ด่วนผ่านแอปมือถือ (LINE, FB, IG, แชต)</span>
            </button>

            <!-- Channel Links Header -->
            <div class="font-bold text-gray-700 text-[11px] flex justify-between items-center px-0.5 pt-0.5">
              <span>เลือกช่องทางโปรโมท:</span>
              <span class="text-[9px] text-gray-400">กดแชร์ตรงหรือก๊อปแคปชั่น</span>
            </div>

            <!-- Channel 1: LINE -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-emerald-200 bg-emerald-50/60 hover:bg-emerald-50 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-xs shadow-2xs">L</span>
                <div class="truncate">
                  <div class="font-bold text-emerald-950 text-xs">LINE (แชตส่วนตัว / ส่งกลุ่ม)</div>
                  <div class="text-[10px] text-emerald-700 truncate">เปิดส่งเข้า LINE ทันที หรือก๊อปแคปชั่น</div>
                </div>
              </div>
              <div class="flex items-center gap-1.5 shrink-0 ml-2">
                <button onclick="shareDirectToLine()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-1 px-2.5 rounded-lg text-[11px] shadow-xs active:scale-95 transition-all flex items-center gap-1">
                  <span>ส่ง LINE</span>
                </button>
                <button onclick="copyLineCaption()" title="คัดลอกข้อความพร้อมส่ง" class="bg-white hover:bg-emerald-100 text-emerald-800 border border-emerald-300 font-semibold py-1 px-2 rounded-lg text-[10px] shadow-2xs active:scale-95 transition-all">
                  ก๊อปแคปชั่น
                </button>
              </div>
            </div>

            <!-- Channel 2: Facebook -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-blue-200 bg-blue-50/60 hover:bg-blue-50 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs shadow-2xs">f</span>
                <div class="truncate">
                  <div class="font-bold text-blue-950 text-xs">Facebook (Marketplace / โพสต์)</div>
                  <div class="text-[10px] text-blue-700 truncate">เปิดแชร์หน้าเว็บ หรือก๊อปโพสต์ขาย</div>
                </div>
              </div>
              <div class="flex items-center gap-1.5 shrink-0 ml-2">
                <button onclick="shareDirectToFacebook()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-1 px-2.5 rounded-lg text-[11px] shadow-xs active:scale-95 transition-all flex items-center gap-1">
                  <span>แชร์ FB</span>
                </button>
                <button onclick="copyFacebookPost()" title="คัดลอกโพสต์ขายพร้อมลง Marketplace" class="bg-white hover:bg-blue-100 text-blue-800 border border-blue-300 font-semibold py-1 px-2 rounded-lg text-[10px] shadow-2xs active:scale-95 transition-all">
                  ก๊อปโพสต์ขาย
                </button>
              </div>
            </div>

            <!-- Channel 3: TikTok / Reels -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-gray-300 bg-gray-50 hover:bg-gray-100/70 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-gray-900 text-white flex items-center justify-center font-bold text-xs shadow-2xs">♪</span>
                <div class="truncate">
                  <div class="font-bold text-gray-950 text-xs">TikTok / Reels / Shorts</div>
                  <div class="text-[10px] text-gray-600 truncate">แคปชั่นสั้นกระชับ สำหรับแปะ Bio / คอมเมนต์</div>
                </div>
              </div>
              <div class="flex items-center gap-1.5 shrink-0 ml-2">
                <button onclick="copyTikTokBioCaption()" class="bg-gray-900 hover:bg-black text-white font-semibold py-1 px-2.5 rounded-lg text-[11px] shadow-xs active:scale-95 transition-all">
                  ก๊อปแคปชั่น & Bio
                </button>
              </div>
            </div>

            <!-- Channel 4: General Web / Forum -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-gray-200 bg-gray-50/70 hover:bg-gray-100/70 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="icon-circle w-6 h-6 shrink-0 bg-gray-800 text-white"><i data-lucide="globe" class="w-3.5 h-3.5 stroke-[1.5]"></i></span>
                <div class="truncate">
                  <div class="font-bold text-gray-900 text-xs">เว็บบอร์ด / LivingInsider / เว็บไซต์</div>
                  <div class="text-[10px] text-gray-500 truncate">ลิงก์กลางสำหรับโพสต์ลงเว็บไซต์ทั่วไป</div>
                </div>
              </div>
              <div class="flex items-center gap-1.5 shrink-0 ml-2">
                <button onclick="copyChannelLink('web')" class="bg-gray-800 hover:bg-gray-900 text-white font-medium py-1 px-2.5 rounded-lg text-[11px] shadow-xs active:scale-95 transition-all">
                  คัดลอกลิงก์
                </button>
              </div>
            </div>

            <!-- Channel 5: QR Code Generator Action Row -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-amber-200/90 bg-amber-50/50 hover:bg-amber-50 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="icon-circle w-6 h-6 shrink-0 bg-amber-700 text-white"><i data-lucide="qr-code" class="w-3.5 h-3.5 stroke-[1.5]"></i></span>
                <div class="truncate">
                  <div class="font-bold text-amber-950 text-xs">QR Code ป้ายหน้าบ้าน / นามบัตร</div>
                  <div class="text-[10px] text-amber-700 truncate">สแกนป้ายแล้วล็อกค่าคอม 60 วัน</div>
                </div>
              </div>
              <button onclick="toggleQrView()" class="shrink-0 ml-2 bg-neutral-900 hover:bg-neutral-800 text-white font-medium py-1 px-3 rounded-lg text-[11px] shadow-xs flex items-center gap-1 active:scale-95 transition-all">
                <i data-lucide="scan-line" class="w-3 h-3"></i>
                <span id="qr-toggle-text">เปิดดู QR</span>
              </button>
            </div>"""

new_js_logic = """    // --- SMART SHARE REAL ACTIONS & LEAD ENGINE ---
    function getSharePropertyObject() {
      if (!currentShareProp || !currentShareProp.id) return null;
      const list = (window.allProperties && window.allProperties.length > 0)
        ? window.allProperties
        : (window.SIWASUP_PROPERTIES || allProperties || []);
      const cleanId = String(currentShareProp.id).trim().toLowerCase();
      return list.find(x => String(x.id || '').trim().toLowerCase() === cleanId || String(x.code || '').trim().toLowerCase() === cleanId) || currentShareProp;
    }

    function shareDirectToLine() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const targetUrl = `${getBaseUrl()}?view=client&property=${p.id}&ref=${ref}&src=line`;

      const title = (typeof getDisplayTitle === 'function' ? getDisplayTitle(p) : (p.title || `ทรัพย์ NPA รหัส #${p.id}`));
      const price = p.price || '';
      const loc = p.location || '';
      const size = p.size ? `ขนาด: ${p.size}` : '';

      const text = `🏡 ${title}\\n💰 ราคา: ${price}\\n📍 ทำเล: ${loc} ${size ? `• ${size}` : ''}\\n\\n✨ ทรัพย์คัดพิเศษ ยื่นกู้ได้เต็ม ดูแลเอกสารฟรี\\n👉 ดูรูปจริง & รายละเอียด: ${targetUrl}`;
      
      if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && rawRef) {
        window.SiwasupAgents.award(rawRef, 'smart_share_click', { channel: 'line', propId: p.id });
      }

      const lineUrl = `https://line.me/R/msg/text/?${encodeURIComponent(text)}`;
      window.open(lineUrl, '_blank');
      showToast('🚀 กำลังเปิด LINE เพื่อส่งต่อ...');
    }

    function copyLineCaption() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const targetUrl = `${getBaseUrl()}?view=client&property=${p.id}&ref=${ref}&src=line`;

      const title = (typeof getDisplayTitle === 'function' ? getDisplayTitle(p) : (p.title || `ทรัพย์ NPA รหัส #${p.id}`));
      const price = p.price || '';
      const loc = p.location || '';
      const size = p.size ? `ขนาด: ${p.size}` : '';

      const text = `🏡 ${title}\\n💰 ราคา: ${price}\\n📍 ทำเล: ${loc} ${size ? `• ${size}` : ''}\\n\\n✨ ทรัพย์คัดพิเศษ ยื่นกู้ได้เต็ม ดูแลเอกสารฟรี\\n👉 ดูรูปจริง & รายละเอียด: ${targetUrl}`;

      navigator.clipboard.writeText(text).then(() => {
        showToast('📋 คัดลอกแคปชั่น LINE พร้อมส่งเรียบร้อย!');
        closeShareModal();
      }).catch(() => {
        copyChannelLink('line');
      });
    }

    function shareDirectToFacebook() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const targetUrl = `${getBaseUrl()}?view=client&property=${p.id}&ref=${ref}&src=facebook`;

      if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && rawRef) {
        window.SiwasupAgents.award(rawRef, 'smart_share_click', { channel: 'facebook', propId: p.id });
      }

      const fbUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(targetUrl)}`;
      window.open(fbUrl, '_blank', 'width=600,height=550');
      showToast('🚀 เปิดหน้าต่างแชร์ Facebook เรียบร้อย');
    }

    function copyFacebookPost() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const targetUrl = `${getBaseUrl()}?view=client&property=${p.id}&ref=${ref}&src=facebook`;

      const title = (typeof getDisplayTitle === 'function' ? getDisplayTitle(p) : (p.title || `ทรัพย์ NPA #${p.id}`));
      const price = p.price || '';
      const loc = p.location || '';
      const size = p.size ? `ขนาดที่ดิน: ${p.size}` : '';
      const usable = p.usable_area ? `พื้นที่ใช้สอย: ${p.usable_area}` : '';

      const postText = `🔥 [เปิดจองทรัพย์คัดพิเศษ NPA] ${title}\\n` +
        `💵 ราคาพิเศษ: ${price}\\n` +
        `📍 ทำเลที่ตั้ง: ${loc}\\n` +
        `📐 ${size} ${usable ? `| ${usable}` : ''}\\n\\n` +
        `✅ โครงสร้างแข็งแรง คัดสภาพดี\\n` +
        `✅ ยื่นกู้สินเชื่อได้ 100% มีเจ้าหน้าที่ช่วยดูแลทุกขั้นตอน\\n` +
        `✅ นัดหมายเข้าชมบ้านจริงได้ทุกวัน\\n\\n` +
        `🔎 ดูรูปภาพจริงและสเปกเต็มคลิกที่นี่:\\n` +
        `👉 ${targetUrl}\\n\\n` +
        `#บ้านมือสอง #ทรัพย์NPA #ขายบ้าน #ศิวาทรัพย์ #สินเชื่อบ้าน`;

      navigator.clipboard.writeText(postText).then(() => {
        showToast('📋 คัดลอกโพสต์ขาย Facebook Marketplace สำเร็จ!');
        closeShareModal();
      }).catch(() => {
        copyChannelLink('facebook');
      });
    }

    function copyTikTokBioCaption() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const targetUrl = `${getBaseUrl()}?view=client&property=${p.id}&ref=${ref}&src=tiktok`;

      const title = (typeof getDisplayTitle === 'function' ? getDisplayTitle(p) : (p.title || `ทรัพย์ NPA #${p.id}`));
      const price = p.price || '';
      const loc = p.location || '';

      const caption = `🏡 ${title} ราคาดีมาก ${price} (${loc}) กู้ได้เต็ม 100% 📍 พิกัด & ดูรูปจริงกดลิงก์หน้าโปรไฟล์: ${targetUrl}`;

      navigator.clipboard.writeText(caption).then(() => {
        showToast('📋 คัดลอกแคปชั่นสำหรับ TikTok / Reels สำเร็จ!');
        closeShareModal();
      }).catch(() => {
        copyChannelLink('tiktok');
      });
    }

    function shareViaSystemNative() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const targetUrl = `${getBaseUrl()}?view=client&property=${p.id}&ref=${ref}&src=native_share`;

      const title = (typeof getDisplayTitle === 'function' ? getDisplayTitle(p) : (p.title || `ทรัพย์ NPA #${p.id}`));
      const price = p.price || '';

      if (navigator.share) {
        navigator.share({
          title: title,
          text: `🏡 ${title} • ราคา ${price}\\nดูรูปจริงและสเปกเต็มได้ที่นี่:`,
          url: targetUrl
        }).then(() => {
          if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && rawRef) {
            window.SiwasupAgents.award(rawRef, 'smart_share_click', { channel: 'native', propId: p.id });
          }
          showToast('🎉 แชร์ผ่านมือถือสำเร็จ!');
          closeShareModal();
        }).catch(err => {
          console.log('Share dismissed or cancelled');
        });
      } else {
        // Fallback to LINE or direct copy
        shareDirectToLine();
      }
    }
"""

# 1. Update modals.js
print("[*] Updating modals.js...")
with open(MODALS_JS, 'r', encoding='utf-8') as f:
    modals_code = f.read()

old_channels_pattern = r'<!-- Channel Links Header -->.*?<!-- Channel 5: QR Code Generator Action Row -->.*?</div>'
match = re.search(old_channels_pattern, modals_code, re.DOTALL)
if match:
    modals_code = modals_code[:match.start()] + new_modal_share_ui + modals_code[match.end():]
    print("[+] modals.js Smart Share UI replaced successfully!")
else:
    print("[-] Could not find old_channels_pattern in modals.js")

with open(MODALS_JS, 'w', encoding='utf-8') as f:
    f.write(modals_code)

# 2. Update catalog.html and index.html
for html_file in [CATALOG_HTML, INDEX_HTML]:
    print(f"[*] Updating {os.path.basename(html_file)}...")
    with open(html_file, 'r', encoding='utf-8') as f:
        c = f.read()

    # Insert new_js_logic right before copyChannelLink
    target_needle = "    function copyChannelLink(channel) {"
    if "function shareDirectToLine" not in c and target_needle in c:
        c = c.replace(target_needle, new_js_logic + "\n" + target_needle)
        print(f"[+] Injected real share functions into {os.path.basename(html_file)}")
    elif "function shareDirectToLine" in c:
        print(f"[!] Already present in {os.path.basename(html_file)}")

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(c)

print("[*] Upgrading complete!")
