# -*- coding: utf-8 -*-
import os
import sys
import re
import ssl
import hashlib
import hmac
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
DASHBOARD_PATH = os.path.join(WEB_DIR, "crawler_dashboard.html")

# Read current HTML
with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Card 2 in Essential Telemetry
old_card2 = '''      <!-- Card 2: SCB ETA -->
      <div class="bg-white/85 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 border border-white shadow-xs text-center">
        <div class="text-[9px] sm:text-[10px] text-neutral-400 font-bold uppercase tracking-wider">SCB ETA</div>
        <div id="stat-eta" class="text-xs sm:text-base font-black text-[#4E2A84] mt-0.5 font-mono">~06:45 AM</div>
        <div class="text-[9px] sm:text-[10px] text-emerald-600 font-bold">Morning Target 🌅</div>
      </div>'''

new_card2 = '''      <!-- Card 2: Dynamic ETA (TTB / Total Run) -->
      <div class="bg-white/85 rounded-xl sm:rounded-2xl p-2.5 sm:p-3.5 border border-white shadow-xs text-center">
        <div id="stat-eta-title" class="text-[9px] sm:text-[10px] text-neutral-400 font-bold uppercase tracking-wider">TTB BATCH ETA</div>
        <div id="stat-eta" class="text-xs sm:text-base font-black text-[#0066B3] mt-0.5 font-mono">~04:50 น.</div>
        <div id="stat-eta-sub" class="text-[9px] sm:text-[10px] text-emerald-600 font-bold">Active Ingestion ⚡</div>
      </div>'''

if old_card2 in content:
    content = content.replace(old_card2, new_card2)
    print("[1] Updated Telemetry Card 2 to Dynamic ETA.")

# 2. Fix Action Hub rendering to never show undefined
old_act_render = '''                  <div class="text-[11px] sm:text-xs font-bold text-amber-200 thai-font">${act.title}</div>
                  <div class="text-[10px] sm:text-[11px] text-neutral-300 thai-font mt-0.5">${act.desc}</div>
                </div>
              </div>
              <div class="shrink-0 flex items-center gap-1.5 self-end sm:self-center">
                ${act.status === 'WAITING' ? `
                  <a href="${act.telegram_url}" target="_blank" class="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[10px] sm:text-[11px] flex items-center gap-1.5 shadow-sm transition-transform active:scale-95 font-mono">
                    <span>🟢 อนุมัติผ่าน Telegram</span>
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14h2v2h-2zm0-10h2v8h-2z"/></svg>
                  </a>
                ` : `
                  <span class="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 font-bold text-[10px] border border-emerald-500/30 flex items-center gap-1">
                    <span>✅ อนุมัติเรียบร้อย</span>
                  </span>
                `}
              </div>'''

new_act_render = '''                  <div class="text-[11px] sm:text-xs font-bold text-amber-200 thai-font">${act.title}</div>
                  <div class="text-[10px] sm:text-[11px] text-neutral-300 thai-font mt-0.5">${act.desc || act.description || ''}</div>
                </div>
              </div>
              <div class="shrink-0 flex items-center gap-1.5 self-end sm:self-center">
                ${act.telegram_url ? `
                  <a href="${act.telegram_url}" target="_blank" class="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[10px] sm:text-[11px] flex items-center gap-1.5 shadow-sm transition-transform active:scale-95 font-mono">
                    <span>${act.badge_text || '🟢 ดำเนินการ'}</span>
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14h2v2h-2zm0-10h2v8h-2z"/></svg>
                  </a>
                ` : `
                  <span class="px-2.5 py-1 rounded-lg ${act.badge_class || 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'} font-bold text-[10px] border flex items-center gap-1">
                    <span>${act.badge_text || '✅ สำเร็จแล้ว'}</span>
                  </span>
                `}
              </div>'''

if old_act_render in content:
    content = content.replace(old_act_render, new_act_render)
    print("[2] Fixed Action Hub undefined bug and dynamic badges.")

# 3. Update applyData for dynamic ETA
old_apply_eta = '''      if (data.speed_per_min) document.getElementById('stat-speed').innerText = `~${data.speed_per_min} props/min`;
      if (data.scb_eta_str) document.getElementById('stat-eta').innerText = `~${data.scb_eta_str}`;'''

new_apply_eta = '''      if (data.speed_per_min) document.getElementById('stat-speed').innerText = `~${data.speed_per_min} props/min`;
      if (data.eta_title) document.getElementById('stat-eta-title').innerText = data.eta_title;
      if (data.eta_str || data.scb_eta_str) document.getElementById('stat-eta').innerText = `~${data.eta_str || data.scb_eta_str}`;
      if (data.eta_sub) document.getElementById('stat-eta-sub').innerText = data.eta_sub;'''

