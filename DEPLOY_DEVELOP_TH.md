# อัปเดต GitHub Branch develop — Phase 2 v2.0.0

Repository: `https://github.com/Piyachon-UP/syllabus-generator-web/tree/develop`

## ขั้นตอน

1. สำรอง JSON ของรายวิชาที่กำลังกรอกก่อนอัปเดต
2. ดาวน์โหลด `Smart_Syllabus_Generator_Web_Phase2_v2_0_Patch.zip` แล้วแตกไฟล์
3. เข้าหน้า Repository และเลือก Branch `develop`
4. อัปโหลดไฟล์จาก ZIP โดย **รักษาตำแหน่งเดิม**:
   - `index.html` — ทับไฟล์ที่ Root
   - `src/app.js` — ทับไฟล์เดิม
   - `src/docx_export.js` — **ไฟล์ใหม่**
   - `src/styles.css` — ทับไฟล์เดิม
   - `tools/build.py` — ทับไฟล์เดิม
   - `tools/test_phase2.py`, `tools/test_docx_node.cjs` — เพิ่มชุดทดสอบ
   - `README_TH.md`, `CHANGELOG_TH.md`, `DEPLOY_DEVELOP_TH.md` — คู่มือ
5. Commit message: `Add browser-only DOCX export Phase 2 v2.0.0`
6. ดาวน์โหลด ZIP ของ Branch `develop` ลง Windows และแตกไฟล์
7. เปิด `index.html` หรือใช้ `py -3 -m http.server 8000` แล้วเปิด `http://localhost:8000/`
8. ทดสอบ **เปิด JSON** จากรายวิชา 244106 หรือข้อมูลอื่นที่สำรองไว้ จากนั้นกด **สร้าง DOCX** แล้วเปิดใน Word
9. ทดสอบบันทึก JSON กลับมาเทียบกับไฟล์เดิม และตรวจปุ่ม DOCX บน Desktop/Tablet/Mobile
10. หากพอใจแล้วจึง Pull Request `develop` → `main` เพื่อเผยแพร่ GitHub Pages

## สิ่งที่ต้องตรวจ

- แถบบนยังมีเฉพาะ **เปิด JSON** ไม่เพิ่มปุ่มตรวจสอบหรือสร้างใหม่
- Sticky Footer มี **บันทึก JSON** และ **สร้าง DOCX**
- Word แสดงภาษาไทยได้ไม่กลายเป็นอักขระผิดเพี้ยน
- Word มีตาราง Lecture และ Lab, CLO/PLO, เกณฑ์เกรดและแหล่งเรียนรู้
- JSON Schema v1.0.0 เดิมและการบันทึก JSON ข้อมูลไม่ครบยังทำงาน
- แสดงผลพอดีบนหน้าจอเล็ก

**สำคัญ:** ไม่ต้องอัปโหลดไฟล์ JSON ของรายวิชาจริงหรือ DOCX ที่มีข้อมูลจริงเข้า Public GitHub Repository; ให้เก็บไว้ในเครื่องผู้สอน
