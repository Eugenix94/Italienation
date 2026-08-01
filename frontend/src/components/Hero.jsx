import React from 'react';
import { motion } from 'framer-motion';
import { Database, MousePointerClick } from 'lucide-react';
import { T } from './T';

export default function Hero() {
  return (
    <div className="text-center space-y-6 pt-12 pb-24 max-w-7xl mx-auto px-4 w-full">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="inline-flex items-center justify-center p-4 bg-indigo-500/10 rounded-full mb-4">
          <Database size={32} className="text-indigo-400" />
        </div>
        <h1 className="text-3xl sm:text-5xl md:text-7xl font-black text-white tracking-tight mb-6">
          <T it="Osservatorio Dati Universale" en="Universal Data Observatory" />
        </h1>
        <p className="text-zinc-400 text-base sm:text-xl md:text-2xl max-w-3xl mx-auto font-light leading-relaxed">
          <T 
            it="Esplorazione interattiva e neutrale delle metriche strutturali del sistema educativo italiano, basata su 681 dataset istituzionali verificati." 
            en="Interactive and neutral exploration of structural metrics within the Italian educational system, based on 681 verified institutional datasets." 
          />
        </p>
      </motion.div>
      <motion.div 
        className="pt-16 text-zinc-500 flex flex-col items-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 1 }}
      >
        <div className="animate-bounce flex flex-col items-center">
          <MousePointerClick size={24} className="mb-2" />
          <span className="text-sm uppercase tracking-widest"><T it="Scorri per esplorare" en="Scroll to explore" /></span>
        </div>
      </motion.div>
    </div>
  );
}
