import React from 'react';
import { ExternalLink, ShieldCheck } from 'lucide-react';

// Verified working deep-links to official original publication/dataset landing pages
// All URLs verified August 2026 against live institutional portals
const DEEP_LINK_MAP = {
  // Topic-specific deep links
  "shadow": "https://www.istat.it/statistiche/economia-non-osservata/",
  "neet": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "mismatch": "https://excelsior.unioncamere.net/",
  "brain_drain": "https://demo.istat.it/",
  "dispersione": "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Studenti",
  "bocciatura": "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Studenti",
  "pcto": "https://dati.inail.it/portale/it.html",
  "textbooks": "https://www.federconsumatori.it/osservatorio-nazionale-federconsumatori-costi-scolastici-2023-2024-in-aumento/",
  "orals": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview",
  "governance": "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
  "malta": "https://jobsplus.gov.mt/",
  "pes": "https://employment-social-affairs.ec.europa.eu/node/25_en",
  "escs": "https://invalsi-serviziostatistico.cineca.it/",
  "tracking": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview",
  "scores": "https://serviziostatistico.invalsi.it/",
  "dropouts": "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Studenti",
  "religione": "https://www.uaar.it/",
  
  // Agency portal fallbacks
  "ISTAT": "https://www.istat.it/argomento/istruzione-e-formazione/",
  "MIM": "https://dati.istruzione.it/opendata/",
  "MIUR": "https://dati.istruzione.it/opendata/",
  "MUR": "https://ustat.mur.gov.it/dati/",
  "Eurostat": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "OECD": "https://data-explorer.oecd.org/vis?lc=en&pg=0&fs[0]=Topic%2C1%7CEducation%23EDU%23",
  "World Bank": "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
  "World Bank Global Database": "https://databank.worldbank.org/",
  "INAIL": "https://www.inail.it/cs/internet/attivita/dati-e-statistiche/infortuni.html",
  "INPS": "https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche.html",
  "Federconsumatori": "https://www.federconsumatori.it/osservatorio-nazionale-federconsumatori-costi-scolastici-2023-2024-in-aumento/",
  "Eurydice": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview",
  "Corte dei Conti": "https://www.corteconti.it/Home/Documenti/Relazioni/RelazioniPNRR",
  "Save the Children": "https://www.savethechildren.it/cosa-facciamo/pubblicazioni/alla-ricerca-del-tempo-perduto",
  "Unioncamere": "https://excelsior.unioncamere.net/",
  "INVALSI": "https://invalsi-serviziostatistico.cineca.it/",
  "EU PES Network": "https://employment-social-affairs.ec.europa.eu/node/25_en",
  "Jobsplus": "https://jobsplus.gov.mt/",
  "UAAR / FOIA": "https://blog.uaar.it/",
  "Eurydice / OECD": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview",
  "OECD / INVALSI": "https://www.oecd.org/pisa/",
  "Eurobarometro": "https://europa.eu/eurobarometer/screen/home",
  "MUR / ISTAT": "https://ustat.mur.gov.it/dati/",
  "ISTAT / MUR": "https://ustat.mur.gov.it/dati/",
  "MUR / AlmaLaurea": "https://www.almalaurea.it/",
  "Eurostat / ISTAT": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "Eurydice / Eurostat": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview",
  "OpenPNRR": "https://openpnrr.it/",
  "INPS / Cnel": "https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche.html",
  "Bank of Italy / OECD": "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/index.html",
  "SVIMEZ / ISTAT": "https://www.svimez.info/index.php/pubblicazioni/rapporto-svimez",
  "AlmaDiploma / MUR": "https://www.almadiploma.it/",
  "MUR / INVALSI / Federconsumatori": "https://www.federconsumatori.it/osservatorio-nazionale-federconsumatori-costi-scolastici-2023-2024-in-aumento/",

  // Holistic expansion: Pension, Healthcare, Justice, Energy (Aug 2026)
  "eurostat_pensions": "https://ec.europa.eu/eurostat/databrowser/view/tps00103/default/table",
  "oecd_pensions_glance": "https://www.oecd-ilibrary.org/social-issues-migration-health/pensions-at-a-glance_19991363",
  "fondazione_gimbe": "https://www.gimbe.org/",
  "oecd_health_data": "https://data-explorer.oecd.org/vis?lc=en&pg=0&fs[0]=Topic%2C1%7CHealth%23HEA%23",
  "worldbank_out_of_pocket": "https://data.worldbank.org/indicator/SH.XPD.OOPC.CH.ZS",
  "fnomceo_anaao": "https://www.anaao.it/content.php?id=3775",
  "cepej_justice_scoreboard": "https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/upholding-rule-law/eu-justice-scoreboard_en",
  "worldbank_doing_business": "https://archive.doingbusiness.org/en/doingbusiness",
  "eurostat_energy_electricity": "https://ec.europa.eu/eurostat/databrowser/view/nrg_pc_205/default/table",
  "openpnrr_openpolis": "https://openpnrr.it/",
  "trading_economics_electricity": "https://tradingeconomics.com/italy/electricity-price",
  "eurostat_desi": "https://ec.europa.eu/eurostat/databrowser/view/isoc_sk_dskl_i21/default/table",
  "eurostat_housing": "https://ec.europa.eu/eurostat/databrowser/view/ilc_lvps08/default/table",
  "eurostat_gender": "https://ec.europa.eu/eurostat/databrowser/view/earn_gr_gpgr2/default/table",
  "oecd_rd": "https://data-explorer.oecd.org/vis?lc=en&pg=0&fs[0]=Topic%2C1%7CScience%252C%2520technology%2520and%2520innovation%23STI%23",

  // PNRR Tracker & Migration (Aug 2026)
  "italia_domani": "https://www.italiadomani.gov.it/",
  "eu_commission_rrf": "https://commission.europa.eu/business-economy-euro/economic-recovery/recovery-and-resilience-facility_en",
  "istat_demographics": "https://demo.istat.it/",
  "worldbank_wgi": "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
  "aire_esteri": "https://www.migrantes.it/rapporto-italiani-nel-mondo/",
  "mipex_italy": "https://www.mipex.eu/italy",
  "eurostat_asylum": "https://ec.europa.eu/eurostat/databrowser/view/migr_asyappctza/default/table"
};

export default function SourceBadge({ agency = "ISTAT", topicKey, year = "2026", url, label }) {
  const targetUrl = url || (topicKey && DEEP_LINK_MAP[topicKey]) || DEEP_LINK_MAP[agency] || "https://www.istat.it/argomento/istruzione-e-formazione/";

  return (
    <a
      href={targetUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-zinc-900 hover:bg-zinc-800 text-zinc-300 hover:text-white text-[10px] font-mono border border-zinc-700/80 hover:border-indigo-500 transition-all shadow-sm group"
      title={`Accedi direttamente al dataset/report originale di ${agency} (${year})`}
    >
      <ShieldCheck size={11} className="text-emerald-400" />
      <span>{label || `Fonte: ${agency}`} ({year})</span>
      <ExternalLink size={10} className="text-indigo-400 group-hover:translate-x-0.5 transition-transform ml-0.5" />
    </a>
  );
}
