const fs = require('fs');

// Fix EconometricCosts.jsx
let file = 'frontend/src/components/EconometricCosts.jsx';
let content = fs.readFileSync(file, 'utf8');
content = content.replace(/import \{ Loader2 \} from 'lucide-react';/, "import { Loader2, TrendingDown } from 'lucide-react';");
content = content.replace(/import DataTooltip from '\.\/DataTooltip';\n/, "");
content = content.replace(/import SectionContext from '\.\/SectionContext';\n/, "");
fs.writeFileSync(file, content);

// Fix TerritorialMap.jsx
file = 'frontend/src/components/TerritorialMap.jsx';
content = fs.readFileSync(file, 'utf8');
content = content.replace(/import \{ MapContainer, TileLayer, GeoJSON \} from 'react-leaflet';/, "import { MapContainer, GeoJSON } from 'react-leaflet';");
fs.writeFileSync(file, content);

// Fix LaborMarketAndCorrelations.jsx
file = 'frontend/src/components/LaborMarketAndCorrelations.jsx';
content = fs.readFileSync(file, 'utf8');
const laborRegex = /<div className="text-center max-w-3xl mx-auto mb-16">[\s\S]*?<\/p>\n\s*<\/motion\.div>\n\s*<\/div>/;
const laborReplace = `<SectionContext 
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
        />`;
content = content.replace(laborRegex, laborReplace);
fs.writeFileSync(file, content);

// Fix MigrationAndRemittances.jsx
file = 'frontend/src/components/MigrationAndRemittances.jsx';
content = fs.readFileSync(file, 'utf8');
const migRegex = /<div className="text-center max-w-3xl mx-auto mb-16">[\s\S]*?<\/p>\n\s*<\/motion\.div>\n\s*<\/div>/;
const migReplace = `<SectionContext 
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
        />`;
content = content.replace(migRegex, migReplace);
content = content.replace(/import \{ Globe, Users, TrendingUp, Briefcase \} from 'lucide-react';/, "import { Globe, Users, TrendingUp } from 'lucide-react';");
fs.writeFileSync(file, content);

console.log('Linting errors fixed.');
