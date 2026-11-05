import json, re

repo = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

# 1. Update siwasup_agents.js: Sort SIWASUP_AGENTS_SEED cleanly S02..S126 without pre-pinning the 6 names at 0 pts
with open(repo + r"\siwasup_agents.js", "r", encoding="utf-8") as f:
    js = f.read()

m = re.search(r"(const SIWASUP_AGENTS_SEED = )(\[\s*\{.*?\}\s*\]);", js, flags=re.S)
assert m, "Could not find SIWASUP_AGENTS_SEED"
agents = json.loads(m.group(2))

def code_num(a):
    d = re.sub(r"\D", "", a.get("code", ""))
    return int(d) if d else 999

for a in agents:
    a["activityPoints"] = 0
    a["performancePoints"] = 0
    a["totalPoints"] = 0
    a["tierId"] = "trainee"
    a["tierName"] = "Trainee"
    a["tierIcon"] = "🌱"
    a.pop("isAlpha", None)
    a.pop("group", None)

agents.sort(key=code_num)
new_seed = json.dumps(agents, ensure_ascii=False, indent=2)
js = js[:m.start(2)] + new_seed + js[m.end(2):]

sync_pattern = re.compile(r"function syncMember\(memberData, autoAwardCheckin = false\) \{.*?\n  \}", re.S)
new_sync_fn = """function syncMember(memberData, autoAwardCheckin = false) {
    if (!memberData) return null;
    const digits = (v) => String(v || '').replace(/\\D/g, '');
    const mPhone = digits(memberData.phone);
    const mNick = String(memberData.nickname || '').trim().toLowerCase();
    const mName = String(memberData.name || '').trim().toLowerCase();
    const mId = String(memberData.code || memberData.id || '').trim();

    // 1. ค้นหาว่าตรงกับตัวแทนเดิมในระบบ (S02 - S126) หรือไม่ (เทียบจากรหัส, เบอร์โทร, ชื่อเล่น หรือชื่อจริง)
    let found = currentAgents.find(a =>
      (mId && a.code.toLowerCase() === mId.toLowerCase()) ||
      (mPhone && mPhone.length >= 9 && digits(a.phone) === mPhone) ||
      (mNick && a.nickname && a.nickname.trim().toLowerCase() === mNick) ||
      (mName && a.name && a.name.trim().toLowerCase() === mName)
    );

    if (!found) {
      let newCode = 'TON';
      if (!(mId === 'app_office_004' || mName.includes('ต้น') || mNick === 'ต้น' || mName.includes('nassty'))) {
        if (mId && /^S\\d+$/i.test(mId)) {
          newCode = mId.toUpperCase();
        } else {
          const maxNum = currentAgents.reduce((mx, a) => {
            const n = parseInt(String(a.code || '').replace(/\\D/g, ''), 10);
            return (!isNaN(n) && n < 900 && n > mx) ? n : mx;
          }, 126);
          newCode = 'S' + (maxNum + 1);
        }
      }

      found = currentAgents.find(a => a.code.toUpperCase() === newCode.toUpperCase());
      if (!found) {
        const newAgent = {
          code: newCode,
          name: memberData.name || 'สมาชิกศิวาทรัพย์',
          nickname: memberData.nickname || (newCode === 'TON' ? 'ต้น' : memberData.name),
          status: 'active',
          startDate: 'Season 1 (2569)',
          phone: memberData.phone || '',
          lineId: memberData.line_id || '',
          email: '',
          avatar: memberData.avatar || '',
          isAlpha: true,
          checkedInToday: true,
          group: 'Season 1 Active',
          activityPoints: 0,
          performancePoints: 0,
          totalPoints: 0,
          tierId: 'trainee',
          tierName: 'Trainee',
          tierIcon: '🌱'
        };
        saveCustomMember(newAgent);
        currentAgents.unshift(newAgent);
        applyTransactionsToAgents();
        saveAgentsToCache();
        found = currentAgents.find(a => a.code === newCode);
      }
    } else {
      if (memberData.avatar) found.avatar = memberData.avatar;
      if (memberData.phone && !found.phone) found.phone = memberData.phone;
      if (memberData.line_id && !found.lineId) found.lineId = memberData.line_id;
      found.isAlpha = true;
      found.checkedInToday = true;
    }

    if (found) {
      try {
        localStorage.setItem('siwasup_my_agent_ref', found.code);
      } catch (e) {}

      let awardedToday = false;
      if (autoAwardCheckin) {
        const today = new Date().toISOString().split('T')[0];
        const checkinKey = `siwasup_checked_in_${found.code}_${today}`;
        if (!localStorage.getItem(checkinKey)) {
          awardPoints(found.code, 'meeting_checkin', { date: today, source: 'verified_onboarding' });
          try { localStorage.setItem(checkinKey, 'true'); } catch (e) {}
          awardedToday = true;
        }
      }
      saveAgentsToCache();
      return { agent: found, awardedToday: awardedToday };
    }
    return null;
  }"""

assert sync_pattern.search(js), "syncMember not found"
js = sync_pattern.sub(lambda _: new_sync_fn, js)

