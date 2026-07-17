// Build separate catalog JSONs for raw (local_data) and processed (processed_data) files
const fs = require('fs');
const path = require('path');

function walkDir(dir) {
    let results = [];
    const items = fs.readdirSync(dir);
    for (const item of items) {
        const full = path.join(dir, item);
        const stat = fs.statSync(full);
        if (stat.isDirectory()) {
            // Skip 'processed' subfolder inside local_data
            if (item === 'processed' && dir.endsWith('local_data')) continue;
            results = results.concat(walkDir(full));
        } else if (item.endsWith('.csv')) {
            results.push(full.replace(/\\/g, '/'));
        }
    }
    return results;
}

function categorize(filePath) {
    const p = filePath.toLowerCase();
    if (p.includes('/institutional_frameworks/')) return { cat: 'Comparative/Legal', inst: 'OECD / Eurydice / Legislative', src: 'https://github.com/Eugenix94/Italienation/tree/main/local_data/institutional_frameworks' };
    if (p.includes('/istat/')) return { cat: 'ISTAT', inst: 'ISTAT Open Data', src: 'https://esploradati.istat.it/' };
    if (p.includes('/eurostat/')) return { cat: 'Eurostat', inst: 'Eurostat', src: 'https://ec.europa.eu/eurostat/databrowser/' };
    if (p.includes('/oecd/') || p.includes('/ocse/')) return { cat: 'OECD', inst: 'OECD', src: 'https://data.oecd.org/' };
    if (p.includes('/ministruzione/') || p.includes('/mim/')) return { cat: 'MIM', inst: 'Ministero Istruzione', src: 'https://dati.istruzione.it/opendata/' };
    if (p.includes('/mur/')) return { cat: 'MUR', inst: 'MUR/USTAT', src: 'https://ustat.mur.gov.it/' };
    if (p.includes('/invalsi/')) return { cat: 'INVALSI', inst: 'INVALSI Open Data', src: 'https://invalsi-open.cineca.it/index.php?get=statistiche' };
    if (p.includes('/mef/') || p.includes('/siope/')) return { cat: 'MEF/SIOPE', inst: 'MEF/OpenCivitas', src: 'https://opencivitas.mef.gov.it/' };
    if (p.includes('/inps/')) return { cat: 'INPS', inst: 'INPS Open Data', src: 'https://servizi2.inps.it/servizi/statistiche/' };
    if (p.includes('/almalaurea/')) return { cat: 'AlmaLaurea', inst: 'AlmaLaurea', src: 'https://www.almalaurea.it/universita/dati-e-ricerche/indagini' };
    if (p.includes('/anpal/')) return { cat: 'ANPAL', inst: 'ANPAL', src: 'https://www.anpal.gov.it/' };
    if (p.includes('/openpolis/')) return { cat: 'Openpolis', inst: 'Openpolis', src: 'https://www.openpolis.it/' };
    if (p.includes('/opencoesione/')) return { cat: 'OpenCoesione', inst: 'OpenCoesione', src: 'https://opencoesione.gov.it/' };
    if (p.includes('/ourworlddata/') || p.includes('/worldbank/')) return { cat: 'Global', inst: 'Our World in Data / World Bank', src: 'https://ourworldindata.org/' };
    if (p.includes('/uksdgstats/')) return { cat: 'UK SDG', inst: 'UK Office for National Statistics', src: 'https://sdgdata.gov.uk/' };
    if (p.includes('/openeurydice/')) return { cat: 'Eurydice', inst: 'European Commission Eurydice', src: 'https://eurydice.eacea.ec.europa.eu/' };
    return { cat: 'Other', inst: 'Various', src: 'https://github.com/Eugenix94/Italienation' };
}

function nameFromPath(fp) {
    const base = path.basename(fp, '.csv');
    return base.replace(/[_-]+/g, ' ').replace(/\b\w/g, c => c.toUpperCase()).substring(0, 80);
}

// Build RAW catalog (local_data, excluding local_data/processed)
const rawFiles = walkDir('local_data');
const rawCatalog = rawFiles.map(f => {
    const c = categorize(f);
    return { path: f, name: nameFromPath(f), category: c.cat, institution: c.inst, source: c.src };
});

// Build PROCESSED catalog (processed_data)
const procFiles = walkDir('processed_data');
const procCatalog = procFiles.map(f => ({
    path: f, name: nameFromPath(f), category: 'Processed', institution: 'Italienation Project', source: 'https://github.com/Eugenix94/Italienation/tree/main/processed_data'
}));

fs.writeFileSync('web/catalog_raw.json', JSON.stringify(rawCatalog));
fs.writeFileSync('web/catalog_processed.json', JSON.stringify(procCatalog));

console.log(`Raw: ${rawCatalog.length} files (${(fs.statSync('web/catalog_raw.json').size/1024).toFixed(1)} KB)`);
console.log(`Processed: ${procCatalog.length} files (${(fs.statSync('web/catalog_processed.json').size/1024).toFixed(1)} KB)`);

// Show categories breakdown for raw
const cats = {};
rawCatalog.forEach(x => { cats[x.category] = (cats[x.category]||0)+1; });
console.log('\nRaw categories:');
Object.entries(cats).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`  ${k}: ${v}`));
