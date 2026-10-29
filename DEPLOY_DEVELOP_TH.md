# การอัปเดต GitHub: v2.1.0 — ช่องปฏิทินวันที่บันทึก/ปรับปรุงข้อมูล

Repository: https://github.com/Piyachon-UP/syllabus-generator-web/tree/develop

## ขั้นตอนอัปเดต

1. หากกำลังกรอก Syllabus อยู่ ให้กด **บันทึก JSON** และเก็บไฟล์สำรองก่อน
2. ดาวน์โหลด Patch v2.1.0 แล้วแตกไฟล์
3. เปิด GitHub Repository → เลือก Branch `develop` (อย่าแก้ `main` โดยตรง)
4. อัปโหลดไฟล์ต่อไปนี้ใน **ตำแหน่งเดิม**:
   - `index.html` ที่ Root — หน้า Web App ที่ build แล้ว
   - `src/app.js` — ช่อง Calendar, สถานะการเลือกวันที่และ JSON
   - `src/styles.css` — รูปแบบ Calendar/Responsive
   - `src/docx_export.js` — แสดงวันที่ พ.ศ. ใน DOCX
   - `schema/syllabus.v1.schema.json` — เพิ่ม optional field `LastUpdatedDate`
   - `tools/build.py` — แสดงเวอร์ชัน v2.1.0
   - `tools/test_calendar_v21.py` — Regression Test ใหม่
   - ไฟล์ test เดิมที่เปลี่ยนเวอร์ชัน และเอกสารคู่มือ
5. Commit ด้วยข้อความ `Add course update date calendar and DOCX date v2.1.0`
6. ดาวน์โหลด ZIP ของ `develop` มาทดสอบบนเครื่องด้วย `py -3 -m http.server 8000` จาก Root
7. เปิด `http://localhost:8000/`, กด `Ctrl + Shift + R`
8. ทดสอบ **ข้อมูลรายวิชา → วันที่บันทึก/ปรับปรุงข้อมูล** คลิกไอคอนปฏิทิน เลือกวัน/เดือน/ปี
9. กด **บันทึก JSON** ตรวจดูฟิลด์ `CourseInfo.LastUpdatedDate` มีค่า `YYYY-MM-DD`
10. กด **สร้าง DOCX** ตรวจวันที่ในหน้าแรกเป็นปี พ.ศ.
11. ทดสอบ **เปิด JSON** ไฟล์เก่าที่ไม่มีวันที่: ค่า Calendar ควรเป็นช่องว่าง และข้อมูลอื่นยังอยู่ครบ
12. หากผ่านแล้ว สร้าง PR `develop` → `main` เพื่ออัปเดต GitHub Pages

**ข้อควรระวัง:** Repository นี้เป็น Public ห้ามอัปโหลด JSON รายวิชาจริงหรือข้อมูลผู้สอนที่ไม่ควรเผยแพร่

**สำหรับผู้พัฒนา Blazor:** `LastUpdatedDate` เป็น optional string ประเภท date; ถ้าใช้ Schema/DTO เดิมแบบ strict ต้องอัปเดตให้รู้จักฟิลด์นี้ก่อน import JSON ใหม่ที่มีวันที่
