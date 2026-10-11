import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const outputDir = fileURLToPath(new URL('.', import.meta.url));
const wb = Workbook.create();
const model = wb.worksheets.add('Valuation');
const comps = wb.worksheets.add('Comps');
const inputs = wb.worksheets.add('Inputs');
const colors = { ink: '#242A31', navy: '#344354', blue: '#0000FF', green: '#008000', amber: '#FFF2CC', pale: '#EDF1F5', line: '#CCD3DB', red: '#9C2525' };
const number = '#,##0.0;(#,##0.0);"-"';
const money = '$#,##0.0;($#,##0.0);"-"';
const percent = '0.0%;(0.0%);"-"';
const multiple = '0.0"x"';
const cols = ['D','E','F','G','H','I','J','K','L','M','N'];
const BASE26 = 64;          // 2026 recognised revenue, derived from the published ARR ramp
const ANCHOR28 = 195;       // midpoint of the reported $190-200bn 2028 projection

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
  s.getRange('A1:N130').format = { font:{name:'Arial',size:10,color:colors.ink}, rowHeight:21, verticalAlignment:'center', horizontalAlignment:'left' };
  s.getRange('A1:B130').format.columnWidth=2.2;
  s.getRange('C1:C130').format.columnWidth=39;
  s.getRange('D1:N130').format.columnWidth=13;
  s.getRange('F1:F130').format.columnWidth=19;
  s.getRange('D1:N130').setNumberFormat(number);
  s.getRange('D1:N130').format.horizontalAlignment='right';
  s.getRange('C2').format.font={size:16,bold:true};
  s.getRange('C2:N2').format.rowHeight=30;
  s.getRange('C4:N4').format.borders={bottom:{style:'thin',color:colors.line}};
}
// Comps needs a wider label column and a source column
comps.showGridLines=false;
comps.getRange('A1:N130').format = { font:{name:'Arial',size:10,color:colors.ink}, rowHeight:21, verticalAlignment:'center', horizontalAlignment:'left' };
comps.getRange('A1:B130').format.columnWidth=2.2;
comps.getRange('C1:C130').format.columnWidth=40;
comps.getRange('D1:D130').format.columnWidth=12;
comps.getRange('E1:G130').format.columnWidth=13;
comps.getRange('H1:H130').format.columnWidth=17;
comps.getRange('I1:I130').format.columnWidth=10;
comps.getRange('J1:J130').format.columnWidth=12;
comps.getRange('K1:K130').format.columnWidth=15;
comps.getRange('L1:L130').format.columnWidth=10;
comps.getRange('D1:L130').setNumberFormat(number);
comps.getRange('D1:L130').format.horizontalAlignment='right';
comps.getRange('C2').format.font={size:16,bold:true};
comps.getRange('C2:N2').format.rowHeight=30;
comps.getRange('C4:N4').format.borders={bottom:{style:'thin',color:colors.line}};

model.tabColor=colors.navy;
comps.tabColor='#7A5C8E';
inputs.tabColor='#6F8194';

value(model,'C2','Anthropic IPO valuation');
value(model,'C3','USD billions. Research: 11 Oct 2026. Valuation date: assumed 31 Dec 2026.');
model.getRange('C3').format.font={italic:true,color:'#606A75'};
value(comps,'C2','Comparable company valuation');
value(comps,'C3','USD billions. Public market data as of 8-9 Oct 2026; private marks as dated. Anthropic is the target, not a comp.');
comps.getRange('C3').format.font={italic:true,color:'#606A75'};
value(inputs,'C2','Inputs and public information');
value(inputs,'C3','Blue cells are editable assumptions. Green cells link to published inputs. Update cutoff: 11 Oct 2026.');
inputs.getRange('C3').format.font={italic:true,color:'#606A75'};

