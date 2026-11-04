# -*- coding: utf-8 -*-
import sys
import re

p = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"
with open(p, "r", encoding="utf-8") as f:
    code = f.read()

target = "['ตันฑเศรษฐี', 'ภมรมาศ', 'pamornmas']"
replacement = "['ตันฑุลทุกุล', 'ภมรมาศ', 'pamornmas']"

if target in code:
    code = code.replace(target, replacement, 1)
    with open(p, "w", encoding="utf-8") as f:
        f.write(code)
    print("Successfully replaced with ภมรมาศ ตันฑุลทุกุล")
else:
    print("Warning: target not found")
