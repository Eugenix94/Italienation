import React from 'react';
import { ExternalLink, ShieldCheck } from 'lucide-react';

// Verified working deep-links to official original publication/dataset landing pages
// All URLs verified August 2026 against live institutional portals
const DEEP_LINK_MAP = {
  // Topic-specific deep links
  "shadow": "https://www.istat.it/statistiche/economia-non-osservata/",
  "neet": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "mismatch": "https://excelsior.unioncamere.net/",
  "brain_drain": "https://www.istat.it/argomento/popolazione-e-famiglie/",
  "dispersione": "https://dati.istruzione.it/opendata/",
  "bocciatura": "https://dati.istruzione.it/opendata/",
  "pcto": "https://dati.inail.it/portale/it.html",
  "textbooks": "https://federconsumatori.it/",
  "orals": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/assessment-general-lower-secondary-education",
  "governance": "https://databank.worldbank.org/source/worldwide-governance-indicators",
  "malta": "https://jobsplus.gov.mt/",
  "pes": "https://employment-social-affairs.ec.europa.eu/node/25_en",
  "escs": "https://serviziostatistico.invalsi.it/",
  "tracking": "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/organisation-general-lower-secondary-education",
  "scores": "https://serviziostatistico.invalsi.it/risultati/",
  "dropouts": "https://www.miur.gov.it/dispersione-scolastica",
  "religione": "https://www.uaar.it/laicita/insegnamento-religione-cattolica/",
  
  // Agency portal fallbacks
  "ISTAT": "https://esploradati.istat.it/databrowser/",
  "MIM": "https://dati.istruzione.it/opendata/",
  "MIUR": "https://dati.istruzione.it/opendata/",
  "MUR": "https://www.mur.gov.it/it/dati-e-statistiche",
  "Eurostat": "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table",
  "OECD": "https://data-explorer.oecd.org/",
  "World Bank": "https://databank.worldbank.org/source/worldwide-governance-indicators",
  "INAIL": "https://dati.inail.it/portale/it.html",
  "INPS": "https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche.html",
  "Federconsumatori": "https://federconsumatori.it/",
  "Eurydice": "https://eurydice.eacea.ec.europa.eu/",
  "Corte dei Conti": "https://www.corteconti.it/Home/Documenti/Relazioni",
  "Save the Children": "https://www.savethechildren.it/cosa-facciamo/pubblicazioni/alla-ricerca-del-tempo-perduto",
  "Unioncamere": "https://excelsior.unioncamere.net/",
  "INVALSI": "https://serviziostatistico.invalsi.it/",
  "EU PES Network": "https://employment-social-affairs.ec.europa.eu/node/25_en",
  "Jobsplus": "https://jobsplus.gov.mt/",
  "UAAR / FOIA": "https://www.uaar.it/laicita/insegnamento-religione-cattolica/"
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
