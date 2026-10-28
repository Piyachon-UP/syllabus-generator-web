// Node smoke test of exact browser DOCX module (no external packages).
const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'..');
const {makeDocx}=require(path.join(ROOT,'src/docx_export.js'));
const input=process.argv[2]||path.join(ROOT,'sample/Smart_Syllabus_Demo.json');
const output=process.argv[3]||path.join(ROOT,'sample/Smart_Syllabus_Demo.docx');
(async()=>{
 const obj=JSON.parse(fs.readFileSync(input,'utf8'));
 const docx=makeDocx(obj);
 if(docx.type!=='application/vnd.openxmlformats-officedocument.wordprocessingml.document')throw Error('DOCX MIME invalid');
 fs.writeFileSync(output,Buffer.from(await docx.arrayBuffer()));
 console.log('OK',output,fs.statSync(output).size);
})().catch(e=>{console.error(e);process.exit(1)});
