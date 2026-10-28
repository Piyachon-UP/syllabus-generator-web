"""Client-side UI v1.3.2 smoke/regression test (no production services)."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
SCHEMA=json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text(encoding='utf-8'))

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(accept_downloads=True,viewport={'width':1440,'height':900})
 page=context.new_page()
 errors=[]
 page.on('pageerror', lambda exc: errors.append(str(exc)))
 page.on('dialog',lambda dlg: dlg.accept())
 # The test browser runs the bundled standalone page without network access.
 # A localStorage shim is enough to verify Save/Load in-page; full reload persistence is
 # recommended for the user to test on localhost where browser security policies permit it.
 page.evaluate("""() => {
   const items={};
   Object.defineProperty(window,'indexedDB',{configurable:true,value:undefined});
   Object.defineProperty(window,'localStorage',{configurable:true,value:{
      getItem(k){return items[k]??null},setItem(k,v){items[k]=String(v)},
      removeItem(k){delete items[k]}
   }});
 }""")
 page.set_content(HTML,wait_until='load')
 page.wait_for_selector('nav#nav button')
 assert 'v1.3.2' in page.locator('.brand-small').inner_text()
 assert page.locator('nav#nav button').count()==6
 assert page.locator('#f-CourseInfo-AcademicYear').input_value()==''
 assert page.locator('#f-CourseInfo-Semester').input_value()==''
 assert page.locator('#f-CourseInfo-Credits').input_value()==''
 assert page.locator('.hero,.stats,.progress-card,.course-jumps').count()==0
 # Empty starter row in each requested tab; no fake data in exported JSON.
 page.locator('[data-action="tab"][data-value="instructors"]').click()
 assert page.locator('.instructor-editor tbody tr').count()==1
 assert page.locator('[data-action="instructor-select"]').count()==1
 staff=page.evaluate('JSON.parse(document.getElementById("instructors-json").textContent).instructors')
 chem=[u for u in staff if u['department']=='สาขาวิชาเคมี']
 assert chem[-1]['name']=='ผกาสุคนธ์ เมฆรัตนชัย'
 index=staff.index(chem[-1]); assert index+1<len(staff) and staff[index+1]['department']!='สาขาวิชาเคมี'
 page.locator('[data-action="tab"][data-value="clos"]').click()
 assert page.locator('.table-CLOs tbody tr').count()==1
 page.locator('[data-action="tab"][data-value="assessment"]').click()
 assert page.locator('.table-Assessments tbody tr').count()==1
 assert page.locator('.table-Resources tbody tr').count()==1
 for typ in ['Assessments','Resources']:
  assert page.locator(f'button[data-action="delete"][data-group="{typ}"]').count()==1
  page.locator(f'button[data-action="delete"][data-group="{typ}"]').click()
  assert page.locator(f'.table-{typ} tbody tr').count()==1
  assert page.locator(f'.table-{typ} .row-no').count()==1
 assert 'กำหนดเอง' in page.locator('[id^="choices-Assessments"]').first.locator('option').all_text_contents() or page.evaluate("!!document.querySelector('#choices-Assessments-0-AssessmentType option[value=\"กำหนดเอง\"]')")
 # custom assessment entry
 assess_type=page.locator('input[data-group="Assessments"][data-key="AssessmentType"]')
 assess_type.fill('กำหนดเอง')
 assert assess_type.input_value()==''
 assert 'ระบุประเภทประเมินเอง' in assess_type.get_attribute('placeholder')
 assess_type.fill('การสอบปฏิบัติพิเศษ')
 # CourseInfo required values
 page.locator('[data-action="tab"][data-value="course"]').click()
 for f,v in [('CourseCode','244442'),('CourseTitleTh','ไมโครคอนโทรลเลอร์และการเขียนโปรแกรม'),('CourseTitleEn','Microcontroller and Programming'),('AcademicYear','2569'),('Semester','1'),('Section','01'),('Credits','3'),('LectureHours','2'),('LabHours','2'),('SelfStudyHours','5'),('CourseDescriptionTh','ศึกษาไมโครคอนโทรลเลอร์'),('CourseDescriptionEn','Study microcontrollers')]:
  page.locator(f'#f-CourseInfo-{f}').fill(v)
 page.locator('[data-action="tab"][data-value="plos"]').click()
 page.locator('#curriculum-pick').select_option('BS-PHYSICS')
 assert page.locator('.plo-item').count()==11
 # Select instructor into the pre-existing single empty row, mark responsible
 page.locator('[data-action="tab"][data-value="instructors"]').click()
 teacher=page.locator('[data-action="instructor-select"]').first
 idx=teacher.locator('option').evaluate_all("o=>o.find(x=>x.textContent.includes('ปิยชนน์')).value")
 teacher.select_option(idx)
 page.locator('.instructor-editor input[data-key="IsResponsibleInstructor"]').check()
 assert page.locator('.instructor-editor tbody tr').count()==1
 page.locator('[data-action="tab"][data-value="clos"]').click()
 page.locator('input[data-key="CloCode"]').fill('CLO1')
 page.locator('textarea[data-key="DescriptionTh"]').fill('ประยุกต์ไมโครคอนโทรลเลอร์')
 page.locator('select[data-action="plo-add"]').select_option('PLO7')
 assert page.locator('.table-CLOs tbody tr').count()==1
 # Lecture method custom option selection and free text; Lab separate
 page.locator('[data-action="tab"][data-value="weekly"]').click()
 for group,value in [('LecturePlans','บรรยายแลกเปลี่ยนเชิงปฏิบัติ'),('LabPlans','ทดลองออกแบบเอง')]:
  page.locator(f'[data-action="week-switch"][data-value="{group}"]').click()
  ctrl=page.locator(f'input[data-group="{group}"][data-key="TeachingMethods"]').first
  assert page.evaluate("g=>!!document.querySelector('#choices-'+g+'-0-TeachingMethods option[value=\"กำหนดเอง\"]')",group)
  ctrl.fill('กำหนดเอง')
  assert ctrl.input_value()==''
  assert 'ระบุวิธีการสอนเอง' in ctrl.get_attribute('placeholder')
  ctrl.fill(value)
  page.locator(f'textarea[data-group="{group}"][data-key="Topic"]').first.fill('เนื้อหาและกิจกรรมสัปดาห์ที่ 1')
  page.locator(f'input[data-group="{group}"][data-key="MappedCloCodes"]').first.fill('CLO1')
 # Assessment filled (first row, no extra row), Resources remains blank
 page.locator('[data-action="tab"][data-value="assessment"]').click()
 page.locator('input[data-key="AssessmentName"]').fill('การประเมินผล')
 page.locator('input[data-key="WeightPercent"]').fill('100')
 page.locator('input[data-key="MappedCloCodes"]').fill('CLO1')
 page.locator('#grade-mode').select_option('su')
 page.locator('input[data-action="grade-cutoff"][data-value="S"]').fill('60')
 page.locator('input[data-action="grade-cutoff"][data-value="S"]').press('Tab')
 page.locator('[data-action="validate"]').click()
 assert '0 ข้อผิดพลาด' in page.locator('#issue-heading').inner_text(),page.locator('#issue-list').inner_text()
 page.locator('[data-action="save"]').click()
 page.locator('[data-action="drafts"]').click()
 assert page.locator('.draft-item').count()>=1
 page.locator('[data-action="close-drawer"]').click()
 with page.expect_download() as d:page.locator('[data-action="export"]').click()
 path=ROOT/'sample/UI_v1_3_2_export.json';d.value.save_as(str(path))
 output=json.loads(path.read_text(encoding='utf-8'))
 assert not list(Draft202012Validator(SCHEMA).iter_errors(output))
 assert len(output['Instructors'])==1
 assert len(output['CLOs'])==1
 assert len(output['Assessments'])==1
 assert output['Resources']==[]
 assert output['Assessments'][0]['AssessmentType']=='การสอบปฏิบัติพิเศษ'
 assert output['LecturePlans'][0]['TeachingMethods']=='บรรยายแลกเปลี่ยนเชิงปฏิบัติ'
 assert output['LabPlans'][0]['TeachingMethods']=='ทดลองออกแบบเอง'
 assert output['GradeScale'][0]['MinimumScore']==60
 # New Draft after data entry should clear term/year and regenerate starter rows.
 page.locator('details#tools-menu summary').click()
 page.locator('[data-action="new"]').click()
 assert page.locator('#f-CourseInfo-AcademicYear').input_value()==''
 assert page.locator('#f-CourseInfo-Semester').input_value()==''
 page.locator('[data-action="tab"][data-value="instructors"]').click()
 assert page.locator('.instructor-editor tbody tr').count()==1
 page.locator('[data-action="tab"][data-value="assessment"]').click()
 assert page.locator('.table-Assessments tbody tr').count()==1 and page.locator('.table-Resources tbody tr').count()==1
 assert not errors,errors
 print('PASS: blank year/semester; one empty row per requested section; delete-last fallback; chemistry instructor order; custom method dropdown lecture/lab; custom assessment dropdown; JSON Schema and Validation; Save/Draft list; new Draft clearing')
 browser.close()
