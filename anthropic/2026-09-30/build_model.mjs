import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const outputDir = fileURLToPath(new URL('.', import.meta.url));
const wb = Workbook.create();
const model = wb.worksheets.add('Valuation');
const inputs = wb.worksheets.add('Inputs');
const colors = { ink: '#242A31', navy: '#344354', blue: '#0000FF', green: '#008000', amber: '#FFF2CC', pale: '#EDF1F5', line: '#CCD3DB', red: '#9C2525' };
const number = '#,##0.0;(#,##0.0);"-"';
const money = '$#,##0.0;($#,##0.0);"-"';
const percent = '0.0%;(0.0%);"-"';
const multiple = '0.0"x"';
const cols = ['D','E','F','G','H','I','J','K','L','M','N'];

function value(s, cell, x, editable=false) {
  s.getRange(cell).values = [[x]];
  if (editable) s.getRange(cell).format = { fill: colors.amber, font: { color: colors.blue } };
}
function formula(s, cell, x, output=false) {
  s.getRange(cell).formulas = [[x]];
  s.getRange(cell).format.font.color = output ? colors.ink : (x.includes('!') ? colors.green : '#000000');
}
function section(s, row, text, end='N') {
  const r=s.getRange(`C${row}:${end}${row}`);
  r.format = { fill: colors.navy, font: { bold: true, color: '#FFFFFF' }, rowHeight: 23 };
  value(s, `C${row}`, text);
}
function label(s, row, text) { value(s, `C${row}`, text); }
function note(s, row, text, cell='F') { value(s, `${cell}${row}`, text); s.getRange(`${cell}${row}`).format.font.color='#606A75'; }
function total(s, row, end='N') {
  s.getRange(`C${row}:${end}${row}`).format = { fill: colors.pale, font:{ bold:true }, borders:{ top:{style:'thin',color:colors.line} } };
}
for (const s of [model, inputs]) {
  s.showGridLines=false;
  s.getRange('A1:N100').format = { font:{name:'Arial',size:10,color:colors.ink}, rowHeight:21, verticalAlignment:'center', horizontalAlignment:'left' };
  s.getRange('A1:B100').format.columnWidth=2.2;
  s.getRange('C1:C100').format.columnWidth=39;
  s.getRange('D1:N100').format.columnWidth=13;
  s.getRange('F1:F100').format.columnWidth=19;
  s.getRange('D1:N100').setNumberFormat(number);
  s.getRange('D1:N100').format.horizontalAlignment='right';
  s.getRange('C2').format.font={size:16,bold:true};
  s.getRange('C2:N2').format.rowHeight=30;
  s.getRange('C4:N4').format.borders={bottom:{style:'thin',color:colors.line}};
}
model.tabColor=colors.navy;
inputs.tabColor='#6F8194';
value(model,'C2','Anthropic IPO valuation');
value(model,'C3','USD billions. Research: 30 Sep 2026. Valuation date: assumed 31 Dec 2026.');
model.getRange('C3').format.font={italic:true,color:'#606A75'};
value(inputs,'C2','Inputs and public information');
value(inputs,'C3','Blue cells are editable assumptions. Green cells link to published inputs. Blank offering inputs mean unavailable.');
inputs.getRange('C3').format.font={italic:true,color:'#606A75'};

