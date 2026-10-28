"""Headless smoke tests using Playwright (not required by end users)."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(accept_downloads=True,viewport={'width':1440,'height':900},device_scale_factor=1)
 page=context.new_page()
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 # This environment blocks network/file navigation from automated browsers.
 # set_content tests the same self-contained HTML/JS without external URLs.
 page.set_content((ROOT/'index.html').read_text(encoding='utf8'),wait_until='load')
 page.wait_for_timeout(700)
 assert page.title().startswith('Smart Syllabus Generator')
 assert page.locator('#nav button').count()==6
 assert page.locator('#s-instructors').inner_text()=='0'
 page.screenshot(path=str(ROOT/'sample/Syllabus_Web_Desktop.png'),full_page=True)
 page.get_by_role('button',name='ตรวจสอบ').click()
 page.wait_for_timeout(150)
 assert 'ข้อผิดพลาด' in page.locator('#issue-heading').inner_text()
 page.on('dialog',lambda dialog:dialog.accept())
 page.get_by_role('button',name='ข้อมูลตัวอย่าง').click()
 page.wait_for_timeout(450)
 print('offering',page.locator('#offering-label').inner_text())
 assert page.locator('#offering-label').inner_text()=='244442-1-2569-SEC01'
 assert page.locator('#s-instructors').inner_text()=='1'
 page.get_by_role('button',name='ตรวจสอบ').click()
 print('validation:',page.locator('#issue-heading').inner_text())
 assert '0 ข้อผิดพลาด' in page.locator('#issue-heading').inner_text()
 with page.expect_download() as download_info:
  page.get_by_role('button',name='ส่งออก JSON').click()
 download=download_info.value
 assert download.suggested_filename=='244442-1-2569-SEC01.json',download.suggested_filename
 dest=ROOT/'sample/Exported_From_Browser_Demo.json'
 download.save_as(str(dest))
 data=json.loads(dest.read_text(encoding='utf8'))
 schema=json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text(encoding='utf8'))
 violations=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(data))
 print('Schema validation errors:',[x.message for x in violations])
 assert not violations
 # Add a new empty instructor row then verify validation triggers appropriately
 page.locator('#nav button[data-value="instructors"]').click()
 page.locator('button[data-action="add"][data-group="Instructors"]').click()
 assert page.locator('#group-Instructors tbody tr').count()==2
 page.locator('#group-Instructors button[data-action="delete"]').last.click()
 assert page.locator('#group-Instructors tbody tr').count()==1
 # ensure responsive nav available
 page.set_viewport_size({'width':390,'height':844})
 page.screenshot(path=str(ROOT/'sample/Syllabus_Web_Mobile.png'),full_page=True)
 assert page.locator('#nav button').count()==6
 assert not errors,errors
 print('PASS: 6 tabs, demo import, validation, JSON Schema, add/delete, responsive, no JS errors')
 browser.close()
