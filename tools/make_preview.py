from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':820},device_scale_factor=1)
 page.evaluate('''() => {
 const items={};Object.defineProperty(window,'indexedDB',{configurable:true,value:undefined});
 Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return items[k]??null},setItem(k,v){items[k]=String(v)}}});
 }''')
 page.set_content((ROOT/'index.html').read_text(encoding='utf8'),wait_until='load')
 page.wait_for_selector('#f-CourseInfo-Semester')
 page.screenshot(path=str(ROOT/'sample/UI_v1_3_2_course.png'))
 page.locator('[data-action="tab"][data-value="instructors"]').click()
 page.screenshot(path=str(ROOT/'sample/UI_v1_3_2_instructors.png'))
 page.locator('[data-action="tab"][data-value="assessment"]').click()
 page.screenshot(path=str(ROOT/'sample/UI_v1_3_2_assessment.png'))
 browser.close()
