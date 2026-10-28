# นำ UI v1.3.4 ไปทดสอบใน GitHub Branch `develop`

Repository: https://github.com/Piyachon-UP/syllabus-generator-web/tree/develop

## ก่อนอัปเดต

หากมีข้อมูลที่เคยกรอกบน `localhost:8000` ให้เปิดรุ่นที่ใช้อยู่และกด **เครื่องมือ → สำรอง Draft JSON** เพื่อเก็บเป็นไฟล์ไว้ก่อน

## อัปเดต

1. แตก `Smart_Syllabus_Generator_Web_UI_v1_3_4_Patch.zip`
2. ไปยัง GitHub Repository และเปลี่ยน Branch เป็น **develop** (ไม่ใช่ main)
3. อัปโหลดไฟล์ **ตาม path เดิม**:
   - `index.html` (Root)
   - `src/app.js`
   - `tools/build.py`
   - `README_TH.md` และ `DEPLOY_DEVELOP_TH.md`
   - `tools/test_v134.py` (ถ้าต้องการชุดทดสอบ)
4. Commit message: `Start new form blank and make draft restore explicit v1.3.4`
5. ดาวน์โหลด ZIP ของ Branch develop ใหม่ หรือ Clone/Pull มาในเครื่อง ทดสอบผ่าน Localhost:
   ```powershell
   py -3 -m http.server 8000
   ```
6. กด `Ctrl + Shift + R` เพื่อโหลด HTML ใหม่

> ไม่ต้องเปลี่ยน Settings → Pages และยังไม่ต้อง Merge เข้า main

## รายการทดสอบสำคัญ

1. เปิด `http://localhost:8000/` — ช่อง **ปีการศึกษา** และ **ภาคเรียน** ว่าง
2. ไปแท็บ **ผู้สอน** — แสดง `0 คน` และข้อความ `ยังไม่มีผู้สอน` ไม่มีแถวเก่าค้าง
3. กด **＋ เพิ่มผู้สอน** เลือกชื่อ กด **บันทึก Draft**
4. Refresh หน้าเว็บ — **แสดงหน้ากรอกข้อมูลใหม่ว่าง** (พฤติกรรมตั้งใจของรุ่นนี้)
5. กด **Draft ของฉัน** → **เปิด** Draft ที่เพิ่งบันทึก — รายชื่อเดิมกลับมาและข้อมูลไม่สูญหาย
6. เปิด Draft เก่าที่มีปี พ.ศ. 2569 / ภาคเรียน 1 — คงข้อมูลทั้งสองช่องตามที่เคยกรอก
7. เมื่อกรอกครบ ตรวจสอบและ Export JSON ยังคงตรงตาม Schema 1.0.0

**ข้อควรทราบ:** Localhost และ GitHub Pages แยกพื้นที่เก็บ Draft กัน ต้อง Export/Import JSON เมื่อย้ายไปคนละ URL
