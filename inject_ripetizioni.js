const fs = require('fs');

const file = 'frontend/src/components/SystemicDeepDives.jsx';
let content = fs.readFileSync(file, 'utf8');

// Ensure import for ripetizioni_market
if (!content.includes('import ripetizioniMarket')) {
  content = content.replace(
    /import textbookFragmentation from '\.\.\/\.\.\/public\/data\/textbook_fragmentation\.json';/,
    "import textbookFragmentation from '../../public/data/textbook_fragmentation.json';\nimport ripetizioniMarket from '../../public/data/ripetizioni_market.json';"
  );
}

// Find the end of the Generational Lock-in grid and add the new section before it closes the <motion.section>
const insertionPoint = /\{\/\* Mechanism 2: Generational Lock-in \*\/\}/;

const ripetizioniJSX = `
              {/* Ripetizioni Black Market Data */}
              <div className="mt-8 bg-zinc-900/50 border border-zinc-800 rounded-3xl p-6">
                <div className="flex items-center gap-3 mb-6">
                  <Euro className="text-rose-400" size={24} />
                  <h4 className="text-xl font-bold text-white"><T it="Il Mercato Nero delle Ripetizioni" en="The Private Tutoring Black Market" /></h4>
                </div>
                
                <p className="text-zinc-400 mb-6 leading-relaxed">
                  <T it={ripetizioniMarket.structuralIssue.it} en={ripetizioniMarket.structuralIssue.en} />
                </p>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-zinc-950 p-4 rounded-xl border border-zinc-800">
                    <p className="text-xs text-zinc-500 uppercase font-bold mb-1"><T it="Valore Mercato" en="Market Value" /></p>
                    <p className="text-2xl font-black text-rose-400">€{(ripetizioniMarket.totalMarketValue / 1000000)}M</p>
                  </div>
                  <div className="bg-zinc-950 p-4 rounded-xl border border-zinc-800">
                    <p className="text-xs text-zinc-500 uppercase font-bold mb-1"><T it="Tasso Evasione" en="Evasion Rate" /></p>
                    <p className="text-2xl font-black text-rose-400">{ripetizioniMarket.blackMarketPercentage}%</p>
                  </div>
                  <div className="bg-zinc-950 p-4 rounded-xl border border-zinc-800">
                    <p className="text-xs text-zinc-500 uppercase font-bold mb-1"><T it="Studenti Coinvolti" en="Students Involved" /></p>
                    <p className="text-2xl font-black text-rose-400">{(ripetizioniMarket.studentsTakingTutoring / 1000000).toFixed(1)}M</p>
                  </div>
                  <div className="bg-zinc-950 p-4 rounded-xl border border-zinc-800">
                    <p className="text-xs text-zinc-500 uppercase font-bold mb-1"><T it="Costo Medio/Ora" en="Avg Hourly Rate" /></p>
                    <p className="text-2xl font-black text-rose-400">€{ripetizioniMarket.averageHourlyRate}</p>
                  </div>
                </div>
              </div>
            </div>

          {/* Mechanism 2: Generational Lock-in */}`;

if (!content.includes('Il Mercato Nero delle Ripetizioni')) {
  content = content.replace(insertionPoint, ripetizioniJSX);
  fs.writeFileSync(file, content);
  console.log('Injected ripetizioni into SystemicDeepDives.jsx');
} else {
  console.log('Already injected');
}
