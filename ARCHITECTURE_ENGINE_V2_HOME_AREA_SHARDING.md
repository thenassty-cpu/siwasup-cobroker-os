# 🏛️ Siwasup Co-broker OS (Engine v2.0): Area-Based Sharding & Home Area Expansion Spec

**สถานะ:** เอกสารพิมพ์เขียวสถาปัตยกรรม (Future Architectural Milestone)  
**สิทธิ์การเข้าถึง:** แยกโหมดเฉพาะ **System Architect / Platform Lead View (คุณณัฐ - Nassty)** ไม่ปะปนบนหน้างานปฏิบัติการของบัว กูล หรือพี่ลิลลี่  
**เป้าหมาย:** บันทึกลอจิกและเกณฑ์ชี้วัดคณิตศาสตร์สำหรับการเปลี่ยนผ่านจาก Global Pool (125 นายหน้า) สู่ **Home Area (Area-Based Sharding & Quota)** เมื่อเครือข่ายเติบโตในอนาคต

---

## 1. การแบ่งสิทธิ์และสถาปัตยกรรมการเข้าถึง (RBAC Architecture)

| มุมมอง (View Mode) | ผู้ใช้งานหลัก | หน้าที่และสิ่งที่มองเห็นบนระบบ | สิ่งที่ถูกซ่อน (Restricted) |
| :--- | :--- | :--- | :--- |
| **Operational Admin View** | **บัว (Bua), กูล (Jeab), พี่ลิลลี่ (Lily)** | • แผง Executive Metric Strip 5 ช่อง (`แสดงบนเว็บ`, `พร้อมขาย`, `ติดจอง`, `Sold Out เดิม`, `โอนแล้ว`)<br>• จัดการคิวงานประจำวัน, ตรวจสลิปมัดจำ, อนุมัติคิว, เบิก-ส่งกุญแจ NPA | • ซ่อนแผงคำนวณโควตา Eagle Saturation<br>• ซ่อนการวิเคราะห์ Erlang-C Surge Queue<br>• ซ่อนปุ่มสลับ/จำลองแยก Home Area |
| **System Architect Console** | **คุณณัฐ (Nat / Nassty - Platform Lead)** | • แผง **⚙️ System Architect Telemetry** (Obsidian & Satin Gold `#171717` / `#C2A460`)<br>• เกจวัด 3 มิติ (Eagle Cap 15, Erlang-C Surge, Key Dispatch Density)<br>• แถบวิเคราะห์ความพร้อม 7 ทำเล + ปุ่มจำลองแยกโซน (Dry Run) | ไม่ซ่อนอะไร สามารถสลับดูหน้างานของบัว/กูลได้ตลอดเวลา |

---

## 2. กลไกการปลดล็อกเข้าสู่โหมดคุณณัฐ (Secret Access Channels)

1. **URL Parameter ลับ:**
   - เข้าผ่าน URL: `index.html?architect=1` หรือ `index.html?dev=nat`
   - ระบบจะเปิด Console ทันทีและบันทึกสถานะ `localStorage.setItem('siwasup_architect_mode', 'true')`
2. **Easter Egg Triple-Tap ที่โลโก้ S:**
   - กดแตะที่โลโก้ตราประทับตัว **`S`** มุมซ้ายบนติดกัน 3 ครั้ง (Triple-Tap ภายใน 1 วินาที)
   - แผง `nat-architect-console` จะเปิด/ปิด (Toggle) พร้อมบันทึกค่าลง `localStorage` จำสถานะเฉพาะเบราว์เซอร์ของคุณณัฐ

```javascript
// กลไกตรวจจับ Triple-Tap ที่โลโก้ S เพื่อปลดล็อก Architect Console
(function initArchitectModeTrigger() {
  let clickCount = 0;
  let clickTimer = null;

  function toggleArchitectConsole(forceState) {
    const consoleEl = document.getElementById('nat-architect-console');
    if (!consoleEl) return;
    const currentState = !consoleEl.classList.contains('hidden');
    const newState = forceState !== undefined ? forceState : !currentState;
    
    if (newState) {
      consoleEl.classList.remove('hidden');
      localStorage.setItem('siwasup_architect_mode', 'true');
      console.log('🏛️ [Siwasup OS] System Architect Console Activated (Nat View)');
    } else {
      consoleEl.classList.add('hidden');
      localStorage.removeItem('siwasup_architect_mode');
    }
  }

  // 1. ตรวจสอบจาก URL Parameters หรือ localStorage
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('architect') === '1' || urlParams.get('dev') === 'nat' || localStorage.getItem('siwasup_architect_mode') === 'true') {
    toggleArchitectConsole(true);
  }

  // 2. ผูกอีเวนต์ Triple-Click กับโลโก้แบรนด์ S
  const brandLogo = document.getElementById('siwasup-brand-logo') || document.querySelector('.brand-logo-s');
  if (brandLogo) {
    brandLogo.addEventListener('click', () => {
      clickCount++;
      clearTimeout(clickTimer);
      if (clickCount >= 3) {
        toggleArchitectConsole();
        clickCount = 0;
      } else {
        clickTimer = setTimeout(() => { clickCount = 0; }, 800);
      }
    });
  }
})();
```