/* ------------------------------ INPUTS ------------------------------ */
section(inputs,6,'Valuation assumptions');
const assumptionLabels={7:'Assumed valuation date',8:'Research cutoff',9:'2028 revenue anchor',10:'EV / 2028 revenue',11:'Discount rate (WACC)',12:'Pre-IPO net cash adjustment',13:'Terminal revenue growth',14:'Cash tax rate',15:'Reported IPO equity benchmark',16:'Gross primary IPO proceeds',17:'IPO fees / gross proceeds',18:'Existing diluted shares (billions)'};
for(const [r,t] of Object.entries(assumptionLabels)) label(inputs,r,t);
value(inputs,'D7',new Date('2026-12-31T00:00:00Z'),true);
value(inputs,'D8',new Date('2026-10-11T00:00:00Z'));
inputs.getRange('D7:D8').setNumberFormat('dd-mmm-yyyy');
formula(inputs,'D9','=AVERAGE(D43:D44)');
value(inputs,'D10',10,true);
value(inputs,'D11',0.12,true);
value(inputs,'D12',0,true);
value(inputs,'D13',0.03,true);
value(inputs,'D14',0.25,true);
formula(inputs,'D15','=D45');
value(inputs,'D16',null,true);
value(inputs,'D17',0.03,true);
value(inputs,'D18',null,true);
inputs.getRange('D9').setNumberFormat(money);
inputs.getRange('D10').setNumberFormat(multiple);
for(const r of [11,13,14,17]) inputs.getRange(`C${r}:D${r}`).format.font.italic=true;
for(const r of [11,13,14,17]) inputs.getRange(`D${r}`).setNumberFormat(percent);
inputs.getRange('D18').setNumberFormat('0.000');
note(inputs,7,'Reported IPO window has moved to mid-Nov 2026 [S11]. Change this cell to re-time the discounting.');
note(inputs,8,'Public S-1 had not posted to EDGAR as of 9 Oct 2026 [S8]. No audited financials exist yet.');
note(inputs,9,'Midpoint of the reported $190-200bn 2028 company projection [S2].');
note(inputs,10,'Illustrative multiple. See Comps for peer-derived ranges.');
note(inputs,11,'Analyst assumption for a risky growth business.');
note(inputs,12,'Assumed zero. Current cash, debt and conversion adjustments are unavailable.');
note(inputs,13,'Perpetual growth after 2036. Must be below WACC.');
note(inputs,14,'Assumes cash taxes on positive EBIT. No tax-loss carryforwards modeled.');
note(inputs,15,'$2tn reference from September reporting [S3]. Not a priced offer.');
note(inputs,16,'Reported at up to $100bn by the WSJ [S12]. Exclude secondary sales.');
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
value(inputs,'D22',BASE26,true);
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
value(inputs,'C29','2026 revenue of $64bn is a model output, not a disclosure. It integrates the published run-rate path');
value(inputs,'C30','($9bn Dec-25, $20bn Mar-26, $30bn Apr-26, $47bn May-26, $65bn Jul-26, $100-120bn Dec-26E) over twelve months.');
inputs.getRange('C29:C30').format.font.color='#606A75';
value(inputs,'C31','EBIT includes compute, training, channel fees and stock compensation. Capex is separate cash investment.');
value(inputs,'C32','Long-term compute obligations are not all current debt or one-year capex. Their timing is not modeled separately.');
value(inputs,'C33','DCF assumes financing is available. Any later equity dilution or funding shortfall needs a separate model.');
inputs.getRange('C31:C33').format.font.color='#606A75';

