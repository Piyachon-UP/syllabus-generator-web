"""Rebuild standalone GitHub Pages index.html from local CSS/JS + canonical JSON."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
css=(root/'src/styles.css').read_text(encoding='utf8')
js=(root/'src/app.js').read_text(encoding='utf8')
docxjs=(root/'src/docx_export.js').read_text(encoding='utf8')
contract=(root/'schema/syllabus.v1.schema.json').read_text(encoding='utf8')
demo=(root/'sample/Smart_Syllabus_Demo.json').read_text(encoding='utf8')
curricula=(root/'data/curriculum_plos.json').read_text(encoding='utf8')
instructors=(root/'data/instructors.json').read_text(encoding='utf8')
# Keep data in script tags without introducing HTML closing-tag sequences.
def script_json(value):
    return json.dumps(json.loads(value),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
page=r'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#102c4a">
<meta name="description" content="Smart Syllabus Generator — ออกแบบ Course Syllabus พร้อมเปิดและบันทึก JSON ใน Browser">
<title>Smart Syllabus Generator | Faculty of Science UP</title>
<style>
__CSS__
</style>
</head>
<body>
<div class="app">
<aside class="sidebar" id="sidebar" aria-label="เมนูหมวดข้อมูล">
  <button type="button" class="sidebar-close" data-action="close-menu" aria-label="ปิดเมนูหมวดข้อมูล">✕ ปิดเมนู</button>
  <div class="brand"><div class="brand-mark">∑</div><div><div class="brand-title">SYLLABUS</div><div class="brand-small">GENERATOR · WEB v2.0.0</div></div></div>
  <div><div class="sidebar-label">WORKSPACE</div><nav class="nav" id="nav" aria-label="เมนูกรอกข้อมูล"></nav></div>
  <div class="sidebar-bottom"><span class="dot"></span>ทำงานในเครื่องของผู้ใช้งาน<br>Faculty of Science · University of Phayao<br>JSON Contract 1.0.0</div>
</aside>
<div class="sidebar-backdrop" data-action="close-menu" aria-hidden="true"></div>
<main class="main">
 <div class="topline">
  <button id="mobile-menu-button" class="btn mobile-menu-button" data-action="mobile-menu" type="button" aria-controls="sidebar" aria-expanded="false">☰ หมวดข้อมูล</button>
  <div class="header-group"><div class="eyebrow">ACADEMIC TOOLS / COURSE PLANNING</div><h1>Smart Syllabus Generator</h1><p class="header-desc">ระบบจัดทำรายละเอียดรายวิชาออนไลน์ · ประมวลผลใน Browser ไม่ใช้ Backend</p></div>
  <div class="actions" role="group" aria-label="เครื่องมือจัดการไฟล์ JSON">
    <button type="button" class="btn" data-action="import">⇧ เปิด JSON</button>
  </div> </div>
 <div class="pagebar"><div><div class="eyebrow" id="tab-number">SECTION 1 / 6</div><h2 id="tab-title">ข้อมูลรายวิชา</h2><p class="intro" id="tab-desc">ข้อมูลรายวิชา</p></div></div>
 <div id="panel-content" aria-live="polite"></div>
 <div class="section-save-footer" role="region" aria-label="บันทึกไฟล์ข้อมูลรายวิชา">
   <div class="section-save-copy"><span class="section-save-title">บันทึกข้อมูลทั้งหมด</span><span class="section-save-hint">บันทึก JSON หรือสร้างเอกสาร Word ได้ทุกเวลา · ไม่จำเป็นต้องตรวจสอบก่อน</span><span id="save-status" class="save-indicator" role="status" aria-live="polite">ยังไม่ได้บันทึก JSON</span></div>
   <div class="footer-action-buttons"><button type="button" class="btn section-save-button" data-action="save">⇩ บันทึก JSON</button><button type="button" class="btn btn-primary section-save-button" data-action="docx">▤ สร้าง DOCX</button></div>
 </div>
 <div class="footerline">© Faculty of Science, University of Phayao · Browser-only · <span id="storage-label">บันทึกเป็นไฟล์ JSON เท่านั้น</span> · ไม่อัปโหลดข้อมูลไปยัง Server</div>
</main>
</div>
<input id="file-import" class="hidden" type="file" accept=".json,application/json">
<div id="toast" class="toast hidden" role="status" aria-live="polite"></div>
<script type="application/json" id="contract-json">__CONTRACT__</script>
<script type="application/json" id="demo-json">__DEMO__</script>
<script type="application/json" id="curricula-json">__CURRICULA__</script>
<script type="application/json" id="instructors-json">__INSTRUCTORS__</script>
<script>
__DOCXJS__
</script>
<script>
__JS__
</script>
</body></html>
'''
page=page.replace('__CSS__',css).replace('__CONTRACT__',script_json(contract)).replace('__DEMO__',script_json(demo)).replace('__CURRICULA__',script_json(curricula)).replace('__INSTRUCTORS__',script_json(instructors)).replace('__JS__',js).replace('__DOCXJS__',docxjs)
(root/'index.html').write_text(page,encoding='utf8')
print('Wrote',root/'index.html','size',len(page.encode()))
