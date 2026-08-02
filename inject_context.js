const fs = require('fs');

let file = 'frontend/src/components/LaborMarketAndCorrelations.jsx';
let content = fs.readFileSync(file, 'utf8');

if (!content.includes('import DataTooltip')) {
  content = content.replace(
    /import \{ T \} from '\.\/T';/, 
    'import { T } from "./T";\nimport DataTooltip from "./DataTooltip";\nimport MethodologyAlert from "./MethodologyAlert";'
  );

  content = content.replace(
    /La correlazione inversa/,
    '<DataTooltip titleIt="Varianza Statistica" titleEn="Statistical Variance" descIt="L\'analisi bivariata rivela una forte correlazione negativa. Questa non è causalità diretta, ma indica che i paesi con sistemi scolastici olistici hanno anche meccanismi di mercato del lavoro più forti." descEn="Bivariate analysis reveals a strong negative correlation. This is not direct causality, but indicates that countries with holistic school systems also have stronger labor market mechanisms." source="OECD (2024)"><span className="border-b border-dashed border-zinc-500/50 hover:border-indigo-400/50 transition-colors">La correlazione inversa</span></DataTooltip>'
  );
  
  content = content.replace(
    /<\/motion\.div>\n\s*<\/div>\n\s*<\/section>/,
    '  <MethodologyAlert itText="L\'analisi di correlazione incrocia i dati PISA (OCSE) e le classifiche della Rete Europea dei Servizi Pubblici per l\'Impiego. Le variabili indipendenti (es. Tracciamento scolastico) sono analizzate contro i tassi NEET Eurostat." enText="The correlation analysis cross-references PISA data (OECD) and the rankings of the European Network of Public Employment Services. Independent variables (e.g., School Tracking) are analyzed against Eurostat NEET rates." />\n      </motion.div>\n      </div>\n    </section>'
  );

  fs.writeFileSync(file, content);
  console.log('Updated LaborMarketAndCorrelations.jsx');
}

file = 'frontend/src/components/MigrationAndRemittances.jsx';
content = fs.readFileSync(file, 'utf8');
if (!content.includes('import MethodologyAlert')) {
  content = content.replace(
    /import \{ T \} from '\.\/T';/, 
    'import { T } from "./T";\nimport MethodologyAlert from "./MethodologyAlert";'
  );
  
  content = content.replace(
    /<\/motion\.div>\n\s*<\/div>\n\s*<\/section>/,
    '  <MethodologyAlert itText="I dati sui flussi delle rimesse (2024-2025) sono aggregati dai database trimestrali e provinciali della Banca d\'Italia, integrati con i profili dei corridoi migratori della Banca Mondiale." enText="Remittance flow data (2024-2025) are aggregated from the Bank of Italy quarterly and provincial databases, integrated with World Bank migration corridor profiles." linkUrl="https://www.bancaditalia.it/statistiche/tematiche/rapporti-estero/rimesse-immigrati/index.html" linkText="Banca d\'Italia - Rimesse" />\n      </motion.div>\n      </div>\n    </section>'
  );
  
  fs.writeFileSync(file, content);
  console.log('Updated MigrationAndRemittances.jsx');
}

file = 'frontend/src/components/SystemicDeepDives.jsx';
content = fs.readFileSync(file, 'utf8');
if (!content.includes('import DataTooltip')) {
  content = content.replace(
    /import \{ T \} from '\.\/T';/, 
    'import { T } from "./T";\nimport DataTooltip from "./DataTooltip";'
  );
  
  content = content.replace(
    /Asimmetria di Scelta/,
    '<DataTooltip titleIt="Asimmetria Informativa e di Scelta" titleEn="Asymmetry of Choice and Information" descIt="In economia, è un fallimento del mercato. Chi sceglie il prodotto (il docente) non ne sopporta il costo, mentre chi paga (la famiglia) non ha potere decisionale. Questo annulla l\'elasticità della domanda al prezzo." descEn="In economics, this is a market failure. The decision maker (teacher) bears no cost, while the payer (family) has no decision power. This nullifies price elasticity of demand." source="AGCM (Autorità Garante della Concorrenza)"><span className="border-b border-dashed border-zinc-500/50 hover:border-indigo-400/50 transition-colors">Asimmetria di Scelta</span></DataTooltip>'
  );
  
  fs.writeFileSync(file, content);
  console.log('Updated SystemicDeepDives.jsx');
}

