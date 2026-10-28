# ขั้นตอนอัปเดต Branch develop — v1.3.1

1. สำรอง Draft สำคัญเป็น JSON จากหน้าเว็บก่อนเสมอ
2. แตกไฟล์ ZIP **แล้วเข้าไปในโฟลเดอร์ `syllabus_web_v1_3_1`**
3. ที่ [GitHub develop](https://github.com/Piyachon-UP/syllabus-generator-web/tree/develop) ตรวจสอบว่าเลือก **develop** อยู่ ไม่ใช่ main
4. อัปโหลด / แทนที่ตามตำแหน่งเดิมดังนี้:
   * `/index.html` — หน้าเว็บไซต์ Standalone (สำคัญ)
   * `/src/app.js` — โค้ด JavaScript ต้นทาง
   * `/src/styles.css` — สไตล์ตารางคะแนนและผู้สอนหลายคน
   * `/data/instructors.json` — Master รายชื่อที่แก้ไขแล้ว
   * `/tools/build.py` — เวอร์ชัน Build ที่แสดง v1.3.1
   * `README_TH.md` — คู่มือใหม่ (ตามต้องการ)
5. หาก Upload ผ่านหน้าเว็บแล้วตำแหน่งไฟล์ไม่ตรง ให้เลือกไฟล์ใน GitHub แล้วใช้การ Edit หรือ Upload ในโฟลเดอร์ปลายทางเพื่อให้โครงสร้างถูกต้อง
6. Commit ข้อความ `Refine course form, instructors and grading UI v1.3.1`
7. ดาวน์โหลด `develop` แบบ ZIP มาทดสอบจาก Localhost ตาม README_TH.md
8. **ยังไม่ต้อง Merge เข้า `main`** จนกว่าจะตรวจสอบ Draft และ JSON จริงครบ

## ข้อควรระวัง

* `main` เป็น Branch ที่ GitHub Pages กำลัง Deploy อยู่ จึงไม่ถูกกระทบจนกว่าจะ Merge
* การคัดลอก `index.html` อย่างเดียวทำให้เว็บทำงานได้ แต่อย่าลืมซิงก์ `src` กับ Master JSON เพื่อให้แก้ไขรุ่นถัดไปได้ตรงกัน
* JavaScript เป็น Client-side ทั้งหมด: JSON และ Draft ไม่ถูกส่งเข้า Server ของมหาวิทยาลัย
