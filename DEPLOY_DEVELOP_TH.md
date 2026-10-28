# Deploy v1.4.0

1. แตก ZIP แล้วอัปโหลดไฟล์ `index.html`, `src/app.js`, `tools/build.py` ไปยัง `develop` ในตำแหน่งเดิม
2. Commit: `Switch to JSON-only save and reload v1.4`
3. ทดสอบ Localhost ผ่าน `py -3 -m http.server 8000` ใน root ของโฟลเดอร์
4. เปิด `http://localhost:8000/` (ตรวจว่า UI บอก v1.4.0)
5. ทดสอบบันทึก JSON ที่ไม่ครบ, โหลดกลับ, แก้, ตรวจสอบ, บันทึก, และเปิดหลัง Refresh
6. ยังไม่ต้อง Merge เข้า main