---

## 3. เกณฑ์ชี้วัดหลัก 4 มิติ (4 Core Operational Bottlenecks)

| มิติการวัดผล (Metric) | ค่าปกติ (Global Pool) | 🟡 Warning Alert (เตรียมความพร้อม) | 🔴 Critical Alert (ต้องเปิด Home Area ทันที) | เหตุผลทางธุรกิจและระบบ (Engine Logic) |
| :--- | :--- | :--- | :--- | :--- |
| **1. โควตา Eagle Cap**<br>*(Hybrid Dual-Gate)* | Active Agents รวม $\le$ 125 คน<br>*(Eagle Top 8% $\approx$ 9–10 คน)* | Active Agents รวมแตะ **150–170 คน**<br>*(Top 8% $\approx$ 12–13 คน)* | Active Agents รวมทะลุ **188 คนขึ้นไป**<br>*(ทำให้ Top 8% ชนเพดาน **15 Eagles**)* | กฎเหล็กของ Engine v2.0 คือ `Min(Top 8%, 15 per Home Area)` เมื่อตัวเลข 8% ของทั้งระบบชนเพดาน 15 คน หากไม่แยกโซน นายหน้าเก่งๆ จะถูกบล็อกไม่ให้ขึ้น Eagle |
| **2. คิวรอ Mentor (Erlang-C Surge)**<br>*(Co-Closing Queue)* | คิวรอ Wolf เฉลี่ยต่ำกว่า 5 เคส | เกิด `isSurgeActive = true` (คิวรอเกิน 10 เคส) **มากกว่า 3 ครั้ง/สัปดาห์** | คิวรอ Wolf ค้างเกิน **10 เคส ติดต่อกันเกิน 48 ชม.** แม้เปิด Surge Mode (3 เคส/Mentor) แล้ว | Mentor ส่วนกลางรับมือไม่ไหว หรือเกิดปัญหา **Cross-Zone Mismatch** (เช่น ส่ง Mentor บางนาไปช่วยดูเคสบางใหญ่ ทำให้ปิดการขายช้าลง) |
| **3. คอขวดเบิกกุญแจ NPA**<br>*(Key Dispatch & Gul/Lily SLA)* | ระยะเวลาเบิก-ส่งกุญแจหน้างาน $\le$ 2 ชม. | คำขอ `REQUESTED_BY_AGENT` ในโซนเดียวกันพุ่งเกิน **15 ครั้ง/สัปดาห์** หรือคิวทับซ้อนเกิน 20% | เกิดสถานะรอนานเกิน SLA หรือ ผู้ประสานงาน/สายตรวจ (กูล/พี่ลิลลี่) ต้องวิ่งข้ามโซนเกิน **3 โซนหลัก/วัน** | ทรัพย์และนายหน้ากระจุกตัวในทำเลใดทำเลหนึ่งสูงเกินไป ต้องแยก Home Area เพื่อตั้ง **จุดพักกุญแจย่อย (Zone Key Hub)** และจัดคิวประจำโซน |
| **4. ความหนาแน่นต่อทำเล**<br>*(Zone Density & Liquidity)* | ทรัพย์และนายหน้ากระจายตัว | ทำเลใดทำเลหนึ่งมีทรัพย์พร้อมขาย $\ge$ **25 รายการ** และ Active Agents ประจำถิ่น $\ge$ **30 คน** | ทำเลนั้นมี Active Agents ทะลุ **45–50 คน** และมี Mentor (Lion/Falcon/Eagle) ในพื้นที่ $\ge$ **8 คน** | ขนาดของทำเลนั้นใหญ่พอที่จะเลี้ยง Ecosystem ของตัวเองได้สมบูรณ์ (มีทั้งทรัพย์, Wolf และ Mentor พอดีโดยไม่ต้องพึ่งพากลุ่มกลาง) |

