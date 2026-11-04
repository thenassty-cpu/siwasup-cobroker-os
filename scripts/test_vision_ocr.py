# scripts/test_vision_ocr.py
# -*- coding: utf-8 -*-
import os
import sys
import base64
import subprocess
import anthropic

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

key = os.environ.get('ANTHROPIC_API_KEY')
if not key:
    cmd = '[System.Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")'
    key = subprocess.check_output(['powershell', '-Command', cmd]).decode('utf-8').strip()

client = anthropic.Anthropic(api_key=key)

img_path = r'C:\Users\ITss-Advice\.gemini\antigravity\brain\17c99f72-a76b-4f3c-8d41-af7fb89d1ef1\.user_uploaded\media_1793804272546_8b0b9e6f.png'
with open(img_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

print("[*] Calling Claude Haiku Vision on test image...")
res = client.messages.create(
    model='claude-haiku-5-5',
    max_tokens=2000,
    thinking={'type': 'disabled'},
    messages=[{
        'role': 'user',
        'content': [
            {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/png', 'data': b64}},
            {'type': 'text', 'text': 'ทำ OCR สกัดข้อความในรูปนี้ออกมาตรงๆ บรรทัดต่อบรรทัด และวิเคราะห์ฟอนต์ที่ใช้สั้นๆ'}
        ]
    }]
)

print(f"Stop reason: {res.stop_reason}, Blocks: {len(res.content)}")
for i, b in enumerate(res.content):
    print(f"Block {i} type: {getattr(b, 'type', None)}")
    if hasattr(b, 'text'):
        print(f"Text:\n{b.text}")
    elif hasattr(b, 'thinking'):
        print(f"Thinking: {b.thinking[:60]}...")

