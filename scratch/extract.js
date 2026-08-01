const fs = require('fs');
const content = fs.readFileSync('c:/Users/Dell/Documents/Antigravity/Italienation/FILE_BY_FILE_PROVENANCE.md', 'utf8');
const lines = content.split('\n');
const links = {};

for (const line of lines) {
  if (line.includes('[Direct Link]')) {
    const parts = line.split('|');
    if (parts.length >= 6) {
      const filenameRaw = parts[2].trim().replace(/`/g, '');
      const linkRaw = parts[5].trim();
      const match = linkRaw.match(/\[Direct Link\]\(([^)]+)\)/);
      if (match) {
        let name = filenameRaw.replace('.csv', '').replace('.xlsx', '').replace('.parquet', '');
        links[name] = match[1];
      }
    }
  }
}

const master = JSON.parse(fs.readFileSync('c:/Users/Dell/Documents/Antigravity/Italienation/frontend/public/data/master_data_observatory.json', 'utf8'));
const originLinks = {};
let found = 0;
let fallback = 0;

for (const catName of Object.keys(master)) {
  for (const ds of master[catName]) {
    const key = ds.filename.replace('.csv', '');
    if (links[key] && !links[key].includes('Generated via') && !links[key].includes('Literature Review')) {
      originLinks[ds.id] = links[key];
      found++;
    } else {
      originLinks[ds.id] = 'https://dati.gov.it/';
      fallback++;
    }
  }
}

fs.writeFileSync('c:/Users/Dell/Documents/Antigravity/Italienation/frontend/src/assets/originLinks.json', JSON.stringify(originLinks, null, 2));
console.log('Found exact links: ' + found + ', Fallbacks: ' + fallback);
