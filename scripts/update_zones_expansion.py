import os

ROOT = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

# ==============================================================================
# 1. UPDATE agent_registration.html
# ==============================================================================
reg_path = os.path.join(ROOT, "agent_registration.html")
with open(reg_path, "r", encoding="utf-8") as f:
    reg_html = f.read()

old_zone_block = """        <!-- Territory Zone -->
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
        </div>"""

new_zone_block = """        <!-- Territory Zone (Expanded + Custom Input) -->
        <div class="space-y-2">
          <label class="text-xs font-bold text-slate-700 flex items-center justify-between">
            <span class="flex items-center gap-1.5">
              <i data-lucide="map-pin" class="w-3.5 h-3.5 text-rose-600"></i>
              <span>โซนพื้นที่ที่ท่านเชี่ยวชาญ / ปฏิบัติงาน *</span>
            </span>
            <span class="text-[10px] font-medium text-amber-700">เลือกจากรายการ หรือพิมพ์ระบุเองได้</span>
          </label>
          <select id="regZone" onchange="handleZoneSelectChange(this.value)" class="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-semibold text-slate-900 focus:outline-none focus:border-amber-500 transition">
            <optgroup label="🏢 ส่วนกลาง / สำนักงานใหญ่">
              <option value="โซนท่าข้าม-พระราม 2">โซนท่าข้าม - พระราม 2 (Hub ใหญ่ศิวาทรัพย์)</option>
              <option value="สำนักงานใหญ่">สำนักงานใหญ่ / ดูแลทุกโซนพื้นที่</option>
            </optgroup>
            <optgroup label="🌉 โซนฝั่งธนบุรี & กรุงเทพฯ ตะวันตก">
              <option value="โซนพระราม 2-บางขุนเทียน">โซนพระราม 2 - ท่าข้าม - บางขุนเทียน - แสมดำ</option>
              <option value="โซนสุขสวัสดิ์-ประชาอุทิศ">โซนสุขสวัสดิ์ - ประชาอุทิศ - ทุ่งครุ - ราษฎร์บูรณะ</option>
              <option value="โซนธนบุรี-ดาวคะนอง-ท่าพระ">โซนธนบุรี - ดาวคะนอง - ท่าพระ - เจริญนคร</option>
              <option value="โซนเพชรเกษม-บางแค-หนองแขม">โซนเพชรเกษม - บางแค - หนองแขม - พุทธมณฑล</option>
              <option value="โซนปิ่นเกล้า-ตลิ่งชัน-จรัญฯ">โซนปิ่นเกล้า - ตลิ่งชัน - จรัญสนิทวงศ์ - บางพลัด</option>
              <option value="โซนกัลปพฤกษ์-ราชพฤกษ์-บางหว้า">โซนกัลปพฤกษ์ - ราชพฤกษ์ - บางหว้า - ตลาดพลู</option>
            </optgroup>
            <optgroup label="🏙️ โซนกรุงเทพฯ ตอนเหนือ & ตะวันออก">
              <option value="โซนรามอินทรา-วัชรพล-สายไหม">โซนรามอินทรา - วัชรพล - สายไหม - สุขาภิบาล 5</option>
              <option value="โซนวิภาวดี-ดอนเมือง-แจ้งวัฒนะ">โซนวิภาวดี - ดอนเมือง - หลักสี่ - แจ้งวัฒนะ</option>
              <option value="โซนลาดพร้าว-เกษตรนวมินทร์">โซนลาดพร้าว - เกษตรนวมินทร์ - โชคชัย 4 - วังหิน</option>
              <option value="โซนรัชดา-พระราม 9-ห้วยขวาง">โซนรัชดา - พระราม 9 - ห้วยขวาง - สุทธิสาร</option>
              <option value="โซนรามคำแหง-บางกะปิ-เสรีไทย">โซนรามคำแหง - บางกะปิ - เสรีไทย - สะพานสูง</option>
              <option value="โซนมีนบุรี-หทัยราษฎร์-คลองสามวา">โซนมีนบุรี - หทัยราษฎร์ - นิมิตใหม่ - คลองสามวา</option>
              <option value="โซนลาดกระบัง-สุวินทวงศ์-ร่มเกล้า">โซนลาดกระบัง - สุวินทวงศ์ - ร่มเกล้า - ประเวศ</option>
              <option value="โซนบางนา-ศรีนครินทร์-อุดมสุข">โซนบางนา - ศรีนครินทร์ - อุดมสุข - อ่อนนุช</option>
            </optgroup>
            <optgroup label="🏢 โซนใจกลางเมือง (CBD)">
              <option value="โซนสุขุมวิท-ทองหล่อ-เอกมัย">โซนสุขุมวิท - ทองหล่อ - เอกมัย - พระโขนง</option>
              <option value="โซนสีลม-สาทร-พระราม 3">โซนสีลม - สาทร - พระราม 3 - เจริญกรุง</option>
              <option value="โซนปทุมวัน-สยาม-พญาไท-อารีย์">โซนปทุมวัน - สยาม - พญาไท - อารีย์ - ดินแดง</option>
            </optgroup>
            <optgroup label="🏡 โซนปริมณฑล & จังหวัดใกล้เคียง">
              <option value="โซนนนทบุรี-บางใหญ่-บางบัวทอง">โซนนนทบุรี - บางใหญ่ - บางบัวทอง - เวสต์เกต</option>
              <option value="โซนนนทบุรี-เมืองนนท์-ปากเกร็ด">โซนนนทบุรี - เมืองนนท์ - แคราย - ปากเกร็ด - ติวานนท์</option>
              <option value="โซนปทุมธานี-ลำลูกกา-รังสิต">โซนปทุมธานี - ลำลูกกา - รังสิต - ธัญบุรี - คลองหลวง</option>
              <option value="โซนสมุทรปราการ-เทพารักษ์-บางพลี">โซนสมุทรปราการ - เทพารักษ์ - แพรกษา - บางพลี - สำโรง</option>
              <option value="โซนสมุทรสาคร-มหาชัย-กระทุ่มแบน">โซนสมุทรสาคร - มหาชัย - กระทุ่มแบน - พันท้ายนรสิงห์</option>
              <option value="โซนนครปฐม-ศาลายา-สามพราน">โซนนครปฐม - ศาลายา - สามพราน - นครชัยศรี</option>
              <option value="โซนชลบุรี-พัทยา-ศรีราชา">โซนชลบุรี - พัทยา - ศรีราชา - บางแสน</option>
            </optgroup>
            <optgroup label="✏️ ระบุพื้นที่อื่นๆ ด้วยตนเอง">
              <option value="__custom__">✏️ อื่นๆ (พิมพ์ระบุโซน / อำเภอ / จังหวัดด้วยตนเอง...)</option>
            </optgroup>
          </select>

          <!-- Custom Zone Input Box -->
          <div id="regZoneCustomWrapper" class="pt-0.5">
            <div class="relative">
              <input type="text" id="regZoneCustom" placeholder="✏️ พิมพ์ระบุโซน/พื้นที่ย่อยเพิ่มเติมได้ (เช่น ประชาอุทิศ 90, บางปู, อยุธยา...)" class="w-full bg-amber-50/40 border border-slate-300 rounded-xl px-3.5 py-2 text-xs text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none focus:border-amber-500 transition">
            </div>
          </div>
        </div>"""

