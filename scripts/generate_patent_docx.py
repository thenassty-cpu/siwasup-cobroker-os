# scripts/generate_patent_docx.py
# -*- coding: utf-8 -*-
"""
Generate official Petty Patent Application Document (.docx) for DIP submission
Applicant: นายณัฐ ระวังภัย
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_font(run, font_name="TH Sarabun New", size_pt=16, bold=False, italic=False, color_rgb=(0, 0, 0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    
    # Set complex script font for Thai in Word XML
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rPr.append(rFonts)

def create_patent_docx(output_path):
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Title Document Header
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_top = p_top.add_run("คำขอรับอนุสิทธิบัตร (ร่างบทพรรณนาการประดิษฐ์)")
    set_font(r_top, "TH Sarabun New", 20, bold=True)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("กรมทรัพย์สินทางปัญญา กระทรวงพาณิชย์ ประเทศไทย\n")
    set_font(r_sub, "TH Sarabun New", 16, bold=True, color_rgb=(80, 80, 80))

    # Meta Table
    table = doc.add_table(rows=3, cols=2)
    table.style = 'Light Shading Accent 1'
    
    meta_data = [
        ("ผู้ประดิษฐ์ (Inventor):", "นายณัฐ ระวังภัย (Ton / NASSTY)"),
        ("ผู้ขอรับอนุสิทธิบัตร (Applicant):", "นายณัฐ ระวังภัย (บุคคลธรรมดา - สิทธิ์เดี่ยว)"),
        ("สถานะการอนุญาตสิทธิ์ (Licensing):", "Exclusive License ให้แก่ บริษัท ศิวาทรัพย์ จำกัด (เฉพาะธุรกิจอสังหาริมทรัพย์)")
    ]

    for i, (k, v) in enumerate(meta_data):
        row = table.rows[i]
        p0 = row.cells[0].paragraphs[0]
        r0 = p0.add_run(k)
        set_font(r0, "TH Sarabun New", 14, bold=True)
        
        p1 = row.cells[1].paragraphs[0]
        r1 = p1.add_run(v)
        set_font(r1, "TH Sarabun New", 14, bold=False)

    doc.add_paragraph() # spacing

    sections_content = [
        ("1. ชื่อที่แสดงถึงการประดิษฐ์ (Title of the Invention)", 
         "ภาษาไทย: ระบบและกรรมวิธีการประมวลผลจับคู่อสังหาริมทรัพย์และจัดสรรสิทธิ์ตัวแทนแบบกระจายศูนย์ผ่านเครือข่ายสื่อสารดิจิทัล\n"
         "ภาษาอังกฤษ: SYSTEM AND METHOD FOR DECENTRALIZED REAL ESTATE MATCHING AND DYNAMIC AGENT ATTRIBUTION VIA DIGITAL COMMUNICATION NETWORK"),

        ("2. สาขาวิทยาการที่เกี่ยวข้องกับการประดิษฐ์ (Field of the Invention)",
         "วิศวกรรมคอมพิวเตอร์และเทคโนโลยีสารสนเทศ (Computer Engineering and Information Technology) ในส่วนที่เกี่ยวข้องกับระบบสถาปัตยกรรมเว็บแอปพลิเคชันแบบก้าวหน้า (Progressive Web Application), ระบบบริหารความสัมพันธ์ลูกค้าและตัวแทนจำหน่าย (CRM & Co-Broker Allocation), และระบบสังเคราะห์ข้อมูลข้ามแพลตฟอร์มแบบอัตโนมัติ (Omni-Channel Content Transformation Engine)"),

        ("3. ภูมิหลังของศิลปะหรือวิทยาการที่เกี่ยวข้อง (Background / Prior Art)",
         "ในระบบแพลตฟอร์มการซื้อขายและนายหน้าอสังหาริมทรัพย์ในปัจจุบัน (Conventional PropTech & Brokerage Systems) ประสบปัญหาทางเทคนิคและอุปสรรคในการปฏิบัติการหลายประการ ได้แก่:\n\n"
         "1. ปัญหาการสูญเสียสิทธิ์ของตัวแทน (Agent Attribution Leakage): ระบบเดิมเมื่อตัวแทนส่งลิงก์ทรัพย์ให้ผู้ซื้อ ลิงก์มักเป็นลิงก์ส่วนกลางของแพลตฟอร์ม ทำให้เมื่อผู้ซื้อกดเข้าชม ข้อมูลการติดต่อมักจะหลุดไปยังเจ้าของแพลตฟอร์ม หรือตัวแทนรายอื่น ส่งผลให้เกิดความขัดแย้งและขาดแรงจูงใจในการกระจายสินค้า\n"
         "2. ปัญหาความหน่วงและภาระการประมวลผลจากการโหลดแคตตาล็อกขนาดใหญ่ (Catalog Overload & Cognitive Friction): เมื่อผู้ซื้อเปิดดูทรัพย์ที่สนใจเฉพาะเจาะจง 1 แปลง ระบบเดิมมักจะบังคับโหลดฐานข้อมูลทรัพย์ทั้งหมดขึ้นมาแสดงผล ทำให้เกิดความหน่วงต่ออุปกรณ์พกพา และทำให้ผู้ซื้อเกิดความสับสน หลงทางจากทรัพย์เป้าหมายที่แท้จริง\n"
         "3. ความยุ่งยากในการแปลงข้อมูลเพื่อกระจายสู่ช่องทางโซเชียลมีเดีย (Cross-Platform Distribution Inefficiency): ตัวแทนต้องเสียเวลาคัดลอกรูปภาพและพิมพ์ข้อความ ดัดแปลงฟอร์แมตให้เข้ากับแต่ละแพลตฟอร์ม (LINE, Facebook Marketplace, TikTok, Instagram) ด้วยตนเอง ซึ่งใช้เวลานาน ข้อมูลผิดเพี้ยน และขาดการควบคุมมาตรฐานคำนวณสินเชื่อ\n"
         "4. การพึ่งพาเซิร์ฟเวอร์ส่วนกลางที่มีต้นทุนสูงตลอด 24 ชั่วโมง (Heavy Centralized Infrastructure): แพลตฟอร์มทั่วไปต้องเปิดเซิร์ฟเวอร์ประมวลผลตลอดเวลา ก่อให้เกิดค่าใช้จ่ายสูงและเสี่ยงต่อการถูกปฏิเสธการให้บริการ (DDoS)\n\n"
         "การประดิษฐ์นี้จึงถูกคิดค้นขึ้นเพื่อแก้ไขปัญหาดังกล่าวอย่างเป็นรูปธรรม"),

        ("4. ลักษณะและความมุ่งหมายของการประดิษฐ์ (Summary of the Invention)",
         "การประดิษฐ์นี้มุ่งหมายที่จะจัดให้มี ระบบและกรรมวิธีการประมวลผลจับคู่อสังหาริมทรัพย์และจัดสรรสิทธิ์ตัวแทนแบบกระจายศูนย์ ซึ่งมีองค์ประกอบนวัตกรรม 4 ประการหลัก:\n\n"
         "1. กลไกการจัดสรรสิทธิ์ตัวแทนแบบไดนามิกและทนทาน (Dynamic Agent Attribution & Resilient Tokenization): ระบบสามารถตรวจจับ รหัสตัวแทน (Agent Ref) และฝังรหัสดังกล่าวลงในโครงสร้าง URL, Dynamic QR Code, และกิจกรรมการแชร์ทุกรูปแบบอย่างอัตโนมัติ โดยมีระบบความจำภายในเครื่อง (Local Persistent State) คอยล็อกสิทธิ์ตัวแทนเดิมไว้ แม้ผู้ซื้อจะปิดหน้าต่างและกลับเข้ามาใหม่\n"
         "2. สถาปัตยกรรมการแสดงผลแบบแยกบริบททรัพย์เดี่ยว (Context-Isolated Single Property Architecture): ระบบสามารถดักจับพารามิเตอร์รหัสทรัพย์ เพื่อทำการสกัดและล็อกฉากหลังของเว็บแอปพลิเคชันให้แสดงผลเฉพาะการ์ดทรัพย์เป้าหมายเพียงแปลงเดียวอย่างสมบูรณ์แบบ ลดภาระการเรนเดอร์หน่วยความจำ และมีกลไกปลดล็อกกลับสู่โหมดแคตตาล็อกรวม (Mega-Pool) ได้อย่างไร้รอยต่อ\n"
         "3. ระบบสังเคราะห์ชุดข้อมูลการขายข้ามช่องทางอัตโนมัติ (Omni-Channel Share Payload Synthesizer): อัลกอริทึมที่แปลงข้อมูลอสังหาริมทรัพย์เดี่ยว ออกมาเป็น 4 รูปแบบข้อมูลที่ปรับแต่งเฉพาะทาง ได้แก่ การ์ดบรอดแคสต์สำหรับ LINE, โพสต์ขายเต็มรูปแบบสำหรับ Facebook Marketplace พร้อมตารางสินเชื่อ, แคปชั่นสั้นสำหรับ Bio TikTok, และการแชร์ผ่าน Native Web Share API\n"
         "4. สถาปัตยกรรมประมวลผลแบบไฮบริดไร้เซิร์ฟเวอร์หลัก (Ephemeral Webhook with Pre-Sleep State Flushing): ระบบประมวลผลฝั่งเซิร์ฟเวอร์แบบตื่นเมื่อมีงานและหลับเมื่อว่าง (On-Demand Compute) โดยมีตัวดักจับสัญญาณยุติการทำงาน (SIGTERM) เพื่อทำการฟลัชเซฟข้อมูลธุรกรรมและบันทึกการสนทนาขึ้นสู่หน่วยจัดเก็บแบบกระจายศูนย์ (Object Storage) ก่อนระบบเข้าสู่สภาวะพักตัว"),

        ("5. คำอธิบายการประดิษฐ์โดยสมบูรณ์ (Detailed Description)",
         "สถาปัตยกรรมของระบบประกอบด้วย 4 ส่วนการทำงานหลักที่ประสานกันแบบบูรณาการ:\n\n"
         "ก. ชั้นการแสดงผลและส่วนติดต่อผู้ใช้ (Frontend Progressive Web App): จัดการส่วนต่อประสานผู้ใช้ ทำงานผ่านเทคโนโลยีเว็บแบบไร้เซิร์ฟเวอร์ มีโมดูลล็อกสิทธิ์ตัวแทน โมดูลแยกทรัพย์เดี่ยว และตัวจำลองการคัดลอกข้อความคู่ขนาน (Dual-Mode Clipboard Fallback)\n\n"
         "ข. ชั้นจัดเก็บข้อมูลไร้เซิร์ฟเวอร์หลัก (Cloud Object Storage): จัดเก็บฐานข้อมูลดัชนีทรัพย์กว่า 1,849 แปลงในรูปแบบโครงสร้าง JSON น้ำหนักเบา และคลังภาพถ่ายจริงความละเอียดสูง\n\n"
         "ค. ชั้นประมวลผลชาญฉลาดแบบชั่วคราว (Ephemeral Webhook Engine): ระบบรับคำร้องและประมวลผลข้อความภาษาธรรมชาติ มีโมดูลวิเคราะห์พิกัดเขต 50 เขตกรุงเทพฯ แบบไดนามิก พร้อมระบบดักจับการตัดการทำงานของเซิร์ฟเวอร์\n\n"
         "ง. ระบบสังเคราะห์สารสนเทศการขาย: ตรวจสอบเบราว์เซอร์ภายในแอป (In-App Webview) หากตรวจพบ จะสลับคำสั่งจากการเปิดหน้าต่างใหม่ (window.open) มาเป็นการนำทางตรง (window.location.href) เพื่อหลบเลี่ยงระบบบล็อกหน้าต่างป็อปอัป ทำให้ตัวแทนสามารถส่งงานต่อได้อย่างราบรื่น 100%"),

        ("6. ข้อถือสิทธิ (Patent Claims)",
         "ข้อ 1. ระบบประมวลผลจับคู่อสังหาริมทรัพย์และจัดสรรสิทธิ์ตัวแทนแบบกระจายศูนย์ผ่านเครือข่ายสื่อสารดิจิทัล ซึ่งประกอบด้วย:\n"
         "- ส่วนประมวลผลฝั่งไคลเอนต์ ที่ทำงานผ่านสถาปัตยกรรมเว็บแอปพลิเคชันแบบก้าวหน้า\n"
         "- โมดูลจัดสรรสิทธิ์ตัวแทนแบบไดนามิก ที่ทำหน้าที่ตรวจสอบ บันทึก และผสานรหัสตัวแทนเข้ากับชุดข้อมูลการสืบค้น\n"
         "- โมดูลแยกบริบททรัพย์เดี่ยว ซึ่งทำหน้าที่จำกัดขอบเขตการแสดงผลของฐานข้อมูลให้แสดงเฉพาะทรัพย์ที่ถูกระบุในพารามิเตอร์การเรียกดู พร้อมแสดงส่วนควบคุมการปลดล็อกกลับสู่รายการรวม\n"
         "- โมดูลสังเคราะห์สารสนเทศการขายหลายช่องทาง ซึ่งทำหน้าที่แปลงระเบียนข้อมูลอสังหาริมทรัพย์แปลงเดียวให้เป็นชุดข้อมูลที่สอดคล้องกับข้อกำหนดของแต่ละแพลตฟอร์มโซเชียลมีเดียโดยอัตโนมัติ\n\n"
         "ข้อ 2. ระบบตามข้อถือสิทธิ 1 ที่ซึ่ง โมดูลจัดสรรสิทธิ์ตัวแทนแบบไดนามิก มีลักษณะพิเศษคือ มีกลไกการบันทึกรหัสตัวแทนลงในหน่วยความจำถาวรภายในเครื่องของผู้ใช้ และทำการสร้างรหัสตอบสนองแบบรวดเร็ว (Dynamic QR Code) ที่ผูกติดรหัสตัวแทนนั้นแบบเรียลไทม์โดยไม่ต้องพึ่งพาการประมวลผลจากเซิร์ฟเวอร์ส่วนกลาง\n\n"
         "ข้อ 3. ระบบตามข้อถือสิทธิ 1 ที่ซึ่ง โมดูลสังเคราะห์สารสนเทศการขายหลายช่องทาง ประกอบด้วยกลไกการตรวจสอบสภาพแวดล้อมการทำงานของเบราว์เซอร์ โดยหากตรวจพบว่าทำงานอยู่บนเบราว์เซอร์ภายในแอปพลิเคชัน (In-App Webview) ระบบจะเปลี่ยนคำสั่งเปิดหน้าต่างใหม่เป็นการนำทางโดยตรงผ่าน Uniform Resource Identifier (URI Scheme) เพื่อป้องกันการถูกปิดกั้นจากระบบป้องกันหน้าต่างป็อปอัป\n\n"
         "ข้อ 4. ระบบตามข้อถือสิทธิ 1 ถึง 3 ข้อใดข้อหนึ่ง ที่ซึ่ง มีระบบสำรองการคัดลอกข้อความแบบคู่ขนาน (Dual-Mode Clipboard Fallback) ที่ตรวจสอบความพร้อมใช้งานของ navigator.clipboard และหากตรวจพบข้อจำกัดด้านความปลอดภัยหรือข้อจำกัดของระบบปฏิบัติการ จะสั่งการให้สร้างส่วนประกอบข้อความจำลองในเอกสารเพื่อทำการคัดลอกผ่านคำสั่งระดับระบบโดยไม่แสดงข้อผิดพลาดต่อผู้ใช้\n\n"
         "ข้อ 5. ระบบตามข้อถือสิทธิ 1 ที่ซึ่ง เชื่อมโยงการทำงานร่วมกับเซิร์ฟเวอร์ประมวลผลคำร้องแบบชั่วคราว ที่มีโมดูลวิเคราะห์พิกัดเขตแบบไดนามิก สำหรับจำแนกคำค้นหาโซนพื้นที่จากภาษาธรรมชาติ และมีระบบดักจับสัญญาณการพักตัว (SIGTERM) เพื่อทำการฟลัชบันทึกธุรกรรมขึ้นสู่ระบบจัดเก็บแบบกระจายศูนย์ก่อนเซิร์ฟเวอร์เข้าสู่สภาวะตัดการทำงาน"),

        ("7. บทสรุปการประดิษฐ์ (Abstract)",
         "การประดิษฐ์นี้เปิดเผยระบบและกรรมวิธีการประมวลผลจับคู่อสังหาริมทรัพย์และจัดสรรสิทธิ์ตัวแทนแบบกระจายศูนย์ผ่านเครือข่ายสื่อสารดิจิทัล โดยมีโครงสร้างการทำงานแบบเว็บแอปพลิเคชันก้าวหน้าที่ทำงานร่วมกับที่จัดเก็บข้อมูลแบบกระจายศูนย์ ระบบประกอบด้วยโมดูลจัดสรรสิทธิ์ตัวแทนแบบไดนามิกที่ป้องกันการสูญเสียสิทธิ์ของตัวแทนผ่านรหัสเฉพาะตัว, โมดูลแยกบริบททรัพย์เดี่ยวที่ล็อกการแสดงผลเฉพาะแปลงที่สนใจเพื่อลดภาระการประมวลผลบนอุปกรณ์พกพา, โมดูลสังเคราะห์สารสนเทศการขายที่สามารถแปลงข้อมูลทรัพย์หนึ่งแปลงออกเป็นรูปแบบที่เหมาะสมกับแต่ละช่องทางโซเชียลมีเดียได้ทันทีในคลิกเดียว พร้อมระบบคัดลอกและนำทางที่รองรับเบราว์เซอร์ภายในแอปพลิเคชันอย่างทนทาน ช่วยยกระดับประสิทธิภาพการซื้อขายอสังหาริมทรัพย์แบบนายหน้าร่วมได้อย่างแม่นยำ ปลอดภัย และมีต้นทุนการดูแลรักษาระบบต่ำ")
    ]

    for title, text in sections_content:
        h = doc.add_paragraph()
        r_h = h.add_run(title)
        set_font(r_h, "TH Sarabun New", 16, bold=True, color_rgb=(0, 51, 102)) # Navy blue title
        
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(8)
        r_p = p.add_run(text)
        set_font(r_p, "TH Sarabun New", 15, bold=False)

    # Footer note
    doc.add_paragraph()
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_foot = p_foot.add_run("เอกสารจัดเตรียมโดย: นายณัฐ ระวังภัย (ผู้ประดิษฐ์)\nวันที่จัดทำ: 4 พฤศจิกายน 2569")
    set_font(r_foot, "TH Sarabun New", 13, italic=True, color_rgb=(100, 100, 100))

    doc.save(output_path)
    print(f"[OK] Generated Word Document successfully at: {output_path}")

if __name__ == "__main__":
    desktop_path = r"C:\Users\ITss-Advice\Desktop\ร่างคำขออนุสิทธิบัตร_Siwasup_OS_ณัฐ_ระวังภัย.docx"
    create_patent_docx(desktop_path)
    
    # Also save to repo docs folder
    repo_docs = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\docs"
    os.makedirs(repo_docs, exist_ok=True)
    repo_path = os.path.join(repo_docs, "ร่างคำขออนุสิทธิบัตร_Siwasup_OS_ณัฐ_ระวังภัย.docx")
    create_patent_docx(repo_path)