old_get_active = """  function getActiveAgents() {
    return currentAgents.filter(a => a.status === 'active');
  }"""
new_get_active = """  function getActiveAgents() {
    const active = currentAgents.filter(a => a.status === 'active');
    return [...active].sort((a, b) => {
      const pDiff = (b.totalPoints || 0) - (a.totalPoints || 0);
      if (pDiff !== 0) return pDiff;
      const cDiff = (b.checkedInToday ? 1 : 0) - (a.checkedInToday ? 1 : 0);
      if (cDiff !== 0) return cDiff;
      return (parseInt(String(a.code).replace(/\\D/g, ''), 10) || 999) - (parseInt(String(b.code).replace(/\\D/g, ''), 10) || 999);
    });
  }"""
if old_get_active in js:
    js = js.replace(old_get_active, new_get_active)

with open(repo + r"\siwasup_agents.js", "w", encoding="utf-8") as f:
    f.write(js)

print("1. siwasup_agents.js updated")

# 2. Update agent_registration.html:
# - Step 1 Add Friend LINE OA + Step 2 Connect LINE
# - Copy Invite Message for Gool in qrModal
# - Direct button to welcome_landing.html upon approval
with open(repo + r"\agent_registration.html", "r", encoding="utf-8") as f:
    reg = f.read()

old_line_banner = """      <!-- LINE connect banner -->
      <div id="regLineBanner" class="card-light rounded-2xl p-4 border-2 border-emerald-300 bg-emerald-50/50 flex items-center justify-between gap-3">
        <div id="regLineBannerText" class="text-xs text-emerald-900 leading-relaxed">
          <strong>ขั้นที่ 1:</strong> เชื่อมบัญชี LINE ของท่านก่อนสมัคร เพื่อยืนยันตัวตน (ไม่ต้องตั้งรหัสผ่าน)
        </div>
        <button id="regLineBannerBtn" type="button" onclick="startLineLogin('register')" class="shrink-0 px-3.5 py-2 rounded-xl bg-[#06C755] hover:brightness-95 text-white font-black text-xs shadow-sm">เชื่อม LINE</button>
      </div>"""

new_line_banner = """      <!-- STEP 1 & 2: ADD FRIEND LINE OA + CONNECT LINE (ไม่ต้องสแกน QR ในจอตัวเอง) -->
      <div class="card-light rounded-2xl p-4 border-2 border-emerald-400 bg-emerald-50/60 space-y-3">
        <div class="flex items-center justify-between gap-3 pb-2.5 border-b border-emerald-200/80">
          <div class="text-xs text-emerald-950 leading-relaxed">
            <span class="inline-block px-2 py-0.5 rounded bg-emerald-600 text-white font-black text-[10px] mr-1">ก้าวที่ 1</span>
            <strong>แอดเพื่อน LINE OA ศิวาทรัพย์</strong> เพื่อรับแจ้งเตือนคิวเปิดบ้านและลีดลูกค้า
          </div>
          <a href="https://line.me/R/ti/p/@813nyyia" target="_blank" class="shrink-0 px-3.5 py-2 rounded-xl bg-white hover:bg-emerald-100 text-emerald-800 border border-emerald-400 font-black text-xs shadow-2xs flex items-center gap-1">
            <span>➕ แอดเพื่อน @813nyyia</span>
          </a>
        </div>
        <div id="regLineBanner" class="flex items-center justify-between gap-3">
          <div id="regLineBannerText" class="text-xs text-emerald-900 leading-relaxed">
            <span class="inline-block px-2 py-0.5 rounded bg-amber-500 text-slate-950 font-black text-[10px] mr-1">ก้าวที่ 2</span>
            <strong>กดเชื่อมบัญชี LINE ของท่าน</strong> เพื่อยืนยันตัวตนและรับ <strong>+10 แต้มแรกเข้า</strong>
          </div>
          <button id="regLineBannerBtn" type="button" onclick="startLineLogin('register')" class="shrink-0 px-3.5 py-2 rounded-xl bg-[#06C755] hover:brightness-95 text-white font-black text-xs shadow-sm">เชื่อม LINE</button>
        </div>
      </div>"""

if old_line_banner in reg:
    reg = reg.replace(old_line_banner, new_line_banner)

# Update unlockedActions in agent_registration.html so after approval, button #1 takes them to welcome_landing.html!
old_unlocked = """          <a id="btnGoCard" href="#" target="_blank" class="w-full gold-gradient hover:brightness-105 text-slate-950 font-black py-3 rounded-2xl shadow-lg text-sm flex items-center justify-center gap-2 transition">
            <i data-lucide="credit-card" class="w-4 h-4"></i>
            <span>เปิดดูนามบัตรดิจิทัลทางการของท่าน</span>
          </a>

          <a href="https://assets.siwasup.com/catalog.html" target="_blank" class="w-full bg-white hover:bg-slate-50 text-slate-800 font-bold py-2.5 rounded-2xl border border-slate-300 text-xs flex items-center justify-center gap-2 shadow-sm transition">
            <i data-lucide="home" class="w-4 h-4 text-emerald-600"></i>
            <span>เข้าสู่คลังทรัพย์พร้อมขาย & เครื่องมือแชร์ลิงก์ลูกค้า</span>
          </a>"""

