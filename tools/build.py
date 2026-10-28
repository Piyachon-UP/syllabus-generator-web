"""Rebuild standalone GitHub Pages index.html from local CSS/JS + canonical JSON."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
css=(root/'src/styles.css').read_text(encoding='utf8')
js=(root/'src/app.js').read_text(encoding='utf8')
contract=(root/'schema/syllabus.v1.schema.json').read_text(encoding='utf8')
demo=(root/'sample/Smart_Syllabus_Demo.json').read_text(encoding='utf8')
# Keep data in script tags without introducing HTML closing-tag sequences.
def script_json(value):
    return json.dumps(json.loads(value),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
page=r'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#102c4a">
<meta name="description" content="Smart Syllabus Generator — ออกแบบ Course Syllabus พร้อมบันทึก Draft และส่งออก JSON ใน Browser">
<title>Smart Syllabus Generator | Faculty of Science UP</title>
<style>
__CSS__
</style>
</head>
<body>
<div class="app">
<aside class="sidebar">
  <div class="brand"><div class="brand-mark">∑</div><div><div class="brand-title">SYLLABUS</div><div class="brand-small">GENERATOR · WEB v1.0</div></div></div>
  <div><div class="sidebar-label">WORKSPACE</div><nav class="nav" id="nav" aria-label="เมนูกรอกข้อมูล"></nav></div>
  <div class="sidebar-bottom"><span class="dot"></span>ทำงานในเครื่องของผู้ใช้งาน<br>Faculty of Science · University of Phayao<br>JSON Contract 1.0.0</div>
</aside>
<main class="main">
 <div class="topline">
  <div><div class="eyebrow">ACADEMIC TOOLS / COURSE PLANNING</div><h1>Smart Syllabus Generator</h1><p class="header-desc">ระบบจัดทำรายละเอียดรายวิชาออนไลน์ · ประมวลผลใน Browser ไม่ใช้ Backend</p></div>
  <div class="actions">
    <button type="button" class="btn" data-action="drafts">▤ Draft ของฉัน</button>
    <button type="button" class="btn" data-action="new">＋ สร้างใหม่</button>
    <button type="button" class="btn" data-action="import">⇧ นำเข้า JSON</button>
    <button type="button" class="btn" data-action="backup">⇩ สำรอง Draft JSON</button>
    <button type="button" class="btn btn-navy" data-action="save">☑ บันทึก Draft</button>
  </div>
 </div>
 <div class="hero"><div><div class="meta">COURSE SYLLABUS · ACADEMIC YEAR</div><h2 id="hero-course">เริ่มต้นสร้าง Course Syllabus</h2><p class="sub" id="hero-sub">Faculty of Science · University of Phayao</p></div><div class="offering"><span>OFFERING ID (AUTO)</span><strong id="offering-label">—</strong><span>สำหรับนำเข้าระบบ Blazor ในอนาคต</span></div></div>
 <div class="stats"><div class="stat"><div><div class="hint">อาจารย์ผู้สอน</div><div class="number" id="s-instructors">0</div></div><div class="symbol">♙</div></div><div class="stat"><div><div class="hint">Course Learning Outcomes</div><div class="number" id="s-clos">0</div></div><div class="symbol">◎</div></div><div class="stat"><div><div class="hint">แผนสอน (รายการ)</div><div class="number" id="s-plans">0</div></div><div class="symbol">▦</div></div><div class="stat"><div><div class="hint">น้ำหนักคะแนนรวม</div><div class="number" id="s-weight">0%</div></div><div class="symbol">◫</div></div></div>
 <div class="pagebar"><div><div class="eyebrow" id="tab-number">SECTION 1 / 6</div><h2 id="tab-title">ข้อมูลรายวิชา</h2><p class="intro" id="tab-desc">ข้อมูลรายวิชา</p></div><div class="inline-row"><span class="pill neutral" id="save-status">กำลังโหลด...</span><button type="button" class="btn" data-action="demo">◈ ข้อมูลตัวอย่าง</button><button type="button" class="btn" data-action="validate">✓ ตรวจสอบ</button><button type="button" class="btn btn-primary" data-action="export">⇩ ส่งออก JSON</button></div></div>
 <div id="panel-content" aria-live="polite"></div>
 <section id="validation" class="validate-area" aria-live="polite"><div class="results-head"><h2 id="issue-heading">ผลตรวจสอบ</h2><span class="pill neutral">คลิกเพื่อไปยังแท็บที่เกี่ยวข้อง</span></div><div class="issues" id="issue-list"></div></section>
 <div class="footerline">© Faculty of Science, University of Phayao · Browser-only draft · Storage: <span id="storage-label">—</span> · ไม่อัปโหลดข้อมูลไปยัง Server</div>
</main>
</div>
<div id="drawer" class="drawer-back hidden"><div class="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-title"><div class="topline"><div><h2 id="drawer-title">Draft ที่บันทึกไว้</h2><p class="muted">เก็บใน Browser ของเครื่องและโปรไฟล์นี้เท่านั้น</p></div><button class="btn btn-mini" data-action="close-drawer" aria-label="ปิด">✕ ปิด</button></div><div class="notice warn" style="margin-top:20px">ข้อมูลนี้จะไม่ซิงก์ระหว่างอุปกรณ์ หากเปลี่ยนเครื่องหรือล้างข้อมูล Browser อาจสูญหาย กรุณา Export JSON เป็นระยะ</div><div id="draft-list"></div></div></div>
<input id="file-import" class="hidden" type="file" accept=".json,application/json">
<div id="toast" class="toast hidden" role="status" aria-live="polite"></div>
<script type="application/json" id="contract-json">__CONTRACT__</script>
<script type="application/json" id="demo-json">__DEMO__</script>
<script>
__JS__
</script>
</body></html>
'''
page=page.replace('__CSS__',css).replace('__CONTRACT__',script_json(contract)).replace('__DEMO__',script_json(demo)).replace('__JS__',js)
(root/'index.html').write_text(page,encoding='utf8')
print('Wrote',root/'index.html','size',len(page.encode()))