section(inputs,35,'Published reference figures');
inputs.getRange('C36:G36').values=[['Metric','Value','Period','Classification','Source ID']];
inputs.getRange('C36:G36').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
inputs.getRange('C37:G64').values=[
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
 ['Revenue run-rate, end-2025',9,'Dec-25','Company-reported','S6'],
 ['Revenue run-rate, March 2026',20,'Mar-26','Media-reported','S7'],
 ['Revenue run-rate, April 2026',30,'Apr-26','Media-reported','S7'],
 ['Revenue run-rate, end-July 2026',65,'Jul-26','Company-reported','S6'],
 ['Revenue run-rate, end-2026 expected',110,'2026E','Investor expectation','S7'],
 ['Secondary-market implied value, about',1100,'Oct-26','Media-reported','S8'],
 ['Institutional fair value, low',1800,'Oct-26','Media-reported','S11'],
 ['Institutional fair value, high',2000,'Oct-26','Media-reported','S11'],
 ['Pre-IPO perpetual futures implied value',2150,'17-Sep-26','Market-implied','S10'],
 ['Pre-IPO perpetual futures peak',2360,'Sep-26','Market-implied','S10'],
 ['AMD investment commitment, up to',5,'22-Jul-26','Media-reported','S12'],
 ['AWS spend commitment, over',100,'2026','Company-reported','S9'],
 ['Amazon investment commitment, up to',33,'2026','Media-reported','S9'],
 ['IPO gross proceeds, up to',100,'2026','Media-reported','S12'],
 ['Revolving credit facility',15,'Oct-26','Media-reported','S12'],
];
inputs.getRange('D37:D64').format.font.color=colors.blue;
inputs.getRange('E37:G64').format.horizontalAlignment='left';
inputs.getRange('E37:E64').setNumberFormat('0');
inputs.getRange('D47:D48').setNumberFormat(percent);
inputs.getRange('C47:D48').format.font.italic=true;
inputs.getRange('D49').setNumberFormat('$0.000');
value(inputs,'C66','Conflict: two 2025 loss figures circulate - more than $8bn (Reuters, 29 Sep, draft prospectus) and close to $42bn [S9].');
inputs.getRange('C66').format.font={italic:true,color:colors.red};
value(inputs,'C67','They cannot both be right. Neither is used in the model. Run-rate revenue annualises one month; it is not recognised revenue.');
inputs.getRange('C67').format.font={italic:true,color:colors.red};
const sources=[
 ['S1. Anthropic, 28 May 2026. Series H announcement.','https://www.anthropic.com/news/series-h'],
 ['S2. Reuters, article dated 14 Aug 2026, syndicated 17 Aug. 2028 revenue projection.','https://www.investing.com/news/stock-market-news/anthropic-ipo-valuation-hinges-on-190200-billion-2028-revenue-forecast-sources-say-4862222?ampMode=1'],
 ['S3. Reuters, 29 Sep 2026. Prospectus figures and dependence on cloud partners.','https://www.streetinsider.com/Reuters/Exclusive-Anthropic%2BIPO%2Bprospectus%2Blays%2Bbare%2Bdeep%2Bdependence%2Bon%2BBig%2BTech%2Bpartners/27123187.html'],
 ['S4. Axios, 18 Sep 2026. Reported revenue pace.','https://www.axios.com/2026/09/18/anthropic-100-billion-revenue'],
 ['S5. Anthropic, 1 Jun 2026. Confidential draft S-1 submitted.','https://www.anthropic.com/news/confidential-draft-s1-sec'],
 ['S6. Bloomberg, 17 Aug 2026, via Kagels Trading 6 Oct 2026. Run-rate path $9bn to $65bn.','https://kagels-trading.com/blog/anthropic-stock'],
 ['S7. Bloomberg and NYT, Sep 2026, via Kagels Trading. End-2026 run-rate expectation $100-120bn.','https://kagels-trading.com/blog/anthropic-stock'],
 ['S8. Kagels Trading, 6 Oct 2026. Secondary market $1.05-1.15tn; EDGAR check 9 Oct 2026.','https://kagels-trading.com/blog/anthropic-stock'],
 ['S9. Euronews, 17 Sep 2026. Amazon and AWS commitments; 2025 loss figure.','https://euronews.com/business/2026/09/17/anthropic-priced-above-2-trillion-as-markets-eagerly-await-ipo-filing'],
 ['S10. Euronews and BrokerChooser, 17 Sep 2026. Hyperliquid pre-IPO perpetual futures.','https://brokerchooser.com/news/anthropic-breaks-2-trillion-valuation-barrier-ahead-of-ipo-debut--58150e7e'],
 ['S11. Bloomberg, 1 Oct 2026, via Fello AI. Fair value $1.8-2tn; marketing from 9 Nov.','https://felloai.com/anthropic-ipo'],
 ['S12. Fello AI, Oct 2026, citing WSJ and CNBC. Raise up to $100bn; revolver; AMD; Series G.','https://felloai.com/anthropic-ipo'],
 ['S13. Reuters, 14 Aug 2026, LSEG data, via Pebblous. PLTR 53x, SpaceX 41.6x, Cloudflare 41.6x.','https://blog.pebblous.ai/report/anthropic-ipo-forward-revenue-multiple-2026-09/en'],
 ['S14. openai-stock.com and Premier Alts, Oct 2026. OpenAI $852bn round, $70bn ARR, secondary marks.','https://openai-stock.com/valuation'],
 ['S15. AI Business Weekly, Oct 2026. xAI $250bn (Feb-26); Mistral AI about $24bn (Sep-26).','https://aibusinessweekly.net/p/biggest-ai-companies'],
 ['S16. StockAnalysis, Yahoo Finance and Morningstar, Sep-Oct 2026. Public comp caps and multiples.','https://stockanalysis.com/stocks/snow/market-cap'],
 ['S17. AInvest and Daloopa, May-Jun 2026. CoreWeave and Nebius EV to 2026 revenue.','https://www.ainvest.com/news/coreweave-nebius-market-cap-math-2605'],
];
section(inputs,69,'Source links');
sources.forEach(([title,url],i)=>{value(inputs,`C${71+i*3}`,title);value(inputs,`C${72+i*3}`,url);inputs.getRange(`C${72+i*3}`).format.font={size:9,color:'#365D85'};});
value(inputs,'C122','The confidential draft itself was not independently reviewed. Reported targets and projections may change.');
inputs.freezePanes.freezeRows(4);

/* ------------------------------ COMPS ------------------------------ */
// Tier 1 - frontier AI labs
section(comps,5,'Tier 1 - Frontier AI labs (private). Closest business model. Marks are negotiated or secondary, not exchange-traded.','L');
comps.getRange('C6:L6').values=[['Company','Ticker','Value $bn','EV $bn','Revenue $bn','Revenue basis','Rev growth','Value / revenue','As of','Source']];
comps.getRange('C6:L6').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const t1=[
 ['OpenAI - last priced round','Private',852,'n.a.',70,'ARR, Sep-26','n.a.',null,'Mar-26 / Sep-26','S14'],
 ['OpenAI - secondary mark','Private',1200,'n.a.',70,'ARR, Sep-26','n.a.',null,'Oct-26','S14'],
 ['Anthropic - last priced round','TARGET',965,'n.a.',65,'ARR, Jul-26','n.a.',null,'May-26 / Jul-26','S1, S6'],
 ['xAI','Private',250,'n.a.','n.a.','[MISSING]','n.a.',null,'Feb-26','S15'],
 ['Mistral AI','Private',24,'n.a.','n.a.','[MISSING]','n.a.',null,'Sep-26','S15'],
];
t1.forEach((row,i)=>{
  const r=7+i;
  comps.getRange(`C${r}:L${r}`).values=[row];
  formula(comps,`J${r}`,`=IF(AND(ISNUMBER(E${r}),ISNUMBER(G${r}),G${r}>0),E${r}/G${r},"n.a.")`);
});
comps.getRange('C9:L9').format.font.bold=true;
comps.getRange('C9').format.font.color=colors.red;
comps.getRange('E7:G11').setNumberFormat(money);
comps.getRange('J7:J11').setNumberFormat(multiple);
note(comps,12,'OpenAI carries two marks on the same $70bn ARR. That spread is the private-market error bar, not an anomaly.','C');