new_unlocked = """          <a id="btnGoWelcome" href="https://assets.siwasup.com/welcome_landing.html?checkin=1" class="w-full gold-gradient hover:brightness-105 text-slate-950 font-black py-3.5 rounded-2xl shadow-lg text-sm flex items-center justify-center gap-2 transition">
            <i data-lucide="sparkles" class="w-4 h-4"></i>
            <span>เข้าสู่หน้าต้อนรับศิวาทรัพย์ (รับ +10 แต้มแรกเข้าเรียบร้อย!)</span>
          </a>

          <a id="btnGoCard" href="#" target="_blank" class="w-full bg-emerald-50 hover:bg-emerald-100 text-emerald-900 font-bold py-2.5 rounded-2xl border border-emerald-300 text-xs flex items-center justify-center gap-2 shadow-2xs transition">
            <i data-lucide="credit-card" class="w-4 h-4 text-emerald-600"></i>
            <span>เปิดดูนามบัตรดิจิทัลทางการของท่าน</span>
          </a>

          <a id="btnGoCatalog" href="https://assets.siwasup.com/catalog.html?checkin=1" class="w-full bg-white hover:bg-slate-50 text-slate-800 font-bold py-2.5 rounded-2xl border border-slate-300 text-xs flex items-center justify-center gap-2 shadow-sm transition">
            <i data-lucide="home" class="w-4 h-4 text-amber-600"></i>
            <span>ข้ามไปหน้าคลังทรัพย์พร้อมขายทันที</span>
          </a>"""

if old_unlocked in reg:
    reg = reg.replace(old_unlocked, new_unlocked)

# Update handleApplicantApproved to set btnGoWelcome and btnGoCatalog with the agent's real synced code
old_sync_call = """      if (window.SiwasupAgents && typeof window.SiwasupAgents.syncMember === 'function') {
        window.SiwasupAgents.syncMember(approvedData, true);
      }"""

new_sync_call = """      if (window.SiwasupAgents && typeof window.SiwasupAgents.syncMember === 'function') {
        const sr = window.SiwasupAgents.syncMember(approvedData, true);
        if (sr && sr.agent) {
          const q = `?my_agent=${encodeURIComponent(sr.agent.code)}&my_name=${encodeURIComponent(approvedData.name || '')}&my_nick=${encodeURIComponent(approvedData.nickname || '')}&checkin=1`;
          const wBtn = document.getElementById('btnGoWelcome');
          const cBtn = document.getElementById('btnGoCatalog');
          if (wBtn) wBtn.href = `https://assets.siwasup.com/welcome_landing.html${q}#announcements`;
          if (cBtn) cBtn.href = `https://assets.siwasup.com/catalog.html${q}`;
        }
      }"""

if old_sync_call in reg:
    reg = reg.replace(old_sync_call, new_sync_call)

# Also add Welcome Landing button in renderLoggedInPortal
old_portal_action = """      actions.push(`
        <a href="https://assets.siwasup.com/catalog.html${catParams}" target="_blank" class="p-3 rounded-2xl bg-emerald-50 hover:bg-emerald-100 border border-emerald-300 text-emerald-950 font-bold flex items-center justify-between transition shadow-2xs">
          <div class="flex items-center gap-2">
            <i data-lucide="award" class="w-4 h-4 text-emerald-600"></i>
            <span>คลังทรัพย์ & กระเป๋าคะแนน (${syncedCode})</span>
          </div>
          <span class="text-[10px] bg-emerald-500 text-white px-1.5 py-0.5 rounded font-bold">+10 แต้ม</span>
        </a>
      `);"""

new_portal_action = """      actions.unshift(`
        <a href="https://assets.siwasup.com/welcome_landing.html${catParams}#announcements" class="sm:col-span-2 p-3.5 rounded-2xl gold-gradient hover:brightness-105 text-slate-950 font-black flex items-center justify-between transition shadow-md">
          <div class="flex items-center gap-2">
            <i data-lucide="sparkles" class="w-4 h-4 text-slate-950"></i>
            <span>เข้าสู่หน้าต้อนรับ Season 1 & กระดานคะแนน (${syncedCode})</span>
          </div>
          <span class="text-[10px] bg-slate-950 text-amber-300 px-2 py-0.5 rounded-full font-bold">หน้าต้อนรับ →</span>
        </a>
      `);
      actions.push(`
        <a href="https://assets.siwasup.com/catalog.html${catParams}" class="p-3 rounded-2xl bg-emerald-50 hover:bg-emerald-100 border border-emerald-300 text-emerald-950 font-bold flex items-center justify-between transition shadow-2xs">
          <div class="flex items-center gap-2">
            <i data-lucide="award" class="w-4 h-4 text-emerald-600"></i>
            <span>คลังทรัพย์ & กระเป๋าคะแนน (${syncedCode})</span>
          </div>
          <span class="text-[10px] bg-emerald-500 text-white px-1.5 py-0.5 rounded font-bold">+10 แต้ม</span>
        </a>
      `);"""