---

## 4. โค้ด Engine คำนวณ Telemetry สำหรับคุณณัฐ (`siwasup_coclose_engine.js`)

```javascript
/**
 * ฟังก์ชันคำนวณสัญญาณขยายสเกลสู่ Home Area (เฉพาะ System Architect - คุณณัฐ)
 */
function getArchitectScalingTelemetry(systemStats, zoneMetrics) {
  const activeAgents = systemStats.activeAgentsCount || 125;
  
  // 1. คำนวณเพดาน Eagle Quota: Min(Top 8%, 15)
  const rawEagleCount = Math.floor(activeAgents * 0.08);
  const eagleCapSaturation = Math.min(100, Math.round((rawEagleCount / 15) * 100));
  
  // จุดตัด: 188 คน = 15.04 (ชนเพดาน 15 Eagles ทันที)
  const agentsUntilHardCap = Math.max(0, 188 - activeAgents);

  // 2. วิเคราะห์ความพร้อมรายโซน (7 ทำเลหลัก)
  const zoneReadiness = Object.entries(zoneMetrics).map(([zoneName, z]) => {
    // เกณฑ์: นายหน้าประจำถิ่น >= 40, ทรัพย์พร้อมขาย >= 25, Mentor (Lion/Falcon/Eagle) >= 8, เบิกกุญแจ >= 18/สัปดาห์
    const scoreAgent = Math.min(100, (z.activeAgents / 40) * 100);
    const scoreProp = Math.min(100, (z.availableProperties / 25) * 100);
    const scoreMentor = Math.min(100, (z.localMentors / 8) * 100);
    const scoreKey = Math.min(100, (z.weeklyKeyRequests / 18) * 100);

    const readinessPercent = Math.round((scoreAgent * 0.35) + (scoreMentor * 0.30) + (scoreProp * 0.20) + (scoreKey * 0.15));
    
    return {
      zoneName,
      ...z,
      readinessPercent,
      status: readinessPercent >= 95 ? 'READY_TO_SHARD' : (readinessPercent >= 75 ? 'WARMING_UP' : 'GLOBAL_POOL')
    };
  }).sort((a, b) => b.readinessPercent - a.readinessPercent);

  // 3. สรุปสถานะ Alert ถึงคุณณัฐ
  let alertLevel = 'NORMAL'; // NORMAL | WARNING | CRITICAL
  if (rawEagleCount >= 15 || zoneReadiness.some(z => z.status === 'READY_TO_SHARD') || systemStats.surgeHoursLast7Days >= 48) {
    alertLevel = 'CRITICAL';
  } else if (rawEagleCount >= 12 || zoneReadiness.some(z => z.status === 'WARMING_UP') || systemStats.surgeHoursLast7Days >= 24) {
    alertLevel = 'WARNING';
  }

  return {
    alertLevel,
    activeAgents,
    rawEagleCount,
    eagleCapSaturation,
    agentsUntilHardCap,
    surgeHoursLast7Days: systemStats.surgeHoursLast7Days || 0,
    crossZoneMismatchRate: systemStats.crossZoneMismatchRate || 0,
    zoneReadiness
  };
}
```

---

## 5. โครงสร้าง UI แผงควบคุมส่วนตัว (`#nat-architect-console`)

ออกแบบตามกฎ **Digital Luxury Ratio (75-15-5-5)** โทน **Obsidian & Satin Gold (`#171717` / `#C2A460`)**:

