# scripts/claude_auditor.py
# -*- coding: utf-8 -*-
"""
Siwasup & FBT - Dedicated Claude Auditor (The Cold Inspector)
Role: Ruthless Code & Architecture Auditor
Models: claude-sonnet-5 (default for deep inspection) or claude-haiku-5-5 (fast/cheap)
"""

import os
import sys
import argparse
import anthropic

# Ensure UTF-8 output on Windows terminal
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def audit(prompt: str, context: str = "", model: str = "claude-sonnet-5") -> str:
    """Run an audit query against Claude API."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set in environment!")

    client = anthropic.Anthropic(api_key=api_key)

    system_instruction = (
        "คุณคือ 'ผู้ตรวจการ' (The Cold Inspector) ประจำทีมของพี่ต้น\n"
        "บุคลิก: ยึดหลักการ ตรรกะ ความปลอดภัย และความถูกต้อง 100% ไม่ประจบ ไม่อวย ไม่มีคำเยินยอ\n"
        "หน้าที่: วิเคราะห์โค้ด สถาปัตยกรรม หาจุดบกพร่อง ช่องโหว่ความปลอดภัย และ Edge Cases อย่างตรงไปตรงมา\n"
        "การตอบ: ชัดเจน ตรงประเด็น แยกแยะระหว่างสิ่งที่ยืนยันได้จริงกับสิ่งที่ยังไม่ได้ทดสอบจริง"
    )

    full_user_content = prompt
    if context:
        full_user_content += f"\n\n--- CONTEXT / CODE ---\n{context}"

    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system=system_instruction,
        messages=[{"role": "user", "content": full_user_content}]
    )

    output_texts = []
    for block in response.content:
        if getattr(block, 'type', '') == 'text':
            output_texts.append(block.text)

    return "\n".join(output_texts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Claude Inspector for Siwasup & FBT")
    parser.add_argument("--prompt", "-p", required=True, help="Question or audit instructions")
    parser.add_argument("--file", "-f", help="Path to file to inspect")
    parser.add_argument("--fast", action="store_true", help="Use claude-haiku-5-5 instead of sonnet")
    args = parser.parse_args()

    context_data = ""
    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            context_data = f.read()

    selected_model = "claude-haiku-5-5" if args.fast else "claude-sonnet-5"
    print(f"[*] Running Claude Inspector ({selected_model})...")
    result = audit(args.prompt, context_data, selected_model)
    print("\n" + result)
