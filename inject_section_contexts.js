const fs = require('fs');

function injectContext(file, importRegex, importString, targetRegex, replacementString) {
  let content = fs.readFileSync(file, 'utf8');
  if (!content.includes('import SectionContext')) {
    content = content.replace(importRegex, importString);
    content = content.replace(targetRegex, replacementString);
    fs.writeFileSync(file, content);
    console.log(`Updated ${file}`);
  }
}

// 1. SystemicDeepDives
injectContext(
  'frontend/src/components/SystemicDeepDives.jsx',
  /import \{ T \} from "\.\/T";/,
  'import { T } from "./T";\nimport SectionContext from "./SectionContext";',
  /<div className="text-center space-y-4">[\s\S]*?<\/div>/,
  `<SectionContext 
          domainIt="Meccaniche Strutturali" 
          domainEn="Structural Mechanics"
          titleIt="Deep Dive Sistemici" 
          titleEn="Systemic Deep Dives"
          thesisIt="Le inefficienze del sistema scolastico italiano non sono casuali, ma derivano da precise scelte di governance, meccanismi di valutazione soggettiva e distorsioni di mercato che penalizzano sistematicamente gli studenti."
          thesisEn="The inefficiencies of the Italian school system are not random, but stem from specific governance choices, subjective evaluation mechanisms, and market distortions that systematically penalize students."
          takeaways={[
            {it: "Il verticalismo burocratico blocca l'innovazione", en: "Bureaucratic verticalism blocks innovation"},
            {it: "Il mercato dei libri di testo è un oligopolio inelastico", en: "The textbook market is an inelastic oligopoly"},
            {it: "Le valutazioni soggettive generano dispersione", en: "Subjective evaluations drive dropout rates"}
          ]}
        />`
);

// 2. EconometricCosts
injectContext(
  'frontend/src/components/EconometricCosts.jsx',
  /import \{ T \} from '\.\/T';/,
  'import { T } from "./T";\nimport SectionContext from "./SectionContext";',
  /<motion\.div\n\s*initial=\{\{ opacity: 0, y: 20 \}\}\n\s*animate=\{\{ opacity: 1, y: 0 \}\}\n\s*transition=\{\{ duration: 0\.8 \}\}\n\s*className="relative z-10 text-center mb-16"\n\s*>[\s\S]*?<\/motion\.div>/,
  `<SectionContext 
          domainIt="Macroeconomia" 
          domainEn="Macroeconomics"
          titleIt="Costi Economici del Fallimento" 
          titleEn="Economic Costs of Failure"
          thesisIt="Il fallimento educativo non è solo un problema sociale, è la causa principale del debito pubblico italiano. Il divario di competenze e l'esclusione sociale costano al Paese il 13.5% del PIL ogni anno."
          thesisEn="Educational failure is not just a social problem, it is the root cause of Italian public debt. The skills gap and social exclusion cost the country 13.5% of GDP every year."
          takeaways={[
            {it: "I NEET costano €36 Miliardi all'anno in mancata produttività", en: "NEETs cost €36 Billion annually in lost productivity"},
            {it: "L'economia sommersa pesa per €83 Miliardi", en: "The shadow economy weighs €83 Billion"},
            {it: "La fuga di cervelli è un trasferimento netto di ricchezza", en: "Brain drain is a net wealth transfer"}
          ]}
        />\n\n        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }} className="relative z-10 text-center mb-16"><h1 className="text-5xl md:text-7xl font-black mb-6 tracking-tight text-white flex justify-center"><DataTooltip titleIt="Metodologia di Calcolo (Costi Oculati)" titleEn="Calculation Methodology (Hidden Costs)" descIt="Il costo totale di €259 Miliardi è una stima conservativa che aggrega report di istituzioni ufficiali (ISTAT, Eurofound, INPS) relativi alle inefficienze strutturali del sistema Italia, calcolato su base annua." descEn="The €259 Billion total cost is a conservative estimate aggregating official institutional reports (ISTAT, Eurofound, INPS) regarding the structural inefficiencies of the Italian system, calculated on an annual basis." formulaIt="Costo NEET + Evasione Fiscale (Lavoro Nero) + Mismatch Competenze + Fuga Cervelli + Dispersione + Bocciature" formulaEn="NEET Cost + Shadow Economy Tax Loss + Skills Mismatch + Brain Drain + Dropout Cost + Retention Cost" position="bottom">€259 <span className="text-rose-500">Miliardi</span></DataTooltip></h1><p className="text-xl md:text-2xl text-zinc-300 font-medium max-w-3xl mx-auto"><T it="13.5% del PIL bruciato ogni anno dalle inefficienze sistemiche" en="13.5% of GDP burned every year by systemic inefficiencies" /></p></motion.div>`
);

