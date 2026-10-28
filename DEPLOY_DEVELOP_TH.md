# อัปเดต UX/UI v1.2.0 บน Branch develop (ไม่กระทบ main)

Repository: `https://github.com/Piyachon-UP/syllabus-generator-web`

1. ที่เว็บ GitHub เลือก Branch `develop` ให้แน่ใจว่าไม่ใช่ `main`.
2. เปิด **Add file → Upload files** และอัปโหลดเนื้อหา *ภายใน ZIP* โดยคงตำแหน่งไฟล์ให้ตรงกับต้นฉบับ:
   - `index.html` ที่ Root
   - `src/app.js` และ `src/styles.css`
   - `data/curriculum_plos.json` และ `data/instructors.json` (โฟลเดอร์ใหม่)
   - `tools/build.py` และ `README_TH.md`
   - `schema/` ยังคงใช้ Schema v1.0.0 เดิม
3. กด Commit ลง Branch `develop` โดยใช้ข้อความ `Simplify syllabus form and load PLO/instructor masters v1.2`.
4. ทดสอบด้วยการคลิก **Code → Download ZIP** ใน Branch `develop` แล้วแตกไฟล์ จากนั้นเปิด PowerShell ณ โฟลเดอร์หลักของ Repository:

   ```powershell
   py -3 -m http.server 8000
   ```

5. เปิด `http://localhost:8000/` และรีเฟรชแบบเต็ม (`Ctrl+Shift+R`). ทดสอบ:
   - ไม่มี Dashboard ทั้งหมด
   - Course Info เหลือ 3 กลุ่ม
   - เลือกหลักสูตรในแท็บ PLOs แล้วเห็น PLO จากไฟล์จริง
   - เลือกผู้สอนในแท็บ Instructors แล้วแสดงรายชื่อเฉพาะสาขาวิชา หรือเลือกทั้งหมด
   - Save Draft / Reload / Import / Export JSON / Validation
6. **ยังไม่ต้อง Merge `develop` เข้า `main`** จนกว่าจะทดสอบครบ จากนั้นเปิด Pull Request จาก `develop` ไป `main` เมื่อพร้อมเผยแพร่จริง

หมายเหตุ: ชื่ออาจารย์ 100 คนและ PLOs 15 หลักสูตรอยู่ใน `data/` และถูกฝังใน `index.html` จึงจะปรากฏใน Repository Public และดาวน์โหลดได้โดยผู้ชมเว็บไซต์ ตรวจสอบนโยบายข้อมูลหน่วยงานก่อนเผยแพร่หรือ Merge.

## การแก้ไขในอนาคต

- แก้ CSS/JS ที่ `src/`
- แก้ Master ที่ `data/`
- สร้าง `index.html` ด้วย `py -3 tools/build.py`
- Commit ไฟล์ Source และ index.html ที่สร้างใหม่พร้อมกัน

ไม่จำเป็นต้องแก้ GitHub Pages Settings เพราะ Pages ยังคง Deploy จาก `main` โดยอัตโนมัติ
