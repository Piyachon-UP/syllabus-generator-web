# อัปเดต Smart Syllabus Generator v1.4.3 ลง Branch `develop`

**หลักการ:** ปรับขนาดตัวอักษร / Sidebar / Mobile Cards / Sticky Footer เท่านั้น; ไม่เปลี่ยน Schema, JSON, Dropdown หรือวิธีเปิด/บันทึก JSON

## ขั้นตอน

1. สำรอง JSON ที่กำลังกรอกไว้ในเครื่อง และตรวจว่าไฟล์ถูกดาวน์โหลดครบ
2. เข้า `https://github.com/Piyachon-UP/syllabus-generator-web` เลือก Branch **develop** (ไม่ใช่ main)
3. ดาวน์โหลด Patch v1.4.3 และแตก ZIP; วางไฟล์ให้ตรงตำแหน่งเดิม:
   - `index.html` ที่ Root
   - `src/app.js`, `src/styles.css`
   - `tools/build.py`, `tools/test_ui_v143.py`, `tools/test_responsive_v143.py`
   - `README_TH.md`, `DEPLOY_DEVELOP_TH.md`, `CHANGELOG_TH.md`
4. Commit ด้วยข้อความ `Improve responsive typography and mobile layout v1.4.3`
5. ดาวน์โหลด ZIP จาก Branch develop แล้วแตกไฟล์ เปิด PowerShell ที่โฟลเดอร์โปรเจกต์
6. รัน `py -3 -m http.server 8000` แล้วเปิด `http://localhost:8000/` (หรือดับเบิลคลิก `index.html` เพื่อดู UI เบื้องต้น)
7. กด `Ctrl + Shift + R` เพื่อให้ Chrome โหลด CSS/JS ล่าสุด

## ทดสอบการใช้งาน

- Desktop/Notebook: Sidebar อ่านง่าย, Input และ Dropdown ประมาณ 16px, ตารางยังกรอกได้
- Tablet: `☰ หมวดข้อมูล` เปิด/ปิดเมนูได้, คลิกพื้นหลังหรือ Escape เพื่อปิด, เปลี่ยนหมวดแล้วเมนูปิดเอง
- Smartphone: Chrome F12 → Ctrl+Shift+M → 390x844 / 375x812; ตารางเป็นการ์ดมี Label ครบและไม่มีการเลื่อนหน้าทั้งหน้าในแนวนอน
- ทุกขนาดหน้าจอ: Sticky Footer มีปุ่ม `บันทึก JSON` และใช้งานได้
- เปิด JSON รายวิชาเดิมแล้วตรวจข้อมูล CLO, Lecture, Lab, Assessments, Resources; บันทึกใหม่และเปิดกลับมาอีกครั้ง
- ตรวจว่า **ไม่มีปุ่มสร้างใหม่, ไม่มีปุ่มตรวจสอบข้อมูล และไม่มี Auto Save** ตาม v1.4.2

## สำหรับผู้พัฒนา (เลือกทำ)

```powershell
py -3 tools/build.py
py -3 tools/test_json_only.py
py -3 tools/test_dropdown_roundtrip.py
py -3 tools/test_ui_v143.py
py -3 tools/test_responsive_v143.py
```

ชุดทดสอบ Browser ต้องติดตั้ง Playwright/Chromium และ `jsonschema` ในเครื่องนักพัฒนา แต่ผู้ใช้งานทั่วไปไม่ต้องติดตั้งอะไร

**ยังไม่ต้อง Merge เข้า main** จนกว่าจะตรวจ Responsive บนอุปกรณ์ที่ใช้งานจริงและพอใจกับขนาดตัวอักษรแล้ว