assert old_zone_block in reg_html, "old_zone_block not found"
reg_html = reg_html.replace(old_zone_block, new_zone_block, 1)

old_zone_js = """      const lineId = document.getElementById('regLineId').value.trim();
      const zone = document.getElementById('regZone').value;
      const affiliation = document.querySelector('input[name="affiliation"]:checked').value;"""

new_zone_js = """      const lineId = document.getElementById('regLineId').value.trim();
      const rawZone = document.getElementById('regZone').value;
      const customZone = (document.getElementById('regZoneCustom') ? document.getElementById('regZoneCustom').value.trim() : '');
      if (rawZone === '__custom__' && !customZone) {
        alert("⚠️ กรุณาพิมพ์ระบุโซนพื้นที่ที่ท่านดูแลในช่องระบุพื้นที่ด้วยครับ");
        document.getElementById('regZoneCustom').focus();
        return;
      }
      let zone = rawZone;
      if (rawZone === '__custom__') {
        zone = customZone.startsWith('โซน') ? customZone : `โซน${customZone}`;
      } else if (customZone) {
        zone = `${rawZone} (${customZone})`;
      }
      const affiliation = document.querySelector('input[name="affiliation"]:checked').value;"""

assert old_zone_js in reg_html, "old_zone_js not found"
reg_html = reg_html.replace(old_zone_js, new_zone_js, 1)

