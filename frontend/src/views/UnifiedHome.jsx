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
import ScrollyDataHub from '../components/ScrollyDataHub';
import DeveloperAPI from '../components/DeveloperAPI';
import DataCatalogCTA from '../components/DataCatalogCTA';
import AngloAmericanComparison from '../components/AngloAmericanComparison';
import ReligiousOptOut from '../components/ReligiousOptOut';
import MethodologyNotebooks from '../components/MethodologyNotebooks';
import StructuralDeepDives from '../components/StructuralDeepDives';
import MediaKitExport from '../components/MediaKitExport';
import { BookOpen, LineChart, Map, Layers, Database, BarChart2, Book, Search } from 'lucide-react';
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
    <div className="w-full min-h-screen bg-[#050510] text-white flex flex-col pb-12">
      
      {/* HERO SECTION (Always visible) */}
      <section id="manifesto">
        <Hero />
      </section>

      {/* DASHBOARD NAVIGATION */}
      <div className="sticky top-16 z-40 bg-[#050510]/95 backdrop-blur-xl border-b border-white/10 pt-4 pb-0 mb-8 lg:mb-12 shadow-2xl shadow-black/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex overflow-x-auto custom-scrollbar gap-2 pb-px">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-5 py-4 text-sm font-bold transition-all relative whitespace-nowrap rounded-t-xl
                    ${isActive 
                      ? 'text-indigo-400 bg-white/[0.03]' 
                      : 'text-zinc-500 hover:text-zinc-300 hover:bg-white/[0.01]'
                    }`}
                >
                  <Icon size={16} />
                  <span><T it={tab.it} en={tab.en} /></span>
                  
                  {isActive && (
                    <motion.div 
                      layoutId="activeTabIndicator"
                      className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500 shadow-[0_-2px_8px_rgba(99,102,241,0.5)]"
                    />
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* DASHBOARD CONTENT */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full flex-1 pt-4 lg:pt-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="w-full"
          >
            {activeTab === 'struttura' && (
              <div className="space-y-32 animate-in fade-in slide-in-from-bottom-8 duration-700 pb-24">
                <StructuralOutcomes />
                <AngloAmericanComparison />
                <ReligiousOptOut />
                <InternationalBenchmark />
              </div>
            )}
            
            {activeTab === 'simulator' && (
              <div className="animate-in fade-in slide-in-from-bottom-8 duration-700">
                <TripartiteSimulator />
              </div>
            )}
            
            {activeTab === 'map' && (
              <div className="space-y-24 animate-in fade-in slide-in-from-bottom-8 duration-700">
                <TerritorialMap />
                <GISMap />
              </div>
            )}
            
            {activeTab === 'analysis' && (
              <div className="space-y-24 animate-in fade-in slide-in-from-bottom-8 duration-700">
                <FlowDynamics />
                <SystemicDeepDives />
                <EU27PESComparison />
              </div>
            )}
            
            {activeTab === 'macro' && (
              <div className="space-y-24 animate-in fade-in slide-in-from-bottom-8 duration-700">
                <EconometricCosts />
                <MacroEconomics />
              </div>
            )}
            
            {activeTab === 'data' && (
              <div className="space-y-24 animate-in fade-in slide-in-from-bottom-8 duration-700">
                <ScrollyDataHub />
                <DeveloperAPI />
              </div>
            )}
            
            {activeTab === 'deepdives' && (
              <div className="space-y-24 animate-in fade-in slide-in-from-bottom-8 duration-700">
                <StructuralDeepDives />
              </div>
            )}
            
            {activeTab === 'methodology' && (
              <div className="animate-in fade-in slide-in-from-bottom-8 duration-700">
                <MethodologyNotebooks />
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* MEDIA KIT EXPORT */}
      <MediaKitExport />

      {/* FOOTER CTA */}
      <div>
        <DataCatalogCTA />
      </div>

    </div>
  );
}