// Tier 2 - high-growth AI-enabled software
section(comps,14,'Tier 2 - High-growth AI-enabled software (public). Growth and multiple proxies. Far lower capital intensity than a frontier lab.','L');
comps.getRange('C15:L15').values=[['Company','Ticker','Market cap $bn','EV $bn','Revenue $bn','Revenue basis','Rev growth','EV / revenue','As of','Source']];
comps.getRange('C15:L15').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const t2=[
 ['Palantir','PLTR',439,432,8.15,'2026E revenue',0.60,null,'Aug-26','S13'],
 ['Cloudflare','NET',110,109,2.62,'2026E revenue',0.36,null,'Aug-26','S13'],
 ['CrowdStrike','CRWD',220,218,8.91,'NTM revenue',0.22,null,'Aug-26','S16'],
 ['Snowflake','SNOW',130,128,9.35,'NTM revenue',0.28,null,'Oct-26','S16'],
 ['SpaceX','Private/listed','n.a.','n.a.','n.a.','2026E revenue','n.a.',41.6,'Aug-26','S13'],
];
t2.forEach((row,i)=>{
  const r=16+i;
  comps.getRange(`C${r}:L${r}`).values=[row];
  if (row[7]===null) formula(comps,`J${r}`,`=IF(AND(ISNUMBER(F${r}),ISNUMBER(G${r}),G${r}>0),F${r}/G${r},"n.a.")`);
});
comps.getRange('E16:G20').setNumberFormat(money);
comps.getRange('I16:I19').setNumberFormat(percent);
comps.getRange('J16:J20').setNumberFormat(multiple);
note(comps,21,'Revenue is backed out as value divided by the sourced multiple, so every row is internally consistent.','C');

// Tier 3 - AI infrastructure / neocloud
section(comps,23,'Tier 3 - AI infrastructure / neocloud (public). Capital-intensity and compute-contract proxy.','L');
comps.getRange('C24:L24').values=[['Company','Ticker','Market cap $bn','EV $bn','Revenue $bn','Revenue basis','Rev growth','EV / revenue','As of','Source']];
comps.getRange('C24:L24').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const t3=[
 ['CoreWeave','CRWV',58,86.6,12.93,'2026E revenue',1.20,null,'May-26','S17'],
 ['Nebius','NBIS',55,56.6,3.20,'2026E revenue',3.00,null,'Jun-26','S17'],
];
t3.forEach((row,i)=>{
  const r=25+i;
  comps.getRange(`C${r}:L${r}`).values=[row];
  formula(comps,`J${r}`,`=IF(AND(ISNUMBER(F${r}),ISNUMBER(G${r}),G${r}>0),F${r}/G${r},"n.a.")`);
});
comps.getRange('E25:G26').setNumberFormat(money);
comps.getRange('I25:I26').setNumberFormat(percent);
comps.getRange('J25:J26').setNumberFormat(multiple);
note(comps,27,'These carry the same compute-commitment profile as Anthropic but none of the model-ownership economics.','C');

// Tier 4 - scale reference only
section(comps,29,'Tier 4 - Mega-cap AI platforms. Scale reference only; their multiples are not comparable.','L');
comps.getRange('C30:E30').values=[['Company','Ticker','Market cap $bn']];
comps.getRange('C30:E30').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
comps.getRange('C31:E35').values=[
 ['Nvidia','NVDA',5600],
 ['Alphabet','GOOGL',4100],
 ['Microsoft','MSFT',3800],
 ['Meta','META',1800],
 ['Oracle','ORCL',444],
];
comps.getRange('E31:E35').setNumberFormat(money);
comps.getRange('F31:F35').values=[['Compute supplier, not a model developer'],['Investor, cloud partner and competitor'],['Holds about 27% of OpenAI [S14]'],['Consumer AI distribution'],['Cloud capacity provider']];
comps.getRange('F31:F35').format.horizontalAlignment='left';

