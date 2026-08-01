import React from 'react';
import { motion } from 'framer-motion';
import { Database, ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';
import { T } from './T';

export default function DataCatalogCTA() {
  return (
    <motion.div 
      className="text-center space-y-6 pb-24 pt-12 max-w-7xl mx-auto px-4 w-full"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6 }}
    >
      <Database size={48} className="mx-auto text-indigo-500 mb-6 opacity-50" />
      <h2 className="text-4xl font-bold text-white">
        <T it="I Dati Sono Pubblici" en="The Data is Public" />
      </h2>
      <p className="text-zinc-400 text-xl max-w-2xl mx-auto">
        <T 
          it="Tutti i 681 dataset, i metadati e i notebook Jupyter utilizzati per generare queste metriche sono disponibili in open-source." 
          en="All 681 datasets, metadata, and Jupyter notebooks used to generate these metrics are available open-source." 
        />
      </p>
      <div className="pt-8 flex flex-col sm:flex-row gap-4 justify-center items-center">
        <a 
          href="https://github.com/Eugenix94/Italienation/releases"
          target="_blank" rel="noopener noreferrer"
          className="inline-block bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-4 px-8 rounded-xl transition-all shadow-lg shadow-indigo-500/20"
        >
          <T it="Accedi al Catalogo Completo (ZIP)" en="Access Full Data Catalog (ZIP)" />
        </a>
        <a 
          href="https://github.com/Eugenix94/Italienation"
          target="_blank" rel="noopener noreferrer"
          className="inline-flex items-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-white font-bold py-4 px-8 rounded-xl transition-all border border-zinc-700"
        >
          <ExternalLink size={20} />
          <T it="Repository GitHub" en="GitHub Repository" />
        </a>
      </div>
    </motion.div>
  );
}
