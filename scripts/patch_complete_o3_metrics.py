import re

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Executive Decision Matrix Cards in HTML (lines ~245-285)
old_cards_pattern = r'<!-- Card 1 -->\s*<div onclick="selectMetricOption\(\'opt1\'\)".*?<!-- Card 3 -->\s*<div onclick="selectMetricOption\(\'opt3\'\)".*?</div>\s*</div>'

new_cards = '''<!-- Card 1: o3 Deep Research Formula (Winning Choice) -->
        <div onclick="selectMetricOption('opt1')" class="p-2.5 sm:p-3 rounded-xl border border-emerald-300 bg-emerald-50/70 hover:bg-emerald-50 cursor-pointer transition space-y-1.5 shadow-2xs">
          <div class="flex items-center justify-between">
            <span class="font-bold text-emerald-950 text-[11px] flex items-center gap-1">
              <span>🏆 แบบที่ 1: ผลวิจัย o3 Deep Research (ยาแก้ 4 ความกลัว)</span>
            </span>
            <span class="text-[9.5px] font-bold px-1.5 py-0.5 rounded bg-emerald-600 text-white">แนะนำสูงสุด</span>
          </div>
          <div class="grid grid-cols-4 gap-1 text-center bg-white rounded-lg p-1.5 border border-emerald-100 text-[10px]">
            <div><span class="text-slate-400 block text-[8px]">ค่านายหน้า</span><strong class="text-emerald-700 text-[11px]">0 บาท</strong></div>
            <div><span class="text-slate-400 block text-[8px]">ดันกู้ผ่าน</span><strong class="text-emerald-700 text-[11px]">50+ ราย</strong></div>
            <div><span class="text-slate-400 block text-[8px]">ปิดสำเร็จ</span><strong class="text-slate-900 text-[11px]">45+ หลัง</strong></div>
            <div><span class="text-slate-400 block text-[8px]">ตอบกลับไว</span><strong class="text-slate-900 text-[11px]">15 นาที</strong></div>
          </div>
          <p class="text-[9.5px] text-emerald-800 leading-tight">
            ✓ ขจัด Lifetime Curse ไม่เป็นตราบาปตัวแทน ✓ ชนะใจคนซื้อบ้านด้วยความโปร่งใส 0 บาทและ SLA ทันใจ
          </p>
        </div>

        <!-- Card 2: Annual Period Percent Formula -->
        <div onclick="selectMetricOption('opt2')" class="p-2.5 sm:p-3 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100/80 cursor-pointer transition space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-[11px]">แบบที่ 2: สูตรเปอร์เซ็นต์ตัดรอบปี (Annual Period)</span>
            <span class="text-[9.5px] font-semibold text-slate-500">คลิกดู</span>
          </div>
          <div class="grid grid-cols-4 gap-1 text-center bg-white rounded-lg p-1.5 border border-slate-200 text-[10px]">
            <div><span class="text-slate-400 block text-[8px]">ค่านายหน้า</span><strong class="text-emerald-600 text-[11px]">0 บาท</strong></div>
            <div><span class="text-slate-400 block text-[8px]">กู้ผ่าน (ปี 26)</span><strong class="text-emerald-600 text-[11px]">98%</strong></div>
            <div><span class="text-slate-400 block text-[8px]">ปิดสำเร็จ</span><strong class="text-slate-900 text-[11px]">45+ หลัง</strong></div>
            <div><span class="text-slate-400 block text-[8px]">ตอบกลับไว</span><strong class="text-slate-900 text-[11px]">15 นาที</strong></div>
          </div>
        </div>

        <!-- Card 3: Soft & Friendly Formula -->
        <div onclick="selectMetricOption('opt3')" class="p-2.5 sm:p-3 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100/80 cursor-pointer transition space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-[11px]">แบบที่ 3: สายนุ่มนวล เป็นมิตร สบายใจ (Friendly Advisor)</span>
            <span class="text-[9.5px] font-semibold text-slate-500">คลิกดู</span>
          </div>
          <div class="grid grid-cols-4 gap-1 text-center bg-white rounded-lg p-1.5 border border-slate-200 text-[10px]">
            <div><span class="text-slate-400 block text-[8px]">พานำชม</span><strong class="text-emerald-600 text-[11px]">ฟรี</strong></div>
            <div><span class="text-slate-400 block text-[8px]">ช่วยสินเชื่อ</span><strong class="text-emerald-600 text-[11px]">ดูแลครบ</strong></div>
            <div><span class="text-slate-400 block text-[8px]">ปิดสำเร็จ</span><strong class="text-slate-900 text-[11px]">45+ หลัง</strong></div>
            <div><span class="text-slate-400 block text-[8px]">ตอบกลับไว</span><strong class="text-slate-900 text-[11px]">15 นาที</strong></div>
          </div>
        </div>'''

