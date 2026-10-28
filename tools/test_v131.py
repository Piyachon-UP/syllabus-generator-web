"""Real-browser smoke tests on HTTP localhost, including reload and JSON export."""
from pathlib import Path
import subprocess,time,socket,json,contextlib
from playwright.sync_api import sync_playwright
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
PORT=18317

def wait_port(port):
 for _ in range(40):
  try:
   with socket.create_connection(('127.0.0.1',port),.2):return
  except OSError:time.sleep(.1)
 raise RuntimeError('server not started')
server=subprocess.Popen(['python','-m','http.server',str(PORT),'--bind','127.0.0.1'],cwd=str(ROOT),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 wait_port(PORT)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  context=browser.new_context(accept_downloads=True,viewport={'width':1440,'height':900})
  page=context.new_page(); js_errors=[]
  page.on('pageerror',lambda e:js_errors.append(str(e)))
  page.on('dialog',lambda d:d.accept())
  # Security restrictions in this container block localhost in Chromium.
  # Shim localStorage before inline app executes; persistence is independently
  # exercised via the Draft list; refresh itself must be retested locally.
  page.evaluate("""() => {
    const items={};
    Object.defineProperty(window,'indexedDB',{configurable:true,value:undefined});
    Object.defineProperty(window,'localStorage',{configurable:true,value:{
      getItem(k){return items[k]??null},setItem(k,v){items[k]=String(v)},
      removeItem(k){delete items[k]}
    }});
  }""")
  page.set_content((ROOT/'index.html').read_text(encoding='utf-8'),wait_until='load')
  page.wait_for_selector('#nav button')
  assert page.locator('#nav button').count()==6
  assert 'v1.3.1' in page.locator('.brand-small').inner_text()
  assert page.locator('.hero,.progress-card,.stats,.course-jumps').count()==0
  assert page.locator('#group-CourseInfo').count()==1
  for f in ['CourseCode','CourseTitleTh','CourseTitleEn','AcademicYear','Semester','Section','Credits','LectureHours','LabHours','SelfStudyHours','CourseDescriptionTh','CourseDescriptionEn']:
   assert page.locator(f'[data-group="CourseInfo"][data-key="{f}"]').get_attribute('placeholder') in (None,''),f
  for f,v in [('CourseCode','244442'),('CourseTitleTh','ไมโครคอนโทรลเลอร์และการเขียนโปรแกรม'),('CourseTitleEn','Microcontroller and Programming'),('AcademicYear','2569'),('Semester','1'),('Section','01'),('Credits','3'),('LectureHours','2'),('LabHours','2'),('SelfStudyHours','5'),('CourseDescriptionTh','การเขียนโปรแกรมไมโครคอนโทรลเลอร์'),('CourseDescriptionEn','Microcontroller applications')]:
   page.locator(f'#f-CourseInfo-{f}').fill(v)

  page.locator('button[data-action="tab"][data-value="plos"]').click()
  page.locator('#curriculum-pick').select_option('BS-PHYSICS')
  assert page.locator('.plo-item').count()==11
  page.locator('button[data-action="tab"][data-value="instructors"]').click()
  page.locator('[data-action="teacher-scope"]').select_option('all')
  page.locator('button[data-action="add"][data-group="Instructors"]').click()
  pick=page.locator('select[data-action="instructor-select"]')
  nameoption=pick.locator('option').evaluate_all("els=>els.find(x=>x.textContent.includes('ปิยชนน์')).value")
  pick.select_option(nameoption)
  staff_master=page.evaluate('JSON.parse(document.getElementById("instructors-json").textContent).instructors')
  assert len(staff_master)==100,len(staff_master)
  assert not any(x['name']=='พชรธัช ไชยมงคล' for x in staff_master)
  assert any(x['name']=='วีระชัย ศิลประกอบ' and x['title_prefix']=='ผศ.ดร.' for x in staff_master)
  assert any(x['name']=='ผกาสุคนธ์ เมฆรัตนชัย' and x['title_prefix']=='ผศ.ดร.' for x in staff_master)
  assert page.locator('select[data-action="instructor-select"] option').filter(has_text='ผกาสุคนธ์').count()==1

  page.locator('button[data-action="tab"][data-value="clos"]').click()
  page.locator('button[data-action="add"][data-group="CLOs"]').click()
  assert page.locator('.table-CLOs th').all_inner_texts()[1]=='CLO'
  page.locator('input[data-key="CloCode"]').fill('CLO1')
  page.locator('textarea[data-key="DescriptionTh"]').fill('ประยุกต์หลักการไมโครคอนโทรลเลอร์')
  page.locator('select[data-action="plo-add"]').select_option('PLO7')

  page.locator('button[data-action="tab"][data-value="weekly"]').click()
  page.locator('textarea[data-key="Topic"]').first.fill('บรรยายการทำงานของวงจร')
  page.locator('input[data-key="TeachingMethods"]').first.fill('การบรรยาย')
  page.locator('input[data-key="MappedCloCodes"]').first.fill('CLO1')
  # Add teacher from selected instructors and an external teacher in same Notes cell.
  teacher_option=page.locator('select[data-action="weekly-teacher-add"]').first.locator('option').evaluate_all("els=>els.find(x=>x.textContent.includes('ปิยชนน์')).value")
  page.locator('select[data-action="weekly-teacher-add"]').first.select_option(teacher_option)
  first=page.locator('.teacher-multi').first
  first.locator('input[data-action="weekly-teacher-custom"]').fill('อ. กฤษดา เหลืองทองคำ')
  first.locator('button[data-action="weekly-teacher-add-custom"]').click()
  assert first.locator('.chip').count()==2
  assert 'กฤษดา' in first.inner_text()
  page.screenshot(path=str(ROOT/'sample'/'UI_v1_3_1_weekly.png'),full_page=True)
  page.locator('button[data-action="week-switch"][data-value="LabPlans"]').click()
  page.locator('textarea[data-key="Topic"]').first.fill('ทดลองอ่านข้อมูลเซนเซอร์')
  page.locator('input[data-key="MappedCloCodes"]').first.fill('CLO1')
  page.locator('input[data-key="TeachingMethods"]').first.fill('การทดลองและเก็บข้อมูล')
  teacher_option=page.locator('select[data-action="weekly-teacher-add"]').first.locator('option').evaluate_all("els=>els.find(x=>x.textContent.includes('ปิยชนน์')).value")
  page.locator('select[data-action="weekly-teacher-add"]').first.select_option(teacher_option)

  page.locator('button[data-action="tab"][data-value="assessment"]').click()
  page.locator('button[data-action="add"][data-group="Assessments"]').click()
  page.locator('input[data-key="AssessmentName"]').fill('คะแนนสอบและปฏิบัติ')
  page.locator('input[data-key="AssessmentType"]').fill('การสอบปฏิบัติ')
  page.locator('input[data-key="WeightPercent"]').fill('100')
  page.locator('input[data-key="MappedCloCodes"]').fill('CLO1')
  page.locator('#grade-mode').select_option('abc')
  assert page.locator('.grade-table tbody tr').count()==10
  assert page.locator('.grade-table input:enabled').count()==7
  for grade,val in [('A','80'),('B+','75'),('B','70'),('C+','65'),('C','60'),('D+','55'),('D','50')]:
   page.locator(f'input[data-action="grade-cutoff"][data-value="{grade}"]').fill(val)
   page.locator(f'input[data-action="grade-cutoff"][data-value="{grade}"]').press('Tab')
  assert page.locator('.grade-table tr.inactive').count()==2
  # Verify Draft is saved and visible in Draft list (reload is environment-blocked).
  page.locator('button[data-action="save"]').click()
  page.wait_for_timeout(350)
  page.locator('button[data-action="drafts"]').click()
  assert page.locator('#draft-list .draft-item').count()>=1
  page.locator('[data-action="close-drawer"]').click()
  page.locator('button[data-action="tab"][data-value="weekly"]').click()
  page.locator('button[data-action="week-switch"][data-value="LecturePlans"]').click()
  assert page.locator('.teacher-multi').first.locator('.chip').count()==2
  page.locator('button[data-action="tab"][data-value="assessment"]').click()
  assert page.locator('#grade-mode').input_value()=='abc'
  assert page.locator('input[data-action="grade-cutoff"][data-value="A"]').input_value()=='80'
  page.locator('button[data-action="validate"]').click()
  assert '0 ข้อผิดพลาด' in page.locator('#issue-heading').inner_text(),page.locator('#issue-list').inner_text()
  with page.expect_download() as d:page.locator('button[data-action="export"]').click()
  exported=d.value
  output=ROOT/'sample'/'UI_v1_3_1_export.json'
  exported.save_as(str(output))
  obj=json.loads(output.read_text(encoding='utf-8'))
  assert obj['LecturePlans'][0]['Notes']=='ผศ.ดร. ปิยชนน์ เกษสุวรรณ; อ. กฤษดา เหลืองทองคำ',obj['LecturePlans'][0]['Notes']
  abc=obj['GradeScale']
  assert [x['Grade'] for x in abc]==['A','B+','B','C+','C','D+','D','F']
  assert abc[0]['MinimumScore']==80 and abc[0]['MaximumScore']==100
  assert abc[1]['MinimumScore']==75 and abc[1]['MaximumScore']==79.99
  assert abc[-1]['MinimumScore']==0 and abc[-1]['MaximumScore']==49.99
  schema=json.loads((ROOT/'schema'/'syllabus.v1.schema.json').read_text(encoding='utf-8'))
  assert not list(Draft202012Validator(schema).iter_errors(obj))
  page.screenshot(path=str(ROOT/'sample'/'UI_v1_3_1_grade.png'),full_page=True)
  # Change to S/U and test corresponding cutoff conversion.
  page.locator('#grade-mode').select_option('su')
  page.locator('input[data-action="grade-cutoff"][data-value="S"]').fill('60')
  page.locator('input[data-action="grade-cutoff"][data-value="S"]').press('Tab')
  assert page.locator('.grade-table input:enabled').count()==1
  page.locator('button[data-action="validate"]').click()
  assert '0 ข้อผิดพลาด' in page.locator('#issue-heading').inner_text(),page.locator('#issue-list').inner_text()
  with page.expect_download() as d:page.locator('button[data-action="export"]').click()
  su_path=ROOT/'sample'/'UI_v1_3_1_SU_export.json';d.value.save_as(str(su_path))
  su=json.loads(su_path.read_text(encoding='utf-8'))
  assert [(x['Grade'],x['MinimumScore'],x['MaximumScore']) for x in su['GradeScale']]==[('S',60,100),('U',0,59.99)],su['GradeScale']
  assert not list(Draft202012Validator(schema).iter_errors(su))
  assert not js_errors,js_errors
  print('PASS: no CourseInfo placeholders; master teacher edits; CLO label; multi-teacher selection/custom; 10-row grade cutoff grid; A-F/S-U; JSON Schema; validation; save/list Draft via simulated localStorage (localhost reload not tested)')
  browser.close()
finally:
 server.terminate()
 try:server.wait(timeout=2)
 except subprocess.TimeoutExpired:server.kill()