if old_apply_eta in content:
    content = content.replace(old_apply_eta, new_apply_eta)
    print("[3] Updated applyData for dynamic ETA fields.")

# 4. Replace and expand Next Target Pipeline & Strategic Portfolio Analysis
# Match from `<!-- Next Target Pipeline & Strategic Portfolio Analysis -->` to before `<!-- Mobile Wi-Fi Info Pill & Ticker -->`
pattern = r'<!-- Next Target Pipeline & Strategic Portfolio Analysis -->.*?<!-- Mobile Wi-Fi Info Pill & Ticker -->'

new_pipeline_section = '''<!-- Next Target Pipeline & Strategic Portfolio Analysis -->
    <div class="mt-4 sm:mt-5 bg-white/85 rounded-xl sm:rounded-2xl p-3.5 sm:p-5 border border-white shadow-xs">
      <div class="flex items-center justify-between mb-3 border-b border-neutral-200/70 pb-2.5">
        <div>
          <div class="text-xs sm:text-base font-black text-neutral-800 flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-[#990000]"></span>
            NEXT TARGET PIPELINE & STRATEGIC VAULT (แผนการดูดข้อมูลเฟสถัดไป)
          </div>
          <div class="text-[10px] sm:text-xs text-neutral-500 font-medium mt-0.5">
            วิเคราะห์คลังขุมทรัพย์ NPA ทั่วประเทศ — เตรียมดูดภาพขึ้น Cloudflare R2 ขยายพอร์ต Siwasup Co-Broker
          </div>
        </div>
        <span class="px-2.5 py-1 rounded-full bg-neutral-900 text-[9px] sm:text-[10px] font-bold text-amber-300 font-mono tracking-wider">
          EXPANDING PIPELINE
        </span>
      </div>

      <!-- Live Active Target Status Pill -->
      <div class="mb-3 p-2.5 rounded-xl bg-gradient-to-r from-emerald-950 via-teal-900 to-neutral-900 text-white flex flex-col sm:flex-row items-center justify-between gap-2 border border-emerald-400/40 shadow-xs">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping shrink-0"></span>
          <span class="text-[11px] sm:text-xs font-bold text-emerald-200 thai-font">
            🏆 <b>PHASE 1 ALL DONE 100%:</b> ครบ 10,672 แปลง (SCB 4,207 • SAM 5,100 • TTB 1,365) ➔ ⚡ <b>Phase 2 Activated:</b> เริ่มเจาะพอร์ต ธอส. (GHB)
          </span>
        </div>
        <span class="text-[10px] font-mono font-bold text-amber-300 bg-black/50 px-2.5 py-1 rounded-lg border border-amber-400/30 shrink-0">
          10,672 TRANCHES ON AIR 🚀
        </span>
      </div>

      <!-- 6 Strategic Target Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 sm:gap-3">
        
        <!-- Target 1: GHB (ธอส.) -->
        <div class="bg-gradient-to-br from-amber-500/10 via-white to-white rounded-xl p-3 border border-amber-300 shadow-2xs hover:shadow-xs transition-shadow">
          <div class="flex items-center justify-between mb-1.5">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-lg bg-[#FF5E00] text-white flex items-center justify-center font-black text-xs shadow-xs">GHB</span>
              <div>
                <div class="text-xs sm:text-sm font-extrabold text-neutral-800">ธอส. (ธนาคารอาคารสงเคราะห์)</div>
                <div class="text-[9px] text-amber-700 font-bold">Priority #1 • Liquidity King 👑</div>
              </div>
            </div>
            <span class="text-[9px] font-mono font-extrabold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-300">ความยาก: ง่าย</span>
          </div>
          <div class="grid grid-cols-3 gap-1 text-center my-2 py-1.5 bg-white/80 rounded-lg border border-neutral-200/60 font-mono text-[9px]">
            <div><span class="text-neutral-400 block text-[8px]">EST. VOL</span><b class="text-neutral-800 font-bold">~8,500 แปลง</b></div>
            <div><span class="text-neutral-400 block text-[8px]">EST. GMV</span><b class="text-neutral-800 font-bold">฿18,500 M</b></div>
            <div><span class="text-neutral-400 block text-[8px]">LIQUIDITY</span><b class="text-emerald-600 font-bold">10/10 (สูงสุด)</b></div>
          </div>
          <p class="text-[10px] text-neutral-600 leading-relaxed thai-font">
            <b>บทวิเคราะห์:</b> พระเอกตลาด Mass Market (ราคา 1-3 ล้านบาท) สินเชื่อดอกเบี้ยต่ำพิเศษ ผ่อนดาวน์ตรงกับแบงก์ได้ ซื้อง่ายขายคล่องที่สุด เหมาะเป็นหัวหอกเปิดดีลสร้างยอดเงินเข้ากระเป๋าให้ทีมเอเจนต์ทันที
          </p>
        </div>

        <!-- Target 2: KBANK (กสิกรไทย) -->
        <div class="bg-gradient-to-br from-emerald-500/10 via-white to-white rounded-xl p-3 border border-emerald-300 shadow-2xs hover:shadow-xs transition-shadow">
          <div class="flex items-center justify-between mb-1.5">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-lg bg-[#00A950] text-white flex items-center justify-center font-black text-xs shadow-xs">K</span>
              <div>
                <div class="text-xs sm:text-sm font-extrabold text-neutral-800">KBANK (K-Property)</div>
                <div class="text-[9px] text-emerald-700 font-bold">Priority #2 • Urban Prime Trust 🏢</div>
              </div>
            </div>
            <span class="text-[9px] font-mono font-extrabold px-1.5 py-0.5 rounded bg-blue-100 text-blue-800 border border-blue-300">ความยาก: ปานกลาง</span>
          </div>
          <div class="grid grid-cols-3 gap-1 text-center my-2 py-1.5 bg-white/80 rounded-lg border border-neutral-200/60 font-mono text-[9px]">
            <div><span class="text-neutral-400 block text-[8px]">EST. VOL</span><b class="text-neutral-800 font-bold">~4,500 แปลง</b></div>
            <div><span class="text-neutral-400 block text-[8px]">EST. GMV</span><b class="text-neutral-800 font-bold">฿25,000 M</b></div>
            <div><span class="text-neutral-400 block text-[8px]">LIQUIDITY</span><b class="text-emerald-600 font-bold">8.5/10 (สูง)</b></div>
          </div>
          <p class="text-[10px] text-neutral-600 leading-relaxed thai-font">
            <b>บทวิเคราะห์:</b> เด่นเรื่องคอนโดและบ้านแนวราบในเมือง Prime Area มูลค่าต่อหลังสูง เอกสารโอนกรรมสิทธิ์คลีน กติกาเบิกกุญแจ 7 วัน (ตรงกับระบบพี่ลิลลี่) ตอบโจทย์ลูกค้าระดับพรีเมียม
          </p>
        </div>

        <!-- Target 3: KTB (กรุงไทย) -->
        <div class="bg-gradient-to-br from-sky-500/10 via-white to-white rounded-xl p-3 border border-sky-300 shadow-2xs hover:shadow-xs transition-shadow">
          <div class="flex items-center justify-between mb-1.5">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-lg bg-[#00A3E0] text-white flex items-center justify-center font-black text-xs shadow-xs">KTB</span>
              <div>
                <div class="text-xs sm:text-sm font-extrabold text-neutral-800">KTB (กรุงไทย NPA)</div>
                <div class="text-[9px] text-sky-700 font-bold">Priority #3 • Community Commercial 🏪</div>
              </div>
            </div>
            <span class="text-[9px] font-mono font-extrabold px-1.5 py-0.5 rounded bg-blue-100 text-blue-800 border border-blue-300">ความยาก: ปานกลาง</span>
          </div>
          <div class="grid grid-cols-3 gap-1 text-center my-2 py-1.5 bg-white/80 rounded-lg border border-neutral-200/60 font-mono text-[9px]">
            <div><span class="text-neutral-400 block text-[8px]">EST. VOL</span><b class="text-neutral-800 font-bold">~2,200 แปลง</b></div>
            <div><span class="text-neutral-400 block text-[8px]">EST. GMV</span><b class="text-neutral-800 font-bold">฿12,000 M</b></div>
            <div><span class="text-neutral-400 block text-[8px]">LIQUIDITY</span><b class="text-emerald-600 font-bold">8.0/10 (สูง)</b></div>
          </div>
          <p class="text-[10px] text-neutral-600 leading-relaxed thai-font">
            <b>บทวิเคราะห์:</b> โดดเด่นด้านอาคารพาณิชย์ ทำเลค้าขาย แหล่งชุมชน ตลาดสด และที่ดินต่างจังหวัด มีเครือข่ายสาขากว้างขวาง กติกาเบิกกุญแจ 7 วันทำการ ซื้อง่ายขายคล่อง
          </p>
        </div>

        <!-- Target 4: BAM (กรุงเทพพาณิชย์) -->
        <div class="bg-gradient-to-br from-blue-500/10 via-white to-white rounded-xl p-3 border border-blue-300 shadow-2xs hover:shadow-xs transition-shadow">
          <div class="flex items-center justify-between mb-1.5">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-lg bg-[#004B87] text-white flex items-center justify-center font-black text-xs shadow-xs">BAM</span>
              <div>
                <div class="text-xs sm:text-sm font-extrabold text-neutral-800">BAM (กรุงเทพพาณิชย์)</div>
                <div class="text-[9px] text-blue-700 font-bold">Priority #4 • Nationwide Titan 🐘</div>
              </div>
            </div>
            <span class="text-[9px] font-mono font-extrabold px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-300">ความยาก: ปานกลาง-สูง</span>
          </div>
          <div class="grid grid-cols-3 gap-1 text-center my-2 py-1.5 bg-white/80 rounded-lg border border-neutral-200/60 font-mono text-[9px]">
            <div><span class="text-neutral-400 block text-[8px]">EST. VOL</span><b class="text-neutral-800 font-bold">~20,000+ แปลง</b></div>
            <div><span class="text-neutral-400 block text-[8px]">EST. GMV</span><b class="text-neutral-800 font-bold">฿75,000+ M</b></div>
            <div><span class="text-neutral-400 block text-[8px]">LIQUIDITY</span><b class="text-amber-600 font-bold">7.5/10 (ปานกลาง)</b></div>
          </div>
          <p class="text-[10px] text-neutral-600 leading-relaxed thai-font">
            <b>บทวิเคราะห์:</b> คลังทรัพย์ที่ใหญ่ที่สุดในประเทศ เด่นเรื่องที่ดินแปลงใหญ่ อาคารพาณิชย์ และทรัพย์ต่างจังหวัด เป็นคลังอาวุธสำคัญสำหรับเครือข่ายทีมคุณกูล (เชียงใหม่ & ภาคเหนือ)
          </p>
        </div>

        <!-- Target 5: GSB (ธนาคารออมสิน) -->
        <div class="bg-gradient-to-br from-pink-500/10 via-white to-white rounded-xl p-3 border border-pink-300 shadow-2xs hover:shadow-xs transition-shadow">
          <div class="flex items-center justify-between mb-1.5">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-lg bg-[#ED008C] text-white flex items-center justify-center font-black text-xs shadow-xs">GSB</span>
              <div>
                <div class="text-xs sm:text-sm font-extrabold text-neutral-800">GSB (ธนาคารออมสิน)</div>
                <div class="text-[9px] text-pink-700 font-bold">Priority #5 • Regional Community 🌸</div>
              </div>
            </div>
            <span class="text-[9px] font-mono font-extrabold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-300">ความยาก: ง่าย</span>
          </div>
          <div class="grid grid-cols-3 gap-1 text-center my-2 py-1.5 bg-white/80 rounded-lg border border-neutral-200/60 font-mono text-[9px]">
            <div><span class="text-neutral-400 block text-[8px]">EST. VOL</span><b class="text-neutral-800 font-bold">~1,210 แปลง</b></div>
            <div><span class="text-neutral-400 block text-[8px]">EST. GMV</span><b class="text-neutral-800 font-bold">฿5,200 M</b></div>
            <div><span class="text-neutral-400 block text-[8px]">LIQUIDITY</span><b class="text-emerald-600 font-bold">7.8/10 (ดี)</b></div>
          </div>
          <p class="text-[10px] text-neutral-600 leading-relaxed thai-font">
            <b>บทวิเคราะห์:</b> มีโครงสร้างข้อมูลและภาพพร้อมอยู่ในคลัง R2 บางส่วนแล้ว เตรียมเปิดขึ้นหน้าเว็บแคตตาล็อกได้เร็ว ทรัพย์กระจายตัวตามแหล่งชุมชน เข้าถึงง่าย
          </p>
        </div>

        <!-- Target 6: LED (กรมบังคับคดี) -->
        <div class="bg-gradient-to-br from-purple-500/10 via-white to-white rounded-xl p-3 border border-purple-300 shadow-2xs hover:shadow-xs transition-shadow">
          <div class="flex items-center justify-between mb-1.5">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-lg bg-[#4E2A84] text-white flex items-center justify-center font-black text-xs shadow-xs">LED</span>
              <div>
                <div class="text-xs sm:text-sm font-extrabold text-neutral-800">LED (กรมบังคับคดี)</div>
                <div class="text-[9px] text-purple-700 font-bold">Phase 3 • Deep Value Auction ⚖️</div>
              </div>
            </div>
            <span class="text-[9px] font-mono font-extrabold px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 border border-rose-300">ความยาก: ซับซ้อน</span>
          </div>
          <div class="grid grid-cols-3 gap-1 text-center my-2 py-1.5 bg-white/80 rounded-lg border border-neutral-200/60 font-mono text-[9px]">
            <div><span class="text-neutral-400 block text-[8px]">EST. VOL</span><b class="text-neutral-800 font-bold">~35,000+ แปลง</b></div>
            <div><span class="text-neutral-400 block text-[8px]">EST. GMV</span><b class="text-neutral-800 font-bold">฿90,000+ M</b></div>
            <div><span class="text-neutral-400 block text-[8px]">LIQUIDITY</span><b class="text-rose-600 font-bold">6.0/10 (เฉพาะกลุ่ม)</b></div>
          </div>
          <p class="text-[10px] text-neutral-600 leading-relaxed thai-font">
            <b>บทวิเคราะห์:</b> ราคาต่ำกว่าตลาด 30-50% มีความซับซ้อนเรื่องนัดประมูล วางมัดจำ และการขับไล่ผู้อยู่อาศัย เหมาะกับกลุ่มนักลงทุนกระเป๋าหนักและเอเจนต์ระดับฉลามปิดดีลเหมา
          </p>
        </div>

      </div>

      <!-- Strategy Recommendation Summary Banner -->
      <div class="mt-3.5 p-3 rounded-xl bg-neutral-900 text-white flex flex-col sm:flex-row items-center justify-between gap-2.5 text-xs">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse shrink-0"></span>
          <span class="text-[11px] sm:text-xs text-neutral-200 thai-font">
            <b>ยุทธศาสตร์แนะนำ Phase 2:</b> ปิดงาน <b>TTB (1.3k แปลง คืนนี้)</b> ➔ ลุย <b>ธอส. (8.5k แปลง สภาพคล่องสูงสุด)</b> ➔ <b>KBANK (คอนโดหรูเมือง)</b> ➔ <b>BAM (คลังภาคเหนือ/คุณกูล)</b>
          </span>
        </div>
        <span class="text-[10px] font-mono font-bold text-amber-300 shrink-0 bg-white/10 px-2.5 py-1 rounded-lg border border-amber-300/30">
          POTENTIAL PIPELINE GMV: +135,700 MB
        </span>
      </div>
    </div>

    <!-- Mobile Wi-Fi Info Pill & Ticker -->'''