```html
<!-- แสดงผลเฉพาะเมื่อเปิดโหมด Architect ของคุณณัฐ (เช่น กดโลโก้ S 3 ครั้ง หรือมี ?architect=1) -->
<section id="nat-architect-console" class="hidden mb-6 bg-neutral-900 text-neutral-100 rounded-2xl border border-neutral-800 shadow-xl overflow-hidden">
  
  <!-- Header Bar: บ่งบอกสิทธิ์ผู้รับผิดชอบระบบชัดเจน -->
  <div class="px-5 py-3 bg-neutral-950 border-b border-neutral-800 flex flex-wrap items-center justify-between gap-2">
    <div class="flex items-center gap-2.5">
      <span class="w-2 h-2 rounded-full bg-[#C2A460] animate-pulse"></span>
      <span class="text-xs font-semibold tracking-wider uppercase text-[#C2A460]">System Architect Console (ดูแลโดย: ณัฐ)</span>
      <span id="scale-status-badge" class="px-2 py-0.5 text-[11px] rounded-full bg-gradient-to-r from-[#990000] to-[#660000] text-[#E5C985] font-medium">
        ⚡ จับตาสเกล: ใกล้จุดแยก Home Area
      </span>
    </div>
    <div class="text-xs text-neutral-400">
      Engine v2.0 Mode: <strong class="text-white">Global Pool (125 Baseline)</strong>
    </div>
  </div>

  <!-- 3 Core Telemetry Gauges -->
  <div class="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-neutral-800">
    
    <!-- มิติที่ 1: เพดานโควตา Eagle -->
    <div class="p-4">
      <div class="flex justify-between items-center mb-1">
        <span class="text-xs text-neutral-400">1. เพดานโควตา Eagle (Top 8% Cap 15)</span>
        <span class="text-xs font-mono text-[#C2A460]">12 / 15 ที่นั่ง (80%)</span>
      </div>
      <div class="w-full h-1.5 bg-neutral-800 rounded-full overflow-hidden my-2">
        <div class="h-full bg-[#C2A460] rounded-full" style="width: 80%"></div>
      </div>
      <p class="text-[11px] text-neutral-400">
        Active ปัจจุบัน: <strong class="text-white">155 คน</strong> (เหลืออีก <strong class="text-amber-400">33 คน</strong> จะชนเพดาน 188 คน ต้องเปิด Home Area)
      </p>
    </div>

    <!-- มิติที่ 2: Erlang-C Surge & Cross-Zone Mismatch -->
    <div class="p-4">
      <div class="flex justify-between items-center mb-1">
        <span class="text-xs text-neutral-400">2. คิว Co-Close & ข้ามโซนผิดฝาผิดตัว</span>
        <span class="text-xs font-mono text-emerald-400">ปกติ (Surge 14 ชม./สัปดาห์)</span>
      </div>
      <div class="w-full h-1.5 bg-neutral-800 rounded-full overflow-hidden my-2">
        <div class="h-full bg-emerald-500 rounded-full" style="width: 30%"></div>
      </div>
      <p class="text-[11px] text-neutral-400">
        จับคู่ Mentor ข้ามโซน: <strong class="text-white">22%</strong> (เกณฑ์เตือนคือเกิน 35% หรือ Surge เกิน 48 ชม.)
      </p>
    </div>

    <!-- มิติที่ 3: คอขวดกุญแจ NPA หน้างาน -->
    <div class="p-4">
      <div class="flex justify-between items-center mb-1">
        <span class="text-xs text-neutral-400">3. ความหนาแน่นเบิกกุญแจ (Key Dispatch)</span>
        <span class="text-xs font-mono text-amber-400">โซนบางใหญ่ พุ่งสูง</span>
      </div>
      <div class="w-full h-1.5 bg-neutral-800 rounded-full overflow-hidden my-2">
        <div class="h-full bg-amber-500 rounded-full" style="width: 78%"></div>
      </div>
      <p class="text-[11px] text-neutral-400">
        โซนบางใหญ่เบิกกุญแจ <strong class="text-white">16 ครั้ง/สัปดาห์</strong> (แตะ 18 ครั้งเมื่อไหร่ ระบบจะแจ้งให้แยกโซนแรก)
      </p>
    </div>

  </div>

  <!-- แถบความพร้อมรายทำเล (Zone Readiness Strip) + ปุ่มสวิตช์ของคุณณัฐ -->
  <div class="px-5 py-3 bg-neutral-950/60 border-t border-neutral-800 flex flex-wrap items-center justify-between gap-3">
    <div class="flex items-center gap-4 overflow-x-auto text-xs py-1">
      <span class="text-neutral-400 whitespace-nowrap">ความพร้อมแยกโซน:</span>
      <span class="px-2.5 py-1 rounded-full bg-neutral-800 text-amber-300 whitespace-nowrap">● บางใหญ่ 88%</span>
      <span class="px-2.5 py-1 rounded-full bg-neutral-800 text-neutral-300 whitespace-nowrap">● ลำลูกกา 72%</span>
      <span class="px-2.5 py-1 rounded-full bg-neutral-800 text-neutral-400 whitespace-nowrap">● บางนา 54%</span>
      <span class="px-2.5 py-1 rounded-full bg-neutral-800 text-neutral-500 whitespace-nowrap">● พระราม 9 41%</span>
    </div>
    <button class="px-3.5 py-1.5 rounded-lg bg-[#C2A460] hover:bg-[#b89d68] text-neutral-950 font-semibold text-xs transition whitespace-nowrap">
      ⚙️ จำลองการแยก Home Area (Dry Run)
    </button>
  </div>

</section>
```