// Revenue bases
section(comps,37,'Anthropic revenue bases - the denominator drives everything','H');
comps.getRange('C38:H38').values=[['Revenue base','Definition','2026E recognised','Exit-2026 ARR','2027E','2028E']];
comps.getRange('C38:H38').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
value(comps,'C39','$bn');
formula(comps,'E39',"='Inputs'!D22");
formula(comps,'F39',"='Inputs'!D54");
formula(comps,'G39',"='Valuation'!E30");
formula(comps,'H39',"='Inputs'!D9");
comps.getRange('E39:H39').setNumberFormat(money);
comps.getRange('E39:H39').format={font:{bold:true}};
value(comps,'C40','Classification');
comps.getRange('E40:H40').values=[['Model output','Investor expectation','Model output','Reported projection']];
comps.getRange('E40:H40').format={font:{italic:true,color:'#606A75'},horizontalAlignment:'right'};
total(comps,39,'H');

// Embedded multiples
section(comps,42,'Multiple embedded in each market mark (value / revenue base)','H');
comps.getRange('C43:H43').values=[['Market mark','Value $bn','2026E','Exit-2026 ARR','2027E','2028E']];
comps.getRange('C43:H43').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const marks=[['Series H private round (28-May-26)',"'Inputs'!D39"],['Secondary market (Oct-26)',"'Inputs'!D55"],['Institutional fair value, low',"'Inputs'!D56"],['IPO target / fair value, high',"'Inputs'!D57"],['Pre-IPO perpetual futures (17-Sep-26)',"'Inputs'!D58"]];
marks.forEach(([t,src],i)=>{
  const r=44+i;
  label(comps,r,t);
  formula(comps,`D${r}`,`=${src}`);
  for(const c of ['E','F','G','H']) formula(comps,`${c}${r}`,`=IF(AND(ISNUMBER($D${r}),ISNUMBER(${c}$39),${c}$39>0),$D${r}/${c}$39,"n.a.")`);
  comps.getRange(`D${r}`).setNumberFormat(money);
  comps.getRange(`E${r}:H${r}`).setNumberFormat(multiple);
});
note(comps,49,'Read across a row: the same mark looks cheap or expensive purely by moving the denominator.','C');

// Implied value matrix
section(comps,51,'Implied equity value ($bn) = peer multiple x Anthropic revenue base','H');
comps.getRange('C52:H52').values=[['Multiple applied','Multiple (x)','2026E recognised','Exit-2026 ARR','2027E','2028E']];
comps.getRange('C52:H52').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const scen=[['Tier 1 frontier-lab median','=MEDIAN(J7:J8)'],['Tier 1 - OpenAI Oct secondary','=J8'],['Tier 2 AI-software median','=MEDIAN(J16:J20)'],['Tier 2 AI-software mean','=AVERAGE(J16:J20)'],['Tier 3 neocloud median','=MEDIAN(J25:J26)']];
scen.forEach(([t,f],i)=>{
  const r=53+i;
  label(comps,r,t);
  formula(comps,`D${r}`,f);
  comps.getRange(`D${r}`).setNumberFormat(multiple);
  for(const c of ['E','F','G','H']) formula(comps,`${c}${r}`,`=IF(ISNUMBER($D${r}),$D${r}*${c}$39,"n.a.")`);
  comps.getRange(`E${r}:H${r}`).setNumberFormat(money);
});
comps.getRange('D53:H57').conditionalFormats.add('colorScale',{colors:['#F3E1D3','#F5F6F7','#9FB2C5'],thresholds:['min',{type:'percentile',value:50},'max']});

// Selected comps value
section(comps,59,'Selected comparable-company value','H');
label(comps,60,'Selected peer multiple (x)');
formula(comps,'D60','=D54');
label(comps,61,'Selected revenue base ($bn)');
formula(comps,'D61','=F39');
label(comps,62,'Comparable-company enterprise value ($bn)');
formula(comps,'D62','=D60*D61');
comps.getRange('D60').setNumberFormat(multiple);
comps.getRange('D61').setNumberFormat(money);
comps.getRange('D62').setNumberFormat(money);
comps.getRange('C60:D62').format.font.bold=true;
total(comps,62,'H');
note(comps,63,'Only like-for-like pairing available: a private frontier lab multiple on a frontier lab ARR base.','C');
note(comps,64,'Tier 2 multiples embed a capital-light margin profile Anthropic does not have; Tier 3 embeds the opposite.','C');
comps.getRange('E60:H64').format.horizontalAlignment='left';

// Peer statistics
section(comps,66,'Peer multiple statistics - value or EV / revenue (x)','F');
comps.getRange('C67:F67').values=[['Statistic','Tier 1 (labs)','Tier 2 (software)','Tier 3 (neocloud)']];
comps.getRange('C67:F67').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const stats=[['Median','MEDIAN'],['Mean','AVERAGE'],['Low','MIN'],['High','MAX'],['Observations (n)','COUNT']];
stats.forEach(([t,fn],i)=>{
  const r=68+i;
  label(comps,r,t);
  formula(comps,`D${r}`,`=${fn}(J7:J8)`);
  formula(comps,`E${r}`,`=${fn}(J16:J20)`);
  formula(comps,`F${r}`,`=${fn}(J25:J26)`);
  comps.getRange(`D${r}:F${r}`).setNumberFormat(fn==='COUNT'?'0':multiple);
});

