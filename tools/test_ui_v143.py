"""Browser regression for static JSON-only v1.4.3.

Developer-only: python tools/test_ui_v142.py
Requires python packages playwright and jsonschema plus local Chromium.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
from jsonschema import Draft202012Validator
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT/'index.html').read_text(encoding='utf-8')
SCHEMA = json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text(encoding='utf-8'))
EXAMPLE = json.loads((ROOT/'sample/Smart_Syllabus_Demo.json').read_text(encoding='utf-8'))
ACTUAL = Path(os.environ.get('SYLLABUS_TEST_JSON', '/mnt/data/SYLLABUS_244106_2569_2_2.json'))

with TemporaryDirectory() as tmpdir, sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'), args=['--no-sandbox'])
    context = browser.new_context(accept_downloads=True, viewport={'width':1400,'height':850})
    page = context.new_page()
    js_errors=[]
    page.on('pageerror', lambda err: js_errors.append(str(err)))
    page.on('dialog', lambda dialog:dialog.accept())
    page.goto('about:blank')
    page.set_content(HTML, wait_until='load')
    assert 'v2.1.0' in page.locator('.brand-small').inner_text()
    assert page.locator('.topline [data-action="import"]').count() == 1
    assert page.locator('.topline [data-action="import"]').count() == 1
    assert page.locator('.topline [data-action="mobile-menu"]').count() == 1
    assert page.locator('[data-action="new"]').count() == 0
    assert page.locator('[data-action="validate"]').count() == 0
    assert page.locator('.section-save-footer [data-action="save"]').count() == 1
    assert page.locator('[data-action="save"]').count() == 1
    assert page.locator('#f-CourseInfo-CourseCode').input_value() == ''
    assert page.locator('.section-save-footer').evaluate('(el)=>getComputedStyle(el).position') == 'sticky'
    # Sticky footer stays in the visual viewport at the start and after switching tabs.
    def check_footer():
        assert page.locator('.section-save-footer').is_visible()
        rect=page.locator('.section-save-footer').bounding_box()
        assert rect and rect['y'] >= 0 and rect['y'] + rect['height'] <= 855,rect
    check_footer()
    for name in ['plos','instructors','clos','weekly','assessment','course']:
        page.locator('[data-action="tab"][data-value="'+name+'"]').click()
        check_footer()
    # Incomplete information is still downloadable with no validator action.
    page.locator('#f-CourseInfo-CourseCode').fill('244442')
    with page.expect_download() as event:
        page.locator('.section-save-footer [data-action="save"]').click()
    partial_path = Path(tmpdir)/'partial.json'
    event.value.save_as(str(partial_path))
    partial = json.loads(partial_path.read_text(encoding='utf-8'))
    assert partial['CourseInfo']['CourseCode']=='244442'
    assert partial['SchemaVersion']=='1.0.0'
    assert list(Draft202012Validator(SCHEMA).iter_errors(partial)), 'Incomplete data must not pretend to be fully valid'
    # Reload and reopen partial data file.
    page.goto('about:blank')
    page.set_content(HTML, wait_until='load')
    assert page.locator('#f-CourseInfo-CourseCode').input_value()==''
    page.locator('#file-import').set_input_files(str(partial_path))
    page.wait_for_function("document.querySelector('#f-CourseInfo-CourseCode')?.value === '244442'")
    # Complete original JSON still meets the same schema and rounds back without modification.
    example_path = Path(tmpdir)/'example.json'
    example_path.write_text(json.dumps(EXAMPLE,ensure_ascii=False),encoding='utf-8')
    page.locator('#file-import').set_input_files(str(example_path))
    page.wait_for_function("document.querySelector('#f-CourseInfo-CourseCode')?.value === '244442' && document.querySelector('#save-status')?.textContent.includes('เปิดไฟล์')")
    with page.expect_download() as event:
        page.locator('.section-save-footer [data-action="save"]').click()
    full_path = Path(tmpdir)/'full.json'
    event.value.save_as(str(full_path))
    full = json.loads(full_path.read_text(encoding='utf-8'))
    assert not list(Draft202012Validator(SCHEMA).iter_errors(full))
    assert full['CLOs'] == EXAMPLE['CLOs']
    assert full['LecturePlans'] == EXAMPLE['LecturePlans']
    assert full['LabPlans'] == EXAMPLE['LabPlans']
    assert full['Assessments'] == EXAMPLE['Assessments']
    # Full choice list after load, with requested additional type.
    page.locator('[data-action="tab"][data-value="assessment"]').click()
    options = page.locator('.table-Assessments select[data-action="choice-select"]').first.locator('option').all_text_contents()
    assert 'ปฏิบัติการ' in options
    assert 'กำหนดเอง' in options
    # Confirm the requested value persists and is not a sentinel.
    page.locator('.table-Assessments select[data-action="choice-select"]').first.select_option('ปฏิบัติการ')
    with page.expect_download() as event:
        page.locator('[data-action="save"]').click()
    updated_path=Path(tmpdir)/'assessment.json'
    event.value.save_as(str(updated_path))
    updated=json.loads(updated_path.read_text(encoding='utf-8'))
    assert updated['Assessments'][0]['AssessmentType']=='ปฏิบัติการ'
    page.goto('about:blank')
    page.set_content(HTML, wait_until='load')
    page.locator('#file-import').set_input_files(str(updated_path))
    page.wait_for_function("document.querySelector('#save-status')?.textContent.includes('เปิดไฟล์')")
    page.locator('[data-action="tab"][data-value="assessment"]').click()
    assert page.locator('.table-Assessments select[data-action="choice-select"]').first.input_value() == 'ปฏิบัติการ'
    # User-uploaded syllabus regression if file available.
    if ACTUAL.exists():
        before = json.loads(ACTUAL.read_text(encoding='utf-8'))
        page.locator('#file-import').set_input_files(str(ACTUAL))
        page.wait_for_function("document.querySelector('#f-CourseInfo-CourseCode')?.value === '244106'")
        with page.expect_download() as event:
            page.locator('[data-action="save"]').click()
        actual_out=Path(tmpdir)/'user.json';event.value.save_as(str(actual_out))
        after=json.loads(actual_out.read_text(encoding='utf-8'))
        for group in ('LecturePlans','LabPlans','Assessments','Resources','PLOs','CLOs'):
            assert after[group] == before[group],group
    # Mobile sticky layout check.
    page.set_viewport_size({'width':390,'height':844})
    check_footer()
    assert not js_errors,js_errors
    print('PASS v1.4.3: only Open JSON at top; save sticky on 6 tabs; no New/Validation UI; incomplete + valid JSON save/reopen; extra assessment choice; original data preserved; mobile sticky')
    context.close();browser.close()
