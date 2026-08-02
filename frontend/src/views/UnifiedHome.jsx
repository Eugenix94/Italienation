import React, { useState } from 'react';
import Hero from '../components/Hero';
import StructuralOutcomes from '../components/StructuralOutcomes';
import InternationalBenchmark from '../components/InternationalBenchmark';
import TripartiteSimulator from '../components/TripartiteSimulator';
import GISMap from '../components/GISMap';
import TerritorialMap from '../components/TerritorialMap';
import FlowDynamics from '../components/FlowDynamics';
import SystemicDeepDives from '../components/SystemicDeepDives';
import EU27PESComparison from '../components/EU27PESComparison';
import EconometricCosts from '../components/EconometricCosts';
import MacroEconomics from '../components/MacroEconomics';
import LaborMarketAndCorrelations from '../components/LaborMarketAndCorrelations';
import MigrationAndRemittances from '../components/MigrationAndRemittances';
import ScrollyDataHub from '../components/ScrollyDataHub';
import DeveloperAPI from '../components/DeveloperAPI';
import DataCatalogCTA from '../components/DataCatalogCTA';
import AngloAmericanComparison from '../components/AngloAmericanComparison';
import ReligiousOptOut from '../components/ReligiousOptOut';
import MethodologyNotebooks from '../components/MethodologyNotebooks';
import StructuralDeepDives from '../components/StructuralDeepDives';
import CulturalPhenomenology from '../components/CulturalPhenomenology';
import MediaKitExport from '../components/MediaKitExport';
import { BookOpen, LineChart, Map, Layers, Database, BarChart2, Book, Search, ChevronRight } from 'lucide-react';
import { T } from '../components/T';
import { motion, AnimatePresence } from 'framer-motion';

export default function UnifiedHome() {
  const [activeTab, setActiveTab] = useState('struttura');

  const tabs = [
    { id: 'struttura', icon: BookOpen, it: 'Struttura & Tracking', en: 'Structure & Tracking' },
    { id: 'simulator', icon: LineChart, it: 'Esperienza Tripartita', en: 'Tripartite Experience' },
    { id: 'map', icon: Map, it: 'Mappa GIS', en: 'GIS Map' },
    { id: 'analysis', icon: Layers, it: 'Mercato & Lavoro', en: 'Labor Market' },
    { id: 'macro', icon: BarChart2, it: 'Costi Macro', en: 'Macro Costs' },
    { id: 'data', icon: Database, it: 'Dati & API', en: 'Data Hub & API' },
    { id: 'deepdives', icon: Search, it: 'Approfondimenti', en: 'Deep Dives' },
    { id: 'methodology', icon: Book, it: 'Metodologia', en: 'Methodology' }
  ];

  return (
    <div className="w-full min-h-screen bg-[#050510] text-white flex flex-col relative">
      
      {/* AMBIENT MESH GRADIENT */}
      <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-b from-indigo-900/10 via-purple-900/5 to-transparent rounded-full blur-[120px] pointer-events-none" />

      {/* HERO SECTION */}
      <section id="manifesto" className="relative z-10">
        <Hero />
      </section>

      {/* SIDEBAR + CONTENT LAYOUT */}
      <div className="flex flex-col lg:flex-row flex-1 relative z-10">
        
        {/* NAVIGATION SIDEBAR */}
        <nav aria-label="Main dashboard navigation" className="lg:w-72 lg:shrink-0 lg:border-r border-white/[0.05] bg-white/[0.01] backdrop-blur-3xl lg:sticky lg:top-16 lg:h-[calc(100vh-4rem)] z-40 border-b lg:border-b-0 sticky top-16 shadow-[20px_0_40px_rgba(0,0,0,0.5)] lg:shadow-none">
          <div className="flex lg:flex-col overflow-x-auto hide-scrollbar p-4 lg:p-6 gap-2 lg:gap-3 snap-x snap-mandatory">
            <h3 className="hidden lg:block text-xs font-black tracking-widest text-zinc-500 uppercase mb-4 px-4" id="sidebar-heading">
              <T it="Osservatorio Dati" en="Data Observatory" />
            </h3>
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  aria-current={isActive ? 'page' : undefined}
                  className={`group flex items-center gap-3 px-4 lg:px-5 py-3 lg:py-4 text-sm font-bold transition-all duration-300 relative whitespace-nowrap rounded-2xl lg:w-full lg:text-left snap-start focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-[#050510]
                    ${isActive 
                      ? 'text-white bg-gradient-to-r from-indigo-500/20 to-purple-500/10 border border-indigo-500/30 shadow-[0_0_20px_rgba(99,102,241,0.15)]' 
                      : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/[0.03] border border-transparent hover:border-white/[0.05]'
                    }`}
                >
                  <div className={`p-1.5 rounded-lg transition-colors ${isActive ? 'bg-indigo-500/20 text-indigo-400' : 'bg-transparent text-zinc-500 group-hover:text-zinc-300'}`}>
                    <Icon size={18} aria-hidden="true" />
                  </div>
                  <span className="flex-1"><T it={tab.it} en={tab.en} /></span>
                  {isActive && (
                    <motion.div layoutId="sidebar-active" className="hidden lg:block">
                      <ChevronRight size={16} className="text-indigo-400" aria-hidden="true" />
                    </motion.div>
                  )}
                </button>
              );
            })}
          </div>
        </nav>

        {/* DASHBOARD CONTENT */}
        <div className="flex-1 w-full lg:max-w-[calc(100vw-18rem)] overflow-hidden relative">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-12 pt-8 lg:pt-16 pb-24">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(4px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 1.02, filter: 'blur(4px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="w-full"
              >
                {activeTab === 'struttura' && (
                  <div className="space-y-32">
                    <StructuralOutcomes />
                    <AngloAmericanComparison />
                    <ReligiousOptOut />
                    <InternationalBenchmark />
                  </div>
                )}
                
                {activeTab === 'simulator' && (
                  <div>
                    <TripartiteSimulator />
                  </div>
                )}
                
                {activeTab === 'map' && (
                  <div className="space-y-24">
                    <TerritorialMap />
                    <GISMap />
                  </div>
                )}
                
                {activeTab === 'analysis' && (
                  <div className="space-y-24">
                    <FlowDynamics />
                    <LaborMarketAndCorrelations />
                    <MigrationAndRemittances />
                    <SystemicDeepDives />
                    <EU27PESComparison />
                  </div>
                )}
                
                {activeTab === 'macro' && (
                  <div className="space-y-24">
                    <EconometricCosts />
                    <MacroEconomics />
                  </div>
                )}
                
                {activeTab === 'data' && (
                  <div className="space-y-24">
                    <ScrollyDataHub />
                    <DeveloperAPI />
                    <MediaKitExport />
                  </div>
                )}
                
                {activeTab === 'deepdives' && (
                  <div className="space-y-24">
                    <StructuralDeepDives />
                    <CulturalPhenomenology />
                  </div>
                )}
                
                {activeTab === 'methodology' && (
                  <div>
                    <MethodologyNotebooks />
                  </div>
                )}
              </motion.div>
            </AnimatePresence>
          </div>

          {/* BOTTOM SECTIONS */}
          <div>
            <DataCatalogCTA />
          </div>

        </div>
      </div>
    </div>
  );
}
