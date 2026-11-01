import re

FILE_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update follow handling
old_follow = """                if ev_type == 'follow':
                    def process_follow(uid):
                        prof = get_line_profile(uid)
                        append_chat_log({
                            "id": f"LOG_{int(time.time()*1000)}",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "user_name": prof.get("displayName"),
                            "user_pic": prof.get("pictureUrl"),
                            "user_id_tail": uid[-6:] if uid else "anon",
                            "event_type": "follow",
                            "user_text": "[แอดเพื่อนเข้าสู่ระบบ LINE OA]",
                            "ai_reply": "(ระบบส่งข้อความต้อนรับอัตโนมัติ)",
                            "matched_codes": [],
                            "search_mode": "FOLLOW_EVENT",
                            "latency_ms": 0
                        })
                    threading.Thread(target=process_follow, args=(user_id,), daemon=True).start()"""

new_follow = """                if ev_type == 'follow':
                    reply_token = event.get('replyToken')
                    def process_follow(uid, rtoken):
                        prof = get_line_profile(uid)
                        user_name = prof.get("displayName", "ท่าน")
                        welcome_msg = (
                            f"สวัสดีครับคุณ {user_name}! ยินดีต้อนรับสู่ Siwasup Co-Broker OS ครับ 🏠✨\\n\\n"
                            "น้องศิวาเป็น AI ผู้ช่วยค้นหาทรัพย์และประสานงานนำชมบ้าน พร้อมทำงาน 24 ชั่วโมงครับ\\n\\n"
                            "📋 สำหรับทีมงานออฟฟิศและตัวแทนพันธมิตร เพื่อเริ่มต้นใช้งานและรับ 'นามบัตรดิจิทัลทางการ' "
                            "กรุณาลงทะเบียนเข้าสู่ระบบที่นี่ได้เลยครับ:\\n"
                            "👉 https://assets.siwasup.com/agent_registration.html\\n\\n"
                            "💡 หรือพิมพ์ค้นหาบ้านได้ทันที เช่น:\\n"
                            "• 'บ้านเดี่ยว นนทบุรี งบ 4 ล้าน'\\n"
                            "• 'ค้นหาทรัพย์ 1090965'\\n"
                            "• พิมพ์ 'นามบัตร' หรือ 'ลงทะเบียน' เพื่อเปิดดูหรือสร้างนามบัตรของคุณได้ตลอดเวลาครับ"
                        )
                        if rtoken:
                            reply_line(rtoken, welcome_msg)
                        append_chat_log({
                            "id": f"LOG_{int(time.time()*1000)}",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "user_name": prof.get("displayName"),
                            "user_pic": prof.get("pictureUrl"),
                            "user_id_tail": uid[-6:] if uid else "anon",
                            "event_type": "follow",
                            "user_text": "[แอดเพื่อนเข้าสู่ระบบ LINE OA]",
                            "ai_reply": welcome_msg,
                            "matched_codes": [],
                            "search_mode": "FOLLOW_EVENT",
                            "latency_ms": 0
                        })
                    threading.Thread(target=process_follow, args=(user_id, reply_token), daemon=True).start()"""

# 2. Update message handling for registration/login
old_msg = """                            if mtype == 'text':
                                ai_reply, matched_codes, search_mode = ask_gemini(uid, text, is_continuous=continuous)
                            else:"""

new_msg = """                            if mtype == 'text':
                                text_clean = text.strip().lower()
                                if any(k in text_clean for k in ['สมัคร', 'ลงทะเบียน', 'login', 'เข้าสู่ระบบ', 'ขอนามบัตร', 'นามบัตร', 'โปรไฟล์', 'profile']):
                                    ai_reply = (
                                        f"สวัสดีครับคุณ {prof.get('displayName', '')}! สำหรับการลงทะเบียนทีมงานออฟฟิศ หรือรับนามบัตรดิจิทัลทางการของ Siwasup Co-Broker OS:\\n\\n"
                                        "👉 คลิกที่นี่เพื่อลงทะเบียน/เข้าสู่ระบบได้ทันทีครับ:\\n"
                                        "https://assets.siwasup.com/agent_registration.html\\n\\n"
                                        "เมื่อลงทะเบียนเสร็จ ท่านจะได้นามบัตรเฉพาะตัวพร้อมลิงก์และ QR Code ส่งต่อให้ลูกค้าดูได้ทันทีครับ ✨"
                                    )
                                    matched_codes, search_mode = [], "ONBOARDING_REGISTRATION"
                                else:
                                    ai_reply, matched_codes, search_mode = ask_gemini(uid, text, is_continuous=continuous)
                            else:"""

# Normalize line endings
old_follow_crlf = old_follow.replace('\n', '\r\n')
new_follow_crlf = new_follow.replace('\n', '\r\n')
old_msg_crlf = old_msg.replace('\n', '\r\n')
new_msg_crlf = new_msg.replace('\n', '\r\n')

patched_count = 0
if old_follow_crlf in code:
    code = code.replace(old_follow_crlf, new_follow_crlf, 1)
    patched_count += 1
elif old_follow in code:
    code = code.replace(old_follow, new_follow, 1)
    patched_count += 1

if old_msg_crlf in code:
    code = code.replace(old_msg_crlf, new_msg_crlf, 1)
    patched_count += 1
elif old_msg in code:
    code = code.replace(old_msg, new_msg, 1)
    patched_count += 1

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print(f"[OK] Patched line_gemini_webhook.py (Patches applied: {patched_count}/2)")
