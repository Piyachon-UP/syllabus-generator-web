# Deploy UX/UI v1.3.0 เข้า GitHub Branch `develop`

**Repository:** `https://github.com/Piyachon-UP/syllabus-generator-web/tree/develop`

**ก่อนเริ่ม:** บน `localhost:8000` หรือ URL ใด ๆ ที่มี Draft จริง ให้กด **เครื่องมือ → สำรอง Draft JSON** ก่อน

## วิธีง่ายที่สุด: ทดสอบหน้าเว็บก่อน

1. แตก ZIP รุ่น v1.3.0
2. เปิด `index.html` โดยตรงเพื่อดูหน้าจอ หรือเปิด PowerShell ในโฟลเดอร์ ZIP แล้วรัน `py -3 -m http.server 8000`
3. ไป `http://localhost:8000/` และทดสอบการกรอกข้อมูล, Dropdown, การเลือก PLO, Save Draft, Refresh, Validate, Export JSON

## อัปโหลดไป GitHub

1. ไปหน้า Repository และเลือก Branch **develop** ให้แน่ใจ (ไม่ใช่ main)
2. อัปโหลด `index.html` (ที่ Root ของ Repository) โดยใช้ไฟล์จาก ZIP นี้
3. อัปเดต `src/app.js`, `src/styles.css`, `tools/build.py`, `README_TH.md` และเอกสารนี้ในตำแหน่งเดิม เพื่อเก็บ Source ให้ตรงกับเว็บ
4. ไม่ต้องเปลี่ยน `schema/syllabus.v1.schema.json`, `data/` และ `sample/Smart_Syllabus_Demo.json` หากไม่มีการแก้ไข Master; มีไฟล์เหล่านี้ใน ZIP เพื่อให้พัฒนาแบบออฟไลน์ได้ครบ
5. Commit message แนะนำ: `Simplify authoring forms and add editable Thai dropdowns v1.3`
6. อย่าเพิ่ง Merge `develop` เข้า `main` จนกว่าจะทดสอบครบ

> **การทดสอบ v1.3 ผ่าน GitHub Pages ในปัจจุบัน:** Pages ของคุณเผยแพร่ Branch `main` อยู่ จึงยังเป็นเวอร์ชันเก่า แม้จะอัปโหลด `develop` แล้ว การทดลอง `develop` ให้ดาวน์โหลด ZIP จาก Branch นั้น หรือใช้ Local Web Server ตามขั้นตอนแรก

## Checklist ก่อน Merge

- ข้อมูลรายวิชาไม่มี * และทุกช่องเป็นข้อความ; Credits เป็น `3`
- ไม่มี Lecture% และ Lab% ในหน้าผู้สอน; เพิ่มผู้สอนที่ไม่มีใน Master ได้
- เลือก PLO ใน CLOs ได้หลายรหัส
- วิธีสอน Lecture/Lab เป็นภาษาไทยแยกชุด และพิมพ์รายการอื่นได้
- ผู้สอนใน Weekly Plan เลือกหรือพิมพ์ได้
- ประเภทประเมิน/แหล่งเรียนรู้เป็นภาษาไทยและพิมพ์เองได้
- ระบบเกรด A–F หรือ S/U ทำงาน
- ลอง Refresh หน้าเว็บ / เปิด Draft / Export / Import JSON โดยไม่มีข้อมูลสูญหาย
- ตรวจสอบผล Validate และ JSON Schema