section(inputs,6,'Valuation assumptions');
const assumptionLabels={7:'Assumed valuation date',8:'Research cutoff',9:'2028 revenue anchor',10:'EV / 2028 revenue',11:'Discount rate (WACC)',12:'Pre-IPO net cash adjustment',13:'Terminal revenue growth',14:'Cash tax rate',15:'Reported IPO equity benchmark',16:'Gross primary IPO proceeds',17:'IPO fees / gross proceeds',18:'Existing diluted shares (billions)'};
for(const [r,t] of Object.entries(assumptionLabels)) label(inputs,r,t);
value(inputs,'D7',new Date('2026-12-31T00:00:00Z'),true);
value(inputs,'D8',new Date('2026-09-30T00:00:00Z'));
inputs.getRange('D7:D8').setNumberFormat('dd-mmm-yyyy');
formula(inputs,'D9','=AVERAGE(D42:D43)');
value(inputs,'D10',10,true);
value(inputs,'D11',0.12,true);
value(inputs,'D12',0,true);
value(inputs,'D13',0.03,true);
value(inputs,'D14',0.25,true);
formula(inputs,'D15','=D44');
value(inputs,'D16',null,true);
value(inputs,'D17',0.03,true);
value(inputs,'D18',null,true);
inputs.getRange('D9').setNumberFormat(money);
inputs.getRange('D10').setNumberFormat(multiple);
for(const r of [11,13,14,17]) inputs.getRange(`C${r}:D${r}`).format.font.italic=true;
for(const r of [11,13,14,17]) inputs.getRange(`D${r}`).setNumberFormat(percent);
inputs.getRange('D18').setNumberFormat('0.000');
note(inputs,7,'Assumed year-end IPO date. DCF uses end-of-year cash flows from 2027 onward.');
note(inputs,8,'Information retrieved on this date. IPO timing and terms remain unconfirmed.');
note(inputs,9,'Midpoint of the reported $190–200bn 2028 company projection [S2].');
note(inputs,10,'Illustrative multiple, not a measured current peer median.');
note(inputs,11,'Analyst assumption for a risky growth business.');
note(inputs,12,'Assumed zero. Current cash, debt and conversion adjustments are unavailable.');
note(inputs,13,'Perpetual growth after 2036. Must be below WACC.');
note(inputs,14,'Assumes cash taxes on positive EBIT. No tax-loss carryforwards modeled.');
note(inputs,15,'$2tn reference from September reporting [S3]. Not a priced offer.');
note(inputs,16,'Enter primary capital raised. Exclude sales by existing holders.');
note(inputs,17,'Illustrative fee rate. Actual underwriting terms are unavailable.');
note(inputs,18,'Enter shares after all pre-IPO conversions. Actual count is unavailable.');
inputs.getRange('E7:N18').format.horizontalAlignment='left';
inputs.getRange('D10').dataValidation={rule:{type:'decimal',operator:'greaterThan',formula1:0}};
inputs.getRange('D11').dataValidation={rule:{type:'decimal',operator:'between',formula1:0.01,formula2:0.99}};
inputs.getRange('D14').dataValidation={rule:{type:'decimal',operator:'between',formula1:0,formula2:0.99}};

section(inputs,20,'Annual forecast assumptions');
label(inputs,21,'Calendar year');
inputs.getRange('D21:N21').values=[[2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036]];
inputs.getRange('D21:N21').setNumberFormat('0');
inputs.getRange('C21:N21').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const driverLabels={22:'2026 full-year revenue estimate',23:'Revenue growth',24:'EBIT / revenue',25:'D&A / revenue',26:'Cash capex / revenue',27:'Operating working capital / revenue'};
for(const [r,t] of Object.entries(driverLabels)) label(inputs,r,t);
value(inputs,'D22',60,true);
inputs.getRange('D22').setNumberFormat(money);
inputs.getRange('E23:N23').values=[[1,null,0.35,0.25,0.20,0.15,0.10,0.07,0.05,0.03]];
formula(inputs,'F23','=$D$9/($D$22*(1+E23))-1');
inputs.getRange('E24:N24').values=[[0.10,0.20,0.25,0.30,0.32,0.33,0.34,0.35,0.35,0.35]];
inputs.getRange('E25:N25').values=[[0.03]];
inputs.getRange('E26:N26').values=[[0.08]];
inputs.getRange('D27:N27').values=[[0.02]];
inputs.getRange('E23:N27').format={fill:colors.amber,font:{color:colors.blue,italic:true}};
inputs.getRange('D27').format={fill:colors.amber,font:{color:colors.blue,italic:true}};
inputs.getRange('F23').format={fill:'#E8EDF2',font:{color:'#000000',italic:true}};
inputs.getRange('D23:N27').setNumberFormat(percent);
inputs.getRange('C23:C27').format.font.italic=true;
value(inputs,'C29','All annual drivers above are analyst assumptions. 2028 growth is calibrated to the revenue anchor.');
value(inputs,'C30','EBIT includes compute, training, channel fees and stock compensation. Capex is separate cash investment.');
value(inputs,'C31','Long-term compute obligations are not all current debt or one-year capex. Their timing is not modeled separately.');
value(inputs,'C32','DCF assumes financing is available. Any later equity dilution or funding shortfall needs a separate model.');
inputs.getRange('C29:C32').format.font.color='#606A75';

