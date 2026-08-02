import React, { useState, useEffect } from 'react';
import { T } from './T';
import { Search, Library, BookOpen, Hash, Tag, Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function DataLexicon() {
  const [lexicon, setLexicon] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/glossary.json`)
      .then(res => res.json())
      .then(data => {
        setLexicon(data.glossary);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load glossary:", err);
        setLoading(false);
      });
  }, []);

  const filteredLexicon = lexicon.filter(item => {
    if (!searchTerm) return true;
    const searchLower = searchTerm.toLowerCase();
    const matchIt = item.term.it.toLowerCase().includes(searchLower) || item.definition.it.toLowerCase().includes(searchLower);
    const matchEn = item.term.en.toLowerCase().includes(searchLower) || item.definition.en.toLowerCase().includes(searchLower);
    const matchAcronym = item.acronym ? item.acronym.toLowerCase().includes(searchLower) : false;
    return matchIt || matchEn || matchAcronym;
  });

  if (loading) {
    return (
      <div className="flex justify-center items-center h-[500px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="w-full">
      {/* Header Section */}
      <div className="mb-12 max-w-4xl">
        <h2 className="text-3xl font-black text-white mb-4 flex items-center gap-3">
          <Library className="text-indigo-400" size={32} />
          <T it="Glossario & Lessico Dati" en="Data Lexicon & Glossary" />
        </h2>
        <p className="text-zinc-400 text-lg">
          <T 
            it="Un dizionario centralizzato per decodificare il gergo istituzionale, gli acronimi e le metriche utilizzate in questo osservatorio. Cerca un termine per comprenderne il significato nel contesto del sistema educativo italiano."
            en="A centralized dictionary to decode the institutional jargon, acronyms, and metrics used in this observatory. Search for a term to understand its meaning within the context of the Italian educational system."
          />
        </p>
      </div>

      {/* Search Bar */}
      <div className="mb-12 relative max-w-2xl">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search className="text-zinc-500" size={20} />
        </div>
        <input
          type="text"
          className="block w-full pl-12 pr-4 py-4 bg-zinc-900/50 border border-zinc-800 rounded-2xl leading-5 bg-transparent placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-lg text-white transition-all shadow-inner"
          placeholder="Cerca acronimo o termine (es. ESCS, INVALSI, Bocciatura)..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Masonry / Grid of Terms */}
      {filteredLexicon.length === 0 ? (
        <div className="text-center py-20 bg-zinc-900/20 rounded-2xl border border-zinc-800 border-dashed">
          <Search className="mx-auto text-zinc-600 mb-4" size={48} />
          <p className="text-xl font-bold text-zinc-400">
            <T it="Nessun termine trovato." en="No terms found." />
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <AnimatePresence>
            {filteredLexicon.map((item, idx) => (
              <motion.div
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.2, delay: idx * 0.05 }}
                key={item.id}
                className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-6 hover:border-indigo-500/50 transition-colors group flex flex-col h-full shadow-lg hover:shadow-indigo-500/10"
              >
                <div className="flex justify-between items-start mb-4 gap-4">
                  <div>
                    {item.acronym && (
                      <span className="inline-block px-2 py-1 bg-indigo-500/10 text-indigo-400 text-xs font-black tracking-widest rounded-md mb-2 border border-indigo-500/20">
                        {item.acronym}
                      </span>
                    )}
                    <h3 className="text-xl font-bold text-white leading-tight">
                      <T it={item.term.it} en={item.term.en} />
                    </h3>
                  </div>
                  <div className="shrink-0">
                    <BookOpen className="text-zinc-700 group-hover:text-indigo-400 transition-colors" size={24} />
                  </div>
                </div>
                
                <div className="flex-grow">
                  <p className="text-zinc-400 text-sm leading-relaxed">
                    <T it={item.definition.it} en={item.definition.en} />
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-zinc-800/50 flex items-center gap-2">
                  <Tag size={14} className="text-zinc-600" />
                  <span className="text-xs uppercase tracking-wider font-bold text-zinc-500">
                    {item.category}
                  </span>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
