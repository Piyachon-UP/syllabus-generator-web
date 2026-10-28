# Smart Syllabus Generator — Phase 1: Static Web App

**คณะวิทยาศาสตร์ มหาวิทยาลัยพะเยา | Version 1.0.0**  
**สถานะ:** ต้นแบบใช้งาน (Phase 1) — กรอกข้อมูล 6 แท็บ, ตรวจสอบ, บันทึก Draft, นำเข้า/ส่งออก JSON **ไม่ต้องมี Backend และไม่ต้องติดตั้ง Python / Node.js เพื่อใช้งานเว็บ**

## วิธีเริ่มใช้งาน

- สำหรับผู้สอน: เปิด URL ของ GitHub Pages ที่ผู้ดูแลระบบจัดให้ หรือเปิด `index.html` ด้วย Chrome / Edge / Safari รุ่นปัจจุบันเพื่อทดลอง (การเก็บ Draft ในโหมด `file://` อาจมีข้อจำกัดตาม Browser จึงแนะนำใช้งานบน HTTPS)
- กรอกข้อมูลผ่าน 6 แท็บในเมนูด้านซ้าย: **Course Info**, **PLOs**, **Instructors**, **CLOs**, **Weekly Plan**, **Assessments**
- ระบบจะบันทึก Draft อัตโนมัติใน Browser (IndexedDB; หากไม่พร้อมจะลอง localStorage) และมีปุ่ม **บันทึก Draft** สำหรับการบันทึกทันที
- กด **สำรอง Draft JSON** เพื่อเก็บงานแม้ยังกรอกไม่ครบ; ไฟล์นี้ยังไม่ใช่เอกสารยืนยันว่าผ่าน Validation
- กด **ตรวจสอบ** เพื่อดูข้อผิดพลาด/คำเตือน; คลิกข้อผิดพลาดเพื่อไปยังแท็บนั้น
- กด **ส่งออก JSON** เมื่อไม่มีข้อผิดพลาด เพื่อดาวน์โหลดไฟล์ข้อมูลรูปแบบกลาง นำกลับมาแก้ได้ด้วย **นำเข้า JSON**
- ปุ่ม **ข้อมูลตัวอย่าง** โหลดชุดข้อมูลสมมติ 244442 จาก Excel Demo เพื่อสาธิตการทำงานเท่านั้น ต้องเปลี่ยนเป็นข้อมูลจริงทุกฟิลด์

**สำคัญ:** ข้อมูล Draft ใน Browser **ไม่ซิงก์ข้ามอุปกรณ์**, ไม่ใช่ Cloud Backup; อาจหายเมื่อเคลียร์ข้อมูลเว็บไซต์ / ใช้ Incognito / เปลี่ยน Browser จึงควรใช้ **สำรอง Draft JSON** บ่อย ๆ ขณะกรอก และเก็บไฟล์ที่ปลอดภัยตามนโยบายมหาวิทยาลัย

## โครงสร้างข้อมูล: ใช้ร่วมกับ Smart Excel + Central Python Extractor

แอปนี้เก็บและส่งออกคีย์ JSON แบบ **PascalCase** ตามไฟล์ `schema/syllabus.v1.schema.json` (v1.0.0) ที่เคยใช้กับ Excel Extractor:

```text
SchemaVersion, OfferingId, SourceType, ExtractedAt,
CourseInfo, Curriculum, Instructors, PLOs, CLOs,
ClassMeetings, Exams, StudentGroups,
LecturePlans, LabPlans, Assessments, GradeScale, Resources
```