section(inputs,34,'Published reference figures');
inputs.getRange('C35:G35').values=[['Metric','Value','Period','Classification','Source ID']];
inputs.getRange('C35:G35').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
inputs.getRange('C36:G48').values=[
 ['Revenue, approximately',4.6,'2025','Media-reported','S3'],
 ['Operating loss, more than',-8,'2025','Media-reported','S3'],
 ['Series H post-money equity value',965,'28-May-26','Company-reported','S1'],
 ['Series H funds raised',65,'28-May-26','Company-reported','S1'],
 ['Revenue run rate, over',47,'May-26','Company-reported','S1'],
 ['Revenue pace, over',100,'18-Sep-26','Media-reported','S4'],
 ['2028 revenue forecast, low',190,'2028','Reported projection','S2'],
 ['2028 revenue forecast, high',200,'2028','Reported projection','S2'],
 ['IPO equity benchmark, about',2000,'Sep-26','Reported target','S3'],
 ['Long-term compute commitments, over',417,'Early 2026','Media-reported','S3'],
 ['Each of two largest customers / sales',0.12,'2025','Media-reported','S3'],
 ['Amazon and Google channels / sales',0.47,'2025','Media-reported','S3'],
 ['Channel partner distribution fees',0.351,'2025','Media-reported','S3'],
];
inputs.getRange('D36:D48').format.font.color=colors.blue;
inputs.getRange('E36:G48').format.horizontalAlignment='left';
inputs.getRange('E36:E48').setNumberFormat('0');
inputs.getRange('D46:D47').setNumberFormat(percent);
inputs.getRange('C46:D47').format.font.italic=true;
inputs.getRange('D48').setNumberFormat('$0.000');
value(inputs,'C50','Run-rate revenue annualizes a recent pace. It is not full-year recognized revenue or contracted ARR.');
inputs.getRange('C50').format.font={italic:true,color:colors.red};
const sources=[
 ['S1. Anthropic, 28 May 2026. Series H announcement.','https://www.anthropic.com/news/series-h'],
 ['S2. Reuters, article dated 14 Aug 2026, syndicated 17 Aug. 2028 revenue projection.','https://www.investing.com/news/stock-market-news/anthropic-ipo-valuation-hinges-on-190200-billion-2028-revenue-forecast-sources-say-4862222?ampMode=1'],
 ['S3. Reuters, 29 Sep 2026. Prospectus figures and dependence on cloud partners.','https://www.streetinsider.com/Reuters/Exclusive-Anthropic%2BIPO%2Bprospectus%2Blays%2Bbare%2Bdeep%2Bdependence%2Bon%2BBig%2BTech%2Bpartners/27123187.html'],
 ['S4. Axios, 18 Sep 2026. Reported revenue pace.','https://www.axios.com/2026/09/18/anthropic-100-billion-revenue'],
 ['S5. Anthropic, 1 Jun 2026. Confidential draft S-1 submitted.','https://www.anthropic.com/news/confidential-draft-s1-sec'],
];
section(inputs,52,'Source links');
sources.forEach(([title,url],i)=>{value(inputs,`C${54+i*3}`,title);value(inputs,`C${55+i*3}`,url);inputs.getRange(`C${55+i*3}`).format.font={size:9,color:'#365D85'};});
value(inputs,'C69','The confidential draft itself was not independently reviewed. Reported targets and projections may change.');
inputs.freezePanes.freezeRows(4);

