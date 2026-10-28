# Smart Syllabus Generator Web v2.0.0 — Phase 2: Browser DOCX

ระบบ Static Web App สำหรับคณะวิทยาศาสตร์ มหาวิทยาลัยพะเยา ใช้งานบน GitHub Pages ได้โดยไม่ต้องมี Backend หรือ Python ฝั่งผู้ใช้

## สิ่งที่เพิ่มจาก v1.4.3

- เพิ่มปุ่ม **สร้าง DOCX** ใน Sticky Footer คู่กับ **บันทึก JSON** (มีอยู่ในหน้าจอทั้ง 6 หมวด)
- สร้าง Microsoft Word `.docx` จากข้อมูลในฟอร์มโดย JavaScript **ภายใน Browser** ไม่มีการส่งไฟล์ไป Server และไม่มีการโหลดไลบรารีจาก CDN
- จัดหน้า A4 พร้อมหัวข้อและตาราง: ข้อมูลรายวิชา/คำอธิบาย, PLOs, ผู้สอน, CLOs, Lecture Plan, Lab Plan, การวัดและประเมินผล, เกณฑ์เกรด, หนังสือและแหล่งเรียนรู้
- เก็บข้อมูลตารางเรียน ตารางสอบ และกลุ่มนิสิตจาก JSON เดิมใน **ภาคผนวก** ถ้ามีข้อมูล
- แปลงหน่วยกิตและชั่วโมงเรียนเป็น `3(2-2-5)` ตามข้อมูลในช่องกรอก (เช่น `Credits=3`, `LectureHours=2`, `LabHours=2`, `SelfStudyHours=5`)
- ชื่อผู้สอนหลายคนใน `LecturePlans.Notes` และ `LabPlans.Notes` จะขึ้นหลายบรรทัดใน DOCX
- ถ้าข้อมูลรายวิชาในส่วนหัวไม่ครบ จะใส่ข้อความ **ฉบับร่าง** ใน DOCX; ยังอนุญาตให้สร้างไฟล์ได้
- JSON Schema **v1.0.0 ไม่เปลี่ยน**; บันทึก JSON ไม่บังคับ Validation เหมือนเดิม

## วิธีใช้งาน

1. เปิด `index.html` ด้วย Chrome/Edge หรือ GitHub Pages (ไม่จำเป็นต้องรัน Server)
2. กรอกข้อมูลใหม่ หรือคลิก **เปิด JSON** เพื่อโหลดไฟล์เดิม
3. เมื่อกำลังแก้ไขข้อมูล ให้กด **บันทึก JSON** เพื่อเก็บต้นฉบับที่นำมาแก้ไขต่อในภายหลัง (ไม่ใช่ Auto Save)
4. เมื่ออยากได้เอกสาร Word ให้กด **สร้าง DOCX** จาก Sticky Footer ในหมวดใดก็ได้
5. เปิดเอกสารที่ดาวน์โหลดใน Microsoft Word และตรวจรูปแบบ/ความครบถ้วนก่อนนำไปใช้จริง

ตัวอย่างชื่อไฟล์: `SYLLABUS_244106_2569_2_2.json` และ `SYLLABUS_244106_2569_2_2.docx`

## ข้อควรทราบ

- Word ที่สร้างเป็น **แม่แบบเอกสารฉบับแรกสำหรับ Phase 2** ยังไม่ใช่เอกสารที่ได้รับการรับรองตามรูปแบบทางการของมหาวิทยาลัย หากต้องการให้เหมือน DOCX Generator รุ่น Python ทุกจุด ต้องเทียบกับตัวอย่างเอกสารจริงและปรับรูปแบบใน `src/docx_export.js`
- ฟอนต์ใน DOCX กำหนดชื่อเป็น `TH Sarabun New` ซึ่งจะใช้ได้ตรงตามที่กำหนดเมื่อมีฟอนต์บนเครื่องเปิด Word; ไม่ฝังหรือแจกฟอนต์มากับไฟล์
- ZIP DOCX ภายในถูกประกอบด้วย JavaScript (WordprocessingML + ZIP STORE) ไม่ต้องใช้บริการ CDN, npm หรือ Backend ขณะใช้งาน
- DOCX คือ **ผลลัพธ์อ่าน/พิมพ์** ส่วน **JSON เป็นไฟล์ต้นฉบับสำหรับแก้ไขซ้ำและนำเข้า Blazor** จึงควรเก็บ JSON ไว้ด้วยทุกครั้ง
- Phase 2 ไม่มีปุ่ม Validation ตามที่กำหนดไว้ใน v1.4.2; การสร้าง DOCX ไม่ได้แปลว่าข้อมูลผ่านการตรวจสอบหรือพร้อมส่งระบบกลาง
- ไม่ใช้ IndexedDB/LocalStorage ในการบันทึกงาน ต้องกด **บันทึก JSON** ก่อนปิดหรือ Refresh
- การสร้าง DOCX ไม่อัปโหลดข้อมูลเข้าระบบใด ๆ ข้อมูลและไฟล์จะอยู่บนอุปกรณ์ของผู้ใช้

## โครงสร้างไฟล์

```text
syllabus-generator-web/
├── index.html                       # Static Web ใช้งานจริง (รวมสคริปต์และ Master JSON แล้ว)
├── src/
│   ├── app.js                       # จัดการ UI, JSON, และเรียก DOCX Generator
│   ├── docx_export.js               # สร้าง DOCX ใน Browser (เพิ่มใหม่)
│   └── styles.css                   # Responsive Layout, Sticky Footer
├── tools/
│   ├── build.py                     # ประกอบ index.html จากไฟล์ Source
│   ├── test_phase2.py               # Browser end-to-end test
│   └── test_docx_node.cjs           # Node smoke test สำหรับตัวสร้าง Word
├── data/
│   ├── curriculum_plos.json
│   └── instructors.json
├── schema/
│   └── syllabus.v1.schema.json      # ไม่เปลี่ยนจาก v1.4.3
└── sample/
    ├── Smart_Syllabus_Demo.json
    └── Smart_Syllabus_Demo.docx     # เอกสารตัวอย่างสร้างด้วย JS
```

## Build และทดสอบสำหรับนักพัฒนา

```powershell
py -3 tools/build.py
py -3 tools/test_phase2.py
# สำหรับผู้มี Node.js: 
node tools/test_docx_node.cjs
```

หากเปิดเว็บไซต์ออนไลน์จาก GitHub Pages ให้ Upload ชุดไฟล์ `index.html`, `src/`, `tools/` ใน Branch `develop` ก่อน; GitHub Pages ที่ใช้ `main` จะยังไม่เปลี่ยนจนกว่าจะ Merge.
