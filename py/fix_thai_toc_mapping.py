#!/usr/bin/env python3
"""
Fix Thai TOC with proper ID mapping
"""

import re

def fix_toc_with_mapping(input_file, output_file):
    # Manual mapping of TOC text to actual chapter IDs
    toc_to_chapter_id = {
        "คำนำ": "คำนำ",
        "RECOVERY DHARMA คืออะไร?": "การฟื้นฟูด้วยธรรมะคืออะไร?",
        "จะเริ่มต้นจากที่ไหน": "เริ่มต้นจากที่ไหน",
        "การปฏิบัติ": "การปฏิบัติ",
        "การตื่นรู้: พระพุทธเจ้า": "การตื่นรู้-พระพุทธเจ้า",
        "เรื่องราวของพระพุทธเจ้าองค์ดั้งเดิม:": "เรื่องราวของพระพุทธเจ้ากำเนิด",
        "เดินตามรอยพระพุทธเจ้า:": "เดินตามรอยพระพุทธเจ้า",
        "ความจริง: ธรรมะ": "ความจริง-ธรรมะ",
        "อริยสัจข้อที่หนึ่ง": "สัจจะข้อแรก",
        "อริยสัจข้อที่สอง": "สัจจะข้อที่สอง",
        "อริยสัจข้อที่สาม": "สัจจะข้อที่สาม",
        "อริยสัจข้อที่สี่": "สัจจะข้อที่สี่",
        "มรรคมีองค์แปด": "มัฌฌิมาปฏิปทา",
        "ความเข้าใจที่ถูกต้อง": "ความเข้าใจที่ชาญฉลาด",
        "ความตั้งใจที่ถูกต้อง": "จิตสำนึกที่ชาญฉลาด",
        "การพูดที่ถูกต้อง": "การพูดที่ชาญฉลาด",
        "การกระทำที่ถูกต้อง": "การกระทำที่ชาญฉลาด",
        "การดำรงชีวิตที่ถูกต้อง": "การประกอบอาชีพที่ชาญฉลาด",
        "ความพยายามที่ถูกต้อง": "ความพยายามที่ชาญฉลาด",
        "สติที่ถูกต้อง": "ความระลึกที่ชาญฉลาด",
        "ความตั้งมั่นที่ถูกต้อง": "ความเข้มข้นที่ชาญฉลาด",
        "ชุมชน: สังฆะ": "สถาบัน-สงฆ์",
        "ความโดดเดี่ยวและการเชื่อมต่อ": "การแยกตัวและการเชื่อมต่อ",
        "การเอื้อมมือออกไป:": "การเอื้อมมือออกไป",
        "เพื่อนและที่ปรึกษาที่ฉลาด": "เพื่อนที่ฉลาดและพี่เลี้ยง",
        "การบริการและความเอื้อเฟื้อ": "การบริการและความเอื้อเฟื้อเผื่อแผ่",
        "การฟื้นตัวเป็นไปได้": "การฟื้นฟูเป็นไปได้",
    }

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace each TOC link with the correct href
    for toc_text, chapter_id in toc_to_chapter_id.items():
        # Find and replace the href
        old_href = f'<a href="#{toc_text}" class="TOCentry">{toc_text}</a>'
        new_href = f'<a href="#{chapter_id}" class="TOCentry">{toc_text}</a>'
        content = content.replace(old_href, new_href)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Fixed TOC links with proper chapter ID mapping")
    print(f"✓ Mapped {len(toc_to_chapter_id)} TOC entries to chapter IDs")

if __name__ == '__main__':
    input_file = '/mnt/c/Users/scott/Documents/RecoveryDharma/RDGBook/output_V1/docs/rdgThai2.html'
    output_file = input_file

    fix_toc_with_mapping(input_file, output_file)