section(model,6,'Valuation results', 'I');
const resultRows={7:'Revenue-multiple enterprise value',8:'DCF enterprise value',9:'Illustrative pre-IPO equity value',10:'Reported IPO equity benchmark',11:'Multiple equity / benchmark − 1',12:'DCF equity / benchmark − 1',13:'Benchmark EV / 2028 revenue',14:'Terminal value / DCF enterprise value',16:'2028 revenue used',17:'Selected EV / revenue multiple'};
for(const [r,t] of Object.entries(resultRows)) label(model,r,t);
const resultFormulas={7:'=D23',8:'=D57',9:'=D25',10:"='Inputs'!D15",11:'=D25/D10-1',12:'=IF(ISNUMBER(D58),D58/D10-1,"n.a.")',13:'=(D10-D24)/D21',14:'=D59',16:'=D21',17:'=D22'};
for(const [r,f] of Object.entries(resultFormulas)) formula(model,`D${r}`,f,true);
for(const r of [7,8,9,10,16]) model.getRange(`D${r}`).setNumberFormat(money);
for(const r of [11,12,14]) model.getRange(`D${r}`).setNumberFormat(percent);
for(const r of [13,17]) model.getRange(`D${r}`).setNumberFormat(multiple);
for(const r of [11,12,13,14,17]) model.getRange(`C${r}:D${r}`).format.font.italic=true;
note(model,7,'2028 revenue × selected forward multiple.');
note(model,8,'2027–2036 cash flows plus perpetual growth.');
note(model,9,'Net cash assumed zero. Offering proceeds excluded.');
note(model,10,'Reference target. Final offer price is unavailable.');
note(model,11,'Illustrative equity comparison using assumed net cash.');
note(model,12,'Gap indicates growth and cash margins required.');
note(model,13,'Converts equity target using the net cash assumption.');
note(model,14,'Measures reliance on cash flows beyond 2036.');
note(model,16,'Midpoint of a reported company forecast.');
note(model,17,'Editable on Inputs.');
model.getRange('E7:I18').format.horizontalAlignment='left';
total(model,7,'I');total(model,8,'I');

section(model,20,'Revenue multiple valuation');
const multLabels={21:'2028 revenue',22:'Selected EV / 2028 revenue',23:'Enterprise value',24:'Add: pre-IPO net cash adjustment',25:'Illustrative pre-IPO equity value'};
for(const [r,t] of Object.entries(multLabels))label(model,r,t);
formula(model,'D21','=F30');
formula(model,'D22',"='Inputs'!D10");
formula(model,'D23','=D21*D22');
formula(model,'D24',"='Inputs'!D12");
formula(model,'D25','=SUM(D23:D24)');
model.getRange('D22').setNumberFormat(multiple);
model.getRange('C22:D22').format.font.italic=true;
model.getRange('D23:D25').setNumberFormat(money);
total(model,25,'N');
note(model,26,'Forward multiple prices value at the valuation date. Do not discount the revenue-multiple result again.', 'C');

section(model,28,'DCF forecast at the assumed year-end 2026 valuation date');
label(model,29,'Calendar year');
model.getRange('D29:N29').values=[[2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036]];
model.getRange('D29:N29').setNumberFormat('0"E"');
model.getRange('C29:N29').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const dcfLabels={30:'Revenue',31:'Revenue growth',32:'EBIT margin',33:'EBIT',34:'Cash taxes',35:'After-tax operating profit',36:'Add: depreciation & amortization',37:'Less: cash capital expenditure',38:'Operating working capital balance',39:'Less: increase in working capital',40:'Unlevered free cash flow',41:'Years from valuation date',42:'Discount factor',43:'Present value of free cash flow'};
for(const [r,t] of Object.entries(dcfLabels))label(model,r,t);
formula(model,'D30',"='Inputs'!D22");
formula(model,'D31',"=D30/'Inputs'!D36-1");
formula(model,'D38',"=D30*'Inputs'!D27");
for(let i=1;i<cols.length;i++){
 const c=cols[i],p=cols[i-1];
 const f={30:`=${p}30*(1+${c}31)`,31:`='Inputs'!${c}23`,32:`='Inputs'!${c}24`,33:`=${c}30*${c}32`,34:`=-MAX(${c}33,0)*'Inputs'!$D$14`,35:`=SUM(${c}33:${c}34)`,36:`=${c}30*'Inputs'!${c}25`,37:`=-${c}30*'Inputs'!${c}26`,38:`=${c}30*'Inputs'!${c}27`,39:`=-(${c}38-${p}38)`,40:`=SUM(${c}35:${c}37,${c}39)`,41:`=${c}$29-YEAR('Inputs'!$D$7)`,42:`=(1+'Inputs'!$D$11)^(-${c}41)`,43:`=${c}40*${c}42`};
 for(const [r,x]of Object.entries(f))formula(model,`${c}${r}`,x);
}
for(const r of [31,32,42]) {model.getRange(`C${r}:N${r}`).format.font.italic=true;model.getRange(`D${r}:N${r}`).setNumberFormat(r===42?'0.000':percent);}
model.getRange('E41:N41').setNumberFormat('0');
for(const r of [30,35,40,43]){model.getRange(`D${r}:N${r}`).setNumberFormat(money);total(model,r);}

