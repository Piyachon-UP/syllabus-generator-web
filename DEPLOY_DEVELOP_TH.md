# ขั้นตอนอัปเดต UI v1.4.2 ลง Branch develop

1. สำรอง JSON ของรายวิชาที่กำลังแก้ไขและตรวจว่าดาวน์โหลดสำเร็จ
2. เปิด GitHub Repository `Piyachon-UP/syllabus-generator-web` และเลือก Branch `develop`
3. อัปโหลดไฟล์ Patch โดยรักษาตำแหน่งโฟลเดอร์ไว้:
   - `index.html` ที่ Root
   - `src/app.js`
   - `src/styles.css`
   - `tools/build.py`
   - `README_TH.md` และ `DEPLOY_DEVELOP_TH.md`
4. Commit: `Simplify JSON save UI with persistent footer v1.4.2`
5. ดาวน์โหลด Code → Download ZIP จาก Branch `develop`, แตกไฟล์ แล้วเปิด PowerShell ในโฟลเดอร์นั้น
6. รัน `py -3 -m http.server 8000` แล้วเปิด `http://localhost:8000/`
7. ตรวจว่าแถบบนมีเฉพาะ “เปิด JSON”, ไม่มี “สร้างใหม่” และ “ตรวจสอบข้อมูล”
8. สลับครบ 6 หมวด ดูว่า Sticky Footer มี “บันทึก JSON” อยู่ตลอด ทดลองกรอกไม่ครบแล้วบันทึก JSON
9. ใช้ “เปิด JSON” โหลดไฟล์นั้นกลับมา และทดสอบ Dropdown ประเภทประเมินว่ามี “ปฏิบัติการ” กับ “กำหนดเอง”
10. **ยังไม่ Merge เข้า main** จนกว่าจะตรวจสอบเสร็จ

Schema v1.0.0 เดิมไม่มีการเปลี่ยนแปลง การบันทึกแม้ไม่ผ่านเงื่อนไขการตรวจสอบไม่ถือว่าข้อมูลพร้อมเข้าระบบ Blazor โดยอัตโนมัติ