html = re.sub(old_cards_pattern, new_cards, html, flags=re.DOTALL)

# 2. Update METRIC_OPTIONS Javascript object cleanly
start_marker = 'const METRIC_OPTIONS = {'
end_marker = 'function init()'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_js = '''const METRIC_OPTIONS = {
      opt1: {
        id: "opt1",
        name: "แบบที่ 1: สูตรงานวิจัย o3 Deep Research (ยาแก้ 4 ความกลัว)",
        badge: "ผลวิจัย o3 🏆",
        tag: "Trust & Morale สูงสุด",
        desc: "ขจัด 4 ความกลัวของคนซื้อบ้าน: <strong>1. ผู้ซื้อ 0 บาท</strong> (ไม่มีค่าใช้จ่ายแอบแฝง) + <strong>2. ดันผ่าน 50+ ราย</strong> (ยอดสะสมเชิงบวก ไม่เป็นตราบาปตัวแทน) + <strong>3. ปิดสำเร็จ 45+ หลัง</strong> (หลักฐานความสำเร็จจริง) + <strong>4. ตอบไว ใน 15 นาที</strong> (SLA ชี้ขาดตลาด)",
        metrics: [
          { label: "ค่านายหน้าผู้ซื้อ", value: "0 บาท", isHighlight: true },
          { label: "ช่วยกู้ผ่านแล้ว", value: "50+ ราย", isHighlight: true },
          { label: "ปิดการขายสำเร็จ", value: "45+ หลัง", isHighlight: false },
          { label: "ตอบกลับเฉลี่ย", value: "15 นาที", isHighlight: false }
        ]
      },
      opt2: {
        id: "opt2",
        name: "แบบที่ 2: สูตรเปอร์เซ็นต์ตัดรอบปี (Annual Period)",
        badge: "Percent & Track",
        tag: "โชว์สถิติรายปี",
        desc: "ใช้เปอร์เซ็นต์ที่ระบุรอบปีชัดเจน <strong>'สินเชื่อผ่าน 98% (ปี 2026)'</strong> เพื่อไม่ให้เป็นสถิติตลอดชีพติดตัวตัวแทนไปจนตาย ผสานกับยอดพาชมจริง และยอดปิดการขาย",
        metrics: [
          { label: "ค่านายหน้าผู้ซื้อ", value: "0 บาท", isHighlight: true },
          { label: "กู้ผ่าน (ปี 26)", value: "98%", isHighlight: true },
          { label: "ปิดการขายสำเร็จ", value: "45+ หลัง", isHighlight: false },
          { label: "ตอบกลับไว", value: "15 นาที", isHighlight: false }
        ]
      },
      opt3: {
        id: "opt3",
        name: "แบบที่ 3: สายนุ่มนวล เป็นมิตร สบายใจ (Friendly Advisor)",
        badge: "Soft & Friendly",
        tag: "เข้าถึงง่ายสุด",
        desc: "เน้นบริการนำชมฟรีและดูแลครบวงจร ปรึกษาได้ตลอดเวลา เหมาะสำหรับดึงดูดลูกค้าที่ยังมีความลังเลหรือไม่กล้าคุยกับนายหน้า",
        metrics: [
          { label: "พานำชมบ้าน", value: "ฟรี", isHighlight: true },
          { label: "ช่วยสินเชื่อ", value: "ดูแลครบ", isHighlight: true },
          { label: "ปิดการขายสำเร็จ", value: "45+ หลัง", isHighlight: false },
          { label: "ตอบกลับไว", value: "15 นาที", isHighlight: false }
        ]
      }
    };

    '''
    html = html[:start_idx] + new_js + html[end_idx:]
    print("Replaced METRIC_OPTIONS JS successfully!")
else:
    print("Warning: markers not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: agent_profile.html updated with complete o3 Deep Research findings!")
