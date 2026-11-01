import re

profile_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(profile_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace METRIC_OPTIONS with realistic, honest, platform-backed guarantees
old_metrics_block = '''    const METRIC_OPTIONS = {
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
    };'''

new_metrics_block = '''    const METRIC_OPTIONS = {
      opt1: {
        id: "opt1",
        name: "แบบที่ 1: การันตีมาตรฐานบริการศิวาสัพย์ (Platform Service Guarantee)",
        badge: "มาตรฐานทางการ 🏆",
        tag: "โปร่งใส ตรงปก 100%",
        desc: "ขจัดความกังวลของคนซื้อบ้านด้วยมาตรฐานบริการของเครือข่ายศิวาสัพย์: <strong>1. ผู้ซื้อ 0 บาท</strong> (ไม่คิดค่านายหน้า) + <strong>2. พาชมฟรีทุกหลัง</strong> (ไม่มีเก็บค่าเปิดบ้าน) + <strong>3. ปรึกษาสินเชื่อฟรี</strong> (ยื่นกู้ได้ทุกธนาคาร) + <strong>4. คลังบ้าน 59,000+ หลัง</strong> (สต๊อกบ้าน NPA ใหญ่ที่สุด)",
        metrics: [
          { label: "ค่านายหน้าผู้ซื้อ", value: "0 บาท", isHighlight: true },
          { label: "พานำชมบ้านจริง", value: "ฟรีทุกหลัง", isHighlight: true },
          { label: "ปรึกษาสินเชื่อ", value: "ฟรีทุกแบงก์", isHighlight: false },
          { label: "คลังบ้านในระบบ", value: "59,000+ หลัง", isHighlight: true }
        ]
      },
      opt2: {
        id: "opt2",
        name: "แบบที่ 2: สถิติผลงานการดูแลเคส (Track Record)",
        badge: "Success Rate",
        tag: "อัตราความสำเร็จสูง",
        desc: "เน้นย้ำความมั่นใจด้านการประสานงานสินเชื่อและการอำนวยความสะดวกให้ผู้ซื้อบ้านทุกขั้นตอน",
        metrics: [
          { label: "ค่านายหน้าผู้ซื้อ", value: "0 บาท", isHighlight: true },
          { label: "ช่วยประสานกู้", value: "ดูแลถึงวันโอน", isHighlight: true },
          { label: "พอร์ตทรัพย์ในมือ", value: "59,000+ หลัง", isHighlight: false },
          { label: "ตอบกลับไว", value: "15 นาที", isHighlight: false }
        ]
      },
      opt3: {
        id: "opt3",
        name: "แบบที่ 3: สายนุ่มนวล เป็นมิตร สบายใจ (Friendly Advisor)",
        badge: "Soft & Friendly",
        tag: "เข้าถึงง่ายสุด",
        desc: "เน้นบริการนำชมฟรีและดูแลครบวงจร ปรึกษาได้ตลอดเวลา เหมาะสำหรับผู้ซื้อที่ต้องการที่ปรึกษาที่ไว้ใจได้",
        metrics: [
          { label: "พานำชมบ้านจริง", value: "ฟรีทุกหลัง", isHighlight: true },
          { label: "ช่วยยื่นสินเชื่อ", value: "ดูแลครบ 100%", isHighlight: true },
          { label: "เครือข่าย Co-Broker", value: "ทั่วกรุงเทพฯ", isHighlight: false },
          { label: "ปรึกษาซื้อบ้าน", value: "ฟรีตลอดชีพ", isHighlight: false }
        ]
      }
    };'''

text_norm = text.replace("\r\n", "\n")
old_m_norm = old_metrics_block.replace("\r\n", "\n")

if old_m_norm in text_norm:
    text_norm = text_norm.replace(old_m_norm, new_metrics_block)
    print("Replaced METRIC_OPTIONS with honest, platform-backed metrics!")
else:
    print("Warning: old_metrics_block not found in agent_profile.html")

# Also check role-based dynamic metrics for executives and keybox
role_metrics_patch = '''
      // Check Role-based customized metrics if executive or keybox
      const titleLower = (a.clientTitle || "").toLowerCase();
      if (titleLower.includes("executive") || titleLower.includes("ceo") || titleLower.includes("managing")) {
        opt.metrics = [
          { label: "อำนาจเคาะราคา", value: "ราคาพิเศษ", isHighlight: true },
          { label: "คลังบ้านในพอร์ต", value: "59,000+ หลัง", isHighlight: true },
          { label: "ล็อกค่านายหน้า", value: "60 วันเต็ม", isHighlight: false },
          { label: "สัญญามาตรฐาน", value: "นิติ 100%", isHighlight: false }
        ];
      } else if (titleLower.includes("keybox") || titleLower.includes("viewing") || titleLower.includes("กุญแจ")) {
        opt.metrics = [
          { label: "คุมกล่องกุญแจ", value: "OTP 100%", isHighlight: true },
          { label: "ฮับพื้นที่หลัก", value: "ท่าข้าม 12", isHighlight: true },
          { label: "พานำชมบ้านจริง", value: "ฟรีทุกหลัง", isHighlight: false },
          { label: "ความปลอดภัย", value: "มีพยานบุคคล", isHighlight: false }
        ];
      }
'''

# Insert role_metrics_patch into selectMetricOption before renderMetrics
old_select_fn = '      // Render 4 metrics on card\n      renderMetrics(opt.metrics);'
new_select_fn = role_metrics_patch + '\n      // Render 4 metrics on card\n      renderMetrics(opt.metrics);'

if old_select_fn in text_norm:
    text_norm = text_norm.replace(old_select_fn, new_select_fn, 1)
    print("Added role-based metrics in selectMetricOption!")
else:
    print("Warning: old_select_fn not found")

with open(profile_path, "w", encoding="utf-8") as f:
    f.write(text_norm)

print("Finished updating agent_profile.html with realistic metrics!")
