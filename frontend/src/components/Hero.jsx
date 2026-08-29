import React from 'react';
import { motion } from 'framer-motion';
import { Database, MousePointerClick, ExternalLink, ArrowRight, Home, GraduationCap, Briefcase, TrendingDown, Users, Brain, Euro } from 'lucide-react';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';

export default function Hero() {
  const { lang } = useLanguage();
  const isIt = lang === 'it';

  const phases = [
    {
      id: 'O',
      icon: Home,
      color: 'from-amber-500/20 to-amber-600/10',
      border: 'border-amber-500/30',
      iconColor: 'text-amber-400',
      label: isIt ? 'Origine' : 'Origin',
      sublabel: isIt ? 'Famiglia & Territorio' : 'Family & Territory',
      metrics: [
        { value: '€14k–€35k', desc: isIt ? 'Reddito familiare per indirizzo scolastico' : 'Family income by school track' },
        { value: '8.5', desc: isIt ? 'Indice di segregazione sociale' : 'Social segregation index' },
      ]
    },
    {
      id: 'E',
      icon: GraduationCap,
      color: 'from-indigo-500/20 to-indigo-600/10',
      border: 'border-indigo-500/30',
      iconColor: 'text-indigo-400',
      label: isIt ? 'Educazione' : 'Education',
      sublabel: isIt ? 'Sistema Tripartito' : 'Tripartite System',
      metrics: [
        { value: '14', desc: isIt ? 'Età del tracking (vs 16–18 UE)' : 'Tracking age (vs 16–18 EU)' },
        { value: '31%', desc: isIt ? 'Precarietà docenti (Professionali)' : 'Teacher precarity (Professionali)' },
      ]
    },
    {
      id: 'D',
      icon: Briefcase,
      color: 'from-rose-500/20 to-rose-600/10',
      border: 'border-rose-500/30',
      iconColor: 'text-rose-400',
      label: isIt ? 'Destinazione' : 'Destination',
      sublabel: isIt ? 'Mercato del Lavoro & Emigrazione' : 'Labor Market & Emigration',
      metrics: [
        { value: '22.3%', desc: isIt ? 'Disoccupazione giovanile' : 'Youth unemployment' },
        { value: '22%', desc: isIt ? 'Tasso NEET (Professionali)' : 'NEET rate (Professionali)' },
      ]
    }
  ];

  const downstream = [
    { icon: TrendingDown, label: isIt ? 'Fuga di cervelli' : 'Brain Drain', color: 'text-purple-400' },
    { icon: Euro, label: isIt ? 'Costi Fiscali' : 'Fiscal Costs', color: 'text-emerald-400' },
    { icon: Users, label: isIt ? 'Declino Demografico' : 'Demographic Decline', color: 'text-cyan-400' },
    { icon: Brain, label: isIt ? 'Capitale Umano Perso' : 'Lost Human Capital', color: 'text-amber-400' },
  ];

  return (
    <div className="text-center space-y-12 pt-8 pb-16 max-w-7xl mx-auto px-4 w-full">
      {/* TITLE */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="inline-flex items-center justify-center p-4 bg-indigo-500/10 rounded-full mb-4">
          <Database size={32} className="text-indigo-400" />
        </div>
        <h1 className="text-3xl sm:text-5xl md:text-7xl font-black text-white tracking-tight mb-4">
          Italienation
        </h1>
        <p className="text-zinc-400 text-base sm:text-lg md:text-xl max-w-3xl mx-auto font-light leading-relaxed">
          <T 
            it="Un osservatorio dati open-source che mappa il ciclo completo del capitale umano italiano — dall'origine socioeconomica, attraverso il sistema educativo, fino alla destinazione nel mercato del lavoro e oltre." 
            en="An open-source data observatory mapping the full cycle of Italian human capital — from socioeconomic origin, through the education system, to labor market destination and beyond." 
          />
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3 mt-6">
          <a 
            href="https://osf.io/fh7qr/" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700/50 hover:border-indigo-500/50 text-sm font-semibold text-zinc-300 hover:text-white transition-all shadow-lg group"
          >
            <svg viewBox="0 0 24 24" fill="none" className="w-4 h-4 text-indigo-400" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
              <path d="M2 12h20" />
            </svg>
            <span>OSF Open Science</span>
            <ExternalLink size={12} className="text-indigo-400 group-hover:translate-x-0.5 transition-transform" />
          </a>
          <a 
            href="https://github.com/Eugenix94/Italienation" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700/50 hover:border-indigo-500/50 text-sm font-semibold text-zinc-300 hover:text-white transition-all shadow-lg group"
          >
            <Database size={14} className="text-indigo-400" />
            <span>GitHub</span>
            <ExternalLink size={12} className="text-indigo-400 group-hover:translate-x-0.5 transition-transform" />
          </a>
        </div>
      </motion.div>

      {/* OED FRAMEWORK VISUAL */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.3 }}
        className="w-full"
      >
        {/* Section Label */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-800 text-zinc-400 border border-zinc-700/50 text-xs font-bold uppercase tracking-widest">
            <T it="Framework Analitico" en="Analytical Framework" />
          </div>
          <h2 className="text-2xl sm:text-3xl font-black text-white mt-4">
            <T it="Origine → Educazione → Destinazione" en="Origin → Education → Destination" />
          </h2>
          <p className="text-zinc-400 text-sm sm:text-base mt-2 max-w-2xl mx-auto">
            <T
              it="Il framework OED traccia come il background socioeconomico determini la traiettoria educativa e, di conseguenza, gli esiti occupazionali — creando un ciclo strutturale di disuguaglianza."
              en="The OED framework traces how socioeconomic background determines educational trajectory and, consequently, labor market outcomes — creating a structural cycle of inequality."
            />
          </p>
        </div>

        {/* OED Pipeline — 3 Cards with arrows */}
        <div className="flex flex-col lg:flex-row items-stretch gap-4 lg:gap-0 w-full">
          {phases.map((phase, i) => (
            <React.Fragment key={phase.id}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.5 + i * 0.2 }}
                className={`flex-1 bg-gradient-to-br ${phase.color} border ${phase.border} rounded-2xl p-6 relative`}
              >
                {/* Phase ID badge */}
                <div className="absolute -top-3 -left-1 sm:left-4">
                  <span className={`text-xs font-black px-2.5 py-0.5 rounded-full bg-zinc-900 border ${phase.border} ${phase.iconColor}`}>
                    {phase.id}
                  </span>
                </div>

                <div className="flex items-center gap-3 mb-4 mt-1">
                  <div className={`p-2.5 rounded-xl bg-zinc-900/60 ${phase.iconColor}`}>
                    <phase.icon size={22} />
                  </div>
                  <div className="text-left">
                    <div className="text-white font-bold text-lg leading-tight">{phase.label}</div>
                    <div className="text-zinc-400 text-xs">{phase.sublabel}</div>
                  </div>
                </div>

                <div className="space-y-3 mt-4">
                  {phase.metrics.map((m, j) => (
                    <div key={j} className="flex items-baseline gap-2">
                      <span className={`text-xl font-black ${phase.iconColor}`}>{m.value}</span>
                      <span className="text-xs text-zinc-400 leading-tight">{m.desc}</span>
                    </div>
                  ))}
                </div>
              </motion.div>

              {/* Arrow between cards */}
              {i < phases.length - 1 && (
                <div className="flex items-center justify-center lg:px-2 py-2 lg:py-0">
                  <ArrowRight size={20} className="text-zinc-600 rotate-90 lg:rotate-0" />
                </div>
              )}
            </React.Fragment>
          ))}
        </div>

        {/* DOWNSTREAM EFFECTS — what these three phases produce */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.2 }}
          className="mt-8"
        >
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-px h-8 bg-zinc-700" />
          </div>
          <p className="text-xs text-zinc-500 uppercase tracking-widest font-bold mb-4">
            <T it="Effetti sistemici a valle" en="Downstream systemic effects" />
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            {downstream.map((d, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 1.4 + i * 0.1 }}
                className="flex items-center gap-2 px-4 py-2 bg-zinc-900/60 border border-zinc-800 rounded-xl"
              >
                <d.icon size={14} className={d.color} />
                <span className="text-sm text-zinc-300 font-medium">{d.label}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </motion.div>

      {/* Scroll CTA */}
      <motion.div 
        className="pt-8 text-zinc-400 flex flex-col items-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.8, duration: 1 }}
      >
        <div className="animate-bounce flex flex-col items-center">
          <MousePointerClick size={24} className="mb-2" />
          <span className="text-sm uppercase tracking-widest"><T it="Scorri per esplorare i dati" en="Scroll to explore the data" /></span>
        </div>
      </motion.div>
    </div>
  );
}
