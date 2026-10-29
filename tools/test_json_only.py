"""Verify JSON-only v1.4.3 save/reload, incomplete file round-trip, course reuse, and no browser storage."""
from pathlib import Path
import json, tempfile
from jsonschema import Draft202012Validator
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf8')
SCHEMA=json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text(encoding='utf8'))
DEMO=json.loads((ROOT/'sample/Smart_Syllabus_Demo.json').read_text(encoding='utf8'))

def run():
  with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    ctx=b.new_context(accept_downloads=True,viewport={'width':1450,'height':920})
    p=ctx.new_page(); failures=[]
    p.on('pageerror',lambda e:failures.append(str(e)))
    p.on('dialog',lambda d:d.accept())
    p.goto('about:blank')
    p.set_content(HTML,wait_until='load')
    p.wait_for_selector('#f-CourseInfo-CourseCode')
    assert 'v2.1.0' in p.locator('.brand-small').inner_text()
    assert p.locator('[data-action="save"]').count()==1
    assert p.locator('[data-action="import"]').count()==1
    assert p.locator('[data-action="new"]').count()==0
    assert p.locator('[data-action="drafts"]').count()==0
    assert p.locator('[data-action="export"]').count()==0
    assert p.locator('#f-CourseInfo-AcademicYear').input_value()==''
    p.locator('#f-CourseInfo-CourseCode').fill('244442')
    assert 'ยังไม่ได้บันทึก' in p.locator('#save-status').inner_text()
    # Incomplete records must download (unlike v1.3.4 validated export).
    with p.expect_download() as info:p.locator('[data-action="save"]').click()
    dl=info.value
    assert dl.suggested_filename=='SYLLABUS_244442_YEAR_TERM_SECTION.json',dl.suggested_filename
    tmp=Path(tempfile.mkdtemp(prefix='syllabusv14_'))
    partial=tmp/'partial.json';dl.save_as(partial)
    data=json.loads(partial.read_text(encoding='utf8'))
    assert data['CourseInfo']['CourseCode']=='244442'
    assert not data['OfferingId']
    assert list(Draft202012Validator(SCHEMA).iter_errors(data)), 'Partial JSON should not claim to pass schema'
    # Import after fresh page; saved file is the only source of recovery.
    p.goto('about:blank')
    p.set_content(HTML,wait_until='load');p.wait_for_selector('#f-CourseInfo-CourseCode')
    assert p.locator('#f-CourseInfo-CourseCode').input_value()==''
    p.locator('#file-import').set_input_files(str(partial))
    assert p.locator('#f-CourseInfo-CourseCode').input_value()=='244442'
    assert p.locator('[data-action="validate"]').count()==0
    # Build a complete record by importing the old version's valid demo file.
    demo_path=tmp/'demo.json';demo_path.write_text(json.dumps(DEMO,ensure_ascii=False),encoding='utf8')
    p.locator('#file-import').set_input_files(str(demo_path))
    assert p.locator('#f-CourseInfo-AcademicYear').input_value()==str(DEMO['CourseInfo']['AcademicYear'])
    with p.expect_download() as info:p.locator('[data-action="save"]').click()
    good=tmp/'good.json';info.value.save_as(good)
    obj=json.loads(good.read_text(encoding='utf8'))
    assert list(Draft202012Validator(SCHEMA).iter_errors(obj))==[]
    assert obj['OfferingId']==DEMO['OfferingId']
    # New semester/reuse: make sure OfferingId changes with course values.
    p.locator('#f-CourseInfo-AcademicYear').fill('2570')
    p.locator('#f-CourseInfo-Semester').fill('2')
    with p.expect_download() as info:p.locator('[data-action="save"]').click()
    reused=tmp/'reused.json';info.value.save_as(reused)
    updated=json.loads(reused.read_text(encoding='utf8'))
    assert updated['OfferingId']=='244442-2-2570-SEC01',updated['OfferingId']
    assert updated['CLOs']==obj['CLOs']
    assert updated['LecturePlans']==obj['LecturePlans']
    assert list(Draft202012Validator(SCHEMA).iter_errors(updated))==[]
    # Verify the app does not silently write user drafts to either storage mechanism.
    assert 'localStorage.setItem(' not in (ROOT/'src/app.js').read_text(encoding='utf8')
    assert 'indexedDB.open(' not in (ROOT/'src/app.js').read_text(encoding='utf8')
    assert not failures,failures
    ctx.close();b.close()
  print('PASS v1.4.3 JSON-only: incomplete download and restore; validation independent; previous JSON compatible; year/semester reuse; full schema valid; no auto-storage')

if __name__=='__main__':run()
