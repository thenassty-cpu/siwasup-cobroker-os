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
          <button onclick="closeBookingModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
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
          <button type="submit" class="w-full bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 rounded-lg text-sm shadow-xs flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="check" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ยืนยันส่งข้อมูลให้แอดมิน (เจี๊ยบ/บัว) ตรวจสอบ</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Smart Share Center Modal (Omni-Channel Share) -->
    <div id="share-modal" class="hidden modal-backdrop !items-center !p-3 sm:!p-4 z-50" onclick="if(event.target === this) closeShareModal()">
      <div id="share-modal-card" class="modal-card no-scrollbar w-full max-w-md transition-all duration-300 p-4 sm:p-5 my-auto overflow-hidden">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5 mb-2.5">
          <h3 class="font-bold text-sm sm:text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5 bg-amber-50 text-amber-700 border border-amber-200"><i data-lucide="share-2" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>Smart Share Center</span>
            <span class="text-[10px] text-amber-800 font-normal hidden sm:inline">(เลือกลิงก์โปรโมท)</span>
          </h3>
          <button onclick="closeShareModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold leading-none p-1">&times;</button>
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
    <div id="mobile-qr-modal" class="hidden modal-backdrop !items-center !p-4 z-[60]" onclick="if(event.target === this) closeMobileQrModal()">
      <div class="modal-card-sm no-scrollbar space-y-3 text-center bg-white border border-amber-200 shadow-2xl p-4 rounded-2xl max-w-[320px] mx-auto animate-fadeIn">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="font-bold text-xs text-gray-800 flex items-center gap-1.5 text-left">
            <span class="icon-circle w-5 h-5 bg-amber-50 text-amber-700 border border-amber-200">
              <i data-lucide="qr-code" class="w-3 h-3 stroke-[1.5]"></i>
            </span>
            <span>QR Code สำหรับสแกน</span>
          </div>
          <button onclick="closeMobileQrModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold leading-none p-1">&times;</button>
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
    <div id="call-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3 text-center">
        <div class="icon-circle w-12 h-12 bg-amber-900/60 text-[#D4AF37] mx-auto">
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
    <div id="inquiry-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="calendar" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>ขอนัดหมายเข้าชมห้องจริง / ปรึกษาสินเชื่อ</span>
          </h3>
          <button onclick="closeInquiryModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
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
          <button type="submit" class="w-full bg-[#B89D68] hover:bg-[#A38854] text-white font-bold py-2.5 rounded-xl shadow-xs text-xs mt-2 flex items-center justify-center gap-1.5 active:scale-95 transition-all">
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
        <button onclick="adminApproveBooking()" class="flex-1 bg-[#D4AF37] hover:bg-[#c49f2b] text-gray-950 font-bold py-1.5 rounded text-center shadow-xs flex items-center justify-center gap-1.5">
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
          <button onclick="closeConsignModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
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

          <button type="submit" class="w-full bg-[#B89D68] hover:bg-[#A38854] text-white font-bold py-2.5 rounded-xl shadow-xs text-xs mt-2 flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ยืนยันส่งข้อมูลฝากขาย (ฟรี)</span>
          </button>
        </form>
      </div>
    </div>

    <!-- 🤝 Member Get Member (MGM) Referral Modal -->
    <div id="mgm-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3.5">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="users" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>ชวนเพื่อนมาเป็น Agent (MGM)</span>
          </h3>
          <button onclick="closeMgmModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <div class="bg-gray-50 border border-gray-200 p-2.5 rounded-xl text-xs space-y-1 text-gray-800 border-l-4 border-[#D4AF37]">
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
    <div id="offer-modal" class="hidden modal-backdrop !items-center !p-3 sm:!p-4">
      <div class="modal-card max-w-2xl space-y-3.5 max-h-[94vh] overflow-y-auto custom-scrollbar !p-4 sm:!p-5">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-2">
            <span class="icon-circle w-6 h-6 bg-neutral-900 text-white"><i data-lucide="badge-dollar-sign" class="w-3.5 h-3.5 stroke-[1.8]"></i></span>
            <div>
              <h3 class="font-extrabold text-base text-slate-900 leading-tight">เสนอราคา</h3>
              <p class="text-[11px] text-slate-500">กรอกราคาที่ต้องการเสนอและข้อมูลติดต่อเพื่อดำเนินการยื่นข้อเสนอซื้อ</p>
            </div>
          </div>
          <button onclick="closeOfferModal()" class="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center text-lg font-bold">&times;</button>
        </div>

        <!-- Property Summary Banner -->
        <div id="offer-prop-info" class="bg-slate-50 border border-slate-200/90 p-3 rounded-2xl text-xs"></div>

        <form id="homerun-offer-form" onsubmit="handleOfferSubmit(event)" class="grid grid-cols-1 md:grid-cols-12 gap-4 text-xs" novalidate>
          <!-- Left Column: Offer Price & Buyer Details (Homerun Layout) -->
          <div class="md:col-span-7 space-y-3">
            <!-- รูปแบบที่ต้องการซื้อ (เงินสด / สินเชื่อ) -->
            <div>
              <label class="block font-bold text-slate-700 mb-1.5">รูปแบบที่ต้องการซื้อ <span class="text-red-500">*</span></label>
              <div class="grid grid-cols-2 gap-2">
                <label class="cursor-pointer">
                  <input type="radio" name="offer_PurchaseType" value="เงินสด" checked class="peer sr-only" onchange="updateOfferSummaryBox()">
                  <div class="p-2 rounded-xl border border-slate-200 bg-white peer-checked:border-neutral-900 peer-checked:bg-neutral-50 peer-checked:text-neutral-900 font-bold text-center transition-all flex items-center justify-center gap-1.5">
                    <i data-lucide="banknote" class="w-3.5 h-3.5"></i>
                    <span>ซื้อเงินสด</span>
                  </div>
                </label>
                <label class="cursor-pointer">
                  <input type="radio" name="offer_PurchaseType" value="สินเชื่อธนาคาร" class="peer sr-only" onchange="updateOfferSummaryBox()">
                  <div class="p-2 rounded-xl border border-slate-200 bg-white peer-checked:border-neutral-900 peer-checked:bg-neutral-50 peer-checked:text-neutral-900 font-bold text-center transition-all flex items-center justify-center gap-1.5">
                    <i data-lucide="landmark" class="w-3.5 h-3.5"></i>
                    <span>ขอสินเชื่อ</span>
                  </div>
                </label>
              </div>
            </div>

            <!-- ราคาที่ต้องการเสนอ (พร้อมปุ่มกดเลือกช่วงราคาอัตโนมัติ & ล็อกเพดานขั้นต่ำ 70%) -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <label for="offer-price" class="font-bold text-slate-700">ราคาที่เสนอ (บาท) <span class="text-red-500">*</span></label>
                <span id="offer-discount-badge" class="text-[10px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">ระบุราคาที่ต้องการ</span>
              </div>
              <div class="relative">
                <span class="absolute left-3 top-2.5 font-extrabold text-slate-400 text-sm">฿</span>
                <input type="number" id="offer-price" required min="50000" step="1000"
                       oninput="updateOfferSummaryBox()"
                       placeholder="เช่น 2,850,000"
                       class="w-full border border-slate-300 rounded-xl py-2 pl-7 pr-3 outline-none focus:ring-2 focus:ring-neutral-900 focus:border-neutral-900 font-extrabold text-base text-neutral-900 bg-white">
              </div>
              <!-- Quick Offer Chips -->
              <div class="flex flex-wrap items-center gap-1.5 mt-1.5">
                <span class="text-[10px] text-slate-400">กดเลือกไว:</span>
                <button type="button" onclick="setQuickOfferRatio(1.0)" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 hover:bg-sky-50 text-slate-700 hover:text-neutral-900 border border-slate-200 transition-colors">ราคาตั้ง (โอกาสได้สูงสุด)</button>
                <button type="button" onclick="setQuickOfferRatio(0.95)" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#FAF7F2] hover:bg-[#F3EDE2] text-[#8C734B] border border-[#DFD3C3] transition-colors">-5% (แนะนำ)</button>
                <button type="button" onclick="setQuickOfferRatio(0.90)" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 hover:bg-sky-50 text-slate-700 hover:text-neutral-900 border border-slate-200 transition-colors">-10%</button>
                <button type="button" onclick="setQuickOfferRatio(0.85)" class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 hover:bg-sky-50 text-slate-700 hover:text-neutral-900 border border-slate-200 transition-colors">-15%</button>
              </div>
              <p id="offer-price-hint" class="text-[10px] text-slate-400 mt-1">🛡️ ระบบล็อกเกณฑ์เสนอซื้อขั้นต่ำที่ 70% ของราคาตั้งขาย เพื่อป้องกันการปั่นราคา</p>
            </div>

            <!-- ชื่อ - นามสกุล (แยกช่องตามแบบ Homerun) -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              <div>
                <label for="offer-firstname" class="block font-bold text-slate-700 mb-1">ชื่อ <span class="text-red-500">*</span></label>
                <input type="text" id="offer-firstname" required placeholder="กรอกชื่อจริง"
                       oninput="updateOfferSummaryBox()"
                       class="w-full border border-slate-300 rounded-xl p-2 outline-none focus:ring-2 focus:ring-neutral-900 bg-white">
              </div>
              <div>
                <label for="offer-lastname" class="block font-bold text-slate-700 mb-1">นามสกุล <span class="text-red-500">*</span></label>
                <input type="text" id="offer-lastname" required placeholder="กรอกนามสกุล"
                       oninput="updateOfferSummaryBox()"
                       class="w-full border border-slate-300 rounded-xl p-2 outline-none focus:ring-2 focus:ring-neutral-900 bg-white">
              </div>
            </div>

            <!-- อีเมล - เบอร์โทร (ตามแบบ Homerun + ตรวจจับเบอร์ไทยแท้ 10 หลัก) -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              <div>
                <label for="offer-email" class="block font-bold text-slate-700 mb-1">อีเมล <span class="text-red-500">*</span></label>
                <input type="email" id="offer-email" required placeholder="name@email.com"
                       oninput="updateOfferSummaryBox()"
                       class="w-full border border-slate-300 rounded-xl p-2 outline-none focus:ring-2 focus:ring-neutral-900 bg-white">
              </div>
              <div>
                <label for="offer-phone" class="block font-bold text-slate-700 mb-1">เบอร์โทรศัพท์ <span class="text-red-500">*</span></label>
                <input type="tel" id="offer-phone" required pattern="^0[689][0-9]{8}$" maxlength="10"
                       placeholder="08xxxxxxxx (10 หลัก)"
                       oninput="this.value = this.value.replace(/[^0-9]/g, ''); updateOfferSummaryBox();"
                       class="w-full border border-slate-300 rounded-xl p-2 outline-none focus:ring-2 focus:ring-neutral-900 bg-white">
              </div>
            </div>

            <!-- 🍯 Honeypot Bot Trap (ซ่อนจากคนจริง ดักจับสคริปต์บอทยิงฟอร์ม) -->
            <div class="hidden" aria-hidden="true">
              <label for="offer-company-website">Website</label>
              <input type="text" id="offer-company-website" name="company_website" tabindex="-1" autocomplete="off">
            </div>

            <!-- เงื่อนไขเพิ่มเติม -->
            <div>
              <label for="offer-terms" class="block font-medium text-slate-600 mb-1">เงื่อนไขเพิ่มเติม (ถ้ามี)</label>
              <input type="text" id="offer-terms" placeholder="เช่น พร้อมวางมัดจำภายใน 3 วัน / ต้องการปรึกษาสินเชื่อ"
                     oninput="updateOfferSummaryBox()"
                     class="w-full border border-slate-200 rounded-xl p-2 outline-none focus:ring-2 focus:ring-neutral-900 bg-slate-50/60">
            </div>

            <!-- ข้อกำหนดและเงื่อนไข -->
            <label class="flex items-start gap-2 pt-0.5 cursor-pointer text-[11px] text-slate-600">
              <input type="checkbox" id="offer-consent" required checked class="mt-0.5 rounded text-neutral-900 focus:ring-neutral-900">
              <span>ข้าพเจ้ายืนยันความประสงค์ในการเสนอราคาซื้อทรัพย์สินข้างต้น และยินยอมให้เจ้าหน้าที่ศิวาทรัพย์ติดต่อกลับเพื่อดำเนินการด้านเอกสาร</span>
            </label>
          </div>

          <!-- Bottom-Right Column: Replaces Homerun's "ช่องทางการชำระเงิน -> QR Code" with LINE Official ศิวาทรัพย์ -->
          <div class="md:col-span-5 flex flex-col justify-between bg-gradient-to-b from-slate-50 to-emerald-50/40 border border-slate-200 rounded-2xl p-3.5 space-y-3">
            <div class="space-y-2.5">
              <!-- Summary Breakdown -->
              <div class="bg-white rounded-xl p-2.5 border border-slate-200/80 space-y-1.5">
                <div class="text-[11px] font-bold text-slate-700 border-b border-slate-100 pb-1">สรุปรายการเสนอราคา</div>
                <div class="flex justify-between items-center text-[11px]">
                  <span class="text-slate-500">ราคาก่อนต่อรอง</span>
                  <span id="offer-summary-original" class="font-semibold text-slate-700 line-through">฿0</span>
                </div>
                <div class="flex justify-between items-center text-xs">
                  <span class="text-slate-700 font-bold">ราคาที่ท่านเสนอ</span>
                  <span id="offer-summary-proposed" class="font-black text-neutral-900 text-sm">฿0</span>
                </div>
                <div class="flex justify-between items-center text-[11px] pt-1 border-t border-dashed border-slate-200">
                  <span class="text-slate-500">หลักประกันการเสนอราคา</span>
                  <span id="offer-summary-deposit" class="font-bold text-slate-900">฿50,000</span>
                </div>
              </div>

              <!-- Bottom-Right Channel Box (LINE Official instead of QR Code) -->
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span id="offer-line-box-header" class="font-bold text-slate-800 text-xs">ช่องทางยืนยันและวางหลักประกัน</span>
                  <span class="text-[9.5px] bg-neutral-100 text-neutral-700 font-bold px-2 py-0.5 rounded-full">LINE Official</span>
                </div>

                <!-- Interactive Wording Selector for Bua & Team to test live -->
                <div id="offer-wording-selector-box" class="bg-amber-50/90 border border-amber-200 rounded-xl p-2 space-y-1">
                  <div class="text-[10px] font-bold text-amber-900 flex items-center gap-1">
                    <i data-lucide="sparkles" class="w-3 h-3 text-amber-600"></i>
                    <span>ตัวเลือกคำพูดปุ่มมุมขวาล่าง (ให้บัวเลือกเทียบ):</span>
                  </div>
                  <select id="offer-cta-wording-preset" onchange="applyOfferLineWordingPreset(this.value)" class="w-full border border-amber-300 rounded-lg p-1 text-[10px] bg-white font-semibold text-slate-800 outline-none">
                    <option value="option1" selected>แบบที่ 1: ยืนยันใบเสนอราคา & วางหลักประกันผ่าน LINE (แนะนำ)</option>
                    <option value="option2">แบบที่ 2: ติดต่อเจ้าหน้าที่เพื่อรับใบวางหลักประกันทาง LINE</option>
                    <option value="option3">แบบที่ 3: ส่งข้อเสนอซื้อและชำระเงินมัดจำผ่าน LINE ศิวาทรัพย์</option>
                    <option value="option4">แบบที่ 4: ประสานงานยื่นข้อเสนอราคาผ่าน LINE Official</option>
                  </select>
                </div>

                <!-- Active LINE Channel Card (Replacing Homerun's QR Code Radio Card) -->
                <div class="p-3 rounded-xl border border-neutral-200 bg-white shadow-2xs space-y-2 hover:border-emerald-500/60 transition">
                  <div class="flex items-start gap-2.5">
                    <div class="w-8 h-8 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center justify-center shrink-0 font-bold text-xs">
                      L
                    </div>
                    <div class="min-w-0 flex-1">
                      <div id="offer-line-card-title" class="font-extrabold text-slate-900 text-xs leading-snug">
                        ยืนยันใบเสนอราคา & วางหลักประกันผ่าน LINE
                      </div>
                      <div id="offer-line-card-desc" class="text-[10.5px] text-slate-500 leading-relaxed mt-0.5">
                        ส่งรายละเอียดราคาที่เสนอเข้า LINE ศิวาทรัพย์ (@siwasup) เพื่อรับเอกสารใบเสนอซื้อและเลขบัญชีวางหลักประกันโดยตรง
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Document Download Box inside Offer Modal (Role-aware) -->
              <div id="offer-modal-docs-box" class="bg-white border border-slate-200 rounded-xl p-2.5 space-y-1.5"></div>
            </div>

            <!-- Submit & Open LINE Button -->
            <div class="pt-1 space-y-1.5">
              <button type="submit" id="offer-submit-btn" class="w-full bg-white hover:bg-neutral-50 border border-neutral-200 hover:border-emerald-500 text-neutral-900 font-bold py-3 px-3 rounded-xl shadow-2xs text-xs flex items-center justify-center gap-2 active:scale-95 transition-all">
                <span class="w-4 h-4 rounded-full bg-[#06C755] text-white flex items-center justify-center text-[9px] font-black shrink-0">L</span>
                <span id="offer-submit-btn-text">ส่งใบเสนอราคาผ่าน LINE ศิวาทรัพย์</span>
              </button>
              <p class="text-[10px] text-center text-slate-400">ระบบจะสรุปข้อมูลใบเสนอราคาและเปิดแชท LINE @siwasup อัตโนมัติ</p>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- 📥 Owner Leads Management Modal (สำหรับแอดมินบัว/เจี๊ยบ) -->
    <div id="owner-leads-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card space-y-3.5">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="inbox" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>รายการทรัพย์ฝากขายใหม่ (Lead Magnet)</span>
          </h3>
          <button onclick="closeOwnerLeadsModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <div id="owner-leads-container" class="space-y-2 text-xs">
          <!-- Dynamically populated -->
        </div>
      </div>
    </div>

    <!-- 💰 Edit Price Modal (สำหรับเจ้าของ/แอดมิน บัว & กูล) -->
    <div id="edit-price-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3.5">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="edit-3" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>แก้ไขราคาขาย (แอดมิน บัว & กูล)</span>
          </h3>
          <button onclick="closeEditPriceModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
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
          <button onclick="closeBundleModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
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
          <button onclick="closeVinylModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
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
                       class="w-full border rounded-lg p-1.5 text-xs font-bold text-[#967C3E] outline-none focus:ring-1 focus:ring-amber-600 bg-amber-50/20">
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

          <!-- Download Action Buttons -->
          <div class="grid grid-cols-2 gap-2 pt-1">
            <button type="button" onclick="downloadVinylPDF()" class="bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
              <span class="icon-circle w-4 h-4"><i data-lucide="download" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
              <span>โหลด PDF ส่งโรงพิมพ์</span>
            </button>
            <button type="button" onclick="downloadVinylJPG()" class="bg-gray-900 hover:bg-black text-white font-bold py-2.5 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
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

    <!-- Homerun-Style Clean Property Detail Modal -->
    <div id="property-detail-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card max-w-lg space-y-4 max-h-[92vh] overflow-y-auto">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-2">
            <span id="detail-category-badge" class="capsule-bokeh text-[11px] font-medium px-3 py-0.5">ทาวน์โฮม</span>
            <span id="detail-bank-badge"></span>
            <span id="detail-code" class="text-xs text-slate-400 font-mono">รหัส: -</span>
          </div>
          <button onclick="closePropertyDetailModal()" class="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center text-lg font-bold">&times;</button>
        </div>

        <!-- Detail Image Carousel / Hero -->
        <div class="relative aspect-[16/10] bg-slate-100 rounded-2xl overflow-hidden shadow-inner">
          <img id="detail-main-img" src="" alt="" class="w-full h-full object-cover">
          <div class="absolute bottom-2.5 left-2.5">
            <span id="detail-status-pill" class="bg-[#FF3838] text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full shadow-sm">New</span>
          </div>
          <a id="detail-external-link" href="#" target="_blank" class="absolute bottom-2.5 right-2.5 capsule-bokeh hover:bg-slate-900/70 text-white text-[11px] font-medium px-3 py-1 flex items-center gap-1 shadow-sm">
            <i data-lucide="external-link" class="w-3 h-3"></i>
            <span>ดูหน้าเว็บเดิม</span>
          </a>
        </div>

        <!-- Title & Location -->
        <div class="space-y-1">
          <h2 id="detail-title" class="font-bold text-slate-900 text-base md:text-lg leading-snug"></h2>
          <div class="flex items-center gap-1.5 text-xs text-slate-500">
            <i data-lucide="map-pin" class="w-3.5 h-3.5 text-slate-400 shrink-0"></i>
            <span id="detail-location">กรุงเทพฯ และปริมณฑล</span>
          </div>
        </div>

        <!-- Homerun Specs Grid -->
        <div class="grid grid-cols-2 gap-2 bg-slate-50/80 p-3 rounded-2xl border border-slate-100 text-xs">
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-500">
              <i data-lucide="grid" class="w-3.5 h-3.5"></i>
            </div>
            <div>
              <div class="text-[10px] text-slate-400">เนื้อที่</div>
              <div id="detail-size" class="font-bold text-slate-800">43.9 ตร.ว.</div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-500">
              <i data-lucide="home" class="w-3.5 h-3.5"></i>
            </div>
            <div>
              <div class="text-[10px] text-slate-400">พื้นที่ใช้สอย</div>
              <div id="detail-usable" class="font-bold text-slate-800">110 ตร.ม.</div>
            </div>
          </div>
        </div>

        <!-- Description -->
        <p id="detail-desc" class="text-xs text-slate-600 leading-relaxed bg-white border border-slate-100 p-3 rounded-2xl"></p>

        <!-- 🔑 NPA Key & Messenger Banner (Employee, Agent & Owner) -->
        <div id="detail-npa-key-banner" class="bg-neutral-50 border border-neutral-200/80 rounded-2xl p-3 flex items-center justify-between gap-2 shadow-2xs">
          <div class="flex items-center gap-2.5 min-w-0">
            <div class="w-9 h-9 rounded-xl bg-neutral-900 text-white flex items-center justify-center shrink-0 shadow-xs">
              <i data-lucide="key" class="w-4 h-4"></i>
            </div>
            <div class="min-w-0">
              <div class="font-bold text-xs text-sky-950 flex items-center gap-1.5">
                <span>บริการเบิกกุญแจ NPA & Messenger</span>
                <span class="text-[9px] bg-sky-200/80 text-sky-900 px-1.5 py-0.2 rounded font-bold">พี่ลิลลี่</span>
              </div>
              <div class="text-[10.5px] text-sky-700 truncate">มี Messenger วิ่งรับกุญแจจากแบงก์ส่งมอบหน้างาน</div>
            </div>
          </div>
          <button type="button" id="detail-btn-banner-npa-key" onclick="" class="shrink-0 bg-neutral-900 hover:bg-neutral-800 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-2xs flex items-center gap-1 transition-all active:scale-95">
            <span>ขอนัดชม</span>
            <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
          </button>
        </div>

        <!-- Financial Breakdown (Homerun Style) -->
        <div class="bg-neutral-50 p-3.5 rounded-2xl border border-neutral-200/80 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-600 flex items-center gap-1.5">
              <span class="w-4 h-4 rounded-full border border-neutral-300 text-neutral-600 font-bold text-[10px] inline-flex items-center justify-center leading-none select-none">฿</span>
              <span>ราคาก่อนต่อรอง</span>
            </span>
            <span id="detail-price" class="text-lg font-black text-neutral-900 tracking-tight">฿3,410,000</span>
          </div>
          <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-200/60">
            <span class="text-slate-500 flex items-center gap-1.5">
              <span class="w-4 h-4 rounded-full border border-slate-400 text-slate-600 font-bold text-[11px] inline-flex items-center justify-center leading-none select-none">฿</span>
              <span>หลักประกันเพื่อต่อรองราคา</span>
            </span>
            <span id="detail-deposit" class="font-bold text-slate-800">฿50,000</span>
          </div>
          <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-200/60">
            <span class="text-slate-500 flex items-center gap-1.5">
              <i data-lucide="calculator" class="w-3.5 h-3.5 text-emerald-600"></i>
              <span>ประมาณการผ่อนต่อเดือน</span>
            </span>
            <span id="detail-installment" class="font-bold text-emerald-700">~ 12,000 บ./เดือน</span>
          </div>
        </div>

        <!-- 📄 Role-Based Document Downloads (Admin/Agent gets all Bank Offer PDFs; Client gets Sales Contract) -->
        <div id="detail-documents-section" class="bg-slate-50/90 border border-slate-200/80 p-3.5 rounded-2xl space-y-2 text-xs">
          <!-- Populated dynamically by renderPropertyDocumentDownloads(prop) based on currentMode -->
        </div>

        <!-- Primary Homerun-Style Action Bar -->
        <div class="space-y-2 pt-1">
          <div id="detail-agent-actions-row" class="space-y-1.5">
            <div class="grid grid-cols-2 gap-2">
              <button id="detail-btn-vinyl" onclick="" class="w-full bg-amber-50 hover:bg-amber-100 text-[#8C6D23] font-bold py-2.5 rounded-full border border-amber-300 text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
                <i data-lucide="printer" class="w-4 h-4 text-amber-600"></i>
                <span>พิมพ์ป้ายไวนิล (Auto PDF)</span>
              </button>
              <button id="detail-btn-share" onclick="" class="w-full bg-neutral-900 hover:bg-neutral-800 text-white font-bold py-2.5 rounded-full shadow-xs text-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
                <i data-lucide="share-2" class="w-4 h-4"></i>
                <span>แชร์ล็อกสิทธิ์ (3-5%)</span>
              </button>
            </div>
            <button id="detail-btn-npa-key" onclick="" class="w-full bg-sky-50 hover:bg-sky-100 text-neutral-900 font-bold py-2 rounded-full border border-sky-300 text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
              <i data-lucide="key" class="w-3.5 h-3.5 text-neutral-900"></i>
              <span>เบิกกุญแจ NPA & ติดตาม Messenger (Demo พี่ลิลลี่)</span>
            </button>
          </div>
          <button id="detail-btn-offer" onclick="" class="w-full bg-[#BFA267] hover:bg-[#b09257] text-white font-bold py-3 rounded-full shadow-xs flex items-center justify-center gap-2 text-sm active:scale-95 transition-all">
            <i data-lucide="badge-dollar-sign" class="w-4 h-4"></i>
            <span id="detail-btn-offer-label">เสนอราคา</span>
          </button>
          <div id="detail-waitlist-row" class="hidden"></div>
        </div>
      </div>
    </div>

    <!-- 🏆 Agent Directory & Leaderboard Modal (125 Agents: S02-S126) -->
    <div id="agent-leaderboard-modal" class="hidden modal-backdrop !items-center !p-3">
      <div class="modal-card max-w-xl space-y-3.5 max-h-[92vh] overflow-y-auto custom-scrollbar !p-4">
        <!-- Header -->
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-2">
            <span class="icon-circle w-7 h-7 bg-amber-500 text-white"><i data-lucide="trophy" class="w-4 h-4 stroke-[1.5]"></i></span>
            <div>
              <h3 class="font-bold text-sm sm:text-base text-gray-900 leading-tight">ทำเนียบตัวแทน & Leaderboard</h3>
              <p class="text-[10px] text-gray-500">ระบบวัดผลอัตโนมัติ 2 แทร็ก (กิจกรรม & ผลงาน) • 125 ท่าน</p>
            </div>
          </div>
          <button onclick="closeAgentLeaderboardModal()" class="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center text-lg font-bold">&times;</button>
        </div>

        <!-- Quick Action Bar for Admins & Agents -->
        <div class="grid grid-cols-2 gap-2 bg-gradient-to-r from-amber-50/60 to-red-50/60 p-2.5 rounded-xl border border-amber-200/60">
          <button type="button" onclick="openMeetingCheckinModal()" class="bg-white hover:bg-amber-50 text-amber-900 border border-amber-300 font-bold py-1.5 px-2 rounded-lg text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <i data-lucide="qr-code" class="w-3.5 h-3.5 text-amber-600"></i>
            <span>🎟️ QR เช็คชื่อเข้าประชุม (+10)</span>
          </button>
          <button type="button" onclick="openVinylProofModal()" class="bg-[#990000] hover:bg-red-800 text-white font-bold py-1.5 px-2 rounded-lg text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <i data-lucide="camera" class="w-3.5 h-3.5"></i>
            <span>📸 ส่งภาพติดป้าย GPS (+15)</span>
          </button>
        </div>

        <!-- 👑 Owner-Only Animal Intelligence Matrix Bar (Visible ONLY when currentMode === 'owner') -->
        <div id="owner-animal-intelligence-bar" class="hidden bg-gradient-to-r from-amber-50 via-yellow-50 to-orange-50 p-3 rounded-2xl border-2 border-amber-300 space-y-2 shadow-xs">
          <div class="flex items-center justify-between text-xs">
            <span class="font-bold text-amber-950 flex items-center gap-1.5">
              <span class="w-5 h-5 rounded-full bg-amber-400 text-amber-950 font-black flex items-center justify-center text-[11px] shadow-2xs">🐾</span>
              <span>วิเคราะห์ศักยภาพตัวแทน 4 กลุ่ม (เฉพาะแอดมิน/บัว & กูล)</span>
            </span>
            <span class="text-[9.5px] bg-amber-200 text-amber-900 font-bold px-2 py-0.5 rounded-full border border-amber-300">Admin Only</span>
          </div>

          <!-- 4 Animal Filter Tabs -->
          <div class="grid grid-cols-4 gap-1 text-[10px] font-bold">
            <button type="button" id="animal-btn-all" onclick="filterByAnimal('all')" class="p-1.5 rounded-xl border border-amber-400 bg-amber-400 text-amber-950 shadow-2xs text-center transition-all">
              <div>ทั้งหมด</div>
              <div class="text-[9px] font-normal">125 ท่าน</div>
            </button>
            <button type="button" id="animal-btn-eagle" onclick="filterByAnimal('eagle')" class="p-1.5 rounded-xl border border-amber-200 bg-white text-amber-900 shadow-2xs text-center transition-all hover:bg-amber-100/60 active:scale-95 flex flex-col items-center justify-center">
              <div class="flex items-center justify-center gap-1">
                <span class="w-3.5 h-3.5 inline-flex items-center justify-center text-amber-600">${window.SiwasupAgents ? window.SiwasupAgents.getAnimalSvg('eagle', 'w-full h-full') : '🦅'}</span>
                <span>Eagle</span>
              </div>
              <div class="text-[9px] text-amber-700 font-normal"><span id="animal-count-eagle">0</span> ท่าน</div>
            </button>
            <button type="button" id="animal-btn-lion" onclick="filterByAnimal('lion')" class="p-1.5 rounded-xl border border-purple-200 bg-white text-purple-900 shadow-2xs text-center transition-all hover:bg-purple-100/60 active:scale-95 flex flex-col items-center justify-center">
              <div class="flex items-center justify-center gap-1">
                <span class="w-3.5 h-3.5 inline-flex items-center justify-center text-purple-600">${window.SiwasupAgents ? window.SiwasupAgents.getAnimalSvg('lion', 'w-full h-full') : '🦁'}</span>
                <span>Lion</span>
              </div>
              <div class="text-[9px] text-purple-700 font-normal"><span id="animal-count-lion">0</span> ท่าน</div>
            </button>
            <button type="button" id="animal-btn-wolf" onclick="filterByAnimal('wolf')" class="p-1.5 rounded-xl border border-blue-200 bg-white text-blue-900 shadow-2xs text-center transition-all hover:bg-blue-100/60 active:scale-95 flex flex-col items-center justify-center">
              <div class="flex items-center justify-center gap-1">
                <span class="w-3.5 h-3.5 inline-flex items-center justify-center text-blue-600">${window.SiwasupAgents ? window.SiwasupAgents.getAnimalSvg('wolf', 'w-full h-full') : '🐺'}</span>
                <span>Wolf</span>
              </div>
              <div class="text-[9px] text-blue-700 font-normal"><span id="animal-count-wolf">0</span> ท่าน</div>
            </button>
          </div>

          <!-- Bear full width row -->
          <div class="text-[10px] font-bold bg-white/90 p-1.5 rounded-xl border border-slate-200">
            <button type="button" id="animal-btn-bear" onclick="filterByAnimal('bear')" class="w-full text-slate-700 flex items-center justify-between px-1 hover:text-slate-900 transition-colors">
              <span class="flex items-center gap-1.5">
                <span class="w-4 h-4 inline-flex items-center justify-center text-slate-600">${window.SiwasupAgents ? window.SiwasupAgents.getAnimalSvg('bear', 'w-full h-full') : '🐻'}</span>
                <span><strong>Hibernating Bear (หมีจำศีล)</strong></span>
                <span class="text-[9px] text-gray-400 font-normal hidden sm:inline">- สมาชิกพักรบ รอจังหวะปลุกพลัง</span>
              </span>
              <span class="bg-slate-100 px-2 py-0.5 rounded-full border border-slate-300 text-slate-800 font-mono"><span id="animal-count-bear">0</span> ท่าน</span>
            </button>
          </div>

          <!-- Strategy & Archetype Visual Banner -->
          <div id="animal-strategy-box" class="bg-white p-2.5 rounded-xl border border-amber-200 text-[10.5px] text-gray-700 leading-snug space-y-1.5">
            <div class="flex items-start gap-2.5">
              <img src="assets/animal_archetypes_terracotta.jpg" alt="Animal Archetypes" class="w-14 h-14 rounded-lg object-cover border border-amber-200 shadow-2xs shrink-0 cursor-pointer hover:scale-105 transition-transform" onclick="window.open('assets/animal_archetypes_terracotta.jpg', '_blank')" title="คลิกดูภาพขยายสัญลักษณ์ 4 สัตว์">
              <div class="min-w-0 flex-1">
                <div class="font-bold text-amber-900 flex items-center gap-1">
                  <span>💡 คำแนะนำเชิงบริหารสำหรับบัว:</span>
                </div>
                <div id="animal-strategy-title" class="font-bold text-xs text-amber-950 mt-0.5">ตัวแทนทั้งหมด 125 ท่าน</div>
                <div id="animal-strategy-desc" class="text-gray-600 text-[10px] mt-0.5">
                  คัดกรองตัวแทนเพื่อส่งต่อทรัพย์ให้ตรงมือ หรือส่งโค้ชไปประกบปิดการขาย (คลิกเลือกปุ่มสัตว์ด้านบน)
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Top 3 Podium Cards -->
        <div id="leaderboard-podium" class="grid grid-cols-3 gap-1.5 sm:gap-2 text-center pt-1">
          <!-- Injected via JS -->
        </div>

        <!-- Filter Tracks & Search -->
        <div class="space-y-2 pt-1 border-t border-gray-100">
          <div class="flex items-center justify-between gap-1 text-[11px]">
            <div class="flex items-center gap-1 bg-gray-100 p-0.5 rounded-lg border border-gray-200">
              <button id="lb-tab-total" onclick="filterLeaderboard('total')" class="py-1 px-2.5 rounded-md font-bold bg-white text-gray-900 shadow-2xs transition-all">รวมทุกแต้ม</button>
              <button id="lb-tab-activity" onclick="filterLeaderboard('activity')" class="py-1 px-2 rounded-md font-medium text-gray-600 hover:text-gray-900 transition-all">🎪 กิจกรรม</button>
              <button id="lb-tab-performance" onclick="filterLeaderboard('performance')" class="py-1 px-2 rounded-md font-medium text-gray-600 hover:text-gray-900 transition-all">💰 ผลงาน</button>
            </div>
            <span id="lb-count-label" class="text-[10px] text-gray-400 font-mono">125 ตัวแทน</span>
          </div>

          <!-- Search Input -->
          <div class="relative">
            <input type="text" id="lb-search-input" oninput="searchLeaderboard(this.value)" 
                   placeholder="ค้นหา: รหัส S02-S126, ชื่อเล่น, หรือชื่อจริง..." 
                   class="w-full bg-gray-50 border border-gray-200 rounded-lg pl-8 pr-3 py-1.5 text-xs outline-none focus:ring-1 focus:ring-red-700">
            <span class="absolute left-2.5 top-2 text-gray-400">
              <i data-lucide="search" class="w-3.5 h-3.5"></i>
            </span>
          </div>
        </div>

        <!-- Leaderboard Table List -->
        <div id="leaderboard-list" class="space-y-1.5 max-h-[52vh] sm:max-h-[58vh] overflow-y-auto custom-scrollbar pr-2">
          <!-- Injected via JS -->
        </div>
      </div>
    </div>

    <!-- 🎟️ Meeting QR Check-in Modal -->
    <div id="modal-meeting-checkin" class="hidden modal-backdrop !items-center !p-3">
      <div class="modal-card max-w-sm space-y-3.5 !p-4 text-center">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-1.5">
            <span class="icon-circle w-6 h-6 bg-amber-600 text-white"><i data-lucide="calendar-check" class="w-3.5 h-3.5"></i></span>
            <h3 class="font-bold text-sm text-gray-900">เช็คชื่อเข้าอบรม / ประชุมทีม</h3>
          </div>
          <button onclick="closeMeetingCheckinModal()" class="w-6 h-6 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center font-bold">&times;</button>
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
            <span>ยืนยันเช็คชื่อรับ +10 แต้ม</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 📸 Vinyl Photo + GPS Proof Modal -->
    <div id="modal-vinyl-proof" class="hidden modal-backdrop !items-center !p-3">
      <div class="modal-card max-w-sm space-y-3.5 !p-4">
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-1.5">
            <span class="icon-circle w-6 h-6 bg-emerald-600 text-white"><i data-lucide="camera" class="w-3.5 h-3.5"></i></span>
            <div>
              <h3 class="font-bold text-sm text-gray-900 leading-tight">ส่งภาพติดป้ายหน้างานจริง</h3>
              <p class="text-[9.5px] text-gray-500">Proof of Installation • รับทันที +15 แต้ม</p>
            </div>
          </div>
          <button onclick="closeVinylProofModal()" class="w-6 h-6 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center font-bold">&times;</button>
        </div>

        <form onsubmit="submitVinylProof(event)" class="space-y-2.5 text-xs">
          <!-- Agent Selection -->
          <div>
            <label class="block font-medium mb-1 text-gray-700">รหัสตัวแทนผู้ติดป้าย:</label>
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
            <label class="block font-medium mb-1 text-gray-700">ภาพถ่ายป้ายที่ผูกหน้าบ้าน:</label>
            <input type="file" id="proof-photo-file" accept="image/*" capture="environment" required 
                   class="w-full text-[11px] text-gray-500 file:mr-2 file:py-1 file:px-2.5 file:rounded-lg file:border-0 file:text-[11px] file:font-semibold file:bg-emerald-100 file:text-emerald-800 hover:file:bg-emerald-200">
          </div>

          <button type="submit" class="w-full bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 px-3 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <i data-lucide="upload-cloud" class="w-3.5 h-3.5"></i>
            <span>ยืนยันส่งผลงานรับ +15 แต้ม</span>
          </button>
        </form>
      </div>
    </div>

    <!-- 👤 My Profile & Scorecard Modal -->
    <div id="modal-my-profile" class="hidden modal-backdrop !items-center !p-3">
      <div class="modal-card max-w-md space-y-3.5 max-h-[92vh] overflow-y-auto no-scrollbar !p-4">
        <!-- Header -->
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-2">
            <span class="icon-circle w-7 h-7 bg-amber-500 text-white"><i data-lucide="user-check" class="w-4 h-4 stroke-[1.5]"></i></span>
            <div>
              <h3 class="font-bold text-sm sm:text-base text-gray-900 leading-tight">โปรไฟล์ตัวแทน & กระเป๋าคะแนน</h3>
              <p class="text-[10px] text-gray-500">Siwasup Co-Broker Agent Scorecard</p>
            </div>
          </div>
          <button onclick="closeMyProfileModal()" class="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center text-lg font-bold">&times;</button>
        </div>

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
            <div id="profile-avatar-circle" class="w-14 h-14 rounded-2xl bg-siwasup-gold text-gray-950 font-black text-lg flex items-center justify-center shadow-xs border-2 border-white shrink-0">
              S22
            </div>
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-1.5 flex-wrap">
                <span id="profile-nickname" class="font-black text-base text-gray-900">เจ็ม</span>
                <span id="profile-code-pill" class="text-[10px] font-mono font-bold bg-gray-900 text-white px-2 py-0.5 rounded-full">S22</span>
                <span id="profile-tier-badge" class="text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300 px-2 py-0.5 rounded-full">🥇 Gold Agent</span>
              </div>
              <div id="profile-fullname" class="text-xs text-gray-600 truncate mt-0.5">นางสาวกันยาวีร์ กำธรศิริวัฒน์</div>
              <div id="profile-start-date" class="text-[10px] text-gray-400 mt-0.5">เริ่มงาน: 8 มีนาคม 2566</div>
            </div>
          </div>

          <!-- Contact Details Grid -->
          <div class="grid grid-cols-2 gap-1.5 text-[11px] pt-1 border-t border-amber-100/80">
            <div class="flex items-center gap-1.5 text-gray-700 bg-white/70 p-1.5 rounded-lg border border-amber-100/60 truncate">
              <i data-lucide="phone" class="w-3 h-3 text-emerald-600 shrink-0"></i>
              <span id="profile-phone" class="font-mono font-bold truncate">06-2396-5161</span>
            </div>
            <div class="flex items-center gap-1.5 text-gray-700 bg-white/70 p-1.5 rounded-lg border border-amber-100/60 truncate">
              <i data-lucide="message-circle" class="w-3 h-3 text-emerald-600 shrink-0"></i>
              <span id="profile-line" class="truncate font-medium">@siwasup</span>
            </div>
          </div>

          <!-- Tier Progress Bar -->
          <div class="space-y-1 pt-1 border-t border-amber-100/80">
            <div class="flex justify-between items-center text-[10.5px]">
              <span class="font-bold text-gray-700 flex items-center gap-1">
                <span>เลื่อนสู่</span>
                <span id="profile-next-tier-name" class="text-purple-700 font-bold">💎 Diamond Master</span>
              </span>
              <span id="profile-tier-progress-text" class="font-mono text-gray-500 font-bold">765 / 1,000 แต้ม</span>
            </div>
            <div class="w-full bg-gray-200/80 rounded-full h-2 overflow-hidden shadow-inner">
              <div id="profile-tier-progress-bar" class="bg-gradient-to-r from-amber-500 to-purple-600 h-2 rounded-full transition-all duration-500" style="width: 76.5%;"></div>
            </div>
            <p id="profile-tier-perk" class="text-[9.5px] text-gray-500 italic">สิทธิพิเศษ: สิทธิ์จองทรัพย์ Hot Deals ล่วงหน้า 24 ชม.</p>
          </div>
        </div>

        <!-- 👑 Owner-Only Intelligence Analysis Card (Visible only when currentMode === 'owner') -->
        <div id="profile-owner-intelligence-box" class="hidden p-3 rounded-2xl bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-300 space-y-1.5 text-xs shadow-2xs">
          <div class="flex items-center justify-between">
            <span class="font-bold text-amber-950 flex items-center gap-1.5">
              <span class="w-4 h-4 rounded-full bg-amber-400 text-amber-950 font-black flex items-center justify-center text-[10px]">🐾</span>
              <span>วิเคราะห์สไตล์ตัวแทน (เฉพาะเจ้าของ / แอดมิน)</span>
            </span>
            <span id="profile-animal-badge" class="px-2 py-0.5 rounded-full font-bold text-[10px] bg-blue-100 text-blue-900 border border-blue-300">🐺 Wolf</span>
          </div>
          <div id="profile-animal-desc" class="text-[11px] text-gray-700 font-medium"></div>
          <div class="p-2 rounded-xl bg-white border border-amber-200 text-[10.5px] text-amber-950">
            <strong>🎯 แนะนำสำหรับบัว:</strong> <span id="profile-animal-action"></span>
          </div>
        </div>

        <!-- 2-Track Points Scorecard Grid -->
        <div class="grid grid-cols-2 gap-2 text-center text-xs">
          <!-- Activity Track -->
          <div class="bg-emerald-50/70 p-2.5 rounded-xl border border-emerald-200/80 space-y-0.5">
            <div class="text-[10px] text-emerald-700 font-bold flex items-center justify-center gap-1">
              <span>🎪 คะแนนกิจกรรม</span>
            </div>
            <div id="profile-activity-pts" class="text-xl font-black text-emerald-800 font-mono">145</div>
            <div class="text-[9px] text-emerald-600">ประชุม / ไวนิล / แชร์</div>
          </div>

          <!-- Performance Track -->
          <div class="bg-blue-50/70 p-2.5 rounded-xl border border-blue-200/80 space-y-0.5">
            <div class="text-[10px] text-blue-700 font-bold flex items-center justify-center gap-1">
              <span>💰 คะแนนผลงาน</span>
            </div>
            <div id="profile-perf-pts" class="text-xl font-black text-blue-800 font-mono">620</div>
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
          <div id="profile-total-pts" class="text-2xl font-black font-mono text-amber-300">765</div>
        </div>

        <!-- Quick Action Buttons -->
        <div class="grid grid-cols-2 gap-2 pt-1">
          <button type="button" onclick="closeMyProfileModal(); openMeetingCheckinModal();" class="bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold py-2 px-2 rounded-xl text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <i data-lucide="qr-code" class="w-3.5 h-3.5 text-amber-600"></i>
            <span>เช็คชื่อเข้าประชุม (+10)</span>
          </button>
          <button type="button" onclick="closeMyProfileModal(); openVinylProofModal();" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold py-2 px-2 rounded-xl text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
            <i data-lucide="camera" class="w-3.5 h-3.5 text-emerald-600"></i>
            <span>ส่งภาพติดป้าย GPS (+15)</span>
          </button>
        </div>

        <!-- View Full Leaderboard Link -->
        <button type="button" onclick="closeMyProfileModal(); openAgentLeaderboardModal();" class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold py-2 px-3 rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all active:scale-95">
          <i data-lucide="trophy" class="w-3.5 h-3.5 text-amber-600"></i>
          <span>ดูอันดับในทำเนียบตัวแทน (Leaderboard 125)</span>
        </button>
      </div>
    </div>

    <!-- 🔑 NPA Key Dispatch & Messenger Tracking Modal (Demo Prototype) -->
    <div id="npa-key-dispatch-modal" class="hidden modal-backdrop !items-center !p-3">
      <div class="modal-card max-w-xl space-y-3.5 max-h-[92vh] overflow-y-auto custom-scrollbar !p-4">
        <!-- Header -->
        <div class="flex justify-between items-center bg-white border-b border-neutral-100 pb-2.5">
          <div class="flex items-center gap-2">
            <span class="w-8 h-8 rounded-full bg-sky-50 text-neutral-900 flex items-center justify-center font-bold">
              <i data-lucide="key" class="w-4 h-4"></i>
            </span>
            <div>
              <div class="font-bold text-gray-900 text-sm flex items-center gap-1.5">
                <span>ระบบเบิกกุญแจ NPA & ติดตาม Messenger</span>
                <span class="bg-amber-100 text-amber-800 text-[10px] font-bold px-2 py-0.5 rounded-full border border-amber-200">Demo Prototype</span>
              </div>
              <div class="text-[11px] text-gray-500">ผู้รับผิดชอบงานเบิก-คืนกุญแจ NPA: <strong class="text-gray-700">พี่ลิลลี่ (Admin ศิวาทรัพย์)</strong></div>
            </div>
          </div>
          <button type="button" onclick="closeNpaKeyModal()" class="w-7 h-7 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-500 flex items-center justify-center font-bold text-sm transition-colors">&times;</button>
        </div>

        <!-- Development Status Notice -->
        <div class="bg-amber-50/80 border border-amber-200/90 rounded-xl p-2.5 text-xs text-amber-900 flex items-start gap-2">
          <i data-lucide="info" class="w-4 h-4 text-amber-600 shrink-0 mt-0.5"></i>
          <div class="leading-relaxed">
            <strong>สถานะระบบ:</strong> ระบบเบิกกุญแจและประเมินคะแนนตัวแทนนี้เป็นแบบจำลอง (Demo) รอการประชุมสรุปข้อกำหนดร่วมกับ <strong>กูล, บัว และพี่ลิลลี่</strong> เพิ่มเติม (รอ <em>Argon</em> กลับมาพัฒนาต่อ)
          </div>
        </div>

        <!-- Tab Switcher -->
        <div class="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl text-xs font-semibold">
          <button type="button" id="tab-npa-btn-req" onclick="switchNpaKeyTab('req')" class="py-1.5 px-1 rounded-lg bg-white text-slate-800 shadow-2xs text-center transition-all">1. ยื่นขอเบิก (Agent)</button>
          <button type="button" id="tab-npa-btn-track" onclick="switchNpaKeyTab('track')" class="py-1.5 px-1 rounded-lg text-slate-500 hover:text-slate-800 text-center transition-all">2. ติดตาม Messenger</button>
          <button type="button" id="tab-npa-btn-audit" onclick="switchNpaKeyTab('audit')" class="py-1.5 px-1 rounded-lg text-slate-500 hover:text-slate-800 text-center transition-all">3. ตรวจสอบ (พี่ลิลลี่)</button>
        </div>

        <!-- TAB 1: Agent Key Request Form -->
        <div id="npa-tab-req" class="space-y-3">
          <div class="bg-slate-50 border border-slate-200/80 rounded-xl p-3 space-y-2 text-xs">
            <div class="font-bold text-slate-800 flex items-center justify-between">
              <span>ข้อมูลทรัพย์ NPA ที่ต้องการเบิกกุญแจ</span>
              <span id="npa-req-bank" class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-100 text-sky-800">SCB</span>
            </div>
            <div id="npa-req-prop-title" class="font-semibold text-slate-700 text-xs truncate">ทาวน์โฮม 3 ชั้น รีโนเวทพร้อมอยู่</div>
            <div class="text-[11px] text-slate-500">รหัสทรัพย์: <span id="npa-req-prop-id" class="font-mono font-bold text-slate-700">#1069562</span></div>
          </div>

          <div class="space-y-2.5 text-xs">
            <div>
              <label class="block font-semibold text-slate-700 mb-1">เวลานัดหมายพาลูกค้าเข้าชมหน้างาน</label>
              <div class="grid grid-cols-2 gap-2">
                <input type="date" id="npa-date" class="w-full bg-white border border-slate-200 rounded-xl px-2.5 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-neutral-900">
                <input type="time" id="npa-time" value="14:00" class="w-full bg-white border border-slate-200 rounded-xl px-2.5 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-neutral-900">
              </div>
              <div class="mt-1 text-[11px] text-emerald-700 flex items-center gap-1 font-medium">
                <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i>
                <span>แจ้งล่วงหน้า 24 ชม. (ผ่านเกณฑ์ Fast-Track เบิกกุญแจทันที)</span>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block font-semibold text-slate-700 mb-1">ชื่อผู้จะซื้อ (ลูกค้า)</label>
                <input type="text" id="npa-client-name" placeholder="คุณสมชาย ใจดี" class="w-full bg-white border border-slate-200 rounded-xl px-2.5 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-neutral-900">
              </div>
              <div>
                <label class="block font-semibold text-slate-700 mb-1">เบอร์โทรลูกค้า</label>
                <input type="tel" id="npa-client-phone" placeholder="08x-xxx-xxxx" class="w-full bg-white border border-slate-200 rounded-xl px-2.5 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-neutral-900">
              </div>
            </div>

            <div class="bg-sky-50/70 border border-sky-100 rounded-xl p-2.5 text-[11px] text-sky-900 space-y-1">
              <div class="font-bold flex items-center gap-1 text-neutral-900">
                <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
                <span>ข้อตกลงและนโยบายการเบิกกุญแจธนาคาร</span>
              </div>
              <ul class="list-disc list-inside space-y-0.5 text-slate-600 pl-1">
                <li>Messenger จะนำกุญแจไปส่งมอบให้ Agent ณ จุดนัดพบหน้าทรัพย์</li>
                <li>Agent ต้องตรวจนับดอกกุญแจและเซ็นรับมอบต่อหน้า Messenger</li>
                <li>เมื่อชมเสร็จ ต้องล็อกบ้านเรียบร้อยและส่งมอบกุญแจคืนทันที (ไม่เกิน 24 ชม.)</li>
              </ul>
            </div>
          </div>

          <button type="button" onclick="submitNpaKeyRequestDemo()" class="w-full bg-neutral-900 hover:bg-neutral-800 text-white font-bold py-2.5 rounded-full text-xs shadow-xs flex items-center justify-center gap-1.5 transition-all active:scale-95">
            <i data-lucide="send" class="w-3.5 h-3.5"></i>
            <span>ยื่นคำขอเบิกกุญแจถึงพี่ลิลลี่ (Admin)</span>
          </button>
        </div>

        <!-- TAB 2: Messenger & Bank Live Tracker -->
        <div id="npa-tab-track" class="hidden space-y-3">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-slate-800">สถานะคำขอเบิกกุญแจ #KEY-2026-089</span>
              <span class="bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full text-[10px]">กำลังวิ่งส่ง</span>
            </div>
            
            <!-- Stepper -->
            <div class="space-y-2 pt-1 text-xs">
              <div class="flex items-center gap-2.5">
                <span class="w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] font-bold">✓</span>
                <span class="text-slate-700">10:00 น. - Agent ยื่นคำขอเบิกกุญแจเข้าระบบ</span>
              </div>
              <div class="flex items-center gap-2.5">
                <span class="w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] font-bold">✓</span>
                <span class="text-slate-700">10:30 น. - <strong>พี่ลิลลี่</strong> ตรวจสอบเอกสาร & อนุมัติใบส่งตัวธนาคาร</span>
              </div>
              <div class="flex items-center gap-2.5">
                <span class="w-5 h-5 rounded-full bg-sky-600 text-white flex items-center justify-center text-[10px] font-bold animate-pulse">🛵</span>
                <span class="font-bold text-sky-800">13:15 น. - Messenger (พี่สมชาย) รับกุญแจจาก สนง.ใหญ่ กำลังวิ่งไปหน้างาน</span>
              </div>
              <div class="flex items-center gap-2.5 text-slate-400">
                <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-500 flex items-center justify-center text-[10px] font-bold">4</span>
                <span>รอส่งมอบกุญแจให้ Agent ณ หน้าบ้าน (นัด 14:00 น.)</span>
              </div>
              <div class="flex items-center gap-2.5 text-slate-400">
                <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-500 flex items-center justify-center text-[10px] font-bold">5</span>
                <span>รอรับกุญแจคืน & ถ่ายรูปยืนยันปิดล็อกบ้าน</span>
              </div>
            </div>
          </div>

          <!-- Messenger Contact Card -->
          <div class="bg-white border border-slate-200 rounded-xl p-3 flex items-center justify-between text-xs shadow-2xs">
            <div class="flex items-center gap-2.5">
              <div class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 font-bold">🛵</div>
              <div>
                <div class="font-bold text-slate-800">คุณสมชาย (Messenger ศิวาทรัพย์)</div>
                <div class="text-[11px] text-slate-500">โทร 089-224-xxxx • Honda Wave ดำ-แดง</div>
              </div>
            </div>
            <a href="tel:089224xxxx" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1">
              <i data-lucide="phone" class="w-3.5 h-3.5"></i>
              <span>โทร</span>
            </a>
          </div>
        </div>

        <!-- TAB 3: Admin Lily Audit & Agent Trust Score -->
        <div id="npa-tab-audit" class="hidden space-y-3">
          <div class="bg-gradient-to-br from-slate-900 to-slate-800 text-white p-3.5 rounded-2xl space-y-2">
            <div class="flex justify-between items-center text-xs">
              <span class="text-slate-300">ตัวแทนที่เบิกกุญแจ</span>
              <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-400/40 text-[10px] font-bold px-2.5 py-0.5 rounded-full">Fast-Track Trusted</span>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <div class="font-bold text-base">ภมรมาศ (Agent S02 / บัว)</div>
                <div class="text-xs text-slate-300">ประวัติเบิกกุญแจ: 18 ครั้ง | กุญแจหาย: 0 ครั้ง</div>
              </div>
              <div class="text-right">
                <div class="text-2xl font-black text-[#C2A460]">96 <span class="text-xs font-normal text-slate-400">/ 100</span></div>
                <div class="text-[10px] text-slate-300">Trust Score</div>
              </div>
            </div>
          </div>

          <!-- Quick Scoring by Lily -->
          <div class="space-y-1.5 text-xs">
            <div class="font-bold text-slate-800 flex items-center gap-1">
              <i data-lucide="award" class="w-3.5 h-3.5 text-amber-600"></i>
              <span>แผงตัดเกรด & บันทึกคะแนนโดยพี่ลิลลี่ (1-Click Audit):</span>
            </div>
            <div class="grid grid-cols-2 gap-1.5">
              <button type="button" onclick="rateAgentDemo('punctual')" class="bg-white hover:bg-emerald-50 border border-slate-200 hover:border-emerald-300 p-2 rounded-xl text-left transition-all">
                <div class="font-bold text-emerald-700 text-xs">+5 ⭐ ตรงเวลาดีเยี่ยม</div>
                <div class="text-[10px] text-slate-400">มารอ Messenger ตามนัด</div>
              </button>
              <button type="button" onclick="rateAgentDemo('keysafe')" class="bg-white hover:bg-emerald-50 border border-slate-200 hover:border-emerald-300 p-2 rounded-xl text-left transition-all">
                <div class="font-bold text-emerald-700 text-xs">+5 🔑 กุญแจครบ 100%</div>
                <div class="text-[10px] text-slate-400">ล็อกบ้าน ปิดน้ำไฟเรียบร้อย</div>
              </button>
              <button type="button" onclick="rateAgentDemo('report')" class="bg-white hover:bg-sky-50 border border-slate-200 hover:border-sky-300 p-2 rounded-xl text-left transition-all">
                <div class="font-bold text-sky-700 text-xs">+3 📝 รีพอร์ตผลไว</div>
                <div class="text-[10px] text-slate-400">ส่ง Feedback ลูกค้าใน 24 ชม.</div>
              </button>
              <button type="button" onclick="rateAgentDemo('late')" class="bg-white hover:bg-rose-50 border border-slate-200 hover:border-rose-300 p-2 rounded-xl text-left transition-all">
                <div class="font-bold text-rose-700 text-xs">-5 ⚠️ มาสาย > 20 นาที</div>
                <div class="text-[10px] text-slate-400">Messenger ต้องยืนรอ</div>
              </button>
            </div>
          </div>

          <div class="text-[11px] text-slate-500 bg-slate-50 border border-slate-200 rounded-xl p-2.5">
            <strong>เกณฑ์ระบบ:</strong> Agent ที่มีคะแนนเกิน 85 แต้มจะได้รับสิทธิ์ <em>Fast-Track</em> เบิกกุญแจฟรีโดยไม่ต้องวางเงินประกัน 1,000 บาท หากคะแนนต่ำกว่า 70 แต้ม ระบบจะระงับการเบิกอัตโนมัติ
          </div>
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
