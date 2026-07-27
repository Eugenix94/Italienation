import React, { useState, useEffect } from 'react';
import { T } from '../components/T';
import { Search, Database, ExternalLink, Download } from 'lucide-react';
import { motion } from 'framer-motion';
import catalogData from '../assets/catalog.json';

export default function DataCatalog() {
  const [searchTerm, setSearchTerm] = useState('');
  const [items, setItems] = useState([]);

  useEffect(() => {
    // catalogData is an array of categories containing datasets
    // We flatten it for easy searching, or render by category.
    // Assuming structure based on previous commits:
    // [ { category: 'MIM', description: '...', links: [ { title, url, origin, raw_link } ] } ]
    if (Array.isArray(catalogData)) {
      setItems(catalogData);
    }
  }, []);

  const filteredItems = items.map(cat => ({
    ...cat,
    links: cat.links?.filter(link => 
      link.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
      (link.origin && link.origin.toLowerCase().includes(searchTerm.toLowerCase()))
    ) || []
  })).filter(cat => cat.links.length > 0);

  return (
    <div className="max-w-6xl mx-auto px-4 py-12 space-y-8">
      <div className="space-y-4">
        <div className="flex items-center gap-3 text-indigo-400">
          <Database size={32} />
          <h1 className="text-3xl font-black text-white">
            <T it="Directory Dati" en="Data Directory" />
          </h1>
        </div>
        <p className="text-zinc-400 max-w-3xl text-lg">
          <T 
            it="L'intero archivio di 681+ dataset ufficiali utilizzati in questo progetto. Tutti i link puntano direttamente alle fonti istituzionali primarie o al mirror rielaborato." 
            en="The complete archive of 681+ official datasets used in this project. All links point directly to the primary institutional sources or the processed mirror." 
          />
        </p>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500" size={20} />
        <input 
          type="text" 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Cerca dataset, fonte (es. ISTAT, MIM)... / Search datasets..."
          className="w-full pl-12 pr-4 py-4 bg-zinc-900/50 border border-zinc-800 rounded-2xl text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
        />
      </div>

      {/* Catalog Grid */}
      <div className="space-y-12">
        {filteredItems.map((category, idx) => (
          <div key={idx} className="space-y-6">
            <div className="border-b border-zinc-800 pb-2">
              <h2 className="text-xl font-bold text-zinc-200 flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-indigo-500"></div>
                {category.category}
              </h2>
              {category.description && (
                <p className="text-sm text-zinc-500 mt-1">{category.description}</p>
              )}
            </div>
            
            <motion.div 
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-50px" }}
              variants={{
                hidden: {},
                visible: {
                  transition: { staggerChildren: 0.05 }
                }
              }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
            >
              {category.links.map((link, lidx) => (
                <motion.div 
                  key={lidx} 
                  variants={{
                    hidden: { opacity: 0, y: 10 },
                    visible: { opacity: 1, y: 0 }
                  }}
                  transition={{ duration: 0.4 }}
                  className="bg-white/[0.02] backdrop-blur-md border border-white/5 rounded-xl p-5 hover:bg-white/[0.04] hover:border-indigo-500/30 transition-all flex flex-col justify-between group shadow-lg"
                >
                  <div className="space-y-3">
                    <div className="flex items-start justify-between gap-4">
                      <h3 className="font-medium text-sm text-zinc-300 group-hover:text-white leading-snug">
                        {link.title}
                      </h3>
                    </div>
                    {link.origin && (
                      <span className="inline-flex px-2 py-1 rounded-md bg-zinc-800 text-[10px] font-bold text-zinc-400 tracking-wider">
                        {link.origin}
                      </span>
                    )}
                  </div>
                  <div className="mt-6 flex items-center gap-3">
                    {link.raw_link && (
                      <a href={link.raw_link} target="_blank" rel="noopener noreferrer" className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-xs font-medium text-zinc-300 transition-colors">
                        <Download size={14} />
                        Raw Data
                      </a>
                    )}
                    {link.url && (
                      <a href={link.url} target="_blank" rel="noopener noreferrer" className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg bg-indigo-600/10 hover:bg-indigo-600/20 text-indigo-400 text-xs font-medium transition-colors border border-indigo-500/20">
                        <ExternalLink size={14} />
                        Source
                      </a>
                    )}
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </div>
        ))}
        {filteredItems.length === 0 && (
          <div className="text-center py-20 text-zinc-500">
            <Database size={48} className="mx-auto mb-4 opacity-20" />
            <T it="Nessun dataset trovato per questa ricerca." en="No datasets found for this search." />
          </div>
        )}
      </div>
    </div>
  );
}
