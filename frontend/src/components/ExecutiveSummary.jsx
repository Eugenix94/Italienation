import React from 'react';
import { motion } from 'framer-motion';
import { T } from './T';
import { TrendingDown, Percent, Users, Scale, Activity, GraduationCap, ArrowDown } from 'lucide-react';

const stats = [
  {
    icon: TrendingDown,
    value: '€292.5B',
    labelIt: 'Costo Sistemico Annuo',
    labelEn: 'Annual Systemic Cost',
    subIt: '~14.6% del PIL italiano sprecato',
    subEn: '~14.6% of Italian GDP wasted',
    color: 'text-rose-400',
    border: 'border-rose-500/30',
    bg: 'bg-rose-500/10'
  },
  {
    icon: Percent,
    value: '45.1%',
    labelIt: 'Cuneo Fiscale sul Lavoro',
    labelEn: 'Labor Tax Wedge',
    subIt: '3° più elevato nell\'OCSE',
    subEn: '3rd highest in the OECD',
    color: 'text-amber-400',
    border: 'border-amber-500/30',
    bg: 'bg-amber-500/10'
  },
  {
    icon: Users,
    value: '1.35',
    labelIt: 'Attivi per Pensionato',
    labelEn: 'Workers per Retiree',
    subIt: 'Sotto la soglia critica di 1.50',
    subEn: 'Below critical threshold of 1.50',
    color: 'text-red-400',
    border: 'border-red-500/30',
    bg: 'bg-red-500/10'
  },
  {
    icon: Scale,
    value: '540 gg',
    labelIt: 'Durata Processo Civile',
    labelEn: 'Civil Trial Duration',
    subIt: 'Quasi il doppio della media UE (280)',
    subEn: 'Almost double EU average (280)',
    color: 'text-orange-400',
    border: 'border-orange-500/30',
    bg: 'bg-orange-500/10'
  },
  {
    icon: Activity,
    value: '21.4%',
    labelIt: 'Spesa Sanitaria Out-of-Pocket',
    labelEn: 'Out-of-Pocket Health Cost',
    subIt: 'Spesa privata (vs 9.3% Francia)',
    subEn: 'Private spending (vs 9.3% France)',
    color: 'text-cyan-400',
    border: 'border-cyan-500/30',
    bg: 'bg-cyan-500/10'
  },
  {
    icon: GraduationCap,
    value: '25.0%',
    labelIt: 'Tasso di Sovraistruzione',
    labelEn: 'Overeducation Rate',
    subIt: 'Laureati in mansioni dequalificate',
    subEn: 'Graduates in low-skill jobs',
    color: 'text-indigo-400',
    border: 'border-indigo-500/30',
    bg: 'bg-indigo-500/10'
  }
];

export default function ExecutiveSummary({ onExploreClick }) {
  return (
    <motion.section 
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="w-full max-w-6xl mx-auto px-4 sm:px-6 mb-16"
    >
      <div className="bg-zinc-900/60 border border-white/10 rounded-3xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl relative overflow-hidden">
        {/* Glow ambient */}
        <div className="absolute top-0 right-1/4 w-96 h-32 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-1/4 w-96 h-32 bg-rose-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/5 pb-6 mb-6">
          <div>
            <span className="text-xs font-black tracking-widest text-indigo-400 uppercase">
              <T it="Sintesi Esecutiva in 60 Secondi" en="Executive Summary in 60 Seconds" />
            </span>
            <h2 className="text-2xl sm:text-3xl font-black text-white mt-1">
              <T it="L'Anatomia del Declino Strutturale Italiano" en="The Anatomy of Italy's Structural Decline" />
            </h2>
          </div>
          <button
            onClick={onExploreClick}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600/80 hover:bg-indigo-600 text-white text-sm font-semibold transition shadow-lg shadow-indigo-600/20 border border-indigo-400/30 self-start md:self-auto cursor-pointer"
          >
            <span><T it="Inizia l'Indagine Completa" en="Start Full Investigation" /></span>
            <ArrowDown size={16} />
          </button>
        </div>

        {/* 6 Key Indicators Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
          {stats.map((stat, idx) => {
            const Icon = stat.icon;
            return (
              <div 
                key={idx}
                className="bg-black/30 border border-white/5 hover:border-white/15 p-3.5 sm:p-4 rounded-2xl transition flex flex-col justify-between"
              >
                <div>
                  <div className={`w-8 h-8 rounded-lg ${stat.bg} ${stat.border} border flex items-center justify-center mb-3`}>
                    <Icon size={16} className={stat.color} />
                  </div>
                  <div className={`text-xl sm:text-2xl font-black ${stat.color} tracking-tight font-mono`}>
                    {stat.value}
                  </div>
                </div>
                <div className="mt-2 pt-2 border-t border-white/5">
                  <p className="text-xs font-bold text-zinc-200 leading-snug">
                    <T it={stat.labelIt} en={stat.labelEn} />
                  </p>
                  <p className="text-[10px] text-zinc-400 mt-0.5 leading-tight">
                    <T it={stat.subIt} en={stat.subEn} />
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </motion.section>
  );
}
