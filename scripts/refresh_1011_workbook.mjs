import fs from 'node:fs/promises';
import path from 'node:path';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';
const root=path.resolve(import.meta.dirname,'..');
await fs.mkdir(path.join(root,'tmp/1011_runtime'),{recursive:true});
const workbook=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(root,'model/valuation_model.xlsx')));
const before=process.argv.includes('--inspect');
if(before){
  console.log((await workbook.inspect({kind:'region',sheetId:'Summary',range:'A1:D9',maxChars:2000})).ndjson);
  const img=await workbook.render({sheetName:'Summary',range:'A1:D9',scale:1.5,format:'png'});
  await fs.writeFile(path.join(root,'tmp/1011_runtime/before.png'),new Uint8Array(await img.arrayBuffer()));
}else{
  const p=JSON.parse(await fs.readFile(path.join(root,'tmp/refresh_1011_workbook.json'),'utf8'));
  const assumptions=workbook.worksheets.getItem('Assumptions');
  assumptions.getRange('B8').values=[[p.market_date]];
  assumptions.getRange('B9').values=[[p.market_price]];
  assumptions.getRange('C5').values=[['September monthly return (2 Oct): 263,059,605 H + 224,528,485 unlisted shares; awards unvested. https://www1.hkexnews.hk/listedco/listconews/sehk/2026/1002/2026100201832_c.pdf']];
  workbook.worksheets.getItem('Audit Summary').getRange('A1:B10').values=p.audit;
  const comps=workbook.worksheets.getItem('Valuation Comps');
  for(let i=0;i<p.comps.length;i++){
    // Leave the calculated multiple formula and all formatting intact.
    comps.getRange(`A${i+2}:M${i+2}`).values=[p.comps[i].slice(0,13)];
  }
  workbook.recalculate();
  const summary=workbook.worksheets.getItem('Summary');
  const value=summary.getRange('D6').values[0][0];
  if(Math.abs(value-p.weighted_dcf)>1e-7)throw new Error(`DCF mismatch ${value}`);
  if(Math.abs(summary.getRange('B9').values[0][0]-p.zhipu_multiple)>1e-7)throw new Error('Market multiple mismatch');
  // A meaningful input perturbation must flow through the existing formulas.
  assumptions.getRange('B9').values=[[p.market_price*1.1]];
  workbook.recalculate();
  if(Math.abs(summary.getRange('B9').values[0][0]-p.zhipu_multiple*1.1)>1e-7)throw new Error('Price propagation failed');
  assumptions.getRange('B9').values=[[p.market_price]];
  workbook.recalculate();
  const errors=await workbook.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#N/A',options:{useRegex:true,maxResults:30},maxChars:2000});
  console.log(errors.ndjson);
  const img=await workbook.render({sheetName:'Summary',range:'A1:D9',scale:1.5,format:'png'});
  await fs.writeFile(path.join(root,'tmp/1011_runtime/after.png'),new Uint8Array(await img.arrayBuffer()));
  await (await SpreadsheetFile.exportXlsx(workbook)).save(path.join(root,'model/valuation_model.xlsx'));
  console.log(JSON.stringify({weightedDcf:value,market:p.market_price,multiple:p.zhipu_multiple,pricePropagation:true}));
}
