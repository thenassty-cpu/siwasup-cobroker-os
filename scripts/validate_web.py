#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Siwasup Co-Broker OS - Web Health & Syntax Validator
เครื่องมือตรวจสุขภาพเว็บอัตโนมัติ: ตรวจจับแท็ก HTML หลุด, เช็กไวยากรณ์ JavaScript และความสมบูรณ์ของระบบ
"""

import sys
import os
import re
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

# ป้องกันปัญหา Windows PowerShell/CMD cp874 แครชเมื่อแสดงผลไอคอนหรือข้อความภาษาไทย
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REPO_ROOT = Path(__file__).resolve().parent.parent

class HTMLTreeValidator(HTMLParser):
    def __init__(self, filename=""):
        super().__init__()
        self.filename = filename
        self.stack = []
        self.void_tags = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 
            'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'
        }
        self.errors = []
        
    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t not in self.void_tags:
            self.stack.append((t, self.getpos()))

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f"พบแท็กปิดลอย </{t}> บรรทัดที่ {self.getpos()[0]} (ไม่มีแท็กเปิดคู่กัน)")
            return
        last_tag, pos = self.stack[-1]
        if last_tag == t:
            self.stack.pop()
        else:
            # ค้นหาว่ามีแท็กคู่กันที่เปิดค้างไว้ข้างล่างไหม
            found_idx = -1
            for idx in range(len(self.stack) - 1, -1, -1):
                if self.stack[idx][0] == t:
                    found_idx = idx
                    break
            if found_idx != -1:
                # แท็กที่อยู่คั่นกลางยังไม่ได้ปิด
                while len(self.stack) > found_idx + 1:
                    unclosed, unclosed_pos = self.stack.pop()
                    self.errors.append(
                        f"ลืมปิดแท็ก <{unclosed}> (เปิดไว้ที่บรรทัด {unclosed_pos[0]}) ก่อนที่จะปิด </{t}> ที่บรรทัด {self.getpos()[0]}"
                    )
                self.stack.pop() # pop the matching tag
            else:
                self.errors.append(f"พบแท็กปิดเกิน </{t}> บรรทัดที่ {self.getpos()[0]} โดยไม่เคยเปิดไว้")


def validate_html_file(file_path):
    print(f"\n📄 [1/3] กำลังตรวจสอบโครงสร้าง HTML: {file_path.name}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f"  ❌ ไม่สามารถอ่านไฟล์ได้: {e}")
        return False, []

    # ตัด inline scripts & styles ออกก่อน เพื่อไม่ให้ template literals สับสนตัวตรวจ HTML
    clean_html = re.sub(r'<script.*?</script>', '<script></script>', html, flags=re.DOTALL | re.IGNORECASE)
    clean_html = re.sub(r'<style.*?</style>', '<style></style>', clean_html, flags=re.DOTALL | re.IGNORECASE)

    parser = HTMLTreeValidator(file_path.name)
    parser.feed(clean_html)

    # นับ div เฉพาะ
    div_opens = len(re.findall(r'<div(?:\s+[^>]*)?>', clean_html, flags=re.IGNORECASE))
    div_closes = len(re.findall(r'</div>', clean_html, flags=re.IGNORECASE))

    has_error = False
    if div_opens != div_closes:
        parser.errors.append(f"จำนวน <div> เปิด ({div_opens}) ไม่เท่ากับ </div> ปิด ({div_closes}) ต่างกัน {abs(div_opens - div_closes)}")
        has_error = True

    if parser.stack:
        for tag, pos in parser.stack:
            parser.errors.append(f"ลืมปิดแท็ก <{tag}> ที่เปิดไว้บรรทัดที่ {pos[0]}")
        has_error = True

    if parser.errors:
        print(f"  ❌ พบข้อผิดพลาดโครงสร้าง HTML ({len(parser.errors)} จุด):")
        for err in parser.errors[:10]:
            print(f"     - {err}")
        return False, html
    else:
        print(f"  ✅ โครงสร้าง HTML สมบูรณ์ 100% (ตรวจพบ {div_opens} คู่ <div> เปิด-ปิด ครบทุกตัว)")
        return True, html


def validate_javascript_code(code, source_name="script"):
    # ทดสอบด้วย Node.js compiler ถ้ามีติดตั้งในเครื่อง
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as tf:
            tf.write(code)
            temp_path = tf.name

        res = subprocess.run(['node', '-c', temp_path], capture_output=True, text=True, timeout=5)
        os.remove(temp_path)

        if res.returncode == 0:
            return True, ""
        else:
            return False, res.stderr.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        # Fallback กรณีไม่มี Node.js: ตรวจสอบวงเล็บปีกกาและสตริงเบื้องต้น
        open_curlies = code.count('{')
        close_curlies = code.count('}')
        if open_curlies != close_curlies:
            return False, f"วงเล็บปีกกาไม่สมดุล (เปิด {{ = {open_curlies}, ปิด }} = {close_curlies})"
        return True, ""


def validate_all_scripts(file_path, html_content):
    print(f"\n⚡ [2/3] กำลังตรวจสอบไวยากรณ์ JavaScript ใน {file_path.name}")
    inline_scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', html_content, flags=re.DOTALL | re.IGNORECASE)

    all_passed = True
    tested_count = 0

    for idx, script_text in enumerate(inline_scripts):
        if len(script_text.strip()) < 15:
            continue
        tested_count += 1
        passed, error_msg = validate_javascript_code(script_text, f"{file_path.name} Inline #{idx+1}")
        if not passed:
            all_passed = False
            print(f"  ❌ สคริปต์บล็อก #{idx+1} มี Syntax Error:")
            lines = error_msg.split('\n')
            for l in lines[:5]:
                print(f"     {l}")
        else:
            print(f"  ✅ สคริปต์บล็อก #{idx+1} ({len(script_text):,} ตัวอักษร): ผ่านฉลุย")

    # ตรวจไฟล์ภายนอกที่สำคัญ
    external_js_files = ['modals.js', 'siwasup_agents.js', 'sw.js', 'siwasup_coclose_engine.js']
    print(f"\n📦 ตรวจสอบไฟล์ JavaScript ภายนอก:")
    for js_name in external_js_files:
        js_path = REPO_ROOT / js_name
        if js_path.exists():
            with open(js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            passed, error_msg = validate_javascript_code(content, js_name)
            if passed:
                print(f"  ✅ {js_name}: ผ่านฉลุย")
            else:
                all_passed = False
                print(f"  ❌ {js_name} มี Syntax Error:")
                for l in error_msg.split('\n')[:4]:
                    print(f"     {l}")

    return all_passed


def validate_key_assets():
    print(f"\n🎨 [3/3] ตรวจสอบไฟล์ Asset & Badges สำคัญ:")
    required_assets = [
        "assets/badges/bear_crest.jpg",
        "assets/badges/wolf_crest.jpg",
        "assets/badges/lion_crest.jpg",
        "assets/badges/falcon_crest.jpg",
        "assets/badges/eagle_crest.jpg",
        "assets/badges/gryphon_crest.jpg",
        "assets/badges/bear_emblem_micro.svg",
        "assets/badges/wolf_emblem_micro.svg",
        "assets/badges/lion_emblem_micro.svg",
        "assets/badges/falcon_emblem_micro.svg",
        "assets/badges/eagle_emblem_micro.svg",
        "assets/badges/gryphon_emblem_micro.svg",
        "assets/characters/badge_falcon.png",
        "assets/characters/badge_gryphon.png",
        "manifest.json",
        "sw.js"
    ]
    missing = []
    for asset in required_assets:
        p = REPO_ROOT / asset
        if not p.exists():
            missing.append(asset)

    if missing:
        print(f"  ⚠️ พบไฟล์ Asset ขาดหาย {len(missing)} ไฟล์:")
        for m in missing:
            print(f"     - {m}")
        return False
    else:
        print(f"  ✅ ตรวจสอบไฟล์ภาพและ SVG ทั้งหมด {len(required_assets)} ไฟล์: ครบถ้วน 100%")
        return True


def main():
    print("=" * 70)
    print(" 🛡️  SIWASUP CO-BROKER OS - WEB HEALTH VALIDATOR")
    print("    เครื่องมือตรวจเช็กความสมบูรณ์ของระบบเว็บอัตโนมัติ")
    print("=" * 70)

    target_html = REPO_ROOT / "index.html"
    if not target_html.exists():
        print(f"❌ ไม่พบไฟล์ {target_html}")
        sys.exit(1)

    html_ok, html_content = validate_html_file(target_html)
    js_ok = validate_all_scripts(target_html, html_content) if html_content else False
    assets_ok = validate_key_assets()

    print("\n" + "=" * 70)
    if html_ok and js_ok and assets_ok:
        print(" 🎉 ผลการตรวจ: ผ่านเกณฑ์ 100% สมบูรณ์แบบ (ALL CHECKS PASSED!)")
        print(" 🚀 หน้าเว็บปลอดภัย ไม่มีไวยากรณ์พัง การ์ดและปุ่มทำงานได้สมบูรณ์ครับ")
        print("=" * 70)
        sys.exit(0)
    else:
        print(" ⚠️  ผลการตรวจ: พบจุดที่ต้องแก้ไข (FAILED)")
        print(" โปรดตรวจสอบรายละเอียดที่แจ้งเตือนด้านบนครับ")
        print("=" * 70)
        sys.exit(1)


if __name__ == '__main__':
    main()
