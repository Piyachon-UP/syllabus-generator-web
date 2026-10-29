import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'sample';out.mkdir(exist_ok=True)
source=ROOT/'sample/Smart_Syllabus_Demo.json'
errors=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h,label in [(1920,1080,'desktop'),(1366,900,'notebook'),(1024,900,'tablet'),(768,1024,'smalltablet'),(390,844,'mobile'),(375,812,'smallmobile')]:
  context=browser.new_context(viewport={'width':w,'height':h},device_scale_factor=1,accept_downloads=True)
  page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda dialog:dialog.accept())
  page.goto('about:blank'); page.set_content(ROOT.joinpath('index.html').read_text(encoding='utf8'),wait_until='load')
  page.wait_for_selector('#f-CourseInfo-CourseCode')
  assert 'v2.1.0' in page.locator('.brand-small').text_content()
  assert page.locator('[data-action="import"]').count()==1
  assert page.locator('[data-action="save"]').count()==1
  assert page.locator('[data-action="validate"]').count()==0
  assert page.locator('[data-action="new"]').count()==0
  if w<=1100:
   assert page.locator('#mobile-menu-button').is_visible(),label
   assert page.locator('#sidebar').get_attribute('inert') is not None,label
   page.locator('#mobile-menu-button').click()
   page.wait_for_timeout(240)
   assert page.locator('#sidebar').is_visible(),label
   assert page.locator('#mobile-menu-button').get_attribute('aria-expanded')=='true'
   page.locator('#nav [data-action="tab"][data-value="weekly"]').click()
   assert page.locator('#sidebar').get_attribute('inert') is not None
   assert page.locator('#tab-title').inner_text()=='แผนการสอน'
  else:
   assert not page.locator('#mobile-menu-button').is_visible()
   page.locator('#nav [data-action="tab"][data-value="weekly"]').click()
  page.locator('[data-action="fill-weeks"]').click()
  assert page.locator('.table-LecturePlans tbody tr').count()==15
  if w<=700:
   display=page.locator('.table-LecturePlans tbody tr').first.evaluate('(el)=>getComputedStyle(el).display')
   assert display=='block',(label,display)
   assert page.locator('.table-LecturePlans tbody tr td[data-label="วิธีสอน"]').count()==15
   assert page.locator('.table-LecturePlans tbody tr').first.locator('textarea').is_visible()
  else:
   assert page.locator('.table-LecturePlans').evaluate('(el)=>getComputedStyle(el).display')=='table'
  x=page.evaluate('document.documentElement.scrollWidth')
  print(f'{label}: {w}px viewport, {x}px document')
  if w<=700: assert x <= w+1,(label,x,w)
  foot=page.locator('.section-save-footer')
  assert foot.is_visible()
  page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
  br=foot.bounding_box()
  assert br and br['y'] >= -1 and br['y']+br['height'] <= h+2,(label,br)
  if label in ('desktop','tablet','mobile'):
   page.screenshot(path=str(out/f'UI_v1_4_3_{label}.png'),full_page=False)
  if label=='mobile':
   # import real JSON then select assessment and test card and dropdown
   page.locator('#file-import').set_input_files(str(source))
   page.wait_for_function("document.querySelector('#save-status')?.textContent.includes('เปิดไฟล์')")
   page.locator('#mobile-menu-button').click()
   page.locator('#nav [data-value="assessment"]').click()
   assert page.locator('.table-Assessments tbody tr').count()==len(json.loads(source.read_text('utf8'))['Assessments'])
   assert page.locator('.table-Assessments tbody tr td[data-label="ประเภทประเมิน"]').count()==len(json.loads(source.read_text('utf8'))['Assessments'])
   assert 'ปฏิบัติการ' in page.locator('.table-Assessments select[data-action="choice-select"]').first.locator('option').all_text_contents()
   page.screenshot(path=str(out/'UI_v1_4_3_mobile_assessment.png'))
   with page.expect_download() as ev: page.locator('[data-action="save"]').click()
   from tempfile import TemporaryDirectory
   with TemporaryDirectory() as tmp:
    path=Path(tmp)/'roundtrip.json';ev.value.save_as(str(path))
    result=json.loads(path.read_text('utf8'))
   orig=json.loads(source.read_text('utf8'))
   for k in ('LecturePlans','LabPlans','Assessments','Resources','CLOs'):
    assert result[k]==orig[k],k
   assert result['SchemaVersion']=='1.0.0'
  context.close()
 assert not errors,errors
 browser.close()
print('PASS responsive 6 viewports, nav, 15 cards, import/export round-trip')
