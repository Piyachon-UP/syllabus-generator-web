# การอัปเดต UX/UI v1.1 ไปยัง GitHub Branch `develop`

**Project:** `Piyachon-UP/syllabus-generator-web`  
**Website ที่เผยแพร่อยู่:** https://piyachon-up.github.io/syllabus-generator-web/  
**ข้อกำหนด:** ไม่แก้ Branch `main` จนกว่าจะทดสอบ UX/UI v1.1 ผ่าน

## สิ่งที่เปลี่ยนใน v1.1

1. จัดปุ่มใหม่: ด้านบนมี **Draft ของฉัน**, **เครื่องมือ**, **บันทึก Draft**; เมนูเครื่องมือรวม **สร้าง Draft ใหม่**, **นำเข้า JSON**, **สำรอง Draft JSON**, **โหลดข้อมูลตัวอย่าง**. ส่วนคำสั่งที่เกี่ยวกับการตรวจเอกสารคง **ตรวจสอบ** และ **ส่งออก JSON** ที่หัวข้อแต่ละแท็บ
2. Course Info ถูกแบ่งเป็น 3 การ์ด: รายวิชาและภาคเรียน / หน่วยกิตและรูปแบบการสอน / คำอธิบายและหน่วยงาน และเพิ่มแถบกระโดดไปยังหมวดสำคัญ
3. เพิ่มแถบความคืบหน้า 6 ส่วนทั้ง Desktop และ Mobile อิงข้อมูลจริง; แสดง *ครบเบื้องต้น / กำลังกรอก / ยังไม่กรอก*. ความคืบหน้านี้ไม่ใช่ผลรับรอง Validation
4. **ไม่เปลี่ยน JSON Schema v1.0.0**, คีย์ใน JSON, `OfferingId` หรือชื่อที่เก็บ Draft `up-syllabus-drafts-v1`

## ก่อนอัปโหลด

- หากมี Draft สำคัญในเว็บเดิม ให้เปิดเว็บเดิม → **สำรอง Draft JSON** ไว้ในเครื่องก่อน เพื่อความปลอดภัย
- อัปโหลด **ไฟล์ที่แตกออกมาจาก ZIP** ไม่ใช่อัปโหลด ZIP ลง Repository
- อย่า Commit ชื่อ-อีเมล-รหัสบุคลากรจริงหรือไฟล์ Draft ของบุคคลอื่นลง Public Repository

## วิธีใช้ GitHub Website (ไม่ต้องใช้ Git Command)

1. เปิด https://github.com/Piyachon-UP/syllabus-generator-web แล้วกด **Code**.
2. คลิกช่องเลือก Branch ที่แสดง `main` และเลือก **develop**. ถ้ายังไม่มี ให้พิมพ์ `develop` แล้วกด **Create branch: develop from main**.
3. ตรวจสอบว่า Branch ปัจจุบันเป็น **develop** ก่อนแก้ไฟล์.
4. กด **Add file → Upload files** และลากเนื้อหาภายในโฟลเดอร์โปรเจกต์ ZIP เข้าสู่ Root ของ Repository (ต้องมี `index.html` อยู่ Root เดียวกับของเดิม).
5. ไฟล์ที่ต้องอัปเดตเป็นอย่างน้อย: `index.html`, `src/app.js`, `src/styles.css`, `tools/build.py`, `tools/test_ui.py`, `tools/test_storage.py`, `README_TH.md`, `DEPLOY_DEVELOP_TH.md`; ชุดส่งมอบนี้มี `schema/` และ `sample/` ด้วยเพื่อให้ครบถ้วน.
6. ที่ Commit message ให้ใส่ `Improve UX/UI: grouped Course Info, progress and actions (v1.1)` และยืนยัน Commit ไป Branch **develop**.
7. ตรวจสอบหน้า Code ของ Branch `develop` ว่า `index.html` อัปเดตแล้ว โดยค้นหาคำว่า `COMPLETION OVERVIEW`.

## ทดสอบ Develop โดยไม่กระทบเว็บไซต์หลัก

GitHub Pages ปัจจุบันเผยแพร่จาก `main` ดังนั้นอัปโหลด `develop` อย่างเดียวจะยัง **ไม่ปรับเว็บ Live**.

ทางเลือกทดสอบง่ายที่สุด: ดาวน์โหลดไฟล์ `index.html` ของ Branch `develop` มาเปิดใน Chrome/Edge หรือรัน local static server:

```powershell
py -3 -m http.server 8000
```

แล้วเปิด http://localhost:8000/ ในเครื่องนักพัฒนาเพื่อทดสอบ (สำรอง Draft JSON ก่อนทดสอบ URL ใหม่). ถ้าต้องการ URL แยกสำหรับ `develop` ในอนาคต ให้สร้าง staging repository/Pages หรือใช้บริการ Preview เฉพาะทาง ไม่ควรเปลี่ยน Pages Source ไป develop เพราะจะกระทบเว็บ Live.

## ตรวจสอบก่อน Merge เข้า main

- เปิดครบ 6 แท็บ / แถบความคืบหน้ามีครบ 6 ขั้น
- Course Info มี 3 การ์ด ไม่ตกหล่นฟิลด์เดิม 18 ช่อง
- ค้นหาและกดใช้ปุ่มใต้เมนู **เครื่องมือ** ได้ รวมถึง Import/Backup JSON
- กรอกข้อมูลตัวอย่าง: รหัส `244442-1-2569-SEC01`, ความคืบหน้าเบื้องต้น `6 / 6 ส่วน`
- กด **ตรวจสอบ**: ข้อผิดพลาด = 0 (อาจมีคำเตือนตามข้อมูลตัวอย่าง)
- **ส่งออก JSON** และ **นำเข้า JSON** กลับมาได้
- บันทึก Draft แล้ว Reload ยังมีข้อมูล และ Backup JSON ได้
- ทดสอบบนจอ Desktop และ Mobile

เมื่อทดสอบเสร็จ ให้ไปที่ Pull requests → New pull request → base: `main`, compare: `develop` → Create pull request → ตรวจ Diff → Merge Pull Request. GitHub Pages จาก `main` จะอัปเดตตามการ Merge.

## สร้างไฟล์ index.html ใหม่ในการพัฒนาครั้งต่อไป

แก้ `src/app.js` และ `src/styles.css` แล้วรันในโฟลเดอร์หลัก:

```powershell
py -3 tools/build.py
```

จึง Commit ทั้ง Source Code และ `index.html` ที่ Build ใหม่ไปยัง `develop`.

**ข้อควรทราบ:** แอปยังประมวลผลทั้งหมดใน Browser และไม่มี Cloud Sync / Backend / DOCX Generator (DOCX อยู่ Phase 2).
