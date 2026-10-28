"""Regression checks for v1.3.4; simulate persisted IndexedDB fallback on about:blank."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf8')
SCHEMA=json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text(encoding='utf8'))
DEMO=json.loads((ROOT/'sample/Smart_Syllabus_Demo.json').read_text(encoding='utf8'))

def open_page(ctx, persisted=None):
    page=ctx.new_page(); errors=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('dialog', lambda d: d.accept())
    page.evaluate('''saved => {
      const items = {};
      if(saved !== null)items['up-syllabus-drafts-v1'] = saved;
      Object.defineProperty(window, 'indexedDB', {configurable:true,value:undefined});
      Object.defineProperty(window, 'localStorage', {configurable:true,value:{
       getItem(k){return Object.prototype.hasOwnProperty.call(items,k)?items[k]:null},
       setItem(k,v){items[k]=String(v)},
       removeItem(k){delete items[k]},
       clear(){Object.keys(items).forEach(k=>delete items[k])}
      }});
    }''', persisted)
    page.set_content(HTML, wait_until='load')
    page.wait_for_selector('#f-CourseInfo-AcademicYear')
    return page,errors

def snapshot(page):
    return json.loads(page.evaluate('localStorage.getItem("up-syllabus-drafts-v1")') or '[]')

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    ctx=browser.new_context(accept_downloads=True,viewport={'width':1440,'height':900})
    ctx.set_default_timeout(8000)
    saved=json.dumps([{'id':'previous-course','updatedAt':'2026-10-28T08:00:00Z','name':'งานฟิสิกส์เดิม','data':DEMO}],ensure_ascii=False)
    pg, errors=open_page(ctx, saved)
    assert 'v1.3.4' in pg.locator('.brand-small').inner_text()
    assert pg.locator('#f-CourseInfo-AcademicYear').input_value()==''
    assert pg.locator('#f-CourseInfo-Semester').input_value()==''
    assert 'แบบฟอร์มใหม่ (ว่าง)' in pg.locator('#save-status').inner_text()
    pg.locator('nav#nav [data-value="instructors"]').click()
    assert pg.locator('table.instructor-editor tbody .row-no').count()==0
    assert 'ยังไม่มีผู้สอน' in pg.locator('table.instructor-editor').inner_text()
    assert len(snapshot(pg))==1, 'opening stored Drafts must not generate another blank Draft'
    pg.locator('[data-action="drafts"]').click()
    assert 'งานฟิสิกส์เดิม' in pg.locator('#draft-list').inner_text()
    pg.locator('#draft-list [data-action="load-draft"]').click()
    assert pg.locator('#f-CourseInfo-AcademicYear').input_value()=='2569'
    assert pg.locator('#f-CourseInfo-Semester').input_value()=='1'
    pg.locator('nav#nav [data-value="instructors"]').click()
    assert pg.locator('table.instructor-editor tbody .row-no').count()==len(DEMO['Instructors'])
    pg.locator('details#tools-menu summary').click()
    pg.locator('[data-action="new"]').click()
    assert pg.locator('#f-CourseInfo-AcademicYear').input_value()==''
    assert pg.locator('#f-CourseInfo-Semester').input_value()==''
    pg.locator('nav#nav [data-value="instructors"]').click()
    assert pg.locator('table.instructor-editor tbody .row-no').count()==0
    assert len(snapshot(pg))==1, 'new blank Draft should not overwrite saved data or save empty copies'
    pg.locator('nav#nav [data-value="course"]').click()
    pg.locator('#f-CourseInfo-CourseCode').fill('244442')
    pg.locator('[data-action="save"]').click()
    assert len(snapshot(pg))==2
    fresh, fresh_errors=open_page(ctx, json.dumps(snapshot(pg),ensure_ascii=False))
    assert fresh.locator('#f-CourseInfo-CourseCode').input_value()==''
    assert fresh.locator('#f-CourseInfo-Semester').input_value()==''
    fresh.locator('nav#nav [data-value="instructors"]').click()
    assert fresh.locator('table.instructor-editor tbody .row-no').count()==0
    fresh.locator('[data-action="drafts"]').click()
    assert len(fresh.locator('#draft-list .draft-item').all())==2
    # Demonstrate that old sentinel values are cleared only on explicit reload.
    legacy=json.loads(json.dumps(DEMO,ensure_ascii=False))
    legacy['CourseInfo']['AcademicYear']=1
    legacy['CourseInfo']['Semester']='0'
    legacy['Instructors']=[{}]
    legacy_stored=json.dumps([{'id':'old','name':'Legacy','updatedAt':'2026-10-27T01:00:00Z','data':legacy}],ensure_ascii=False)
    legacy_page, legacy_errors=open_page(ctx, legacy_stored)
    legacy_page.locator('[data-action="drafts"]').click()
    legacy_page.locator('#draft-list [data-action="load-draft"]').click()
    assert legacy_page.locator('#f-CourseInfo-AcademicYear').input_value()==''
    assert legacy_page.locator('#f-CourseInfo-Semester').input_value()==''
    legacy_page.locator('nav#nav [data-value="instructors"]').click()
    assert legacy_page.locator('table.instructor-editor tbody .row-no').count()==0
    # Existing complete demo should still validate / export identically after explicit loading.
    demo_page, demo_errors=open_page(ctx)
    demo_page.locator('details#tools-menu summary').click()
    demo_page.locator('[data-action="demo"]').click()
    demo_page.locator('[data-action="validate"]').click()
    assert '0 ข้อผิดพลาด' in demo_page.locator('#issue-heading').inner_text(), demo_page.locator('#issue-list').inner_text()
    with demo_page.expect_download() as dl: demo_page.locator('[data-action="export"]').click()
    output=ROOT/'sample'/'UI_v1_3_4_export.json'
    dl.value.save_as(output)
    data=json.loads(output.read_text(encoding='utf-8'))
    assert list(Draft202012Validator(SCHEMA).iter_errors(data))==[]
    assert not (errors+fresh_errors+legacy_errors+demo_errors), (errors,fresh_errors,legacy_errors,demo_errors)
    print('PASS v1.3.4: fresh blank year/term and no instructors even when saved draft exists; explicit restoration; no phantom blank drafts; safe Save/New; legacy sanitize; schema-valid export')
    browser.close()