section(model,45,'Terminal value and DCF calculation');
const termLabels={46:'2037 terminal revenue',47:'Terminal EBIT',48:'Terminal cash taxes',49:'Terminal after-tax operating profit',50:'Terminal D&A',51:'Terminal cash capex',52:'Terminal change in working capital',53:'Terminal unlevered free cash flow',54:'Terminal enterprise value',55:'Present value of terminal value',56:'PV of 2027–2036 free cash flow',57:'DCF enterprise value',58:'Illustrative DCF equity value',59:'Terminal value / enterprise value',60:'Terminal FCF needed for benchmark',61:'Terminal EBIT margin needed'};
for(const [r,t]of Object.entries(termLabels))label(model,r,t);
const termFormulas={46:"=N30*(1+'Inputs'!D13)",47:'=D46*N32',48:"=-MAX(D47,0)*'Inputs'!D14",49:'=SUM(D47:D48)',50:"=D46*'Inputs'!N25",51:"=-D46*'Inputs'!N26",52:"=-(D46-N30)*'Inputs'!N27",53:'=SUM(D49:D52)',54:"=IF('Inputs'!D11>'Inputs'!D13,D53/('Inputs'!D11-'Inputs'!D13),\"n.a.\")",55:'=IF(ISNUMBER(D54),D54*N42,"n.a.")',56:'=SUM(E43:N43)',57:'=IF(ISNUMBER(D55),SUM(D55:D56),"n.a.")',58:'=IF(ISNUMBER(D57),D57+D24,"n.a.")',59:'=IF(ISNUMBER(D57),D55/D57,"n.a.")',60:"=IF('Inputs'!D11>'Inputs'!D13,(D10-D24-D56)/N42*('Inputs'!D11-'Inputs'!D13),\"n.a.\")",61:"=IF(ISNUMBER(D60),(D60-SUM(D50:D52))/D46/(1-'Inputs'!D14),\"n.a.\")"};
for(const [r,f]of Object.entries(termFormulas))formula(model,`D${r}`,f);
model.getRange('D46:D58').setNumberFormat(money);
model.getRange('D60').setNumberFormat(money);
for(const r of [59,61]){model.getRange(`D${r}`).setNumberFormat(percent);model.getRange(`C${r}:D${r}`).format.font.italic=true;}
total(model,57);total(model,58);
note(model,54,'Terminal FCF / (WACC − growth). Returns n.a. if WACC ≤ growth.');
note(model,59,'Terminal-year investment ratios and margins equal 2036 assumptions.');
note(model,60,'Holds the explicit forecast, investment ratios and discount rate constant.');
note(model,61,'Required perpetual EBIT margin to support the benchmark equity target.');
value(model,'C63','Growth, compute efficiency and future financing are the main valuation risks. Revenue multiples do not prove cash returns.');
model.getRange('C63').format.font={italic:true,color:'#606A75'};

