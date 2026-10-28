# อัปเดต UX/UI v1.3.3 ไปยัง GitHub `develop`

Repository: https://github.com/Piyachon-UP/syllabus-generator-web/tree/develop

## วิธีอัปเดต

1. สำรอง Draft สำคัญจาก Web App เป็น JSON ก่อนแก้ไข
2. ดาวน์โหลดและแตก `Smart_Syllabus_Generator_Web_UI_v1_3_3_Patch.zip`
3. ไปที่ Branch **develop** บน GitHub (อย่าเลือก main)
4. อัปเดตไฟล์ตาม path เดิม:
   - `index.html` ที่ Repository Root (สำคัญสำหรับเว็บ)
   - `src/app.js` (ให้ตรงกับ index.html)
   - `tools/build.py` (แสดงเวอร์ชัน 1.3.3)
   - `README_TH.md` และ `DEPLOY_DEVELOP_TH.md` (คู่มือ)
5. Commit ด้วยข้อความ `Fix persisted term values and instructor rows; add custom resource type v1.3.3`
6. ดาวน์โหลด ZIP ของ Branch `develop` เพื่อทดสอบในเครื่อง ผ่าน `py -3 -m http.server 8000`
7. กด `Ctrl + Shift + R` ใน Browser หลังอัปเดต

`main` ยัง Deploy ผ่าน GitHub Pages รุ่นปัจจุบัน ไม่ต้อง Merge จนกว่าจะทดสอบเรียบร้อย

## ผลที่ต้องตรวจ

- สร้าง Draft ใหม่ → ปีการศึกษาและภาคเรียนเป็นช่องว่าง
- เปิด Draft เก่าที่เคยมีปี `1` / ภาคเรียน `0` → ช่องสองช่องนี้ว่าง แต่ข้อมูลอื่นอยู่ครบ
- เปิด Draft ที่ปี `2569` / ภาคเรียน `1` → ยังคงค่าเดิม
- เมนูผู้สอน → ไม่แสดงแถวว่างเอง แต่กด “＋ เพิ่มผู้สอน” แล้วเริ่มกรอกได้
- Draft เก่าที่มีแถวผู้สอนเปล่าและแถวที่กรอกแล้ว → แสดงเฉพาะแถวที่กรอกแล้ว
- การประเมิน → หนังสือและแหล่งเรียนรู้ → ประเภทแหล่งเรียนรู้ → `กำหนดเอง` → กรอกข้อความอื่นได้
- Save Draft, Refresh, Validate, Export JSON

> ปี `1` และภาคเรียน `0` ใน Draft เก่ามีความเป็นไปได้ว่าเกิดจากค่าที่เคยบันทึกไว้ การปรับรุ่นนี้ทำความสะอาดเฉพาะค่าที่ไม่ถูกต้องดังกล่าว ไม่ล้างค่าปี/ภาคเรียนที่ผู้ใช้กรอกถูกต้อง