if old_portal_action in reg:
    reg = reg.replace(old_portal_action, new_portal_action)

with open(repo + r"\agent_registration.html", "w", encoding="utf-8") as f:
    f.write(reg)

print("2. agent_registration.html updated")

# 3. Update welcome_landing.html:
# - Remove QR Code on screen (so phone users in conference don't wonder how to scan their own screen)
# - Remove hardcoded 6 Alpha cards
# - Show Personal Welcome Pass + Self Check-in Button + Dynamic Active Check-in Board + Copy Invite Link for Gool
with open(repo + r"\welcome_landing.html", "r", encoding="utf-8") as f:
    wl = f.read()

ann_pattern = re.compile(r'<section id="announcements".*?</section>', re.S)

new_ann_section = """<!-- =====================================================================
       SECTION 2: SEASON 1 WELCOME PASS & REAL-TIME CHECK-IN BOARD (CONFERENCE READY)
       ===================================================================== -->
  <section id="announcements" class="py-16 sm:py-24 bg-[#0d111a] border-y border-white/5 relative">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">

      <!-- Section Header -->
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <div class="inline-flex items-center gap-1.5 text-emerald-400 text-xs font-bold uppercase tracking-wider mb-2">
            <i data-lucide="sparkles" class="w-4 h-4"></i>
            <span>OFFICIAL LAUNCH • SEASON 1 (เริ่มต้นกระดานใหม่ 100%)</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-white">
            ยินดีต้อนรับสู่ <span class="gold-gradient-text">Siwasup Co-Broker OS</span>
          </h2>
          <p class="text-xs sm:text-sm text-slate-400 mt-1">
            ระบบบริหารงานขายร่วมและสะสมคะแนนตามผลงานจริง (กดทำรายการบนหน้าจอมือถือของท่านได้ทันที ไม่ต้องสแกน QR ซ้ำ)
          </p>
        </div>

        <div class="flex items-center gap-2 self-start md:self-auto flex-wrap">
          <button type="button" onclick="copyLineConferenceInvite()" class="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/40 text-xs text-emerald-300 font-bold transition cursor-pointer">
            <i data-lucide="copy" class="w-3.5 h-3.5"></i>
            <span id="copyInviteBtnText">คัดลอกลิงก์ส่งเข้ากลุ่ม LINE (สำหรับคุณกูล)</span>
          </button>
        </div>
      </div>

      <!-- 2-Column Interactive Layout -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">

        <!-- Left (5 cols): Personal Welcome Pass / Self-Screen Onboarding -->
        <div class="lg:col-span-5 rounded-3xl p-6 sm:p-7 card-glass border-2 border-amber-500/40 flex flex-col justify-between relative overflow-hidden bg-gradient-to-b from-amber-500/10 via-[#111622] to-[#111622]">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-[11px] font-bold flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span>ทำรายการบนหน้าจอนี้ได้เลย</span>
              </span>
              <span class="text-xs font-mono text-amber-300 font-bold">+10 แต้มแรกเข้า</span>
            </div>

            <!-- Dynamic Box: Shown when user has registered/checked in -->
            <div id="myWelcomePassBox" class="hidden p-5 rounded-2xl bg-emerald-950/50 border-2 border-emerald-400/60 space-y-3 text-left shadow-lg">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-0.5 rounded-md bg-amber-400 text-slate-950 font-mono font-black text-xs" id="passAgentCode">S--</span>
                <span class="text-xs font-bold text-emerald-300">✅ เช็กอินสำเร็จ (+10 แต้ม)</span>
              </div>
              <div>
                <div class="text-lg font-black text-white" id="passAgentName">ยินดีต้อนรับสมาชิก</div>
                <div class="text-xs text-slate-300 mt-0.5">คะแนนสะสมปัจจุบันของคุณ: <strong class="text-amber-300 font-mono text-sm" id="passAgentPoints">10 แต้ม</strong> (🐻 หมีตื่นตัว)</div>
              </div>
              <a id="passGoCatalogBtn" href="catalog.html" class="w-full py-3 px-4 rounded-xl gold-gradient text-slate-950 font-black text-xs sm:text-sm flex items-center justify-center gap-2 shadow-lg hover:brightness-105 transition">
                <i data-lucide="building-2" class="w-4 h-4"></i>
                <span>เข้าสู่คลังทรัพย์พร้อมขาย & แชร์ลิงก์ลูกค้า →</span>
              </a>
            </div>

            <!-- Step-by-Step Onboarding Box (For Conference / Mobile Users) -->
            <div id="stepOnboardingBox" class="space-y-3">
              <h3 class="text-lg font-black text-white leading-snug">
                ลำดับการเริ่มต้นใช้งาน (กดจากมือถือได้ทันที)
              </h3>
              <p class="text-xs text-slate-300 leading-relaxed">
                สำหรับตัวแทนที่เข้าประชุมออนไลน์ (Conference) สามารถกดปุ่มตามลำดับด้านล่างบนหน้าจอมือถือของท่านได้เลยครับ:
              </p>

              <!-- Step 1: Add Friend LINE OA -->
              <a href="https://line.me/R/ti/p/@813nyyia" target="_blank" class="w-full p-3.5 rounded-2xl bg-[#06C755]/15 hover:bg-[#06C755]/25 border border-[#06C755]/50 flex items-center justify-between transition group">
                <div class="flex items-center gap-3">
                  <span class="w-7 h-7 rounded-xl bg-[#06C755] text-white font-black text-xs flex items-center justify-center shrink-0">1</span>
                  <div class="text-left">
                    <div class="text-xs sm:text-sm font-black text-white group-hover:text-emerald-300 transition">แอดเพื่อน LINE OA ศิวาทรัพย์</div>
                    <div class="text-[11px] text-slate-400">รับแจ้งเตือนคิวเปิดบ้านและลีดลูกค้า (@813nyyia)</div>
                  </div>
                </div>
                <span class="px-2.5 py-1 rounded-lg bg-[#06C755] text-white text-[11px] font-bold shrink-0">แอดเพื่อน →</span>
              </a>

              <!-- Step 2: Register & Connect LINE -->
              <a href="agent_registration.html" class="w-full p-3.5 rounded-2xl bg-amber-500/15 hover:bg-amber-500/25 border border-amber-400/60 flex items-center justify-between transition group">
                <div class="flex items-center gap-3">
                  <span class="w-7 h-7 rounded-xl bg-amber-400 text-slate-950 font-black text-xs flex items-center justify-center shrink-0">2</span>
                  <div class="text-left">
                    <div class="text-xs sm:text-sm font-black text-amber-300 group-hover:text-white transition">ลงทะเบียน & เชื่อม LINE ยืนยันตัวตน</div>
                    <div class="text-[11px] text-slate-300">เมื่ออนุมัติแล้ว ระบบพากลับมาหน้านี้พร้อมรับ +10 แต้มทันที</div>
                  </div>
                </div>
                <span class="px-2.5 py-1 rounded-lg gold-gradient text-slate-950 text-[11px] font-black shrink-0">สมัครเลย →</span>
              </a>
            </div>

            <!-- Self Check-in Selector (สำหรับสมาชิกที่มีชื่อในระบบแล้ว กดรับแต้มบนจอตัวเองได้เลย) -->
            <div class="pt-3 border-t border-white/10 space-y-2">
              <label class="text-[11px] text-slate-400 block font-semibold">
                หรือหากท่านมีรหัสตัวแทนแล้ว กดเช็กอินรับ +10 แต้มบนหน้าจอนี้ได้ทันที:
              </label>
              <div class="flex gap-2">
                <select id="landingSelfCheckinSelect" class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-400">
                  <option value="">-- เลือกชื่อของท่านเพื่อเช็กอิน (+10 แต้ม) --</option>
                </select>
                <button type="button" onclick="triggerSelfScreenCheckin()" class="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs shrink-0 transition cursor-pointer">
                  กดเช็กอิน
                </button>
              </div>
            </div>
          </div>

          <div class="pt-4 mt-4 border-t border-white/10 flex items-center justify-between text-[11px] text-slate-400">
            <span>สถานะระบบ: <strong class="text-emerald-400">พร้อมใช้งานจริง 100%</strong></span>
            <a href="catalog.html" class="text-amber-300 hover:underline font-bold">เข้าหน้าคลังทรัพย์ →</a>
          </div>
        </div>

        <!-- Right (7 cols): Live Checked-In Agents Board (แสดงเฉพาะคนที่ลงทะเบียน/เช็กอินจริง ไม่ล็อก 6 ชื่อล่วงหน้า!) -->
        <div class="lg:col-span-7 rounded-3xl p-6 sm:p-8 card-glass border border-white/10 flex flex-col justify-between space-y-6">
          <div class="space-y-2">
            <div class="flex items-center justify-between flex-wrap gap-2">
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
                <i data-lucide="users" class="w-4 h-4"></i>
                <span>กระดานต้อนรับผู้เข้าร่วม Season 1 วันนี้ (Real-Time)</span>
              </span>
              <span id="checkedInCountBadge" class="text-[11px] px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 font-mono">
                เช็กอินแล้ว 0 ท่าน
              </span>
            </div>
            <h3 class="text-xl sm:text-2xl font-black text-white">
              ทำเนียบตัวแทนที่ลงทะเบียนและเช็กอินเข้าสู่ระบบจริง
            </h3>
            <p class="text-xs text-slate-400 leading-relaxed">
              เริ่มต้น Season 1 ที่ <strong>0 แต้ม</strong> เท่ากันทุกคน — รายชื่อด้านล่างจะปรากฏขึ้นตามจริงเฉพาะผู้ที่ลงทะเบียนและกดเช็กอินเข้างานวันนี้แล้วเท่านั้น (ไม่ว่าจะมีผู้เข้าร่วมกี่ท่าน ระบบจะแสดงผลตามจริงทั้งหมด)
            </p>
          </div>

          <!-- Dynamic Grid of Checked-In Agents -->
          <div id="liveCheckedInGrid" class="grid grid-cols-1 sm:grid-cols-2 gap-3 my-auto">
            <!-- Populated dynamically by JS -->
          </div>

          <!-- Bottom Summary & Action -->
          <div class="p-4 rounded-2xl bg-slate-900/90 border border-white/10 flex flex-col sm:flex-row items-center justify-between gap-3">
            <div class="text-xs text-slate-300">
              💡 <strong>กติกา Season 1:</strong> เช็กอินเข้างานรับทันที <span class="text-emerald-400 font-bold">+10 แต้ม</span> • แชร์ลิงก์ทรัพย์ <span class="text-amber-300 font-bold">+5 แต้ม</span> • ติดป้ายไวนิล GPS <span class="text-amber-300 font-bold">+15 แต้ม</span>
            </div>
            <a href="catalog.html" class="w-full sm:w-auto text-center px-5 py-2.5 rounded-xl gold-gradient text-slate-950 font-black text-xs shrink-0 shadow-md hover:brightness-105 transition">
              เปิดคลังทรัพย์พร้อมขาย →
            </a>
          </div>
        </div>

      </div>

    </div>
  </section>"""