---

## 6. ขั้นตอนการเปลี่ยนผ่านแบบ Hybrid Soft Sharding (3 ระยะ)

1. **ระยะที่ 1: เก็บข้อมูล `primaryHomeArea` และ `secondaryArea` (เมื่อแตะ 140 Agents)**
2. **ระยะที่ 2: Carve-out Hot Zones (แยกเฉพาะโซนที่พร้อมจริง เช่น บางใหญ่/ลำลูกกา ออกมาก่อน ส่วนที่เหลืออยู่ใน General Pool)**
3. **ระยะที่ 3: Overflow Fallback (คิวข้ามโซนอัตโนมัติหาก Mentor ในโซนติดเคสนานเกิน 30 นาที)**


---

## 7. งานวิจัยเชิงลึก 5 มิติ (Deep Research Whitepaper Synthesis)

อ้างอิงเอกสารวิจัยฉบับเต็ม: `E:\TON\#Siwasub\images\แผนการค้นคว้า-โครงสร้างระบบ-co-broker-os-และการจัดการ-5-ช่องโหว่ความเสี่ยง.pdf`

### มิติที่ 1: Non-Stationary Erlang-C Queue (แก้ Weekend Clustering)
- **พฤติกรรมจริง:** 70–80% ของการนัดดูบ้านเกิดขึ้นช่วงสุดสัปดาห์ (ส-อา 10:00–16:00 น.) อัตราการมาถึง $\lambda(t)$ ไม่คงที่
- **สมการคิวแบบแปรผันตามเวลา:**
  $$\lambda(t) = \begin{cases} \lambda_{\text{peak}}, & t \in [10:00, 16:00] \text{ เสาร์–อาทิตย์} \\ \lambda_{\text{off}}, & \text{ช่วงเวลาอื่น ๆ} \end{cases}$$
  $$a(t) = \frac{\lambda(t)}{\mu}, \quad P_{\text{wait}}(t) = C(c(t), a(t))$$
- **Time Slot Reserves & Auto-Surge Trigger:**
  $$\text{If } Q_z > 0 \text{ AND Mentor ในโซนไม่ว่างทุกคน AND เวลารอ } \ge 30 \text{ นาที } \implies \text{isSurgeActive} = \text{true}$$

### มิติที่ 2: Game Theory & Anti-Arbitrage Mechanics
- **Carrot: Cross-Zone Surge Bounty (ชดเชยการเดินทางข้ามโซน):**
  $$\text{Commission}_{\text{mentor}}^{(\text{overflow})} = \text{Commission}_{\text{mentor}}^{(\text{base})} \times (1 + \gamma) \quad (\gamma = 0.10 \implies +10\%)$$
  $$\text{Point}_{\text{mentor}}^{(\text{overflow})} = 150 \times (1 + \delta) \quad (\delta = 0.20 \implies 180 \text{ แต้ม})$$
- **Silent Algorithmic Guardrails (ระบบควบคุมอัตโนมัติ):**
  - **Cooldown Period:** ปล่อยคิว Overflow หลุดเกิน 2 ครั้ง/วัน $\rightarrow$ ระบบพักการจ่ายงานใหม่ 4 ชม. และดีเลย์การมองเห็น Hot Deals 24 ชม.
  - **Pairing Frequency Cap:** $\text{PairCount}_{(w, m)}(90 \text{ วัน}) \le N$ ป้องกันการฮั้วปั๊มแต้มคู่เดิม
  - **Time-to-Close Anomaly:** $T_{\text{close}} = t_{\text{ปิดดีล}} - t_{\text{เปิดดีล}} < 6 \text{ ชม.} \implies$ แจ้งเตือนตรวจยอดผิดปกติ
  - **Home Area Lock-in:** ย้ายได้ไม่เกิน 2 ครั้ง/ปี, ต้องมี Proof of Local Activity ใน 90 วัน, และรีเซ็ตแต้มจัดอันดับใหม่ในโซนใหม่

