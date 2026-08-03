const fs = require('fs');

const file = 'frontend/src/components/TerritorialMap.jsx';
let content = fs.readFileSync(file, 'utf8');

if (!content.includes('import ediliziaData')) {
  content = content.replace(
    /import \{ T \} from '\.\/T';/,
    "import { T } from './T';\nimport ediliziaData from '../../public/data/edilizia_scolastica.json';"
  );
}

const insertionPoint = /\{\/\* Instructions or empty state \*\/\}/;

const ediliziaJSX = `
            {/* Edilizia Scolastica Panel */}
            <div className="mt-8 pt-6 border-t border-zinc-800">
              <div className="flex items-center gap-2 mb-4">
                <AlertTriangle className="text-amber-500" size={20} />
                <h3 className="text-lg font-bold text-white"><T it="Edilizia Scolastica (Mense)" en="School Infrastructure (Cafeterias)" /></h3>
              </div>
              <p className="text-sm text-zinc-400 mb-4 leading-relaxed">
                <T it={ediliziaData.structuralIssue.it} en={ediliziaData.structuralIssue.en} />
              </p>
              
              <div className="space-y-4">
                {ediliziaData.territorialDivide.map((area, idx) => (
                  <div key={idx} className="bg-zinc-950 p-3 rounded-lg border border-zinc-800/50">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-bold text-zinc-300">{area.macroArea}</span>
                      <span className="text-xs text-rose-400 font-semibold">{area.withoutCafeteria}% <T it="Senza Mensa" en="Without Cafeteria" /></span>
                    </div>
                    <div className="w-full bg-zinc-800 rounded-full h-2">
                      <div className="bg-rose-500 h-2 rounded-full" style={{ width: \`\${area.withoutCafeteria}%\` }}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Instructions or empty state */}`;

if (!content.includes('Edilizia Scolastica (Mense)')) {
  content = content.replace(insertionPoint, ediliziaJSX);
  fs.writeFileSync(file, content);
  console.log('Injected edilizia into TerritorialMap.jsx');
} else {
  console.log('Already injected');
}