assert ann_pattern.search(wl), "Could not find Section 2 in welcome_landing.html"
wl = ann_pattern.sub(lambda _: new_ann_section, wl)

# Replace the script at the bottom of welcome_landing.html
script_pattern = re.compile(r'<script src="siwasup_agents\.js[^"]*"></script>\s*<script>.*?</script>', re.S)
new_wl_script = """<script src="siwasup_agents.js?v=20261104-conf"></script>
  <script>
    lucide.createIcons();

    function copyLineConferenceInvite() {
      const msg = [
        "🌟 ยินดีต้อนรับพี่น้องตัวแทนสู่การเปิดตัว Siwasup Co-Broker OS (Season 1) ครับ!",
        "",
        "กรุณากดทำรายการตามลำดับ 1-2 บนจอมือถือของท่านเพื่อรับรหัสและคะแนนแรกเข้า (+10 แต้ม) ได้เลยครับ:",
        "",
        "1️⃣ กดแอดเพื่อน LINE OA ศิวาทรัพย์:",
        "👉 https://line.me/R/ti/p/@813nyyia",
        "",
        "2️⃣ กดลงทะเบียน & เชื่อม LINE เข้าสู่ห้องรับรอง (Lobby):",
        "👉 https://assets.siwasup.com/agent_registration.html",
        "",
        "(เมื่อฝ่ายบริหารกดอนุมัติแล้ว หน้าจอมือถือของท่านจะพาเข้าสู่หน้าต้อนรับและคลังทรัพย์พร้อมรับ +10 แต้มทันทีครับ 🎉)"
      ].join("\\n");
      navigator.clipboard.writeText(msg).then(() => {
        const el = document.getElementById('copyInviteBtnText');
        if (el) {
          el.textContent = "✅ คัดลอกข้อความเชิญเรียบร้อย! นำไปวางในกลุ่ม LINE ได้เลย";
          setTimeout(() => { el.textContent = "คัดลอกลิงก์ส่งเข้ากลุ่ม LINE (สำหรับคุณกูล)"; }, 4000);
        }
      });
    }

    function populateSelfCheckinDropdown() {
      const sel = document.getElementById('landingSelfCheckinSelect');
      if (!sel || !window.SiwasupAgents) return;
      const all = window.SiwasupAgents.getActive();
      const currentVal = sel.value || localStorage.getItem('siwasup_my_agent_ref') || '';
      sel.innerHTML = '<option value="">-- เลือกชื่อของท่านเพื่อเช็กอิน (+10 แต้ม) --</option>' +
        all.map(a => `<option value="${a.code}" ${a.code === currentVal ? 'selected' : ''}>${a.code} - ${a.nickname || a.name} (${a.totalPoints || 0} แต้ม)</option>`).join('');
    }

    function triggerSelfScreenCheckin() {
      const sel = document.getElementById('landingSelfCheckinSelect');
      if (!sel || !sel.value) {
        alert('กรุณาเลือกชื่อรหัสตัวแทนของท่านก่อนกดเช็กอินครับ (หรือกดปุ่มที่ 2 เพื่อลงทะเบียนใหม่)');
        return;
      }
      const code = sel.value;
      const found = window.SiwasupAgents.find(code);
      if (found && window.SiwasupAgents.syncMember) {
        window.SiwasupAgents.syncMember({
          code: found.code,
          name: found.name,
          nickname: found.nickname,
          phone: found.phone
        }, true);
        showMyWelcomePass(found.code);
        renderLiveCheckedInBoard();
        populateSelfCheckinDropdown();
      }
    }

    function showMyWelcomePass(code) {
      if (!window.SiwasupAgents || !code) return;
      const ag = window.SiwasupAgents.find(code);
      if (!ag) return;
      const passBox = document.getElementById('myWelcomePassBox');
      const codeEl = document.getElementById('passAgentCode');
      const nameEl = document.getElementById('passAgentName');
      const ptsEl = document.getElementById('passAgentPoints');
      const catBtn = document.getElementById('passGoCatalogBtn');
      if (passBox) passBox.classList.remove('hidden');
      if (codeEl) codeEl.textContent = ag.code;
      if (nameEl) nameEl.textContent = `🎉 ยินดีต้อนรับ คุณ${ag.nickname || ag.name} (${ag.code})`;
      if (ptsEl) ptsEl.textContent = `${ag.totalPoints || 0} แต้ม`;
      if (catBtn) catBtn.href = `catalog.html?my_agent=${encodeURIComponent(ag.code)}&checkin=1`;
    }

    function renderLiveCheckedInBoard() {
      const grid = document.getElementById('liveCheckedInGrid');
      const countBadge = document.getElementById('checkedInCountBadge');
      if (!grid || !window.SiwasupAgents) return;

      const all = window.SiwasupAgents.getActive();
      const checkedInList = all.filter(a => (a.totalPoints || 0) > 0 || a.checkedInToday);

      if (countBadge) {
        countBadge.textContent = `เช็กอินเข้างานแล้ว ${checkedInList.length} ท่าน`;
      }

      if (checkedInList.length === 0) {
        grid.innerHTML = `
          <div class="sm:col-span-2 p-8 rounded-2xl bg-slate-900/60 border border-dashed border-slate-700 text-center space-y-2">
            <div class="text-2xl">🌱</div>
            <div class="text-sm font-bold text-white">กระดาน Season 1 พร้อมต้อนรับสมาชิกท่านแรก!</div>
            <p class="text-xs text-slate-400 max-w-md mx-auto">
              ขณะนี้คะแนนทุกคนรีเซ็ตเป็น 0 แต้มเท่ากันทั้งหมด เมื่อตัวแทนลงทะเบียนผ่านลิงก์ในกลุ่ม LINE หรือกดเช็กอิน รายชื่อและคะแนนจริง (+10 แต้ม) จะปรากฏขึ้นที่นี่ทันทีครับ
            </p>
          </div>
        `;
        return;
      }

      grid.innerHTML = checkedInList.map(a => {
        const pts = a.totalPoints || 0;
        return `
          <a href="catalog.html?my_agent=${encodeURIComponent(a.code)}&checkin=1" class="p-4 rounded-2xl border bg-emerald-950/30 border-emerald-500/50 hover:border-amber-400 transition flex items-center justify-between group">
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-11 h-11 rounded-xl bg-emerald-500 text-slate-950 font-mono font-black text-xs flex items-center justify-center shrink-0">
                ${a.code}
              </div>
              <div class="min-w-0">
                <div class="text-sm font-black text-white group-hover:text-amber-300 transition truncate">
                  คุณ${a.nickname || a.name} <span class="text-[11px] font-normal text-slate-400">(${a.name})</span>
                </div>
                <div class="text-[11px] text-emerald-400 font-bold">
                  ✅ ลงทะเบียน & เช็กอินสำเร็จ (+10 แต้ม)
                </div>
              </div>
            </div>
            <div class="text-right shrink-0 ml-2">
              <span class="text-sm font-mono font-black text-emerald-400">${pts} แต้ม</span>
              <span class="block text-[10px] text-slate-400">เข้าคลังทรัพย์ →</span>
            </div>
          </a>
        `;
      }).join('');
    }

    document.addEventListener('DOMContentLoaded', async () => {
      const params = new URLSearchParams(window.location.search);
      const myAgent = params.get('my_agent');
      const myName = params.get('my_name');
      const myNick = params.get('my_nick');
      const isCheckin = params.get('checkin') === '1';

      if (myAgent && window.SiwasupAgents && window.SiwasupAgents.syncMember) {
        const sr = window.SiwasupAgents.syncMember({
          code: myAgent,
          name: myName || myAgent,
          nickname: myNick || myName || myAgent
        }, isCheckin);
        if (sr && sr.agent) {
          showMyWelcomePass(sr.agent.code);
        }
      } else {
        // Check if logged in via LINE session
        const sess = localStorage.getItem('siwasup_session');
        if (sess && window.SiwasupAgents && window.SiwasupAgents.syncMember) {
          try {
            const r = await fetch('https://siwasup-cobroker-os.onrender.com/api/auth/me', {
              headers: { 'Authorization': 'Bearer ' + sess },
              cache: 'no-store'
            });
            if (r.ok) {
              const me = await r.json();
              if (me && me.status === 'approved' && me.member) {
                const sr = window.SiwasupAgents.syncMember(me.member, true);
                if (sr && sr.agent) showMyWelcomePass(sr.agent.code);
              }
            }
          } catch (e) {}
        } else {
          const savedRef = localStorage.getItem('siwasup_my_agent_ref');
          if (savedRef && window.SiwasupAgents) {
            const ag = window.SiwasupAgents.find(savedRef);
            if (ag && (ag.totalPoints > 0 || ag.checkedInToday)) {
              showMyWelcomePass(ag.code);
            }
          }
        }
      }

      populateSelfCheckinDropdown();
      renderLiveCheckedInBoard();
    });
  </script>"""

