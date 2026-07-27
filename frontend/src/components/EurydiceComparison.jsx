import React from 'react';
import { Globe, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';
import { T } from './T';

export default function EurydiceComparison() {
  return (
    <div className="w-full relative space-y-8 bg-white/[0.02] backdrop-blur-xl p-8 sm:p-12 rounded-3xl border border-white/10 shadow-2xl overflow-hidden group hover:border-white/20 transition-all">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
      
      <div className="text-center mb-12 relative z-10">
        <h2 className="text-3xl md:text-5xl font-black tracking-tight mb-4 text-white">
          <T it="Il Contesto Internazionale" en="The International Context" />
        </h2>
        <p className="text-xl text-gray-400 max-w-3xl mx-auto">
          <T 
            it="Confronto tra il modello rigido Tripartito italiano e i sistemi Comprensivi del Nord Europa basato sui benchmark OCSE ed Eurydice." 
            en="Comparing Italy's rigid Tripartite model with the Comprehensive systems of Northern Europe using OECD and Eurydice benchmarks." 
          />
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12 relative z-10">
        {/* Tripartite Model */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-white/5 border border-red-500/30 p-8 rounded-2xl backdrop-blur-sm"
        >
          <div className="flex items-center mb-4">
            <AlertTriangle className="w-8 h-8 text-red-400 mr-3" />
            <h3 className="text-2xl font-bold text-white">
              <T it="Il Sistema Tripartito (Italia, Germania)" en="The Tripartite System (Italy, Germany)" />
            </h3>
          </div>
          <p className="text-gray-300 mb-6">
            <T 
              it="Smista gli studenti a 10-14 anni in percorsi accademici, tecnici o professionali distinti. Risultato: Alta correlazione tra reddito familiare e indirizzo. Rigida segregazione sociale." 
              en="Tracks students at age 10-14 into distinct academic, technical, or vocational pathways. Result: High correlation between family income and track placement. Rigid social segregation." 
            />
          </p>
          <ul className="space-y-3">
            <li className="flex items-center text-sm text-gray-400">
              <span className="w-2 h-2 rounded-full bg-red-500 mr-2"></span>
              <T it="Età di Smistamento: 10-14 anni" en="Tracking Age: 10-14 years old" />
            </li>
            <li className="flex items-center text-sm text-gray-400">
              <span className="w-2 h-2 rounded-full bg-red-500 mr-2"></span>
              <T it="Segregazione di Classe: Grave" en="Class Segregation: Severe" />
            </li>
            <li className="flex items-center text-sm text-gray-400">
              <span className="w-2 h-2 rounded-full bg-red-500 mr-2"></span>
              <T it="Rischio NEET: Alto (19%+)" en="NEET Risk: High (19%+)" />
            </li>
          </ul>
        </motion.div>

        {/* Comprehensive Model */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
          className="bg-white/5 border border-indigo-500/30 p-8 rounded-2xl backdrop-blur-sm"
        >
          <div className="flex items-center mb-4">
            <Globe className="w-8 h-8 text-indigo-400 mr-3" />
            <h3 className="text-2xl font-bold text-white">
              <T it="Il Sistema Comprensivo (Nordici, Canada)" en="The Comprehensive System (Nordics, Canada)" />
            </h3>
          </div>
          <p className="text-gray-300 mb-6">
            <T 
              it="Mantiene tutti gli studenti in un curriculum unificato fino a 16-18 anni. Risultato: Riduce drasticamente l'impatto dell'origine socioeconomica sulla destinazione finale." 
              en="Keeps all students in a unified curriculum until age 16-18. Result: Drastically reduces the impact of socioeconomic origin on final educational destination." 
            />
          </p>
          <ul className="space-y-3">
            <li className="flex items-center text-sm text-gray-400">
              <span className="w-2 h-2 rounded-full bg-indigo-500 mr-2"></span>
              <T it="Età di Smistamento: 16+ anni" en="Tracking Age: 16+ years old" />
            </li>
            <li className="flex items-center text-sm text-gray-400">
              <span className="w-2 h-2 rounded-full bg-indigo-500 mr-2"></span>
              <T it="Segregazione di Classe: Bassa" en="Class Segregation: Low" />
            </li>
            <li className="flex items-center text-sm text-gray-400">
              <span className="w-2 h-2 rounded-full bg-indigo-500 mr-2"></span>
              <T it="Rischio NEET: Basso (Sotto l'8%)" en="NEET Risk: Low (Under 8%)" />
            </li>
          </ul>
        </motion.div>
      </div>
      
      <div className="text-center relative z-10">
        <p className="text-sm text-gray-500 italic">
          <T 
            it="Dati derivati dalla Rete Eurydice (Commissione Europea) e dai Rapporti OCSE PISA." 
            en="Data derived from the Eurydice Network (European Commission) and OECD PISA Reports." 
          />
        </p>
      </div>
    </div>
  );
}
