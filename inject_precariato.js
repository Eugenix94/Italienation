const fs = require('fs');

const file = 'frontend/src/components/LaborMarketAndCorrelations.jsx';
let content = fs.readFileSync(file, 'utf8');

if (!content.includes('import precariatoData')) {
  content = content.replace(
    /import \{ T \} from '\.\/T';/,
    "import { T } from './T';\nimport precariatoData from '../../public/data/precariato_docenti.json';"
  );
}

// ensure lucide-react has BookDashed
if (!content.includes('BookDashed')) {
  content = content.replace(
    /from 'lucide-react';/,
    ", BookDashed } from 'lucide-react';"
  );
}


const insertionPoint = /\{\/\* Correlations Card - Full Width \*\/\}/;

const precariatoJSX = `
        {/* Il Precariato Card - Full Width */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.25 }}
          className="bg-zinc-900/50 border border-white/10 backdrop-blur-md rounded-3xl p-8 hover:border-indigo-500/30 transition-colors mb-8"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 bg-amber-500/20 rounded-xl">
              <BookDashed className="text-amber-400" size={24} />
            </div>
            <div>
              <h3 className="text-xl font-bold"><T it="Il Precariato Docenti" en="Teacher Precarity" /></h3>
              <p className="text-sm text-zinc-400"><T it="L'impatto della discontinuità didattica sugli studenti" en="The impact of pedagogical discontinuity on students" /></p>
            </div>
          </div>
          <p className="text-sm text-zinc-300 mb-8 max-w-4xl leading-relaxed">
            <T it={precariatoData.structuralIssue.it} en={precariatoData.structuralIssue.en} />
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
            <div className="bg-zinc-950 p-5 rounded-2xl border border-zinc-800">
              <p className="text-xs text-zinc-500 uppercase font-bold mb-2"><T it="Docenti Precari" en="Precarious Teachers" /></p>
              <div className="flex items-end gap-2">
                <p className="text-3xl font-black text-amber-400">{(precariatoData.precariousTeachers / 1000)}K</p>
                <p className="text-sm font-bold text-amber-400/50 mb-1">({precariatoData.precariousPercentage}%)</p>
              </div>
            </div>
            <div className="bg-zinc-950 p-5 rounded-2xl border border-zinc-800 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-16 h-16 bg-emerald-500/10 blur-xl" />
              <p className="text-xs text-zinc-500 uppercase font-bold mb-2"><T it="Media Europea" en="EU Average" /></p>
              <div className="flex items-end gap-2">
                <p className="text-3xl font-black text-emerald-400">{precariatoData.euPrecariousPercentage}%</p>
              </div>
            </div>
            <div className="bg-zinc-950 p-5 rounded-2xl border border-zinc-800">
              <p className="text-xs text-zinc-500 uppercase font-bold mb-2"><T it="Età Media" en="Average Age" /></p>
              <div className="flex items-end gap-2">
                <p className="text-3xl font-black text-rose-400">{precariatoData.averageAge}</p>
                <p className="text-sm font-bold text-rose-400/50 mb-1">anni</p>
              </div>
            </div>
            <div className="bg-zinc-950 p-5 rounded-2xl border border-zinc-800 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-16 h-16 bg-emerald-500/10 blur-xl" />
              <p className="text-xs text-zinc-500 uppercase font-bold mb-2"><T it="Età Media EU" en="EU Average Age" /></p>
              <div className="flex items-end gap-2">
                <p className="text-3xl font-black text-emerald-400">{precariatoData.euAverageAge}</p>
                <p className="text-sm font-bold text-emerald-400/50 mb-1">anni</p>
              </div>
            </div>
          </div>
          
          <div className="bg-amber-950/20 border border-amber-900/30 rounded-xl p-4 flex items-center justify-between">
            <span className="text-amber-200 font-medium text-sm"><T it="Anni di continuità didattica media per studente (Stima):" en="Average years of teaching continuity per student (Est):" /></span>
            <span className="text-xl font-black text-amber-400">{precariatoData.averageContinuityYears} <span className="text-sm font-normal text-amber-400/60">anni / years</span></span>
          </div>

        </motion.div>

        {/* Correlations Card - Full Width */}`;

if (!content.includes('Il Precariato Docenti')) {
  content = content.replace(insertionPoint, precariatoJSX);
  fs.writeFileSync(file, content);
  console.log('Injected precariato into LaborMarketAndCorrelations.jsx');
} else {
  console.log('Already injected');
}
