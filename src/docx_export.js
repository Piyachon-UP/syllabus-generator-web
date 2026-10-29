/* Smart Syllabus Generator: self-contained browser DOCX generator.
   No CDN, server, npm dependencies or mutation of syllabus JSON.
   Produces valid WordprocessingML in a ZIP archive (STORE method). */
(function(root, factory){
  const api=factory();
  if(typeof module==='object' && module.exports)module.exports=api;
  if(root)root.SyllabusDocx=api;
})(typeof window!=='undefined'?window:undefined, function(){
'use strict';
const encoder=new TextEncoder();
const TYPE='application/vnd.openxmlformats-officedocument.wordprocessingml.document';
const asText=v=>v==null?'':String(v);
const value=v=>asText(v).trim()||'—';
const xml=v=>asText(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&apos;');
const list=v=>Array.isArray(v)?v.filter(x=>x!=null&&x!=='').join(', '):asText(v);
function r(text){const parts=asText(text).replace(/\r\n/g,'\n').replace(/\r/g,'\n').split('\n');return parts.map((t,i)=>(i?'<w:br/>':'')+`<w:t xml:space="preserve">${xml(t)}</w:t>`).join('');}
function p(text,style='Normal'){
  return `<w:p><w:pPr><w:pStyle w:val="${style}"/></w:pPr><w:r>${r(text)}</w:r></w:p>`;
}
function tc(text,width,heading=false){
 const shading=heading?'D9EAF3':'FFFFFF';
 return `<w:tc><w:tcPr><w:tcW w:w="${width}" w:type="dxa"/><w:shd w:fill="${shading}"/><w:tcMar><w:top w:w="84" w:type="dxa"/><w:left w:w="95" w:type="dxa"/><w:bottom w:w="84" w:type="dxa"/><w:right w:w="95" w:type="dxa"/></w:tcMar></w:tcPr>${p(value(text),heading?'TableHead':'TableBody')}</w:tc>`;
}
function table(heads,rows,widths){
 if(!rows?.length)return p('ไม่มีข้อมูล');
 if(!widths){const one=Math.floor(9400/heads.length);widths=heads.map((_,i)=>i===heads.length-1?9400-one*(heads.length-1):one);}
 const grid=widths.map(w=>`<w:gridCol w:w="${w}"/>`).join('');
 const row=(cells,heading=false)=>`<w:tr>${heading?'<w:trPr><w:tblHeader w:val="true"/></w:trPr>':''}${heads.map((_,i)=>tc(cells[i],widths[i],heading)).join('')}</w:tr>`;
 return `<w:tbl><w:tblPr><w:tblW w:w="9400" w:type="dxa"/><w:tblLayout w:type="fixed"/><w:tblBorders><w:top w:val="single" w:sz="4" w:color="C6D4E0"/><w:left w:val="single" w:sz="4" w:color="C6D4E0"/><w:bottom w:val="single" w:sz="4" w:color="C6D4E0"/><w:right w:val="single" w:sz="4" w:color="C6D4E0"/><w:insideH w:val="single" w:sz="4" w:color="D7E2EA"/><w:insideV w:val="single" w:sz="4" w:color="D7E2EA"/></w:tblBorders></w:tblPr><w:tblGrid>${grid}</w:tblGrid>${row(heads,true)}${rows.map(x=>row(x)).join('')}</w:tbl>`;
}
const heading=(text)=>p(text,'Heading1');
const subheading=(text)=>p(text,'Heading2');
function displayDate(v){if(!v)return '—';return String(v);}
// Date is stored as Gregorian YYYY-MM-DD; display the selected date in Buddhist Era for Thai documents.
function displayThaiDate(v){
 const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(String(v||''));
 if(!m)return value(v);
 const [year,month,day]=m.slice(1).map(Number);
 const date=new Date(Date.UTC(year,month-1,day));
 if(date.getUTCFullYear()!==year||date.getUTCMonth()!==month-1||date.getUTCDate()!==day)return value(v);
 return `${String(day).padStart(2,'0')}/${String(month).padStart(2,'0')}/${year+543}`;
}
function cleanCourseData(data){if(!data||typeof data!=='object')throw Error('ไม่มีข้อมูลรายวิชา');const s=data.SchemaVersion;if(s!=='1.0.0')throw Error('รองรับ SchemaVersion 1.0.0 เท่านั้น');return data;}
function documentXML(data){
 data=cleanCourseData(data);
 const ci=data.CourseInfo||{}, cur=data.Curriculum||{},plos=data.PLOs||[],clos=data.CLOs||[];
 const teachers=data.Instructors||[],lecture=data.LecturePlans||[],lab=data.LabPlans||[],assess=data.Assessments||[],grades=data.GradeScale||[],resource=data.Resources||[];
 const meeting=data.ClassMeetings||[], exams=data.Exams||[],students=data.StudentGroups||[];
 const required=!!(ci.CourseCode && ci.CourseTitleTh && ci.AcademicYear && ci.Semester);
 const credits=[value(ci.Credits),'(',asText(ci.LectureHours||0),'-',asText(ci.LabHours||0),'-',asText(ci.SelfStudyHours||0),')'].join('');
 const b=[];
 b.push(p('รายละเอียดรายวิชา','Title'));
 b.push(p('Course Syllabus','Subtitle'));
 b.push(p('คณะวิทยาศาสตร์ · มหาวิทยาลัยพะเยา','Centered'));
 b.push(p(value(ci.CourseCode)+'  '+value(ci.CourseTitleTh),'CourseTitle'));
 if(ci.CourseTitleEn)b.push(p(ci.CourseTitleEn,'Centered'));
 if(!required)b.push(p('ฉบับร่าง — ข้อมูลส่วนหัวรายวิชายังไม่ครบ กรุณาตรวจสอบก่อนใช้งาน','Warning'));
 b.push(heading('1. ข้อมูลรายวิชา'));
 b.push(table(['รายการ','รายละเอียด'],[
 ['รหัสรายวิชา',value(ci.CourseCode)],['ชื่อรายวิชาภาษาไทย',value(ci.CourseTitleTh)],['ชื่อรายวิชาภาษาอังกฤษ',value(ci.CourseTitleEn)],['หน่วยกิต',credits],['ปีการศึกษา / ภาคเรียน',`${value(ci.AcademicYear)} / ${value(ci.Semester)}`],['กลุ่มเรียน',value(ci.Section)],...(ci.LastUpdatedDate?[['วันที่บันทึก/ปรับปรุงข้อมูล',displayThaiDate(ci.LastUpdatedDate)]]:[]),['หลักสูตร',value(cur.CurriculumName)],['สาขาวิชา',value(cur.ProgramName)]
 ],[2400,7000]));
 b.push(subheading('คำอธิบายรายวิชา (ภาษาไทย)'));b.push(p(value(ci.CourseDescriptionTh)));
 b.push(subheading('Course Description (English)'));b.push(p(value(ci.CourseDescriptionEn)));
 b.push(heading('2. ผลลัพธ์การเรียนรู้ระดับหลักสูตร (PLOs)'));
 b.push(table(['PLO','ผลลัพธ์การเรียนรู้'],plos.map(x=>[x.PloCode,x.DescriptionTh]),[1080,8320]));
 b.push(heading('3. ผู้รับผิดชอบรายวิชาและผู้สอน'));
 b.push(table(['ลำดับ','ชื่อผู้สอน','สาขาวิชา','บทบาท'],teachers.map((x,i)=>[i+1,x.DisplayName||[x.Prefix,x.FirstName,x.LastName].filter(Boolean).join(' '),x.Department,x.IsResponsibleInstructor?'ผู้รับผิดชอบรายวิชา':'ผู้สอน']),[800,3430,3050,2120]));
 b.push(heading('4. ผลลัพธ์การเรียนรู้ระดับรายวิชา (CLOs)'));
 b.push(table(['CLO','ผลลัพธ์การเรียนรู้ระดับรายวิชา','เชื่อมโยง PLO'],clos.map(x=>[x.CloCode,x.DescriptionTh,list(x.MappedPloCodes)]),[950,6650,1800]));
 const weekly=(name,rows)=>{
  b.push(heading(name));
  b.push(table(['สัปดาห์','หัวข้อ / กิจกรรมการเรียนรู้','วิธีการสอน','CLO','ผู้สอน'],rows.map(x=>[x.WeekNumber,[x.Topic,x.LearningActivities].filter(Boolean).join('\n'),x.TeachingMethods,list(x.MappedCloCodes),asText(x.Notes).replace(/;\s*/g,'\n')]),[900,3150,1800,950,2600]));
 };
 weekly('5. แผนการสอนภาคบรรยาย (Lecture)',lecture);
 weekly('6. แผนการสอนภาคปฏิบัติการ (Lab)',lab);
 b.push(heading('7. การวัดและประเมินผล'));
 b.push(table(['รายการวัดและประเมินผล','ประเภทประเมิน','น้ำหนัก (%)','CLO'],assess.map(x=>[x.AssessmentName,x.AssessmentType,x.WeightPercent,list(x.MappedCloCodes)]),[3600,3000,1350,1450]));
 if(assess.length){const sum=assess.reduce((s,x)=>s+(Number(x.WeightPercent)||0),0);b.push(p(`น้ำหนักรวม ${sum}%`));}
 b.push(heading('8. เกณฑ์การตัดเกรด'));
 b.push(table(['ระดับเกรด','คะแนนขั้นต่ำ (≥)','คะแนนสูงสุด'],grades.map(x=>[x.Grade,x.MinimumScore==null?'':x.MinimumScore,x.MaximumScore==null?'':x.MaximumScore]),[2300,3550,3550]));
 b.push(heading('9. หนังสือและแหล่งเรียนรู้'));
 b.push(table(['ประเภทแหล่งเรียนรู้','ชื่อเรื่อง / แหล่งเรียนรู้','ผู้แต่ง / ปี / URL'],resource.map(x=>[x.ResourceType,x.Title,[x.Author,x.Year,x.Url].filter(Boolean).join(' · ')]),[2400,4000,3000]));
 if(meeting.length||exams.length||students.length){
  b.push(heading('ภาคผนวก: ข้อมูลตารางเรียนและนิสิต'));
  if(meeting.length){b.push(subheading('ตารางเรียน'));b.push(table(['วัน','เวลา','ห้อง'],meeting.map(x=>[x.DayOfWeek,`${x.StartTime||''}–${x.EndTime||''}`,x.RoomCode]),[2200,3300,3900]));}
  if(exams.length){b.push(subheading('ตารางสอบ'));b.push(table(['ประเภท','วันที่','เวลา / ห้อง'],exams.map(x=>[x.ExamTypeCode,displayDate(x.ExamDate),`${x.StartTime||''}–${x.EndTime||''} ${x.RoomCode||''}`]),[2000,2600,4800]));}
  if(students.length){b.push(subheading('กลุ่มนิสิต'));b.push(table(['สาขาวิชา','ชั้นปี','จำนวนนิสิต'],students.map(x=>[x.StudentProgramName,x.StudentYearLevel,x.RegisteredStudentCount]),[5200,1700,2500]));}
 }
 return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>${b.join('')}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1080" w:right="1150" w:bottom="1080" w:left="1150" w:header="540" w:footer="540" w:gutter="0"/></w:sectPr></w:body></w:document>`;
}
function stylesXML(){
 const style=(id,name,size,attrs='')=>`<w:style w:type="paragraph" w:styleId="${id}"><w:name w:val="${name}"/><w:basedOn w:val="Normal"/><w:pPr>${attrs}</w:pPr><w:rPr><w:rFonts w:ascii="TH Sarabun New" w:hAnsi="TH Sarabun New" w:eastAsia="TH Sarabun New" w:cs="TH Sarabun New"/><w:sz w:val="${size}"/><w:szCs w:val="${size}"/>${['Title','CourseTitle','Heading1','Heading2','TableHead'].includes(id)?'<w:b/>':''}</w:rPr></w:style>`;
 const space=(before,after)=>`<w:spacing w:before="${before}" w:after="${after}" w:line="320" w:lineRule="auto"/>`;
 return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="TH Sarabun New" w:hAnsi="TH Sarabun New" w:cs="TH Sarabun New" w:eastAsia="TH Sarabun New"/><w:sz w:val="30"/><w:szCs w:val="30"/><w:lang w:val="th-TH" w:eastAsia="th-TH"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr>${space(0,70)}</w:pPr></w:style>${style('Title','Title',44,`<w:jc w:val="center"/>${space(200,90)}`)}${style('Subtitle','Subtitle',28,`<w:jc w:val="center"/>${space(0,100)}`)}${style('CourseTitle','Course Title',36,`<w:jc w:val="center"/>${space(90,70)}`)}${style('Centered','Centered',29,'<w:jc w:val="center"/>')}${style('Heading1','Heading 1',35,`<w:keepNext/>${space(250,130)}`)}${style('Heading2','Heading 2',31,`<w:keepNext/>${space(160,75)}`)}${style('TableHead','Table heading',25,space(0,0))}${style('TableBody','Table body',25,space(0,0))}${style('Warning','Draft warning',27,space(40,80))}</w:styles>`;
}
function crc32(bytes){let crc=0xFFFFFFFF;for(let i=0;i<bytes.length;i++){crc^=bytes[i];for(let j=0;j<8;j++)crc=(crc&1)?(0xEDB88320^(crc>>>1)):(crc>>>1);}return (crc^0xFFFFFFFF)>>>0;}
function little16(v){return [v&255,(v>>>8)&255];}function little32(v){return [v&255,(v>>>8)&255,(v>>>16)&255,(v>>>24)&255];}
function zipFiles(files){
 const local=[],central=[];let offset=0,count=0;
 for(const [name,content] of Object.entries(files)){
  const n=encoder.encode(name),d=encoder.encode(content),c=crc32(d),sz=d.length;
  const l=new Uint8Array([0x50,0x4b,3,4,...little16(20),...little16(0x0800),...little16(0),...little16(0),...little16(0),...little32(c),...little32(sz),...little32(sz),...little16(n.length),...little16(0)]);
  local.push(l,n,d);
  central.push(new Uint8Array([0x50,0x4b,1,2,...little16(20),...little16(20),...little16(0x0800),...little16(0),...little16(0),...little16(0),...little32(c),...little32(sz),...little32(sz),...little16(n.length),...little16(0),...little16(0),...little16(0),...little16(0),...little32(0),...little32(offset)]),n);
  offset+=l.length+n.length+d.length;count++;
 }
 const clen=central.reduce((n,x)=>n+x.length,0);
 const end=new Uint8Array([0x50,0x4b,5,6,...little16(0),...little16(0),...little16(count),...little16(count),...little32(clen),...little32(offset),...little16(0)]);
 return new Blob([...local,...central,end],{type:TYPE});
}
function makeDocx(data){
 const files={
  '[Content_Types].xml':`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>`,
  '_rels/.rels':`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>`,
  'word/document.xml':documentXML(data),
  'word/styles.xml':stylesXML(),
  'word/_rels/document.xml.rels':`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`,
  'docProps/core.xml':`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Course Syllabus</dc:title><dc:creator>Smart Syllabus Generator</dc:creator></cp:coreProperties>`,
  'docProps/app.xml':`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Smart Syllabus Generator Web</Application></Properties>`
 };
 return zipFiles(files);
}
return {makeDocx,documentXML,TYPE};
});