// 3. LaborMarketAndCorrelations
injectContext(
  'frontend/src/components/LaborMarketAndCorrelations.jsx',
  /import \{ T \} from "\.\/T";/,
  'import { T } from "./T";\nimport SectionContext from "./SectionContext";',
  /<div className="text-center max-w-3xl mx-auto mb-16">[\s\S]*?<\/p>\n\s*<\/motion\.div>\n\s*<\/div>/,
  `<SectionContext 
          domainIt="Economia del Lavoro" 
          domainEn="Labor Economics"
          titleIt="Il Mercato del Lavoro" 
          titleEn="The Labor Market"
          thesisIt="Esiste una correlazione diretta tra l'architettura del sistema scolastico e le inefficienze del mercato del lavoro. Il tracciamento precoce e l'assenza di apprendistato generano il mismatch di competenze e spingono i giovani verso l'economia sommersa."
          thesisEn="There is a direct correlation between school system architecture and labor market inefficiencies. Early tracking and the absence of apprenticeships drive the skills mismatch and push youth into the shadow economy."
          takeaways={[
            {it: "Forte divario retributivo per i giovani (Under 30)", en: "Massive wage gap for youth (Under 30)"},
            {it: "Assenza di politiche attive efficaci (PES)", en: "Absence of effective active policies (PES)"},
            {it: "Correlazione tra tracciamento e tasso NEET", en: "Correlation between tracking and NEET rate"}
          ]}
        />`
);

// 4. MigrationAndRemittances
injectContext(
  'frontend/src/components/MigrationAndRemittances.jsx',
  /import \{ T \} from "\.\/T";/,
  'import { T } from "./T";\nimport SectionContext from "./SectionContext";',
  /<div className="text-center max-w-3xl mx-auto mb-16">[\s\S]*?<\/p>\n\s*<\/motion\.div>\n\s*<\/div>/,
  `<SectionContext 
          domainIt="Demografia" 
          domainEn="Demographics"
          titleIt="Fuga di Cervelli & Rimesse" 
          titleEn="Brain Drain & Remittances"
          thesisIt="L'Italia subisce un doppio drenaggio: esporta laureati a costo zero verso il Nord Europa e importa manodopera a basso costo, generando enormi deflussi di capitali tramite rimesse senza trattenere valore aggiunto."
          thesisEn="Italy suffers a double drain: it exports graduates at zero cost to Northern Europe and imports cheap labor, generating massive capital outflows through remittances without retaining added value."
          takeaways={[
            {it: "Sussidio netto al Nord Europa (Costo formazione)", en: "Net subsidy to Northern Europe (Training cost)"},
            {it: "Deflusso di capitali via rimesse (Bangladesh, Romania)", en: "Capital outflow via remittances"},
            {it: "Sostituzione demografica a bassa specializzazione", en: "Low-skill demographic substitution"}
          ]}
        />`
);

// 5. TripartiteSimulator
injectContext(
  'frontend/src/components/TripartiteSimulator.jsx',
  /import \{ T \} from '\.\/T';/,
  'import { T } from "./T";\nimport SectionContext from "./SectionContext";',
  /<div className="text-center max-w-3xl mx-auto mb-16">[\s\S]*?<\/p>\n\s*<\/motion\.div>\n\s*<\/div>/,
  `<SectionContext 
          domainIt="Sociologia dell'Educazione" 
          domainEn="Sociology of Education"
          titleIt="Il Simulatore di Tracciamento" 
          titleEn="The Tracking Simulator"
          thesisIt="Il sistema italiano costringe a una scelta irreversibile a 13 anni (Path Dependency). Questo strumento simula matematicamente come il background socio-economico predetermina i tassi di laurea in base al binario scolastico scelto."
          thesisEn="The Italian system forces an irreversible choice at age 13 (Path Dependency). This tool mathematically simulates how socio-economic background predetermines graduation rates based on the chosen school track."
          takeaways={[
            {it: "Forte componente di Path Dependency (Dipendenza dal percorso)", en: "Strong Path Dependency component"},
            {it: "Imbuto sociale: i Professionali bloccano l'accesso universitario", en: "Social funnel: Vocational schools block university access"},
            {it: "L'estrazione sociale pesa al 70% sull'esito finale", en: "Social extraction weighs 70% on final outcome"}
          ]}
        />`
);
