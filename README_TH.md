# Smart Syllabus Generator Web — UI v1.3.3

แอป HTML/CSS/JavaScript ทำงานทั้งหมดใน Browser โดยไม่ใช้ Backend และไม่ต้องติดตั้ง Node.js เพื่อ Deploy ไป GitHub Pages

## สิ่งที่เปลี่ยนจาก v1.3.2

1. **ปีการศึกษา / ภาคเรียน**: Draft ใหม่เริ่มช่องว่างทั้งคู่; ปิด Browser autocomplete สำหรับช่องข้อมูลรายวิชา; เมื่ออ่าน Draft รุ่นเดิม จะเปลี่ยน `AcademicYear` เป็นว่างเฉพาะกรณีค่าไม่ถูกต้อง `0` หรือ `1` และเปลี่ยน `Semester` ที่เป็น `0` ให้เป็นว่าง (ปี พ.ศ. ที่กรอกถูกต้อง เช่น `2569` และภาคเรียน `1` จะไม่ถูกเปลี่ยน)
2. **ผู้สอน**: ไม่มีแถวว่างเริ่มต้น ต้องคลิก **＋ เพิ่มผู้สอน** จึงเห็นแถวกรอก; หากเปิด Draft เก่าที่มีแถวผู้สอนเปล่าปนอยู่ ระบบซ่อน/ตัดแถวเปล่านั้น แต่เก็บรายการที่กรอกชื่อหรือข้อมูลไว้แล้ว
3. **แหล่งเรียนรู้**: เพิ่ม `กำหนดเอง` ใน Dropdown ประเภทแหล่งเรียนรู้ เมื่อเลือกแล้วช่องจะว่างและสามารถพิมพ์ประเภทภาษาไทยใหม่ได้

**ไม่เปลี่ยน JSON Schema v1.0.0, โครงสร้าง OfferingId, ข้อมูล Master และไฟล์ src/styles.css**

## วิธีทดลองบน Windows

1. แตก ZIP และเปิด PowerShell ในโฟลเดอร์ `syllabus_web_v1_3_3`
2. รัน `py -3 -m http.server 8000`
3. เปิด `http://localhost:8000/`
4. หากยังเห็นข้อมูลเดิม ระบบกำลังเปิด **Draft ที่บันทึกไว้ก่อนหน้า**; ลอง `เครื่องมือ → สร้าง Draft ใหม่` เพื่อตรวจช่องว่างใหม่ โดย **สำรอง Draft ที่สำคัญเป็น JSON ก่อน**
5. ทดสอบปีการศึกษาและภาคเรียนว่าง, ผู้สอนเริ่มต้นไม่มีแถว, เพิ่มผู้สอนและบันทึก, ประเภทแหล่งเรียนรู้เลือกกำหนดเองแล้วกรอกข้อความใหม่
6. กด Save Draft, Refresh และตรวจว่าข้อมูลที่กรอกยังอยู่
7. กดตรวจสอบและส่งออก JSON กับ Draft ที่กรอกครบ

> การแก้ไขทำใน Browser ของผู้ใช้และข้อมูลเก็บใน IndexedDB หรือ localStorage ตามความพร้อมของ Browser การเปิดแอปผ่าน `localhost` และ GitHub Pages เป็นคนละ Origin จึงไม่เห็น Draft ข้ามกันโดยอัตโนมัติ ควร Backup JSON ก่อนเปลี่ยน URL

## สำหรับนักพัฒนา

โครงสร้างสำคัญ:

- `index.html` ไฟล์ Standalone สำหรับ Deploy ที่ Root บน GitHub Pages
- `src/app.js` ต้นทาง JavaScript
- `src/styles.css` CSS เดิม (ไม่เปลี่ยนในรุ่นนี้)
- `data/` ข้อมูล Master เดิม (ไม่เปลี่ยนในรุ่นนี้)
- `schema/` JSON Schema v1.0.0
- `tools/build.py` ใช้สร้าง index.html จากโค้ด/ข้อมูล Master
- `tools/test_v133.py` ทดสอบด้วย Chromium/Playwright และ JSON Schema แบบจำลอง Storage (เครื่องพัฒนาที่รันทดสอบต้องมี `playwright` และ `jsonschema` และ Chromium)

Build หลังแก้ไข Source:

```powershell
py -3 tools/build.py
```

สำหรับขั้นตอน Upload ไป Branch develop ดู `DEPLOY_DEVELOP_TH.md`