- `OfferingId` สร้างอัตโนมัติเป็น `CourseCode-Semester-AcademicYear-SECxx` เช่น `244442-1-2569-SEC01`
- รหัสหลักสูตร **CurriculumRevisionYear** และข้อมูลกลุ่มนิสิตแยกตามหลักสูตร **StudentCurriculumRevisionYear**
- ผู้สอนมี `StaffId` / `Email` และ `IsResponsibleInstructor` เลือกผู้รับผิดชอบ 1 คน
- ตาราง `ClassMeetings`, `Exams`, `StudentGroups` อยู่ภายในแท็บ Course Info
- ตาราง `LecturePlans` และ `LabPlans` แยกจากกัน พร้อมแม่แบบ 15 สัปดาห์
- ค่าร้อยละใช้ **0–100** เช่น `25` หมายถึง 25% ไม่ใช่ `0.25`
- รหัส PLO / CLO ที่เชื่อมโยงกรอกโดยคั่นด้วยจุลภาค (`,`)
- `SourceType` ส่งออกเป็น **`BlazorManual`** เนื่องจาก enum ของ JSON Schema v1.0.0 เดิมมีเพียง `ExcelManual`, `RegView`, `BlazorManual` เท่านั้น จึงใช้ค่าเดิมเพื่อให้ Blazor Import รับได้ (หมายถึงแหล่งข้อมูลกรอกเองใน UI; เว็บนี้ไม่ได้ใช้ Blazor) หากจะเพิ่ม `WebManual` ภายหลังต้องออกรุ่น Schema ใหม่ให้ครบทั้ง Excel, Web, DTO และฐานข้อมูล
- ข้อมูลว่างแบบ optional ไม่รวมใน JSON; ข้อมูลที่จำเป็นแต่ยังไม่กรอกจะมี Validation error
- ขณะนี้ **ไม่มีการเชื่อมต่อ REG, SQL Server, Google Drive หรือ Cloud** ข้อมูลคงอยู่ในเครื่องจนกว่าผู้ใช้ดาวน์โหลดและส่งไฟล์เอง

## การนำเว็บไซต์ขึ้น GitHub Pages (โดยไม่ต้องตั้ง Backend)

1. เข้า GitHub แล้วสร้าง Repository เช่น `syllabus-generator-web` (สำหรับ GitHub Pages บัญชีฟรีแนะนำ **Public Repository**)
2. กด **Add file → Upload files** อัปโหลดไฟล์ `index.html` ที่โฟลเดอร์ root ของ Repository (อาจเพิ่ม `.nojekyll`, `README_TH.md`, `schema/` แต่หน้าเว็บใช้งานได้ด้วย **index.html เพียงไฟล์เดียว**)
3. กด **Commit changes** ไปที่ Branch `main`
4. เข้า **Settings → Pages → Build and deployment** เลือก **Deploy from a branch** และตั้งค่า Branch: `main`, Folder: `/(root)` แล้วกด Save
5. เปิด URL รูปแบบ `https://<ชื่อผู้ใช้>.github.io/syllabus-generator-web/` เมื่อระบบเผยแพร่เรียบร้อย
6. หากต้องการแก้ไข UI ให้แก้ `src/app.js` / `src/styles.css` แล้วรัน `python tools/build.py` (เครื่องนักพัฒนาเท่านั้น) เพื่อสร้าง `index.html` ใหม่ จากนั้น Commit ทับไฟล์เดิม

> GitHub Pages เป็น **Static Hosting** ไม่ใช่พื้นที่เก็บไฟล์ Draft ของอาจารย์ และ Repository ที่เป็น Public เปิดเผย Source Code ทุกคน จึง **ห้าม Commit ข้อมูลบุคลากรจริง / รายชื่อนิสิต / รหัสผ่าน / OAuth client secret** ลงไปใน Repository

## การทดสอบในเครื่องนักพัฒนา (ไม่จำเป็นต่อผู้ใช้)

ทดสอบผ่าน Local Static Server เพื่อให้ Origin ทำงานคล้าย GitHub Pages:

```bash
cd syllabus-generator-web
python -m http.server 8000
# เปิด http://localhost:8000/
```

