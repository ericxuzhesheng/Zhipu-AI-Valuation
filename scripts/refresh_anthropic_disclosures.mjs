import fs from 'node:fs/promises';
import path from 'node:path';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';

const root = path.resolve(import.meta.dirname, '..');
const target = path.join(root, 'anthropic/2026-10-11/Anthropic_IPO_Basic_Valuation.xlsx');
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(target));
const inputs = wb.worksheets.getItem('Inputs');
const valuation = wb.worksheets.getItem('Valuation');
const runtime = path.join(root, 'tmp/1011_runtime');
if (process.argv.includes('--inspect')) {
  console.log((await wb.inspect({ kind: 'region', sheetId: 'Valuation', range: 'C6:I19', maxChars: 1500 })).ndjson);
  const preview = await wb.render({ sheetName: 'Valuation', range: 'C6:I19', scale: 1.5, format: 'png' });
  await fs.writeFile(path.join(runtime, 'anthropic-before.png'), new Uint8Array(await preview.arrayBuffer()));
} else {
  const expected = JSON.parse(await fs.readFile(path.join(runtime, 'anthropic-latest.json'), 'utf8'));
  inputs.getRange('D8').values = [[new Date(`${expected.cutoff}T00:00:00Z`)]];
  inputs.getRange('C3').values = [['USD billions. S-1 review: 26 Oct 2026. Annuals audited; interim statements unaudited.']];
  valuation.getRange('C3').values = [['USD billions. S-1 review: 26 Oct 2026. Valuation date remains assumed 31 Dec 2026.']];
  inputs.getRange('F8').values = [['Public S-1 included [S25]; filing PDF conversion used; EDGAR HTML retrieval blocked.']];
  inputs.getRange('F12').values = [['Zero remains a Dec-2026 assumption. June liquidity and debt sensitivities appear below.']];
  inputs.getRange('F16').values = [['Public S-1 leaves offering size blank. Proceeds remain an unfilled input.']];
  inputs.getRange('F18').values = [['Final post-conversion diluted offering share count remains blank in the S-1.']];
  valuation.getRange('F81').values = [['Final IPO share count remains blank; historical shares cannot determine an offer price.']];
  inputs.getRange('F15').values = [['USD1.5tn discussion reaffirmed 22 Oct [S20]; offering not priced.']];
  inputs.getRange('C45:G45').values = [['IPO investor discussion, about', 1500, '22-Oct-26 BJT', 'Media-reported', 'S20']];
  inputs.getRange('C46:G46').values = [['Prior Reuters compute observation', 518, '15-Oct-26', 'Historical report', 'S19']];
  inputs.getRange('C29').values = [['2026 revenue of USD64bn remains an analyst assumption, not a reported annual result.']];
  inputs.getRange('C30').values = [['Latest quarterly observations and a full-year reconciliation appear below and on Valuation.']];
  inputs.getRange('I36:M36').copyFrom(inputs.getRange('C36:G36'), 'all');
  inputs.getRange('I36:M36').values = [['Period', 'Revenue $bn', 'Available BJT', 'Classification', 'Source']];
  inputs.getRange('I37:M39').copyFrom(inputs.getRange('C37:G39'), 'all');
  inputs.getRange('I37:M39').values = [
    ['2026Q1', expected.quarters[0], new Date('2026-10-26T00:00:00Z'), 'S-1 unaudited', 'S25'],
    ['2026Q2', expected.quarters[1], new Date('2026-10-26T00:00:00Z'), 'S-1 unaudited', 'S25'],
    ['2026Q3', expected.quarters[2], new Date('2026-10-15T00:00:00Z'), 'Reuters; not S-1', 'S19'],
  ];
  inputs.getRange('J37:J39').setNumberFormat('0.000');
  inputs.getRange('K37:K39').setNumberFormat('yyyy-mm-dd');
  inputs.getRange('C125').values = [['S18. Reuters, 15 Oct 21:00 UTC / 16 Oct 05:00 Beijing. IPO investor discussion.']];
  inputs.getRange('C126').values = [['https://www.aol.com/articles/exclusive-investors-temper-anthropic-ipo-210007000.html']];
  inputs.getRange('C128').values = [['S19. Reuters, 15 Oct Beijing. Quarterly revenue and decade-long compute commitments.']];
  inputs.getRange('C129').values = [['https://uk.marketscreener.com/news/anthropic-s-q3-revenue-surges-45-to-nearly-17-billion-ce785dd2d08cf221']];
  inputs.getRange('C131').values = [['S20. Reuters, 22 Oct 22:51 Beijing; November IPO timetable is provisional.']];
  inputs.getRange('C132').values = [['https://uk.marketscreener.com/news/anthropic-ipo-stands-alone-as-ai-market-jitters-sideline-others-ce785cdeda8cf026']];
  inputs.getRange('C134').values = [['S21. Anthropic, 18 Oct: 5% public-benefit share commitment, subject to shareholder approval.']];
  inputs.getRange('C135').values = [['https://www.anthropic.com/news/public-benefit-fund']];
  inputs.getRange('C137').values = [['S22. Claude Duet, 21 Oct: US Pro/Max research preview, with shared plan limits.']];
  inputs.getRange('C138').values = [['https://claude.com/resources/articles/claude-duet']];
  inputs.getRange('C140').values = [['S23. Claude Platform on Google Cloud, 22 Oct: Anthropic managed service generally available.']];
  inputs.getRange('C141').values = [['https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed']];
  inputs.getRange('C143').values = [['S24. Agent Skills donated to AAIF, 22 Oct; no quantified revenue or cash-flow uplift.']];
  inputs.getRange('C144').values = [['https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation']];
  valuation.getRange('C114').values = [['26 Oct S-1 included: Q1/Q2 are exact filing values; Q3 remains Reuters-reported.']];
  valuation.getRange('C115').values = [['S-1 annuals are audited; interim statements are unaudited. Forecasts remain assumptions.']];
  valuation.getRange('C116').values = [['June liquidity is not December net cash. Amazon conversion is subject to an ownership cap.']];
  valuation.getRange('C101').values = [['Active December net-cash assumption remains zero; separate June snapshot sensitivities are shown below.']];
  valuation.getRange('C103').values = [['Latest investor discussion is USD1.5tn; the earlier USD2tn expectation is a historical stress case.']];
  valuation.getRange('C10').values = [['IPO investor discussion']];
  valuation.getRange('C99').values = [['IPO investor discussion']];
  valuation.getRange('F10').values = [['Investor discussion; no priced offering or company valuation guidance.']];
  valuation.getRange('F13').values = [['Heterogeneous peer references; excluded from Zhipu transaction multiples.']];
  valuation.getRange('C108:D108').values = [['Reported quarters and annual revenue assumption', null]];
  valuation.getRange('C109:C112').values = [['Reported Q1-Q3 revenue (USD bn)'], ['FY2026 revenue assumption (USD bn)'], ['Q4 revenue needed (USD bn)'], ['Required Q4 growth vs Q3']];
  valuation.getRange('D109:D112').formulas = [["=SUM('Inputs'!J37:J39)"], ["='Inputs'!D22"], ['=D110-D109'], ["=D111/'Inputs'!J39-1"]];
  valuation.getRange('D109:D111').setNumberFormat('0.000');
  valuation.getRange('D112').setNumberFormat('0.0%');
  // Extend the existing input/output sections; retain the operating forecast and share-price blanks.
  const number = '#,##0.000;(#,##0.000);"-"';
  inputs.getRange('C146').values = [['S1 actuals in USD bn: FY2025 audited; H1 periods and quarterly MD&A unaudited.']];
  inputs.getRange('C148:H157').format = { font: { name: 'Arial', size: 10 }, rowHeight: 23 };
  inputs.getRange('C148:H148').values = [['S1 actuals', 'FY2025', 'H1 2025', 'H1 2026', 'Unit', 'Source']];
  const metrics = [
    ['Revenue', 'revenue_usdbn'], ['Operating income (loss)', 'operating_income_usdbn'],
    ['Net income (loss)', 'net_income_usdbn'], ['Financing fair-value loss', 'financing_fair_value_loss_usdbn'],
    ['Operating cash flow', 'operating_cash_flow_usdbn'], ['Cash capex', 'cash_capex_usdbn'],
    ['D&A', 'da_usdbn'], ['Share-based compensation', 'share_based_compensation_usdbn'],
  ];
  inputs.getRange('C149:H156').values = metrics.map(([label, metric]) =>
    [label, ...['FY2025', 'H1 2025', 'H1 2026'].map(period => expected.financials[period][metric]), 'USD bn', 'S25']);
  inputs.getRange('C37:G38').values = [
    ['Revenue', null, '2025', 'S-1 audited', 'S25'],
    ['Operating income (loss)', null, '2025', 'S-1 audited', 'S25'],
  ];
  inputs.getRange('D37:D38').formulas = [['=D149'], ['=D150']];
  inputs.getRange('D37:D38').setNumberFormat(number);
  inputs.getRange('D149:F156').setNumberFormat(number);
  inputs.getRange('C160:H172').format = { font: { name: 'Arial', size: 10 }, rowHeight: 23 };
  inputs.getRange('C160:H160').values = [['June 2026 balance / terms', 'Value', 'Unit', 'Status', 'Source', null]];
  const balances = [
    ['Cash and equivalents', 'Cash and equivalents'], ['Short-term investments', 'Short-term investments'],
    ['Restricted cash (excluded)', 'Restricted cash'], ['Notes at fair value', 'Convertible note carrying value'],
    ['Amazon 2023 principal', 'Amazon 2023 note principal'], ['Amazon 2024 principal', 'Amazon 2024 note principal'],
    ['Finance lease liabilities', 'Finance lease liabilities'], ['Operating lease liabilities', 'Operating lease liabilities'],
    ['Uncommenced lease obligations', 'Uncommenced lease obligations'], ['Minimum purchase commitments', 'Minimum purchase commitments'],
    ['Amazon conversion ownership cap', 'Amazon conversion ownership cap'],
  ];
  inputs.getRange('C161:H171').values = balances.map(([label, metric]) =>
    [label, expected.balance[metric], metric.includes('cap') ? 'fraction' : 'USD bn', 'S1; see notes', 'S25', null]);
  inputs.getRange('D161:D170').setNumberFormat(number);
  inputs.getRange('D171').setNumberFormat('0%');
  inputs.getRange('C173').values = [['Purchase commitments and uncommenced leases are separate multiyear categories, not current debt.']];
  inputs.getRange('C175').values = [['S25. Anthropic Form S-1 filed 26 Oct 2026. MD&A p160/p164; statements F-5/F-7/F-12; notes F-35/F-58.']];
  inputs.getRange('C176').values = [['https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm']];
  inputs.getRange('C178').values = [['Retrieval: SEC HTML blocked / reader size limit. Filing PDF conversion checked; conversion fidelity is a source limitation.']];
  inputs.getRange('C179').values = [['https://sec2pdf.com/ANTHROPIC']];
  valuation.getRange('C118:N141').format = { font: { name: 'Arial', size: 10 }, rowHeight: 23 };
  valuation.getRange('C118').values = [['S1 operating observations (USD bn)']];
  valuation.getRange('C119:C124').values = [['H1 2026 revenue'], ['H1 operating income (loss)'], ['H1 net income (loss)'], ['H1 operating cash flow'], ['H1 cash flow less cash capex'], ['H1 financing fair-value loss']];
  valuation.getRange('D119:D124').formulas = [
    ["='Inputs'!F149"], ["='Inputs'!F150"], ["='Inputs'!F151"], ["='Inputs'!F153"],
    ["=D122-'Inputs'!F154"], ["='Inputs'!F152"],
  ];
  valuation.getRange('F119').values = [['H1 interim statements are unaudited; Q3 revenue remains a separate media observation.']];
  valuation.getRange('F123').values = [['Cash-flow less cash capex is not unlevered FCF; vendor-payment timing affects operating cash flow.']];
  valuation.getRange('C126').values = [['June cash bridge sensitivity (USD bn)']];
  valuation.getRange('C127:C135').values = [
    ['Cash plus short-term investments'], ['Less: finance lease liabilities'], ['Amazon note principal'],
    ['Cash proxy: notes retained'], ['Cash proxy: full conversion'], ['DCF equity: notes retained'],
    ['DCF equity: full conversion'], ['Terminal margin: notes retained'], ['Terminal margin: full conversion'],
  ];
  valuation.getRange('D127:D133').formulas = [
    ["=SUM('Inputs'!D161:D162)"], ["='Inputs'!D167"], ["=SUM('Inputs'!D165:D166)"],
    ['=D127-SUM(D128:D129)'], ['=D127-D128'], ['=$D$8+D130'], ['=$D$8+D131'],
  ];
  valuation.getRange('D134:D135').formulas = [130, 131].map(row =>
    [`=((D10-D${row}-D56)/N42*('Inputs'!D11-'Inputs'!D13)-SUM(D50:D52))/D46/(1-'Inputs'!D14)`]);
  valuation.getRange('D119:D133').setNumberFormat(number);
  valuation.getRange('D134:D135').setNumberFormat('0.0%');
  valuation.getRange('C137').values = [['June snapshot only: no H2 cash roll-forward, new funding or IPO proceeds; not an existing-common equity allocation.']];
  valuation.getRange('C138').values = [['Full conversion is illustrative, subject to Amazon 12% ownership cap; residual notes may remain outstanding.']];
  valuation.getRange('C139').values = [['Restricted cash is excluded. Operating rent remains in forecast margins and is not deducted a second time.']];
  valuation.getRange('C140').values = [['The USD108.566bn note carrying value is not the USD6.203bn cash principal.']];
  for (const [sheet, range] of [[inputs, 'C148:H148'], [inputs, 'C160:H160'], [valuation, 'C118:N118'], [valuation, 'C126:N126']]) {
    sheet.getRange(range).format = { fill: '#31465A', font: { name: 'Arial', size: 10, bold: true, color: '#FFFFFF' }, rowHeight: 25 };
  }
  wb.recalculate();
  const close = (actual, target, label) => { if (Math.abs(actual - target) > 1e-8) throw new Error(`${label}: ${actual} != ${target}`); };
  close(valuation.getRange('D8').values[0][0], expected.dcf, 'DCF');
  close(valuation.getRange('D10').values[0][0], 1500, 'IPO benchmark');
  close(valuation.getRange('D61').values[0][0], expected.requiredMargin, 'Reverse margin');
  close(valuation.getRange('D111').values[0][0], expected.q4Required, 'Q4 reconciliation');
  close(valuation.getRange('D112').values[0][0], expected.q4Growth, 'Q4 growth');
  close(valuation.getRange('D119').values[0][0], 16.286, 'H1 revenue');
  close(inputs.getRange('D37').values[0][0], 4.585, 'Audited FY2025 revenue reference');
  close(valuation.getRange('D123').values[0][0], 3.447, 'Cash flow less cash capex');
  close(valuation.getRange('D132').values[0][0], expected.bridges[0].dcf_equity_usdbn, 'Principal bridge equity');
  close(valuation.getRange('D135').values[0][0], expected.bridges[1].required_terminal_ebit_margin, 'Conversion bridge margin');
  inputs.getRange('D45').values = [[2000]];
  wb.recalculate();
  close(valuation.getRange('D61').values[0][0], expected.historicalMargin, 'Historical benchmark propagation');
  inputs.getRange('D45').values = [[1500]];
  inputs.getRange('D161').values = [[expected.balance['Cash and equivalents'] + 1]];
  wb.recalculate();
  close(valuation.getRange('D132').values[0][0], expected.bridges[0].dcf_equity_usdbn + 1, 'Cash input propagation');
  inputs.getRange('D161').values = [[expected.balance['Cash and equivalents']]];
  inputs.getRange('D12').values = [[10]];
  wb.recalculate();
  close(valuation.getRange('D58').values[0][0], expected.dcf + 10, 'Active net-cash propagation');
  inputs.getRange('D12').values = [[0]];
  wb.recalculate();
  console.log((await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!', options: { useRegex: true, maxResults: 30 }, maxChars: 1000 })).ndjson);
  for (const [sheetName, range, filename] of [['Valuation', 'C6:I19', 'anthropic-after'], ['Valuation', 'C108:N140', 'anthropic-s1-review'], ['Inputs', 'C146:H171', 'anthropic-s1-inputs']]) {
    const preview = await wb.render({ sheetName, range, scale: 1.5, format: 'png' });
    await fs.writeFile(path.join(runtime, `${filename}.png`), new Uint8Array(await preview.arrayBuffer()));
  }
  await (await SpreadsheetFile.exportXlsx(wb)).save(target);
  console.log(JSON.stringify({ benchmark: 1500, dcf: expected.dcf, q4Required: expected.q4Required, propagationVerified: true }));
}
