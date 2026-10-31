import re

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update METRIC_OPTIONS with o3 Deep Research results
old_metric_options_pattern = r'const METRIC_OPTIONS = \{.*?\}\;\s*function init\(\)'

new_metric_options = '''const METRIC_OPTIONS = {
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
        name: "แบบที่ 2: สูตรเปอร์เซ็นต์แบบตัดรอบปี (Annual Period)",
        badge: "Percent & Track",
        tag: "โชว์สถิติรายปี",
        desc: "ใช้เปอร์เซ็นต์ที่ระบุรอบปีชัดเจน <strong>'สินเชื่อผ่าน 98% (ปี 2026)'</strong> เพื่อไม่ให้เป็นสถิติตลอดชีพติดตัวตัวแทนไปจนตาย ผสานกับยอดพาชมจริง 120+ เคส และยอดปิดการขาย",
        metrics: [
          { label: "ค่านายหน้า", value: "0 บาท", isHighlight: true },
          { label: "สินเชื่อผ่าน (ปี 26)", value: "98%", isHighlight: true },
          { label: "ปิดการขายสำเร็จ", value: "45+ หลัง", isHighlight: false },
          { label: "ตอบกลับไว", value: "15 นาที", isHighlight: false }
        ]
      },
      opt3: {
        id: "opt3",
        name: "แบบที่ 3: สายนุ่มนวล สบายใจ ปรึกษาฟรี (Friendly Advisor)",
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

    function init()'''

html = re.sub(old_metric_options_pattern, new_metric_options, html, flags=re.DOTALL)

# 2. Add o3 Recommended Empathetic Tagline under the metrics
old_metrics_container = '''      <!-- Quick Metrics Grid (4 คอลัมน์ ออกแบบให้คมชัด ไม่เบียดบนจอมือถือ) -->
      <div id="metricsContainer" class="pt-1">
        <div id="metricsGrid" class="grid grid-cols-4 gap-1.5 sm:gap-2 text-center">
          <!-- Dynamic JS Render -->
        </div>
      </div>'''

new_metrics_container = '''<!-- Quick Metrics Grid (4 คอลัมน์ ออกแบบให้คมชัด ไม่เบียดบนจอมือถือ) -->
      <div id="metricsContainer" class="pt-1 space-y-1.5">
        <div id="metricsGrid" class="grid grid-cols-4 gap-1.5 sm:gap-2 text-center">
          <!-- Dynamic JS Render -->
        </div>
        <!-- Empathetic Tagline (Recommended by o3 Deep Research) -->
        <div class="text-center pt-0.5">
          <p class="text-[10px] sm:text-[10.5px] text-amber-900/80 font-medium tracking-tight">
            🤝 <em>"ซื้อบ้านเรื่องใหญ่ ปรึกษาเราได้ฟรี... ไม่ซื้อไม่ว่ากัน"</em>
          </p>
        </div>
      </div>'''

html = html.replace(old_metrics_container, new_metrics_container)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: agent_profile.html updated with o3 Deep Research formula and empathetic tagline!")