// Caveats
section(comps,74,'Why this peer set is imperfect','L');
const caveats=[
 'No listed company combines frontier-model development with Anthropic growth and capital intensity. Every comp is partial.',
 'Tier 1 marks are negotiated or secondary prints, not exchange prices. OpenAI alone spans 12.2x to 17.1x on one revenue base.',
 'Tier 2 firms are capital-light. Their multiples embed a margin and capex profile Anthropic has not demonstrated.',
 'Tier 3 matches the compute-commitment profile but not the software margin profile.',
 'Anthropic gross versus net revenue recognition is unresolved. Channel distribution fees were 35.1% of sales in 2025 [S3].',
 'If revenue is restated net of channel fees, every multiple in this sheet rises and every implied value falls proportionally.',
];
caveats.forEach((t,i)=>{value(comps,`C${75+i}`,t);comps.getRange(`C${75+i}`).format.font={italic:true,color:'#606A75'};});
value(comps,'C82','This sheet supports research only. It is not a personal investment recommendation.');
comps.getRange('C82').format.font={italic:true,color:colors.red};
comps.freezePanes.freezeRows(4);

/* ------------------------------ VALUATION ------------------------------ */
section(model,6,'Valuation results', 'I');
const resultRows={7:'Revenue-multiple enterprise value',8:'DCF enterprise value',9:'Comparable-company enterprise value',10:'Reported IPO equity benchmark',11:'Multiple equity / benchmark - 1',12:'DCF equity / benchmark - 1',13:'Comps EV / benchmark - 1',14:'Benchmark EV / 2028 revenue',15:'Terminal value / DCF enterprise value',17:'2028 revenue used',18:'Selected EV / revenue multiple'};
for(const [r,t] of Object.entries(resultRows)) label(model,r,t);
const resultFormulas={7:'=D23',8:'=D57',9:"='Comps'!D62",10:"='Inputs'!D15",11:'=D25/D10-1',12:'=IF(ISNUMBER(D58),D58/D10-1,"n.a.")',13:'=D9/D10-1',14:'=(D10-D24)/D21',15:'=D59',17:'=D21',18:'=D22'};
for(const [r,f] of Object.entries(resultFormulas)) formula(model,`D${r}`,f,true);
for(const r of [7,8,9,10,17]) model.getRange(`D${r}`).setNumberFormat(money);
for(const r of [11,12,13,15]) model.getRange(`D${r}`).setNumberFormat(percent);
for(const r of [14,18]) model.getRange(`D${r}`).setNumberFormat(multiple);
for(const r of [11,12,13,14,18]) model.getRange(`C${r}:D${r}`).format.font.italic=true;
note(model,7,'2028 revenue x selected forward multiple.');
note(model,8,'2027-2036 cash flows plus perpetual growth.');
note(model,9,'Frontier-lab secondary multiple on exit-2026 ARR. See Comps.');
note(model,10,'Reference target. Final offer price is unavailable.');
note(model,11,'Illustrative equity comparison using assumed net cash.');
note(model,12,'Gap indicates growth and cash margins required.');
note(model,13,'Comps sits below the benchmark; DCF sits far below both.');
note(model,14,'Converts equity target using the net cash assumption.');
note(model,15,'Measures reliance on cash flows beyond 2036.');
note(model,17,'Midpoint of a reported company forecast.');
note(model,18,'Editable on Inputs.');
model.getRange('E7:I18').format.horizontalAlignment='left';
total(model,7,'I');total(model,8,'I');total(model,9,'I');

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
formula(model,'D31',"=D30/'Inputs'!D37-1");
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
const termLabels={46:'2037 terminal revenue',47:'Terminal EBIT',48:'Terminal cash taxes',49:'Terminal after-tax operating profit',50:'Terminal D&A',51:'Terminal cash capex',52:'Terminal change in working capital',53:'Terminal unlevered free cash flow',54:'Terminal enterprise value',55:'Present value of terminal value',56:'PV of 2027-2036 free cash flow',57:'DCF enterprise value',58:'Illustrative DCF equity value',59:'Terminal value / enterprise value',60:'Terminal FCF needed for benchmark',61:'Terminal EBIT margin needed'};
for(const [r,t]of Object.entries(termLabels))label(model,r,t);
const termFormulas={46:"=N30*(1+'Inputs'!D13)",47:'=D46*N32',48:"=-MAX(D47,0)*'Inputs'!D14",49:'=SUM(D47:D48)',50:"=D46*'Inputs'!N25",51:"=-D46*'Inputs'!N26",52:"=-(D46-N30)*'Inputs'!N27",53:'=SUM(D49:D52)',54:"=IF('Inputs'!D11>'Inputs'!D13,D53/('Inputs'!D11-'Inputs'!D13),\"n.a.\")",55:'=IF(ISNUMBER(D54),D54*N42,"n.a.")',56:'=SUM(E43:N43)',57:'=IF(ISNUMBER(D55),SUM(D55:D56),"n.a.")',58:'=IF(ISNUMBER(D57),D57+D24,"n.a.")',59:'=IF(ISNUMBER(D57),D55/D57,"n.a.")',60:"=IF('Inputs'!D11>'Inputs'!D13,(D10-D24-D56)/N42*('Inputs'!D11-'Inputs'!D13),\"n.a.\")",61:"=IF(ISNUMBER(D60),(D60-SUM(D50:D52))/D46/(1-'Inputs'!D14),\"n.a.\")"};
for(const [r,f]of Object.entries(termFormulas))formula(model,`D${r}`,f);
model.getRange('D46:D58').setNumberFormat(money);
model.getRange('D60').setNumberFormat(money);
for(const r of [59,61]){model.getRange(`D${r}`).setNumberFormat(percent);model.getRange(`C${r}:D${r}`).format.font.italic=true;}
total(model,57);total(model,58);
note(model,54,'Terminal FCF / (WACC - growth). Returns n.a. if WACC <= growth.');
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
value(model,'C73','Each cell is revenue x multiple. Middle revenue row follows the model. Column multiples are illustrative assumptions.');
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

