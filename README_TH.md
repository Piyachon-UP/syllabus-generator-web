# Smart Syllabus Generator Web — UX/UI v1.2.0

**โครงการ:** Syllabus Generator สำหรับคณะวิทยาศาสตร์ มหาวิทยาลัยพะเยา

เว็บแอป HTML/CSS/JavaScript ประมวลผลบนเครื่องผู้ใช้ (Browser-only) ไม่มี Backend สำหรับกรอก Syllabus ใน Phase 1 ใช้สัญญาข้อมูล `SchemaVersion: 1.0.0` แบบเดิม และเก็บ Draft ใน IndexedDB หรือ fallback localStorage ของ Browser (โปรไฟล์/Origin เดียวกัน)

## การเปลี่ยนแปลงตามข้อเสนอ

- ลบ Dashboard ทั้ง Hero, ตัวเลขสถิติ และ Progress Overview ออกจากหน้าจอ
- หน้าข้อมูลรายวิชาเหลือ 3 หมวด: (1) รายวิชาและภาคเรียน (2) หน่วยกิต/ชั่วโมงเรียน (3) คำอธิบายรายวิชาไทย/อังกฤษ
- ยกเลิกเมนูย่อย "ไปยังหมวด" และซ่อนฟิลด์ Course Info ที่ระบุ ได้แก่ TeachingLanguage, DeliveryMode, Prerequisites, FacultyName, UniversityName, Remarks
- ไม่แสดงส่วน Curriculum, ClassMeetings, Exams, StudentGroups ในแท็บข้อมูลรายวิชา (เก็บกลุ่มโครงสร้างไว้ใน JSON Schema v1 เดิม เพื่อรองรับ Draft/Blazor)
- แท็บ PLOs เลือกหลักสูตรจาก Dropdown ที่ใช้ `data/curriculum_plos.json` แล้วแสดง PLO ทุกข้อแบบอ่านอย่างเดียว; ระบบบันทึกลง `Curriculum` และ `PLOs` ใน JSON
- แท็บผู้สอนเลือกหลักสูตรเพื่อกรองรายชื่อผู้สอนตาม **สาขาวิชา (Department)** ของหลักสูตร โดยใช้ `data/instructors.json`; มีตัวเลือกแสดงรายชื่อจากทุกสาขาสำหรับการสอนข้ามสาขา
- กำหนดผู้รับผิดชอบ 1 คน และ Lecture%/Lab% ตามเดิม; รับข้อมูลชื่อ คำนำหน้า และสาขาจาก Master โดยไม่แต่ง StaffId หรือ Email ที่ไม่มีในไฟล์ต้นทาง
- การตรวจสอบ StaffId/Email เปลี่ยนเป็น **ข้อควรตรวจ** แทน Error ทำให้สามารถส่งออก JSON สำหรับใช้งานช่วงรอ REG ได้ (แต่ต้องเติมตัวระบุจริงก่อนเชื่อมต่อ REG/Blazor ที่ต้องใช้คีย์)

## ความหมายของ "ตามหลักสูตร" ในแท็บผู้สอน

ไฟล์ `instructors.json` ที่ให้มามี `title_prefix`, `name`, `department`, `note` แต่ **ไม่มี** ตัวระบุหลักสูตรที่อาจารย์สอน จึงกรองรายชื่อจาก `department` ที่สอดคล้องกับ `major` ของหลักสูตร ไม่ใช่ข้อมูลการมอบหมายผู้สอนเป็นรายหลักสูตรตามฐานทะเบียน ถ้าจำเป็นต้องเลือกผู้สอนต่างสาขา ให้เปลี่ยนตัวกรองเป็น "แสดงรายชื่อทุกสาขาวิชา".

ไฟล์ PLO มี 15 หลักสูตร แต่ไม่มีฟิลด์ปีปรับปรุงหลักสูตร (CurriculumRevisionYear). แอปจึงไม่สร้างปีขึ้นมาเอง และควรเพิ่ม Master Data รุ่นที่ระบุปีการปรับปรุงในอนาคตเพื่อใช้ตรวจสอบความถูกต้องของ PLO กับ REG/Blazor.

## วิธีทดสอบทันที