### มิติที่ 3: Physical Key Custody & Legal Shield (ป.พ.พ. ไทย)
- **เกราะกำบังทางกฎหมาย (ป.พ.พ. มาตรา 657, 659 วรรคสอง, 660, 420):**
  - กุญแจเป็นกรรมสิทธิ์ของธนาคารพาณิชย์ (SCB, KBank, TTB, SAM, BAM)
  - แพลตฟอร์มศิวาทรัพย์จัดทำ **Key Custody Agreement** มอบหมายให้ "Mentor หัวหน้าฐาน (Sub-Hub Custodian)" เป็นผู้รับฝากทรัพย์โดยตรง
  - หากกุญแจสูญหายหรือทรัพย์สินเสียหาย ให้ความรับผิดชอบทางแพ่งตกอยู่กับ Mentor ผู้ถือกุญแจโดยตรง **เพื่อตัดความรับผิดไม่ให้กระเด็นมาถึงผู้บริหาร (กูล/พี่ลิลลี่)**

### มิติที่ 4: 15-Minute Deal-Drop & Grab-Style Live Tracking
- **จิตวิทยาการรอ:** ลูกค้ารอเกิน 15–20 นาที อัตรา Abandonment Rate จะพุ่งสูงแบบ Exponential
- **Dynamic SLA & ETA Matching:**
  - เพิ่มระบบ Live Tracking พิกัด GPS และแสดง ETA ของ Mentor/ผู้ถือกุญแจให้ลูกค้าเห็นแบบโปร่งใส
  - หากลูกค้าเดินทางเหลือ 20 นาที และ Mentor ถึงใน 25 นาที $\rightarrow$ ปรับเวลาผ่อนปรนเป็น 25 นาที (ไม่ผิด SLA)
  - หากลูกค้าถึงหน้างานแล้ว $\rightarrow$ บีบ SLA แจ้งเตือน Mentor ให้ถึงภายใน 15 นาที พร้อมแจ้งเตือนลูกค้าเชิงรุก

### มิติที่ 5: Zero-Downtime Data Sharding Protocol
- **Workflow Draining:** ล็อกไม่รับเคสใหม่ล่วงหน้า 1 ชม. ก่อนตัด Shard เพื่อระบายเคส In-flight ให้จบ 100%
- **Dual Writes & Dual Calculation:** บันทึกและคำนวณ Percentile Ranking คู่ขนานทั้งระบบเก่าและใหม่เพื่อทดสอบ Telemetry
- **Atomic State Consistency:**
  $$\sum \text{Points}_{\text{after sharding}} = \text{Total Points}_{\text{before sharding}}$$

---

## 8. ปรัชญาการสื่อสารและกำหนดกฎเกณฑ์: Carrot First, Algorithmic Guardrails Second

**กฎเหล็กทางจิตวิทยา:** ตัวแทนขาย (Co-Brokers) คือ **"คู่ค้าอิสระ (Partners)"** ไม่ใช่ลูกจ้าง ห้ามประกาศ "กฎการลงโทษ" เด็ดขาด!

1. **หน้าบ้าน (สิ่งที่บัว/กูล ประกาศแก่ตัวแทน 125 คน):**
   - **ใช้ภาษาเชิงบวก (Positive Framing):** ประกาศเฉพาะโอกาสสร้างรายได้, รางวัลความทุ่มเท, โบนัส Surge Bounty ข้ามโซน (+10% ค่าคอมฯ, แต้ม 1.2 เท่า), และการปกป้องสิทธิ์คนทำงานในพื้นที่จริง
   - **ระบบคัดเลือกคนพร้อม:** แทนที่จะบอกว่า "ปฏิเสธงานจะโดนลงโทษ Cooldown 4 ชม." ให้บอกว่า *"เพื่อให้ลูกค้าได้รับการดูแลเร็วที่สุด ระบบจะกระจายเคสให้ Mentor ที่กำลังว่างและพร้อมเข้าพื้นที่ก่อน หากท่านไม่สะดวก ระบบจะพักการแจ้งเตือนไว้ชั่วคราวเพื่อไม่รบกวนเวลาส่วนตัว"*
2. **หลังบ้าน (สิ่งที่คุณณัฐฝังไว้ในโค้ด `siwasup_coclose_engine.js`):**
   - รันระบบ Cooldown อัตโนมัติ, ตรวจจับการฮั้วแต้ม (`PairCount`), และตรวจสอบความผิดปกติของเวลาปิดเคสแบบ **Silent Audit** โดยยิง Alert ไปที่หน้าจอของคุณณัฐ/บัวเพื่อตรวจสอบภายในเงียบๆ โดยไม่สร้างความตื่นตระหนกในเครือข่าย
