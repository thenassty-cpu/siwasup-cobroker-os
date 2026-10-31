# -*- coding: utf-8 -*-
"""
Deploy Automated Pre-Filter NPA for Bua in property_curator.html.
Ensures seamless 1-click filtering of 482 verified bank assets vs 189 sold-out assets.
"""
import os
import sys
import json
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"

# 1. Update all_curation_properties.js to define both ALL_CURATION_PROPERTIES and ALL_CURATION_DATA
json_path = os.path.join(WEB_DIR, "all_curation_properties.json")
with open(json_path, "r", encoding="utf-8") as f:
    props = json.load(f)

js_path = os.path.join(WEB_DIR, "all_curation_properties.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write("window.ALL_CURATION_PROPERTIES = window.ALL_CURATION_DATA = " + json.dumps(props, ensure_ascii=False, indent=2) + ";\n")

print(f"[OK] Updated {js_path} (Total {len(props)} properties)")

# Copy JS & JSON to G:\
shutil.copy2(json_path, os.path.join(G_DIR, "all_curation_properties.json"))
shutil.copy2(js_path, os.path.join(G_DIR, "all_curation_properties.js"))

# 2. Update property_curator.html
curator_path = os.path.join(WEB_DIR, "property_curator.html")
with open(curator_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix data loading check to recognize window.ALL_CURATION_PROPERTIES
old_data_init = """      // 2. Read dataset from all_curation_properties.js (801 items) or fallback
      if (typeof ALL_CURATION_DATA !== 'undefined' && Array.isArray(ALL_CURATION_DATA)) {
        allProperties = ALL_CURATION_DATA;
      } else if (typeof ALL_PROPERTIES_DATA !== 'undefined' && Array.isArray(ALL_PROPERTIES_DATA)) {
        allProperties = ALL_PROPERTIES_DATA;
      } else {"""

new_data_init = """      // 2. Read dataset from all_curation_properties.js (801 items) or fallback
      if (typeof window.ALL_CURATION_PROPERTIES !== 'undefined' && Array.isArray(window.ALL_CURATION_PROPERTIES)) {
        allProperties = window.ALL_CURATION_PROPERTIES;
      } else if (typeof ALL_CURATION_DATA !== 'undefined' && Array.isArray(ALL_CURATION_DATA)) {
        allProperties = ALL_CURATION_DATA;
      } else if (typeof ALL_PROPERTIES_DATA !== 'undefined' && Array.isArray(ALL_PROPERTIES_DATA)) {
        allProperties = ALL_PROPERTIES_DATA;
      } else {"""

html = html.replace(old_data_init, new_data_init)

# Replace the Bua Banner with a rich, interactive Automated Pre-Filter Toolbar
old_banner_marker = '<!-- BUA BANK AUDIT BANNER -->'
if old_banner_marker in html:
    # Remove old banner
    start_idx = html.find('<!-- BUA BANK AUDIT BANNER -->')
    end_idx = html.find('</section>', start_idx) + 10 # wait, let's find the closing div of the banner
    banner_end = html.find('</div>\n  </div>\n', start_idx) + 16
    html = html[:start_idx] + html[banner_end:]

new_prefilter_section = """  <!-- BUA AUTOMATED PRE-FILTER HERO PANEL -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-3 pb-1">
    <div class="bg-gradient-to-r from-[#0d1624] via-[#101b2d] to-[#0d1624] border-2 border-emerald-500/50 rounded-2xl p-4 shadow-xl text-white">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        
        <!-- Left: Status & Notification for Bua -->
        <div class="flex items-start gap-3.5">
          <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 text-slate-950 flex items-center justify-center font-black text-xl shadow-lg shadow-emerald-500/25 flex-shrink-0">
            ⚡
          </div>
          <div>
            <div class="flex items-center gap-2 flex-wrap mb-1">
              <span class="text-[11px] font-black uppercase tracking-wider text-emerald-300 bg-emerald-500/20 border border-emerald-400/40 px-2.5 py-0.5 rounded-full flex items-center gap-1 shadow-sm">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                ระบบคัดกรองอัตโนมัติ (Automated Pre-Filter)
              </span>
              <span class="text-xs text-slate-300 font-medium">✓ เช็กเทียบต้นทางคลังแบงก์ 15,117 แปลงแล้ว</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>แจ้งคุณบัว:</strong> ระบบได้ตรวจเช็ก 671 ทรัพย์ NPA เทียบกับ Master Vault SCB/SAM/GSB เรียบร้อย: 
              อนุมัติ <strong class="text-emerald-400 font-bold">482 แปลงมีในคลังแบงก์ 100%</strong> (พร้อมรหัสและราคาตรงเป๊ะ ปลอดภัยสำหรับทำเป็น Top 20 Hero Deals) 
              และคัดแยก <strong class="text-rose-400 font-bold">189 แปลงที่คาดว่าแบงก์ขายออก/หลุดสต๊อกแล้ว</strong> ออกให้เรียบร้อยค่ะ!
            </p>
          </div>
        </div>

        <!-- Right: 1-Click Filter Chips for Bua -->
        <div class="flex items-center gap-2 flex-wrap lg:flex-nowrap shrink-0">
          <button id="btnFilterSafe" onclick="setAuditMode('safe')" class="px-3.5 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 text-xs font-black shadow-lg shadow-emerald-500/20 transition-all flex items-center gap-1.5 active:scale-95">
            <span>🛡️ โหมดปลอดภัย (มีของจริง 612 แปลง)</span>
          </button>
          <button id="btnFilterBank" onclick="setAuditMode('bank_only')" class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition flex items-center gap-1">
            <span>🟢 เฉพาะแบงก์มีของ (482)</span>
          </button>
          <button id="btnFilterSiwa" onclick="setAuditMode('siwa_only')" class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-semibold border border-amber-500/30 transition flex items-center gap-1">
            <span>✦ ศิวาทรัพย์ (130)</span>
          </button>
          <button id="btnFilterSold" onclick="setAuditMode('sold_out')" class="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-rose-400 text-xs font-medium border border-rose-900/50 transition flex items-center gap-1">
            <span>🔴 แบงก์ตัดสต๊อก (189)</span>
          </button>
          <button id="btnFilterAll" onclick="setAuditMode('all')" class="px-2.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 text-xs font-medium border border-slate-800 transition">
            ดูหมด 801
          </button>
        </div>

      </div>
    </div>
  </div>
"""

# Insert new prefilter section right after header
html = html.replace('</header>', '</header>\n' + new_prefilter_section)

# Update getFilteredProperties logic to handle window.currentAuditMode
old_filter_block = """        // Bank Master Audit Filter
        if (window.currentAuditFilter === 'verified' && item.bank_audit_status === 'bank_sold_out_or_unlisted') {
          return false;
        }"""

new_filter_block = """        // Bank Master Automated Pre-Filter Mode
        if (window.currentAuditMode === 'safe') {
          // Hide all 189 sold-out properties by default
          if (item.bank_audit_status === 'bank_sold_out_or_unlisted') return false;
        } else if (window.currentAuditMode === 'bank_only') {
          if (item.bank_audit_status !== 'verified_bank_active') return false;
        } else if (window.currentAuditMode === 'siwa_only') {
          if (item.bank_audit_status !== 'verified_siwasup') return false;
        } else if (window.currentAuditMode === 'sold_out') {
          if (item.bank_audit_status !== 'bank_sold_out_or_unlisted') return false;
        }"""

html = html.replace(old_filter_block, new_filter_block)

# Add setAuditMode function and set default to 'safe'
old_audit_fn = """    window.currentAuditFilter = 'all';
    function setAuditFilter(mode) {
      window.currentAuditFilter = mode;
      renderGrid();
      showToast(mode === 'verified' ? 'กรองเฉพาะ 482 แปลงที่แบงก์ยืนยันมีของ 100%' : 'แสดงทรัพย์ทั้งหมด');
    }"""

new_audit_fn = """    window.currentAuditMode = 'safe'; // Default: Safe mode (hide 189 sold out)

    function setAuditMode(mode) {
      window.currentAuditMode = mode;
      
      // Update button styles
      const btns = {
        safe: document.getElementById('btnFilterSafe'),
        bank_only: document.getElementById('btnFilterBank'),
        siwa_only: document.getElementById('btnFilterSiwa'),
        sold_out: document.getElementById('btnFilterSold'),
        all: document.getElementById('btnFilterAll')
      };
      
      Object.keys(btns).forEach(k => {
        if (!btns[k]) return;
        if (k === mode) {
          btns[k].className = "px-3.5 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 text-xs font-black shadow-lg shadow-emerald-500/25 transition-all flex items-center gap-1.5";
        } else {
          btns[k].className = "px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-medium border border-slate-800 transition flex items-center gap-1";
        }
      });

      renderGrid();

      const msgs = {
        safe: '🛡️ โหมดปลอดภัย: แสดงเฉพาะ 612 แปลงที่มีของจริง 100% (ซ่อน 189 แปลงที่ตัดสต๊อก)',
        bank_only: '🟢 กรองเฉพาะ 482 แปลงที่คลังแบงก์ SCB/SAM/GSB ยืนยันมีของ 100%',
        siwa_only: '✦ กรองเฉพาะ 130 แปลงของศิวาทรัพย์ รีโนเวท',
        sold_out: '🔴 แสดง 189 แปลงที่ตรวจสอบไม่พบในคลังแบงก์ปัจจุบัน (คาดว่าขายแล้ว)',
        all: '🌐 แสดงทรัพย์ทั้งหมด 801 แปลง'
      };
      showToast(msgs[mode] || 'อัปเดตตัวกรองเรียบร้อย');
    }"""

html = html.replace(old_audit_fn, new_audit_fn)

# Write updated HTML
with open(curator_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"[OK] Updated {curator_path}")

# Sync to G:\
shutil.copy2(curator_path, os.path.join(G_DIR, "property_curator.html"))
print(f"[OK] Mirrored to G:\\Siwasup_Presentation_2026\\property_curator.html")

# Deploy to Cloudflare R2
with open(curator_path, "rb") as f:
    st_curator = put_object_r2("property_curator.html", f.read(), "text/html; charset=utf-8")
with open(js_path, "rb") as f:
    st_js = put_object_r2("all_curation_properties.js", f.read(), "application/javascript; charset=utf-8")

print(f"[R2] Deployed property_curator.html (status {st_curator}) and all_curation_properties.js (status {st_js})")
print("=== BUA AUTOMATED PRE-FILTER FULLY DEPLOYED ===")
