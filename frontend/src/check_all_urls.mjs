import https from 'https';
import fs from 'fs';

const urls = {
  // Topic-specific deep links
  "shadow": "https://www.istat.it/statistiche/economia-non-osservata/",
  "neet": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "mismatch": "https://excelsior.unioncamere.net/",
  "brain_drain": "https://www.istat.it/argomento/popolazione-e-famiglie/",
  "dispersione": "https://dati.istruzione.it/opendata/",
  "bocciatura": "https://dati.istruzione.it/opendata/",
  "pcto": "https://dati.inail.it/portale/it.html",
  "textbooks": "https://federconsumatori.it/",
  "orals": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview",
  "governance": "https://databank.worldbank.org/source/worldwide-governance-indicators",
  "malta": "https://jobsplus.gov.mt/",
  "pes": "https://employment-social-affairs.ec.europa.eu/node/25_en",
  "escs": "https://www.invalsi.it/valutazione/",
  "tracking": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview",
  "scores": "https://serviziostatistico.invalsi.it/",
  "dropouts": "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Studenti&datasetId=DS0280AGESREG17",
  "religione": "https://www.uaar.it/",
  
  // Agency portal fallbacks
  "ISTAT": "https://www.istat.it/argomento/istruzione-e-formazione/",
  "MIM": "https://dati.istruzione.it/opendata/",
  "MIUR": "https://dati.istruzione.it/opendata/",
  "MUR": "https://www.mur.gov.it/",
  "Eurostat": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "OECD": "https://www.oecd.org/en/topics/sub-issues/pisa-results.html",
  "World Bank": "https://databank.worldbank.org/source/worldwide-governance-indicators",
  "INAIL": "https://www.inail.it/cs/internet/attivita/dati-e-statistiche/infortuni.html",
  "INPS": "https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche.html",
  "Federconsumatori": "https://federconsumatori.it/",
  "Eurydice": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview",
  "Corte dei Conti": "https://www.corteconti.it/Home/Documenti/Relazioni",
  "Save the Children": "https://www.savethechildren.it/cosa-facciamo/pubblicazioni",
  "Unioncamere": "https://excelsior.unioncamere.net/",
  "INVALSI": "https://www.invalsi.it/valutazione/",
  "EU PES Network": "https://employment-social-affairs.ec.europa.eu/node/25_en",
  "Jobsplus": "https://jobsplus.gov.mt/",
  "UAAR / FOIA": "https://www.uaar.it/",

  // Holistic expansion: Pension, Healthcare, Justice, Energy (Aug 2026)
  "eurostat_pensions": "https://ec.europa.eu/eurostat/databrowser/view/tps00103/default/table",
  "oecd_pensions_glance": "https://www.oecd.org/els/public-pensions/",
  "fondazione_gimbe": "https://www.gimbe.org/",
  "oecd_health_data": "https://data-explorer.oecd.org/",
  "worldbank_out_of_pocket": "https://data.worldbank.org/indicator/SH.XPD.OOPC.CH.ZS",
  "fnomceo_anaao": "https://www.fnomceo.it/",
  "cepej_justice_scoreboard": "https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/upholding-rule-law/eu-justice-scoreboard_en",
  "worldbank_doing_business": "https://archive.doingbusiness.org/en/doingbusiness",
  "eurostat_energy_electricity": "https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_205/default/table",
  "openpnrr_corte_dei_conti": "https://openpnrr.it/",
  "trading_economics_electricity": "https://tradingeconomics.com/italy/electricity-price",

  // PNRR Tracker & Migration (Aug 2026)
  "italia_domani": "https://www.italiadomani.gov.it",
  "eu_commission_rrf": "https://commission.europa.eu/business-economy-euro/economic-recovery/recovery-and-resilience-facility_en",
  "istat_demographics": "https://demo.istat.it/",
  "worldbank_wgi": "https://datacatalog.worldbank.org/dataset/worldwide-governance-indicators",
  "aire_esteri": "https://www.esteri.it/en/servizi-consolari-e-visti/italiani-all-estero/aire_0/",
  "mipex_italy": "https://www.mipex.eu/italy",
  "eurostat_asylum": "https://ec.europa.eu/eurostat/web/migration-asylum/asylum/database"
};

const checkUrl = (key, url) => {
  return new Promise((resolve) => {
    https.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0' },
      timeout: 10000
    }, (res) => {
      resolve({ key, url, status: res.statusCode });
    }).on('error', (e) => {
      resolve({ key, url, status: e.code });
    }).on('timeout', () => {
      resolve({ key, url, status: 'TIMEOUT' });
    });
  });
};

async function run() {
  console.log('Checking URLs...');
  const promises = Object.entries(urls).map(([key, url]) => checkUrl(key, url));
  const results = await Promise.all(promises);
  const broken = results.filter(r => r.status >= 400 || typeof r.status === 'string');
  console.log(`\nFound ${broken.length} broken/unreachable URLs:`);
  console.log(JSON.stringify(broken, null, 2));
}

run();
