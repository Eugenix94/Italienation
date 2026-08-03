const fs = require('fs');

const file = 'frontend/src/components/GISMap.jsx';
let content = fs.readFileSync(file, 'utf8');

// Ensure DataTooltip is imported
if (!content.includes('import DataTooltip from')) {
  content = content.replace(
    /import SourceBadge from '\.\/SourceBadge';/,
    "import SourceBadge from './SourceBadge';\nimport DataTooltip from './DataTooltip';"
  );
}

// 1. Replace europeData array
const oldEuropeDataRegex = /const europeData = \[[\s\S]*?\];/;
const newEuropeData = `const europeData = [
  { id: 'IT', name: 'Italia', lat: 41.8719, lng: 12.5674, color: '#f43f5e', trackAge: 14, neet: '19.0%', pcto: '0€ (Unpaid)', dropout: '11.5%', type: 'Early Tracking' },
  { id: 'DE', name: 'Germania', lat: 51.1657, lng: 10.4515, color: '#10b981', trackAge: 10, neet: '8.6%', pcto: '€900/mo (Dual)', dropout: '12.2%', type: 'Dual VET' },
  { id: 'FI', name: 'Finlandia', lat: 61.9241, lng: 25.7482, color: '#4f46e5', trackAge: 16, neet: '9.3%', pcto: 'Free Books & Meals', dropout: '7.3%', type: 'Comprehensive' },
  { id: 'FR', name: 'Francia', lat: 46.2276, lng: 2.2137, color: '#f59e0b', trackAge: 15, neet: '11.2%', pcto: 'Alternance', dropout: '7.6%', type: 'Comprehensive' },
  { id: 'SE', name: 'Svezia', lat: 60.1282, lng: 18.6435, color: '#3b82f6', trackAge: 16, neet: '6.1%', pcto: 'Comprehensive', dropout: '8.4%', type: 'Comprehensive' },
  { id: 'ES', name: 'Spagna', lat: 40.4637, lng: -3.7492, color: '#f43f5e', trackAge: 16, neet: '12.7%', pcto: 'Unpaid/Low', dropout: '13.9%', type: 'Comprehensive (Late)' },
  { id: 'PL', name: 'Polonia', lat: 51.9194, lng: 19.1451, color: '#10b981', trackAge: 15, neet: '10.9%', pcto: 'VET Supported', dropout: '4.8%', type: 'Comprehensive' },
  { id: 'NL', name: 'Paesi Bassi', lat: 52.1326, lng: 5.2913, color: '#8b5cf6', trackAge: 12, neet: '4.2%', pcto: 'Paid VET', dropout: '5.3%', type: 'Early Tracking (Fluid)' },
  { id: 'AT', name: 'Austria', lat: 47.5162, lng: 14.5501, color: '#10b981', trackAge: 10, neet: '9.1%', pcto: '€800/mo (Dual)', dropout: '8.1%', type: 'Dual VET' },
  { id: 'GR', name: 'Grecia', lat: 39.0742, lng: 21.8243, color: '#f43f5e', trackAge: 15, neet: '15.4%', pcto: 'Unpaid', dropout: '4.1%', type: 'Comprehensive' }
];`;

content = content.replace(oldEuropeDataRegex, newEuropeData);

// 2. Replace the Europe map markers to include the Tooltip
const oldEuropeMapMarkerRegex = /\{viewMode === 'europe' && europeData\.map\(\(country\) => \([\s\S]*?<\/CircleMarker>\s*\)\)\}/;
const newEuropeMapMarker = `{viewMode === 'europe' && europeData.map((country) => (
            <CircleMarker
              key={country.id}
              center={[country.lat, country.lng]}
              radius={15}
              pathOptions={{
                fillColor: country.color,
                color: country.color,
                weight: 2,
                fillOpacity: 0.6
              }}
            >
              <Popup className="custom-popup">
                <div className="p-1">
                  <h3 className="font-bold text-lg mb-2">{country.name}</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center border-b border-zinc-200 pb-2">
                      <span className="text-zinc-600 font-medium">Tracking Age:</span>
                      <DataTooltip 
                        titleIt="Età di Tracciamento" titleEn="Tracking Age"
                        descIt="L'età in cui gli studenti vengono divisi in percorsi scolastici separati (es. Liceo vs Professionale). Un'età più bassa correla con una maggiore disuguaglianza sociale." 
                        descEn="The age at which students are divided into separate tracks (e.g. Lyceum vs Vocational). A lower age correlates with higher social inequality."
                      >
                        <span className="font-bold text-indigo-600 cursor-help border-b border-dotted border-indigo-600">{country.trackAge}</span>
                      </DataTooltip>
                    </div>
                    <div className="flex justify-between items-center border-b border-zinc-200 pb-2">
                      <span className="text-zinc-600 font-medium">System Type:</span>
                      <span className="font-bold">{country.type}</span>
                    </div>
                    <div className="flex justify-between items-center border-b border-zinc-200 pb-2">
                      <span className="text-zinc-600 font-medium">NEET Rate:</span>
                      <DataTooltip 
                        titleIt="Tasso NEET" titleEn="NEET Rate"
                        descIt="Percentuale di giovani (15-29 anni) che non studiano, non lavorano e non sono in formazione." 
                        descEn="Percentage of youth (15-29 years old) Not in Education, Employment, or Training."
                      >
                        <span className="font-bold text-rose-600 cursor-help border-b border-dotted border-rose-600">{country.neet}</span>
                      </DataTooltip>
                    </div>
                    <div className="flex justify-between items-center border-b border-zinc-200 pb-2">
                      <span className="text-zinc-600 font-medium">Early Dropout:</span>
                      <span className="font-bold text-orange-600">{country.dropout}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-zinc-600 font-medium">Apprentice/PCTO:</span>
                      <span className="font-bold text-emerald-600">{country.pcto}</span>
                    </div>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          ))}`;

content = content.replace(oldEuropeMapMarkerRegex, newEuropeMapMarker);

fs.writeFileSync(file, content);
console.log('Injected european map data into GISMap.jsx');
