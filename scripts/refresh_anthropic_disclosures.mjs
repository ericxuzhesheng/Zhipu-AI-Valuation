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
  inputs.getRange('D8').values = [[new Date('2026-10-16T00:00:00Z')]];
  inputs.getRange('F8').values = [['Reviewed through 16 Oct 2026 Beijing time; latest observations in S18/S19.']];
  inputs.getRange('F15').values = [['Investor discussion reported 16 Oct Beijing time [S18]; not a priced offer.']];
  inputs.getRange('C45:G45').values = [['IPO investor discussion, about', 1500, '16-Oct-26 BJT', 'Media-reported', 'S18']];
  inputs.getRange('C46:G46').values = [['Long-term compute commitments, at least', 518, 'Oct-26', 'Media-reported', 'S19']];
  inputs.getRange('C29').values = [['2026 revenue of USD64bn remains an analyst assumption, not a reported annual result.']];
  inputs.getRange('C30').values = [['Latest quarterly observations and a full-year reconciliation appear below and on Valuation.']];
  inputs.getRange('I36:M36').copyFrom(inputs.getRange('C36:G36'), 'all');
  inputs.getRange('I36:M36').values = [['Period', 'Revenue $bn', 'Available BJT', 'Classification', 'Source']];
  inputs.getRange('I37:M39').copyFrom(inputs.getRange('C37:G39'), 'all');
  inputs.getRange('I37:M39').values = [
    ['2026Q1', 4.7, new Date('2026-10-15T00:00:00Z'), 'Media-reported', 'S19'],
    ['2026Q2', 11.6, new Date('2026-10-15T00:00:00Z'), 'Media-reported', 'S19'],
    ['2026Q3', 16.8, new Date('2026-10-15T00:00:00Z'), 'Media-reported', 'S19'],
  ];
  inputs.getRange('J37:J39').setNumberFormat('0.0');
  inputs.getRange('K37:K39').setNumberFormat('yyyy-mm-dd');
  inputs.getRange('C125').values = [['S18. Reuters, 15 Oct 21:00 UTC / 16 Oct 05:00 Beijing. IPO investor discussion.']];
  inputs.getRange('C126').values = [['https://www.aol.com/articles/exclusive-investors-temper-anthropic-ipo-210007000.html']];
  inputs.getRange('C128').values = [['S19. Reuters, 15 Oct Beijing. Quarterly revenue and decade-long compute commitments.']];
  inputs.getRange('C129').values = [['https://uk.marketscreener.com/news/anthropic-s-q3-revenue-surges-45-to-nearly-17-billion-ce785dd2d08cf221']];
  valuation.getRange('C103').values = [['Latest investor discussion is USD1.5tn; the earlier USD2tn expectation is a historical stress case.']];
  valuation.getRange('C10').values = [['IPO investor discussion']];
  valuation.getRange('C99').values = [['IPO investor discussion']];
  valuation.getRange('F10').values = [['Investor discussion; no priced offering or company valuation guidance.']];
  valuation.getRange('F13').values = [['Heterogeneous peer references; excluded from Zhipu transaction multiples.']];
  valuation.getRange('C108:D108').values = [['Reported quarters and annual revenue assumption', null]];
  valuation.getRange('C109:C112').values = [['Reported Q1-Q3 revenue (USD bn)'], ['FY2026 revenue assumption (USD bn)'], ['Q4 revenue needed (USD bn)'], ['Required Q4 growth vs Q3']];
  valuation.getRange('D109:D112').formulas = [["=SUM('Inputs'!J37:J39)"], ["='Inputs'!D22"], ['=D110-D109'], ["=D111/'Inputs'!J39-1"]];
  valuation.getRange('D109:D111').setNumberFormat('0.0');
  valuation.getRange('D112').setNumberFormat('0.0%');
  wb.recalculate();
  const expected = JSON.parse(await fs.readFile(path.join(runtime, 'anthropic-latest.json'), 'utf8'));
  const close = (actual, target, label) => { if (Math.abs(actual - target) > 1e-8) throw new Error(`${label}: ${actual} != ${target}`); };
  close(valuation.getRange('D8').values[0][0], expected.dcf, 'DCF');
  close(valuation.getRange('D10').values[0][0], 1500, 'IPO benchmark');
  close(valuation.getRange('D61').values[0][0], expected.requiredMargin, 'Reverse margin');
  close(valuation.getRange('D111').values[0][0], 30.9, 'Q4 reconciliation');
  close(valuation.getRange('D112').values[0][0], 30.9 / 16.8 - 1, 'Q4 growth');
  inputs.getRange('D45').values = [[2000]];
  wb.recalculate();
  close(valuation.getRange('D61').values[0][0], expected.historicalMargin, 'Historical benchmark propagation');
  inputs.getRange('D45').values = [[1500]];
  wb.recalculate();
  console.log((await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!', options: { useRegex: true, maxResults: 30 }, maxChars: 1000 })).ndjson);
  for (const [sheetName, range, filename] of [['Valuation', 'C6:I19', 'anthropic-after'], ['Valuation', 'C108:F112', 'anthropic-reconciliation'], ['Inputs', 'I36:M39', 'anthropic-quarter-inputs']]) {
    const preview = await wb.render({ sheetName, range, scale: 1.5, format: 'png' });
    await fs.writeFile(path.join(runtime, `${filename}.png`), new Uint8Array(await preview.arrayBuffer()));
  }
  await (await SpreadsheetFile.exportXlsx(wb)).save(target);
  console.log(JSON.stringify({ benchmark: 1500, dcf: expected.dcf, q4Required: 30.9, propagationVerified: true }));
}
