/* Syllabus Generator Web UI v1.4.0 / JSON Contract v1.0.0 — all operations stay in this browser. */
(() => {
'use strict';
const contract = JSON.parse(document.getElementById('contract-json').textContent);
const demo = JSON.parse(document.getElementById('demo-json').textContent);
const curriculumMaster = JSON.parse(document.getElementById('curricula-json').textContent).curricula;
const instructorMaster = JSON.parse(document.getElementById('instructors-json').textContent).instructors;
let allDepartments = false;
const normalizeName = s=>String(s||'').replace(/\s+/g,' ').trim();
const teacherDisplay = t=>normalizeName([t.title_prefix,t.name].filter(Boolean).join(' '));
const curriculumLabel = c=>[c.major||'ไม่ระบุสาขา',c.program_name,c.curriculum_id].filter(Boolean).join(' · ');
const selectedCurriculum=()=>curriculumMaster.find(c=>c.curriculum_id===state.Curriculum.CurriculumCode);
function curriculumDepartment(){const curr=selectedCurriculum();if(!curr)return '';
  const label=curr.curriculum_id||'';
  if(label.includes('MATHEMATICS'))return 'สาขาวิชาคณิตศาสตร์'; // match the staff department spelling in the supplied master
  return curr.major||'';
}
function activeTeacherDepartment(){return curriculumDepartment()||'';}
function masterTeacherIndex(rec){return instructorMaster.findIndex(t=>normalizeName(teacherDisplay(t))===normalizeName(rec.DisplayName)&&normalizeName(t.department)===normalizeName(rec.Department));}
function selectCurriculum(id){
 const c=curriculumMaster.find(x=>x.curriculum_id===id); const old=state.Curriculum.CurriculumCode||'';
 if(!c)return;
 if(id!==old && state.PLOs.some(p=>isPopulated('PLOs',p)) && !confirm('เปลี่ยนหลักสูตรจะปรับรายการ PLO ตามหลักสูตรใหม่ และอาจกระทบการเชื่อมโยง CLO ยืนยันหรือไม่?'))return false;
 state.Curriculum={...state.Curriculum,CurriculumCode:c.curriculum_id,CurriculumName:c.program_name,ProgramName:c.major||'',DegreeLevel:c.program_name.replace(/^หลักสูตร/,'').trim(),DepartmentName:c.major||''};
 state.CourseInfo.FacultyName=c.faculty||state.CourseInfo.FacultyName;
 state.CourseInfo.UniversityName=c.university||state.CourseInfo.UniversityName;
 state.PLOs=(c.plos||[]).map(p=>({...blankRecord('PLOs'),PloCode:p.plo_id,DescriptionTh:p.description,Category:p.category||'',Notes:p.note||''}));
 allDepartments=false;
 return true;
}

const SECTION_KEYS=['CourseInfo','Curriculum','Instructors','PLOs','CLOs','ClassMeetings','Exams','StudentGroups','LecturePlans','LabPlans','Assessments','GradeScale','Resources'];
const TABS=[
 {id:'course',name:'ข้อมูลรายวิชา',en:'Course Info',desc:'ข้อมูลรายวิชา หน่วยกิต และคำอธิบายรายวิชา'},
 {id:'plos',name:'PLOs',en:'Program Learning Outcomes',desc:'เลือกหลักสูตรเพื่อแสดง PLOs จากข้อมูลหลักสูตร'},
 {id:'instructors',name:'ผู้สอน',en:'Instructors',desc:'เลือกผู้สอนจากรายชื่อสาขาวิชา และกำหนดผู้รับผิดชอบรายวิชา'},
 {id:'clos',name:'CLOs',en:'Course Learning Outcomes',desc:'ผลลัพธ์การเรียนรู้ระดับรายวิชา พร้อมเชื่อมโยงรหัส PLO'},
 {id:'weekly',name:'แผนการสอน',en:'Weekly Plan',desc:'แผนบรรยายและปฏิบัติการ แยกตาราง 15 สัปดาห์'},
 {id:'assessment',name:'การประเมิน',en:'Assessments',desc:'รายการวัดผล น้ำหนักคะแนน เกณฑ์ตัดเกรด และแหล่งเรียนรู้'}];
const MAP={
 CourseCode:'รหัสรายวิชา',CourseTitleTh:'ชื่อรายวิชา (ไทย)',CourseTitleEn:'ชื่อรายวิชา (อังกฤษ)',CourseDescriptionTh:'คำอธิบายรายวิชา (ไทย)',CourseDescriptionEn:'คำอธิบายรายวิชา (อังกฤษ)',Credits:'หน่วยกิต',LectureHours:'ชั่วโมงบรรยาย/สัปดาห์',LabHours:'ชั่วโมงปฏิบัติ/สัปดาห์',SelfStudyHours:'ชั่วโมงศึกษาด้วยตนเอง/สัปดาห์',AcademicYear:'ปีการศึกษา (พ.ศ.)',Semester:'ภาคเรียน',Section:'กลุ่มเรียน',FacultyName:'คณะ',UniversityName:'มหาวิทยาลัย',TeachingLanguage:'ภาษาที่ใช้สอน',DeliveryMode:'รูปแบบการสอน',Prerequisites:'รายวิชาบังคับก่อน',Remarks:'หมายเหตุ',CurriculumCode:'รหัสหลักสูตร',CurriculumName:'ชื่อหลักสูตร',CurriculumRevisionYear:'ปีปรับปรุงหลักสูตร (พ.ศ.)',ProgramCode:'รหัสสาขาวิชา',ProgramName:'ชื่อสาขาวิชา',DegreeLevel:'ระดับปริญญา',DepartmentName:'หน่วยงาน',StaffId:'รหัสบุคลากร',IsResponsibleInstructor:'ผู้รับผิดชอบ',Prefix:'คำนำหน้า',FirstName:'ชื่อ',LastName:'นามสกุล',DisplayName:'ชื่อแสดงผล',Email:'อีเมล',Department:'หน่วยงาน',LecturePercent:'สัดส่วนบรรยาย %',LabPercent:'สัดส่วนปฏิบัติ %',Notes:'หมายเหตุ',PloCode:'รหัส PLO',DescriptionTh:'คำอธิบาย (ไทย)',DescriptionEn:'คำอธิบาย (อังกฤษ)',Category:'หมวดหมู่',CloCode:'CLO',BloomLevel:'Bloom Level',MappedPloCodes:'PLO ที่เชื่อมโยง',MappedCloCodes:'CLO ที่เชื่อมโยง',DayOfWeek:'วันเรียน',StartTime:'เวลาเริ่ม',EndTime:'เวลาสิ้นสุด',RoomCode:'รหัสห้อง',DeliveryType:'ประเภทเรียน',ExamTypeCode:'ประเภทสอบ',ExamDate:'วันสอบ (ค.ศ.)',StudentProgramName:'สาขานิสิต',StudentYearLevel:'ชั้นปี',RegisteredStudentCount:'จำนวนนิสิต',StudentCurriculumCode:'รหัสหลักสูตรนิสิต',StudentCurriculumRevisionYear:'ปีปรับปรุงหลักสูตรนิสิต',WeekNumber:'สัปดาห์',Topic:'หัวข้อ / กิจกรรมการเรียนรู้',LearningActivities:'กิจกรรมการเรียนรู้',TeachingMethods:'วิธีสอน',AssessmentMethods:'การวัดผล',AssessmentCode:'รหัสประเมิน',AssessmentName:'รายการประเมิน',AssessmentType:'ประเภทประเมิน',WeightPercent:'น้ำหนัก %',Grade:'เกรด',MinimumScore:'คะแนนต่ำสุด',MaximumScore:'คะแนนสูงสุด',ResourceType:'ประเภทแหล่งเรียนรู้',Title:'ชื่อหนังสือ / แหล่งเรียนรู้',Author:'ผู้แต่ง',Year:'ปี',Url:'URL'};
const SELECT={DegreeLevel:['วิทยาศาสตรบัณฑิต','วิทยาศาสตรมหาบัณฑิต','วิทยาศาสตรดุษฎีบัณฑิต','ปรัชญาดุษฎีบัณฑิต'],Prefix:['อ.','ดร.','ผศ.','ผศ.ดร.','รศ.','รศ.ดร.'],DayOfWeek:['จันทร์','อังคาร','พุธ','พฤหัสบดี','ศุกร์','เสาร์','อาทิตย์']};
const LECTURE_METHODS=['การบรรยาย','การบรรยายเชิงปฏิสัมพันธ์','การอภิปรายกลุ่ม','การเรียนรู้แบบใช้ปัญหาเป็นฐาน (PBL)','การเรียนรู้แบบใช้โครงงานเป็นฐาน (PjBL)','การเรียนรู้แบบกรณีศึกษา','การเรียนรู้แบบสืบเสาะหาความรู้','การเรียนรู้แบบร่วมมือ','ห้องเรียนกลับด้าน (Flipped Classroom)','การสาธิต','การเรียนรู้แบบผสมผสาน','การนำเสนอและอภิปราย','การเรียนรู้ด้วยตนเอง','การฝึกปฏิบัติคำนวณและแก้โจทย์','การเรียนรู้ผ่านสื่อดิจิทัล','กำหนดเอง'];
const LAB_METHODS=['การสาธิตขั้นตอนปฏิบัติ','การฝึกปฏิบัติในห้องปฏิบัติการ','การทดลองและเก็บข้อมูล','การปฏิบัติแบบรายบุคคล','การปฏิบัติแบบกลุ่ม','การฝึกใช้เครื่องมือและอุปกรณ์','การออกแบบและดำเนินการทดลอง','การเรียนรู้แบบโครงงาน','การแก้ปัญหาจากสถานการณ์จริง','การเรียนรู้แบบฐานกิจกรรม','การฝึกทักษะผ่านสถานการณ์จำลอง','การศึกษาภาคสนาม','การประเมินผลจากชิ้นงาน','การทำเวิร์กช็อป','การเรียนรู้แบบสืบเสาะหาความรู้','กำหนดเอง'];
const ASSESSMENT_TYPES=['การสอบย่อย','การบ้าน / แบบฝึกหัด','การสอบกลางภาค','การสอบปลายภาค','การสอบปฏิบัติ','รายงาน','โครงงาน','การนำเสนอ','การมีส่วนร่วมในชั้นเรียน','การประเมินชิ้นงาน','การประเมินทักษะปฏิบัติ','การสังเกตพฤติกรรม','แฟ้มสะสมผลงาน','การประเมินตนเอง','การประเมินโดยเพื่อน','กำหนดเอง'];
const RESOURCE_TYPES=['ตำราเรียน','หนังสือ','หนังสืออิเล็กทรอนิกส์','เอกสารประกอบการสอน','บทความวิชาการ','บทความวิจัย','วารสาร','เว็บไซต์','วิดีโอการสอน','สื่อออนไลน์','คู่มือปฏิบัติการ','ฐานข้อมูลวิชาการ','ซอฟต์แวร์และเครื่องมือ','สื่อการเรียนรู้แบบเปิด','กำหนดเอง'];
const GRADE_ABC=['A','B+','B','C+','C','D+','D','F'];
const GRADE_SU=['S','U'];
const VISIBLE_COLS={CLOs:['CloCode','DescriptionTh','MappedPloCodes'],LecturePlans:['WeekNumber','Topic','TeachingMethods','MappedCloCodes','Notes'],LabPlans:['WeekNumber','Topic','TeachingMethods','MappedCloCodes','Notes'],Assessments:['AssessmentName','AssessmentType','WeightPercent','MappedCloCodes'],GradeScale:['Grade','MinimumScore','MaximumScore'],Resources:['ResourceType','Title','Author','Year','Url']};
let manualTeacherRows=new Set();
function visibleCols(group){return VISIBLE_COLS[group]||Object.keys(dataFields(group));}
function optionsDatalist(id,items){return `<datalist id="${id}">${items.map(x=>`<option value="${escapeHtml(x)}"></option>`).join('')}</datalist>`;}
function gradeMode(){if(!state.GradeScale.length)return '';return state.GradeScale.some(x=>GRADE_SU.includes(x.Grade))&&!state.GradeScale.some(x=>GRADE_ABC.includes(x.Grade))?'su':'abc';}


const WIDE=new Set(['CourseTitleTh','CourseTitleEn','CourseDescriptionTh','CourseDescriptionEn','CurriculumName','Remarks','Prerequisites']);
const TEXTAREA=new Set(['CourseDescriptionTh','CourseDescriptionEn','Remarks','Notes','DescriptionTh','DescriptionEn','Topic','LearningActivities','TeachingMethods','AssessmentMethods','Title']);
const TABLE_WIDTH={DescriptionTh:'long',DescriptionEn:'long',Topic:'long',LearningActivities:'long',TeachingMethods:'long',AssessmentMethods:'small',AssessmentName:'long',MappedPloCodes:'small',MappedCloCodes:'small',Notes:'small',LecturePercent:'narrow',LabPercent:'narrow',WeekNumber:'narrow',WeightPercent:'narrow',MinimumScore:'narrow',MaximumScore:'narrow',StaffId:'small',Email:'long',RegisteredStudentCount:'narrow',Year:'narrow'};
const GROUP_TAB={CourseInfo:'course',Curriculum:'course',ClassMeetings:'course',Exams:'course',StudentGroups:'course',PLOs:'plos',Instructors:'instructors',CLOs:'clos',LecturePlans:'weekly',LabPlans:'weekly',Assessments:'assessment',GradeScale:'assessment',Resources:'assessment'};
const el=id=>document.getElementById(id);
const escapeHtml=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const dataFields=group=>(contract.properties[group]?.type==='object'?contract.properties[group]:contract.properties[group]?.items).properties;
const blankRecord=(group)=>Object.fromEntries(Object.entries(dataFields(group)).map(([k,v])=>[k,v.type==='boolean'?false:v.type==='array'?[]:'']));
const nowISO=()=>new Date().toISOString();
// Rows that should visibly display an empty editing row when there is no saved data.
const STARTER_ROW_GROUPS=['CLOs','Assessments','Resources'];
function ensureStarterRows(data){
 for(const group of STARTER_ROW_GROUPS){if(!Array.isArray(data[group])||data[group].length===0)data[group]=[blankRecord(group)];}
 return data;
}
function blankData(){return {SchemaVersion:'1.0.0',OfferingId:'',SourceType:'BlazorManual',ExtractedAt:nowISO(),CourseInfo:{...blankRecord('CourseInfo'),FacultyName:'คณะวิทยาศาสตร์',UniversityName:'มหาวิทยาลัยพะเยา'},Curriculum:blankRecord('Curriculum'),Instructors:[],PLOs:[],CLOs:[blankRecord('CLOs')],ClassMeetings:[],Exams:[],StudentGroups:[],LecturePlans:Array.from({length:15},(_,i)=>({...blankRecord('LecturePlans'),WeekNumber:i+1})),LabPlans:Array.from({length:15},(_,i)=>({...blankRecord('LabPlans'),WeekNumber:i+1})),Assessments:[blankRecord('Assessments')],GradeScale:[],Resources:[blankRecord('Resources')]};}
// JSON-only model: nothing is saved to IndexedDB/localStorage.
// Users explicitly download a JSON file and re-open it for further edits.
let state=blankData(), currentTab='course', weeklyKind='LecturePlans', showingErrors=false;
let unsavedChanges=false, lastLoadedFile='';
function isPopulated(group,r){return Object.entries(r||{}).some(([k,v])=>k!=='WeekNumber'&&(Array.isArray(v)?v.length>0:typeof v==='boolean'?false:String(v??'').trim()!==''));}
function normalizedInput(v,type){if(type==='boolean')return Boolean(v);if(type==='array')return String(v??'').split(/[,;\n]/).map(s=>s.trim().toUpperCase()).filter(Boolean).filter((x,i,a)=>a.indexOf(x)===i);if(type==='number'||type==='integer')return v===''?'':Number(v);return String(v??'');}
function inputValue(v){return Array.isArray(v)?v.join(', '):v??'';}
function cleanedRecord(group,r,requiredOnly=false){const prop=dataFields(group),required=(contract.properties[group].type==='object'?contract.properties[group]:contract.properties[group].items).required||[];const o={};for(const [key,spec] of Object.entries(prop)){let v=r?.[key];if(spec.type==='boolean'){o[key]=Boolean(v);continue;}if(spec.type==='array'){if(Array.isArray(v)&&v.length)o[key]=v;continue;}if(v===null||v===undefined||v===''){if(required.includes(key)){if(spec.type==='integer'||spec.type==='number')o[key]=null;else o[key]='';}continue;}if(spec.type==='integer'||spec.type==='number'){const n=Number(v);o[key]=Number.isFinite(n)?n:null;}else{o[key]=String(v).trim();}}return o;}
function safePart(v){return String(v??'').trim().toUpperCase().replace(/\s+/g,'').replace(/[^A-Z0-9_-]/g,'');}
function offeringId(){const c=state.CourseInfo||{},a=safePart(c.CourseCode),b=safePart(c.Semester),y=String(c.AcademicYear||'').trim(),sec=safePart(c.Section).replace(/^SEC/,'');return a&&b&&/^\d{4}$/.test(y)&&sec?`${a}-${b}-${y}-SEC${sec}`:'';}
function payload(){const d={SchemaVersion:'1.0.0',OfferingId:offeringId(),SourceType:'BlazorManual',ExtractedAt:nowISO()};for(const group of SECTION_KEYS){if(group==='CourseInfo'||group==='Curriculum'){d[group]=cleanedRecord(group,state[group]);}else d[group]=(state[group]||[]).filter(r=>isPopulated(group,r)).map(r=>cleanedRecord(group,r));}return d;}
function fromPayload(obj){
 const d=blankData();
 for(const group of SECTION_KEYS){
  const input=obj?.[group];
  if(group==='CourseInfo'||group==='Curriculum')d[group]={...blankRecord(group),...((input&&typeof input==='object'&&!Array.isArray(input))?input:{})};
  else if(Array.isArray(input))d[group]=input.map(x=>({...blankRecord(group),...x}));
 }
 // Earlier Drafts may already contain invalid browser-restored sentinel values.
 // Clear only the known invalid 1/0 values, preserving correctly entered year/term.
 const info=d.CourseInfo;
 if(['0','1'].includes(String(info.AcademicYear??'').trim()))info.AcademicYear='';
 if(String(info.Semester??'').trim()==='0')info.Semester='';
 const oldCredit=String(info.Credits||'');
 if(/^\d+\s*\(\s*\d+\s*[-–]\s*\d+\s*[-–]\s*\d+\s*\)$/.test(oldCredit))info.Credits=oldCredit.split('(')[0].trim();
 // Do not resurface a phantom instructor row from pre-v1.3.3 Drafts.
 d.Instructors=d.Instructors.filter(r=>isPopulated('Instructors',r));
 for(const group of ['LecturePlans','LabPlans']){
  if(!d[group].length)d[group]=Array.from({length:15},(_,i)=>({...blankRecord(group),WeekNumber:i+1}));
 }
 return ensureStarterRows(d);
}
function getArrayType(group,key){return dataFields(group)[key]?.type;}
// Compatible with the existing JSON contract: multiple weekly instructors are saved
// in the pre-existing Notes string separated by semicolons; no new schema fields.
function splitTeacherNames(value){return [...new Set(String(value||'').split(/[;,\n]/).map(normalizeName).filter(Boolean))];}
function setWeeklyTeachers(group,row,items){
 const record=state[group]?.[row];if(!record)return;
 record.Notes=[...new Set(items.map(normalizeName).filter(Boolean))].join('; ');
 render();scheduleSave();
}
function updateGradeCutoffs(mode){
 const grades=mode==='su'?GRADE_SU:GRADE_ABC;
 const existing=new Map(state.GradeScale.map(x=>[x.Grade,x]));
 // A/F/S/U have fixed order. Inactive grade mode is excluded from JSON.
 state.GradeScale=grades.map((grade,i)=>{
   const old=existing.get(grade)||{};
   const out={...blankRecord('GradeScale'),...old,Grade:grade};
   if(i===grades.length-1)out.MinimumScore=0;
   const min=Number(out.MinimumScore);
   const upper= i===0 ? 100 : Number(existing.get(grades[i-1])?.MinimumScore);
   if(out.MinimumScore!=='' && Number.isFinite(min) && (i===0 || (existing.get(grades[i-1])?.MinimumScore!=='' && Number.isFinite(upper)))){
     out.MaximumScore=i===0?100:Math.max(0,Math.round((upper-.01)*100)/100);
   }else out.MaximumScore='';
   return out;
 });
}
function gradeCutoffTable(){
 const mode=gradeMode(),abc=mode==='abc',su=mode==='su';
 const cutoff=(grade,enabled)=>{
   const rec=state.GradeScale.find(x=>x.Grade===grade);
   const terminal=grade==='F'||grade==='U';
   return `<tr class="${enabled?'':'inactive'}"><td class="grade-label">${grade}</td><td class="grade-op">${terminal?'':'≥'}</td><td>${terminal?'<span class="terminal-grade">—</span>':`<input type="number" min="0" max="100" step="0.01" data-action="grade-cutoff" data-value="${grade}" aria-label="คะแนนขั้นต่ำเกรด ${grade}" value="${enabled&&rec&&rec.MinimumScore!==''?escapeHtml(rec.MinimumScore):''}" ${enabled?'':'disabled'}>`}</td></tr>`;
 };
 return `<div class="grade-table-wrap"><table class="grade-table"><thead><tr><th>เกรด</th><th colspan="2">คะแนนสอบ</th></tr></thead><tbody>${GRADE_ABC.map(g=>cutoff(g,abc)).join('')}${GRADE_SU.map(g=>cutoff(g,su)).join('')}</tbody></table></div><div class="grade-help">ระบุคะแนนขั้นต่ำที่ได้เกรดนั้น เช่น A ≥ 80 · F และ U ต่ำกว่าเกรดก่อนหน้าโดยอัตโนมัติ</div>`;
}
function inputElement(group,key,value,scope,row,table=false){
 const spec=dataFields(group)[key], type=spec.type;
 const attr=`${scope==='object'?`id="f-${group}-${key}"`:''} data-group="${group}" data-key="${key}" data-scope="${scope}" ${row!==undefined?`data-row="${row}"`:''}`;
 const cls=table?(TABLE_WIDTH[key]||''):'';
 if(type==='boolean')return `<input aria-label="${escapeHtml(MAP[key]||key)}" class="check" type="checkbox" ${value?'checked':''} ${attr}>`;
 if(group==='CLOs'&&key==='MappedPloCodes'){
   const candidates=state.PLOs||[],selected=Array.isArray(value)?value:[];
   return `<div class="plo-picker"><select aria-label="เพิ่ม PLO ที่เชื่อมโยง" data-action="plo-add" data-row="${row}"><option value="">＋ เลือก PLO</option>${candidates.filter(x=>!selected.includes(x.PloCode)).map(x=>`<option value="${escapeHtml(x.PloCode)}">${escapeHtml(x.PloCode)} — ${escapeHtml(x.DescriptionTh||'').slice(0,85)}</option>`).join('')}</select><div class="chips">${selected.map(x=>`<button type="button" class="chip" data-action="plo-remove" data-row="${row}" data-value="${escapeHtml(x)}" title="ลบ ${escapeHtml(x)}">${escapeHtml(x)} ×</button>`).join('')}</div></div>`;
 }
 if((group==='LecturePlans'||group==='LabPlans')&&key==='Topic'){
   const rec=state[group][row]||{};
   const txt=[rec.Topic,rec.LearningActivities].filter(x=>String(x||'').trim()).join('\n');
   return `<textarea class="long weekly-topic" ${attr} aria-label="หัวข้อและกิจกรรมการเรียนรู้" placeholder="ระบุหัวข้อและกิจกรรมการเรียนรู้">${escapeHtml(txt)}</textarea>`;
 }
 if((group==='LecturePlans'||group==='LabPlans')&&key==='Notes'){
   const names=[...new Set(state.Instructors.map(x=>normalizeName(x.DisplayName)).filter(Boolean))];
   const selected=splitTeacherNames(value);
   return `<div class="teacher-multi" data-teacher-group="${group}" data-teacher-row="${row}"><select data-action="weekly-teacher-add" data-group="${group}" data-row="${row}" aria-label="เพิ่มผู้สอนในสัปดาห์ ${row+1}"><option value="">＋ เลือกผู้สอนเพื่อเพิ่ม</option>${names.filter(x=>!selected.includes(x)).map(name=>`<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join('')}</select><div class="teacher-chips">${selected.map(name=>`<button type="button" class="chip" data-action="weekly-teacher-remove" data-group="${group}" data-row="${row}" data-value="${escapeHtml(name)}" title="นำ ${escapeHtml(name)} ออก">${escapeHtml(name)} ×</button>`).join('')}</div><div class="teacher-custom"><input type="text" data-action="weekly-teacher-custom" data-group="${group}" data-row="${row}" aria-label="พิมพ์ชื่อผู้สอนเพิ่มเติม" placeholder="ชื่อผู้สอนที่ไม่มีในรายการ"><button type="button" data-action="weekly-teacher-add-custom" data-group="${group}" data-row="${row}" class="btn btn-mini">เพิ่ม</button></div></div>`;
 }
 if((group==='LecturePlans'||group==='LabPlans')&&key==='TeachingMethods'||group==='Assessments'&&key==='AssessmentType'||group==='Resources'&&key==='ResourceType'){
   const choices=key==='TeachingMethods'?(group==='LecturePlans'?LECTURE_METHODS:LAB_METHODS):key==='AssessmentType'?ASSESSMENT_TYPES:RESOURCE_TYPES;
   const id=`choices-${group}-${row}-${key}`;
   return `<div class="editable-choice"><input type="text" list="${id}" ${attr} value="${escapeHtml(inputValue(value))}" placeholder="เลือกหรือพิมพ์รายการอื่น" aria-label="${escapeHtml(MAP[key]||key)}">${optionsDatalist(id,choices)}</div>`;
 }
 // Course information is always entered using plain text fields (no asterisk, number spinner or semester select).
 if(group!=='CourseInfo'&&SELECT[key])return `<select aria-label="${escapeHtml(MAP[key]||key)}" class="${cls}" ${attr}><option value="">— เลือก —</option>${SELECT[key].map(item=>`<option value="${escapeHtml(item)}" ${String(value)===String(item)?'selected':''}>${escapeHtml(item)}</option>`).join('')}${value&&!SELECT[key].includes(String(value))?`<option value="${escapeHtml(value)}" selected>${escapeHtml(value)}</option>`:''}</select>`;
 if(TEXTAREA.has(key))return `<textarea aria-label="${escapeHtml(MAP[key]||key)}" class="${cls}" ${attr}>${escapeHtml(inputValue(value))}</textarea>`;
 const htmlType=group==='CourseInfo'?'text':(type==='integer'||type==='number'?'number':key==='Url'?'url':'text');
 const step=type==='integer'?'1':type==='number'?'0.01':undefined;
 const placeholder=group==='CourseInfo'?'':(type==='array'?'CLO1, CLO2':'');
 return `<input aria-label="${escapeHtml(MAP[key]||key)}" type="${htmlType}" class="${cls}" ${group==='CourseInfo'?'inputmode="text" autocomplete="off"':step?`step="${step}"`:''} ${group!=='CourseInfo'&&(type==='number'||type==='integer')?'min="0"':''} ${attr} value="${escapeHtml(inputValue(value))}" placeholder="${placeholder}">`;
}


function fieldMarkup(group,key){const v=state[group]||{},required=contract.properties[group].required||[];return `<div class="field ${WIDE.has(key)?'wide':''} ${/Description/.test(key)?'full':''}"><label for="f-${group}-${key}">${escapeHtml(MAP[key]||key)}</label>${inputElement(group,key,v[key],'object')}<span class="micro">${escapeHtml(key)}</span></div>`;}
function formPanel(group,title,desc,keys=Object.keys(dataFields(group)),id=`group-${group}`){return `<section class="panel" id="${id}"><div class="panel-head"><div><h3>${escapeHtml(title)}</h3><div class="subhead">${escapeHtml(desc)}</div></div><span class="pill neutral">${keys.length} ช่องข้อมูล</span></div><div class="panel-body"><div class="form-grid">${keys.map(key=>fieldMarkup(group,key)).join('')}</div></div></section>`;}
const COURSE_GROUPS=[
 {id:'group-CourseInfo',title:'01 · ข้อมูลรายวิชาและภาคเรียน',desc:'ปีการศึกษาและภาคเรียนเป็นคนละช่อง โดยภาคเรียนอาจเป็น 1 หรือ 2',keys:['CourseCode','CourseTitleTh','CourseTitleEn','AcademicYear','Semester','Section']},
 {id:'course-credits',title:'02 · หน่วยกิตและชั่วโมงเรียน',desc:'จำนวนหน่วยกิตและชั่วโมงสอนต่อสัปดาห์',keys:['Credits','LectureHours','LabHours','SelfStudyHours']},
 {id:'course-descriptions',title:'03 · คำอธิบายรายวิชา',desc:'คำอธิบายรายวิชาภาษาไทยและภาษาอังกฤษ',keys:['CourseDescriptionTh','CourseDescriptionEn']}
];
function curriculumSelectMarkup(){return `<div class="field full"><label for="curriculum-pick">เลือกหลักสูตร</label><select id="curriculum-pick" data-action="curriculum-select" aria-label="เลือกหลักสูตร"><option value="">— เลือกหลักสูตรที่ใช้ PLO —</option>${curriculumMaster.map(c=>`<option value="${escapeHtml(c.curriculum_id)}" ${state.Curriculum.CurriculumCode===c.curriculum_id?'selected':''}>${escapeHtml(curriculumLabel(c))}</option>`).join('')}</select><span class="micro">ข้อมูลจาก curriculum_plos.json · เลือกแล้วระบบเติม PLO ให้อัตโนมัติ</span></div>`;}
function plosPage(){const selected=selectedCurriculum();const plos=state.PLOs||[];return `<div class="section-stack"><section class="panel"><div class="panel-head"><div><h3>เลือกหลักสูตรสำหรับ PLOs</h3><div class="subhead">ใช้รายการที่ให้ไว้โดยไม่ต้องพิมพ์ PLO เอง</div></div><span class="pill neutral">${curriculumMaster.length} หลักสูตร</span></div><div class="panel-body"><div class="form-grid">${curriculumSelectMarkup()}</div>${selected?`<div class="master-summary">${escapeHtml(selected.program_name)} · ${escapeHtml(selected.major||'ไม่ระบุสาขา')} · ${plos.length} PLOs</div>`:''}</div></section>${plos.length?`<section class="panel"><div class="panel-head"><div><h3>ผลลัพธ์การเรียนรู้ระดับหลักสูตร</h3><div class="subhead">แสดงข้อมูลจาก ${selected?'ไฟล์หลักสูตรที่เลือก':'Draft ที่นำเข้า'} · ดูอย่างเดียว</div></div><span class="pill neutral">${plos.length} รายการ</span></div><div class="plo-list">${plos.map(p=>`<div class="plo-item"><strong class="plo-code">${escapeHtml(p.PloCode)}</strong><div><div class="plo-description">${escapeHtml(p.DescriptionTh)}</div>${p.Category?`<div class="plo-category">${escapeHtml(p.Category)}</div>`:''}</div></div>`).join('')}</div></section>`:'<div class="notice">กรุณาเลือกหลักสูตรด้านบน ระบบจะแสดง PLOs ของหลักสูตรนั้นโดยอัตโนมัติ</div>'}</div>`;}
function instructorSelectMarkup(rec,row){
 const picked=masterTeacherIndex(rec),dept=activeTeacherDepartment(),visible=instructorMaster.map((x,i)=>({...x,i})).filter(x=>allDepartments||!dept||normalizeName(x.department)===normalizeName(dept)||x.i===picked);
 const manual=manualTeacherRows.has(row)||(picked===-1&&!!rec.DisplayName);
 return `<select data-action="instructor-select" data-row="${row}" aria-label="เลือกอาจารย์ผู้สอน แถว ${row+1}"><option value="">— เลือกผู้สอน —</option>${visible.map(t=>`<option value="${t.i}" ${!manual&&t.i===picked?'selected':''}>${escapeHtml(teacherDisplay(t))}${allDepartments||!dept?' · '+escapeHtml(t.department):''}</option>`).join('')}<option value="__manual__" ${manual?'selected':''}>＋ ไม่พบรายชื่อ / กรอกเอง</option></select>${manual?`<div class="manual-teacher"><input type="text" data-action="teacher-manual-name" data-row="${row}" value="${escapeHtml(rec.DisplayName||'')}" placeholder="คำนำหน้า ชื่อ นามสกุล"><input type="text" data-action="teacher-manual-department" data-row="${row}" value="${escapeHtml(rec.Department||'')}" placeholder="สาขาวิชา / หน่วยงาน"></div>`:rec.DisplayName?`<div class="teacher-current">${escapeHtml(rec.DisplayName)}</div>`:''}`;
}
function instructorsPage(){const dept=activeTeacherDepartment(),rows=state.Instructors,chosen=rows.filter(x=>isPopulated('Instructors',x)).length;
 const controls=`<section class="panel"><div class="panel-head"><div><h3>กรองรายชื่อผู้สอนตามหลักสูตร</h3><div class="subhead">ข้อมูลจาก instructors.json หรือเพิ่มผู้สอนที่ไม่อยู่ในรายการได้</div></div></div><div class="panel-body"><div class="form-grid">${curriculumSelectMarkup()}<div class="field wide"><label for="teacher-dept">ตัวกรองรายชื่อผู้สอน</label><select id="teacher-dept" data-action="teacher-scope"><option value="matched" ${!allDepartments?'selected':''}>${dept?escapeHtml('สาขา: '+dept):'ทุกสาขาวิชา (ยังไม่เลือกหลักสูตร)'}</option><option value="all" ${allDepartments?'selected':''}>แสดงรายชื่อทุกสาขาวิชา</option></select></div></div></div></section>`;
 return `<div class="section-stack">${controls}<section class="panel" id="group-Instructors"><div class="panel-head"><div><h3>ผู้รับผิดชอบรายวิชาและผู้สอน <span class="pill neutral">${chosen} คน</span></h3><div class="subhead">เลือกจากรายชื่อ หรือเลือก “ไม่พบรายชื่อ / กรอกเอง” · ผู้รับผิดชอบรายวิชาต้องมี 1 คน</div></div><button type="button" class="btn btn-mini btn-primary" data-action="add" data-group="Instructors">＋ เพิ่มผู้สอน</button></div><div class="table-wrap"><table class="editor-table instructor-editor"><thead><tr><th style="width:38px">#</th><th>ชื่อผู้สอน</th><th>สาขาวิชา</th><th>ผู้รับผิดชอบ</th><th>ลบ</th></tr></thead><tbody>${rows.length?rows.map((r,i)=>`<tr><td class="row-no">${i+1}</td><td>${instructorSelectMarkup(r,i)}</td><td><span class="teacher-department">${escapeHtml(r.Department||'—')}</span></td><td class="teacher-check">${inputElement('Instructors','IsResponsibleInstructor',r.IsResponsibleInstructor,'table',i,true)}</td><td><button class="del" data-action="delete" data-group="Instructors" data-row="${i}" aria-label="ลบผู้สอนแถว ${i+1}">×</button></td></tr>`).join(''):'<tr><td colspan="5" class="empty">ยังไม่มีผู้สอน กด “เพิ่มผู้สอน” เพื่อเริ่มกรอก</td></tr>'}</tbody></table></div><div class="table-note">Master รายชื่อยังไม่มี StaffId และ Email · ระบบไม่สมมติรหัสบุคลากรหรืออีเมลขึ้นมา</div></section></div>`;
}


function tablePanel(group,title,desc,actions=''){
 const keys=visibleCols(group),rows=state[group]||[],count=rows.filter(r=>isPopulated(group,r)).length;
 const label=key=>group==='LecturePlans'||group==='LabPlans'?(key==='Notes'?'ผู้สอน':MAP[key]||key):MAP[key]||key;
 return `<section class="panel" id="group-${group}"><div class="panel-head"><div><h3>${escapeHtml(title)} <span class="pill neutral">${count} รายการ</span></h3><div class="subhead">${escapeHtml(desc)}</div></div><div class="inline-row">${actions}<button class="btn btn-mini btn-primary" data-action="add" data-group="${group}">＋ เพิ่มรายการ</button></div></div><div class="table-wrap"><table class="editor-table section-table table-${group}"><thead><tr><th style="width:36px">#</th>${keys.map(k=>`<th>${escapeHtml(label(k))}</th>`).join('')}<th>ลบ</th></tr></thead><tbody>${rows.length?rows.map((r,i)=>`<tr><td class="row-no">${i+1}</td>${keys.map(key=>`<td>${inputElement(group,key,r[key],'table',i,true)}</td>`).join('')}<td><button class="del" data-action="delete" data-group="${group}" data-row="${i}" title="ลบแถว ${i+1}" aria-label="ลบแถว ${i+1}">×</button></td></tr>`).join(''):`<tr><td colspan="${keys.length+2}" class="empty">ยังไม่มีข้อมูล กด “เพิ่มรายการ” เพื่อเริ่มกรอก</td></tr>`}</tbody></table></div><div class="table-note">${group==='LecturePlans'||group==='LabPlans'?'มีช่องสัปดาห์ไว้ 15 สัปดาห์ · เลือกวิธีสอนและผู้สอนจากรายการหรือพิมพ์เพิ่มเติมได้':group==='CLOs'?'เลือก PLO ได้หลายรายการโดยกดเพิ่มทีละรหัส และกด × เพื่อนำออก':group==='Assessments'?'น้ำหนักรวมการประเมินต้องเท่ากับ 100% · CLO คั่นด้วยเครื่องหมายจุลภาค':'กรอกข้อมูลตามที่รายวิชาใช้จริง'}</div></section>`;
}


function coursePage(){return `<div class="section-stack"><div class="notice">ข้อมูลจะอยู่ในหน้านี้จนกว่าจะปิดหรือรีเฟรช หากต้องการกลับมาทำต่อให้กด “บันทึก JSON” แล้วเก็บไฟล์ไว้ เมื่อเปิดครั้งถัดไปให้กด “เปิด JSON” · ระบุหน่วยกิตเป็นตัวเลขเดียว เช่น 3 และชั่วโมงเรียนเป็น 2, 2, 5 ระบบจะจัดรูปแบบ 3(2-2-5) ในขั้นตอนสร้าง DOCX</div>${COURSE_GROUPS.map(g=>formPanel('CourseInfo',g.title,g.desc,g.keys,g.id)).join('')}</div>`;}

function weeklyPage(){return `<div class="section-stack"><div class="notice">กรอกหัวข้อและกิจกรรมในช่องเดียว · เลือกชื่อผู้สอนได้หลายคนต่อสัปดาห์ และเพิ่มรายชื่ออื่นเองได้</div><div class="inline-row"><div class="switchbar"><button data-action="week-switch" data-value="LecturePlans" class="${weeklyKind==='LecturePlans'?'active':''}">บรรยาย (Lecture)</button><button data-action="week-switch" data-value="LabPlans" class="${weeklyKind==='LabPlans'?'active':''}">ปฏิบัติการ (Lab)</button></div><span class="pill neutral">${weeklyKind==='LecturePlans'?'Lecture Plan':'Laboratory Plan'}</span></div>${tablePanel(weeklyKind,weeklyKind==='LecturePlans'?'แผนการสอนภาคบรรยาย':'แผนการสอนภาคปฏิบัติ','หัวข้อ/กิจกรรม วิธีสอน รหัส CLO และผู้สอน',`<button class="btn btn-mini" data-action="fill-weeks" data-group="${weeklyKind}">＋ เติมให้ครบ 15 สัปดาห์</button>`)}</div>`;}
function assessmentPage(){return `<div class="section-stack"><div class="notice warn">น้ำหนักคะแนนประเมินรวม 100% · CLO ที่เชื่อมโยงคั่นด้วยจุลภาค · กำหนดเกณฑ์คะแนนขั้นต่ำตามระบบเกรดที่ใช้</div>${tablePanel('Assessments','รายการวัดและประเมินผล','ประเภทประเมินเป็นภาษาไทย เลือกจากรายการหรือระบุเองได้')}<section class="panel"><div class="panel-head"><div><h3>เกณฑ์ตัดเกรด</h3><div class="subhead">กรอกเฉพาะคะแนนขั้นต่ำของแต่ละเกรดตามตัวอย่าง ไม่ต้องระบุคะแนนสูงสุด</div></div></div><div class="panel-body grade-layout"><div class="field grade-mode-field"><label for="grade-mode">ระบบเกรด</label><select id="grade-mode" data-action="grade-mode"><option value="" ${!gradeMode()?'selected':''}>— เลือกระบบเกรด —</option><option value="abc" ${gradeMode()==='abc'?'selected':''}>A, B+, B, C+, C, D+, D, F</option><option value="su" ${gradeMode()==='su'?'selected':''}>S / U</option></select><span class="micro">เลือกแล้วจึงกรอกคะแนนขั้นต่ำในตาราง</span></div>${gradeCutoffTable()}</div></section>${tablePanel('Resources','หนังสือและแหล่งเรียนรู้','ประเภทแหล่งเรียนรู้ภาษาไทย เลือกจากรายการหรือระบุเองได้')}</div>`;}


function render(){const t=TABS.find(x=>x.id===currentTab);el('nav').innerHTML=TABS.map((x,i)=>`<button class="${x.id===currentTab?'active':''}" data-action="tab" data-value="${x.id}" ${x.id===currentTab?'aria-current="step"':''}><span class="num">${i+1}</span><span>${escapeHtml(x.name)}</span></button>`).join('');el('tab-title').textContent=t.name;el('tab-desc').textContent=t.desc;el('tab-number').textContent=`SECTION ${TABS.findIndex(x=>x.id===currentTab)+1} / 6`;
switch(currentTab){case 'course':el('panel-content').innerHTML=coursePage();break;case 'plos':el('panel-content').innerHTML=plosPage();break;case 'instructors':el('panel-content').innerHTML=instructorsPage();break;case 'clos':el('panel-content').innerHTML=`<div class="section-stack"><div class="notice">เลือกรหัส PLO ที่เชื่อมโยงจากหลักสูตรในแท็บ PLOs สามารถเลือกหลายรหัสต่อ CLO ได้</div>${tablePanel('CLOs','ผลลัพธ์การเรียนรู้รายวิชา','คำอธิบาย CLO และ PLO ที่เชื่อมโยง')}</div>`;break;case 'weekly':el('panel-content').innerHTML=weeklyPage();break;case 'assessment':el('panel-content').innerHTML=assessmentPage();break;}
refreshHeader();}

function refreshHeader(){el('storage-label').textContent='บันทึกเป็นไฟล์ JSON เท่านั้น';}
function toast(message){const root=el('toast');root.textContent=message;root.classList.remove('hidden');clearTimeout(toast._timer);toast._timer=setTimeout(()=>root.classList.add('hidden'),3800);}
// Keep the existing event handlers but replace autosave with an unsaved-changes indicator.
function scheduleSave(){
  unsavedChanges=true;
  el('save-status').textContent='ยังไม่ได้บันทึกการแก้ไขลง JSON';
}
function resetSavedStatus(text){
  unsavedChanges=false;
  el('save-status').textContent=text;
}
function confirmDiscard(){
  return !unsavedChanges || confirm('มีข้อมูลที่ยังไม่ได้บันทึกเป็นไฟล์ JSON หากดำเนินการต่อการแก้ไขเหล่านี้จะหายไป ต้องการดำเนินการต่อหรือไม่?');
}
function tab(id){currentTab=id;render();el('panel-content').scrollIntoView({behavior:'smooth',block:'start'});}
function onInput(event){const t=event.target;
if(t.dataset.action==='curriculum-select'&&event.type==='change'){
  if(!t.value){t.value=state.Curriculum.CurriculumCode||'';return;}
  if(selectCurriculum(t.value)){el('validation').classList.remove('visible');showingErrors=false;render();scheduleSave();}else{t.value=state.Curriculum.CurriculumCode||'';}return;
}
if(t.dataset.action==='teacher-scope'&&event.type==='change'){allDepartments=t.value==='all';render();return;}
if(t.dataset.action==='grade-mode'&&event.type==='change'){
 const mode=t.value;
 if(!mode)return;
 if(state.GradeScale.length&&!confirm('การเปลี่ยนรูปแบบเกรดจะแทนที่เกณฑ์เดิม กรุณาบันทึก JSON หากต้องการเก็บข้อมูลเดิม ยืนยันหรือไม่?')){render();return;}
 state.GradeScale=(mode==='su'?GRADE_SU:GRADE_ABC).map(Grade=>({...blankRecord('GradeScale'),Grade}));updateGradeCutoffs(mode);render();scheduleSave();return;
}
if(t.dataset.action==='weekly-teacher-custom')return;
if(t.dataset.action==='grade-cutoff' && (event.type==='change'||event.type==='input')){
 const grade=t.dataset.value, mode=gradeMode();
 const record=state.GradeScale.find(x=>x.Grade===grade);
 if(!record || grade==='F' || grade==='U' || !mode)return;
 const raw=t.value;
 record.MinimumScore=raw===''?'':Number(raw);
 // Only rebuild derived maximum scores on change; avoids losing input focus.
 if(event.type==='change'){updateGradeCutoffs(mode);render();}
 scheduleSave();return;
}
if(t.dataset.action==='weekly-teacher-add'&&event.type==='change'){
 const group=t.dataset.group,row=Number(t.dataset.row),value=normalizeName(t.value);
 if(value)setWeeklyTeachers(group,row,[...splitTeacherNames(state[group][row].Notes),value]);return;
}
if(t.dataset.action==='plo-add'&&event.type==='change'){
 if(!t.value)return;const r=state.CLOs[Number(t.dataset.row)];if(r){r.MappedPloCodes=[...new Set([...(r.MappedPloCodes||[]),t.value])];render();scheduleSave();}return;
}
if(t.dataset.action==='teacher-manual-name'){
 const row=Number(t.dataset.row),r=state.Instructors[row];if(!r)return;
 const name=t.value.trim();r.DisplayName=name;r.Prefix='';const parts=normalizeName(name).split(' ');r.LastName=parts.length>1?parts.pop():'';r.FirstName=parts.join(' ');r.StaffId='';r.Email='';scheduleSave();return;
}
if(t.dataset.action==='teacher-manual-department'){
 const r=state.Instructors[Number(t.dataset.row)];if(r){r.Department=t.value;r.StaffId='';r.Email='';scheduleSave();}return;
}
if(t.dataset.action==='instructor-select'&&event.type==='change'){
  const index=Number(t.value),row=Number(t.dataset.row),teacher=t.value!==''&&Number.isInteger(index)?instructorMaster[index]:null;
  if(!state.Instructors[row])return;if(t.value==='__manual__'){manualTeacherRows.add(row);const r=state.Instructors[row];r.StaffId='';r.Email='';render();scheduleSave();return;}if(!teacher)return;manualTeacherRows.delete(row);
  const r=state.Instructors[row];const prev=normalizeName(r.DisplayName);
  const parts=normalizeName(teacher.name).split(' ');
  const last=parts.length>1?parts.pop():'';
  const first=parts.join(' ');
  r.Prefix=teacher.title_prefix||'';r.FirstName=first;r.LastName=last;r.DisplayName=teacherDisplay(teacher);r.Department=teacher.department||'';
  if(prev!==normalizeName(r.DisplayName)){r.StaffId='';r.Email='';}
  el('validation').classList.remove('visible');showingErrors=false;render();scheduleSave();return;
}
if(!t.dataset.group)return;
// "กำหนดเอง" is an action in the dropdown, never a saved teaching/assessment/resource value.
// The same input remains editable so users can type any Thai method/category.
if((t.dataset.key==='TeachingMethods'&&['LecturePlans','LabPlans'].includes(t.dataset.group)) ||
   (t.dataset.key==='AssessmentType'&&t.dataset.group==='Assessments') ||
   (t.dataset.key==='ResourceType'&&t.dataset.group==='Resources')){
 if(t.value.trim()==='กำหนดเอง'){
   t.value='';t.placeholder=t.dataset.key==='TeachingMethods'?'ระบุวิธีการสอนเอง':t.dataset.key==='ResourceType'?'ระบุประเภทแหล่งเรียนรู้เอง':'ระบุประเภทประเมินเอง';
   t.focus();
   toast('พิมพ์รายการที่ต้องการในช่องนี้ได้เลย');
 }
}
let {group,key,scope,row}=t.dataset,v=t.type==='checkbox'?t.checked:t.value,typ=getArrayType(group,key);if(scope==='object')state[group][key]=normalizedInput(v,typ);else{if(!state[group][Number(row)])return;state[group][Number(row)][key]=normalizedInput(v,typ);}if((group==='LecturePlans'||group==='LabPlans')&&key==='Topic'&&scope==='table')state[group][Number(row)].LearningActivities='';refreshHeader();scheduleSave();if(showingErrors){el('validation').classList.remove('visible');showingErrors=false;}}
function validate(data){const errors=[], warnings=[],issue=(severity,group,message,field='')=>({severity,group,message,field,tab:GROUP_TAB[group]||'course'});const error=(g,m,f)=>errors.push(issue('error',g,m,f));const warn=(g,m,f)=>warnings.push(issue('warning',g,m,f));
if(data.SchemaVersion!=='1.0.0')error('CourseInfo','SchemaVersion ต้องเป็น 1.0.0');
if(!data.OfferingId||!new RegExp(contract.properties.OfferingId.pattern).test(data.OfferingId))error('CourseInfo','รหัส OfferingId ยังไม่สมบูรณ์ (CourseCode–Semester–ปี พ.ศ.–SECxx)');
for(const group of SECTION_KEYS){const def=contract.properties[group],items=def.type==='object'?[data[group]]:(data[group]||[]),spec=def.type==='object'?def:def.items;items.forEach((r,i)=>{const title=def.type==='object'?group:`${group} แถว ${i+1}`;for(const k of spec.required||[]){const v=r?.[k];if(v===undefined||v===null||typeof v==='string'&&!v.trim())error(group,`${title}: กรุณาระบุ ${MAP[k]||k}`,k);}for(const [k,v] of Object.entries(r||{})){const prop=spec.properties[k];if(!prop){error(group,`${title}: ฟิลด์ไม่รู้จัก ${k}`,k);continue;}if(v===null){error(group,`${title}: ${MAP[k]||k} ต้องเป็นตัวเลขที่ถูกต้อง`,k);continue;}if(prop.type==='integer'&&(!Number.isInteger(v)))error(group,`${title}: ${MAP[k]||k} ต้องเป็นจำนวนเต็ม`,k);if(prop.type==='number'&&(typeof v!=='number'||!Number.isFinite(v)))error(group,`${title}: ${MAP[k]||k} ต้องเป็นตัวเลข`,k);if(prop.type==='string'&&typeof v!=='string')error(group,`${title}: ${MAP[k]||k} ต้องเป็นข้อความ`,k);if(prop.type==='boolean'&&typeof v!=='boolean')error(group,`${title}: ${MAP[k]||k} ต้องเป็นใช่/ไม่ใช่`,k);if(prop.type==='array'&&(!Array.isArray(v)||v.some(x=>typeof x!=='string')))error(group,`${title}: ${MAP[k]||k} ต้องเป็นรายการรหัส`,k);}});}
const course=data.CourseInfo; if(course.CourseCode&&!/^[A-Za-z0-9_-]+$/.test(course.CourseCode))error('CourseInfo','รหัสรายวิชาต้องเป็นอักษรอังกฤษ ตัวเลข - หรือ _','CourseCode');if(course.AcademicYear!==undefined&&(course.AcademicYear<2400||course.AcademicYear>2700))error('CourseInfo','ปีการศึกษาควรใช้ปี พ.ศ. (เช่น 2569)','AcademicYear');if(course.Section&&!/^[A-Za-z0-9]+$/.test(course.Section))error('CourseInfo','Section ต้องไม่มีช่องว่างหรือสัญลักษณ์พิเศษ','Section');
for(const cfg of COURSE_GROUPS)for(const key of cfg.keys){const v=state.CourseInfo[key];if(v===undefined||v===null||String(v).trim()==='')error('CourseInfo',`กรุณากรอก ${MAP[key]||key}` ,key);}
if(course.Credits&&!/^\d+(?:\.\d+)?$/.test(course.Credits))error('CourseInfo','หน่วยกิตให้ใส่ตัวเลขเดียว เช่น 3 (ไม่ต้องใส่ 3(2-2-5))','Credits');
const instructors=data.Instructors;if(!instructors.length)error('Instructors','ต้องระบุผู้สอนอย่างน้อย 1 คน');if(instructors.filter(x=>x.IsResponsibleInstructor).length!==1)error('Instructors','ต้องเลือกผู้รับผิดชอบรายวิชาเพียง 1 คน','IsResponsibleInstructor');
for(const [i,x] of instructors.entries()){if(!x.StaffId&&!x.Email)warn('Instructors',`ผู้สอนแถว ${i+1}: ยังไม่มี StaffId/Email ในข้อมูลต้นทาง กรุณาเติมจาก REG ก่อนนำเข้าระบบ Blazor`,'StaffId');if(!x.DisplayName&&!(x.FirstName&&x.LastName))error('Instructors',`ผู้สอนแถว ${i+1}: กรุณาระบุชื่อแสดงผล หรือชื่อและนามสกุล`,'DisplayName');if(x.Email&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(x.Email))error('Instructors',`อีเมลผู้สอนแถว ${i+1} ไม่ถูกต้อง`,'Email');}

const unique=(group,key)=>{const seen=new Set();for(const r of data[group]){const v=String(r[key]??'').toUpperCase();if(!v)continue;if(seen.has(v))error(group,`รหัส ${v} ซ้ำกัน`,key);seen.add(v);}return seen;};const plo=unique('PLOs','PloCode'),clo=unique('CLOs','CloCode');
for(const r of data.CLOs){for(const ref of r.MappedPloCodes||[])if(!plo.has(ref.toUpperCase()))error('CLOs',`CLO ${r.CloCode||''} อ้างอิง PLO ที่ไม่พบ: ${ref}`,'MappedPloCodes');}
for(const group of ['LecturePlans','LabPlans','Assessments'])for(const r of data[group])for(const ref of r.MappedCloCodes||[])if(!clo.has(ref.toUpperCase()))error(group,`อ้างอิง CLO ที่ไม่พบ: ${ref}`,'MappedCloCodes');
for(const group of ['LecturePlans','LabPlans']){const weeks=new Set();for(const r of data[group]){if(!Number.isInteger(r.WeekNumber)||r.WeekNumber<1||r.WeekNumber>52)error(group,'สัปดาห์ต้องเป็นจำนวนเต็มระหว่าง 1–52','WeekNumber');if(weeks.has(r.WeekNumber))error(group,`สัปดาห์ที่ ${r.WeekNumber} ซ้ำกัน`,'WeekNumber');weeks.add(r.WeekNumber);}if(Number(course[group==='LecturePlans'?'LectureHours':'LabHours'])>0&&data[group].length<15)warn(group,`แผน${group==='LecturePlans'?'บรรยาย':'ปฏิบัติ'}มี ${data[group].length} สัปดาห์ ควรตรวจสอบให้ครอบคลุมตามปฏิทิน`);}
if(!data.PLOs.length)warn('PLOs','ยังไม่มี PLO ของหลักสูตร');if(!data.CLOs.length)warn('CLOs','ยังไม่มี CLO ของรายวิชา');
const sums=data.Assessments.reduce((n,x)=>n+(Number(x.WeightPercent)||0),0);if(!data.Assessments.length)error('Assessments','ต้องมีรายการประเมินอย่างน้อย 1 รายการ');if(Math.abs(sums-100)>.01)error('Assessments',`น้ำหนักคะแนนรวมต้องเท่ากับ 100% (ปัจจุบัน ${Math.round(sums*100)/100}%)`,'WeightPercent');for(const r of data.Assessments){if(r.WeightPercent<0||r.WeightPercent>100)error('Assessments','น้ำหนักคะแนนต้องอยู่ในช่วง 0–100','WeightPercent');}
const clock=(v)=>!v||/^([01]\d|2[0-3]):[0-5]\d$/.test(v);for(const g of ['ClassMeetings','Exams'])for(const r of data[g]){if(!clock(r.StartTime)||!clock(r.EndTime))error(g,'เวลาให้กรอก HH:MM แบบ 24 ชั่วโมง');if(r.StartTime&&r.EndTime&&r.StartTime>=r.EndTime)error(g,'เวลาเริ่มต้องน้อยกว่าเวลาสิ้นสุด');if(g==='Exams'&&r.ExamDate&&!/^\d{4}-\d{2}-\d{2}$/.test(r.ExamDate))error(g,'วันที่สอบต้องเป็น YYYY-MM-DD');}
if(!data.GradeScale.length)warn('GradeScale','ยังไม่เลือกรูปแบบเกรด A–F หรือ S/U');
else {
 const grades=data.GradeScale.map(x=>x.Grade),mode=grades.some(x=>GRADE_SU.includes(x))?'su':'abc', expected=mode==='su'?GRADE_SU:GRADE_ABC;
 if(grades.length!==expected.length || grades.some((g,i)=>g!==expected[i]))error('GradeScale','รูปแบบเกรดต้องเป็นชุด A–F หรือ S/U เท่านั้น','Grade');
 for(let i=0;i<expected.length;i++){
   const r=data.GradeScale[i]||{};
   if(r.MinimumScore===undefined||r.MaximumScore===undefined){error('GradeScale',`กรุณากรอกคะแนนขั้นต่ำของเกรด ${expected[i]||'?'} ให้ครบ`,'MinimumScore');continue;}
   if(r.MinimumScore<0||r.MinimumScore>100||r.MaximumScore<0||r.MaximumScore>100||r.MinimumScore>r.MaximumScore)error('GradeScale',`ช่วงคะแนนเกรด ${r.Grade} ต้องอยู่ในช่วง 0–100`,'MinimumScore');
   if(i>0 && i<expected.length-1 && r.MinimumScore>=data.GradeScale[i-1]?.MinimumScore)error('GradeScale',`คะแนนขั้นต่ำ ${r.Grade} ต้องต่ำกว่า ${expected[i-1]}`,'MinimumScore');
   if(i===expected.length-2 && r.MinimumScore<=0)error('GradeScale',`คะแนนขั้นต่ำ ${r.Grade} ต้องมากกว่า 0 เพื่อแยกจาก ${expected[i+1]}`,'MinimumScore');
 }
}

return {errors,warnings};}
function showValidation(){const r=validate(payload());showingErrors=true;el('validation').classList.add('visible');el('issue-heading').textContent=`ผลตรวจสอบ · ${r.errors.length} ข้อผิดพลาด · ${r.warnings.length} ข้อควรตรวจ`;let html=[...r.errors,...r.warnings].map(x=>`<button class="issue ${x.severity==='warning'?'warning':''}" data-action="issue-tab" data-value="${x.tab}" data-group="${x.group}"><div class="severity">${x.severity==='error'?'ERROR':'เตือน'}</div><div>${escapeHtml(x.message)}<div class="where">${escapeHtml(x.group)} ${x.field?'· '+escapeHtml(x.field):''}</div></div></button>`).join('');el('issue-list').innerHTML=html||'<div class="issue ok">✓ ข้อมูลผ่านการตรวจสอบเงื่อนไขที่กำหนด พร้อมส่งออก JSON</div>';el('validation').scrollIntoView({behavior:'smooth',block:'start'});return r;}
function download(blob,filename){const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500);}
// The same contract is used for incomplete and validated JSON. Incomplete
// data remains importable but is NOT claimed to be schema-valid for Blazor.
function saveJSON(){
  const d=payload();
  const c=state.CourseInfo||{};
  const code=safePart(c.CourseCode)||'UNNAMED';
  const year=/^\d{4}$/.test(String(c.AcademicYear||''))?String(c.AcademicYear):'YEAR';
  const term=safePart(c.Semester)||'TERM';
  const section=safePart(c.Section).replace(/^SEC/,'')||'SECTION';
  const filename=`SYLLABUS_${code}_${year}_${term}_${section}.json`;
  download(new Blob([JSON.stringify(d,null,2)],{type:'application/json;charset=utf-8'}),filename);
  resetSavedStatus('เริ่มดาวน์โหลด JSON แล้ว · ตรวจสอบไฟล์ใน Downloads');
  toast('เริ่มดาวน์โหลด '+filename+' · บันทึกได้แม้ยังตรวจสอบไม่ผ่าน');
}
async function importJSON(file){
 if(!file)return;
 try{
   if(file.size>5*1024*1024)throw new Error('ไฟล์ใหญ่เกิน 5 MB');
   const obj=JSON.parse(await file.text());
   if(obj.SchemaVersion!=='1.0.0')throw new Error('รองรับ SchemaVersion 1.0.0 เท่านั้น');
   if(!obj.CourseInfo||typeof obj.CourseInfo!=='object'||Array.isArray(obj.CourseInfo)||!Array.isArray(obj.Instructors))throw new Error('ไม่ใช่ไฟล์ Syllabus JSON v1');
   if(!confirmDiscard())return;
   state=fromPayload(obj);
   lastLoadedFile=file.name;
   manualTeacherRows.clear();currentTab='course';weeklyKind='LecturePlans';showingErrors=false;
   el('validation').classList.remove('visible');render();
   resetSavedStatus('เปิดไฟล์ '+file.name+' แล้ว');
   toast('เปิด JSON สำเร็จ · แก้ไขข้อมูลแล้วกดบันทึก JSON อีกครั้ง');
 }catch(e){toast('เปิด JSON ไม่สำเร็จ: '+e.message);}
 finally{el('file-import').value='';}
}
function newDraft(){
 if(!confirmDiscard())return;
 state=blankData();lastLoadedFile='';manualTeacherRows.clear();currentTab='course';weeklyKind='LecturePlans';showingErrors=false;
 el('validation').classList.remove('visible');render();resetSavedStatus('เริ่มรายวิชาใหม่ · ยังไม่ได้บันทึก JSON');toast('เริ่มรายวิชาใหม่แล้ว');
}
async function clickAction(e){const b=e.target.closest('[data-action]');if(!b)return;const {action,group,row,value}=b.dataset;if(action==='weekly-teacher-remove'){
 const r=state[group]?.[Number(row)];if(r)setWeeklyTeachers(group,Number(row),splitTeacherNames(r.Notes).filter(x=>x!==value));return;
}if(action==='weekly-teacher-add-custom'){
 const root=b.closest('.teacher-multi'),input=root?.querySelector('[data-action="weekly-teacher-custom"]');
 const name=normalizeName(input?.value);if(!name){input?.focus();return;}
 const rec=state[group]?.[Number(row)];if(rec)setWeeklyTeachers(group,Number(row),[...splitTeacherNames(rec.Notes),name]);return;
}if(b.closest('.tools-dropdown'))el('tools-menu')?.removeAttribute('open');if(action==='tab'){tab(value);return;}if(action==='plo-remove'){const r=state.CLOs[Number(row)];if(r){r.MappedPloCodes=(r.MappedPloCodes||[]).filter(x=>x!==value);render();scheduleSave();}return;}if(action==='jump-group'){document.getElementById(value)?.scrollIntoView({behavior:'smooth',block:'start'});return;}if(action==='add'){const d=blankRecord(group);if(group==='LecturePlans'||group==='LabPlans')d.WeekNumber=Math.max(0,...state[group].map(x=>Number(x.WeekNumber)||0))+1;state[group].push(d);render();scheduleSave();return;}if(action==='delete'){if(group==='Instructors')manualTeacherRows.clear();if(!confirm(`ลบรายการที่ ${Number(row)+1} ใน ${group}?`))return;state[group].splice(Number(row),1);ensureStarterRows(state);render();scheduleSave();return;}if(action==='fill-weeks'){const exists=new Set(state[group].map(x=>Number(x.WeekNumber)));for(let i=1;i<=15;i++)if(!exists.has(i))state[group].push({...blankRecord(group),WeekNumber:i});state[group].sort((a,b)=>Number(a.WeekNumber)-Number(b.WeekNumber));render();scheduleSave();return;}if(action==='week-switch'){weeklyKind=value;render();return;}if(action==='issue-tab'){if(group==='LabPlans')weeklyKind='LabPlans';tab(value);setTimeout(()=>el('group-'+group)?.scrollIntoView({behavior:'smooth',block:'start'}),120);return;}if(action==='validate'){showValidation();return;}
if(action==='save'){saveJSON();return;}
if(action==='import'){el('file-import').click();return;}
if(action==='new'){newDraft();return;}
}
function init(){
 state=blankData();manualTeacherRows.clear();currentTab='course';
 render();resetSavedStatus('ยังไม่ได้บันทึก JSON');
 document.addEventListener('input',onInput);
 document.addEventListener('change',onInput);
 document.addEventListener('click',clickAction);
 el('file-import').addEventListener('change',e=>importJSON(e.target.files?.[0]));
 document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();saveJSON();}});
 window.addEventListener('beforeunload',e=>{if(unsavedChanges){e.preventDefault();e.returnValue='';}});
}

try{init();}catch(e){console.error(e);toast('เริ่มต้นแอปไม่สำเร็จ กรุณารีเฟรชหน้าเว็บ');}
})();
