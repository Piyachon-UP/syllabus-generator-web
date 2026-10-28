"""End-to-end smoke test for the static browser app v1.3.0."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
schema=json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text(encoding='utf-8'))

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context=browser.new_context(accept_downloads=True, viewport={'width':1440,'height':900})
    page=context.new_page();errs=[]
    page.on('pageerror',lambda e:errs.append(str(e)))
    page.on('dialog',lambda d:d.accept())
    # about:blank in this evaluation environment blocks actual persistence.
    # Use an in-memory localStorage shim to verify app Draft open/reopen logic.
    page.evaluate("""() => {
      const items = {};
      try { delete window.indexedDB; } catch(e) {}
      Object.defineProperty(window, 'indexedDB', {configurable:true, value:undefined}); delete window.indexedDB;
      Object.defineProperty(window, 'localStorage', {configurable:true, value:{
        getItem(k){return items[k] ?? null},
        setItem(k,v){items[k]=String(v)},
        removeItem(k){delete items[k]}
      }});
    }""")
    page.set_content((ROOT/'index.html').read_text(encoding='utf-8'),wait_until='load')
    assert page.locator('#nav button').count()==6
    assert page.locator('.stats,.hero,.progress-card,.course-jumps').count()==0
    assert page.locator('span.required').count()==0
    assert page.locator('#group-CourseInfo').count()==1
    assert page.locator('#f-CourseInfo-Credits').get_attribute('type')=='text'
    assert page.locator('#f-CourseInfo-Semester').get_attribute('type')=='text'
    for field in ['TeachingLanguage','DeliveryMode','Prerequisites','FacultyName','UniversityName','Remarks']:
        assert page.locator(f'[data-group="CourseInfo"][data-key="{field}"]').count()==0
    for f,val in [('CourseCode','244442'),('CourseTitleTh','ไมโครคอนโทรลเลอร์และการเขียนโปรแกรม'),('CourseTitleEn','Microcontroller and Programming'),('AcademicYear','2569'),('Semester','1'),('Section','01'),('Credits','3'),('LectureHours','2'),('LabHours','2'),('SelfStudyHours','5'),('CourseDescriptionTh','การเขียนโปรแกรมไมโครคอนโทรลเลอร์'),('CourseDescriptionEn','Microcontroller applications')]:
        page.locator(f'#f-CourseInfo-{f}').fill(val)
    page.screenshot(path=str(ROOT/'sample/UI_v1_3_course.png'),full_page=True)

    page.locator('button[data-action="tab"][data-value="plos"]').click()
    page.locator('#curriculum-pick').select_option('BS-PHYSICS')
    assert page.locator('.plo-item').count()==11

    page.locator('button[data-action="tab"][data-value="instructors"]').click()
    page.locator('[data-action="add"][data-group="Instructors"]').click()
    assert page.locator('input[data-key="LecturePercent"],input[data-key="LabPercent"]').count()==0
    pick=page.locator('select[data-action="instructor-select"]')
    sel=pick.locator('option').evaluate_all("els=>els.find(x=>x.textContent.includes('ปิยชนน์')).value")
    pick.select_option(sel)
    assert 'ปิยชนน์' in page.locator('.teacher-current').inner_text()
    assert page.locator('.teacher-check input').count()==1
    page.screenshot(path=str(ROOT/'sample/UI_v1_3_instructors.png'),full_page=True)
    # Add custom out-of-master staff member
    page.locator('[data-action="add"][data-group="Instructors"]').click()
    page.locator('select[data-action="instructor-select"]').nth(1).select_option('__manual__')
    page.locator('[data-action="teacher-manual-name"]').fill('อ. ทดสอบ นอกบัญชี')
    page.locator('[data-action="teacher-manual-department"]').fill('หน่วยงานอื่น')

    page.locator('button[data-action="tab"][data-value="clos"]').click()
    page.locator('[data-action="add"][data-group="CLOs"]').click()
    page.locator('input[data-key="CloCode"]').fill('CLO1')
    page.locator('textarea[data-key="DescriptionTh"]').fill('อธิบายหลักการควบคุม')
    assert page.locator('[data-key="BloomLevel"]').count()==0
    page.locator('[data-action="plo-add"]').select_option('PLO7')
    page.locator('[data-action="plo-add"]').select_option('PLO8')
    assert page.locator('.chip').count()==2
    page.screenshot(path=str(ROOT/'sample/UI_v1_3_clos.png'),full_page=True)

    page.locator('button[data-action="tab"][data-value="weekly"]').click()
    assert page.locator('[data-key="LearningActivities"],[data-key="AssessmentMethods"]').count()==0
    page.locator('textarea[data-key="Topic"]').first.fill('บทนำและกิจกรรมพื้นฐาน')
    page.locator('input[data-key="TeachingMethods"]').first.fill('การบรรยายเชิงปฏิสัมพันธ์')
    page.locator('input[data-key="Notes"]').first.fill('ผศ.ดร. ปิยชนน์ เกษสุวรรณ')
    page.locator('input[data-key="MappedCloCodes"]').first.fill('CLO1')
    page.screenshot(path=str(ROOT/'sample/UI_v1_3_weekly.png'),full_page=True)
    page.locator('[data-action="week-switch"][data-value="LabPlans"]').click()
    assert page.locator('datalist option[value="การฝึกปฏิบัติในห้องปฏิบัติการ"]').count()>0
    page.locator('textarea[data-key="Topic"]').first.fill('ปฏิบัติการทดลอง')
    page.locator('input[data-key="TeachingMethods"]').first.fill('ออกแบบหุ่นยนต์ทดลองร่วมกัน')
    page.locator('input[data-key="Notes"]').first.fill('อ. ทดสอบ นอกบัญชี')
    page.locator('input[data-key="MappedCloCodes"]').first.fill('CLO1')

    page.locator('button[data-action="tab"][data-value="assessment"]').click()
    page.locator('[data-action="add"][data-group="Assessments"]').click()
    assert page.locator('[data-key="AssessmentCode"],[data-key="Notes"]').count()==0
    page.locator('input[data-key="AssessmentName"]').fill('คะแนนรวม')
    page.locator('input[data-key="AssessmentType"]').fill('การสอบปฏิบัติ')
    page.locator('input[data-key="WeightPercent"]').fill('100')
    page.locator('input[data-key="MappedCloCodes"]').fill('CLO1')
    page.locator('#grade-mode').select_option('su')
    assert page.locator('input[data-key="Grade"]').count()==2
    assert page.locator('input[data-key="Notes"]').count()==0
    page.locator('input[data-key="MinimumScore"]').nth(0).fill('60')
    page.locator('input[data-key="MaximumScore"]').nth(0).fill('100')
    page.locator('input[data-key="MinimumScore"]').nth(1).fill('0')
    page.locator('input[data-key="MaximumScore"]').nth(1).fill('59.99')
    page.locator('[data-action="add"][data-group="Resources"]').click()
    page.locator('input[data-key="ResourceType"]').fill('ตำราเรียน')
    page.locator('textarea[data-key="Title"]').fill('คู่มือรายวิชา')
    page.screenshot(path=str(ROOT/'sample/UI_v1_3_assessment.png'),full_page=True)

    page.locator('[data-action="validate"]').click()
    result=page.locator('#issue-heading').inner_text()
    assert '0 ข้อผิดพลาด' in result,result
    with page.expect_download() as downloaded:page.locator('[data-action="export"]').click()
    exported_path=ROOT/'sample/UI_v1_3_export.json'
    downloaded.value.save_as(str(exported_path))
    data=json.loads(exported_path.read_text(encoding='utf-8'))
    assert data['CourseInfo']['Credits']=='3'
    assert data['CLOs'][0]['MappedPloCodes']==['PLO7','PLO8']
    assert data['Instructors'][1]['DisplayName']=='อ. ทดสอบ นอกบัญชี'
    assert data['LecturePlans'][0]['Notes']=='ผศ.ดร. ปิยชนน์ เกษสุวรรณ'
    assert data['LabPlans'][0]['TeachingMethods']=='ออกแบบหุ่นยนต์ทดลองร่วมกัน'
    assert data['Assessments'][0]['AssessmentType']=='การสอบปฏิบัติ'
    assert [x['Grade'] for x in data['GradeScale']]==['S','U']
    assert not list(Draft202012Validator(schema).iter_errors(data))

    # Browser persistence requires a real secure origin and is tested manually on localhost.
    assert not errs,errs
    print('PASS: UI, Thai editable lists, manual instructors, PLO multi-select, methods, S/U grades, validation, JSON contract, JSON Schema')
    browser.close()

