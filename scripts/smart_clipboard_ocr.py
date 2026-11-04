# scripts/smart_clipboard_ocr.py
# -*- coding: utf-8 -*-
"""
Graphic Studio OCR & Font Inspector
Captures image from clipboard, extracts Thai/English text, identifies font,
and copies the extracted text back into the clipboard for instant pasting!
"""

import os
import sys
import io
import base64
import subprocess
from PIL import ImageGrab, Image
import anthropic

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_api_key():
    key = os.environ.get('ANTHROPIC_API_KEY')
    if not key:
        cmd = '[System.Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")'
        key = subprocess.check_output(['powershell', '-Command', cmd]).decode('utf-8').strip()
    return key

def copy_to_clipboard(text: str):
    """Copy extracted text directly back into Windows clipboard using PowerShell."""
    try:
        proc = subprocess.Popen(['powershell', '-Command', '$input | Set-Clipboard'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
        proc.communicate(input=text)
    except Exception as e:
        print(f"[!] Warning: Could not copy to clipboard: {e}")

def run_clipboard_ocr():
    print("=" * 60)
    print("🎨 GRAPHIC STUDIO - CLIPBOARD OCR & FONT INSPECTOR")
    print("=" * 60)

    # 1. Grab image from clipboard
    im = ImageGrab.grabclipboard()
    if im is None or not isinstance(im, Image.Image):
        print("\n❌ ไม่พบรูปภาพในคลิปบอร์ด!")
        print("💡 วิธีใช้:")
        print("   1. กดปุ่ม [Win + Shift + S] เพื่อแคปภาพส่วนที่ต้องการบนหน้าจอ")
        print("   2. รันสคริปต์นี้อีกครั้ง ระบบจะดูดข้อความและวิเคราะห์ฟอนต์ให้อัตโนมัติครับ")
        return

    print("\n📸 ตรวจพบภาพในคลิปบอร์ดเรียบร้อย!")
    print(f"   ขนาดภาพ: {im.size[0]} x {im.size[1]} พิกเซล, โหมดสี: {im.mode}")

    # Convert to PNG in memory
    buf = io.BytesIO()
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im.save(buf, format='PNG')
    b64_data = base64.b64encode(buf.getvalue()).decode('utf-8')

    print("🤖 กำลังวิเคราะห์ข้อความและฟอนต์ผ่าน Claude Vision...")

    client = anthropic.Anthropic(api_key=get_api_key())

    prompt = (
        "คุณคือผู้ช่วยกราฟิกดีไซเนอร์ประจำห้องแล็บสกรีนและพิมพ์ลายเสื้อ\n"
        "หน้าที่:\n"
        "1. สกัดข้อความ (OCR) ทั้งหมดในภาพออกมาให้ครบถ้วน แม่นยำ วรรณยุกต์/สระภาษาไทยห้ามตกหล่น จัดบรรทัดให้อ่านง่าย\n"
        "2. วิเคราะห์ฟอนต์ (Font Analysis):\n"
        "   - ลักษณะฟอนต์ (เช่น Sans-serif, Serif, Script, Display, Condensed, Bold)\n"
        "   - ชื่อฟอนต์ภาษาไทยและอังกฤษที่ใกล้เคียงที่สุด (เช่น PSL, DB, JS, FC, Cordia, Bebas, Impact, Montserrat ฯลฯ)\n"
        "   - คำแนะนำสำหรับการนำไปใช้ในงานออกแบบ (Illustrator / Flex / Sublimation)\n\n"
        "รูปแบบการตอบ:\n"
        "--- [ข้อความที่สกัดได้ (TEXT)] ---\n"
        "<ใส่เฉพาะข้อความล้วนๆ ตรงนี้>\n\n"
        "--- [วิเคราะห์ฟอนต์ & สไตล์ (FONT)] ---\n"
        "<วิเคราะห์ฟอนต์ตรงนี้>"
    )

    res = client.messages.create(
        model='claude-haiku-5-5',
        max_tokens=2000,
        thinking={'type': 'disabled'},
        messages=[{
            'role': 'user',
            'content': [
                {'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/png', 'data': b64_data}},
                {'type': 'text', 'text': prompt}
            ]
        }]
    )

    raw_output = ""
    for b in res.content:
        if getattr(b, 'type', '') == 'text':
            raw_output += b.text

    print("\n" + raw_output)

    # Extract text section to copy into clipboard
    text_to_copy = raw_output
    if "--- [ข้อความที่สกัดได้ (TEXT)] ---" in raw_output:
        parts = raw_output.split("--- [ข้อความที่สกัดได้ (TEXT)] ---")[1]
        if "--- [วิเคราะห์ฟอนต์ & สไตล์ (FONT)] ---" in parts:
            text_to_copy = parts.split("--- [วิเคราะห์ฟอนต์ & สไตล์ (FONT)] ---")[0].strip()
        else:
            text_to_copy = parts.strip()

    copy_to_clipboard(text_to_copy)

    print("\n" + "=" * 60)
    print("✅ คัดลอกเฉพาะ 'ข้อความ' ลงคลิปบอร์ดให้เรียบร้อยแล้ว!")
    print("👉 พี่ต้นสามารถกด [Ctrl + V] เพื่อวางข้อความลงใน Illustrator หรือแชทได้ทันทีครับ!")
    print("=" * 60)

    # Windows notification beep
    try:
        import winsound
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except Exception:
        pass

if __name__ == "__main__":
    run_clipboard_ocr()