section(model,65,'Enterprise value sensitivity ($bn)');
value(model,'C66','2028 revenue / EV multiple');
model.getRange('D66:I66').values=[[6,8,10,12,14,16]];
model.getRange('D66:I66').setNumberFormat(multiple);
model.getRange('C66:I66').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
model.getRange('C67:C71').values=[[120],[160],[null],[240],[280]];
formula(model,'C69','=D21');
model.getRange('C67:C71').setNumberFormat(money);
model.getRange('C67:C71').format={fill:colors.pale,font:{italic:true},horizontalAlignment:'right'};
for(const r of [67,68,69,70,71])for(const c of ['D','E','F','G','H','I'])formula(model,`${c}${r}`,`=$C${r}*${c}$66`);
model.getRange('D67:I71').setNumberFormat(money);
model.getRange('D67:I71').conditionalFormats.add('colorScale',{colors:['#F3E1D3','#F5F6F7','#9FB2C5'],thresholds:['min',{type:'percentile',value:50},'max']});
value(model,'C73','Each cell is revenue × multiple. Middle revenue row follows the model. Column multiples are illustrative assumptions.');
model.getRange('C73').format.font={italic:true,color:'#606A75'};

section(model,75,'IPO offering mechanics');
const ipoLabels={76:'Pre-offer equity value',77:'Gross primary proceeds',78:'Less: IPO fees',79:'Net primary proceeds',80:'Post-offer equity value',81:'Existing diluted shares (billions)',82:'Implied offer price ($ / share)',83:'New primary shares (billions)',84:'Total shares after IPO (billions)'};
for(const [r,t]of Object.entries(ipoLabels))label(model,r,t);
const ipoFormulas={76:'=D25',77:"=IF(ISNUMBER('Inputs'!D16),'Inputs'!D16,\"n.a.\")",78:"=IF(ISNUMBER(D77),-D77*'Inputs'!D17,\"n.a.\")",79:'=IF(ISNUMBER(D77),SUM(D77:D78),"n.a.")',80:'=IF(ISNUMBER(D79),D76+D79,"n.a.")',81:"=IF(ISNUMBER('Inputs'!D18),'Inputs'!D18,\"n.a.\")",82:'=IF(ISNUMBER(D81),IF(D81>0,D76/D81,"n.a."),"n.a.")',83:'=IF(ISNUMBER(D77),IF(ISNUMBER(D82),IF(D82>0,D77/D82,"n.a."),"n.a."),"n.a.")',84:'=IF(ISNUMBER(D83),D81+D83,"n.a.")'};
for(const [r,f]of Object.entries(ipoFormulas))formula(model,`D${r}`,f);
model.getRange('D76:D80').setNumberFormat(money);
model.getRange('D81:D84').setNumberFormat('0.000');
model.getRange('D82').setNumberFormat('$0.00;($0.00);"-"');
total(model,80);total(model,84);
note(model,77,'Enter gross primary proceeds on Inputs. Secondary sales add no company cash.');
note(model,81,'Actual share count is unavailable. Enter fully converted pre-offer shares.');
note(model,82,'Pre-offer equity / existing shares. No placeholder share count is assumed.');
note(model,84,'Existing diluted shares + new shares sold.');
value(model,'C86','Equity = EV + net cash. Reported private-round equity values and EV multiples use different bases.');
value(model,'C87','The $965bn private mark is post-money from May. It is not an additional cash inflow in this valuation.');
model.getRange('C86:C87').format.font={italic:true,color:'#606A75'};
model.getRange('E46:N61').format.horizontalAlignment='left';
model.getRange('E76:N84').format.horizontalAlignment='left';

// A live forecast chart reads the operating build directly.
const chart=model.charts.add('line');
chart.title='Revenue forecast ($bn)';
chart.titleTextStyle.typeface='Arial';chart.titleTextStyle.fontSize=12;
const series=chart.series.add('Revenue');
series.categoryFormula="'Valuation'!$D$29:$N$29";
series.formula="'Valuation'!$D$30:$N$30";
series.line={fill:'#556B82',style:'solid',width:2};
chart.hasLegend=false;
chart.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial',fontSize:10}};
chart.yAxis={numberFormatCode:'$0',numberFormatSourceLinked:false,textStyle:{typeface:'Arial',fontSize:10}};
chart.setPosition('J6','N18');