assert script_pattern.search(wl), "Could not find script block in welcome_landing.html"
wl = script_pattern.sub(lambda _: new_wl_script, wl)

with open(repo + r"\welcome_landing.html", "w", encoding="utf-8") as f:
    f.write(wl)

print("3. welcome_landing.html updated")

# 4. Update index.html & catalog.html:
# - Group dropdown by Checked-in Active agents (totalPoints > 0 or checkedInToday) vs All S02..S126
# - Support ?my_agent=...&my_name=...&my_nick=...&checkin=1 for newly registered agents
with open(repo + r"\index.html", "r", encoding="utf-8") as f:
    idx = f.read()

old_sw = """        const all = window.SiwasupAgents.getActive();
        const alphas = all.filter(a => a.isAlpha);
        const others = all.filter(a => !a.isAlpha);
        const renderOpt = (a) => `
          <option value="${a.code}" ${a.code === agent.code ? 'selected' : ''}>
            ${a.code} - ${a.nickname || a.name} (${a.tierIcon} ${a.totalPoints} แต้ม)
          </option>
        `;
        switcher.innerHTML = `
          <optgroup label="🌟 ทีมบุกเบิก (Alpha Squad 6 ท่าน)">
            ${alphas.map(renderOpt).join('')}
          </optgroup>
          <optgroup label="📋 ทำเนียบตัวแทนศิวาทรัพย์ทั้งหมด (Season 1)">
            ${others.map(renderOpt).join('')}
          </optgroup>
        `;"""

