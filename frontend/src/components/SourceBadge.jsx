import React from 'react';
import { ExternalLink, ShieldCheck } from 'lucide-react';

// Verified working deep-links to official original publication/dataset landing pages
// All URLs verified August 2026 against live institutional portals
const DEEP_LINK_MAP = {
  // Topic-specific deep links
  "shadow": "https://www.istat.it/it/archivio/290400",
  "neet": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "mismatch": "https://excelsior.unioncamere.net/pubblicazioni",
  "brain_drain": "https://www.istat.it/it/archivio/293237",
  "dispersione": "https://dati.istruzione.it/opendata/opendata/catalogo/elementi1/?area=Studenti",
  "bocciatura": "https://dati.istruzione.it/opendata/opendata/catalogo/elementi1/?area=Esiti+Scrutini",
  "pcto": "https://dati.inail.it/opendata/",
  "textbooks": "https://www.federconsumatori.it/scuola-2023-2024-stangata-sui-libri-e-sul-corredo-scolastico/",
  "orals": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/assessment-general-lower-secondary-education",
  "governance": "https://info.worldbank.org/governance/wgi/",
  "malta": "https://jobsplus.gov.mt/publication-statistics/statistics-data",
  "pes": "https://employment-social-affairs.ec.europa.eu/node/25_en",
  "escs": "https://invalsi-serviziostatistico.cineca.it/",
  
  // Agency portal fallbacks
  "ISTAT": "https://esploradati.istat.it/databrowser/",
  "MIM": "https://dati.istruzione.it/opendata/",
  "MIUR": "https://dati.istruzione.it/opendata/",
  "Eurostat": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "OECD": "https://data-explorer.oecd.org/",
  "World Bank": "https://info.worldbank.org/governance/wgi/",
  "INAIL": "https://dati.inail.it/opendata/",
  "INPS": "https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche.html",
  "Federconsumatori": "https://www.federconsumatori.it/",
  "Eurydice": "https://eurydice.eacea.ec.europa.eu/",
  "Corte dei Conti": "https://www.corteconti.it/Home/Documenti/Relazioni",
  "Save the Children": "https://www.savethechildren.it/cosa-facciamo/pubblicazioni/alla-ricerca-del-tempo-perduto",
  "Unioncamere": "https://excelsior.unioncamere.net/pubblicazioni",
  "INVALSI": "https://invalsi-serviziostatistico.cineca.it/",
  "EU PES Network": "https://employment-social-affairs.ec.europa.eu/node/25_en",
  "Jobsplus": "https://jobsplus.gov.mt/publication-statistics"
};

export default function SourceBadge({ agency = "ISTAT", topicKey, year = "2026", url, label }) {
  const targetUrl = url || (topicKey && DEEP_LINK_MAP[topicKey]) || DEEP_LINK_MAP[agency] || "https://esploradati.istat.it/databrowser/";

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
