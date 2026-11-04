# scripts/patch_share_center.py
# -*- coding: utf-8 -*-
import os

new_code = '''    // --- SMART SHARE CENTER FUNCTIONS ---
    let currentShareProp = null;

    // Helper for robust clipboard copy on mobile / Safari / iOS / In-app Webviews
    function copyTextToClipboard(text, successMsg) {
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
          if (successMsg) showToast(successMsg);
        }).catch(() => {
          fallbackCopyText(text, successMsg);
        });
      } else {
        fallbackCopyText(text, successMsg);
      }
    }

    function fallbackCopyText(text, successMsg) {
      try {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-9999px";
        textArea.style.top = "0";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        if (successful) {
          if (successMsg) showToast(successMsg);
        } else {
          prompt("กดค้างเพื่อคัดลอกข้อความ:", text);
        }
      } catch (err) {
        prompt("กดค้างเพื่อคัดลอกข้อความ:", text);
      }
    }

    function openSmartShare(id, title) {
      currentShareProp = { id, title };
      const savedRef = localStorage.getItem('siwasup_my_agent_ref') || 'AG-บัวรา';
      const refInput = document.getElementById('agent-ref-input');
      if (refInput) refInput.value = savedRef;

      const propInfo = document.getElementById('share-prop-info');
      if (propInfo) {
        propInfo.innerHTML = `
          <div class="font-bold text-gray-900 flex items-center gap-1.5 truncate">
            <span class="icon-circle w-4 h-4 shrink-0"><i data-lucide="home" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span class="truncate" id="share-modal-title-span"></span>
          </div>
          <div class="text-[10px] text-gray-600">รหัสทรัพย์: <span class="font-mono text-amber-800 font-bold" id="share-modal-id-span"></span></div>
        `;
        const titleSpan = document.getElementById('share-modal-title-span');
        const idSpan = document.getElementById('share-modal-id-span');
        if (titleSpan) titleSpan.textContent = title || '';
        if (idSpan) idSpan.textContent = id || '';
      }

      // Reset desktop QR panel state on fresh open
      const desktopPanel = document.getElementById('desktop-qr-panel');
      const shareModalCard = document.getElementById('share-modal-card');
      const toggleText = document.getElementById('qr-toggle-text');
      if (desktopPanel) {
        desktopPanel.classList.remove('max-w-[260px]', 'opacity-100', 'pointer-events-auto');
        desktopPanel.classList.add('max-w-0', 'opacity-0', 'pointer-events-none');
      }
      if (shareModalCard) {
        shareModalCard.classList.remove('md:max-w-2xl');
        shareModalCard.classList.add('md:max-w-md');
      }
      if (toggleText) toggleText.textContent = "เปิดดู QR";

      closeMobileQrModal();
      document.getElementById('share-modal').classList.remove('hidden');
      if (window.lucide) { lucide.createIcons(); }
      updateShareUrls();
    }

    function closeShareModal() {
      const shareModal = document.getElementById('share-modal');
      if (shareModal) shareModal.classList.add('hidden');
      closeMobileQrModal();
    }

    function getBaseUrl() {
      return window.location.href.split('?')[0];
    }

    function updateShareUrls() {
      if (!currentShareProp) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'AG-บัวรา';
      const ref = encodeURIComponent(rawRef || 'AG-บัวรา');
      localStorage.setItem('siwasup_my_agent_ref', rawRef || 'AG-บัวรา');
      
      const safePropId = encodeURIComponent(currentShareProp.id);
      const qrUrl = `${getBaseUrl()}?view=client&prop=${safePropId}&ref=${ref}&src=qr_sign`;
      const qrSrc = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(qrUrl)}`;

      const desktopImg = document.getElementById('qr-image-desktop');
      if (desktopImg) desktopImg.src = qrSrc;

      const mobileImg = document.getElementById('qr-image-mobile');
      if (mobileImg) mobileImg.src = qrSrc;

      const fallbackImg = document.getElementById('qr-image');
      if (fallbackImg) fallbackImg.src = qrSrc;
    }

    // --- SMART SHARE REAL ACTIONS & LEAD ENGINE ---
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
      const safePropId = encodeURIComponent(p.id);
      const targetUrl = `${getBaseUrl()}?view=client&property=${safePropId}&ref=${ref}&src=line`;

      const title = (typeof getDisplayTitle === 'function' ? getDisplayTitle(p) : (p.title || `ทรัพย์ NPA รหัส #${p.id}`));
      const price = p.price || '';
      const loc = p.location || '';
      const size = p.size ? `ขนาด: ${p.size}` : '';

      const text = `🏡 ${title}\\n💰 ราคา: ${price}\\n📍 ทำเล: ${loc} ${size ? `• ${size}` : ''}\\n\\n✨ ทรัพย์คัดพิเศษ ยื่นกู้ได้เต็ม ดูแลเอกสารฟรี\\n👉 ดูรูปจริง & รายละเอียด: ${targetUrl}`;
      
      if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && rawRef) {
        window.SiwasupAgents.award(rawRef, 'smart_share_click', { channel: 'line', propId: p.id });
      }

      const lineUrl = `https://line.me/R/msg/text/?${encodeURIComponent(text)}`;
      
      // If inside mobile browser / in-app webview, window.location.href avoids popup blocker
      const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
      if (isMobile) {
        window.location.href = lineUrl;
      } else {
        window.open(lineUrl, '_blank');
      }
      showToast('🚀 กำลังเปิด LINE เพื่อส่งต่อ...');
    }

    function copyLineCaption() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const safePropId = encodeURIComponent(p.id);
      const targetUrl = `${getBaseUrl()}?view=client&property=${safePropId}&ref=${ref}&src=line`;

      const title = (typeof getDisplayTitle === 'function' ? getDisplayTitle(p) : (p.title || `ทรัพย์ NPA รหัส #${p.id}`));
      const price = p.price || '';
      const loc = p.location || '';
      const size = p.size ? `ขนาด: ${p.size}` : '';

      const text = `🏡 ${title}\\n💰 ราคา: ${price}\\n📍 ทำเล: ${loc} ${size ? `• ${size}` : ''}\\n\\n✨ ทรัพย์คัดพิเศษ ยื่นกู้ได้เต็ม ดูแลเอกสารฟรี\\n👉 ดูรูปจริง & รายละเอียด: ${targetUrl}`;

      copyTextToClipboard(text, '📋 คัดลอกแคปชั่น LINE พร้อมส่งเรียบร้อย!');
      closeShareModal();
    }

    function shareDirectToFacebook() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const safePropId = encodeURIComponent(p.id);
      const targetUrl = `${getBaseUrl()}?view=client&property=${safePropId}&ref=${ref}&src=facebook`;

      if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && rawRef) {
        window.SiwasupAgents.award(rawRef, 'smart_share_click', { channel: 'facebook', propId: p.id });
      }

      const fbUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(targetUrl)}`;
      const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
      if (isMobile) {
        window.location.href = fbUrl;
      } else {
        window.open(fbUrl, '_blank', 'width=600,height=550');
      }
      showToast('🚀 เปิดหน้าต่างแชร์ Facebook เรียบร้อย');
    }

    function copyFacebookPost() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const safePropId = encodeURIComponent(p.id);
      const targetUrl = `${getBaseUrl()}?view=client&property=${safePropId}&ref=${ref}&src=facebook`;

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

      copyTextToClipboard(postText, '📋 คัดลอกโพสต์ขาย Facebook Marketplace สำเร็จ!');
      closeShareModal();
    }

    function copyTikTokBioCaption() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const safePropId = encodeURIComponent(p.id);
      const targetUrl = `${getBaseUrl()}?view=client&property=${safePropId}&ref=${ref}&src=tiktok`;

      const title = (typeof getDisplayTitle === 'function' ? getDisplayTitle(p) : (p.title || `ทรัพย์ NPA #${p.id}`));
      const price = p.price || '';
      const loc = p.location || '';

      const caption = `🏡 ${title} ราคาดีมาก ${price} (${loc}) กู้ได้เต็ม 100% 📍 พิกัด & ดูรูปจริงกดลิงก์หน้าโปรไฟล์: ${targetUrl}`;

      copyTextToClipboard(caption, '📋 คัดลอกแคปชั่นสำหรับ TikTok / Reels สำเร็จ!');
      closeShareModal();
    }

    function shareViaSystemNative() {
      const p = getSharePropertyObject();
      if (!p) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const safePropId = encodeURIComponent(p.id);
      const targetUrl = `${getBaseUrl()}?view=client&property=${safePropId}&ref=${ref}&src=native_share`;

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
          if (err && err.name === 'AbortError') {
            // User canceled / dismissed share dialog - do not show error
            return;
          }
          console.warn('Native share error, fallback to LINE:', err);
          shareDirectToLine();
        });
      } else {
        // Fallback to LINE
        shareDirectToLine();
      }
    }

    function copyChannelLink(channel) {
      if (!currentShareProp) return;
      const refInput = document.getElementById('agent-ref-input');
      const rawRef = refInput ? refInput.value.trim() : 'S90';
      const ref = encodeURIComponent(rawRef || 'S90');
      const safePropId = encodeURIComponent(currentShareProp.id);
      const targetUrl = `${getBaseUrl()}?view=client&prop=${safePropId}&ref=${ref}&src=${channel}`;
      
      // Automated Point Trigger: Smart Share Activity (+5 points)
      if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && rawRef) {
        window.SiwasupAgents.award(rawRef, 'smart_share_click', { channel: channel, propId: currentShareProp.id });
      }

      const channelThai = channel === 'facebook' ? 'Facebook' 
                        : channel === 'tiktok' ? 'TikTok' 
                        : channel === 'line' ? 'LINE' 
                        : channel === 'qr_sign' ? 'QR Code' 
                        : 'ทั่วไป';
      copyTextToClipboard(targetUrl, `✅ คัดลอกลิงก์สำหรับ ${channelThai} แล้ว (ล็อกสิทธิ์ ${rawRef} • +5 แต้มกิจกรรม)`);
      closeShareModal();
    }'''

def patch_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    start_marker = '    // --- SMART SHARE CENTER FUNCTIONS ---'
    end_marker = '    function toggleQrView() {'
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)
    
    if start_pos == -1 or end_pos == -1:
        print(f'Error finding markers in {filename}')
        return False
        
    updated = content[:start_pos] + new_code + '\n\n' + content[end_pos:]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(updated)
    print(f'Successfully updated {filename}')
    return True

if __name__ == '__main__':
    base_dir = r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os'
    patch_file(os.path.join(base_dir, 'catalog.html'))
    patch_file(os.path.join(base_dir, 'index.html'))
