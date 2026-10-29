"""Regression: optional manual calendar date, JSON round trip and browser-only DOCX."""
from __future__ import annotations
import json, tempfile, zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from lxml import etree
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'index.html'
SCHEMA=json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text('utf-8'))
ORIGINAL=Path('/mnt/data/SYLLABUS_244106_2569_2_2.json')
with tempfile.TemporaryDirectory() as td, sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    ctx=browser.new_context(accept_downloads=True, viewport={'width':1366,'height':880},locale='th-TH')
    page=ctx.new_page();errors=[]
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto('about:blank');page.set_content(APP.read_text('utf-8'),wait_until='load')
    assert page.locator('.brand-small').inner_text().endswith('v2.1.0')
    date=page.locator('#f-CourseInfo-LastUpdatedDate')
    assert date.count()==1 and date.get_attribute('type')=='date'
    assert date.input_value()==''
    assert page.locator('label[for="f-CourseInfo-LastUpdatedDate"]').inner_text()=='วันที่บันทึก/ปรับปรุงข้อมูล'
    assert page.locator('[data-action="import"]').count()==1
    assert page.locator('[data-action="save"]').count()==1
    assert page.locator('[data-action="docx"]').count()==1
    # Native date picker is available and acts on the original input.
    assert page.evaluate("typeof document.querySelector('#f-CourseInfo-LastUpdatedDate').showPicker")=='function'
    date.fill('2026-10-29');date.dispatch_event('change')
    assert date.input_value()=='2026-10-29'
    with page.expect_download() as dl:page.locator('[data-action="save"]').click()
    dl.value.save_as(td+'/new-partial.json')
    partial=json.loads(Path(td+'/new-partial.json').read_text('utf-8'))
    assert partial['CourseInfo']['LastUpdatedDate']=='2026-10-29'
    # An incomplete draft still downloads, and can be imported again.
    page.close();page=ctx.new_page();page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto('about:blank');page.set_content(APP.read_text('utf-8'),wait_until='load')
    assert page.locator('#f-CourseInfo-LastUpdatedDate').input_value()==''
    page.locator('#file-import').set_input_files(td+'/new-partial.json')
    assert page.locator('#f-CourseInfo-LastUpdatedDate').input_value()=='2026-10-29'
    with page.expect_download() as dl:page.locator('[data-action="docx"]').click()
    dl.value.save_as(td+'/new.docx')
    with zipfile.ZipFile(td+'/new.docx') as z:
        assert z.testzip() is None
        xml=z.read('word/document.xml').decode('utf-8')
        assert 'วันที่บันทึก/ปรับปรุงข้อมูล' in xml and '29/10/2569' in xml
        etree.fromstring(z.read('word/document.xml'))
    # Old JSON imports with empty optional date; other fields unaffected.
    if ORIGINAL.exists():
        old=json.loads(ORIGINAL.read_text('utf-8'))
        assert 'LastUpdatedDate' not in old['CourseInfo']
        errs=list(Draft202012Validator(SCHEMA,format_checker=FormatChecker()).iter_errors(old))
        assert not errs,[(e.path,e.message) for e in errs][:3]
        page.close();page=ctx.new_page();page.on('pageerror', lambda err: errors.append(str(err)))
        page.goto('about:blank');page.set_content(APP.read_text('utf-8'),wait_until='load')
        page.locator('#file-import').set_input_files(str(ORIGINAL))
        assert page.locator('#f-CourseInfo-LastUpdatedDate').input_value()==''
        assert page.locator('#f-CourseInfo-CourseCode').input_value()=='244106'
        page.locator('#f-CourseInfo-LastUpdatedDate').fill('2026-10-28')
        with page.expect_download() as dl:page.locator('[data-action="save"]').click()
        dl.value.save_as(td+'/updated.json')
        updated=json.loads(Path(td+'/updated.json').read_text('utf-8'))
        assert updated['CourseInfo']['LastUpdatedDate']=='2026-10-28'
        errs=list(Draft202012Validator(SCHEMA,format_checker=FormatChecker()).iter_errors(updated))
        assert not errs,[(e.path,e.message) for e in errs][:3]
        for group in ('PLOs','CLOs','Instructors','LecturePlans','LabPlans','Assessments','GradeScale','Resources'):
            assert updated[group]==old[group],group
    # Test other tabs, desktop + mobile, without unexpected horizontal overflow.
    for width in (1920,1366,1024,768,390,375):
        page.set_viewport_size({'width':width,'height':812})
        if width<=768:
            page.locator('[data-action="mobile-menu"]').click()
        assert page.locator('[data-action="save"]').is_visible()
        assert page.locator('[data-action="docx"]').is_visible()
        assert page.evaluate('document.documentElement.scrollWidth')<=width+1,(width,page.evaluate('document.documentElement.scrollWidth'))
        if width<=768:page.locator('[data-action="close-menu"]').first.click()
    page.set_viewport_size({'width':1366,'height':880})
    page.locator('[data-action="tab"][data-value="course"]').click()
    page.screenshot(path=str(ROOT/'sample'/'UI_v2_1_calendar_desktop.png'),full_page=False)
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(ROOT/'sample'/'UI_v2_1_calendar_mobile.png'),full_page=False)
    assert not errors,errors
    print('PASS: blank date, native date input, JSON save/load, old JSON, Thai DOCX date, schema, six screen widths')
    browser.close()
