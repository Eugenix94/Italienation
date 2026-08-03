import React, { useState, useEffect, useRef } from 'react';
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
import { BookOpen, LineChart, Map, Layers, Database, BarChart2, Book, Search, ChevronRight, Menu, X } from 'lucide-react';
import { T } from '../components/T';
import { motion, AnimatePresence } from 'framer-motion';

export default function UnifiedHome() {
  const [activeTab, setActiveTab] = useState('struttura');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  
  const sectionRefs = useRef({});

  useEffect(() => {
    const handleToggle = () => setIsSidebarOpen(prev => !prev);
    window.addEventListener('toggle-sidebar', handleToggle);

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveTab(entry.target.id);
          }
        });
      },
      {
        rootMargin: '-20% 0px -60% 0px',
        threshold: 0.1
      }
    );

    Object.values(sectionRefs.current).forEach((section) => {
      if (section) observer.observe(section);
    });

    return () => {
      window.removeEventListener('toggle-sidebar', handleToggle);
      observer.disconnect();
    };
  }, []);

  const scrollToSection = (id) => {
    setActiveTab(id);
    const element = document.getElementById(id);
    if (element) {
      // Get the height of the sticky navbar if any (approx 64px) + some padding
      const yOffset = -80; 
      const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  };

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
      <div className="flex flex-col flex-1 relative z-10 w-full">
        
        {/* NAVIGATION SIDEBAR DRAWER */}
        <AnimatePresence>
          {isSidebarOpen && (
            <>
              {/* BACKDROP */}
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setIsSidebarOpen(false)}
                className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[70]"
                aria-hidden="true"
              />
              
              {/* SIDEBAR */}
              <motion.nav 
                initial={{ x: '-100%' }}
                animate={{ x: 0 }}
                exit={{ x: '-100%' }}
                transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                aria-label="Main dashboard navigation" 
                className="fixed top-0 left-0 h-screen w-72 md:w-80 border-r border-white/10 bg-[#09090b]/95 backdrop-blur-3xl z-[80] shadow-[20px_0_40px_rgba(0,0,0,0.5)] flex flex-col"
              >
                <div className="flex items-center justify-between p-6 border-b border-white/10 mt-16 lg:mt-0">
                  <h3 className="text-xs font-black tracking-widest text-zinc-500 uppercase" id="sidebar-heading">
                    <T it="Osservatorio Dati" en="Data Observatory" />
                  </h3>
                  <button 
                    onClick={() => setIsSidebarOpen(false)}
                    className="p-2 text-zinc-400 hover:text-white rounded-lg hover:bg-white/5 transition-colors"
                  >
                    <X size={20} />
                  </button>
                </div>
                
                <div className="flex-1 overflow-y-auto p-4 gap-2 flex flex-col hide-scrollbar">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    const isActive = activeTab === tab.id;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => {
                          scrollToSection(tab.id);
                          setIsSidebarOpen(false);
                        }}
                        aria-current={isActive ? 'page' : undefined}
                        className={`group flex items-center gap-3 px-5 py-4 text-sm font-bold transition-all duration-300 relative whitespace-nowrap rounded-2xl w-full text-left focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-[#050510]
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
                          <motion.div layoutId="sidebar-active">
                            <ChevronRight size={16} className="text-indigo-400" aria-hidden="true" />
                          </motion.div>
                        )}
                      </button>
                    );
                  })}
                </div>
              </motion.nav>
            </>
          )}
        </AnimatePresence>

        {/* DASHBOARD CONTENT */}
        <div className="flex-1 w-full overflow-hidden relative">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-12 pt-8 lg:pt-16 pb-24">
            
            <div className="w-full space-y-32">
                <section id="struttura" ref={el => sectionRefs.current['struttura'] = el} className="scroll-mt-24 space-y-32">
                  <StructuralOutcomes />
                  <AngloAmericanComparison />
                  <ReligiousOptOut />
                  <InternationalBenchmark />
                </section>
                
                <section id="simulator" ref={el => sectionRefs.current['simulator'] = el} className="scroll-mt-24">
                  <TripartiteSimulator />
                </section>
                
                <section id="map" ref={el => sectionRefs.current['map'] = el} className="scroll-mt-24 space-y-24">
                  <TerritorialMap />
                  <GISMap />
                </section>
                
                <section id="analysis" ref={el => sectionRefs.current['analysis'] = el} className="scroll-mt-24 space-y-24">
                  <FlowDynamics />
                  <LaborMarketAndCorrelations />
                  <MigrationAndRemittances />
                  <SystemicDeepDives />
                  <EU27PESComparison />
                </section>
                
                <section id="macro" ref={el => sectionRefs.current['macro'] = el} className="scroll-mt-24 space-y-24">
                  <EconometricCosts />
                  <MacroEconomics />
                </section>
                
                <section id="data" ref={el => sectionRefs.current['data'] = el} className="scroll-mt-24 space-y-24">
                  <ScrollyDataHub />
                  <DeveloperAPI />
                  <MediaKitExport />
                </section>
                
                <section id="deepdives" ref={el => sectionRefs.current['deepdives'] = el} className="scroll-mt-24 space-y-24">
                  <StructuralDeepDives />
                  <CulturalPhenomenology />
                </section>
                
                <section id="methodology" ref={el => sectionRefs.current['methodology'] = el} className="scroll-mt-24">
                  <MethodologyNotebooks />
                </section>
            </div>

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
