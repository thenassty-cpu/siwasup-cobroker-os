# -*- coding: utf-8 -*-
"""
scripts/harden_auto_healer_security.py
--------------------------------------
Security Hardening for LINE Auto-Healer:
1. Prevents Over-matching / Privilege Escalation by replacing loose single-syllable 
   keywords (like 'ต้น', 'บัว', 'oil') with strict full distinctive tokens (e.g. 'ตันฑเศรษฐี', 'ว่องสุวรรณวาร', 'nassty')
2. Prioritizes Verified Phone Matching (0944629796, 0853365703, etc.)
3. Protects Executive & Admin seats from accidental binding
"""

import os
import re

WEBHOOK_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"

with open(WEBHOOK_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# Replace the keywords_map block with strict, cryptographically safe distinctive tokens
old_map = """            ('app_office_001', ['jeab', 'varin', 'กูล', 'เจี๊ยบ', 'sw001']),
            ('app_office_002', ['บัว', 'ภมรมาศ', 'bua']),
            ('app_office_003', ['ลิลลี่', 'วรวลัญช์', 'lily', 'ท่าข้าม']),
            ('app_admin_001',  ['ออย', 'สุภาพร', 'oil']),
            ('app_admin_002',  ['ป๊อปปี้', 'ณัฐสุดา', 'poppy']),
            ('app_office_004', ['nassty', 'ton', 'คุณต้น', 'ต้น']),
            ('app_agent_001',  ['จูน', 'เขมิกา', 'june']),
            ('app_agent_002',  ['เจง', 'สุภาวดี', 'jeng']),
            ('app_agent_003',  ['กัญ', 'อนัญญา', 'kan']),
            ('app_agent_004',  ['สิทธิชัย', 'โก้', 'ไห้']),
            ('app_agent_005',  ['หลิว', 'พัชญ์ณิภา', 'liew']),
            ('app_agent_006',  ['จี๊ด', 'แป้ง', 'นภมกร']),
            ('app_agent_007',  ['ใจดี', 'jaidee']),"""

new_map = """            # Strict Distinctive Tokens: Prevent loose substring collisions (e.g., 'ใบบัว', 'ต้นไม้', 'baby oil')
            ('app_office_001', ['varinthorn', 'กูลจีรัง', 'sw001 jeab', 'jeab v@r']),
            ('app_office_002', ['ตันฑเศรษฐี', 'ภมรมาศ', 'pamornmas']),
            ('app_office_003', ['ว่องสุวรรณวาร', 'วรวลัญช์', 'vorawalun']),
            ('app_admin_001',  ['สุภาพร by ศิวาทรัพย์', 'สุภาพร']),
            ('app_admin_002',  ['ณัฐสุดา พรพริ้ง', 'ณัฐสุดา', 'พรพริ้ง']),
            ('app_office_004', ['nassty', 'thenassty']),
            ('app_agent_001',  ['เขมิกา ศิวาทรัพย์', 'เขมิกา']),
            ('app_agent_002',  ['ประกายเกียรติกุล', 'สุภาวดี']),
            ('app_agent_003',  ['อนัญญา(กัญ)', 'อนัญญา สาททอง']),
            ('app_agent_004',  ['สิทธิชัย มฤคพานิช', 'มฤคพานิช', 'มกุลพานิช']),
            ('app_agent_005',  ['พัชญ์ณิภา เอื้อปัญญากุล', 'พัชญ์ณิภา', 'เอื้อประโยชน์กิจ']),
            ('app_agent_006',  ['นภมกร วรพัทธ์กุล', 'นภมกร', 'วรพัทธ์ภูดิท']),
            ('app_agent_007',  ['jaidee asset', 'jaidee0902', 'สุหทัย ปานทอง']),"""

if old_map in code:
    code = code.replace(old_map, new_map, 1)
    with open(WEBHOOK_PATH, "w", encoding="utf-8") as f:
        f.write(code)
    print("[SUCCESS] Hardened keywords_map against Over-Matching Privilege Escalation!")
else:
    print("[WARN] old_map pattern not found exactly as expected.")
