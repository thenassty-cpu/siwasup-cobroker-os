// ==============================================================================
// 🏢 SIWASUP CO-BROKER OS - MODAL & OVERLAY COMPONENTS
// Module: modals.js
// Extracted to optimize token usage and separate UI templates from business logic.
// All modals use .modal-backdrop, .modal-card, and .capsule-glass-20 global CSS utilities.
// ==============================================================================

(function() {
  const modalHTML = `
    <!-- Booking Modal -->
    <div id="booking-modal" class="hidden modal-backdrop">
      <div class="modal-card space-y-4">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="file-text" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>แจ้งหลักฐานการจอง (วางมัดจำ)</span>
          </h3>
          <button 
            type="button" 
            onclick="closeBookingModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div id="booking-property-info" class="bg-gray-50 p-2.5 rounded-lg text-xs space-y-1"></div>
        <form onsubmit="handleBookingSubmit(event)" class="space-y-3 text-xs">
          <div>
            <label class="block font-medium mb-1">ชื่อเอเจนต์ผู้พาจอง <span class="text-red-500">*</span></label>
            <input type="text" required placeholder="เช่น คุณกานต์ หรือ บัวไหล" class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-red-500 outline-none">
          </div>
          <div>
            <label class="block font-medium mb-1">เบอร์โทรเอเจนต์ <span class="text-red-500">*</span></label>
            <input type="tel" required placeholder="08x-xxx-xxxx" class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-red-500 outline-none">
          </div>
          <div>
            <label class="block font-medium mb-1">ชื่อลูกค้าผู้จอง <span class="text-red-500">*</span></label>
            <input type="text" required placeholder="เช่น คุณสมชาย (นัดทำสัญญา 15 ต.ค.)" class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-red-500 outline-none">
          </div>
          <div>
            <label class="block font-medium mb-1">แนบสลิปเงินมัดจำ (เข้าบัญชีเจี๊ยบ) <span class="text-red-500">*</span></label>
            <input type="file" accept="image/*" class="w-full border rounded-lg p-2 bg-gray-50">
            <p class="text-[10px] text-gray-400 mt-0.5">ยอดมัดจำขั้นต่ำ 10,000 บาท</p>
          </div>
          <button type="submit" class="w-full bg-[#8B0000] hover:bg-[#6B0000] text-white font-bold py-2.5 rounded-lg text-sm shadow-xs flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="check" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ยืนยันส่งข้อมูลให้แอดมิน (เจี๊ยบ/บัว) ตรวจสอบ</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Smart Share Center Modal (Omni-Channel Share) -->
    <div id="share-modal" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6 sm:!p-4 z-50" onclick="if(event.target === this) closeShareModal()">
      <div id="share-modal-card" class="modal-card no-scrollbar w-full max-w-md transition-all duration-300 p-4 sm:p-5 my-auto overflow-hidden">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5 mb-2.5">
          <h3 class="font-bold text-sm sm:text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5 bg-amber-50 text-amber-700 border border-amber-200"><i data-lucide="share-2" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>Smart Share Center</span>
            <span class="text-[10px] text-amber-800 font-normal hidden sm:inline">(เลือกลิงก์โปรโมท)</span>
          </h3>
          <button 
            type="button" 
            onclick="closeShareModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <!-- Adaptive Layout: Side-by-Side on Desktop/Tablet if QR open -->
        <div class="flex flex-col md:flex-row items-stretch">
          
          <!-- Left Column: Channel Links & Controls (LOCKED FIXED WIDTH: 380px) -->
          <div class="w-full md:w-[380px] md:shrink-0 space-y-2 text-xs">
            
            <!-- Property Info Badge -->
            <div id="share-prop-info" class="bg-amber-50/80 border border-amber-200/80 p-2 rounded-lg text-xs"></div>

            <!-- Agent Ref Input with Autocomplete (125 Agents: S02-S126) -->
            <div class="relative">
              <div class="flex justify-between items-center mb-1">
                <label class="font-medium text-[11px] text-gray-700 flex items-center gap-1.5">
                  <span class="icon-circle w-3.5 h-3.5 bg-slate-100"><i data-lucide="user" class="w-2 h-2 stroke-[1.5]"></i></span>
                  <span>รหัสเอเจนต์ของคุณ (ล็อกสิทธิ์ 5%):</span>
                </label>
                <div class="flex items-center gap-1">
                  <span id="agent-tier-badge" class="text-[9.5px] text-amber-800 font-bold bg-amber-50 px-1.5 py-0.2 rounded border border-amber-200">
                    🥇 S22 - เจ็ม
                  </span>
                  <span class="text-[9px] text-emerald-600 font-medium">จำค่า 60 วัน</span>
                </div>
              </div>
              <div class="relative">
                <input type="text" id="agent-ref-input" value="S22" 
                       placeholder="พิมพ์รหัส S02-S126 หรือชื่อเล่น..."
                       oninput="handleAgentAutocomplete(this.value)"
                       onfocus="handleAgentAutocomplete(this.value)"
                       autocomplete="off"
                       class="w-full border rounded-lg py-1.5 pl-8 pr-7 text-xs font-semibold focus:ring-2 focus:ring-amber-500 outline-none bg-gray-50">
                <span class="absolute left-2.5 top-2 text-gray-400">
                  <i data-lucide="search" class="w-3.5 h-3.5"></i>
                </span>
                <button type="button" onclick="clearAgentInput()" class="absolute right-2 top-1.5 text-gray-400 hover:text-gray-600 text-xs font-bold">&times;</button>
              </div>

              <!-- Autocomplete Dropdown List -->
              <div id="agent-autocomplete-dropdown" class="hidden absolute left-0 right-0 top-full mt-1 bg-white border border-gray-200 rounded-xl shadow-xl z-50 max-h-48 overflow-y-auto no-scrollbar py-1"></div>
            </div>

            <!-- Channel Links Header -->
            <div class="font-bold text-gray-700 text-[11px] flex justify-between items-center px-0.5 pt-0.5">
              <span>กดคัดลอกลิงก์เฉพาะช่องทาง:</span>
              <span class="text-[9px] text-gray-400">เลือกลิงก์ที่ต้องการ</span>
            </div>

            <!-- Channel 1: Facebook -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-blue-200 bg-blue-50/60 hover:bg-blue-50 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs shadow-2xs">f</span>
                <div class="truncate">
                  <div class="font-bold text-blue-950 text-xs">Facebook (Marketplace / โพสต์)</div>
                  <div class="text-[10px] text-blue-700 truncate">ดักจับ Lead จากโพสต์ & แคปชั่น FB</div>
                </div>
              </div>
              <button onclick="copyChannelLink('facebook')" class="shrink-0 ml-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-1 px-2.5 rounded text-[11px] shadow-xs active:scale-95 transition-all">
                คัดลอกลิงก์
              </button>
            </div>

            <!-- Channel 2: TikTok / Reels -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-gray-300 bg-gray-50 hover:bg-gray-100/70 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-gray-900 text-white flex items-center justify-center font-bold text-xs shadow-2xs">♪</span>
                <div class="truncate">
                  <div class="font-bold text-gray-950 text-xs">TikTok / Reels / Shorts</div>
                  <div class="text-[10px] text-gray-600 truncate">สำหรับแปะ Bio หรือใต้คอมเมนต์คลิป</div>
                </div>
              </div>
              <button onclick="copyChannelLink('tiktok')" class="shrink-0 ml-2 bg-gray-900 hover:bg-black text-white font-medium py-1 px-2.5 rounded text-[11px] shadow-xs active:scale-95 transition-all">
                คัดลอกลิงก์
              </button>
            </div>

            <!-- Channel 3: LINE -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-emerald-200 bg-emerald-50/60 hover:bg-emerald-50 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-xs shadow-2xs">L</span>
                <div class="truncate">
                  <div class="font-bold text-emerald-950 text-xs">LINE (แชตส่วนตัว / ส่งกลุ่ม)</div>
                  <div class="text-[10px] text-emerald-700 truncate">ส่งต่อให้คนรู้จัก หรือกลุ่มนักลงทุน</div>
                </div>
              </div>
              <button onclick="copyChannelLink('line')" class="shrink-0 ml-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-1 px-2.5 rounded text-[11px] shadow-xs active:scale-95 transition-all">
                คัดลอกลิงก์
              </button>
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
              <button onclick="copyChannelLink('web')" class="shrink-0 ml-2 bg-gray-800 hover:bg-gray-900 text-white font-medium py-1 px-2.5 rounded text-[11px] shadow-xs active:scale-95 transition-all">
                คัดลอกลิงก์
              </button>
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
              <button onclick="toggleQrView()" class="shrink-0 ml-2 bg-neutral-900 hover:bg-neutral-800 text-white font-medium py-1 px-3 rounded text-[11px] shadow-xs flex items-center gap-1 active:scale-95 transition-all">
                <i data-lucide="scan-line" class="w-3 h-3"></i>
                <span id="qr-toggle-text">เปิดดู QR</span>
              </button>
            </div>
          </div>

          <!-- Right Column: Desktop/Tablet Side QR Panel (Smooth Sliding Drawer) -->
          <div id="desktop-qr-panel" class="hidden md:flex flex-col transition-all duration-300 ease-out overflow-hidden max-w-0 opacity-0 pointer-events-none self-stretch">
            <div class="w-56 shrink-0 h-full flex flex-col items-center justify-between p-3 bg-gradient-to-b from-amber-50/70 to-slate-50 border border-amber-200/80 rounded-xl text-center ml-3">
              <div class="w-full">
                <div class="text-[11px] font-bold text-gray-800 mb-1.5 flex items-center justify-center gap-1">
                  <i data-lucide="qr-code" class="w-3 h-3 text-amber-600"></i>
                  <span>QR ป้ายหน้าบ้าน</span>
                </div>
                <div class="bg-white p-2 rounded-lg border border-gray-200 shadow-xs mb-1.5 inline-block">
                  <img id="qr-image-desktop" src="" alt="QR Code" class="w-32 h-32 object-contain">
                </div>
                <div>
                  <span class="inline-block text-[9px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-medium border border-emerald-200">
                    ✓ ล็อกสิทธิ์ 60 วัน
                  </span>
                </div>
              </div>
              <div class="w-full space-y-1.5 mt-2">
                <button onclick="downloadQrImage()" class="w-full bg-neutral-900 hover:bg-neutral-800 text-white font-medium py-1.5 px-2 rounded text-[10px] shadow-2xs flex items-center justify-center gap-1 transition-all active:scale-95">
                  <i data-lucide="download" class="w-2.5 h-2.5"></i>
                  <span>บันทึกรูป QR</span>
                </button>
                <button onclick="copyChannelLink('qr_sign')" class="w-full bg-white hover:bg-slate-100 text-gray-700 border border-gray-300 font-medium py-1.5 px-2 rounded text-[10px] shadow-2xs flex items-center justify-center gap-1 transition-all active:scale-95">
                  <i data-lucide="copy" class="w-2.5 h-2.5"></i>
                  <span>คัดลอกลิงก์ QR</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Dedicated QR Code Sub-Modal (Popup ซ้อนขึ้นมาแบบคลีน ไม่มี Scrollbar) -->
    <div id="mobile-qr-modal" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6 z-[60]" onclick="if(event.target === this) closeMobileQrModal()">
      <div class="modal-card-sm no-scrollbar space-y-3 text-center bg-white border border-amber-200 shadow-2xl p-4 rounded-2xl max-w-[320px] mx-auto animate-fadeIn">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="font-bold text-xs text-gray-800 flex items-center gap-1.5 text-left">
            <span class="icon-circle w-5 h-5 bg-amber-50 text-amber-700 border border-amber-200">
              <i data-lucide="qr-code" class="w-3 h-3 stroke-[1.5]"></i>
            </span>
            <span>QR Code สำหรับสแกน</span>
          </div>
          <button 
            type="button" 
            onclick="closeMobileQrModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div id="mobile-qr-prop-info" class="text-left bg-slate-50 border border-slate-200 p-2 rounded-lg text-[11px] space-y-0.5"></div>

        <div class="bg-amber-50/60 p-3 rounded-xl border border-amber-200/70 inline-block shadow-inner my-1">
          <img id="qr-image-mobile" src="" alt="QR Code" class="w-44 h-44 object-contain bg-white p-2 rounded-lg border border-gray-200 shadow-sm mx-auto">
        </div>

        <div>
          <span class="inline-block text-[10px] bg-emerald-100 text-emerald-800 px-2.5 py-0.5 rounded-full font-medium border border-emerald-200">
            ✓ สแกนแล้วระบบล็อกสิทธิ์เอเจนต์ 60 วัน
          </span>
          <p class="text-[10px] text-gray-400 mt-1">แตะค้างที่รูปเพื่อบันทึก หรือกดปุ่มด้านล่าง</p>
        </div>

        <div class="grid grid-cols-2 gap-2 pt-1">
          <button onclick="downloadQrImage()" class="bg-neutral-900 hover:bg-neutral-800 text-white font-medium py-2 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1 active:scale-95 transition-all">
            <i data-lucide="download" class="w-3.5 h-3.5"></i>
            <span>บันทึกรูป QR</span>
          </button>
          <button onclick="copyChannelLink('qr_sign')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium py-2 px-2 rounded-xl text-xs border border-slate-200 shadow-xs flex items-center justify-center gap-1 active:scale-95 transition-all">
            <i data-lucide="copy" class="w-3.5 h-3.5"></i>
            <span>คัดลอกลิงก์</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Client Call Discount Modal (Click to Call) -->
    <div id="call-modal" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6">
      <div class="modal-card-sm space-y-3 text-center">
        <div class="icon-circle w-12 h-12 bg-amber-900/60 text-[#C2A460] mx-auto">
          <i data-lucide="gift" class="w-6 h-6 stroke-[1.5]"></i>
        </div>
        <h3 class="font-bold text-base text-gray-900">รับสิทธิพิเศษสำหรับคุณ!</h3>
        <p class="text-xs text-gray-600">
          แจ้งรหัสอ้างอิงนี้กับเจ้าหน้าที่ฝ่ายขาย เพื่อรับ <strong class="text-[#990000]">สิทธิ์ฟรีค่าโอนกรรมสิทธิ์ / ส่วนลดพิเศษ</strong>
        </p>
        <div class="bg-amber-50 border-2 border-dashed border-amber-300 rounded-xl p-2.5 text-center">
          <span class="text-[11px] text-amber-800">รหัสส่วนลดของคุณ:</span>
          <div id="call-discount-code" class="text-xl font-extrabold text-amber-900 tracking-wider">SS-09</div>
        </div>
        <div class="pt-2 flex gap-2">
          <a id="btn-actual-call" href="tel:0944629796" onclick="logCallLead()" class="flex-1 bg-siwasup-gold hover:opacity-95 text-gray-950 font-bold py-2.5 rounded-xl text-xs shadow-xs text-center flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="phone" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>โทรติดต่อเจ้าหน้าที่ทันที</span>
          </a>
          <button onclick="closeCallModal()" class="px-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-xl text-xs border border-gray-200">
            ปิด
          </button>
        </div>
      </div>
    </div>

    <!-- Client Inquiry Modal (Appointment / Callback) -->
    <div id="inquiry-modal" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6">
      <div class="modal-card-sm space-y-3">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="calendar" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>ขอนัดหมายเข้าชมห้องจริง / ปรึกษาสินเชื่อ</span>
          </h3>
          <button 
            type="button" 
            onclick="closeInquiryModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div id="inquiry-prop-info" class="bg-gray-50 p-2 rounded-lg text-xs font-medium text-gray-700"></div>
        <form onsubmit="handleInquirySubmit(event)" class="space-y-2.5 text-xs">
          <div>
            <label class="block font-medium mb-1">ชื่อของคุณ <span class="text-red-500">*</span></label>
            <input type="text" id="inquiry-name" required placeholder="เช่น คุณวิชัย" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
          </div>
          <div>
            <label class="block font-medium mb-1">เบอร์โทรศัพท์ติดต่อสะดวก <span class="text-red-500">*</span></label>
            <input type="tel" id="inquiry-phone" required placeholder="08x-xxx-xxxx" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
          </div>
          <div>
            <label class="block font-medium mb-1">วันที่สะดวกเข้าชม (โดยประมาณ)</label>
            <input type="text" id="inquiry-date" placeholder="เช่น เสาร์นี้ ช่วงบ่าย" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
          </div>
          <button type="submit" class="w-full bg-[#C2A460] hover:bg-[#A98B45] text-neutral-900 font-bold py-2.5 rounded-xl shadow-xs text-xs mt-2 flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ยืนยันส่งข้อมูลนัดหมาย</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Admin Notification Toast (Simulate 1-Click Approval) -->
    <div id="admin-toast" class="hidden fixed top-4 inset-x-4 max-w-sm mx-auto z-50 bg-gray-900 text-white p-3 rounded-xl shadow-2xl border border-gray-700 text-xs space-y-2 border-l-4 border-amber-400">
      <div class="flex items-center justify-between font-bold text-amber-300">
        <span class="flex items-center gap-1.5">
          <span class="icon-circle w-4 h-4"><i data-lucide="bell" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
          <span>แจ้งเตือนแอดมิน (เจี๊ยบ/บัว)</span>
        </span>
        <span class="text-[10px] text-gray-400">เมื่อสักครู่</span>
      </div>
      <p id="admin-toast-body" class="text-gray-200 text-[11px]"></p>
      <div class="flex gap-2 pt-1">
        <button onclick="adminApproveBooking()" class="flex-1 bg-[#C2A460] hover:bg-[#c49f2b] text-gray-950 font-bold py-1.5 rounded text-center shadow-xs flex items-center justify-center gap-1.5">
          <span class="icon-circle w-4 h-4"><i data-lucide="check" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
          <span>กดอนุมัติการจอง (1-Click)</span>
        </button>
        <button onclick="document.getElementById('admin-toast').classList.add('hidden')" class="px-3 bg-gray-800 text-gray-300 rounded border border-gray-700">
          ปิด
        </button>
      </div>
    </div>

    <!-- 🏷️ Public Consignment / Trainee Challenge Modal (ฝากขายทรัพย์ฟรี) -->
    <div id="consign-modal" class="hidden modal-backdrop">
      <div class="modal-card space-y-3.5">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div>
            <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5" id="consign-modal-title">
              <span class="icon-circle w-5 h-5"><i data-lucide="building" class="w-3 h-3 stroke-[1.5]"></i></span>
              <span>ฝากขายบ้าน/คอนโด/ที่ดิน กับศิวาทรัพย์</span>
            </h3>
            <p class="text-[10px] text-emerald-600 font-semibold" id="consign-modal-sub">
              ฟรี! ไม่มีค่าแรกเข้า • เข้าถึงเครือข่ายเอเจนต์ทั่วประเทศ
            </p>
          </div>
          <button 
            type="button" 
            onclick="closeConsignModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="bg-amber-50 border border-amber-200 p-2.5 rounded-lg text-[11px] text-amber-900 leading-snug">
          <span class="icon-circle w-3.5 h-3.5 inline-flex mr-1 align-middle"><i data-lucide="sparkles" class="w-2 h-2 stroke-[1.5]"></i></span>
          <strong>สิทธิประโยชน์พิเศษ:</strong> หลังลงทะเบียน เจ้าหน้าที่จะติดต่อประเมินราคา และท่านสามารถเลือกรับสิทธิ์เป็น <strong>Free Agent</strong> เพื่อรับค่าคอมมิชชั่นของตัวเองเต็มๆ ได้ทันที!
        </div>

        <form onsubmit="handleConsignSubmit(event)" class="space-y-2.5 text-xs">
          <div>
            <label class="block font-medium mb-1">ประเภททรัพย์ <span class="text-red-500">*</span></label>
            <select id="consign-type" required class="w-full border rounded-lg p-2 bg-gray-50 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
              <option value="ทาวน์โฮม">ทาวน์โฮม / ทาวน์เฮ้าส์</option>
              <option value="บ้านเดี่ยว">บ้านเดี่ยว / บ้านแฝด</option>
              <option value="คอนโด">คอนโดมิเนียม</option>
              <option value="ที่ดิน">ที่ดินเปล่า</option>
              <option value="อาคารพาณิชย์">อาคารพาณิชย์ / ตึกแถว</option>
            </select>
          </div>

          <div>
            <label class="block font-medium mb-1">ชื่อโครงการ / ทำเล / ซอย / ถนน <span class="text-red-500">*</span></label>
            <input type="text" id="consign-title" required placeholder="เช่น ม.พฤกษา 12 คลองสาม ปทุมธานี" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block font-medium mb-1">ราคาที่ต้องการขาย (บาท) <span class="text-red-500">*</span></label>
              <input type="number" id="consign-price" required placeholder="เช่น 2500000" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
            </div>
            <div>
              <label class="block font-medium mb-1">ขนาดพื้นที่ (ตร.ว. / ตร.ม.)</label>
              <input type="text" id="consign-size" placeholder="เช่น 24 ตร.ว." class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block font-medium mb-1">ชื่อเจ้าของทรัพย์ / ผู้ส่ง <span class="text-red-500">*</span></label>
              <input type="text" id="consign-name" required placeholder="เช่น คุณสมบัติ" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
            </div>
            <div>
              <label class="block font-medium mb-1">เบอร์โทรศัพท์ <span class="text-red-500">*</span></label>
              <input type="tel" id="consign-phone" required placeholder="08x-xxx-xxxx" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900">
            </div>
          </div>

          <div>
            <label class="block font-medium mb-1">แนบรูปถ่ายทรัพย์ / โฉนด (ถ้ามี)</label>
            <input type="file" accept="image/*" class="w-full border rounded-lg p-1.5 bg-gray-50 text-[11px]">
            <p class="text-[10px] text-gray-400 mt-0.5">แนบรูปช่วยให้ประเมินราคาและปล่อยขายได้ไวยิ่งขึ้น</p>
          </div>

          <button type="submit" class="w-full bg-[#C2A460] hover:bg-[#A98B45] text-neutral-900 font-bold py-2.5 rounded-xl shadow-xs text-xs mt-2 flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ยืนยันส่งข้อมูลฝากขาย (ฟรี)</span>
          </button>
        </form>
      </div>
    </div>

    <!-- 🤝 Member Get Member (MGM) Referral Modal -->
    <div id="mgm-modal" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6">
      <div class="modal-card-sm space-y-3.5">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="users" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>ชวนเพื่อนมาเป็น Agent (MGM)</span>
          </h3>
          <button 
            type="button" 
            onclick="closeMgmModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="bg-gray-50 border border-gray-200 p-2.5 rounded-xl text-xs space-y-1 text-gray-800 border-l-4 border-[#C2A460]">
          <div class="font-bold flex items-center gap-1.5 text-gray-900">
            <span class="icon-circle w-4 h-4"><i data-lucide="coins" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>สิทธิประโยชน์ผู้ชวน:</span>
          </div>
          <p class="text-[11px] leading-relaxed text-gray-600">
            1. รับ <strong class="text-[#990000]">100 แต้มสะสม</strong> เมื่อเพื่อนส่งทรัพย์ครบ 3 หลัง<br>
            2. รับ <strong class="text-[#990000]">ค่าบริหารทีม 0.5% (Overriding)</strong> จากยอดขายทุกดีลที่เพื่อนปิดได้ตลอดชีพ!
          </p>
        </div>

        <div class="space-y-1 text-xs">
          <label class="block font-medium text-gray-700">ลิงก์ชวนเพื่อนของคุณ (ฝังรหัสตัวแทน):</label>
          <div class="flex gap-1.5">
            <input type="text" id="mgm-link-input" readonly value="https://thenassty-cpu.github.io/siwasup-cobroker-os/?join_ref=AG-บัวรา" 
                   class="flex-1 bg-gray-100 border rounded-lg px-2.5 py-1.5 text-[11px] font-mono text-gray-700 outline-none">
            <button onclick="copyMgmLink()" class="bg-neutral-900 hover:bg-neutral-800 text-white font-bold px-3 py-1.5 rounded-lg text-xs whitespace-nowrap shadow-xs flex items-center gap-1 active:scale-95 transition-all">
              <span class="icon-circle w-3.5 h-3.5"><i data-lucide="copy" class="w-2 h-2 stroke-[1.5]"></i></span>
              <span>คัดลอก</span>
            </button>
          </div>
        </div>

        <!-- MGM QR Code -->
        <div class="text-center p-2 bg-gray-50 rounded-xl border border-gray-200 space-y-1">
          <div class="text-[10px] text-gray-500 font-medium">ให้เพื่อนสแกน QR สมัครทันที</div>
          <img id="mgm-qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=140x140&data=https://thenassty-cpu.github.io/siwasup-cobroker-os/?join_ref=AG-%E0%B8%9A%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B8%B2" 
               alt="MGM QR" class="w-32 h-32 mx-auto border p-1 bg-white rounded-lg shadow-xs">
        </div>
      </div>
    </div>

    <!-- 💬 Homerun-Style "เสนอราคา" (Submit Offer) Modal -->
    <div id="offer-modal" onclick="if(event.target === this) closeOfferModal()" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6 sm:!p-4 z-50">
      <div class="modal-card max-w-2xl space-y-3.5 max-h-[82dvh] sm:max-h-[88dvh] overflow-y-auto custom-scrollbar !p-4 sm:!p-5 bg-white rounded-3xl shadow-2xl border border-neutral-200/80">
        
        <!-- Sticky Header with Digital Luxury Theme & Pinned Close Button -->
        <div class="sticky top-0 z-20 flex justify-between items-center bg-white/95 backdrop-blur-md border-b border-neutral-200/80 pb-3 -mt-1 pt-1">
          <div class="flex items-center gap-2.5">
            <span class="w-8 h-8 rounded-xl bg-gradient-to-br from-[#8B0000] to-[#5A0000] text-[#E5C985] flex items-center justify-center shadow-xs border border-[#C2A460]/40 shrink-0">
              <i data-lucide="badge-dollar-sign" class="w-4 h-4 stroke-[2]"></i>
            </span>
            <div>
              <h3 class="font-bold text-base text-neutral-900 leading-tight flex items-center gap-2">
                <span>ยื่นเสนอราคา</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-[#FAF7F2] text-[#8C734B] border border-[#DFD3C3] font-semibold">Fast Offer System</span>
              </h3>
              <p class="text-[11px] text-neutral-500">กรอกราคาที่ต้องการเสนอและข้อมูลติดต่อเพื่อดำเนินการยื่นข้อเสนอซื้อ</p>
            </div>
          </div>
          <button 
            type="button" 
            onclick="closeOfferModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <i data-lucide="x" class="w-5 h-5 stroke-[2.5]"></i>
          </button>
        </div>

        <!-- Property Summary Banner (Luxury Warm Alabaster) -->
        <div id="offer-prop-info" class="bg-[#FAF9F6] border border-neutral-200/90 p-3 rounded-2xl text-xs space-y-1"></div>

        <form id="homerun-offer-form" onsubmit="handleOfferSubmit(event)" class="grid grid-cols-1 md:grid-cols-12 gap-4 text-xs" novalidate>
          <!-- Left Column: Offer Price & Buyer Details -->
          <div class="md:col-span-7 space-y-3">
            <!-- รูปแบบที่ต้องการซื้อ (เงินสด / สินเชื่อ) -->
            <div>
              <label class="block font-bold text-neutral-700 mb-1.5">รูปแบบที่ต้องการซื้อ <span class="text-red-500">*</span></label>
              <div class="grid grid-cols-2 gap-2">
                <label class="cursor-pointer">
                  <input type="radio" name="offer_PurchaseType" value="เงินสด" checked class="peer sr-only" onchange="updateOfferSummaryBox()">
                  <div class="p-2.5 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] font-bold text-center transition-all flex items-center justify-center gap-1.5 shadow-2xs">
                    <i data-lucide="banknote" class="w-4 h-4"></i>
                    <span>ซื้อเงินสด</span>
                  </div>
                </label>
                <label class="cursor-pointer">
                  <input type="radio" name="offer_PurchaseType" value="สินเชื่อธนาคาร" class="peer sr-only" onchange="updateOfferSummaryBox()">
                  <div class="p-2.5 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] font-bold text-center transition-all flex items-center justify-center gap-1.5 shadow-2xs">
                    <i data-lucide="landmark" class="w-4 h-4"></i>
                    <span>ขอสินเชื่อ</span>
                  </div>
                </label>
              </div>
            </div>

            <!-- ราคาที่ต้องการเสนอ (ให้ใส่ราคาอย่างอิสระ ไม่แสดงตัวเลขเพดาน 50% ให้ติดตา) -->
            <div>
              <div class="flex justify-between items-baseline mb-1">
                <label class="font-bold text-neutral-700">ราคาที่ต้องการเสนอซื้อ (บาท) <span class="text-red-500">*</span></label>
                <span id="offer-discount-percent" class="text-[11px] font-semibold text-emerald-700"></span>
              </div>
              <div class="relative">
                <input type="text" id="offer-amount-input" required placeholder="เช่น 2,850,000" 
                       class="w-full border border-neutral-200 rounded-xl p-2.5 pl-8 text-base font-extrabold text-[#8B0000] outline-none focus:ring-1 focus:ring-[#C2A460] focus:border-[#C2A460] transition font-mono bg-white"
                       oninput="formatCurrencyInput(this); updateOfferSummaryBox();">
                <span class="absolute left-3 top-3 text-neutral-400 font-bold">฿</span>
              </div>
              
              <!-- ข้อความช่วยเหลือ & กล่องแจ้งเตือนเมื่อลดเกิน 50% (จะ disable ปุ่มส่งทันที) -->
              <div class="mt-1.5 space-y-1">
                <p id="offer-price-hint" class="text-[10.5px] text-neutral-400">
                  ระบุราคาที่ต้องการเสนอซื้ออย่างอิสระ ระบบจะประเมินความเป็นไปได้อัตโนมัติ
                </p>
                <div id="offer-exceed-warning" class="hidden p-2.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-[11px] flex items-center gap-2 font-medium">
                  <i data-lucide="alert-circle" class="w-4 h-4 shrink-0 text-rose-600"></i>
                  <span>ราคาที่เสนอซื้อต่ำกว่าเกณฑ์การพิจารณาเบื้องต้น กรุณาระบุราคาเสนอซื้อใหม่</span>
                </div>
              </div>
            </div>

            <!-- วางเงินมัดจำจะซื้อจะขาย -->
            <div class="p-3 rounded-xl bg-[#FAF9F6] border border-neutral-200/80 space-y-1.5">
              <div class="flex justify-between items-center text-xs">
                <span class="font-bold text-neutral-700 flex items-center gap-1">
                  <i data-lucide="shield-check" class="w-3.5 h-3.5 text-[#C2A460]"></i>
                  <span>เงินมัดจำทำสัญญาจะซื้อจะขาย</span>
                </span>
                <span id="offer-deposit-display" class="font-bold text-[#8B0000] font-mono">฿50,000</span>
              </div>
              <p class="text-[10px] text-neutral-500 leading-tight">
                * วางมัดจำเข้าบัญชีนิติบุคคล <strong>บจก. ศิวาทรัพย์ แอสเซท</strong> เพื่อล็อกสิทธิ์และทำสัญญาจะซื้อจะขายอย่างเป็นทางการ
              </p>
            </div>

            <!-- ข้อมูลผู้เสนอซื้อ -->
            <div class="space-y-2 pt-1 border-t border-neutral-100">
              <div class="font-bold text-neutral-800 text-xs flex items-center gap-1.5">
                <i data-lucide="user" class="w-3.5 h-3.5 text-neutral-500"></i>
                <span>ข้อมูลผู้เสนอซื้อ</span>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <div>
                  <label class="block text-[11px] font-medium text-neutral-600 mb-0.5">ชื่อ-นามสกุล <span class="text-red-500">*</span></label>
                  <input type="text" id="offer-buyer-name" required placeholder="เช่น คุณสมชาย มุ่งมั่น" class="w-full border border-neutral-200 rounded-xl p-2 text-xs outline-none focus:ring-1 focus:ring-[#C2A460] focus:border-[#C2A460] bg-white">
                </div>
                <div>
                  <label class="block text-[11px] font-medium text-neutral-600 mb-0.5">เบอร์โทรศัพท์ <span class="text-red-500">*</span></label>
                  <input type="tel" id="offer-buyer-phone" required placeholder="08x-xxx-xxxx" class="w-full border border-neutral-200 rounded-xl p-2 text-xs outline-none focus:ring-1 focus:ring-[#C2A460] focus:border-[#C2A460] bg-white">
                </div>
              </div>
              <div>
                <label class="block text-[11px] font-medium text-neutral-600 mb-0.5">LINE ID / ช่องทางติดต่อเพิ่มเติม (ถ้ามี)</label>
                <input type="text" id="offer-buyer-line" placeholder="เช่น somchai_line" class="w-full border border-neutral-200 rounded-xl p-2 text-xs outline-none focus:ring-1 focus:ring-[#C2A460] focus:border-[#C2A460] bg-white">
              </div>
              <div>
                <label class="block text-[11px] font-medium text-neutral-600 mb-0.5">เงื่อนไขเพิ่มเติม / วันที่สะดวกโอนกรรมสิทธิ์</label>
                <textarea id="offer-buyer-note" rows="2" placeholder="เช่น ขอตรวจโครงสร้างบ้านก่อนโอน หรือต้องการกู้ 100%" class="w-full border border-neutral-200 rounded-xl p-2 text-xs outline-none focus:ring-1 focus:ring-[#C2A460] focus:border-[#C2A460] bg-white resize-none"></textarea>
              </div>
            </div>
          </div>

          <!-- Right Column: Offer Summary Box & Actions -->
          <div class="md:col-span-5 flex flex-col justify-between space-y-3">
            <div class="space-y-3">
              <!-- Summary Card (Digital Luxury Style) -->
              <div class="bg-[#FAF9F6] border border-[#C2A460]/40 rounded-2xl p-3.5 space-y-2.5">
                <div class="flex items-center justify-between border-b border-neutral-200/80 pb-2">
                  <span class="font-bold text-neutral-800 flex items-center gap-1.5">
                    <i data-lucide="file-check-2" class="w-4 h-4 text-[#C2A460]"></i>
                    <span>สรุปข้อเสนอซื้อ</span>
                  </span>
                  <span id="offer-summary-type-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-neutral-900 text-white">ซื้อเงินสด</span>
                </div>

                <div class="space-y-1.5 text-[11px]">
                  <div class="flex justify-between text-neutral-500">
                    <span>ราคาตั้งขายเดิม:</span>
                    <span id="offer-summary-original-price" class="font-mono line-through">-</span>
                  </div>
                  <div class="flex justify-between items-baseline">
                    <span class="font-semibold text-neutral-700">ราคาที่เสนอซื้อ:</span>
                    <span id="offer-summary-final-price" class="font-mono font-black text-sm text-[#8B0000]">-</span>
                  </div>
                  <div class="flex justify-between text-neutral-500 pt-1 border-t border-neutral-200/60">
                    <span>ส่วนต่างราคา:</span>
                    <span id="offer-summary-diff" class="font-mono font-semibold text-emerald-700">-</span>
                  </div>
                </div>

                <div class="p-2.5 rounded-xl bg-white border border-neutral-200 text-[10px] space-y-1 text-neutral-600">
                  <div class="font-bold text-neutral-800 flex items-center gap-1">
                    <i data-lucide="clock" class="w-3 h-3 text-[#C2A460]"></i>
                    <span>กระบวนการพิจารณา:</span>
                  </div>
                  <p class="leading-relaxed text-neutral-500">
                    ฝ่ายประสานงานจะนำข้อเสนอเข้าบอร์ดพิจารณาและตอบกลับผลการอนุมัติภายใน 24-48 ชั่วโมง
                  </p>
                </div>
              </div>

              <!-- Document Download Box inside Offer Modal (Role-aware) -->
              <div id="offer-modal-docs-box" class="bg-white border border-neutral-200 rounded-xl p-2.5 space-y-1.5"></div>

              <!-- 🛡️ PDPA Consent Checkbox -->
              <div class="p-2.5 rounded-xl bg-neutral-50 border border-neutral-200/80 space-y-1">
                <label class="flex items-start gap-2 text-[11px] text-neutral-600 cursor-pointer select-none">
                  <input type="checkbox" id="offer-pdpa-consent" required checked class="mt-0.5 w-3.5 h-3.5 rounded text-[#8B0000] focus:ring-[#C2A460] border-neutral-300 shrink-0">
                  <span class="leading-tight text-[10px]">
                    ยินยอมให้ บจก. ศิวาทรัพย์ แอสเซท และตัวแทนผู้ดูแล จัดเก็บข้อมูลเพื่อการนัดหมายและยื่นข้อเสนอซื้อตาม <button type="button" onclick="openPrivacyPolicyModal()" class="text-[#8B0000] underline font-semibold cursor-pointer">นโยบายความเป็นส่วนตัว (PDPA)</button>
                  </span>
                </label>
              </div>
            </div>

            <!-- Submit Button (Digital Luxury Gold) -->
            <div class="pt-1 space-y-1.5">
              <button type="submit" id="offer-submit-btn" class="w-full bg-gradient-to-r from-[#C2A460] via-[#E5CF94] to-[#A98B45] text-neutral-950 font-bold py-3 px-3 rounded-xl shadow-md text-xs flex items-center justify-center gap-2 active:scale-95 transition-all cursor-pointer hover:opacity-95">
                <i data-lucide="send" class="w-4 h-4"></i>
                <span id="offer-submit-btn-text">ยืนยันการยื่นเสนอราคา</span>
              </button>
              <p class="text-[10px] text-center text-neutral-400">ระบบจะส่งข้อเสนอเข้าแผงบริหารและแจ้งเตือนผ่าน LINE Official อัตโนมัติ</p>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- 📥 Owner Leads Management Modal (สำหรับแอดมินบัว/เจี๊ยบ) -->
    <div id="owner-leads-modal" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6">
      <div class="modal-card space-y-3.5">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="inbox" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>รายการทรัพย์ฝากขายใหม่ (Lead Magnet)</span>
          </h3>
          <button 
            type="button" 
            onclick="closeOwnerLeadsModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div id="owner-leads-container" class="space-y-2 text-xs">
          <!-- Dynamically populated -->
        </div>
      </div>
    </div>

    <!-- 💰 Edit Price Modal (สำหรับเจ้าของ/แอดมิน บัว & กูล) -->
    <div id="edit-price-modal" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6">
      <div class="modal-card-sm space-y-3.5">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="edit-3" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>แก้ไขราคาขาย (แอดมิน บัว & กูล)</span>
          </h3>
          <button 
            type="button" 
            onclick="closeEditPriceModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div id="edit-price-prop-info" class="bg-gray-50 border border-gray-200 p-2.5 rounded-xl text-xs space-y-0.5"></div>

        <form onsubmit="handleEditPriceSubmit(event)" class="space-y-3 text-xs">
          <div>
            <label class="block font-medium mb-1 text-gray-700">ราคาขายใหม่ (บาท) <span class="text-red-500">*</span></label>
            <input type="number" id="new-price-input" required placeholder="เช่น 3390000" 
                   class="w-full border-2 border-gray-300 rounded-lg p-2.5 outline-none focus:border-[#990000] focus:ring-1 focus:ring-[#990000] font-extrabold text-base text-gray-900 bg-white">
            <p class="text-[10px] text-gray-400 mt-1">ระบบจะคำนวณยอดเงินค่าคอมมิชชั่นของเอเจนต์ใหม่ให้อัตโนมัติ</p>
          </div>

          <div class="flex items-center gap-2 p-2 bg-amber-50 rounded-lg border border-amber-200">
            <input type="checkbox" id="mark-hot-deal" class="rounded text-amber-600 focus:ring-amber-500">
            <label for="mark-hot-deal" class="text-[11px] font-bold text-amber-900 cursor-pointer flex items-center gap-1.5">
              <span class="icon-circle w-3.5 h-3.5"><i data-lucide="flame" class="w-2 h-2 stroke-[1.5]"></i></span>
              <span>แปะป้าย "ลดราคาพิเศษ (Hot Deal)"</span>
            </label>
          </div>

          <button type="submit" class="w-full bg-neutral-900 hover:bg-neutral-800 text-white font-bold py-2.5 rounded-xl shadow-xs text-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <span class="icon-circle w-4 h-4"><i data-lucide="save" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>บันทึกราคาใหม่ทันที</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Instant Bundle Floating Action Bar (White 60% Glassmorphism + Satin Gold 10%) -->
    <div id="bundle-bar" class="hidden fixed bottom-0 inset-x-0 max-w-md mx-auto bg-white/95 backdrop-blur-md text-gray-900 p-3 z-40 shadow-xl flex items-center justify-between border-t-2 border-[#C2A460] border-x border-b border-gray-200 rounded-t-xl">
      <div>
        <div class="font-extrabold text-xs text-gray-900 flex items-center gap-1.5">
          <span class="icon-circle w-5 h-5"><i data-lucide="package" class="w-3 h-3 stroke-[1.5]"></i></span>
          <span>มัดรวมส่งลูกค้า (<span id="bundle-count" class="text-[#990000]">0</span> หลัง)</span>
        </div>
        <div class="text-[10px] text-gray-500">สร้างหน้าเว็บ VIP + แคปชั่นส่งในไลน์</div>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="clearBundleSelection()" class="text-[11px] text-gray-400 hover:text-gray-700 px-2 py-1">
          ล้าง
        </button>
        <button onclick="openBundleModal()" class="bg-siwasup-gold hover:opacity-95 text-gray-950 font-bold py-1.5 px-3 rounded-lg text-xs shadow-xs flex items-center gap-1.5">
          <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
          <span>ส่งลูกค้าทันที</span>
        </button>
      </div>
    </div>

    <!-- 📦 Instant Bundle Modal (มัดรวมส่งลูกค้า) -->
    <div id="bundle-modal" class="hidden modal-backdrop">
      <div class="modal-card space-y-4">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="package" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>มัดรวมส่งลูกค้า (VIP Micro-Catalog)</span>
          </h3>
          <button 
            type="button" 
            onclick="closeBundleModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div>
          <label class="block font-medium text-xs mb-1 text-gray-700 flex items-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="user" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ชื่อลูกค้าผู้รับ (ใส่เพื่อเพิ่มความประทับใจ VIP):</span>
          </label>
          <input type="text" id="bundle-client-name" value="คุณวิชัย" oninput="updateBundlePreview()"
                 placeholder="เช่น คุณวิชัย, คุณสมชาย" 
                 class="w-full border rounded-lg p-2 text-xs font-semibold focus:ring-1 focus:ring-neutral-900 focus:border-neutral-900 outline-none bg-gray-50">
        </div>

        <!-- Selected Properties List Preview -->
        <div class="space-y-1.5">
          <div class="text-xs font-bold text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="home" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>รายการทรัพย์ที่คัดสรร (<span id="bundle-modal-count">0</span> หลัง):</span>
          </div>
          <div id="bundle-selected-list" class="max-h-40 overflow-y-auto space-y-1.5 pr-1"></div>
        </div>

        <!-- Generated Text Preview for LINE -->
        <div class="space-y-1.5">
          <div class="text-xs font-bold text-gray-800 flex justify-between items-center">
            <span class="flex items-center gap-1.5">
              <span class="icon-circle w-4 h-4"><i data-lucide="message-square" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
              <span>ข้อความแคปชั่นพร้อมส่งใน LINE:</span>
            </span>
            <span class="text-[10px] text-gray-500 font-normal">จัดหน้าสวยงามพร้อมลิงก์</span>
          </div>
          <div class="bg-gray-100 border border-gray-300 rounded-lg p-2.5 text-[11px] text-gray-700 whitespace-pre-wrap font-sans leading-relaxed select-all" id="bundle-text-preview"></div>
        </div>

        <div class="grid grid-cols-2 gap-2 pt-1">
          <button onclick="copyBundleMessage()" class="bg-neutral-900 hover:bg-neutral-800 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <span class="icon-circle w-4 h-4"><i data-lucide="copy" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>คัดลอกข้อความ</span>
          </button>
          <button onclick="sendBundleToLine()" class="bg-white hover:bg-neutral-50 border border-neutral-200 hover:border-emerald-500 text-neutral-800 hover:text-emerald-700 font-bold py-2.5 px-3 rounded-xl text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <span class="w-4 h-4 rounded-full bg-[#06C755] text-white flex items-center justify-center text-[9px] font-black shrink-0">L</span>
            <span>ส่งเข้าแอป LINE</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 🖨️ Auto PDF Vinyl Sign Generator Modal -->
    <div id="vinyl-modal" class="hidden modal-backdrop">
      <div class="modal-card space-y-4 max-w-lg">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm sm:text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5 bg-amber-600"><i data-lucide="printer" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>Auto PDF Vinyl Sign Generator (ป้ายไวนิลหน้าบ้าน)</span>
          </h3>
          <button 
            type="button" 
            onclick="closeVinylModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- Live Vinyl Sign Preview Container -->
        <div class="space-y-1">
          <div class="flex justify-between items-center text-xs text-gray-500">
            <span class="font-medium">ตัวอย่างป้ายไวนิลจริง (Live Preview):</span>
            <span id="vinyl-preview-dims" class="text-[10px] bg-gray-100 text-gray-700 font-mono px-2 py-0.5 rounded">120 x 80 ซม. (3:2)</span>
          </div>
          <div class="bg-gray-900/5 p-2 rounded-xl border border-gray-200 flex items-center justify-center overflow-hidden">
            <canvas id="vinyl-canvas" class="w-full max-h-60 rounded shadow-sm object-contain bg-white"></canvas>
          </div>
        </div>

        <!-- Customization Controls -->
        <div class="space-y-2.5 text-xs">
          <!-- Preset Size Selection -->
          <!-- Preset Size Selection (Only 2 Official Master Templates) -->
          <div>
            <label class="block font-medium mb-1 text-gray-700">สัดส่วนขนาดป้าย:</label>
            <div class="grid grid-cols-2 gap-2">
              <button type="button" onclick="setVinylPreset('200x160')" id="btn-preset-200x160" class="py-2 px-2.5 rounded-xl border font-bold text-xs text-center transition-all bg-[#990000] text-white border-[#990000] shadow-xs active:scale-95">
                🔥 200 x 160 ซม.<br><span class="text-[10px] font-normal opacity-90">ป้ายขายด่วนใหญ่ (5:4 สไตล์บัว)</span>
              </button>
              <button type="button" onclick="setVinylPreset('43x49')" id="btn-preset-43x49" class="py-2 px-2.5 rounded-xl border font-medium text-xs text-center transition-all bg-white text-gray-700 border-gray-200 hover:bg-gray-50 active:scale-95">
                🏷️ 43 x 49 ซม.<br><span class="text-[10px] font-normal text-gray-400">ป้ายไซส์ S ส่งร้าน (ติดเสา/รั้ว)</span>
              </button>
            </div>
          </div>

          <!-- Section 1: Inputs for 200x160 cm (ป้ายขายด่วนใหญ่) -->
          <div id="vinyl-section-200x160" class="space-y-2">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block font-medium mb-1 text-gray-700">ข้อความพาดหัว (Horsale):</label>
                <select id="vinyl-headline" onchange="renderVinylCanvas()" class="w-full border rounded-lg p-1.5 text-xs bg-gray-50 font-bold text-[#990000]">
                  <option value="ขายด่วน">ขายด่วน (Siwasup Master)</option>
                  <option value="ขายบ้านรีโนเวท">ขายบ้านรีโนเวท</option>
                  <option value="บ้านหลุดจำนอง / NPA">บ้านหลุดจำนอง / NPA</option>
                  <option value="ขาย / ให้เช่า">ขาย / ให้เช่า</option>
                </select>
              </div>
              <div>
                <label class="block font-medium mb-1 text-gray-700">แถบเว็บ/ไลน์ (Job_Discription):</label>
                <input type="text" id="vinyl-subtitle" value="www.siwasup.com ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี  @siwasup" oninput="renderVinylCanvas()" 
                       class="w-full border rounded-lg p-1.5 text-xs outline-none focus:ring-1 focus:ring-red-700">
              </div>
            </div>
            <!-- Ticker_AgentInfo -->
            <div>
              <label class="block font-medium mb-1 text-gray-700">ข้อมูลตัวแทนประจำป้าย (Ticker_AgentInfo):</label>
              <input type="text" id="vinyl-agent-info" value="ติดต่อ: คุณเอ (ตัวแทนพื้นที่โซนบางนา) LINE ID: ของตัวแทน" oninput="renderVinylCanvas()" 
                     class="w-full border rounded-lg p-1.5 text-xs font-medium text-red-700 outline-none focus:ring-1 focus:ring-red-700 bg-red-50/30 border-red-200">
            </div>
          </div>

          <!-- Section 2: Inputs for 43x49 cm (ป้ายไซส์ S ส่งร้าน/ติดเสา) -->
          <div id="vinyl-section-43x49" class="hidden space-y-2">
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block font-medium mb-1 text-gray-700">ประเภททรัพย์ (Ticker_Asset):</label>
                <input type="text" id="vinyl-asset" value="บ้านเดี่ยวพร้อมอยู่" oninput="renderVinylCanvas()" 
                       placeholder="เช่น บ้านเดี่ยวพร้อมอยู่, ทาวน์โฮม 2 ชั้น"
                       class="w-full border rounded-lg p-1.5 text-xs font-bold text-[#8A6A1F] outline-none focus:ring-1 focus:ring-amber-600 bg-amber-50/20">
              </div>
              <div>
                <label class="block font-medium mb-1 text-gray-700">ราคาขาย (Ticker_Price):</label>
                <input type="text" id="vinyl-price" value="฿ 2,500,000" oninput="renderVinylCanvas()" 
                       placeholder="เช่น ฿ 2,500,000"
                       class="w-full border rounded-lg p-1.5 text-xs font-bold text-red-700 outline-none focus:ring-1 focus:ring-red-700 bg-red-50/20">
              </div>
            </div>
            <div>
              <label class="block font-medium mb-1 text-gray-700">รายละเอียดจุดเด่น (Ticker_Detail):</label>
              <input type="text" id="vinyl-detail" value="2 ห้องนอน 2 ห้องน้ำ ทำเลรามคำแหง" oninput="renderVinylCanvas()" 
                     placeholder="เช่น 3 ห้องนอน ทำเลพุทธมณฑลสาย 2"
                     class="w-full border rounded-lg p-1.5 text-xs font-medium text-gray-900 outline-none focus:ring-1 focus:ring-gray-700">
            </div>
          </div>

          <!-- Common Section: Agent Selection Autocomplete (125 Agents: S02-S126) -->
          <div class="relative">
            <div class="flex justify-between items-center mb-1">
              <label class="block font-medium text-gray-700">รหัสตัวแทนผู้ดูแลป้าย (ดึงเบอร์ & LINE อัตโนมัติ):</label>
              <span id="vinyl-agent-tier-tag" class="text-[9.5px] text-amber-800 font-bold bg-amber-50 px-1.5 py-0.2 rounded border border-amber-200">
                +5 แต้มเมื่อโหลด
              </span>
            </div>
            <div class="relative">
              <input type="text" id="vinyl-agent-search" value="S22" 
                     placeholder="พิมพ์รหัส S02-S126 หรือชื่อเล่น..."
                     oninput="handleVinylAgentAutocomplete(this.value)"
                     onfocus="handleVinylAgentAutocomplete(this.value)"
                     autocomplete="off"
                     class="w-full border rounded-lg p-1.5 pl-7 pr-6 text-xs bg-amber-50/40 font-bold text-gray-900 outline-none focus:ring-1 focus:ring-amber-500 border-amber-200">
              <span class="absolute left-2 top-2 text-gray-400">
                <i data-lucide="user-check" class="w-3.5 h-3.5 text-amber-600"></i>
              </span>
              <button type="button" onclick="clearVinylAgentSearch()" class="absolute right-2 top-1.5 text-gray-400 hover:text-gray-600 text-xs font-bold">&times;</button>
            </div>
            <!-- Autocomplete Dropdown List -->
            <div id="vinyl-agent-autocomplete-dropdown" class="hidden absolute left-0 right-0 top-full mt-1 bg-white border border-gray-200 rounded-xl shadow-xl z-50 max-h-40 overflow-y-auto no-scrollbar py-1"></div>
          </div>

          <!-- Contact Info (Two Phones for GraphicAdsForm parity) -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block font-medium mb-1 text-gray-700">เบอร์โทร 1 (Ticker_NumberA): <span class="text-red-500">*</span></label>
              <input type="tel" id="vinyl-phone" value="094-462-9796" oninput="renderVinylCanvas()" 
                     class="w-full border rounded-lg p-1.5 text-xs font-bold text-gray-900 outline-none focus:ring-1 focus:ring-red-700">
            </div>
            <div>
              <label class="block font-medium mb-1 text-gray-700">เบอร์โทร 2 (Ticker_NumberB):</label>
              <input type="tel" id="vinyl-phone-b" value="096-129-2459" oninput="renderVinylCanvas()" 
                     class="w-full border rounded-lg p-1.5 text-xs font-bold text-gray-900 outline-none focus:ring-1 focus:ring-red-700">
            </div>
          </div>

          <!-- Smart Auto-Fit & Font Weight Controls -->
          <div class="flex flex-wrap items-center justify-between gap-2 p-2 bg-amber-50/50 rounded-lg border border-amber-200/80">
            <label class="flex items-center gap-1.5 cursor-pointer text-gray-800 font-bold text-[11px]">
              <input type="checkbox" id="vinyl-auto-expand" checked onchange="renderVinylCanvas()" class="rounded text-[#990000] focus:ring-red-600">
              <span>✨ Auto-Fit ขยายเต็มกรอบอัตโนมัติ</span>
            </label>
            <div class="flex items-center gap-1.5">
              <span class="text-[10px] text-gray-600 font-medium">ความหนา:</span>
              <select id="vinyl-weight-mode" onchange="renderVinylCanvas()" class="border border-amber-300 rounded-md py-0.5 px-1.5 text-[11px] bg-white font-bold text-gray-800 outline-none focus:ring-1 focus:ring-amber-600">
                <option value="heavy" selected>หนาคมชัด (แนะนำ)</option>
                <option value="ultra">หนาพิเศษ (Ultra Bold)</option>
                <option value="normal">มาตรฐาน (Normal)</option>
              </select>
            </div>
          </div>

          <!-- Download Action Buttons (CTA Hierarchy: Primary Burgundy + Secondary Obsidian Outline) -->
          <div class="grid grid-cols-2 gap-2 pt-1">
            <button type="button" onclick="downloadVinylPDF()" class="bg-[#8B0000] hover:bg-[#6B0000] text-white font-bold py-2.5 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all border border-[#8B0000]">
              <span class="icon-circle w-4 h-4"><i data-lucide="download" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
              <span>โหลด PDF ส่งโรงพิมพ์</span>
            </button>
            <button type="button" onclick="downloadVinylJPG()" class="bg-transparent hover:bg-neutral-100 text-neutral-900 border border-neutral-900 font-bold py-2.5 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
              <span class="icon-circle w-4 h-4"><i data-lucide="image" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
              <span>โหลดรูป HD ส่ง LINE</span>
            </button>
          </div>
          <!-- Field Proof GPS Submission Link Button -->
          <button type="button" onclick="openVinylProofModal(activeVinylProperty ? activeVinylProperty.id : null)" class="w-full bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold py-2 px-3 rounded-xl text-xs shadow-2xs flex items-center justify-center gap-1.5 transition-all active:scale-95">
            <span class="icon-circle w-4 h-4 bg-emerald-600 text-white"><i data-lucide="camera" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ผูกป้ายเสร็จแล้ว? ถ่ายรูปเช็คอิน GPS รับ +15 แต้ม</span>
          </button>
          <p class="text-[10px] text-center text-gray-400">PDF ถูกตั้งค่าขนาดและสเกลจริง (1:1) สำหรับเครื่องพิมพ์อิงค์เจ็ทไวนิล</p>
        </div>
      </div>
    </div>

    <!-- Homerun-Style Clean Property Detail Modal (Digital Luxury 75-15-5-5 & 3-Tier Layout) -->
    <div 
      id="property-detail-modal" 
      onclick="if(event.target === this) closePropertyDetailModal()" 
      class="fixed inset-0 z-50 bg-neutral-950/60 backdrop-blur-xs flex items-center justify-center px-3 pt-10 pb-6 sm:p-6 hidden modal-backdrop"
    >
      <!-- Modal Container: ล็อกความสูงไม่เกิน 82dvh (มือถือ) / 88dvh (คอม) และใช้ flex-col เพื่อแยกส่วนเลื่อน -->
      <div class="relative w-full max-w-lg max-h-[82dvh] sm:max-h-[88dvh] bg-white rounded-3xl shadow-2xl border border-neutral-200/80 flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        <!-- 1. Floating Close Button (เกาะติดมุมขวาบนตลอดเวลา ไม่เลื่อนหายตามเนื้อหา) -->
        <button 
          type="button"
          onclick="closePropertyDetailModal()" 
          aria-label="ปิดหน้าต่าง"
          class="absolute top-3.5 right-3.5 z-30 w-9 h-9 rounded-full bg-neutral-900/75 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90"
        >
          <i data-lucide="x" class="w-5 h-5 stroke-[2.5]"></i>
        </button>

        <!-- 2. Scrollable Body: ส่วนเนื้อหาที่เลื่อนได้อย่างเดียว -->
        <div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 custom-scrollbar">
          
          <!-- Top Badges & Meta -->
          <div class="flex items-center gap-2 pr-10">
            <span id="detail-category-badge" class="capsule-bokeh text-[11px] font-medium px-3 py-0.5">ทาวน์โฮม</span>
            <span id="detail-bank-badge"></span>
            <span id="detail-code" class="text-xs text-neutral-400 font-mono">รหัส: -</span>
          </div>

          <!-- Detail Image Carousel / Hero -->
          <div class="relative aspect-[16/10] bg-neutral-100 rounded-2xl overflow-hidden shadow-inner">
            <img id="detail-main-img" src="" alt="" class="w-full h-full object-cover">
            <div class="absolute bottom-2.5 left-2.5">
              <span id="detail-status-pill" class="bg-[#8B0000] text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full shadow-sm">New</span>
            </div>
            <a id="detail-external-link" href="#" target="_blank" class="absolute bottom-2.5 right-2.5 capsule-bokeh hover:bg-neutral-900/80 text-white text-[11px] font-medium px-3 py-1 flex items-center gap-1 shadow-sm">
              <i data-lucide="external-link" class="w-3 h-3"></i>
              <span>ดูหน้าเว็บเดิม</span>
            </a>
          </div>

          <!-- Title & Location -->
          <div class="space-y-1">
            <h2 id="detail-title" class="font-bold text-neutral-900 text-base md:text-lg leading-snug"></h2>
            <div class="flex items-center gap-1.5 text-xs text-neutral-500">
              <i data-lucide="map-pin" class="w-3.5 h-3.5 text-neutral-400 shrink-0"></i>
              <span id="detail-location">กรุงเทพฯ และปริมณฑล</span>
            </div>
          </div>

          <!-- Homerun Specs Grid -->
          <div class="grid grid-cols-2 gap-2 bg-[#FAF8F5] p-3 rounded-2xl border border-neutral-200/70 text-xs">
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-neutral-500 border border-neutral-200/50">
                <i data-lucide="grid" class="w-3.5 h-3.5"></i>
              </div>
              <div>
                <div class="text-[10px] text-neutral-400">เนื้อที่</div>
                <div id="detail-size" class="font-bold text-neutral-800">43.9 ตร.ว.</div>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-neutral-500 border border-neutral-200/50">
                <i data-lucide="home" class="w-3.5 h-3.5"></i>
              </div>
              <div>
                <div class="text-[10px] text-neutral-400">พื้นที่ใช้สอย</div>
                <div id="detail-usable" class="font-bold text-neutral-800">110 ตร.ม.</div>
              </div>
            </div>
          </div>

          <!-- Description -->
          <p id="detail-desc" class="text-xs text-neutral-600 leading-relaxed bg-[#FAF8F5]/50 border border-neutral-200/70 p-3 rounded-2xl"></p>

          <!-- 👤 POINT 2: INLINE AGENT PROFILE CARD (Shown in Client Mode) -->
          <div id="detail-agent-card" class="hidden rounded-2xl bg-[#FAF9F6] border border-[#C2A460]/40 p-3.5 shadow-sm space-y-2.5">
            <div class="flex items-center justify-between text-[11px]">
              <span class="font-semibold text-neutral-500 uppercase tracking-wider text-[10px]">ผู้ดูแลการเข้าชม & เสนอราคา</span>
              <span id="detail-card-cert-id" class="font-mono font-bold text-neutral-800 bg-white px-2 py-0.5 rounded border border-neutral-200 text-[10px]">ID: SW-042</span>
            </div>
            <div class="flex items-center gap-3">
              <div class="relative shrink-0">
                <img id="detail-card-agent-avatar" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80" alt="Agent" class="w-12 h-12 rounded-full object-cover border-2 border-[#C2A460] shadow-sm">
                <div class="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-[#C2A460] text-neutral-900 flex items-center justify-center border border-white" title="Verified Partner">
                  <i data-lucide="check" class="w-2.5 h-2.5 stroke-[3]"></i>
                </div>
              </div>
              <div class="min-w-0 flex-1">
                <h3 id="detail-card-agent-name" class="text-sm font-bold text-neutral-900 truncate">คุณธนภัทร วงศ์สุวรรณ</h3>
                <div id="detail-card-title-badge" class="inline-flex items-center gap-1 mt-0.5 px-2 py-0.5 rounded text-[10px] font-semibold bg-neutral-900 text-[#C2A460]">
                  <i data-lucide="award" class="w-3 h-3"></i>
                  <span id="detail-card-agent-title">Verified Property Consultant</span>
                </div>
                <p class="text-[10px] text-neutral-500 mt-1 leading-snug">ตัวแทนรับรองโดย ศิวาทรัพย์ แอสเซท • ประสานงานเปิดบ้านและยื่นสินเชื่อครบวงจร</p>
              </div>
            </div>
            <button type="button" onclick="contactViaLine('booking', document.getElementById('detail-title').textContent)" class="w-full py-2.5 px-3 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-white text-xs font-semibold flex items-center justify-center gap-2 transition shadow-sm cursor-pointer">
              <i data-lucide="calendar-check" class="w-4 h-4 text-[#C2A460]"></i>
              <span id="detail-card-btn-text">นัดหมายเข้าชมบ้านหลังนี้กับ คุณธนภัทร</span>
            </button>
          </div>

          <!-- 🔑 NPA Key & Messenger Banner (Dynamic for Agent vs Admin) -->
          <div id="detail-npa-key-banner" class="bg-[#FAF8F5] border border-[#E8DFD1] rounded-2xl p-3 flex items-center justify-between gap-2 shadow-2xs">
            <div class="flex items-center gap-2.5 min-w-0">
              <div id="detail-npa-key-icon-box" class="w-9 h-9 rounded-xl bg-neutral-900 text-white flex items-center justify-center shrink-0 shadow-xs">
                <i data-lucide="key" class="w-4 h-4 text-[#E5C985]"></i>
              </div>
              <div class="min-w-0">
                <div class="font-bold text-xs text-neutral-900 flex items-center gap-1.5">
                  <span id="detail-npa-key-title">บริการเบิกกุญแจ NPA & Messenger</span>
                  <span id="detail-npa-key-tag" class="text-[9px] bg-[#C2A460]/15 text-[#8C6D23] px-1.5 py-0.2 rounded font-bold border border-[#C2A460]/30">พี่ลิลลี่</span>
                </div>
                <div id="detail-npa-key-desc" class="text-[10.5px] text-neutral-600 truncate">มี Messenger วิ่งรับกุญแจจากแบงก์ส่งมอบหน้างาน</div>
              </div>
            </div>
            <button type="button" id="detail-btn-banner-npa-key" class="shrink-0 bg-neutral-900 hover:bg-neutral-800 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-2xs flex items-center gap-1 transition-all active:scale-95 cursor-pointer">
              <span id="detail-btn-banner-npa-key-text">ขอนัดชม</span>
              <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
            </button>
          </div>

          <!-- Financial Breakdown (Homerun Style) -->
          <div class="bg-[#FAF8F5] p-3.5 rounded-2xl border border-neutral-200/70 space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs text-neutral-600 flex items-center gap-1.5">
                <span class="w-4 h-4 rounded-full border border-neutral-300 text-neutral-600 font-bold text-[10px] inline-flex items-center justify-center leading-none select-none">฿</span>
                <span>ราคาก่อนต่อรอง</span>
              </span>
              <span id="detail-price" class="text-lg font-black text-neutral-900 tracking-tight">฿3,410,000</span>
            </div>
            <div class="flex items-center justify-between text-xs pt-1 border-t border-neutral-200/60">
              <span class="text-neutral-500 flex items-center gap-1.5">
                <span class="w-4 h-4 rounded-full border border-neutral-300 text-neutral-500 font-bold text-[11px] inline-flex items-center justify-center leading-none select-none">฿</span>
                <span>หลักประกันเพื่อต่อรองราคา</span>
              </span>
              <span id="detail-deposit" class="font-bold text-neutral-800">฿50,000</span>
            </div>
            <div class="flex items-center justify-between text-xs pt-1 border-t border-neutral-200/60">
              <span class="text-neutral-500 flex items-center gap-1.5">
                <i data-lucide="calculator" class="w-3.5 h-3.5 text-neutral-500"></i>
                <span>ประมาณการผ่อนต่อเดือน</span>
              </span>
              <span id="detail-installment" class="font-bold text-neutral-800">~ 12,000 บ./เดือน</span>
            </div>
          </div>

          <!-- 📄 Role-Based Document Downloads -->
          <div id="detail-documents-section" class="bg-white border border-neutral-200/70 p-3.5 rounded-2xl space-y-2 text-xs">
            <!-- Populated dynamically by renderPropertyDocumentDownloads(prop) based on currentMode -->
          </div>

        </div>

        <!-- 3. Sticky Bottom Action Bar (ล็อกติดล่างตลอดเวลา) -->
        <div class="p-3.5 bg-white/95 backdrop-blur-md border-t border-neutral-200/80 space-y-2 z-20">
          
          <!-- Primary Action Bar -->
          <div id="detail-actions-footer-bar" class="space-y-2">
            <!-- Agent Action Row (สำหรับตัวแทนขาย) -->
            <div id="detail-agent-actions-row" class="space-y-1.5">
              <div class="grid grid-cols-2 gap-2">
                <button id="detail-btn-vinyl" type="button" class="w-full bg-[#FAF8F5] hover:bg-[#F2EDE4] text-[#8C6D23] font-bold py-2 rounded-xl border border-[#E8DFD1] text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                  <i data-lucide="printer" class="w-3.5 h-3.5 text-[#C2A460]"></i>
                  <span>พิมพ์ป้ายไวนิล (Auto PDF)</span>
                </button>
                <button id="detail-btn-share" type="button" class="w-full bg-neutral-900 hover:bg-neutral-800 text-white font-bold py-2 rounded-xl shadow-2xs text-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                  <i data-lucide="share-2" class="w-3.5 h-3.5"></i>
                  <span>แชร์ล็อกสิทธิ์ (3-5%)</span>
                </button>
              </div>
              <button id="detail-btn-npa-key" type="button" class="w-full bg-white hover:bg-neutral-50 text-neutral-800 font-bold py-1.5 rounded-xl border border-neutral-200 text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                <i data-lucide="key" class="w-3.5 h-3.5 text-neutral-600"></i>
                <span>เบิกกุญแจ NPA & Messenger (พี่ลิลลี่)</span>
              </button>
            </div>

            <!-- Admin Dedicated Operational Console (สำหรับบอร์ดบริหาร: บัว, กูล, พี่ลิลลี่) -->
            <div id="detail-admin-actions-row" class="hidden space-y-2">
              <div class="grid grid-cols-2 gap-2">
                <button id="detail-admin-btn-key" type="button" class="w-full bg-neutral-900 hover:bg-neutral-800 text-[#E5C985] font-bold py-2.5 rounded-xl border border-[#C2A460]/50 text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                  <i data-lucide="key" class="w-4 h-4 text-[#C2A460]"></i>
                  <span>ติดตามสถานะกุญแจ</span>
                </button>
                <button id="detail-admin-btn-appointments" type="button" class="w-full bg-white hover:bg-neutral-50 text-neutral-900 font-bold py-2.5 rounded-xl border border-neutral-300 text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                  <i data-lucide="calendar" class="w-4 h-4 text-neutral-700"></i>
                  <span>คิวนัดชมเคสนี้ (<span id="detail-admin-app-count" class="text-[#8B0000] font-black">2</span>)</span>
                </button>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <button id="detail-admin-btn-price" type="button" class="w-full bg-[#FAF8F5] hover:bg-[#F2EDE4] text-neutral-800 font-bold py-2 rounded-xl border border-[#E8DFD1] text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                  <i data-lucide="sliders" class="w-3.5 h-3.5 text-[#8C6D23]"></i>
                  <span>แก้ราคา & Floor Cost</span>
                </button>
                <button id="detail-admin-btn-share" type="button" class="w-full bg-white hover:bg-neutral-50 text-neutral-700 font-bold py-2 rounded-xl border border-neutral-200 text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                  <i data-lucide="share-2" class="w-3.5 h-3.5 text-neutral-500"></i>
                  <span>แชร์ลิงก์ทรัพย์ (กลาง)</span>
                </button>
              </div>
            </div>
            
            <button id="detail-btn-offer" type="button" class="w-full bg-[#C2A460] hover:bg-[#A98B45] text-neutral-900 font-bold py-2.5 rounded-xl shadow-xs flex items-center justify-center gap-2 text-sm active:scale-95 transition-all">
              <i data-lucide="badge-dollar-sign" class="w-4 h-4"></i>
              <span id="detail-btn-offer-label">เสนอราคา</span>
            </button>
            <div id="detail-waitlist-row" class="hidden"></div>
          </div>

          <!-- 4. Bottom Dismiss Button (กดปิดจากด้านล่างได้ ไม่ต้องเลื่อนกลับขึ้นไปบนสุด) -->
          <button 
            type="button"
            onclick="closePropertyDetailModal()" 
            class="w-full py-1.5 text-xs font-medium text-neutral-400 hover:text-neutral-700 hover:bg-neutral-100 rounded-xl transition-all flex items-center justify-center gap-1"
          >
            <span>✕ ปิดหน้าต่างนี้</span>
          </button>

        </div>
      </div>
    </div>

    <!-- 🏆 Agent Directory & Leaderboard Modal (125 Agents: S02-S126) -->
    <div id="agent-leaderboard-modal" onclick="if(event.target === this) closeAgentLeaderboardModal()" class="hidden modal-backdrop fixed inset-0 z-50 bg-neutral-950/60 backdrop-blur-xs flex items-center justify-center px-3 pt-6 pb-6 sm:p-6">
      <div class="relative w-full max-w-2xl max-h-[84dvh] sm:max-h-[88dvh] bg-white rounded-3xl shadow-2xl border border-neutral-200/80 flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        <!-- 1. Fixed Header (คลีน ขาว-ดำ-ทอง พร้อมปุ่มปิดคาไว้ขนาดใหญ่ w-9 h-9) -->
        <div class="sticky top-0 z-30 px-5 py-3.5 sm:py-4 bg-white/95 backdrop-blur-md border-b border-neutral-100 flex items-center justify-between shrink-0 shadow-xs">
          <div class="flex items-center gap-3 min-w-0 pr-2">
            <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-neutral-900 text-[#D4BC8B] flex items-center justify-center text-base shadow-xs shrink-0 font-bold">
              ♛
            </div>
            <div class="min-w-0">
              <h2 class="text-sm sm:text-base font-bold text-neutral-900 tracking-tight leading-tight truncate">ทำเนียบตัวแทน & Leaderboard</h2>
              <p class="text-[10px] sm:text-xs text-neutral-400 truncate">ระบบวัดผลอัตโนมัติ 2 แทร็ก (กิจกรรม & ผลงาน) • 125 ท่าน</p>
            </div>
          </div>
          <button type="button" onclick="closeAgentLeaderboardModal()" aria-label="ปิดหน้าต่าง" class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0" title="ปิดหน้าต่าง">
            <i data-lucide="x" class="w-5 h-5 stroke-[2.5]"></i>
          </button>
        </div>

        <!-- 2. Scrollable Body (Single Scrollbar) -->
        <div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 custom-scrollbar">
          
          <!-- Action Bar เก็บแต้มด่วน (Warm Champagne & Burgundy) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <button type="button" onclick="openMeetingCheckinModal()" class="py-2.5 px-4 rounded-xl bg-[#FAF8F5] hover:bg-[#F3EFE6] border border-[#E5DEC9] text-neutral-800 text-xs font-semibold flex items-center justify-center gap-2 transition cursor-pointer active:scale-95 shadow-2xs">
              <span class="text-[#9A7D46]">⊞</span>
              <span id="lb-btn-meeting-label">QR เช็กชื่อเข้าประชุม</span>
              <span class="px-1.5 py-0.5 rounded bg-[#C2A460]/20 text-[#8C7038] text-[10px] font-bold">+10</span>
            </button>

            <button type="button" onclick="openVinylProofModal()" class="py-2.5 px-4 rounded-xl bg-[#8B0000] hover:bg-[#730000] text-white text-xs font-semibold flex items-center justify-center gap-2 shadow-xs transition cursor-pointer active:scale-95">
              <span>📷</span>
              <span id="lb-btn-vinyl-proof-label">ส่งภาพติดป้าย GPS</span>
              <span class="px-1.5 py-0.5 rounded bg-white/20 text-[#E5C985] text-[10px] font-bold">+15</span>
            </button>
          </div>

          <!-- 👑 Animal Intelligence Matrix Bar (3D Gold Emblem Edition) -->
          <div id="owner-animal-intelligence-bar" class="hidden bg-gradient-to-br from-slate-900 via-slate-900 to-amber-950/90 p-3.5 rounded-2xl border border-amber-500/40 space-y-2.5 shadow-md text-white">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-amber-300 flex items-center gap-1.5">
                <span class="w-5 h-5 rounded-full bg-amber-400 text-slate-950 font-black flex items-center justify-center text-[11px] shadow-2xs">👑</span>
                <span>SIWASUP ANIMAL MATRIX (วิเคราะห์ทีม 4 สาย)</span>
              </span>
              <button type="button" onclick="window.open('assets/characters/team_infographic.png', '_blank')" class="text-[10px] bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 font-bold px-2.5 py-0.5 rounded-full border border-amber-400/40 transition cursor-pointer flex items-center gap-1">
                <span>🖼️ ดูอินโฟกราฟิกเต็ม</span>
              </button>
            </div>

            <!-- 4 Animal Filter Tabs with 3D Gold Badges -->
            <div class="grid grid-cols-5 gap-1.5 text-[10px] font-bold">
              <button type="button" id="animal-btn-all" onclick="filterByAnimal('all')" class="p-1.5 rounded-xl border border-amber-400 bg-amber-400 text-slate-950 shadow-2xs text-center transition-all flex flex-col items-center justify-center cursor-pointer">
                <div class="text-[11px] font-black">ทั้งหมด</div>
                <div class="text-[9px] font-semibold opacity-80">125 ท่าน</div>
              </button>
              <button type="button" id="animal-btn-eagle" onclick="filterByAnimal('eagle')" class="p-1.5 rounded-xl border border-slate-700 bg-slate-800/90 text-amber-200 shadow-2xs text-center transition-all hover:border-amber-400 active:scale-95 flex flex-col items-center justify-center gap-0.5 cursor-pointer">
                <img src="assets/characters/badge_eagle.png" alt="Eagle" class="w-8 h-8 object-contain drop-shadow">
                <span>Eagle</span>
                <div class="text-[9px] text-amber-400 font-normal"><span id="animal-count-eagle">0</span> ท่าน</div>
              </button>
              <button type="button" id="animal-btn-lion" onclick="filterByAnimal('lion')" class="p-1.5 rounded-xl border border-slate-700 bg-slate-800/90 text-amber-200 shadow-2xs text-center transition-all hover:border-amber-400 active:scale-95 flex flex-col items-center justify-center gap-0.5 cursor-pointer">
                <img src="assets/characters/badge_lion.png" alt="Lion" class="w-8 h-8 object-contain drop-shadow">
                <span>Lion</span>
                <div class="text-[9px] text-amber-400 font-normal"><span id="animal-count-lion">0</span> ท่าน</div>
              </button>
              <button type="button" id="animal-btn-wolf" onclick="filterByAnimal('wolf')" class="p-1.5 rounded-xl border border-slate-700 bg-slate-800/90 text-amber-200 shadow-2xs text-center transition-all hover:border-amber-400 active:scale-95 flex flex-col items-center justify-center gap-0.5 cursor-pointer">
                <img src="assets/characters/badge_wolf.png" alt="Wolf" class="w-8 h-8 object-contain drop-shadow">
                <span>Wolf</span>
                <div class="text-[9px] text-amber-400 font-normal"><span id="animal-count-wolf">0</span> ท่าน</div>
              </button>
              <button type="button" id="animal-btn-bear" onclick="filterByAnimal('bear')" class="p-1.5 rounded-xl border border-slate-700 bg-slate-800/90 text-amber-200 shadow-2xs text-center transition-all hover:border-amber-400 active:scale-95 flex flex-col items-center justify-center gap-0.5 cursor-pointer">
                <img src="assets/characters/badge_bear.png" alt="Bear" class="w-8 h-8 object-contain drop-shadow">
                <span>Bear</span>
                <div class="text-[9px] text-amber-400 font-normal"><span id="animal-count-bear">0</span> ท่าน</div>
              </button>
            </div>

            <!-- Strategy & 3D Archetype Visual Banner -->
            <div id="animal-strategy-box" class="bg-slate-950/90 p-2.5 rounded-xl border border-amber-500/30 text-[10.5px] text-slate-200 leading-snug space-y-1.5">
              <div class="flex items-center gap-3">
                <img id="animal-strategy-img" src="assets/characters/badge_eagle.png" alt="Animal Badge" class="w-14 h-14 object-contain drop-shadow-md shrink-0 cursor-pointer hover:scale-105 transition-transform" onclick="toggleLeaderboardTurnaroundPreview()" title="คลิกเพื่อดูโมเดล 3D 4 มุมรอบตัว">
                <div class="min-w-0 flex-1">
                  <div class="flex items-center justify-between gap-1">
                    <span id="animal-strategy-title" class="font-bold text-xs text-amber-300">ตัวแทนทั้งหมด 125 ท่าน</span>

                  </div>
                  <div id="animal-strategy-desc" class="text-slate-300 text-[10px] mt-0.5">
                    คลิกเลือกเหรียญตราสัตว์ด้านบน เพื่อกรองรายชื่อตัวแทนและดูกลยุทธ์การจับคู่ทีม Co-Broker
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Top 3 Podium (คุมโทน Alabaster, Satin Gold และ Slate) -->
          <div id="leaderboard-podium" class="grid grid-cols-3 gap-2 sm:gap-2.5 items-end pt-2">
            <!-- Injected via JS -->
          </div>

          <!-- Filter Tracks & Search -->
          <div class="space-y-2.5 pt-1">
            <div class="flex items-center justify-between">
              <div class="inline-flex p-1 rounded-xl bg-neutral-100 border border-neutral-200/60 text-xs">
                <button id="lb-tab-total" onclick="filterLeaderboard('total')" class="px-3 py-1 rounded-lg bg-white text-neutral-900 font-semibold shadow-2xs transition-all">รวมทุกแต้ม</button>
                <button id="lb-tab-activity" onclick="filterLeaderboard('activity')" class="px-3 py-1 rounded-lg text-neutral-500 hover:text-neutral-900 font-medium transition-all">กิจกรรม</button>
                <button id="lb-tab-performance" onclick="filterLeaderboard('performance')" class="px-3 py-1 rounded-lg text-neutral-500 hover:text-neutral-900 font-medium transition-all">ผลงานขาย</button>
              </div>
              <span class="text-xs text-neutral-400">ทั้งหมด <strong id="lb-count-label" class="text-neutral-700">125</strong> ท่าน</span>
            </div>

            <!-- Search Input -->
            <div class="relative">
              <input 
                type="text" 
                id="lb-search-input" 
                oninput="searchLeaderboard(this.value)"
                placeholder="🔍 ค้นหารหัส S02-S126, ชื่อเล่น หรือชื่อจริง..." 
                class="w-full px-3.5 py-2 rounded-xl bg-neutral-50 border border-neutral-200/80 text-xs text-neutral-800 placeholder-neutral-400 focus:outline-none focus:bg-white focus:border-neutral-400 transition"
              />
            </div>
          </div>

          <!-- รายชื่อตารางคะแนน (ตัดอีโมจิละครสัตว์ออก ใช้ Single Scrollbar) -->
          <div class="border border-neutral-200/80 rounded-2xl bg-white overflow-hidden shadow-2xs">
            <div id="leaderboard-list" class="divide-y divide-neutral-100">
              <!-- Injected via JS -->
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- 🎟️ Meeting QR Check-in Modal -->
    <div id="modal-meeting-checkin" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6">
      <div class="modal-card max-w-sm space-y-3.5 !p-4 text-center">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-1.5">
            <span class="icon-circle w-6 h-6 bg-amber-600 text-white"><i data-lucide="calendar-check" class="w-3.5 h-3.5"></i></span>
            <h3 id="meeting-modal-title" class="font-bold text-sm text-gray-900">เช็คชื่อเข้าอบรม / ประชุมทีม</h3>
          </div>
          <button 
            type="button" 
            onclick="closeMeetingCheckinModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- QR Display for Zoom / Big Screen -->
        <div class="bg-gray-50 p-3 rounded-2xl border border-gray-200 space-y-2">
          <p class="text-[11px] text-gray-600 font-medium">ฉาย QR บนจอเพื่อให้ตัวแทนสแกนเช็คชื่ออัตโนมัติ (<span id="meeting-date-label" class="font-bold text-amber-900">รอบวันนี้</span>):</p>
          <div class="bg-white p-2 rounded-xl inline-block border border-gray-200 shadow-2xs">
            <img id="meeting-qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=https://thenassty-cpu.github.io/siwasup-cobroker-os/?action=checkin" alt="Meeting QR" class="w-40 h-40 object-contain mx-auto">
          </div>
          <div class="text-[10px] text-emerald-700 font-bold bg-emerald-50 py-0.5 px-2 rounded-full border border-emerald-200 inline-block">
            ✓ สแกนรับ +10 แต้มกิจกรรมทันที
          </div>
        </div>

        <!-- Self Check-in Option (for agents checking in right now) -->
        <div class="space-y-2 text-left pt-1 border-t border-gray-100">
          <label class="block font-medium text-xs text-gray-700">หรือเลือกรหัสตัวแทนของคุณเพื่อเช็คชื่อ:</label>
          <div class="relative">
            <select id="meeting-agent-select" class="w-full border rounded-lg p-2 text-xs bg-white font-bold text-gray-800 outline-none focus:ring-1 focus:ring-amber-500">
              <!-- Injected via JS -->
            </select>
          </div>
          <button type="button" onclick="submitMeetingCheckin()" class="w-full bg-siwasup-gold hover:opacity-95 text-gray-950 font-bold py-2 px-3 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
            <span id="meeting-submit-label">ยืนยันเช็คชื่อรับ +10 แต้ม</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 📸 Vinyl Photo + GPS Proof Modal -->
    <div id="modal-vinyl-proof" class="hidden modal-backdrop !items-center px-3 pt-10 pb-6 sm:p-6">
      <div class="modal-card max-w-sm space-y-3.5 !p-4">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-1.5">
            <span id="vinyl-proof-icon-badge" class="icon-circle w-6 h-6 bg-emerald-600 text-white"><i data-lucide="camera" class="w-3.5 h-3.5"></i></span>
            <div>
              <h3 id="vinyl-proof-modal-title" class="font-bold text-sm text-gray-900 leading-tight">ส่งภาพติดป้ายหน้างานจริง</h3>
              <p id="vinyl-proof-modal-subtitle" class="text-[9.5px] text-gray-500">Proof of Installation • รับทันที +15 แต้ม</p>
            </div>
          </div>
          <button 
            type="button" 
            onclick="closeVinylProofModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <form onsubmit="submitVinylProof(event)" class="space-y-2.5 text-xs">
          <!-- Agent Selection -->
          <div>
            <label id="vinyl-proof-agent-label" class="block font-medium mb-1 text-gray-700">รหัสตัวแทนผู้ติดป้าย:</label>
            <select id="proof-agent-select" class="w-full border rounded-lg p-1.5 text-xs bg-gray-50 font-bold text-gray-800 outline-none focus:ring-1 focus:ring-emerald-500">
              <!-- Injected via JS -->
            </select>
          </div>

          <!-- Property ID -->
          <div>
            <label class="block font-medium mb-1 text-gray-700">รหัสทรัพย์ที่ติดป้าย:</label>
            <input type="text" id="proof-prop-id" placeholder="เช่น 1069562 หรือชื่อโครงการ" required 
                   class="w-full border rounded-lg p-1.5 text-xs outline-none focus:ring-1 focus:ring-emerald-500">
          </div>

          <!-- GPS Location Auto-Detection -->
          <div class="bg-gray-50 p-2.5 rounded-xl border border-gray-200 space-y-1.5">
            <div class="flex justify-between items-center">
              <span class="font-medium text-gray-700 flex items-center gap-1">
                <i data-lucide="map-pin" class="w-3 h-3 text-red-600"></i>
                <span>พิกัด GPS หน้างานจริง:</span>
              </span>
              <button type="button" onclick="detectGpsLocation()" class="bg-white hover:bg-emerald-50 text-emerald-800 border border-emerald-300 px-2 py-0.5 rounded text-[10px] font-bold shadow-2xs active:scale-95 transition-all">
                ดึงพิกัดสด
              </button>
            </div>
            <div id="proof-gps-display" class="font-mono text-[10.5px] text-gray-600 bg-white p-1.5 rounded border border-gray-200">
              กดปุ่ม "ดึงพิกัดสด" เพื่อดึงตำแหน่ง GPS
            </div>
          </div>

          <!-- Photo Upload Input -->
          <div>
            <label id="vinyl-proof-photo-label" class="block font-medium mb-1 text-gray-700">ภาพถ่ายป้ายที่ผูกหน้าบ้าน:</label>
            <input type="file" id="proof-photo-file" accept="image/*" capture="environment" 
                   class="w-full text-[11px] text-gray-500 file:mr-2 file:py-1 file:px-2.5 file:rounded-lg file:border-0 file:text-[11px] file:font-semibold file:bg-emerald-100 file:text-emerald-800 hover:file:bg-emerald-200">
          </div>

          <button type="submit" id="vinyl-proof-submit-btn" class="w-full bg-[#8B0000] hover:bg-[#6B0000] text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <i data-lucide="upload-cloud" class="w-3.5 h-3.5"></i>
            <span id="vinyl-proof-submit-text">ยืนยันส่งผลงานรับ +15 แต้ม</span>
          </button>
        </form>
      </div>
    </div>

    <!-- 👤 My Profile & Scorecard Modal -->
    <div 
      id="modal-my-profile" 
      onclick="if(event.target === this) closeMyProfileModal()" 
      class="hidden modal-backdrop fixed inset-0 z-50 bg-neutral-950/60 backdrop-blur-xs flex items-center justify-center px-3 pt-6 pb-6 sm:p-6"
    >
      <div class="modal-card relative w-full max-w-md max-h-[84dvh] sm:max-h-[88dvh] bg-white rounded-3xl shadow-2xl border border-neutral-200/80 flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200 !p-0">
        
        <!-- 1. Sticky Header with Pinned Luxury Close Button ("คาไว้" ตลอดเวลา & ใหญ่เท่ากันกับอันอื่น) -->
        <div class="sticky top-0 z-30 px-4 sm:px-5 py-3.5 bg-white/95 backdrop-blur-md border-b border-neutral-100 flex items-center justify-between shrink-0 shadow-xs">
          <div class="flex items-center gap-2.5 min-w-0 pr-2">
            <span class="icon-circle w-8 h-8 rounded-xl bg-amber-500 text-white shadow-xs shrink-0 flex items-center justify-center">
              <i data-lucide="user-check" class="w-4 h-4 stroke-[2]"></i>
            </span>
            <div class="min-w-0">
              <h3 class="font-bold text-sm sm:text-base text-gray-900 leading-tight truncate">โปรไฟล์ตัวแทน & กระเป๋าคะแนน</h3>
              <p class="text-[10px] text-gray-500 truncate">Siwasup Co-Broker Agent Scorecard</p>
            </div>
          </div>
          
          <!-- ปุ่มปิดหรูแบบลอยคาไว้ (ขนาดใหญ่มาตรฐาน w-9 h-9 เท่ากับป๊อปอัปอื่น) -->
          <button 
            type="button" 
            onclick="closeMyProfileModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
            title="ปิดหน้าต่าง"
          >
            <i data-lucide="x" class="w-5 h-5 stroke-[2.5]"></i>
          </button>
        </div>

        <!-- 2. Scrollable Body (เลื่อนดูข้อมูลได้ โดยที่หัวและปุ่มปิดยังคาอยู่ด้านบนเสมอ) -->
        <div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-3.5 custom-scrollbar">
          <!-- Identity Switcher Dropdown (Select Any Agent) -->
          <div class="bg-gray-50 p-2 rounded-xl border border-gray-200 flex items-center justify-between text-xs">
            <label class="text-[11px] font-medium text-gray-600 flex items-center gap-1 shrink-0">
              <i data-lucide="users" class="w-3.5 h-3.5 text-gray-500"></i>
              <span>สลับตัวแทน:</span>
            </label>
            <select id="profile-agent-switcher" onchange="switchMyAgentProfile(this.value)" class="border border-gray-200 rounded-lg p-1 text-xs bg-white font-bold text-gray-800 outline-none focus:ring-1 focus:ring-amber-500 ml-2 flex-1">
              <!-- Injected via JS -->
            </select>
          </div>

          <!-- Profile Hero Card -->
          <div class="bg-gradient-to-br from-amber-50/80 via-white to-red-50/40 p-3.5 rounded-2xl border border-amber-200/80 relative shadow-2xs space-y-3">
            <div class="flex items-center gap-3">
              <div class="relative shrink-0">
                <img id="profile-3d-badge-img" src="assets/characters/badge_eagle.png" alt="Badge" class="w-16 h-16 object-contain drop-shadow-md">
                <div id="profile-avatar-circle" class=" -bottom-1 -right-1 px-1.5 py-0.5 rounded-full bg-slate-900 text-amber-300 font-mono font-black text-[10px] border border-amber-400 shadow-xs">
                  S22
                </div>
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-1.5 flex-wrap">
                  <span id="profile-nickname" class="font-black text-base text-gray-900">เจ็ม</span>
                  <span id="profile-code" class="text-xs font-mono font-bold bg-neutral-900 text-white px-2 py-0.5 rounded-md shadow-2xs">S22</span>
                  <span id="profile-tier-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">Gold</span>
                </div>
                <div id="profile-fullname" class="text-xs text-gray-600 truncate mt-0.5">นางสาวกัญญา คำทรศิริวัฒน์</div>
                <div class="flex items-center gap-2 text-[10px] text-gray-500 mt-1">
                  <span>📅 เริ่มงาน: <strong id="profile-start-date" class="text-gray-700">8/3/2566</strong></span>
                  <span>•</span>
                  <span>💬 LINE: <strong id="profile-line" class="text-gray-700">ggemmie</strong></span>
                </div>
              </div>
            </div>
          </div>

          <!-- 4 Archetype Stage Visual Selector (Bear -> Wolf -> Lion -> Eagle) -->
          <div class="bg-slate-950/95 p-3 rounded-2xl border border-amber-500/30 text-white space-y-2 shadow-sm">
            <div class="flex items-center justify-between text-xs font-bold text-amber-300">
              <span class="flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
                <span>สายตัวละคร (Archetype Stages):</span>
              </span>
              <span id="profile-active-tier-name" class="text-emerald-400 font-mono font-bold">🦅 พญาอินทรี</span>
            </div>

            <div class="grid grid-cols-3 sm:grid-cols-6 gap-1.5 pt-1">
              <button type="button" onclick="previewProfileArchetypeStage('bear')" id="evo-stage-bear" class="evo-stage-node flex flex-col items-center p-1.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-amber-400/60 transition cursor-pointer relative">
                <img src="assets/characters/badge_bear.png" alt="Bear" class="w-8 h-8 object-contain drop-shadow" />
                <span class="text-[9px] font-bold text-slate-300 mt-0.5">หมีตื่นตัว</span>
                <span class="text-[8px] text-slate-400">เริ่มต้น</span>
              </button>
              <button type="button" onclick="previewProfileArchetypeStage('wolf')" id="evo-stage-wolf" class="evo-stage-node flex flex-col items-center p-1.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-amber-400/60 transition cursor-pointer relative">
                <img src="assets/characters/badge_wolf.png" alt="Wolf" class="w-8 h-8 object-contain drop-shadow" />
                <span class="text-[9px] font-bold text-slate-300 mt-0.5">หมาป่า</span>
                <span class="text-[8px] text-emerald-400/80">ขยัน ≥100</span>
              </button>
              <button type="button" onclick="previewProfileArchetypeStage('lion')" id="evo-stage-lion" class="evo-stage-node flex flex-col items-center p-1.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-amber-400/60 transition cursor-pointer relative">
                <img src="assets/characters/badge_lion.png" alt="Lion" class="w-8 h-8 object-contain drop-shadow" />
                <span class="text-[9px] font-bold text-slate-300 mt-0.5">สิงห์สุขุม</span>
                <span class="text-[8px] text-amber-400/80">ผลงาน ≥300</span>
              </button>
              <button type="button" onclick="previewProfileArchetypeStage('falcon')" id="evo-stage-falcon" class="evo-stage-node flex flex-col items-center p-1.5 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-amber-400/60 transition cursor-pointer relative">
                <img src="assets/characters/badge_falcon.png" alt="Falcon" class="w-8 h-8 object-contain drop-shadow" />
                <span class="text-[9px] font-bold text-[#E5C985] mt-0.5">เหยี่ยว S22</span>
                <span class="text-[8px] text-stone-300">Specialist</span>
              </button>
              <button type="button" onclick="previewProfileArchetypeStage('eagle')" id="evo-stage-eagle" class="evo-stage-node flex flex-col items-center p-1.5 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-amber-400/60 transition cursor-pointer relative">
                <img src="assets/characters/badge_eagle.png" alt="Eagle" class="w-8 h-8 object-contain drop-shadow" />
                <span class="text-[9px] font-bold text-yellow-300 mt-0.5">พญาอินทรี</span>
                <span class="text-[8px] text-yellow-400/90">Super Star</span>
              </button>
              <button type="button" onclick="previewProfileArchetypeStage('gryphon')" id="evo-stage-gryphon" class="evo-stage-node flex flex-col items-center p-1.5 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-amber-400/60 transition cursor-pointer relative">
                <img src="assets/characters/badge_gryphon.png" alt="Gryphon" class="w-8 h-8 object-contain drop-shadow" />
                <span class="text-[9px] font-bold text-amber-300 mt-0.5">กริฟฟอน</span>
                <span class="text-[8px] text-rose-300">Master</span>
              </button>
            </div>

            <div id="profile-animal-quote" class="text-[11px] text-amber-200/90 italic font-medium">“มองไกล เห็นโอกาส พาไปได้ไกลกว่า”</div>
            <div id="profile-animal-desc" class="text-[11px] text-slate-200 font-normal leading-relaxed"></div>
          </div>

          <!-- Dual-Track Milestone Checkpoints (Activity 0->50->100 & Performance 0->150->300) -->
          <div class="bg-slate-950/85 rounded-xl p-3 border border-slate-800 space-y-2.5">
            <div class="text-[10.5px] font-bold text-amber-300 flex items-center justify-between">
              <span>🎯 หลอดเช็กพอยท์อัปเกรดสายตัวละคร (Dual-Track Evolution)</span>
              <span class="text-[9px] text-slate-400 font-normal">ขยับทุกครั้งที่ทำภารกิจ</span>
            </div>

            <!-- Track 1: Activity Evolution Bar -->
            <div class="space-y-1">
              <div class="flex justify-between items-center text-[10px]">
                <span class="font-bold text-emerald-400 flex items-center gap-1">
                  <span>🎪 หลอดความขยัน (Activity)</span>
                </span>
                <span id="profile-act-checkpoint-label" class="font-mono font-bold text-emerald-300">75 / 100 แต้ม</span>
              </div>
              <div class="relative w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-slate-700">
                <div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-400/70 z-10" title="เช็กพอยท์ 50 แต้ม: หมีตื่นตัว"></div>
                <div id="profile-act-evo-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-500" style="width: 75%;"></div>
              </div>
              <div class="flex justify-between text-[8.5px] text-slate-400 font-medium px-0.5">
                <span>0 เริ่มต้น</span>
                <span id="chk-act-50" class="text-emerald-300 font-bold">📍50 หมีตื่นตัว</span>
                <span id="chk-act-100" class="text-slate-500">🐺100 หมาป่าพิทักษ์</span>
              </div>
              <div id="profile-act-quest-Breakdown" class="text-[9.5px] text-emerald-200/90 bg-emerald-950/50 border border-emerald-800/50 rounded-lg px-2 py-1">
                🔥 <strong>ผ่านครึ่งทางแล้ว!</strong> ขาดอีก <strong>25 แต้ม</strong> เพื่อปลดล็อกร่างหมาป่าพิทักษ์ ➔ ติดป้ายอีก 2 จุด (+15) หรือแชร์ทรัพย์ (+5)
              </div>
            </div>

            <!-- Track 2: Performance Evolution Bar -->
            <div class="space-y-1 pt-1.5 border-t border-slate-800/90">
              <div class="flex justify-between items-center text-[10px]">
                <span class="font-bold text-amber-400 flex items-center gap-1">
                  <span>💰 หลอดผลงานปิดดีล (Performance)</span>
                </span>
                <span id="profile-perf-checkpoint-label" class="font-mono font-bold text-amber-300">210 / 300 แต้ม</span>
              </div>
              <div class="relative w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-slate-700">
                <div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-400/70 z-10" title="เช็กพอยท์ 150 แต้ม: นักเจรจาเปิดดีล"></div>
                <div id="profile-perf-evo-bar" class="bg-gradient-to-r from-amber-500 via-yellow-400 to-orange-400 h-full rounded-full transition-all duration-500" style="width: 70%;"></div>
              </div>
              <div class="flex justify-between text-[8.5px] text-slate-400 font-medium px-0.5">
                <span>0 เริ่มต้น</span>
                <span id="chk-perf-150" class="text-amber-300 font-bold">📍150 เปิดดีล/กู้ผ่าน</span>
                <span id="chk-perf-300" class="text-slate-500">🦁/🦅300 สิงห์ & อินทรี</span>
              </div>
              <div id="profile-perf-quest-Breakdown" class="text-[9.5px] text-amber-200/90 bg-amber-950/50 border border-amber-800/50 rounded-lg px-2 py-1">
                🔥 <strong>ใกล้ปลดล็อกร่างพญาอินทรี!</strong> ขาดอีกเพียง <strong>90 แต้ม</strong> ➔ ปิดใบจอง 1 เคส (+100) หรือพาชมบ้าน 2 นัด (+50)
              </div>
            </div>

            <!-- ⚡ Live Activity & Evolution Simulator -->
            <div class="pt-2 border-t border-slate-800 space-y-1.5">
              <div class="flex items-center justify-between text-[9.5px] text-slate-300">
                <span class="font-bold text-amber-300">⚡ ทดลองจำลองทำภารกิจ (ดูหลอดขยับ & เลื่อนขั้นทันที):</span>
                <button type="button" onclick="resetProfileSimulatorPoints()" class="px-1.5 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[8.5px] border border-slate-600 cursor-pointer transition">🔄 รีเซ็ตแต้ม</button>
              </div>
              <div class="grid grid-cols-4 gap-1">
                <button type="button" onclick="simulateProfileQuest('smart_share_click')" class="py-1 px-1 rounded-lg bg-emerald-950/90 hover:bg-emerald-900 border border-emerald-600/50 text-emerald-200 font-bold text-[9px] cursor-pointer active:scale-95 transition text-center">
                  📲 แชร์ทรัพย์<br><span class="text-emerald-400">+5 ขยัน</span>
                </button>
                <button type="button" onclick="simulateProfileQuest('vinyl_field_proof')" class="py-1 px-1 rounded-lg bg-emerald-950/90 hover:bg-emerald-900 border border-emerald-600/50 text-emerald-200 font-bold text-[9px] cursor-pointer active:scale-95 transition text-center">
                  🪧 ติดป้าย GPS<br><span class="text-emerald-400">+15 ขยัน</span>
                </button>
                <button type="button" onclick="simulateProfileQuest('customer_viewing')" class="py-1 px-1 rounded-lg bg-amber-950/90 hover:bg-amber-900 border border-amber-600/50 text-amber-200 font-bold text-[9px] cursor-pointer active:scale-95 transition text-center">
                  🏡 พาชมบ้าน<br><span class="text-amber-400">+50 ผลงาน</span>
                </button>
                <button type="button" onclick="simulateProfileQuest('booking_confirmed')" class="py-1 px-1 rounded-lg bg-amber-950/90 hover:bg-amber-900 border border-amber-600/50 text-amber-200 font-bold text-[9px] cursor-pointer active:scale-95 transition text-center">
                  📝 ปิดใบจอง<br><span class="text-amber-400">+100 ผลงาน</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Score Breakdown Grid -->
          <div class="grid grid-cols-2 gap-2 text-center">
            <div class="bg-emerald-50/70 p-2.5 rounded-xl border border-emerald-200/80 space-y-0.5">
              <div class="text-[10px] text-emerald-700 font-bold flex items-center justify-center gap-1">
                <span>🎪 คะแนนกิจกรรม</span>
              </div>
              <div id="profile-act-pts" class="text-xl font-black text-emerald-800 font-mono">75</div>
              <div class="text-[9px] text-emerald-600">ประชุม / ป้าย GPS / แชร์</div>
            </div>

            <div class="bg-blue-50/70 p-2.5 rounded-xl border border-blue-200/80 space-y-0.5">
              <div class="text-[10px] text-blue-700 font-bold flex items-center justify-center gap-1">
                <span>💰 คะแนนผลงาน</span>
              </div>
              <div id="profile-perf-pts" class="text-xl font-black text-blue-800 font-mono">210</div>
              <div class="text-[9px] text-blue-600">ฝากทรัพย์ / จอง / ปิดโอน</div>
            </div>
          </div>

          <!-- Total Points Big Pill -->
          <div class="bg-gradient-to-r from-[#800000] via-[#990000] to-[#730000] text-white p-2.5 rounded-xl shadow-xs flex items-center justify-between px-3">
            <div class="flex items-center gap-2">
              <i data-lucide="award" class="w-5 h-5 text-amber-300"></i>
              <div>
                <div class="text-[10px] text-red-200">คะแนนสะสมรวมทั้งหมด</div>
                <div class="font-bold text-xs">จัดอันดับใน Leaderboard</div>
              </div>
            </div>
            <div id="profile-total-pts" class="text-2xl font-black font-mono text-amber-300">285</div>
          </div>

          <!-- Quick Action Buttons -->
          <div class="grid grid-cols-2 gap-2 pt-1">
            <button type="button" onclick="closeMyProfileModal(); openMeetingCheckinModal();" class="bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold py-2 px-2 rounded-xl text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
              <i data-lucide="qr-code" class="w-3.5 h-3.5 text-amber-600"></i>
              <span>เช็คชื่อเข้าประชุม (+10)</span>
            </button>
            <button type="button" onclick="closeMyProfileModal(); openVinylProofModal();" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold py-2 px-2 rounded-xl text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
              <i data-lucide="camera" class="w-3.5 h-3.5 text-emerald-600"></i>
              <span>ส่งภาพติดป้าย GPS (+15)</span>
            </button>
          </div>

          <!-- View Full Leaderboard Link -->
          <button type="button" onclick="closeMyProfileModal(); openAgentLeaderboardModal();" class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold py-2.5 px-3 rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all active:scale-95 cursor-pointer">
            <i data-lucide="trophy" class="w-3.5 h-3.5 text-amber-600"></i>
            <span>ดูอันดับในทำเนียบตัวแทน (Leaderboard 125)</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 🔑 NPA Key Dispatch & Messenger Tracking Modal (Demo Prototype - 3-Tier Architecture & Safe Mobile Clearance) -->
    <div 
      id="npa-key-dispatch-modal" 
      onclick="if(event.target === this) closeNpaKeyModal()"
      class="fixed inset-0 z-[100] bg-neutral-950/65 backdrop-blur-xs flex items-center justify-center px-3 pt-10 pb-6 sm:p-6 hidden modal-backdrop"
    >
      <!-- Modal Container: ล็อกความสูง max-h-[82dvh] sm:max-h-[88dvh] ไม่มุดขอบบน Chrome -->
      <div class="relative w-full max-w-lg max-h-[82dvh] sm:max-h-[88dvh] bg-white rounded-3xl shadow-2xl border border-neutral-200/80 flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        <!-- 1. Sticky Header: ล็อกส่วนหัวไว้กับที่ ไม่ให้ไหลขึ้นไปมุดขอบบน -->
        <div class="px-4 py-3.5 sm:px-5 sm:py-4 bg-white border-b border-neutral-100 flex items-start justify-between gap-3 shrink-0">
          <div class="flex items-start gap-2.5 min-w-0">
            <div class="w-9 h-9 rounded-xl bg-neutral-900 text-[#D4BC8B] flex items-center justify-center text-sm shrink-0 mt-0.5 shadow-2xs">
              <i data-lucide="key" class="w-4 h-4 text-[#D4BC8B]"></i>
            </div>
            <div class="min-w-0">
              <div class="flex flex-wrap items-center gap-1.5">
                <h3 id="npa-modal-title" class="text-sm sm:text-base font-bold text-neutral-900 leading-snug">
                  ระบบเบิกกุญแจ NPA & ติดตาม Messenger
                </h3>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-50 text-amber-800 border border-amber-200/70 shrink-0">
                  Demo Prototype
                </span>
              </div>
              <p class="text-[11px] text-neutral-500 mt-0.5 truncate">
                <span id="npa-modal-subtitle">ผู้รับผิดชอบงาน: <strong class="text-neutral-700">พี่ลิลลี่ (Admin ศิวาทรัพย์)</strong></span>
              </p>
            </div>
          </div>

          <!-- ปุ่มปิด (X) ขนาด 32x32px กดง่าย ไม่โดนเบียด -->
          <button 
            type="button" 
            onclick="closeNpaKeyModal()" 
            aria-label="ปิดหน้าต่าง"
            class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- 2. Scrollable Content Body: เลื่อนเฉพาะเนื้อหาด้านใน -->
        <div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 custom-scrollbar">
          
          <!-- กล่องแจ้งสถานะระบบ Demo -->
          <div class="p-3 rounded-2xl bg-[#FAF8F5] border border-[#E8DFD1] text-xs text-neutral-700 leading-relaxed shadow-2xs">
            <strong class="text-[#8C734B]">ⓘ สถานะระบบ:</strong> ระบบเบิกกุญแจและประเมินคะแนนตัวแทนนี้เป็นแบบจำลอง (Demo) รอการประชุมสรุปข้อกำหนดร่วมกับ <strong>กูล, บัว และพี่ลิลลี่</strong> เพิ่มเติม
          </div>

          <!-- Stepper Tabs (1. ยื่นขอเบิก / 2. ติดตาม / 3. ตรวจสอบ) -->
          <div class="grid grid-cols-3 gap-1 p-1 rounded-2xl bg-neutral-100 text-center text-[11px] font-semibold">
            <button type="button" id="tab-npa-btn-req" onclick="switchNpaKeyTab('req')" class="py-2 px-1 rounded-xl bg-white text-neutral-900 shadow-2xs transition-all">
              1. ยื่นขอเบิก<br><span class="text-[10px] font-normal text-neutral-500">(Agent)</span>
            </button>
            <button type="button" id="tab-npa-btn-track" onclick="switchNpaKeyTab('track')" class="py-2 px-1 rounded-xl text-neutral-500 hover:text-neutral-800 transition-all">
              2. ติดตาม<br><span class="text-[10px] font-normal">Messenger</span>
            </button>
            <button type="button" id="tab-npa-btn-audit" onclick="switchNpaKeyTab('audit')" class="py-2 px-1 rounded-xl text-neutral-500 hover:text-neutral-800 transition-all">
              3. ตรวจสอบ<br><span class="text-[10px] font-normal">(พี่ลิลลี่)</span>
            </button>
          </div>

          <!-- TAB 1: Agent Key Request Form -->
          <div id="npa-tab-req" class="space-y-3">
            <div class="p-3.5 rounded-2xl bg-neutral-50 border border-neutral-200/80 space-y-1">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-semibold text-neutral-400">ข้อมูลทรัพย์ NPA ที่ต้องการเบิกกุญแจ</span>
                <span id="npa-req-bank" class="px-2 py-0.5 rounded bg-sky-100 text-sky-800 text-[10px] font-bold">SCB</span>
              </div>
              <p id="npa-req-prop-title" class="text-xs sm:text-sm font-bold text-neutral-900 truncate">คอนโด เซ็นทริค ซีน รัชวิภา</p>
              <p class="text-[11px] text-neutral-500">รหัสทรัพย์: <span id="npa-req-prop-id" class="font-mono font-bold text-neutral-700">#1069562</span></p>
            </div>

            <div class="space-y-3">
              <div>
                <label class="block text-xs font-bold text-neutral-800 mb-1.5">เวลานัดหมายพาลูกค้าเข้าชมหน้างาน</label>
                <div class="grid grid-cols-2 gap-2">
                  <input type="date" id="npa-date" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs font-medium text-neutral-800 focus:outline-none focus:border-neutral-400" />
                  <input type="time" id="npa-time" value="14:00" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs font-medium text-neutral-800 focus:outline-none focus:border-neutral-400" />
                </div>
                <p class="text-[11px] text-emerald-700 font-medium mt-1.5 flex items-center gap-1">
                  <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i>
                  <span>แจ้งล่วงหน้า 24 ชม. (ผ่านเกณฑ์ Fast-Track เบิกกุญแจทันที)</span>
                </p>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs font-bold text-neutral-800 mb-1">ชื่อผู้จะซื้อ (ลูกค้า)</label>
                  <input type="text" id="npa-client-name" placeholder="คุณสมชาย ใจดี" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs focus:outline-none focus:border-neutral-400" />
                </div>
                <div>
                  <label class="block text-xs font-bold text-neutral-800 mb-1">เบอร์โทรลูกค้า</label>
                  <input type="tel" id="npa-client-phone" placeholder="08x-xxx-xxxx" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs focus:outline-none focus:border-neutral-400" />
                </div>
              </div>

              <div class="p-3.5 rounded-2xl bg-neutral-50 border border-neutral-200/70 text-[11px] text-neutral-600 space-y-1.5">
                <div class="font-bold text-neutral-800 flex items-center gap-1.5">
                  <i data-lucide="shield-check" class="w-3.5 h-3.5 text-neutral-700"></i>
                  <span>ข้อตกลงและนโยบายการเบิกกุญแจธนาคาร</span>
                </div>
                <ul class="list-disc pl-4 space-y-1 text-neutral-500">
                  <li>Messenger จะนำกุญแจไปส่งมอบให้ Agent ณ จุดนัดพบหน้าทรัพย์</li>
                  <li>Agent ต้องตรวจนับดอกกุญแจและเซ็นรับมอบต่อหน้า Messenger</li>
                  <li>เมื่อชมเสร็จ ต้องล็อกบ้านเรียบร้อยและส่งมอบกุญแจคืนทันที (ไม่เกิน 24 ชม.)</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- TAB 2: Messenger & Bank Live Tracker -->
          <div id="npa-tab-track" class="hidden space-y-3">
            <!-- Warning / Timeout Banner -->
            <div id="key-timeout-banner" class="bg-amber-50 border border-amber-200/90 rounded-2xl p-3 flex items-start gap-2.5 text-xs text-amber-900 shadow-2xs">
              <span class="text-base leading-none">⚠️</span>
              <div class="space-y-0.5">
                <div class="font-bold flex items-center gap-1.5">
                  <span>ตรวจพบเคสอาจค้าง (14:15 น. เกินเวลานัด 15 นาที)</span>
                  <span class="bg-amber-200 text-amber-900 text-[9px] px-1.5 py-0.2 rounded-full font-bold">Smart Alert</span>
                </div>
                <div class="text-[11px] text-amber-700 leading-tight">
                  นัดหมาย 14:00 น. หาก Messenger เน็ตหลุด/แบตหมด หรือลืมกด แต่ Agent หน้างานได้รับกุญแจแล้ว สามารถใช้ปุ่ม <strong>Fail-Safe Override</strong> ด้านล่างเพื่อปลดล็อคขั้นตอนได้ทันที
                </div>
              </div>
            </div>

            <div class="bg-neutral-50 border border-neutral-200/80 rounded-2xl p-3.5 space-y-2">
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold text-neutral-900">สถานะคำขอเบิกกุญแจ #KEY-2026-089</span>
                <span id="key-track-status-pill" class="bg-sky-100 text-sky-800 font-bold px-2.5 py-0.5 rounded-full text-[10px]">กำลังวิ่งส่ง</span>
              </div>
              
              <div class="space-y-2.5 pt-1 text-xs">
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] font-bold">✓</span>
                  <span class="text-neutral-700">10:00 น. - Agent ยื่นคำขอเบิกกุญแจเข้าระบบ</span>
                </div>
                <div class="flex items-center gap-2.5">
                  <span class="w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] font-bold">✓</span>
                  <span class="text-neutral-700">10:30 น. - <strong>พี่ลิลลี่</strong> ตรวจสอบเอกสาร & อนุมัติใบส่งตัวธนาคาร</span>
                </div>
                <div class="flex items-center gap-2.5" id="key-step-3-row">
                  <span id="key-step-3-icon" class="w-5 h-5 rounded-full bg-sky-600 text-white flex items-center justify-center text-[10px] font-bold animate-pulse">🛵</span>
                  <span id="key-step-3-text" class="font-bold text-sky-800">13:15 น. - Messenger (พี่สมชาย) รับกุญแจจาก สนง.ใหญ่ กำลังวิ่งไปหน้างาน</span>
                </div>
                <div class="flex items-center gap-2.5 text-neutral-400" id="key-step-4-row">
                  <span id="key-step-4-icon" class="w-5 h-5 rounded-full bg-neutral-200 text-neutral-500 flex items-center justify-center text-[10px] font-bold">4</span>
                  <span id="key-step-4-text">รอส่งมอบกุญแจให้ Agent ณ หน้าบ้าน (นัด 14:00 น.)</span>
                </div>
                <div class="flex items-center gap-2.5 text-neutral-400" id="key-step-5-row">
                  <span id="key-step-5-icon" class="w-5 h-5 rounded-full bg-neutral-200 text-neutral-500 flex items-center justify-center text-[10px] font-bold">5</span>
                  <span id="key-step-5-text">รอรับกุญแจคืน & ถ่ายรูปยืนยันปิดล็อกบ้าน</span>
                </div>
              </div>
            </div>

            <!-- Fail-Safe & Admin Override Controls -->
            <div class="bg-gradient-to-br from-[#FAF8F5] to-white border border-[#E8DFD1] rounded-2xl p-3.5 space-y-2 text-xs shadow-2xs">
              <div class="flex items-center justify-between">
                <div class="font-bold text-neutral-900 flex items-center gap-1.5">
                  <span class="text-[#C2A460]">⚡</span>
                  <span>ระบบปลดล็อคสถานะฉุกเฉิน (Fail-Safe & Master Override)</span>
                </div>
                <span class="text-[10px] bg-[#F4EBD9] text-[#8A6A1F] font-bold px-2 py-0.5 rounded-full">แก้เคสค้าง</span>
              </div>
              <p class="text-[11px] text-neutral-500 leading-relaxed">
                กรณี Messenger เน็ตหลุด/แบตหมด หรือลืมกด แต่หน้างานจริงส่งมอบกุญแจแล้ว สามารถเลือกวิธียืนยันด้านล่างเพื่อ <strong>บังคับเลื่อนสถานะ (Force Advance)</strong> ให้ระบบทำงานต่อได้ทันที:
              </p>

              <!-- ปุ่ม Action 4 ปุ่ม -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                <!-- 1. ปุ่มพี่ลิลลี่ Override -->
                <button type="button" onclick="overrideKeyStep('admin_handover')" class="bg-amber-600 hover:bg-amber-700 text-white font-bold p-2.5 rounded-xl text-xs flex items-center justify-center gap-1.5 transition shadow-xs cursor-pointer">
                  <span>🔑</span>
                  <span>พี่ลิลลี่ บังคับส่งมอบ (โทรเช็คแล้ว)</span>
                </button>

                <!-- 2. ปุ่ม Agent กดยืนยันสวนทาง -->
                <button type="button" onclick="overrideKeyStep('agent_confirm')" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold p-2.5 rounded-xl text-xs flex items-center justify-center gap-1.5 transition shadow-xs cursor-pointer">
                  <span>📲</span>
                  <span>Agent กดยืนยัน: ได้กุญแจแล้ว</span>
                </button>

                <!-- 3. ปุ่มปิดเคสส่งคืนกุญแจ -->
                <button type="button" onclick="overrideKeyStep('complete_return')" class="bg-neutral-900 hover:bg-black text-white font-bold p-2.5 rounded-xl text-xs flex items-center justify-center gap-1.5 transition shadow-xs cursor-pointer">
                  <span>🔒</span>
                  <span>บันทึกส่งคืน & ปิดล็อกบ้าน</span>
                </button>

                <!-- 4. ปุ่มรีเซ็ตสำหรับจำลองใหม่ -->
                <button type="button" onclick="overrideKeyStep('reset')" class="bg-white hover:bg-neutral-100 text-neutral-700 border border-neutral-300 font-semibold p-2.5 rounded-xl text-xs flex items-center justify-center gap-1.5 transition cursor-pointer">
                  <span>🔄</span>
                  <span>รีเซ็ตสถานะเพื่อสาธิตใหม่</span>
                </button>
              </div>

              <!-- บันทึก Audit Log ทันทีที่กด -->
              <div id="key-override-log" class="hidden text-[11px] text-emerald-800 bg-emerald-50 border border-emerald-200/80 rounded-xl p-2.5 flex items-center gap-2">
                <span class="w-4 h-4 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] font-bold shrink-0">✓</span>
                <span id="key-override-log-text">ปลดล็อคสถานะสำเร็จ</span>
              </div>
            </div>

            <!-- Messenger Contact Card -->
            <div class="bg-white border border-neutral-200/80 rounded-2xl p-3 flex items-center justify-between text-xs shadow-2xs">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-full bg-neutral-100 flex items-center justify-center text-neutral-600 font-bold">🛵</div>
                <div>
                  <div class="font-bold text-neutral-900">คุณสมชาย (Messenger ศิวาทรัพย์)</div>
                  <div class="text-[11px] text-neutral-500">โทร 089-224-xxxx • Honda Wave ดำ-แดง</div>
                </div>
              </div>
              <a href="tel:089224xxxx" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 font-bold px-3 py-1.5 rounded-xl text-xs flex items-center gap-1 transition-all">
                <i data-lucide="phone" class="w-3.5 h-3.5"></i>
                <span>โทร</span>
              </a>
            </div>
          </div>

          <!-- TAB 3: Admin Lily Audit & Agent Trust Score -->
          <div id="npa-tab-audit" class="hidden space-y-3">
            <div class="bg-gradient-to-br from-neutral-900 to-neutral-800 text-white p-3.5 rounded-2xl space-y-2 shadow-xs">
              <div class="flex justify-between items-center text-xs">
                <span class="text-neutral-400">ตัวแทนที่เบิกกุญแจ</span>
                <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/40 text-[10px] font-bold px-2.5 py-0.5 rounded-full">Fast-Track Trusted</span>
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <div class="font-bold text-base">ภมรมาศ (Agent S02 / บัว)</div>
                  <div class="text-xs text-neutral-400">ประวัติเบิกกุญแจ: 18 ครั้ง | กุญแจหาย: 0 ครั้ง</div>
                </div>
                <div class="text-right">
                  <div class="text-2xl font-black text-[#C2A460]">96 <span class="text-xs font-normal text-neutral-400">/ 100</span></div>
                  <div class="text-[10px] text-neutral-400">Trust Score</div>
                </div>
              </div>
            </div>

            <!-- Quick Scoring by Lily -->
            <div class="space-y-1.5 text-xs">
              <div class="font-bold text-neutral-900 flex items-center gap-1">
                <i data-lucide="award" class="w-3.5 h-3.5 text-[#C2A460]"></i>
                <span>แผงตัดเกรด & บันทึกคะแนนโดยพี่ลิลลี่ (1-Click Audit):</span>
              </div>
              <div class="grid grid-cols-2 gap-1.5">
                <button type="button" onclick="rateAgentDemo('punctual')" class="bg-white hover:bg-emerald-50 border border-neutral-200 hover:border-emerald-300 p-2 rounded-xl text-left transition-all">
                  <div class="font-bold text-emerald-700 text-xs">+5 ⭐ ตรงเวลาดีเยี่ยม</div>
                  <div class="text-[10px] text-neutral-400">มารอ Messenger ตามนัด</div>
                </button>
                <button type="button" onclick="rateAgentDemo('keysafe')" class="bg-white hover:bg-emerald-50 border border-neutral-200 hover:border-emerald-300 p-2 rounded-xl text-left transition-all">
                  <div class="font-bold text-emerald-700 text-xs">+5 🔑 กุญแจครบ 100%</div>
                  <div class="text-[10px] text-neutral-400">ล็อกบ้าน ปิดน้ำไฟเรียบร้อย</div>
                </button>
                <button type="button" onclick="rateAgentDemo('report')" class="bg-white hover:bg-sky-50 border border-neutral-200 hover:border-sky-300 p-2 rounded-xl text-left transition-all">
                  <div class="font-bold text-sky-700 text-xs">+3 📝 รีพอร์ตผลไว</div>
                  <div class="text-[10px] text-neutral-400">ส่ง Feedback ลูกค้าใน 24 ชม.</div>
                </button>
                <button type="button" onclick="rateAgentDemo('late')" class="bg-white hover:bg-rose-50 border border-neutral-200 hover:border-rose-300 p-2 rounded-xl text-left transition-all">
                  <div class="font-bold text-rose-700 text-xs">-5 ⚠️ มาสาย > 20 นาที</div>
                  <div class="text-[10px] text-neutral-400">Messenger ต้องยืนรอ</div>
                </button>
              </div>
            </div>

            <div class="text-[11px] text-neutral-600 bg-[#FAF8F5] border border-[#E8DFD1] rounded-2xl p-2.5">
              <strong>เกณฑ์ระบบ:</strong> Agent ที่มีคะแนนเกิน 85 แต้มจะได้รับสิทธิ์ <em>Fast-Track</em> เบิกกุญแจฟรีโดยไม่ต้องวางเงินประกัน 1,000 บาท หากคะแนนต่ำกว่า 70 แต้ม ระบบจะระงับการเบิกอัตโนมัติ
            </div>
          </div>
        </div>

        <!-- 3. Sticky Bottom Bar: ปุ่มยืนยัน + ปุ่มปิดด้านล่าง -->
        <div class="p-3.5 bg-white border-t border-neutral-100 flex items-center gap-2 shrink-0">
          <button 
            type="button"
            onclick="closeNpaKeyModal()"
            class="px-4 py-2.5 rounded-xl bg-neutral-100 hover:bg-neutral-200 text-neutral-700 text-xs font-semibold transition cursor-pointer"
          >
            ปิดหน้าต่าง
          </button>
          <button 
            type="button"
            onclick="submitNpaKeyRequestDemo()"
            class="flex-1 py-2.5 px-4 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-white text-xs font-semibold shadow-xs transition cursor-pointer flex items-center justify-center gap-1.5"
          >
            <i data-lucide="key" class="w-3.5 h-3.5"></i>
            <span>ยืนยันคำขอเบิกกุญแจ</span>
          </button>
        </div>

      </div>
    </div>

    <!-- 📅 Admin Appointments & Showing Queue Modal (สำหรับบัว, กูล, พี่ลิลลี่) -->
    <div id="admin-appointments-modal" onclick="if(event.target === this) closeAdminCaseAppointments()" class="hidden modal-backdrop fixed inset-0 z-[110] bg-neutral-950/65 backdrop-blur-xs flex items-center justify-center px-3 pt-6 pb-6 sm:p-6">
      <div class="relative w-full max-w-lg max-h-[85dvh] bg-white rounded-3xl shadow-2xl border border-neutral-200/90 flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        <!-- Header -->
        <div class="sticky top-0 z-30 px-5 py-4 bg-white/95 backdrop-blur-md border-b border-neutral-100 flex items-center justify-between shrink-0">
          <div class="flex items-center gap-3 min-w-0 pr-2">
            <div class="w-9 h-9 rounded-xl bg-neutral-900 text-[#E5C985] flex items-center justify-center text-sm shadow-xs shrink-0 font-bold">
              <i data-lucide="calendar" class="w-4 h-4 text-[#C2A460]"></i>
            </div>
            <div class="min-w-0">
              <h3 class="text-sm sm:text-base font-bold text-neutral-900 tracking-tight leading-tight truncate">คิวนัดหมายเข้าชมบ้าน & ลีดผู้ซื้อ</h3>
              <p class="text-[10px] sm:text-xs text-neutral-500 truncate">ระบบติดตามสำหรับผู้บริหาร • บัว, กูล, พี่ลิลลี่</p>
            </div>
          </div>
          <button type="button" onclick="closeAdminCaseAppointments()" aria-label="ปิดหน้าต่าง" class="w-9 h-9 rounded-full bg-neutral-900/80 hover:bg-neutral-900 text-white backdrop-blur-md flex items-center justify-center transition-all shadow-md active:scale-90 cursor-pointer shrink-0">
            <i data-lucide="x" class="w-5 h-5 stroke-[2.2]"></i>
          </button>
        </div>

        <!-- Body -->
        <div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 custom-scrollbar">
          
          <!-- Property Mini Info -->
          <div class="bg-neutral-50 border border-neutral-200/80 rounded-2xl p-3 flex items-center justify-between gap-3 text-xs">
            <div class="min-w-0">
              <div class="text-[10px] text-neutral-400 font-mono" id="admin-app-prop-id">#1069562</div>
              <div class="font-bold text-neutral-900 truncate text-xs sm:text-sm" id="admin-app-prop-title">คอนโด เซ็นทริค ซีน รัชวิภา</div>
              <div class="text-[11px] text-[#8C6D23] font-semibold mt-0.5" id="admin-app-prop-price">฿3,410,000</div>
            </div>
            <span class="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 shrink-0">
              เปิดให้เข้าชม
            </span>
          </div>

          <!-- Key Location Live Status Box -->
          <div class="bg-gradient-to-r from-neutral-900 to-neutral-800 text-white p-3.5 rounded-2xl border border-neutral-700/60 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="text-neutral-400 flex items-center gap-1.5 font-semibold">
                <i data-lucide="key" class="w-3.5 h-3.5 text-[#C2A460]"></i>
                <span>สถานะกุญแจปัจจุบัน (Key Custody):</span>
              </span>
              <span id="admin-app-key-status-badge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/40">
                พร้อมส่งมอบ (In Vault)
              </span>
            </div>
            <div class="text-xs text-neutral-200 leading-relaxed" id="admin-app-key-desc">
              ตำแหน่ง: <strong>ตู้เซฟสำนักงานใหญ่ ชั้น 2 (กล่อง A-14)</strong> • ดอกจริง 2 ดอก + คีย์การ์ด 1 ใบ ครบ 100%
            </div>
          </div>

          <!-- Timeline Showing Queue -->
          <div class="space-y-2.5">
            <div class="flex items-center justify-between text-xs font-bold text-neutral-800">
              <span>รายการนัดหมายเข้าชมบ้านจริง (Showing Queue):</span>
              <span class="text-[11px] text-[#8B0000] font-semibold">2 นัดหมายรอเข้าชม</span>
            </div>

            <!-- Case Item 1 -->
            <div class="bg-white border border-neutral-200/90 rounded-2xl p-3.5 space-y-2 shadow-2xs hover:border-[#C2A460]/60 transition">
              <div class="flex items-center justify-between text-xs">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-neutral-900 text-[#E5C985] text-[10px] font-bold flex items-center justify-center">S22</span>
                  <div>
                    <div class="font-bold text-neutral-900">คุณสมชาย พาเจริญ (Falcon Hunter)</div>
                    <div class="text-[10px] text-neutral-400">โทร 086-333-2211</div>
                  </div>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                  ยืนยันแล้ว
                </span>
              </div>
              <div class="text-xs text-neutral-700 pt-1.5 border-t border-neutral-100 flex items-center justify-between">
                <span>📅 <strong>วันนี้ 14:00 น.</strong> (นัดชมห้องจริง)</span>
                <span class="text-neutral-500">ผู้จะซื้อ: คุณวิชัย นพรัตน์</span>
              </div>
              <div class="text-[11px] text-neutral-500 bg-neutral-50 p-2 rounded-xl">
                💬 <strong>บันทึกลีด:</strong> ลูกค้าทำงาน SCB สำนักงานใหญ่ สนใจกู้ร่วม 2 คน เตรียมเอกสารยื่น Pre-Approve
              </div>
            </div>

            <!-- Case Item 2 -->
            <div class="bg-white border border-neutral-200/90 rounded-2xl p-3.5 space-y-2 shadow-2xs hover:border-[#C2A460]/60 transition">
              <div class="flex items-center justify-between text-xs">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-[#8B0000] text-[#E5C985] text-[10px] font-bold flex items-center justify-center">SW</span>
                  <div>
                    <div class="font-bold text-neutral-900">คุณอัครวินท์ (SW-001 Master Partner)</div>
                    <div class="text-[10px] text-neutral-400">โทร 092-555-8899</div>
                  </div>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">
                  รอยืนยันเวลา
                </span>
              </div>
              <div class="text-xs text-neutral-700 pt-1.5 border-t border-neutral-100 flex items-center justify-between">
                <span>📅 <strong>พรุ่งนี้ 10:30 น.</strong> (นัดชมห้องจริง)</span>
                <span class="text-neutral-500">ผู้จะซื้อ: คุณพัชราภา วงศ์สุวรรณ</span>
              </div>
              <div class="text-[11px] text-neutral-500 bg-neutral-50 p-2 rounded-xl">
                💬 <strong>บันทึกลีด:</strong> ผู้ซื้อเงินสด ซื้อลงทุนปล่อยเช่า พร้อมวางเงินทำสัญญาหากห้องสภาพตรงตามรูป
              </div>
            </div>

          </div>

        </div>

        <!-- Footer Actions -->
        <div class="p-3.5 bg-white border-t border-neutral-100 flex items-center justify-between gap-2 shrink-0">
          <button type="button" onclick="closeAdminCaseAppointments()" class="px-4 py-2 rounded-xl bg-neutral-100 hover:bg-neutral-200 text-neutral-700 text-xs font-semibold transition cursor-pointer">
            ปิดหน้าต่าง
          </button>
          <button type="button" onclick="closeAdminCaseAppointments(); openNpaKeyModal(currentAdminAppPropId, 'track');" class="px-4 py-2 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-[#E5C985] text-xs font-bold transition cursor-pointer flex items-center gap-1.5 shadow-xs">
            <i data-lucide="key" class="w-3.5 h-3.5 text-[#C2A460]"></i>
            <span>ตรวจดูสถานะกุญแจเคสนี้</span>
          </button>
        </div>

      </div>
    </div>

    <!-- Copy Share Toast -->
    <div id="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-4 py-2 rounded-full shadow-lg opacity-0 transition-opacity pointer-events-none z-50">
      ก๊อปปี้เรียบร้อย!
    </div>
  `;

  function mountModals() {
    const root = document.getElementById('modals-root');
    if (root && !root.dataset.mounted) {
      root.innerHTML = modalHTML;
      root.dataset.mounted = 'true';
      if (window.lucide) {
        lucide.createIcons();
      }
    }
  }

  // Execute immediately if root element already exists in DOM, else await DOMContentLoaded
  if (document.getElementById('modals-root')) {
    mountModals();
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountModals);
  } else {
    mountModals();
  }
})();
