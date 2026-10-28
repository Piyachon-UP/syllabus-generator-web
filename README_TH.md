# Smart Syllabus Generator Web UI v1.3.2

เว็บแอป Static HTML/CSS/JavaScript สำหรับอาจารย์ผู้สอน เปิดได้ผ่าน Browser และ GitHub Pages โดยไม่ต้องมี Backend หรือ Python Server สำหรับประมวลผลแอป

## ปรับปรุงจาก v1.3.1

1. **Course Info**: เมื่อสร้าง Draft ใหม่ ฟิลด์ `AcademicYear` (ปีการศึกษา พ.ศ.) และ `Semester` (ภาคเรียน) จะเป็นช่องว่าง ไม่มีค่าเริ่มต้น การเปิด Draft เก่าจะคงค่าที่เคยกรอกจริงไว้
2. **Instructors**: ย้าย ผศ.ดร. ผกาสุคนธ์ เมฆรัตนชัย ไปท้ายกลุ่มสาขาวิชาเคมีใน `data/instructors.json` โดยไม่เปลี่ยนจำนวนรวม 100 รายการ
3. **Instructors, CLOs, Assessments, Resources**: เมื่อยังไม่มีข้อมูลจะแสดงแถวกรอกเปล่า 1 แถว และหลังลบรายการสุดท้ายจะมีแถวเปล่าให้อัตโนมัติ
4. **Weekly Plan Lecture/Lab**: เพิ่ม `กำหนดเอง` ในรายการวิธีสอน เมื่อเลือกจะแสดงช่องให้พิมพ์วิธีการสอนด้วยตนเอง
5. **Assessments**: เพิ่ม `กำหนดเอง` ในประเภทประเมิน เมื่อเลือกจะแสดงช่องให้พิมพ์ประเภทประเมินด้วยตนเอง

แถวเปล่าเป็นเพียง UI ไม่ถูกนับเป็นข้อมูลจริงในระบบตรวจสอบหรือไฟล์ JSON Export

## โครงสร้างไฟล์

- `index.html` — หน้าเว็บแบบ standalone ฝัง CSS/JS/Schema/Master JSON ทั้งหมด พร้อมใช้บน GitHub Pages
- `src/app.js` — JavaScript ต้นฉบับ
- `src/styles.css` — CSS ต้นฉบับ
- `data/instructors.json` — รายชื่อผู้สอนและลำดับใหม่
- `data/curriculum_plos.json` — ข้อมูล PLO หลักสูตร
- `schema/syllabus.v1.schema.json` — JSON Contract v1.0.0 เดิม
- `sample/Smart_Syllabus_Demo.json` — ตัวอย่างข้อมูล
- `tools/build.py` — สร้าง index.html จากไฟล์ต้นฉบับ
- `tools/test_v132.py` — ชุดทดสอบแบบ Browser สำหรับนักพัฒนา (ต้องติดตั้ง playwright / jsonschema และ chromium)

## ทดสอบผ่าน Localhost บน Windows

เปิด PowerShell จากโฟลเดอร์นี้:

```powershell
py -3 -m http.server 8000
```

เปิด `http://localhost:8000/` แล้วเลือก **เครื่องมือ → สร้าง Draft ใหม่** เพื่อดูช่องปีการศึกษา/ภาคเรียนที่ว่าง และแถวเริ่มต้นให้กรอกในแท็บผู้สอน, CLOs, การประเมิน

**สำคัญ:** Draft เก่าที่มีข้อมูลบันทึกแล้วจะถูกเรียกคืนโดยอัตโนมัติ และยังคงค่า AcademicYear/Semester เดิมไว้เพื่อไม่เปลี่ยนข้อมูลของผู้ใช้โดยไม่ได้รับอนุญาต หากต้องการทดสอบค่าที่ว่าง ให้ **สำรอง Draft JSON** แล้วกด **สร้าง Draft ใหม่** ก่อน

## การบันทึกข้อมูล

บันทึก Draft ใน Browser ผู้ใช้ และสำรอง/ส่งออกเป็น JSON Schema v1.0.0 ไม่มีการส่งข้อมูลไปยัง Server อัตโนมัติ แนะนำให้สำรอง Draft เป็น JSON เป็นระยะ เพราะ Storage ใน Browser อาจถูกลบได้

## เผยแพร่

อัปโหลด `index.html`, `src/app.js`, `data/instructors.json`, `tools/build.py` ไปยังตำแหน่งเดิมใน Branch `develop` ไม่ต้อง Merge ไป `main` จนกว่าจะทดสอบเสร็จ

หากแก้ Source Code ต่อเอง เรียก `py -3 tools/build.py` ทุกครั้งก่อน Commit `index.html` ใหม่ เนื่องจาก `index.html` เป็นไฟล์ที่สร้างขึ้นจาก Source

## ความเข้ากันได้

- JSON Schema/Contract ยังเป็น `1.0.0`
- ไม่เปลี่ยน API / ชื่อ Field ใน JSON
- `curriculum_plos.json` เดิมไม่เปลี่ยน
- แถวเปล่าจะไม่ถูกส่งออก JSON แต่ Validation ยังเตือนเมื่อข้อมูลที่จำเป็นยังไม่ครบ
- ไม่ได้เปลี่ยนข้อมูล Draft ที่เคยบันทึกไว้
