import React from 'react';
import { motion } from 'framer-motion';
import { BookOpen, CheckCircle } from 'lucide-react';
import { T } from './T';

export default function SectionContext({ 
  domainIt, domainEn,
  titleIt, titleEn,
  thesisIt, thesisEn,
  takeaways = []
}) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="mb-12 w-full"
    >
      <div className="bg-gradient-to-br from-indigo-900/20 via-zinc-900/50 to-zinc-950/80 border border-indigo-500/20 rounded-3xl p-6 md:p-8 lg:p-10 shadow-2xl relative overflow-hidden">
        {/* Subtle background element */}
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-[80px] pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row gap-8 lg:gap-12">
          {/* Left Side: Thesis */}
          <div className="flex-1">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-6">
              <BookOpen size={14} />
              <T it={domainIt} en={domainEn} />
            </div>
            
            <h2 className="text-3xl md:text-4xl font-black text-white mb-6 leading-tight tracking-tight">
              <T it={titleIt} en={titleEn} />
            </h2>
            
            <p className="text-lg text-zinc-300 leading-relaxed font-medium">
              <T it={thesisIt} en={thesisEn} />
            </p>
          </div>

          {/* Right Side: Key Takeaways */}
          <div className="md:w-5/12 lg:w-1/3 shrink-0">
            <div className="bg-white/[0.03] border border-white/5 rounded-2xl p-6 h-full backdrop-blur-sm">
              <h4 className="text-xs font-black uppercase tracking-widest text-zinc-500 mb-5">
                <T it="Concetti Chiave" en="Key Takeaways" />
              </h4>
              <ul className="space-y-4">
                {takeaways.map((takeaway, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
                    <span className="text-sm text-zinc-300 leading-relaxed">
                      <T it={takeaway.it} en={takeaway.en} />
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
