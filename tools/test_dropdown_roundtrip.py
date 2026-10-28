"""End-to-end browser regression for v1.4.3 dropdowns.

Run: python tools/test_dropdown_roundtrip.py
Optional external JSON for local testing (never added to the repository):
  SYLLABUS_TEST_JSON=/absolute/path/syllabus.json python tools/test_dropdown_roundtrip.py
Requires Playwright + Chromium on the *developer's* machine, not end users.
"""
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
TEST_JSON=Path(os.environ.get('SYLLABUS_TEST_JSON', str(ROOT/'sample'/'Smart_Syllabus_Demo.json')))
REFERENCE=json.loads(TEST_JSON.read_text(encoding='utf-8'))

def check_options(locator, expected_count, saved):
    assert locator.count()>0, 'Dropdown not rendered'
    items=locator.first.locator('option').all_text_contents()
    assert len(items)>=expected_count,(len(items),items)
    assert 'กำหนดเอง' in items
    expected=saved if saved in [x for x in items] else ('__custom__' if saved else '')
    assert locator.first.input_value()==expected,(locator.first.input_value(),expected)
    return len(items)

with TemporaryDirectory() as temp, sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1500,'height':900},accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    # Inline page content avoids environment-specific restrictions on file:// or localhost in headless CI.
    # The published artifact remains a normal standalone index.html.
    page.goto('about:blank')
    page.set_content((ROOT/'index.html').read_text(encoding='utf-8'),wait_until='load')
    page.locator('#file-import').set_input_files(str(TEST_JSON))
    page.wait_for_function("document.querySelector('#save-status')?.textContent.includes('เปิดไฟล์')")
    page.locator('[data-action="tab"][data-value="weekly"]').click()
    lec=page.locator('.table-LecturePlans select[data-action="choice-select"]')
    counts={}
    counts['lecture']=check_options(lec,17,REFERENCE['LecturePlans'][0]['TeachingMethods'])
    assert 'การเรียนรู้แบบใช้ปัญหาเป็นฐาน (PBL)' in lec.first.locator('option').all_text_contents()
    page.locator('[data-action="week-switch"][data-value="LabPlans"]').click()
    lab=page.locator('.table-LabPlans select[data-action="choice-select"]')
    counts['lab']=check_options(lab,17,REFERENCE['LabPlans'][0]['TeachingMethods'])
    page.locator('[data-action="tab"][data-value="assessment"]').click()
    assess=page.locator('.table-Assessments select[data-action="choice-select"]')
    counts['assessment']=check_options(assess,18,REFERENCE['Assessments'][0]['AssessmentType'])
    assert 'ปฏิบัติการ' in assess.first.locator('option').all_text_contents()
    resource=page.locator('.table-Resources select[data-action="choice-select"]')
    counts['resources']=check_options(resource,16,REFERENCE['Resources'][0]['ResourceType'])
    with page.expect_download() as d:page.locator('[data-action="save"]').click()
    output=Path(temp)/'syllabus-output.json'
    d.value.save_as(str(output))
    unchanged=json.loads(output.read_text(encoding='utf-8'))
    for group in ['LecturePlans','LabPlans','Assessments','Resources']:
        assert unchanged[group]==REFERENCE[group],f'Unexpected changes to imported {group}'
    # Choice change and custom-value lifecycle.
    page.locator('[data-action="tab"][data-value="weekly"]').click()
    page.locator('[data-action="week-switch"][data-value="LecturePlans"]').click()
    page.locator('.table-LecturePlans select[data-action="choice-select"]').first.select_option('การอภิปรายกลุ่ม')
    page.locator('.table-LecturePlans select[data-action="choice-select"]').nth(1).select_option('__custom__')
    page.locator('.table-LecturePlans input[data-action="choice-custom"]').nth(1).fill('การเรียนรู้ตามสถานการณ์เฉพาะ')
    page.locator('[data-action="tab"][data-value="assessment"]').click()
    page.locator('.table-Assessments select[data-action="choice-select"]').first.select_option('__custom__')
    page.locator('.table-Assessments input[data-action="choice-custom"]').first.fill('การประเมินแบบใหม่')
    page.locator('.table-Resources select[data-action="choice-select"]').first.select_option('__custom__')
    page.locator('.table-Resources input[data-action="choice-custom"]').first.fill('ฐานความรู้ชุมชน')
    with page.expect_download() as d:page.locator('[data-action="save"]').click()
    d.value.save_as(str(output))
    changed=json.loads(output.read_text(encoding='utf-8'))
    assert changed['LecturePlans'][0]['TeachingMethods']=='การอภิปรายกลุ่ม'
    assert changed['LecturePlans'][1]['TeachingMethods']=='การเรียนรู้ตามสถานการณ์เฉพาะ'
    assert changed['Assessments'][0]['AssessmentType']=='การประเมินแบบใหม่'
    assert changed['Resources'][0]['ResourceType']=='ฐานความรู้ชุมชน'
    # Reinitialize web page and re-import custom values.
    page.goto('about:blank')
    page.set_content((ROOT/'index.html').read_text(encoding='utf-8'),wait_until='load')
    page.locator('#file-import').set_input_files(str(output))
    page.wait_for_function("document.querySelector('#save-status')?.textContent.includes('เปิดไฟล์')")
    page.locator('[data-action="tab"][data-value="weekly"]').click()
    select=page.locator('.table-LecturePlans select[data-action="choice-select"]').nth(1)
    assert select.input_value()=='__custom__'
    assert page.locator('.table-LecturePlans input[data-action="choice-custom"]').nth(1).input_value()=='การเรียนรู้ตามสถานการณ์เฉพาะ'
    assert len(select.locator('option').all())>=17
    page.locator('[data-action="tab"][data-value="assessment"]').click()
    assert page.locator('.table-Assessments select[data-action="choice-select"]').first.input_value()=='__custom__'
    assert page.locator('.table-Resources select[data-action="choice-select"]').first.input_value()=='__custom__'
    assert not errors, errors
    print('PASS: complete dropdowns, import/export roundtrip unchanged, custom fields survive save/reload; no browser JS errors')
    print('Option counts (including custom and blank):',counts)
    browser.close()
