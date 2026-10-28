# Changelog: v2.0.0 (Phase 2)

- เพิ่ม Client-side DOCX Export แบบ Standalone ไม่ใช้ Server และไม่มี CDN
- เพิ่มปุ่มสร้าง DOCX ใน Sticky Footer ของทุกหมวด พร้อมรักษาปุ่ม JSON เดิม
- Generate Word จากข้อมูล 6 หมวด และจาก JSON ที่เปิดเข้ามา
- DOCX ใช้ A4 ตารางตามหมวด พร้อมฟอนต์ชื่อ TH Sarabun New
- เอกสารที่มีข้อมูลส่วนหัวไม่ครบจะแสดงสถานะฉบับร่าง
- ปรับข้อความ Toast ไม่ให้บังปุ่มบนมือถือ
- คง JSON Schema v1.0.0 และการทำงาน JSON-only/Responsive v1.4.3
- ชุดทดสอบเพิ่มเติม: Browser → Download DOCX → ZIP/XML check, JSON roundtrip และ Responsive