# Add handleZoneSelectChange helper right before submitToLobby
old_submit_fn = "    function submitToLobby() {"
new_submit_fn = """    function handleZoneSelectChange(val) {
      const customInput = document.getElementById('regZoneCustom');
      if (!customInput) return;
      if (val === '__custom__') {
        customInput.placeholder = "✏️ กรุณาพิมพ์ระบุโซน / อำเภอ / จังหวัดที่ท่านดูแล *";
        customInput.className = "w-full bg-amber-50 border-2 border-amber-500 rounded-xl px-3.5 py-2.5 text-xs font-semibold text-slate-900 placeholder-amber-700/70 focus:bg-white focus:outline-none transition";
        customInput.focus();
      } else {
        customInput.placeholder = "✏️ พิมพ์ระบุโซน/พื้นที่ย่อยเพิ่มเติมได้ (เช่น ประชาอุทิศ 90, บางปู, อยุธยา...)";
        customInput.className = "w-full bg-amber-50/40 border border-slate-300 rounded-xl px-3.5 py-2 text-xs text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none focus:border-amber-500 transition";
      }
    }

    function submitToLobby() {"""

assert old_submit_fn in reg_html, "old_submit_fn not found"
reg_html = reg_html.replace(old_submit_fn, new_submit_fn, 1)

with open(reg_path, "w", encoding="utf-8") as f:
    f.write(reg_html)

print("Updated agent_registration.html with expanded zones + custom input!")

# ==============================================================================
# 2. UPDATE admin_lobby_manager.html (Add Zone selector + custom input in Edit Modal)
# ==============================================================================
lobby_path = os.path.join(ROOT, "admin_lobby_manager.html")
with open(lobby_path, "r", encoding="utf-8") as f:
    lobby_html = f.read()

old_modal_title_grid = """                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="space-y-1">
            <label class="text-xs font-bold text-slate-700">ตำแหน่งทางการ (Official Title):</label>
            <input type="text" id="editMemberTitleInput" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none focus:border-amber-500">
          </div>
          
        </div>"""

