const fs = require('fs');

const file = 'frontend/src/components/SystemicDeepDives.jsx';
let content = fs.readFileSync(file, 'utf8');

// Ensure import for textbook fragmentation
if (!content.includes('import textbookFragmentation')) {
  content = content.replace(
    /import textbookOligopoly from '\.\.\/assets\/textbook_oligopoly\.json';/,
    "import textbookOligopoly from '../assets/textbook_oligopoly.json';\nimport textbookFragmentation from '../../public/data/textbook_fragmentation.json';"
  );
}

// Find the end of the textbook oligopoly grid
const insertionPoint = /<\/div>\n\n\s*\{\/\* Mechanism 2: Generational Lock-in \*\/\}/;

const fragmentationJSX = `
              {/* Textbook Fragmentation Data */}
              <div className="mt-8 bg-zinc-900/50 border border-zinc-800 rounded-3xl p-6">
                <div className="flex items-center gap-3 mb-6">
                  <BookOpen className="text-rose-400" size={24} />
                  <h4 className="text-xl font-bold text-white"><T it="Frammentazione del Mercato (42.560 Titoli Attivi)" en="Market Fragmentation (42,560 Active Titles)" /></h4>
                </div>
                
                <p className="text-zinc-400 mb-6 leading-relaxed">
                  <T it={textbookFragmentation.structuralIssue.it} en={textbookFragmentation.structuralIssue.en} />
                </p>

                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="border-b border-zinc-800">
                        <th className="py-3 px-4 text-sm font-bold text-zinc-500 uppercase tracking-wider"><T it="Materia (Esempio)" en="Subject (Example)" /></th>
                        <th className="py-3 px-4 text-sm font-bold text-zinc-500 uppercase tracking-wider text-right"><T it="Edizioni Attive in Commercio" en="Active Editions in Market" /></th>
                        <th className="py-3 px-4 text-sm font-bold text-zinc-500 uppercase tracking-wider text-right"><T it="Costo Medio" en="Average Cost" /></th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-zinc-800/50">
                      {textbookFragmentation.subjectFragmentation.map((item, idx) => (
                        <tr key={idx} className="hover:bg-white/[0.02] transition-colors">
                          <td className="py-3 px-4 font-medium text-zinc-300"><T it={item.subject.it} en={item.subject.en} /></td>
                          <td className="py-3 px-4 text-right text-rose-400 font-bold">{item.differentEditionsActive} <span className="text-zinc-500 text-xs font-normal">versioni</span></td>
                          <td className="py-3 px-4 text-right text-zinc-300">€{item.averageCost.toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

          {/* Mechanism 2: Generational Lock-in */}`;

content = content.replace(insertionPoint, fragmentationJSX);

fs.writeFileSync(file, content);
console.log('Injected textbook fragmentation into SystemicDeepDives.jsx');
