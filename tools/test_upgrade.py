"""Regression: draft created in v1.0 reloads in UI v1.1 without migration."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib,zipfile
root=Path(__file__).resolve().parents[1]
old_html=(root / "tools/fixtures/phase1_index_v1_0.html").read_text(encoding='utf-8')
new_html=(root/'index.html').read_text(encoding='utf-8')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(accept_downloads=True,viewport={'width':1440,'height':900})
 page.evaluate('''() => { window.__oldStore = {}; Object.defineProperty(window,'indexedDB',{value:undefined,configurable:true});Object.defineProperty(window,'localStorage',{value:{ getItem:(k)=>window.__oldStore[k]??null,setItem:(k,v)=>window.__oldStore[k]=v,removeItem:(k)=>delete window.__oldStore[k] },configurable:true}); }''')
 page.on('dialog',lambda d:d.accept())
 page.set_content(old_html,wait_until='load')
 page.locator('button[data-action="demo"]').click()
 page.wait_for_timeout(1000)
 assert page.locator('#offering-label').inner_text()=='244442-1-2569-SEC01'
 stored=page.evaluate('JSON.parse(window.__oldStore["up-syllabus-drafts-v1"])')
 assert len(stored)>=2
 page.set_content(new_html,wait_until='load')
 page.wait_for_timeout(250)
 assert page.locator('#offering-label').inner_text()=='244442-1-2569-SEC01'
 assert page.locator('#progress-label').inner_text()=='6 / 6 ส่วน'
 assert page.locator('#nav button').count()==6
 print('PASS: v1.0 browser draft migrated without changes to v1.1, 6/6 overview')
 browser.close()
