const fs = require('fs');
const masterPath = 'c:/Users/Dell/Documents/Antigravity/Italienation/frontend/public/data/master_data_observatory.json';
const outPath = 'c:/Users/Dell/Documents/Antigravity/Italienation/frontend/src/assets/originLinks.json';

const master = JSON.parse(fs.readFileSync(masterPath, 'utf8'));
const originLinks = {};

for (const catName of Object.keys(master)) {
  for (const ds of master[catName]) {
    const fname = ds.filename.toLowerCase();
    let inst_url = "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/";

    if (fname.includes("huggingface") || fname.includes("hf_")) {
        inst_url = "https://huggingface.co/datasets/diatribe00/italian-schools-opendata/tree/main/";
    } else if (["alu", "edi", "bis", "doc", "ata"].some(k => fname.includes(k)) && fname.length > 8 && !fname.includes("istat")) {
        const code = ds.filename.substring(0, 6).toUpperCase();
        inst_url = `https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=ricerca&q=${code}`;
    } else if (fname.includes("invalsi") || fname.includes("punteggi") || fname.includes("eccellenza")) {
        inst_url = "https://invalsi-serviziostatistico.cineca.it/";
    } else if (fname.includes("istat") || fname.includes("dccv") || fname.includes("neet") || fname.includes("asili_nido") || fname.includes("bocciati") || fname.includes("income_by_region") || fname.includes("employment") || fname.includes("poverty") || fname.includes("household") || fname.includes("youth") || fname.includes("graduates")) {
        inst_url = "https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z07,1.0/ALL_THEMES/IT1";
    } else if (fname.includes("eurostat") || fname.includes("estat") || fname.includes("educ_uoe") || fname.includes("edat")) {
        let code = fname.replace("estat_", "").replace("eurostat_", "").split("_")[0].split(".")[0];
        if (!code || code.length < 3) code = "edat_lfse_20";
        inst_url = `https://ec.europa.eu/eurostat/databrowser/view/${code}/default/table`;
    } else if (fname.includes("oecd") || fname.includes("pisa") || fname.includes("escs") || fname.includes("teacher")) {
        inst_url = "https://data-explorer.oecd.org/";
    } else if (fname.includes("worldbank") || fname.includes("wb_")) {
        inst_url = "https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS";
    } else if (fname.includes("mur") || fname.includes("fuorisede") || fname.includes("university")) {
        inst_url = "https://ustat.mur.gov.it/dati/";
    } else if (fname.includes("almalaurea") || fname.includes("almadiploma")) {
        inst_url = "https://www2.almalaurea.it/cgi-php/universita/statistiche/tendine.php?config=occupazione";
    } else if (fname.includes("bancaditalia") || fname.includes("shiw") || fname.includes("gini") || fname.includes("financial_literacy")) {
        inst_url = "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/index.html";
    } else if (fname.includes("federconsumatori") || fname.includes("textbook") || fname.includes("corredo")) {
        inst_url = "https://www.federconsumatori.it/caro-scuola-2024-2025-aumenti-a-dismisura-su-libri-e-materiale-scolastico/";
    } else if (fname.includes("macro_cost_of_failure")) {
        inst_url = "https://www.ambrosetti.eu/ricerche-e-studi/";
    } else if (fname.includes("pnrr") || fname.includes("opencoesione")) {
        inst_url = "https://opencoesione.gov.it/it/opendata/";
    } else if (fname.includes("openpolis") || fname.includes("transport")) {
        inst_url = "https://www.openpolis.it/esercizi-di-potere/";
    } else if (fname.includes("anpal")) {
        inst_url = "https://www.lavoro.gov.it/";
    } else if (fname.includes("mim") || fname.includes("diplomifici") || fname.includes("curriculum") || fname.includes("quadro_orario") || fname.includes("ptof") || fname.includes("pof") || fname.includes("framework")) {
        inst_url = "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/";
    }

    originLinks[ds.id] = inst_url;
  }
}

fs.writeFileSync(outPath, JSON.stringify(originLinks, null, 2));
console.log('Successfully generated precise institutional links for ' + Object.keys(originLinks).length + ' datasets.');