new_sw = """        const all = window.SiwasupAgents.getActive();
        const checkedIn = all.filter(a => (a.totalPoints || 0) > 0 || a.checkedInToday);
        const others = all.filter(a => !((a.totalPoints || 0) > 0 || a.checkedInToday));
        const renderOpt = (a) => `
          <option value="${a.code}" ${a.code === agent.code ? 'selected' : ''}>
            ${a.code} - ${a.nickname || a.name} (${a.tierIcon} ${a.totalPoints} แต้ม)
          </option>
        `;
        switcher.innerHTML = (checkedIn.length > 0 ? `
          <optgroup label="🌟 สมาชิกที่ลงทะเบียน & เช็กอินเข้างานแล้ว (${checkedIn.length} ท่าน)">
            ${checkedIn.map(renderOpt).join('')}
          </optgroup>` : '') + `
          <optgroup label="📋 รายชื่อตัวแทนในระบบ (เรียงตามรหัส S02 - S126)">
            ${others.map(renderOpt).join('')}
          </optgroup>
        `;"""

if old_sw in idx:
    idx = idx.replace(old_sw, new_sw)

old_my_agent_check = """      const myAgentParam = params.get('my_agent');
      const isAutoCheckin = params.get('checkin') === '1';
      if (myAgentParam && window.SiwasupAgents && typeof window.SiwasupAgents.syncMember === 'function') {
        const synced = window.SiwasupAgents.syncMember({
          id: myAgentParam,
          code: myAgentParam,
          name: myAgentParam === 'TON' ? 'คุณต้น (NASSTY)' : myAgentParam,
          nickname: myAgentParam === 'TON' ? 'ต้น' : myAgentParam
        }, isAutoCheckin);"""

