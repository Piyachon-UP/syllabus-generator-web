# Smart Syllabus Generator — v1.4.2 Simplified JSON Save

เว็บไซต์ Static HTML/CSS/JavaScript สำหรับอาจารย์ผู้สอน ใช้กับ GitHub Pages ได้โดยไม่ต้องมี Backend หรือ Build Server และไม่ต้องติดตั้ง Python ในเครื่องผู้ใช้

## หน้าจอหลัก v1.4.2

- **ด้านบน:** มีคำสั่งเดียว คือ **เปิด JSON** เพื่อเลือกไฟล์ Syllabus เดิมจากเครื่อง
- **ด้านล่าง:** แถบ **บันทึก JSON** (Sticky Footer) แสดงอยู่ตลอดเมื่อเลื่อนหน้าและอยู่ในทุกหมวดทั้ง 6 หมวด
- **ไม่มีปุ่มสร้างใหม่และไม่มีปุ่มตรวจสอบข้อมูล** ในรุ่นนี้ เปิด/รีเฟรชเว็บจะเริ่มฟอร์มว่าง
- **บันทึก JSON ได้ทุกเวลา** ไม่ว่ากรอกครบหรือไม่ครบ และบันทึกข้อมูล **ทุกหมวด** เป็นไฟล์เดียว
- ในหมวดการประเมิน Dropdown ประเภทประเมินมี **ปฏิบัติการ** เพิ่มจากรายการเดิม พร้อมตัวเลือก **กำหนดเอง**

## ข้อมูลที่บันทึก

ใช้ JSON SchemaVersion `1.0.0` และชื่อฟิลด์เดิมทั้งหมด เช่น `CourseInfo`, `Curriculum`, `Instructors`, `PLOs`, `CLOs`, `LecturePlans`, `LabPlans`, `Assessments`, `GradeScale`, `Resources` ข้อมูลไม่ครบสามารถ Export/Import ต่อได้ แต่อาจ **ไม่ผ่าน JSON Schema** จึงยังไม่ควรส่งเข้า Blazor/SQL Server จนกว่าจะตรวจสอบความถูกต้องจากระบบที่รองรับ

## วิธีใช้งาน

1. เปิด `index.html` ใน Chrome หรือ Edge หรือเปิดเว็บ GitHub Pages
2. กรอกข้อมูลทั้ง 6 หมวดตามต้องการ
3. กด **บันทึก JSON** จากแถบล่างในหมวดใดก็ได้
4. เก็บไฟล์ `.json` ที่ดาวน์โหลดไว้ในโฟลเดอร์ที่ต้องการ
5. ครั้งต่อไปเปิดเว็บไซต์ → กด **เปิด JSON** → เลือกไฟล์เดิม → แก้ไข → กด **บันทึก JSON** อีกครั้ง
6. หากต้องการเริ่มรายวิชาใหม่ ให้เปิดหน้าเว็บใหม่หรือรีเฟรช (แนะนำบันทึก JSON ก่อน)

**คำเตือน:** เว็บรุ่นนี้ไม่มี Auto Save และไม่บันทึกใน IndexedDB ดังนั้นหากปิด/รีเฟรชหน้าเว็บโดยยังไม่กด **บันทึก JSON** การแก้ไขรอบนั้นจะหายไป Browser อาจเตือนก่อนปิด และการดาวน์โหลดไม่ได้เขียนทับไฟล์ต้นฉบับโดยอัตโนมัติ ให้ตรวจสอบไฟล์ใหม่ใน Downloads ก่อน

## โครงสร้างสำคัญ

```text
syllabus-generator-web/
├── index.html                      # เว็บ Standalone สำหรับ GitHub Pages
├── src/
│   ├── app.js                      # UI/JSON import/export
│   └── styles.css                  # รวม Sticky Footer
├── tools/
│   ├── build.py                    # สร้าง index.html ใหม่จาก src และ Master JSON
│   └── test_ui_v142.py             # ทดสอบหน้าจอและ JSON end-to-end (นักพัฒนา)
├── data/
│   ├── curriculum_plos.json
│   └── instructors.json
├── schema/
│   └── syllabus.v1.schema.json     # ไม่เปลี่ยนจาก v1.4.1
└── sample/
    └── Smart_Syllabus_Demo.json
```

## พัฒนาหรืออัปเดตบน GitHub

1. เลือก Branch `develop` (ไม่ใช่ `main`)
2. จาก ZIP Patch ให้อัปโหลดแทนที่ `index.html`, `src/app.js`, `src/styles.css`, `tools/build.py` และอัปเดตคู่มือ
3. Commit ด้วยข้อความ `Simplify JSON save UI with persistent footer v1.4.2`
4. ดาวน์โหลด ZIP ของ Branch `develop` แล้วทดสอบโดยเปิดไฟล์ `index.html` หรือเรียก `py -3 -m http.server 8000` ในโฟลเดอร์โปรเจกต์
5. ตรวจสอบการ Import JSON จริง, Dropdown ประเภทประเมิน “ปฏิบัติการ”, ปุ่มบันทึกทุกหมวด และเปิด JSON กลับมาอีกครั้ง
6. เมื่อผ่านการทดสอบ จึงสร้าง Pull Request `develop` → `main` เพื่อเผยแพร่ GitHub Pages

สำหรับนักพัฒนาที่มี Playwright + Chromium และ jsonschema:

```bash
python tools/build.py
python tools/test_ui_v142.py
python tools/test_dropdown_roundtrip.py
python tools/test_json_only.py
```

**หมายเหตุ:** ตัวเว็บ Standalone ไม่จำเป็นต้องโหลดข้อมูลจากไฟล์ `data/` ณ เวลาใช้งาน เพราะ Master JSON ถูกฝังใน `index.html` โดย `tools/build.py` แล้ว
