# UI v1.1.1 — แก้ไข Sidebar เมนูซ้าย

## สาเหตุ
ไฟล์ `src/app.js` ใช้คลาส `empty` กับสัญลักษณ์สถานะของเมนู ซึ่งตรงกับ `.empty` ใน `src/styles.css` ที่ตั้ง `padding:30px` สำหรับข้อความแสดงผลเมื่อไม่มีข้อมูล ส่งผลให้เมนูสูงผิดปกติและตัดคำขึ้นบรรทัดใหม่

## สิ่งที่แก้
- ใช้ `not-started` แทน `empty` สำหรับสถานะใน Sidebar เพื่อหลีกเลี่ยงการชนกันของคลาส
- บังคับป้ายชื่อเมนูเป็นบรรทัดเดียวใน Desktop และกำหนดขนาดไอคอน/สถานะให้แน่นอน
- คงฟังก์ชันทั้ง 6 แท็บ Progress, Draft, Validation และ JSON Schema v1.0.0 เดิม

## อัปเดต Branch develop ผ่าน GitHub
1. สำรอง JSON Draft ใน localhost ของท่าน
2. เลือก Branch `develop` ใน GitHub (อย่าเลือก `main`)
3. เปลี่ยนไฟล์ `index.html` ที่ Root และ `src/app.js`, `src/styles.css` ตามชุดนี้ (อัปโหลดทับในตำแหน่งเดิมหรือแก้ผ่านเว็บ)
4. Commit โดยใช้ข้อความ `Fix sidebar navigation layout v1.1.1`
5. Download ZIP จาก Branch develop มา Extract แล้วรัน `py -3 -m http.server 8000` ภายในโฟลเดอร์นั้น
6. เปิด `http://localhost:8000/` หรือหาก Server เดิมเปิดอยู่ให้กด Ctrl+C และเริ่ม Server ใหม่ในโฟลเดอร์ไฟล์รุ่นล่าสุด
7. ตรวจ Sidebar ทั้ง 6 รายการ การโหลดตัวอย่าง และ JSON Export อีกครั้ง

หากอัปโหลดไฟล์ผ่าน GitHub Web แล้วเสี่ยงผิดโฟลเดอร์ ให้เลือกแต่ละไฟล์ใน `develop` → Edit (รูปดินสอ) → แทนที่เนื้อหา → Commit changes

ไม่จำเป็นต้อง Merge เข้า `main` จนกว่าจะทดสอบผ่าน
