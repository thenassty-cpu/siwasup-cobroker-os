# scripts/setup_claude_inspector.py
# -*- coding: utf-8 -*-
import ctypes
import base64
import json
import os
import subprocess
from ctypes import wintypes

class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', wintypes.DWORD), ('pbData', ctypes.POINTER(ctypes.c_byte))]

crypt32 = ctypes.windll.crypt32
kernel32 = ctypes.windll.kernel32

cred_path = r'C:\Users\ITss-Advice\AppData\Local\Packages\AetoxAI.Aetox_qh6w3m69v8a0y\LocalCache\Roaming\aetox\credentials.json'

with open(cred_path, 'r', encoding='utf-8') as f:
    raw = f.read().strip()

if not raw.startswith('dpapi:'):
    raise ValueError("Unexpected credentials format")

ciphertext = base64.b64decode(raw[6:])
in_blob = DATA_BLOB(len(ciphertext), ctypes.cast(ctypes.create_string_buffer(ciphertext), ctypes.POINTER(ctypes.c_byte)))
out_blob = DATA_BLOB()

if not crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob)):
    raise RuntimeError("Failed to decrypt credentials")

buf = ctypes.string_at(out_blob.pbData, out_blob.cbData)
kernel32.LocalFree(out_blob.pbData)
data = json.loads(buf.decode('utf-8'))
key = data['provider_api_keys']['anthropic']

# Set Windows User Environment Variable permanently
cmd = f'[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "{key}", "User")'
subprocess.run(['powershell', '-Command', cmd], check=True)
print('[OK] Set ANTHROPIC_API_KEY permanently in Windows User Environment!')

# Test live connection via anthropic SDK
import anthropic
client = anthropic.Anthropic(api_key=key)
response = client.messages.create(
    model='claude-3-5-sonnet-20241022',
    max_tokens=60,
    messages=[{'role': 'user', 'content': 'รายงานตัวสั้นๆ ประโยคเดียว ในฐานะผู้ตรวจการประจำทีมของพี่ต้น'}]
)
print('[CLAUDE_INSPECTOR_LIVE]:', response.content[0].text)
