import re

repo = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
with open(repo + r"\agent_registration.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace from <!-- AUTH MODE SELECTOR TABS --> to <!-- STATE 1.8: LOGGED IN MEMBER PORTAL
start_marker = "    <!-- AUTH MODE SELECTOR TABS -->"
end_marker = "    <!-- ============================================================== -->\n    <!-- STATE 1.8: LOGGED IN MEMBER PORTAL"
if end_marker not in html:
    end_marker = "    <!-- ============================================================== -->\r\n    <!-- STATE 1.8: LOGGED IN MEMBER PORTAL"

assert start_marker in html, "start_marker not found"
assert end_marker in html, "end_marker not found"

stepper_and_forms = """    <!-- ============================================================== -->
    <!-- 4-STEP VISUAL PROGRESS STEPPER (แทนที่ระบบ Tab เดิมทั้งหมด) -->
    <!-- ============================================================== -->
    <div id="regStepperBar" class="card-light rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-sm">
      <div class="relative flex items-start justify-between">
        <!-- Connecting Track Line -->
        <div class="absolute top-5 left-8 right-8 h-1.5 bg-slate-200 rounded-full overflow-hidden z-0">
          <div id="stepperProgressFill" class="h-full bg-gradient-to-r from-emerald-500 via-amber-500 to-amber-400 transition-all duration-500" style="width: 0%;"></div>
        </div>

        <!-- Step 1 Node -->
        <button type="button" onclick="tryClickStep(1)" class="relative z-10 flex flex-col items-center gap-1.5 w-1/4 group focus:outline-none">
          <div id="stepCircle1" class="w-10 h-10 rounded-full flex items-center justify-center font-black text-sm transition-all duration-300 bg-amber-500 text-slate-950 ring-4 ring-amber-400/30 shadow-md">
            1
          </div>
          <div class="text-center">
            <div id="stepLabel1" class="text-[10px] sm:text-xs font-black text-slate-900 leading-tight">Step 1</div>
            <div class="text-[9px] sm:text-[10px] text-slate-500 leading-tight">เชื่อม LINE</div>
          </div>
        </button>

        <!-- Step 2 Node -->
        <button type="button" onclick="tryClickStep(2)" class="relative z-10 flex flex-col items-center gap-1.5 w-1/4 group focus:outline-none">
          <div id="stepCircle2" class="w-10 h-10 rounded-full flex items-center justify-center font-black text-sm transition-all duration-300 bg-slate-200 text-slate-500 border-2 border-white">
            2
          </div>
          <div class="text-center">
            <div id="stepLabel2" class="text-[10px] sm:text-xs font-bold text-slate-400 leading-tight">Step 2</div>
            <div class="text-[9px] sm:text-[10px] text-slate-400 leading-tight">ข้อมูลส่วนตัว</div>
          </div>
        </button>

        <!-- Step 3 Node -->
        <button type="button" onclick="tryClickStep(3)" class="relative z-10 flex flex-col items-center gap-1.5 w-1/4 group focus:outline-none">
          <div id="stepCircle3" class="w-10 h-10 rounded-full flex items-center justify-center font-black text-sm transition-all duration-300 bg-slate-200 text-slate-500 border-2 border-white">
            3
          </div>
          <div class="text-center">
            <div id="stepLabel3" class="text-[10px] sm:text-xs font-bold text-slate-400 leading-tight">Step 3</div>
            <div class="text-[9px] sm:text-[10px] text-slate-400 leading-tight">เลือกโซนงาน</div>
          </div>
        </button>

        <!-- Step 4 Node -->
        <button type="button" onclick="tryClickStep(4)" class="relative z-10 flex flex-col items-center gap-1.5 w-1/4 group focus:outline-none">
          <div id="stepCircle4" class="w-10 h-10 rounded-full flex items-center justify-center font-black text-sm transition-all duration-300 bg-slate-200 text-slate-500 border-2 border-white">
            4
          </div>
          <div class="text-center">
            <div id="stepLabel4" class="text-[10px] sm:text-xs font-bold text-slate-400 leading-tight">Step 4</div>
            <div class="text-[9px] sm:text-[10px] text-slate-400 leading-tight">รับ +10 แต้ม</div>
          </div>
        </button>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- WIZARD STEPS CONTAINER (แสดงทีละการ์ด ไม่ต้องเลื่อนยาว ไม่มี Tab) -->
    <!-- ============================================================== -->
    <div id="viewRegisterForm" class="space-y-4">

      <!-- ==================== STEP 1 CARD: ADD FRIEND & LINE CONNECT ==================== -->
      <div id="wizardStep1" class="card-light rounded-3xl p-6 border-2 border-amber-300 space-y-5 shadow-md">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <span class="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 font-black text-[10px]">STEP 1 OF 4</span>
            <h2 class="text-lg font-black text-slate-900 mt-1">แอดเพื่อน & เชื่อมบัญชี LINE</h2>
          </div>
          <div class="w-11 h-11 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-600 flex items-center justify-center shrink-0">
            <i data-lucide="message-circle" class="w-6 h-6"></i>
          </div>
        </div>

        <div class="space-y-3">
          <!-- Sub-action A: Add Friend LINE OA -->
          <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between gap-3">
            <div class="text-xs text-slate-700 leading-relaxed">
              <strong class="text-slate-900 block">1. แอดเพื่อน LINE OA ศิวาทรัพย์ (@813nyyia)</strong>
              <span>เพื่อรับแจ้งเตือนคิวเปิดบ้านและลีดลูกค้าอัตโนมัติ</span>
            </div>
            <a href="https://line.me/R/ti/p/@813nyyia" target="_blank" class="shrink-0 px-3.5 py-2.5 rounded-xl bg-white hover:bg-emerald-50 text-emerald-700 border border-emerald-400 font-black text-xs shadow-2xs transition">
              ➕ แอดเพื่อน
            </a>
          </div>

          <!-- Sub-action B: Connect LINE Login -->
          <div id="regLineBanner" class="p-4 rounded-2xl bg-emerald-50/70 border-2 border-emerald-300 space-y-3">
            <div id="regLineBannerText" class="text-xs text-emerald-950 leading-relaxed">
              <strong class="block text-sm">2. กดเชื่อมบัญชี LINE ของท่าน (ไม่ต้องตั้งรหัสผ่าน)</strong>
              <span>หากท่านเป็นสมาชิกที่ได้รับอนุมัติแล้ว ระบบจะพาท่านเข้าสู่หน้าต้อนรับทันที</span>
            </div>
            <button id="regLineBannerBtn" type="button" onclick="startLineLogin('register')" class="w-full py-3.5 px-4 rounded-2xl bg-[#06C755] hover:brightness-95 text-white font-black text-sm shadow-md flex items-center justify-center gap-2 transition active:scale-[0.99] cursor-pointer">
              <i data-lucide="log-in" class="w-4 h-4"></i>
              <span>เชื่อมบัญชี LINE & ดำเนินการต่อ</span>
            </button>
          </div>
        </div>

        <!-- Next Button (Enabled once LINE is connected) -->
        <div class="pt-1 flex justify-end">
          <button id="btnStep1Next" type="button" onclick="goToRegStep(2)" class="w-full py-3.5 px-6 rounded-2xl gold-gradient hover:brightness-105 text-slate-950 font-black text-sm shadow-lg flex items-center justify-center gap-2 transition cursor-pointer">
            <span>ถัดไป: กรอกข้อมูลส่วนตัว (Next)</span>
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- ==================== STEP 2 CARD: PERSONAL DETAILS ==================== -->
      <div id="wizardStep2" class="card-light rounded-3xl p-6 border-2 border-amber-300 space-y-4 shadow-md hidden">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <span class="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 font-black text-[10px]">STEP 2 OF 4</span>
            <h2 class="text-lg font-black text-slate-900 mt-1">ข้อมูลส่วนตัว & เบอร์ติดต่อ</h2>
          </div>
          <div class="w-11 h-11 rounded-2xl bg-amber-50 border border-amber-200 text-amber-600 flex items-center justify-center shrink-0">
            <i data-lucide="user" class="w-6 h-6"></i>
          </div>
        </div>

        <!-- Photo Upload & Avatar Picker -->
        <div class="space-y-2 p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
          <label class="text-xs font-bold text-slate-800 flex items-center justify-between">
            <span class="flex items-center gap-1.5">
              <i data-lucide="camera" class="w-3.5 h-3.5 text-amber-600"></i>
              <span>รูปโปรไฟล์นามบัตรดิจิทัล</span>
            </span>
            <span class="text-[10px] text-slate-500">ดึงจาก LINE อัตโนมัติ หรือแตะเปลี่ยน</span>
          </label>

          <div class="flex items-center gap-3.5">
            <label for="regPhotoFile" class="relative cursor-pointer shrink-0 group block" title="แตะเพื่อเลือกรูปจากมือถือ">
              <img id="regPhotoPreview" 
                   src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80" 
                   alt="Profile Preview" 
                   class="w-16 h-16 rounded-2xl object-cover border-2 border-amber-400 shadow-md group-hover:scale-105 transition">
              <span class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center border border-white shadow-sm group-hover:bg-amber-600 transition">
                <i data-lucide="upload" class="w-3 h-3"></i>
              </span>
            </label>
            <input type="file" id="regPhotoFile" accept="image/*" class="hidden" onchange="handleRegPhotoUpload(event)">

            <div class="space-y-1.5 flex-1 min-w-0">
              <button type="button" onclick="document.getElementById('regPhotoFile').click()" class="w-full py-1.5 px-3 rounded-xl bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 text-xs font-bold flex items-center justify-center gap-1.5 shadow-sm transition">
                <i data-lucide="image" class="w-3.5 h-3.5 text-amber-600"></i>
                <span>📁 เปลี่ยนรูปจากมือถือ</span>
              </button>
              <div class="flex items-center gap-1.5 overflow-x-auto pb-0.5">
                <span class="text-[9px] text-slate-500 shrink-0">หรือเลือก:</span>
                <button type="button" onclick="selectPresetAvatar('https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80')" class="w-6 h-6 rounded-full overflow-hidden border border-slate-300 hover:border-amber-500 shrink-0"><img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&auto=format&fit=crop&q=80" class="w-full h-full object-cover"></button>
                <button type="button" onclick="selectPresetAvatar('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80')" class="w-6 h-6 rounded-full overflow-hidden border border-slate-300 hover:border-amber-500 shrink-0"><img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80" class="w-full h-full object-cover"></button>
                <button type="button" onclick="selectPresetAvatar('https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&auto=format&fit=crop&q=80')" class="w-6 h-6 rounded-full overflow-hidden border border-slate-300 hover:border-amber-500 shrink-0"><img src="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=100&auto=format&fit=crop&q=80" class="w-full h-full object-cover"></button>
                <button type="button" onclick="selectPresetAvatar('https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80')" class="w-6 h-6 rounded-full overflow-hidden border border-slate-300 hover:border-amber-500 shrink-0"><img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80" class="w-full h-full object-cover"></button>
              </div>
            </div>
          </div>
        </div>

        <!-- Full Name -->
        <div class="space-y-1">
          <label class="text-xs font-bold text-slate-700 flex items-center gap-1.5">
            <i data-lucide="user" class="w-3.5 h-3.5 text-amber-600"></i>
            <span>ชื่อ - นามสกุลจริง (สำหรับออกนามบัตรดิจิทัล) *</span>
          </label>
          <input type="text" id="regName" placeholder="ระบุชื่อ - นามสกุลจริงของท่าน" class="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-amber-500 transition">
        </div>

        <!-- Nickname & Phone -->
        <div class="grid grid-cols-2 gap-3">
          <div class="space-y-1">
            <label class="text-xs font-bold text-slate-700">ชื่อเล่น *</label>
            <input type="text" id="regNickname" placeholder="ระบุชื่อเล่นของท่าน" class="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-amber-500 transition">
          </div>
          <div class="space-y-1">
            <label class="text-xs font-bold text-slate-700">เบอร์โทรศัพท์มือถือ *</label>
            <input type="tel" id="regPhone" placeholder="08X-XXX-XXXX" class="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-amber-500 transition">
          </div>
        </div>

        <!-- Step 2 Navigation -->
        <div class="pt-2 flex items-center gap-2.5">
          <button type="button" onclick="goToRegStep(1)" class="px-4 py-3 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs transition cursor-pointer">
            ← ย้อนกลับ
          </button>
          <button type="button" onclick="validateAndGoStep3()" class="flex-1 py-3.5 px-6 rounded-2xl gold-gradient hover:brightness-105 text-slate-950 font-black text-sm shadow-lg flex items-center justify-center gap-2 transition cursor-pointer">
            <span>ถัดไป: เลือกโซนพื้นที่ (Next)</span>
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- ==================== STEP 3 CARD: TERRITORY & SUBMIT ==================== -->
      <div id="wizardStep3" class="card-light rounded-3xl p-6 border-2 border-amber-300 space-y-4 shadow-md hidden">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <span class="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 font-black text-[10px]">STEP 3 OF 4</span>
            <h2 class="text-lg font-black text-slate-900 mt-1">เลือกโซนพื้นที่ & ส่งใบสมัคร</h2>
          </div>
          <div class="w-11 h-11 rounded-2xl bg-rose-50 border border-rose-200 text-rose-600 flex items-center justify-center shrink-0">
            <i data-lucide="map-pin" class="w-6 h-6"></i>
          </div>
        </div>

        <!-- Affiliation Selection -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-slate-700 flex items-center gap-1.5">
            <i data-lucide="briefcase" class="w-3.5 h-3.5 text-amber-600"></i>
            <span>รูปแบบการร่วมงาน *</span>
          </label>
          <div class="grid grid-cols-2 gap-2">
            <label class="flex items-center gap-2.5 p-3 rounded-2xl bg-amber-50/60 border border-amber-300 cursor-pointer hover:bg-amber-50 transition">
              <input type="radio" name="affiliation" value="agent" checked class="text-amber-600 focus:ring-0">
              <div>
                <div class="text-xs font-bold text-slate-900">🤝 Co-Broker</div>
                <div class="text-[9px] text-slate-500">ตัวแทนอิสระ / พันธมิตร</div>
              </div>
            </label>
            <label class="flex items-center gap-2.5 p-3 rounded-2xl bg-slate-50 border border-slate-200 cursor-pointer hover:bg-slate-100 transition">
              <input type="radio" name="affiliation" value="office" class="text-amber-600 focus:ring-0">
              <div>
                <div class="text-xs font-bold text-slate-900">🏢 ทีมงานออฟฟิศ</div>
                <div class="text-[9px] text-slate-500">เจ้าหน้าที่ประจำ</div>
              </div>
            </label>
          </div>
        </div>

        <!-- Territory Zone -->
        <div class="space-y-1">
          <label class="text-xs font-bold text-slate-700 flex items-center gap-1.5">
            <i data-lucide="map-pin" class="w-3.5 h-3.5 text-rose-600"></i>
            <span>โซนพื้นที่ที่ท่านเชี่ยวชาญ / ปฏิบัติงาน *</span>
          </label>
          <select id="regZone" class="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:border-amber-500 transition">
            <option value="โซนท่าข้าม-พระราม 2">โซนท่าข้าม - พระราม 2 (Hub ใหญ่ศิวาทรัพย์)</option>
            <option value="โซนบางนา-ศรีนครินทร์">โซนบางนา - ศรีนครินทร์ - สุขุมวิท</option>
            <option value="โซนราชพฤกษ์-นนทบุรี">โซนราชพฤกษ์ - ปิ่นเกล้า - นนทบุรี</option>
            <option value="โซนปทุมวัน-สยาม">โซนในเมือง ปทุมวัน - สีลม - สาทร</option>
            <option value="สำนักงานใหญ่">สำนักงานใหญ่ / ทุกโซนพื้นที่</option>
          </select>
        </div>

        <!-- Line ID -->
        <div class="space-y-1">
          <label class="text-xs font-bold text-slate-700 flex items-center gap-1.5">
            <i data-lucide="message-circle" class="w-3.5 h-3.5 text-emerald-600"></i>
            <span>LINE ID สำหรับติดต่อประสานงาน (ถ้ามี)</span>
          </label>
          <input type="text" id="regLineId" placeholder="เช่น line_id หรือ เบอร์โทร" class="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-amber-500 transition">
        </div>

        <!-- Step 3 Navigation / Submit -->
        <div class="pt-2 flex items-center gap-2.5">
          <button type="button" onclick="goToRegStep(2)" class="px-4 py-3 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs transition cursor-pointer">
            ← ย้อนกลับ
          </button>
          <button type="button" onclick="submitToLobby()" class="flex-1 gold-gradient hover:brightness-105 text-slate-950 font-black py-3.5 px-6 rounded-2xl shadow-lg shadow-amber-500/20 text-sm flex items-center justify-center gap-2 transition active:scale-[0.99] cursor-pointer">
            <i data-lucide="send" class="w-4 h-4"></i>
            <span>ส่งข้อมูล & เข้าสู่ Step 4 (รับ +10 แต้ม)</span>
          </button>
        </div>
      </div>

    </div>

    <!-- Hidden legacy container for compatibility -->
    <div id="viewLoginForm" class="hidden"></div>

"""

idx_s = html.index(start_marker)
idx_e = html.index(end_marker)
html = html[:idx_s] + stepper_and_forms + html[idx_e:]

# Now add the JavaScript functions for the 4-Step Wizard (updateStepperUI, goToRegStep, validateAndGoStep3, tryClickStep)
js_target = "    let currentApplicant = null;"
wizard_js = """    let currentApplicant = null;
    let currentRegStep = 1;

    function updateStepperUI(step, isCompletedAll = false) {
      currentRegStep = step;
      const fill = document.getElementById('stepperProgressFill');
      if (fill) {
        const pct = step === 1 ? 0 : step === 2 ? 33 : step === 3 ? 66 : 100;
        fill.style.width = pct + '%';
      }

      for (let i = 1; i <= 4; i++) {
        const circle = document.getElementById('stepCircle' + i);
        const label = document.getElementById('stepLabel' + i);
        if (!circle || !label) continue;

        if (i < step || (i === 4 && isCompletedAll)) {
          // Completed step: Emerald checkmark
          circle.className = "w-10 h-10 rounded-full flex items-center justify-center font-black text-sm transition-all duration-300 bg-emerald-500 text-white ring-4 ring-emerald-400/25 shadow-sm";
          circle.innerHTML = "✓";
          label.className = "text-[10px] sm:text-xs font-black text-emerald-700 leading-tight";
        } else if (i === step) {
          // Current active step: Glowing amber/blue focus
          circle.className = "w-10 h-10 rounded-full flex items-center justify-center font-black text-sm transition-all duration-300 bg-amber-500 text-slate-950 ring-4 ring-amber-400/40 shadow-md scale-110";
          circle.innerHTML = String(i);
          label.className = "text-[10px] sm:text-xs font-black text-amber-700 leading-tight";
        } else {
          // Future step: Muted grey
          circle.className = "w-10 h-10 rounded-full flex items-center justify-center font-black text-sm transition-all duration-300 bg-slate-200 text-slate-500 border-2 border-white";
          circle.innerHTML = String(i);
          label.className = "text-[10px] sm:text-xs font-bold text-slate-400 leading-tight";
        }
      }
    }

    function goToRegStep(step) {
      if (step >= 2 && !getSession()) {
        alert('กรุณากดปุ่มสีเขียว "เชื่อมบัญชี LINE" ใน Step 1 ก่อนไปขั้นตอนถัดไปครับ');
        return;
      }
      document.getElementById('viewRegisterForm').classList.remove('hidden');
      document.getElementById('viewLobbyWaiting').classList.add('hidden');
      document.getElementById('viewLoggedInPortal').classList.add('hidden');

      ['wizardStep1', 'wizardStep2', 'wizardStep3'].forEach((id, idx) => {
        const el = document.getElementById(id);
        if (!el) return;
        if (idx + 1 === step) el.classList.remove('hidden');
        else el.classList.add('hidden');
      });

      updateStepperUI(step, false);
      if (window.lucide) lucide.createIcons();
    }

    function tryClickStep(step) {
      if (loggedInMember) {
        updateStepperUI(4, true);
        return;
      }
      if (step <= 3) {
        if (step === 3) {
          validateAndGoStep3();
        } else {
          goToRegStep(step);
        }
      }
    }

    function validateAndGoStep3() {
      if (!getSession()) {
        alert('กรุณาเชื่อมบัญชี LINE ใน Step 1 ก่อนครับ');
        goToRegStep(1);
        return;
      }
      const name = document.getElementById('regName').value.trim();
      const phone = document.getElementById('regPhone').value.trim();
      if (!name || name.length < 3) {
        alert('⚠️ กรุณาระบุชื่อ-นามสกุลจริงใน Step 2 ก่อนไปขั้นตอนถัดไปครับ');
        document.getElementById('regName').focus();
        return;
      }
      const cleanPhone = phone.replace(/\\D/g, '');
      if (!/^(06|08|09)\\d{8}$/.test(cleanPhone)) {
        alert('⚠️ กรุณาระบุเบอร์โทรศัพท์มือถือ 10 หลักให้ถูกต้องก่อนไปขั้นตอนถัดไปครับ');
        document.getElementById('regPhone').focus();
        return;
      }
      saveDraft();
      goToRegStep(3);
    }"""

assert js_target in html, "js_target not found"
html = html.replace(js_target, wizard_js, 1)

# Update submitToLobby, handleApplicantApproved, applyMe, renderLoggedInPortal, renderLineBanner to drive the 4-Step Stepper
html = html.replace(
    "// 2. Switch UI to Lobby Waiting Room\n      document.getElementById('viewRegisterForm').classList.add('hidden');\n      document.getElementById('viewLobbyWaiting').classList.remove('hidden');",
    "// 2. Switch UI to Step 4: Lobby Waiting Room\n      updateStepperUI(4, false);\n      document.getElementById('viewRegisterForm').classList.add('hidden');\n      document.getElementById('viewLobbyWaiting').classList.remove('hidden');"
)
html = html.replace(
    "// 2. Switch UI to Lobby Waiting Room\r\n      document.getElementById('viewRegisterForm').classList.add('hidden');\r\n      document.getElementById('viewLobbyWaiting').classList.remove('hidden');",
    "// 2. Switch UI to Step 4: Lobby Waiting Room\r\n      updateStepperUI(4, false);\r\n      document.getElementById('viewRegisterForm').classList.add('hidden');\r\n      document.getElementById('viewLobbyWaiting').classList.remove('hidden');"
)

html = html.replace(
    "function handleApplicantApproved(approvedData) {\n      const card = document.getElementById('lobbyStatusCard');",
    "function handleApplicantApproved(approvedData) {\n      updateStepperUI(4, true);\n      const card = document.getElementById('lobbyStatusCard');"
)
html = html.replace(
    "function handleApplicantApproved(approvedData) {\r\n      const card = document.getElementById('lobbyStatusCard');",
    "function handleApplicantApproved(approvedData) {\r\n      updateStepperUI(4, true);\r\n      const card = document.getElementById('lobbyStatusCard');"
)

old_render_line = """    function renderLineBanner(me) {
      const txt = document.getElementById('regLineBannerText');
      const btn = document.getElementById('regLineBannerBtn');
      if (!txt || !btn) return;
      if (me && me.line) {
        txt.innerHTML = '<strong>✅ เชื่อม LINE แล้ว:</strong> ' + (me.line.name || 'บัญชี LINE') + ' &mdash; กรอกข้อมูลด้านล่างแล้วส่งเข้า Lobby ได้เลย';
        btn.classList.add('hidden');
      } else {
        txt.innerHTML = '<strong>ขั้นที่ 1:</strong> เชื่อมบัญชี LINE ของท่านก่อนสมัคร เพื่อยืนยันตัวตน (ไม่ต้องตั้งรหัสผ่าน)';
        btn.classList.remove('hidden');
      }
    }"""

new_render_line = """    function renderLineBanner(me) {
      const txt = document.getElementById('regLineBannerText');
      const btn = document.getElementById('regLineBannerBtn');
      if (!txt || !btn) return;
      if (me && me.line) {
        txt.innerHTML = '<strong class="text-emerald-800 text-sm">✅ เชื่อมบัญชี LINE สำเร็จ: ' + (me.line.name || 'บัญชี LINE') + '</strong><span class="block text-emerald-700 mt-0.5">กดปุ่มถัดไปเพื่อกรอกชื่อและเบอร์โทรใน Step 2 ได้เลยครับ</span>';
        btn.classList.add('hidden');
      } else {
        txt.innerHTML = '<strong class="block text-sm">2. กดเชื่อมบัญชี LINE ของท่าน (ไม่ต้องตั้งรหัสผ่าน)</strong><span>หากท่านเป็นสมาชิกที่ได้รับอนุมัติแล้ว ระบบจะพาท่านเข้าสู่ Step 4 ทันที</span>';
        btn.classList.remove('hidden');
      }
    }"""

html = html.replace(old_render_line, new_render_line)
html = html.replace(old_render_line.replace("\n", "\r\n"), new_render_line.replace("\n", "\r\n"))

# In applyMe:
# - If me.status === 'approved' -> updateStepperUI(4, true) & renderLoggedInPortal
# - If me.status === 'pending' -> updateStepperUI(4, false) & show Lobby Waiting
# - If me && me.line (connected LINE, new applicant) -> automatically advance to Step 2!
old_apply_me = """      if (me.status === 'approved') {
        switchAuthMode('login');
        renderLoggedInPortal(me.member);
      } else if (me.status === 'pending') {
        currentApplicant = me.applicant;
        document.getElementById('viewRegisterForm').classList.add('hidden');
        document.getElementById('viewLoginForm').classList.add('hidden');
        document.getElementById('viewLobbyWaiting').classList.remove('hidden');
        document.getElementById('displayAppCode').innerText = me.applicant.id || 'SW-APP';
        document.getElementById('displayName').innerText = me.applicant.name || '';
        document.getElementById('displayPhone').innerText = me.applicant.phone || '';
        document.getElementById('displayZone').innerText = me.applicant.zone || 'สำนักงานใหญ่';
        showLineIdHint(me.line && me.line.userId);
        startPollingForApproval();
        if (window.lucide) lucide.createIcons();
      } else {
        restoreDraft();
        const nameEl = document.getElementById('regName');
        if (nameEl && !nameEl.value && me.line && me.line.name) {
          nameEl.value = me.line.name;
        }
        if (me.line && me.line.picture) {
          selectedAvatarUrl = me.line.picture;
          const prevImg = document.getElementById('regPhotoPreview');
          if (prevImg) prevImg.src = me.line.picture;
        }
        if (mode === 'login') switchAuthMode('register');
      }"""

new_apply_me = """      if (me.status === 'approved') {
        updateStepperUI(4, true);
        renderLoggedInPortal(me.member);
      } else if (me.status === 'pending') {
        updateStepperUI(4, false);
        currentApplicant = me.applicant;
        document.getElementById('viewRegisterForm').classList.add('hidden');
        document.getElementById('viewLobbyWaiting').classList.remove('hidden');
        document.getElementById('displayAppCode').innerText = me.applicant.id || 'SW-APP';
        document.getElementById('displayName').innerText = me.applicant.name || '';
        document.getElementById('displayPhone').innerText = me.applicant.phone || '';
        document.getElementById('displayZone').innerText = me.applicant.zone || 'สำนักงานใหญ่';
        showLineIdHint(me.line && me.line.userId);
        startPollingForApproval();
        if (window.lucide) lucide.createIcons();
      } else {
        restoreDraft();
        const nameEl = document.getElementById('regName');
        if (nameEl && !nameEl.value && me.line && me.line.name) {
          nameEl.value = me.line.name;
        }
        if (me.line && me.line.picture) {
          selectedAvatarUrl = me.line.picture;
          const prevImg = document.getElementById('regPhotoPreview');
          if (prevImg) prevImg.src = me.line.picture;
        }
        if (me.line) {
          goToRegStep(2);
        } else {
          goToRegStep(1);
        }
      }"""

html = html.replace(old_apply_me, new_apply_me)
html = html.replace(old_apply_me.replace("\n", "\r\n"), new_apply_me.replace("\n", "\r\n"))

# Also update logoutUser to return to Step 1
old_logout = """    function logoutUser() {
      loggedInMember = null;
      try { localStorage.removeItem(SESSION_KEY); } catch(e) {}
      renderLineBanner(null);
      switchAuthMode('login');
    }"""
new_logout = """    function logoutUser() {
      loggedInMember = null;
      try { localStorage.removeItem(SESSION_KEY); } catch(e) {}
      renderLineBanner(null);
      goToRegStep(1);
    }"""
html = html.replace(old_logout, new_logout)
html = html.replace(old_logout.replace("\n", "\r\n"), new_logout.replace("\n", "\r\n"))

with open(repo + r"\agent_registration.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated agent_registration.html to 4-Step Visual Progress Stepper successfully!")