content = re.sub(pattern, new_pipeline_section, content, flags=re.DOTALL)
print("[4] Expanded Next Target Pipeline with 6 Banks and TTB Live Batch Status.")

# Save updated HTML
with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
    f.write(content)
print("[5] Successfully saved updated crawler_dashboard.html.")

# Upload to Cloudflare R2
ACCESS_KEY = "21ea6725b31de7a08eb4e15c89181c56"
SECRET_KEY = "ec0b53061b1ca77e0f87b534194dd247949ed82679a591d5eda9752fa14f784a"
ACCOUNT_ID = "b2f4f44870ea14a9a5114dfb6163b48c"
BUCKET = "siwasup-npa-assets"

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def put_object_r2(object_key, data_bytes, content_type="text/html; charset=utf-8"):
    now = datetime.utcnow()
    amz_date = now.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = now.strftime('%Y%m%d')
    region = "auto"
    service = "s3"
    
    host = f"{ACCOUNT_ID}.r2.cloudflarestorage.com"
    payload_hash = hashlib.sha256(data_bytes).hexdigest()
    
    canonical_uri = f"/{BUCKET}/{object_key}"
    canonical_querystring = ""
    canonical_headers = f"content-type:{content_type}\nhost:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
    signed_headers = "content-type;host;x-amz-content-sha256;x-amz-date"
    
    canonical_request = f"PUT\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    
    signing_key = get_signature_key(SECRET_KEY, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    
    authorization_header = f"{algorithm} Credential={ACCESS_KEY}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    
    url = f"https://{host}{canonical_uri}"
    import urllib.request
    req = urllib.request.Request(url, data=data_bytes, method="PUT")
    req.add_header("Content-Type", content_type)
    req.add_header("x-amz-date", amz_date)
    req.add_header("x-amz-content-sha256", payload_hash)
    req.add_header("Authorization", authorization_header)
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return resp.status

status = put_object_r2("crawler_dashboard.html", content.encode("utf-8"), "text/html; charset=utf-8")
print(f"[6] Cloudflare R2 Upload Status: {status} OK! (https://assets.siwasup.com/crawler_dashboard.html)")