// Triangulation
section(model,89,'Valuation triangulation ($bn)','I');
model.getRange('C90:E90').values=[['Method','Value','vs IPO benchmark']];
model.getRange('C90:E90').format={fill:colors.pale,font:{bold:true},horizontalAlignment:'center'};
const triang=[
 ['DCF enterprise value','=D8'],
 ['Comps - neocloud median x 2026E',"='Comps'!E57"],
 ['Comps - frontier-lab secondary x exit-2026 ARR',"='Comps'!F54"],
 ['Comps - AI-software median x 2026E',"='Comps'!E55"],
 ['Comps - selected',"='Comps'!D62"],
 ['Last private round (Series H)',"='Inputs'!D39"],
 ['Secondary market mark',"='Inputs'!D55"],
 ['Institutional fair value, low',"='Inputs'!D56"],
 ['IPO equity benchmark','=D10'],
];
triang.forEach(([t,f],i)=>{
  const r=91+i;
  label(model,r,t);
  formula(model,`D${r}`,f);
  formula(model,`E${r}`,`=IF(ISNUMBER(D${r}),D${r}/$D$10-1,"n.a.")`);
  model.getRange(`D${r}`).setNumberFormat(money);
  model.getRange(`E${r}`).setNumberFormat(percent);
});
total(model,95,'E');
model.getRange('F91:I99').format.horizontalAlignment='left';
value(model,'C101','Net cash is assumed zero, so enterprise value equals equity value throughout.');
value(model,'C102','DCF and the neocloud multiple cluster near $0.8tn. The AI-software multiple reaches $2.7tn.');
value(model,'C103','The entire $2tn case rests on which peer tier the market assigns, not on the discount rate.');
model.getRange('C101:C103').format.font={italic:true,color:'#606A75'};
value(model,'C105','This model supports research only. It is not a personal investment recommendation.');
model.getRange('C105').format.font={italic:true,color:colors.red};

// Live forecast chart reads the operating build directly
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

// Triangulation bar chart
const bchart=model.charts.add('bar');
bchart.title='Valuation triangulation ($bn)';
bchart.titleTextStyle.typeface='Arial';bchart.titleTextStyle.fontSize=12;
const bseries=bchart.series.add('Value ($bn)');
bseries.categoryFormula="'Valuation'!$C$91:$C$99";
bseries.formula="'Valuation'!$D$91:$D$99";
bchart.hasLegend=false;
bchart.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial',fontSize:10}};
bchart.yAxis={numberFormatCode:'$0',numberFormatSourceLinked:false,textStyle:{typeface:'Arial',fontSize:10}};
bchart.setPosition('J20','N36');

