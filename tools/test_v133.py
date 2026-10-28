"""Browser regression checks using bundled HTML and storage emulation.
Localhost cannot be navigated to in this sandbox; real refresh is user acceptance test.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf8')
SCHEMA=json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text(encoding='utf8'))

def open_browser_page(ctx,storage_json=None):
    page=ctx.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('dialog',lambda d:d.accept())
    page.evaluate('''storage_json => {
      const items={}; if(storage_json!==null)items['up-syllabus-drafts-v1']=storage_json;
      Object.defineProperty(window,'indexedDB',{configurable:true,value:undefined});
      Object.defineProperty(window,'localStorage',{configurable:true,value:{
        getItem(k){return Object.prototype.hasOwnProperty.call(items,k)?items[k]:null;},
        setItem(k,v){items[k]=String(v)},removeItem(k){delete items[k]},clear(){Object.keys(items).forEach(k=>delete items[k])}
      }});
    }''',storage_json)
    page.set_content(HTML,wait_until='load');page.wait_for_selector('#f-CourseInfo-AcademicYear')
    return page,errors

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    ctx=browser.new_context(accept_downloads=True,viewport={'width':1440,'height':900})
    ctx.set_default_timeout(4000)
    print('start blank',flush=True)
    page,errors=open_browser_page(ctx)
    print('loaded blank',flush=True)
    assert page.locator('.brand-small').inner_text().endswith('v1.3.3')
    assert page.locator('#f-CourseInfo-AcademicYear').input_value()==''
    assert page.locator('#f-CourseInfo-Semester').input_value()==''
    assert page.locator('#f-CourseInfo-AcademicYear').get_attribute('autocomplete')=='off'
    print('go instructors',flush=True)
    page.locator('nav#nav [data-value="instructors"]').click()
    assert page.locator('table.instructor-editor tbody .row-no').count()==0
    assert 'ยังไม่มีผู้สอน' in page.locator('table.instructor-editor').inner_text()
    page.locator('button[data-action="add"][data-group="Instructors"]').click()
    assert page.locator('table.instructor-editor tbody .row-no').count()==1
    selector=page.locator('[data-action="instructor-select"]');opt=selector.locator('option').evaluate_all("a=>a.find(x=>x.textContent.includes('ปิยชนน์'))?.value")
    selector.select_option(opt)
    page.locator('table.instructor-editor input[data-key="IsResponsibleInstructor"]').check()
    print('go assessment',flush=True)
    page.locator('nav#nav [data-value="assessment"]').click()
    assert page.locator('.table-Resources tbody .row-no').count()==1
    assert page.evaluate('!!document.querySelector(\'#choices-Resources-0-ResourceType option[value="กำหนดเอง"]\')')
    resource=page.locator('input[data-key="ResourceType"]')
    resource.fill('กำหนดเอง'); assert resource.input_value()==''
    assert resource.get_attribute('placeholder')=='ระบุประเภทแหล่งเรียนรู้เอง'
    resource.fill('แหล่งเรียนรู้ภายนอกคณะ');page.locator('textarea[data-key="Title"]').fill('เอกสารทดสอบ')
    page.locator('button[data-action="save"]').click()
    page.wait_for_timeout(200)
    snapshot=page.evaluate('localStorage.getItem("up-syllabus-drafts-v1")')
    assert snapshot and 'แหล่งเรียนรู้ภายนอกคณะ' in snapshot
    # Simulate a new page session with the same saved draft.
    print('resume',flush=True)
    resumed,errors_resumed=open_browser_page(ctx,snapshot)
    assert resumed.locator('#f-CourseInfo-AcademicYear').input_value()==''
    assert resumed.locator('#f-CourseInfo-Semester').input_value()==''
    resumed.locator('nav#nav [data-value="instructors"]').click()
    assert resumed.locator('table.instructor-editor tbody .row-no').count()==1
    resumed.locator('nav#nav [data-value="assessment"]').click()
    assert resumed.locator('input[data-key="ResourceType"]').input_value()=='แหล่งเรียนรู้ภายนอกคณะ'
    # Restore legacy Draft with false defaults and phantom empty staff rows.
    demo=json.loads((ROOT/'sample/Smart_Syllabus_Demo.json').read_text(encoding='utf8'))
    demo['CourseInfo']['AcademicYear']=1;demo['CourseInfo']['Semester']='0'
    demo['Instructors']=[{},demo['Instructors'][0],{}]
    old_store=json.dumps([{'id':'old','updatedAt':'2026-10-28T00:00:00Z','name':'Legacy','data':demo}],ensure_ascii=False)
    print('legacy',flush=True)
    legacy,errors_legacy=open_browser_page(ctx,old_store)
    assert legacy.locator('#f-CourseInfo-AcademicYear').input_value()==''
    assert legacy.locator('#f-CourseInfo-Semester').input_value()==''
    legacy.locator('nav#nav [data-value="instructors"]').click()
    assert legacy.locator('table.instructor-editor tbody .row-no').count()==1
    assert 'ปิยชนน์' in legacy.locator('table.instructor-editor').inner_text()
    # Valid saved term should not be erased.
    demo['CourseInfo']['AcademicYear']=2569;demo['CourseInfo']['Semester']='1'
    valid_store=json.dumps([{'id':'good','updatedAt':'2026-10-28T00:00:00Z','name':'Valid','data':demo}],ensure_ascii=False)
    print('valid',flush=True)
    valid,errors_valid=open_browser_page(ctx,valid_store)
    assert valid.locator('#f-CourseInfo-AcademicYear').input_value()=='2569'
    assert valid.locator('#f-CourseInfo-Semester').input_value()=='1'
    valid.locator('nav#nav [data-value="instructors"]').click()
    assert valid.locator('table.instructor-editor tbody .row-no').count()==1
    # Export valid sample and confirm schema/regression.
    print('new demo',flush=True)
    page2,err2=open_browser_page(ctx)
    page2.locator('details#tools-menu summary').click()
    page2.locator('[data-action="demo"]').click()
    page2.locator('[data-action="validate"]').click()
    assert '0 ข้อผิดพลาด' in page2.locator('#issue-heading').inner_text(),page2.locator('#issue-list').inner_text()
    with page2.expect_download() as d: page2.locator('[data-action="export"]').click()
    output_path=ROOT/'sample'/'UI_v1_3_3_export.json';d.value.save_as(output_path)
    exported=json.loads(output_path.read_text(encoding='utf8'))
    errs=list(Draft202012Validator(SCHEMA).iter_errors(exported));assert not errs,errs
    assert exported['CourseInfo']['AcademicYear']==2569
    assert not(errors+errors_resumed+errors_legacy+errors_valid+err2),(errors,errors_resumed,errors_legacy,errors_valid,err2)
    print('PASS v1.3.3: new year/semester empty; no initial instructor row; add and save teacher; custom resource choice; Draft restore simulated; sanitize old 1/0/blank rows; retain valid old values; JSON validates; no browser JS errors')
    browser.close()
