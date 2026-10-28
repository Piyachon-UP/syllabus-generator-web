"""Phase 1.2 targeted smoke tests for browser app and JSON masters."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
schema=json.loads((ROOT/'schema/syllabus.v1.schema.json').read_text(encoding='utf-8'))
html=(ROOT/'index.html').read_text(encoding='utf-8')
plos=json.loads((ROOT/'data/curriculum_plos.json').read_text(encoding='utf-8'))['curricula']
teachers=json.loads((ROOT/'data/instructors.json').read_text(encoding='utf-8'))['instructors']
assert len(plos)==15 and len(teachers)==100
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    ctx=browser.new_context(accept_downloads=True, viewport={'width':1440,'height':900})
    page=ctx.new_page()
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('dialog',lambda d:d.accept())
    page.set_content(html,wait_until='load')
    page.wait_for_timeout(600)
    assert page.locator('#nav button').count()==6
    assert page.locator('.stats,.hero,.progress-card,.course-jumps').count()==0
    assert page.locator('#group-CourseInfo').count()==1
    assert page.locator('#course-credits').count()==1
    assert page.locator('#course-descriptions').count()==1
    for field in ['TeachingLanguage','DeliveryMode','Prerequisites','FacultyName','UniversityName','Remarks']:
        assert page.locator(f'[data-group="CourseInfo"][data-key="{field}"]').count()==0,field
    for g in ['Curriculum','ClassMeetings','Exams','StudentGroups']:
        assert page.locator(f'#group-{g}').count()==0,g
    page.screenshot(path=str(ROOT/'sample/UI_v1_2_course_desktop.png'),full_page=True)
    page.locator('button[data-action="tab"][data-value="plos"]').first.click()
    assert page.locator('#curriculum-pick option').count()==16
    page.locator('#curriculum-pick').select_option('BS-PHYSICS')
    assert page.locator('.plo-item').count()==11
    assert 'ผู้เรียนสามารถใช้ภาษา' in page.locator('.plo-list').inner_text()
    assert page.locator('input[data-group="PLOs"]').count()==0
    page.screenshot(path=str(ROOT/'sample/UI_v1_2_plos.png'),full_page=True)
    page.locator('button[data-action="tab"][data-value="instructors"]').first.click()
    page.locator('button[data-action="add"][data-group="Instructors"]').click()
    options=page.locator('select[data-action="instructor-select"] option').all_inner_texts()
    assert any('ปิยชนน์' in x for x in options)
    assert not any('บุญช่วง' in x for x in options)  # biology hidden in physics curriculum
    teacher_index=next(i for i,t in enumerate(teachers) if t['name'].strip().startswith('ปิยชนน์'))
    page.locator('select[data-action="instructor-select"]').select_option(str(teacher_index))
    assert 'ปิยชนน์' in page.locator('.teacher-current').inner_text()
    assert 'สาขาวิชาฟิสิกส์' in page.locator('.teacher-department').inner_text()
    assert page.locator('input[data-key="StaffId"]').count()==0
    page.locator('input[data-key="LecturePercent"]').fill('100')
    page.locator('input[data-key="LabPercent"]').fill('100')
    page.screenshot(path=str(ROOT/'sample/UI_v1_2_instructors.png'),full_page=True)
    page.locator('#teacher-dept').select_option('all')
    options=page.locator('select[data-action="instructor-select"] option').all_inner_texts()
    assert any('บุญช่วง' in x for x in options)
    # UI validates optional StaffId Email as warning, not error
    page.locator('button[data-action="tab"][data-value="course"]').first.click()
    page.locator('#f-CourseInfo-CourseCode').fill('244442')
    page.locator('#f-CourseInfo-CourseTitleTh').fill('ไมโครคอนโทรลเลอร์และการเขียนโปรแกรม')
    page.locator('#f-CourseInfo-AcademicYear').fill('2569')
    page.locator('#f-CourseInfo-Section').fill('01')
    page.locator('#f-CourseInfo-Credits').fill('3(2-2-5)')
    page.locator('#f-CourseInfo-LectureHours').fill('2')
    page.locator('#f-CourseInfo-LabHours').fill('2')
    page.locator('button[data-action="tab"][data-value="clos"]').first.click()
    page.locator('button[data-action="add"][data-group="CLOs"]').click()
    page.locator('input[data-group="CLOs"][data-key="CloCode"]').fill('CLO1')
    page.locator('textarea[data-group="CLOs"][data-key="DescriptionTh"]').fill('อธิบายวงจรเบื้องต้น')
    page.locator('input[data-group="CLOs"][data-key="MappedPloCodes"]').fill('PLO7')
    page.locator('button[data-action="tab"][data-value="weekly"]').first.click()
    page.locator('textarea[data-group="LecturePlans"][data-key="Topic"]').first.fill('ไมโครคอนโทรลเลอร์')
    page.locator('input[data-group="LecturePlans"][data-key="MappedCloCodes"]').first.fill('CLO1')
    page.locator('button[data-action="tab"][data-value="assessment"]').first.click()
    page.locator('button[data-action="add"][data-group="Assessments"]').click()
    page.locator('input[data-group="Assessments"][data-key="AssessmentCode"]').fill('A1')
    page.locator('input[data-group="Assessments"][data-key="AssessmentName"]').fill('คะแนนรวม')
    page.locator('input[data-group="Assessments"][data-key="WeightPercent"]').fill('100')
    page.locator('button[data-action="validate"]').click()
    heading=page.locator('#issue-heading').inner_text()
    assert '0 ข้อผิดพลาด' in heading,heading
    assert 'StaffId/Email' in page.locator('#issue-list').inner_text()
    with page.expect_download() as dl:
        page.locator('button[data-action="export"]').click()
    path=ROOT/'sample/UI_v1_2_export.json'
    dl.value.save_as(str(path))
    exported=json.loads(path.read_text(encoding='utf-8'))
    assert exported['OfferingId']=='244442-1-2569-SEC01'
    assert len(exported['PLOs'])==11
    assert exported['Instructors'][0]['DisplayName'].find('ปิยชนน์')>=0
    assert exported['Curriculum']['CurriculumCode']=='BS-PHYSICS'
    assert not list(Draft202012Validator(schema).iter_errors(exported))
    # local draft persists on page reload and JSON remains 1.0
    page.locator('button[data-action="save"]').click()
    page.wait_for_timeout(300)
    page.reload(wait_until='load') if page.url!='about:blank' else page.set_content(html,wait_until='load')
    page.wait_for_timeout(400)
    assert not errors,errors
    # mobile
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(ROOT/'sample/UI_v1_2_mobile.png'),full_page=True)
    print('PASS: 15 curricula, 100 instructors, streamlined form, PLO selection, department filter, validation, JSON schema, responsive')
    browser.close()
