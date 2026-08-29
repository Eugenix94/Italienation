import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Info, HelpCircle } from 'lucide-react';
import { T } from './T';

export default function DataTooltip({ 
  children, 
  titleIt, titleEn, 
  descIt, descEn, 
  source, formulaIt, formulaEn,
  position = 'top' // 'top' or 'bottom'
}) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div 
      className="relative inline-flex items-center gap-1 group cursor-help"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      onClick={() => setIsVisible(!isVisible)}
    >
      <span className="border-b border-dashed border-zinc-500/50 hover:border-indigo-400/50 transition-colors">
        {children}
      </span>
      <HelpCircle className="w-3.5 h-3.5 text-zinc-400 group-hover:text-indigo-400 transition-colors" />

      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, y: position === 'top' ? 5 : -5, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: position === 'top' ? 5 : -5, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className={`absolute z-50 w-64 md:w-80 p-4 bg-zinc-900 border border-zinc-700/80 shadow-2xl rounded-xl backdrop-blur-xl ${
              position === 'top' 
                ? 'bottom-full mb-2 left-1/2 -translate-x-1/2' 
                : 'top-full mt-2 left-1/2 -translate-x-1/2'
            }`}
            onClick={(e) => e.stopPropagation()}
          >
            {titleIt && (
              <h4 className="text-sm font-bold text-white mb-2 pb-2 border-b border-zinc-800/80">
                <T it={titleIt} en={titleEn} />
              </h4>
            )}
            
            <p className="text-xs text-zinc-300 mb-3 leading-relaxed">
              <T it={descIt} en={descEn} />
            </p>

            {formulaIt && (
              <div className="bg-zinc-950 rounded-md p-2 mb-3 border border-zinc-800 font-mono text-[10px] text-zinc-400">
                <span className="text-indigo-400 mr-1 block mb-1">Methodology / Formula:</span>
                <T it={formulaIt} en={formulaEn} />
              </div>
            )}

            {source && (
              <div className="flex items-center gap-1.5 text-[10px] text-zinc-400 font-medium">
                <Info className="w-3 h-3" />
                <span>Source: {source}</span>
              </div>
            )}
            
            {/* Caret */}
            <div className={`absolute w-3 h-3 bg-zinc-900 border-zinc-700/80 rotate-45 left-1/2 -translate-x-1/2 ${
              position === 'top' 
                ? '-bottom-1.5 border-b border-r' 
                : '-top-1.5 border-t border-l'
            }`} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
