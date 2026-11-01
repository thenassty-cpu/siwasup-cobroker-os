import sys

update_text = '''

==============================================================================
SESSION UPDATE: 1 พ.ย. 2569 (16:15 น.) - PRICING PRIVILEGE & 5-PILLAR RBAC MATRIX
==============================================================================
1. PROPERTY PRICING & DISCOUNT PRIVILEGE (สิทธิ์แก้ราคาบ้าน & เคาะส่วนลด):
   - เพิ่มสิทธิ์การเงินระดับสูง: '💰 สิทธิ์ปรับแก้ราคาบ้าน & ส่วนลดพิเศษ (Pricing & Discount Authority)'
   - วัตถุประสงค์: สงวนสิทธิ์การเคาะราคาขายตั้งต้น, การทำโปรโมชัน Shock Price, และการปรับเรตคอมมิชชัน ไว้เฉพาะ 'คุณกูล & คุณบัว' และ 'คุณต้น'
   - ป้องกันเจ้าหน้าที่ทั่วไปหรือพี่ลิลลี่เผลอแก้ไขราคาโดยไม่ได้รับอนุญาต

2. 5-PILLAR ACCESS MATRIX (agent_registration.html & executive_quick_hub.html):
   - วางสถาปัตยกรรมสิทธิ์: Standard Admin (ทุกคนมีเป็นฐาน) + Checkboxes สิทธิ์เฉพาะด้าน 6 ช่อง
   - เพิ่มปุ่มลัด 1-Click Preset ในหน้าลงทะเบียนสำหรับ 5 เสาหลัก:
     • คุณกูล & คุณบัว (เทียบเท่ากูล): ผู้บริหารสูงสุด + สิทธิ์แก้ราคาบ้าน + ตรวจลีด + คัดทรัพย์เด่น
     • พี่ลิลลี่: Standard Admin + คุมกุญแจ & อนุมัติ OTP 100% (Lily Cockpit)
     • คุณเจี๊ยบ: Standard Admin + ตรวจลีด/แชท + สำรองกุญแจ OTP + คุม Co-Broker
     • คุณต้น: Standard Admin + Super Tech Admin ทุกระบบ
   - พุชขึ้น GitHub Main และดีพลอยสู่ R2 (Status 200 OK) เรียบร้อย
==============================================================================
'''

with open(r'G:\Home_Brain_Update.txt', 'a', encoding='utf-8') as f:
    f.write(update_text)

print('Successfully appended Pricing & 5-Pillar RBAC to G:\\Home_Brain_Update.txt')
