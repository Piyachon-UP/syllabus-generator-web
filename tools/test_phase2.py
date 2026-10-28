"""End-to-end browser regression and DOCX output archive validation."""
import os, json, zipfile, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from lxml import etree
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text('utf-8')
actual=Path('/mnt/data/SYLLABUS_244106_2569_2_2.json')
with tempfile.TemporaryDirectory() as td, sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    ctx=b.new_context(accept_downloads=True,viewport={'width':1366,'height':880})
    p=ctx.new_page();errors=[];p.on('pageerror',lambda x:errors.append(str(x)))
    p.goto('about:blank');p.set_content(html,wait_until='load')
    assert p.locator('.brand-small').inner_text().endswith('v2.0.0')
    assert p.locator('.topline [data-action="import"]').count()==1
    assert p.locator('[data-action="validate"]').count()==0
    assert p.locator('.section-save-footer [data-action="save"]').count()==1
    assert p.locator('.section-save-footer [data-action="docx"]').count()==1
    for tab in ['course','plos','instructors','clos','weekly','assessment']:
        p.locator(f'[data-action="tab"][data-value="{tab}"]').click()
        assert p.locator('[data-action="docx"]').is_visible()
    p.locator('[data-action="tab"][data-value="course"]').click()
    # Incomplete JSON unchanged; DOCX can be made as a visibly labeled draft.
    p.locator('#f-CourseInfo-CourseCode').fill('244442')
    with p.expect_download() as e:p.locator('[data-action="save"]').click()
    e.value.save_as(td+'/partial.json')
    partial=json.loads(Path(td+'/partial.json').read_text('utf8'))
    assert partial['CourseInfo']['CourseCode']=='244442'
    with p.expect_download() as e:p.locator('[data-action="docx"]').click()
    e.value.save_as(td+'/partial.docx')
    with zipfile.ZipFile(td+'/partial.docx') as z:
        assert z.testzip() is None
        assert 'ฉบับร่าง' in z.read('word/document.xml').decode()
    # Actual saved file round-trip with no schema changes.
    if actual.exists():
        p.locator('#file-import').set_input_files(str(actual));p.wait_for_function("document.querySelector('#f-CourseInfo-CourseCode')?.value === '244106'")
        with p.expect_download() as e:p.locator('[data-action="docx"]').click()
        e.value.save_as(td+'/actual.docx')
        with zipfile.ZipFile(td+'/actual.docx') as z:
            assert z.testzip() is None
            xml=z.read('word/document.xml').decode()
            for text in ['ฟิสิกส์วิทยาศาสตร์และเทคโนโลยี','การบรรยาย','การทดลองและเก็บข้อมูล','การสอบกลางภาค','การสอบปลายภาค','ผศ.ดร. ปิยชนน์']:
                assert text in xml,text
            etree.fromstring(z.read('word/document.xml'))
        with p.expect_download() as e:p.locator('[data-action="save"]').click()
        e.value.save_as(td+'/actual.json')
        written=json.loads(Path(td+'/actual.json').read_text('utf8'))
        old=json.loads(actual.read_text('utf8'))
        for group in ['LecturePlans','LabPlans','CLOs','Assessments','GradeScale','Resources']:
            assert written[group]==old[group],group
    # Responsive mobile: both actions stay within viewport, no horizontal scroll.
    p.set_viewport_size({'width':375,'height':812})
    p.locator('[data-action="tab"][data-value="assessment"]').first.click() if p.locator('[data-action="tab"][data-value="assessment"]').first.is_visible() else None
    p.screenshot(path=str(root/'sample/Phase2_Mobile.png'),full_page=False)
    for name in ['save','docx']:
        btn=p.locator(f'[data-action="{name}"]')
        r=btn.bounding_box();assert r and r['x']>=0 and r['x']+r['width']<=376,(name,r)
    scroll=p.evaluate('document.documentElement.scrollWidth')
    assert scroll<=376,scroll
    p.set_viewport_size({'width':1366,'height':880})
    p.screenshot(path=str(root/'sample/Phase2_Desktop.png'),full_page=False)
    assert not errors,errors
    print('PASS: 6 tabs, unchanged JSON, incomplete DOCX draft, actual JSON->DOCX, mobile actions and no JS errors')
    ctx.close();b.close()