new_modal_title_grid = """        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="space-y-1">
            <label class="text-xs font-bold text-slate-700">ตำแหน่งทางการ (Official Title):</label>
            <input type="text" id="editMemberTitleInput" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900 focus:outline-none focus:border-amber-500">
          </div>
          <div class="space-y-1">
            <label class="text-xs font-bold text-slate-700">โซนพื้นที่ดูแล (เลือกหรือพิมพ์ระบุเอง):</label>
            <input type="text" id="editMemberZoneInput" list="siwasupZoneSuggestions" placeholder="เลือกหรือพิมพ์ระบุโซน..." class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold text-slate-900 focus:outline-none focus:border-amber-500">
            <datalist id="siwasupZoneSuggestions">
              <option value="โซนท่าข้าม-พระราม 2"></option>
              <option value="สำนักงานใหญ่"></option>
              <option value="โซนพระราม 2-บางขุนเทียน"></option>
              <option value="โซนสุขสวัสดิ์-ประชาอุทิศ"></option>
              <option value="โซนธนบุรี-ดาวคะนอง-ท่าพระ"></option>
              <option value="โซนเพชรเกษม-บางแค-หนองแขม"></option>
              <option value="โซนปิ่นเกล้า-ตลิ่งชัน-จรัญฯ"></option>
              <option value="โซนกัลปพฤกษ์-ราชพฤกษ์-บางหว้า"></option>
              <option value="โซนรามอินทรา-วัชรพล-สายไหม"></option>
              <option value="โซนวิภาวดี-ดอนเมือง-แจ้งวัฒนะ"></option>
              <option value="โซนลาดพร้าว-เกษตรนวมินทร์"></option>
              <option value="โซนรัชดา-พระราม 9-ห้วยขวาง"></option>
              <option value="โซนรามคำแหง-บางกะปิ-เสรีไทย"></option>
              <option value="โซนมีนบุรี-หทัยราษฎร์-คลองสามวา"></option>
              <option value="โซนลาดกระบัง-สุวินทวงศ์-ร่มเกล้า"></option>
              <option value="โซนบางนา-ศรีนครินทร์-อุดมสุข"></option>
              <option value="โซนสุขุมวิท-ทองหล่อ-เอกมัย"></option>
              <option value="โซนสีลม-สาทร-พระราม 3"></option>
              <option value="โซนปทุมวัน-สยาม-พญาไท-อารีย์"></option>
              <option value="โซนนนทบุรี-บางใหญ่-บางบัวทอง"></option>
              <option value="โซนนนทบุรี-เมืองนนท์-ปากเกร็ด"></option>
              <option value="โซนปทุมธานี-ลำลูกกา-รังสิต"></option>
              <option value="โซนสมุทรปราการ-เทพารักษ์-บางพลี"></option>
              <option value="โซนสมุทรสาคร-มหาชัย-กระทุ่มแบน"></option>
              <option value="โซนนครปฐม-ศาลายา-สามพราน"></option>
              <option value="โซนชลบุรี-พัทยา-ศรีราชา"></option>
            </datalist>
          </div>
        </div>"""

assert old_modal_title_grid in lobby_html, "old_modal_title_grid not found"
lobby_html = lobby_html.replace(old_modal_title_grid, new_modal_title_grid, 1)

old_open_modal_inputs = """      document.getElementById('editMemberRoleInput').value = member.role || '';
      document.getElementById('editMemberTitleInput').value = member.title || '';"""

new_open_modal_inputs = """      document.getElementById('editMemberRoleInput').value = member.role || '';
      document.getElementById('editMemberTitleInput').value = member.title || '';
      const zoneInp = document.getElementById('editMemberZoneInput');
      if (zoneInp) zoneInp.value = member.zone || '';"""

assert old_open_modal_inputs in lobby_html, "old_open_modal_inputs not found"
lobby_html = lobby_html.replace(old_open_modal_inputs, new_open_modal_inputs)

old_save_modal_inputs = """      const newRole = document.getElementById('editMemberRoleInput').value.trim() || member.role;
      const newTitle = document.getElementById('editMemberTitleInput').value.trim() || member.title;"""

new_save_modal_inputs = """      const newRole = document.getElementById('editMemberRoleInput').value.trim() || member.role;
      const newTitle = document.getElementById('editMemberTitleInput').value.trim() || member.title;
      const newZoneEl = document.getElementById('editMemberZoneInput');
      const newZone = (newZoneEl && newZoneEl.value.trim()) ? newZoneEl.value.trim() : member.zone;"""

assert old_save_modal_inputs in lobby_html, "old_save_modal_inputs not found"
lobby_html = lobby_html.replace(old_save_modal_inputs, new_save_modal_inputs)

old_assign_member = """      member.role = newRole;
      member.title = newTitle;
      member.permissions = newPerms;
      member.badges = newBadges;"""

new_assign_member = """      member.role = newRole;
      member.title = newTitle;
      member.zone = newZone;
      member.permissions = newPerms;
      member.badges = newBadges;"""

assert old_assign_member in lobby_html, "old_assign_member not found"
lobby_html = lobby_html.replace(old_assign_member, new_assign_member)

with open(lobby_path, "w", encoding="utf-8") as f:
    f.write(lobby_html)

print("Updated admin_lobby_manager.html with zone editing + datalist!")