function expected() {
 const growth=[1,195/(60*2)-1,.35,.25,.2,.15,.1,.07,.05,.03];
 const margins=[.1,.2,.25,.3,.32,.33,.34,.35,.35,.35];
 const wacc=.12,tax=.25,g=.03;
 let priorRev=60,priorWc=1.2,pv=0,rev,fcf;
 for(let t=1;t<=10;t++){
  rev=priorRev*(1+growth[t-1]);
  const wc=rev*.02;
  fcf=rev*margins[t-1]*(1-tax)+rev*.03-rev*.08-(wc-priorWc);
  pv+=fcf/(1+wacc)**t;priorRev=rev;priorWc=wc;
 }
 const nextRev=rev*(1+g);
 const terminalFcf=nextRev*.35*(1-tax)+nextRev*.03-nextRev*.08-(nextRev-rev)*.02;
 const terminalPv=terminalFcf/(wacc-g)/(1+wacc)**10;
 return {rev2036:rev,pv,terminalFcf,terminalPv,dcf:pv+terminalPv,multipleEv:1950,terminalShare:terminalPv/(pv+terminalPv)};
}
function assertClose(cell, expectedValue, tolerance=1e-7) {
 const actual=model.getRange(cell).values[0][0];
 if(typeof actual!=='number'||Math.abs(actual-expectedValue)>tolerance*Math.max(1,Math.abs(expectedValue))) throw new Error(`${cell}: expected ${expectedValue}, got ${actual}`);
}
// Perturb relevant inputs and restore. Tests are authoring-only, not workbook tabs.
const e=expected();
assertClose('D7',1950);assertClose('D8',e.dcf);assertClose('N30',e.rev2036);assertClose('D56',e.pv);
value(inputs,'D10',12,true);assertClose('D7',2340);assertClose('D8',e.dcf);value(inputs,'D10',10,true);
const baseDcf=model.getRange('D8').values[0][0];
value(inputs,'N24',.30,true);
if(!(model.getRange('D8').values[0][0]<baseDcf))throw new Error('Later-year margin failed to update DCF');
value(inputs,'N24',.35,true);
value(inputs,'D11',.03,true);
if(model.getRange('D8').values[0][0]!=='n.a.')throw new Error('WACC <= growth boundary not handled');
value(inputs,'D11',.12,true);
value(inputs,'D16',0,true);value(inputs,'D18',10,true);
assertClose('D79',0);assertClose('D80',1950);assertClose('D82',195);assertClose('D84',10);
value(inputs,'D16',100,true);assertClose('D79',97);assertClose('D80',2047);assertClose('D83',100/195);
value(inputs,'D18',0,true);
if(model.getRange('D82').values[0][0]!=='n.a.')throw new Error('Zero share count not handled');
value(inputs,'D16',null,true);value(inputs,'D18',null,true);
if(model.getRange('D82').values[0][0]!=='n.a.')throw new Error('Missing share count not handled');

wb.recalculate();
assertClose('D7',e.multipleEv);assertClose('D8',e.dcf);assertClose('D14',e.terminalShare);
const headline=await wb.inspect({kind:'table',range:'Valuation!C6:D17',include:'values,formulas',tableMaxRows:12,tableMaxCols:2,maxChars:3500});
console.log(headline.ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'Formula errors',maxChars:1000});
console.log(errors.ndjson);
console.log(JSON.stringify({independent:e,requiredMargin:model.getRange('D61').values[0][0],verified:['multiple perturbation','later-period margin','WACC/growth boundary','IPO zero and positive proceeds','missing and zero share count'],chartSeries:chart.series.items.map(s=>({formula:s.formula,categoryFormula:s.categoryFormula}))}));

for(const [s,range,name]of [[model,'C2:N18','valuation_summary'],[model,'C28:N43','dcf_forecast'],[model,'C45:N87','valuation_detail'],[inputs,'C2:N32','assumptions'],[inputs,'C34:N69','public_sources']]){
 const preview=await wb.render({sheetName:s.name,range,scale:1.3,format:'png'});
 await fs.writeFile(`${outputDir}/${name}.png`,new Uint8Array(await preview.arrayBuffer()));
}
const out=await SpreadsheetFile.exportXlsx(wb);
await out.save(`${outputDir}/Anthropic_IPO_Basic_Valuation.xlsx`);
await fs.writeFile(`${outputDir}/verification.json`,JSON.stringify({independent:e,requiredMargin:model.getRange('D61').values[0][0],errors:errors.ndjson},null,2));
console.log('Saved Anthropic_IPO_Basic_Valuation.xlsx');
