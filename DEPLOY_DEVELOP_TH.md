# อัปเดต UX/UI v1.4.1 บน Branch develop

## สิ่งที่แก้
แก้ dropdown หลังเปิด JSON: วิธีสอน Lecture/Lab, ประเภทประเมิน และประเภทแหล่งเรียนรู้ ให้เห็นตัวเลือกครบเสมอ และรองรับ “กำหนดเอง” โดยไม่เปลี่ยน JSON Schema เดิม

## อัปโหลดไฟล์

1. สำรองไฟล์ JSON ที่กำลังทำอยู่บนเครื่องก่อน (การอัปเดต source ไม่แก้ไขไฟล์ JSON ที่ดาวน์โหลดไว้)
2. ไปที่ GitHub Repository และเลือก Branch `develop` (อย่าอัปเดต `main` ระหว่างทดลอง)
3. แตกไฟล์ ZIP Patch แล้วอัปโหลด **โดยรักษาตำแหน่ง** ให้ตรงเดิม:
   - `index.html` → root
   - `src/app.js` → src
   - `src/styles.css` → src
   - `tools/build.py` → tools
   - `README_TH.md` / `DEPLOY_DEVELOP_TH.md` → root
4. Commit: `Fix complete dropdown choices after JSON import v1.4.1`
5. Download ZIP ของ Branch `develop` เปิด PowerShell ในโฟลเดอร์หลัก แล้วรัน `py -3 -m http.server 8000`
6. เปิด `http://localhost:8000/` และกด `Ctrl+Shift+R` แล้วตรวจเวอร์ชัน v1.4.1 ทางซ้ายบน
7. กด **เปิด JSON** เลือกไฟล์รายวิชาที่เคยบันทึกไว้ เช่น `SYLLABUS_244106_2569_2_2.json`
8. ไปที่ **แผนการสอน** เลือกทั้ง Lecture และ Lab แล้วคลิก Dropdown วิธีสอน: ต้องเห็นรายการทั้งหมด แม้มีค่าที่กรอกไว้แล้ว
9. ไปที่ **การประเมิน** ทดสอบ Dropdown ประเภทประเมินและประเภทแหล่งเรียนรู้
10. เลือก `กำหนดเอง` พิมพ์คำใหม่ กด `บันทึก JSON`, เปิด JSON ใหม่นั้นแล้วตรวจว่าค่ายังครบ

หมายเหตุ: **ยังไม่ต้อง Merge เข้า main** จนกว่าจะทดสอบสำเร็จ