`index.html` เป็น Standalone HTML ที่ฝัง CSS/JS/JSON Schema/ตัวอย่างไว้ทั้งหมด **ไม่โหลด CDN, API หรือ Font จากภายนอก**. สามารถเปิดหน้าเว็บได้ใน Safari, Edge, Chrome, Firefox รุ่นใหม่ที่รองรับ JavaScript และ IndexedDB โดยต้องทดสอบกับ Browser ที่บุคลากรใช้จริงก่อนเปิดใช้ทั้งคณะ

ชุดคำสั่งทดสอบเพิ่มเติม (สำหรับนักพัฒนาเท่านั้น, ต้องมี Playwright, Chromium และ jsonschema ในเครื่องทดสอบ):

```bash
python tools/test_ui.py
python tools/test_storage.py
```

## สิ่งที่ Phase 1 ทำแล้ว

- ✅ 6 แท็บหลัก พร้อม Course Info/Curriculum, ผู้สอน, PLO, CLO, แผนสอน, Assessment
- ✅ ตารางเพิ่ม/ลบแถวสำหรับผู้สอน PLO CLO ตารางเรียน/สอบ กลุ่มนิสิต แผนสอน 2 ตาราง การประเมิน เกณฑ์ตัดเกรด และเอกสารประกอบ
- ✅ สร้าง OfferingId อัตโนมัติ และสรุปจำนวนผู้สอน, CLO, แผนสอน, น้ำหนักคะแนนบนหน้าแรก
- ✅ ตรวจสอบฟิลด์จำเป็น ค่าร้อยละ ชื่อผู้รับผิดชอบ รหัส PLO/CLO อ้างอิงซ้ำ การอ้างอิง PLO/CLO ที่ไม่พบ รายการสอน สอบและช่วงคะแนน
- ✅ บันทึก Draft อัตโนมัติ + บันทึกทันที + จัดการหลาย Draft ใน Browser
- ✅ สำรอง Draft JSON (แม้ข้อมูลยังไม่ครบ), นำเข้า JSON และส่งออก JSON เมื่อผ่าน Validation
- ✅ ไม่มี Backend, npm, build tool หรือการเรียก CDN ในการใช้งานจริง

## สิ่งที่ยังไม่อยู่ใน Phase 1

- ⏳ DOCX Generator แบบ Browser (Phase 2)
- ⏳ ลงทะเบียน PWA / Offline Cache (Phase 3)
- ⏳ Save/Open จาก Google Drive และ OAuth (Phase 4)
- ⏳ Blazor API + SQL Server + REG View (Phase 5)

**ข้อควรทราบ:** ยังต้องทดสอบกับข้อมูลหลักสูตรจริงและตรวจผล JSON Import กับ EF Core Migration ปัจจุบันของโปรเจกต์ Blazor ก่อนใช้ Production เต็มรูปแบบ การทดสอบ JSON Schema ที่ผ่านไม่ได้แปลว่าฐานข้อมูล Blazor ติดตั้งตรงกันทุกคอลัมน์โดยอัตโนมัติ

## โครงสร้าง Source Code

```text
syllabus-generator-web/
├── index.html                         # Standalone production site (deploy this)
├── .nojekyll
├── src/
│   ├── app.js                         # Form, validation, IndexedDB, JSON import/export
│   └── styles.css                     # UI & responsive CSS
├── schema/
│   └── syllabus.v1.schema.json        # Canonical JSON Schema v1.0.0
├── sample/
│   ├── Smart_Syllabus_Demo.json       # ตัวอย่างสมมติจากชุด Excel รุ่นก่อน
│   ├── Exported_From_Browser_Demo.json
│   ├── Syllabus_Web_Desktop.png
│   └── Syllabus_Web_Mobile.png
└── tools/
    ├── build.py                       # รวม HTML / JS / CSS / schema เป็นไฟล์เดียว
    ├── test_ui.py                      # Smoke test UI, Export JSON & Schema
    └── test_storage.py                 # ทดสอบ fallback localStorage / draft
```