- แตก ZIP แล้วเปิด `index.html` ด้วย Chrome/Edge (ไฟล์นี้ฝัง CSS, JavaScript, JSON Schema และ Master JSON ไว้ในไฟล์แล้ว)
- วิธีที่แนะนำสำหรับการทดสอบ Draft และการ Import/Export ให้เปิด Terminal/PowerShell ในโฟลเดอร์นี้ แล้วใช้ `py -3 -m http.server 8000` (Windows) หรือ `python3 -m http.server 8000` (macOS)
- เปิด `http://localhost:8000/` แล้วเลือกแท็บ PLOs → เลือกหลักสูตร → แสดง PLO → แท็บผู้สอน → เพิ่มผู้สอนจาก Dropdown → กรอกข้อมูล Course Info / CLO / Weekly Plan / Assessment → ตรวจสอบ → ส่งออก JSON
- ต้องสำรอง Draft ที่สำคัญด้วยปุ่ม "สำรอง Draft JSON" ในเมนูเครื่องมือ เพื่อหลีกเลี่ยงความเสี่ยงเมื่อ Browser หรืออุปกรณ์เปลี่ยน

## ไฟล์สำคัญ

```text
index.html                        เว็บไซต์ไฟล์เดียว (GitHub Pages)
src/app.js                        ฟังก์ชันและฟอร์ม UI
src/styles.css                   สไตล์หน้าจอ
data/curriculum_plos.json         Master ข้อมูลหลักสูตร/PLO จากไฟล์ที่ผู้ใช้ให้
data/instructors.json             Master รายชื่ออาจารย์จากไฟล์ที่ผู้ใช้ให้
schema/syllabus.v1.schema.json   JSON Contract v1.0.0 เดิม
tools/build.py                    รวม Source + Master + Schema → index.html
sample/Smart_Syllabus_Demo.json   ข้อมูลสมมติของ Phase 1
```

> หมายเหตุ: ก่อนเผยแพร่ Repository แบบ Public โปรดตรวจสอบนโยบายของหน่วยงานเกี่ยวกับการนำข้อมูลรายชื่ออาจารย์และ PLO ขึ้นเว็บไซต์ แม้จะเป็นข้อมูลที่ผู้ใช้ส่งมาให้ก็ตาม และห้ามใส่ข้อมูลลับ/รหัสผ่าน/Token ใน Source Code

## วิธีพัฒนาต่อ

แก้ไขไฟล์ใน `src/` หรือ Master ใน `data/` แล้วสร้าง `index.html` อีกครั้งก่อนอัปโหลด:

```powershell
py -3 tools/build.py
```

ไม่มี Node.js หรือ npm เป็นข้อบังคับในการใช้งานหรือสร้างไฟล์เว็บในรุ่นนี้ (เครื่องนักพัฒนาต้องมี Python เพื่อรัน build.py เท่านั้น)

**สำคัญ:** การอัปโหลดไฟล์ Master ใหม่เข้าสู่ `data/` อย่างเดียว **ไม่ทำให้ `index.html` เปลี่ยนแปลง** ต้อง Build ใหม่ เพราะไฟล์ `index.html` ฝัง Master ไว้แล้ว เพื่อให้การเปิดเว็บไฟล์เดียวและ `file://` ทำงานได้โดยไม่ต้อง Fetch ไฟล์ข้อมูล

## การรองรับ Draft เดิม

- **ไม่ได้เปลี่ยน** ชื่อ IndexedDB/localStorage (`up-syllabus-drafts-v1`) และ JSON Schema (`1.0.0`)
- ฟิลด์และตารางที่ซ่อนจากหน้าจอจะยังคงอยู่ใน JSON เมื่อเปิด Draft รุ่นเก่าที่มีข้อมูลอยู่ เพื่อไม่ลบข้อมูลที่ผู้ใช้เคยกรอกโดยอัตโนมัติ
- เมื่อเปลี่ยนหลักสูตรที่มี PLO อยู่ ระบบขอให้ยืนยันก่อนแทนข้อมูล PLO; ควรตรวจ `MappedPloCodes` ของ CLO อีกครั้ง
- Browser แต่ละ Origin (`localhost:8000` และ GitHub Pages) มี Draft แยกกัน ให้ Backup JSON → Import JSON เมื่อต้องการย้ายงานข้าม Origin

## สิ่งที่ยังไม่รวมใน Phase 1

- สร้าง DOCX (Phase 2)
- เชื่อม REG View และการระบุตัวตนในระบบ Blazor
- ฐานข้อมูลกลาง / ระบบสิทธิ์ / ซิงก์ Draft ข้ามเครื่อง
