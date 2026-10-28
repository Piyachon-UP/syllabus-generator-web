# อัปเดต v1.3.2 ไปยัง GitHub Branch develop

Repository: https://github.com/Piyachon-UP/syllabus-generator-web/tree/develop

1. **สำรอง Draft:** เปิดเว็บที่กำลังใช้งาน เลือก **เครื่องมือ → สำรอง Draft JSON** สำหรับงานที่กรอกไว้
2. ดาวน์โหลด `Smart_Syllabus_Generator_Web_UI_v1_3_2_Patch.zip` แล้วแตกไฟล์บน Windows
3. เข้า Repository และเลือก Branch **develop** (ไม่ใช่ main)
4. แทนที่ไฟล์ตามตำแหน่งเดิมด้วยไฟล์จาก ZIP:
   - `index.html`
   - `src/app.js`
   - `data/instructors.json`
   - `tools/build.py`
5. Commit ข้อความ `Refine blank starter rows and custom dropdowns v1.3.2`
6. ดาวน์โหลด ZIP จาก Branch develop เพื่อทดสอบในเครื่อง หรือใช้ GitHub Desktop เพื่อ Pull โค้ดใหม่
7. เปิด PowerShell ในโฟลเดอร์ที่แตก ZIP แล้วรัน `py -3 -m http.server 8000`
8. เปิด `http://localhost:8000/` และกด Ctrl+Shift+R
9. เลือก **เครื่องมือ → สร้าง Draft ใหม่** เพื่อทดสอบ ช่อง `AcademicYear` / `Semester` ต้องว่าง และแถวเปล่า 1 แถวในแท็บผู้สอน, CLOs, รายการประเมิน และแหล่งเรียนรู้
10. ตรวจ Dropdown วิธีสอนทั้ง Lecture / Lab และประเภทประเมิน ให้มี `กำหนดเอง` เลือกแล้วกรอกค่าอื่นได้

**ไม่ต้องแก้ Settings → Pages** และยังไม่ต้อง Merge `develop` ไป `main` เพราะหน้าเว็บ production ยังคง Deploy จาก `main`

## ทำไม Draft เดิมยังเห็นปี/ภาคเรียนเดิม?

แอป Auto Restore Draft ล่าสุดจาก IndexedDB หรือ localStorage การอัปเดตเว็บไซต์จะไม่ลบค่าที่กรอกไว้ หากต้องการทดสอบช่องเปล่าในเวอร์ชันนี้ ให้สำรอง JSON ก่อน แล้วใช้ **สร้าง Draft ใหม่**

## การอัปโหลดไฟล์ย่อยผ่าน GitHub Web

ต้องให้ path ของไฟล์ถูกต้อง: `src/app.js` อยู่ในโฟลเดอร์ `src`, `data/instructors.json` อยู่ใน `data`, `tools/build.py` อยู่ใน `tools`, และ `index.html` อยู่ที่ root ของ Repo หากหน้าเว็บแสดงเวอร์ชันเดิม ให้ตรวจว่าบันทึก Commit เข้า `develop` ถูก Branch และลองรีเฟรชแบบไม่ใช้ Cache

## การตรวจสอบหลังอัปเดต

- ช่องปีและภาคเรียนว่างเมื่อกดสร้าง Draft ใหม่
- ผู้สอนเคมี: ผกาสุคนธ์เป็นคนสุดท้ายของกลุ่ม
- ฟอร์มผู้สอน/CLO/Assessments/Resources มีแถวเริ่มต้นอย่างละ 1 แถว
- เปลี่ยนเป็นกำหนดเองแล้วพิมพ์ค่าอื่นได้
- ป้อนข้อมูลทดสอบให้ครบ, ตรวจสอบ, ส่งออก JSON, นำเข้า JSON กลับได้
