"""Test draft save/load on a simulated persistent browser storage."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf8')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1280,'height':900})
 page.evaluate('''() => { window.__store = {};
 Object.defineProperty(window,'indexedDB',{value:undefined,configurable:true});
 Object.defineProperty(window,'localStorage',{value:{
 getItem:(k)=>window.__store[k]??null,
 setItem:(k,v)=>{window.__store[k]=v},
 removeItem:(k)=>{delete window.__store[k]}
 },configurable:true}); }''')
 page.on('dialog',lambda d:d.accept())
 page.set_content(HTML,wait_until='load')
 page.locator('#tools-menu summary').click()
 page.locator('button[data-action="demo"]').click()
 page.wait_for_timeout(1100)
 before=page.locator('#offering-label').inner_text()
 assert before=='244442-1-2569-SEC01',before
 count=page.evaluate("JSON.parse(window.__store['up-syllabus-drafts-v1']).length")
 assert count>=2,count
 page.set_content(HTML,wait_until='load')
 page.wait_for_timeout(550)
 assert page.locator('#offering-label').inner_text()==before
 page.get_by_role('button',name='Draft ของฉัน').click()
 assert page.locator('.draft-item').count()>=2
 page.locator('button[data-action="close-drawer"]').click()
 with page.expect_download() as event:
  page.locator('#tools-menu summary').click()
  page.locator('button[data-action="backup"]').click()
 assert event.value.suggested_filename.startswith('DRAFT_')
 print('PASS: localStorage fallback draft persistence, multiple drafts, backup JSON')
 b.close()