new_my_agent_check = """      const myAgentParam = params.get('my_agent');
      const myNameParam = params.get('my_name');
      const myNickParam = params.get('my_nick');
      const isAutoCheckin = params.get('checkin') === '1';
      if (myAgentParam && window.SiwasupAgents && typeof window.SiwasupAgents.syncMember === 'function') {
        const synced = window.SiwasupAgents.syncMember({
          id: myAgentParam,
          code: myAgentParam,
          name: myNameParam || (myAgentParam === 'TON' ? 'คุณต้น (NASSTY)' : myAgentParam),
          nickname: myNickParam || (myAgentParam === 'TON' ? 'ต้น' : (myNameParam || myAgentParam))
        }, isAutoCheckin);"""

if old_my_agent_check in idx:
    idx = idx.replace(old_my_agent_check, new_my_agent_check)

idx = re.sub(r'siwasup_agents\.js(\?v=[^"]*)?', 'siwasup_agents.js?v=20261104-conf', idx)

with open(repo + r"\index.html", "w", encoding="utf-8") as f:
    f.write(idx)
with open(repo + r"\catalog.html", "w", encoding="utf-8") as f:
    f.write(idx)

with open(repo + r"\sw.js", "r", encoding="utf-8") as f:
    sw = f.read()
sw = re.sub(r"const CACHE_NAME = '[^']+';", "const CACHE_NAME = 'siwasup-os-v20261104-conf';", sw)
with open(repo + r"\sw.js", "w", encoding="utf-8") as f:
    f.write(sw)

print("4. index.html, catalog.html, and sw.js updated")