/* --------------------------- VERIFICATION --------------------------- */
function expected() {
 const growth=[1,ANCHOR28/(BASE26*2)-1,.35,.25,.2,.15,.1,.07,.05,.03];
 const margins=[.1,.2,.25,.3,.32,.33,.34,.35,.35,.35];
 const wacc=.12,tax=.25,g=.03;
 let priorRev=BASE26,priorWc=BASE26*.02,pv=0,rev,fcf;
 for(let t=1;t<=10;t++){
  rev=priorRev*(1+growth[t-1]);
  const wc=rev*.02;
  fcf=rev*margins[t-1]*(1-tax)+rev*.03-rev*.08-(wc-priorWc);
  pv+=fcf/(1+wacc)**t;priorRev=rev;priorWc=wc;
 }
 const nextRev=rev*(1+g);
 const terminalFcf=nextRev*.35*(1-tax)+nextRev*.03-nextRev*.08-(nextRev-rev)*.02;
 const terminalPv=terminalFcf/(wacc-g)/(1+wacc)**10;
 return {rev2036:rev,pv,terminalFcf,terminalPv,dcf:pv+terminalPv,multipleEv:ANCHOR28*10,terminalShare:terminalPv/(pv+terminalPv)};
}
function assertClose(cell, expectedValue, tolerance=1e-7, sheet=model) {
 const actual=sheet.getRange(cell).values[0][0];
 if(typeof actual!=='number'||Math.abs(actual-expectedValue)>tolerance*Math.max(1,Math.abs(expectedValue))) throw new Error(`${cell}: expected ${expectedValue}, got ${actual}`);
}
// Independent comps arithmetic
const tier1=[852/70,1200/70];
const tier2=[432/8.15,109/2.62,218/8.91,128/9.35,41.6];
const tier3=[86.6/12.93,56.6/3.2];
const med=a=>{const s=[...a].sort((x,y)=>x-y);const m=s.length>>1;return s.length%2?s[m]:(s[m-1]+s[m])/2;};
const expComps={t1med:med(tier1),t2med:med(tier2),t3med:med(tier3),selected:(1200/70)*110,t2x26:med(tier2)*BASE26,t3x26:med(tier3)*BASE26};

const e=expected();
assertClose('D7',1950);assertClose('D8',e.dcf);assertClose('N30',e.rev2036);assertClose('D56',e.pv);
assertClose('D30',BASE26);assertClose('E30',BASE26*2);assertClose('F30',ANCHOR28);
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
assertClose('D7',e.multipleEv);assertClose('D8',e.dcf);assertClose('D15',e.terminalShare);
assertClose('J7',tier1[0],1e-9,comps);assertClose('J8',tier1[1],1e-9,comps);
assertClose('J16',tier2[0],1e-9,comps);assertClose('J20',41.6,1e-9,comps);
assertClose('D53',expComps.t1med,1e-9,comps);assertClose('D55',expComps.t2med,1e-9,comps);assertClose('D57',expComps.t3med,1e-9,comps);
assertClose('D62',expComps.selected,1e-9,comps);
assertClose('E55',expComps.t2x26,1e-9,comps);assertClose('E57',expComps.t3x26,1e-9,comps);
assertClose('D9',expComps.selected);
assertClose('E39',BASE26,1e-9,comps);assertClose('F39',110,1e-9,comps);assertClose('G39',BASE26*2,1e-9,comps);assertClose('H39',ANCHOR28,1e-9,comps);
// Comps should react when a peer multiple is perturbed
value(comps,'G16',16.3,true);
if(!(comps.getRange('D55').values[0][0]<expComps.t2med))throw new Error('Tier 2 median did not react to a peer multiple change');
value(comps,'G16',8.15,true);
if(Math.abs(comps.getRange('D55').values[0][0]-expComps.t2med)>1e-6)throw new Error('Tier 2 median did not restore');

const headline=await wb.inspect({kind:'table',range:'Valuation!C6:E19',include:'values,formulas',tableMaxRows:14,tableMaxCols:3,maxChars:3500});
console.log(headline.ndjson);
const triangView=await wb.inspect({kind:'table',range:'Valuation!C89:E99',include:'values',tableMaxRows:11,tableMaxCols:3,maxChars:3000});
console.log(triangView.ndjson);
const compsView=await wb.inspect({kind:'table',range:'Comps!C42:H48',include:'values',tableMaxRows:7,tableMaxCols:6,maxChars:3000});
console.log(compsView.ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'Formula errors',maxChars:1000});
console.log(errors.ndjson);
console.log(JSON.stringify({independent:e,comps:expComps,requiredMargin:model.getRange('D61').values[0][0],verified:['multiple perturbation','later-period margin','WACC/growth boundary','IPO zero and positive proceeds','missing and zero share count','comps multiples and medians','comps peer perturbation'],charts:[chart.series.items.length,bchart.series.items.length]},null,2));

for(const [s,range,name]of [[model,'C2:N18','valuation_summary'],[model,'C28:N43','dcf_forecast'],[model,'C45:N105','valuation_detail'],[comps,'C2:L82','comps_table'],[inputs,'C2:N33','assumptions'],[inputs,'C35:N67','public_sources']]){
 const preview=await wb.render({sheetName:s.name,range,scale:1.3,format:'png'});
 await fs.writeFile(`${outputDir}/${name}.png`,new Uint8Array(await preview.arrayBuffer()));
}
const out=await SpreadsheetFile.exportXlsx(wb);
await out.save(`${outputDir}/Anthropic_IPO_Basic_Valuation.xlsx`);
await fs.writeFile(`${outputDir}/verification.json`,JSON.stringify({independent:e,comps:expComps,requiredMargin:model.getRange('D61').values[0][0],errors:errors.ndjson},null,2));
console.log('Saved Anthropic_IPO_Basic_Valuation.xlsx');
