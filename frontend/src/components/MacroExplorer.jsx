import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { T } from './T';
import { 
  BarChart3, 
  Receipt, 
  UserMinus, 
  Activity, 
  Scale, 
  Zap, 
  Construction, 
  Layers,
  TrendingDown
} from 'lucide-react';


import MacroEconomics from './MacroEconomics';
import FiscalAnatomy from './FiscalAnatomy';
import PensionTimebomb from './PensionTimebomb';
import HealthcareAnatomy from './HealthcareAnatomy';
import JusticeAndFDI from './JusticeAndFDI';
import EnergyAndPNRR from './EnergyAndPNRR';
import PNRRTracker from './PNRRTracker';

const pillars = [
  { id: 'all', icon: Layers, it: 'Tutti i Pilastri', en: 'All Pillars', badge: '8 Moduli' },
  { id: 'macro', icon: BarChart3, it: 'Macro & PIL', en: 'Macro & GDP', badge: '101.2 TFP' },
  { id: 'fiscal', icon: Receipt, it: 'Fisco & Cuneo', en: 'Fiscal & Tax Wedge', badge: '45.1%' },
  { id: 'pensions', icon: UserMinus, it: 'Pensioni & Demografia', en: 'Pensions & Demographics', badge: '1.35 Ratio' },
  { id: 'health', icon: Activity, it: 'Sanità Pubblica', en: 'Public Healthcare', badge: '21.4% OOP' },
  { id: 'justice', icon: Scale, it: 'Giustizia Civile & FDI', en: 'Civil Justice & FDI', badge: '540 Giorni' },
  { id: 'energy', icon: Zap, it: 'Energia & Costi Imprese', en: 'Energy & Business Costs', badge: 'EUR/MWh' },
  { id: 'pnrr', icon: Construction, it: 'Monitoraggio PNRR', en: 'PNRR Execution', badge: '€194.4B' }
];

export default function MacroExplorer() {
  const [activePillar, setActivePillar] = useState('all');

  return (
    <div className="w-full space-y-12">
      {/* SECTION HEADER */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-semibold uppercase tracking-wider">
          <BarChart3 size={14} />
          <T it="Istituzioni & Macroeconomia" en="Institutions & Macroeconomics" />
        </div>
        <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
          <T it="L'Anatomia Sistemica della Stagnazione" en="The Systemic Anatomy of Stagnation" />
        </h2>
        <p className="text-zinc-400 text-sm sm:text-base leading-relaxed">
          <T 
            it="I fallimenti della formazione a monte si propagano a valle su fisco, welfare, giustizia e competitività industriale. Esplora ciascun pilastro istituzionale singolarmente o visualizza l'analisi completa."
            en="Upstream education failures cascade downstream into taxes, welfare, justice, and industrial competitiveness. Explore each institutional pillar individually or view the full synthesis."
          />
        </p>

        {/* PILL NAVIGATION CONTROLLER */}
        <div className="flex flex-wrap items-center justify-center gap-2 pt-4">
          {pillars.map((pillar) => {
            const Icon = pillar.icon;
            const isActive = activePillar === pillar.id;
            return (
              <button
                key={pillar.id}
                onClick={() => setActivePillar(pillar.id)}
                className={`inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all border cursor-pointer ${
                  isActive 
                    ? 'bg-indigo-600 text-white border-indigo-400 shadow-[0_0_20px_rgba(79,70,229,0.35)]' 
                    : 'bg-zinc-900/80 text-zinc-400 border-white/5 hover:border-white/20 hover:text-white hover:bg-zinc-800/80'
                }`}
              >
                <Icon size={14} className={isActive ? 'text-white' : 'text-zinc-400'} />
                <span><T it={pillar.it} en={pillar.en} /></span>
                <span className={`px-1.5 py-0.5 text-[10px] rounded-md ${
                  isActive ? 'bg-white/20 text-white' : 'bg-white/5 text-zinc-400'
                }`}>
                  {pillar.badge}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* CONTENT VIEWER */}
      <div className="w-full">
        <AnimatePresence mode="wait">
          {activePillar === 'all' && (
            <motion.div 
              key="all"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25 }}
              className="space-y-24"
            >
              <MacroEconomics />
              <div className="border-t border-zinc-800/50" />
              <FiscalAnatomy />
              <div className="border-t border-zinc-800/50" />
              <PensionTimebomb />
              <div className="border-t border-zinc-800/50" />
              <HealthcareAnatomy />
              <div className="border-t border-zinc-800/50" />
              <JusticeAndFDI />
              <div className="border-t border-zinc-800/50" />
              <EnergyAndPNRR />
              <div className="border-t border-zinc-800/50" />
              <PNRRTracker />
            </motion.div>
          )}


          {activePillar === 'macro' && (
            <motion.div key="macro" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <MacroEconomics />
            </motion.div>
          )}

          {activePillar === 'fiscal' && (
            <motion.div key="fiscal" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <FiscalAnatomy />
            </motion.div>
          )}

          {activePillar === 'pensions' && (
            <motion.div key="pensions" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <PensionTimebomb />
            </motion.div>
          )}

          {activePillar === 'health' && (
            <motion.div key="health" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <HealthcareAnatomy />
            </motion.div>
          )}

          {activePillar === 'justice' && (
            <motion.div key="justice" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <JusticeAndFDI />
            </motion.div>
          )}

          {activePillar === 'energy' && (
            <motion.div key="energy" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <EnergyAndPNRR />
            </motion.div>
          )}

          {activePillar === 'pnrr' && (
            <motion.div key="pnrr" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.25 }}>
              <PNRRTracker />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
