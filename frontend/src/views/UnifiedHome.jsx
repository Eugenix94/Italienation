import React, { useState, useEffect, useRef, Suspense, lazy } from 'react';
import Hero from '../components/Hero';
import { BookOpen, LineChart, Map, Layers, Database, BarChart2, Book, Search, ChevronRight, Menu, X, BrainCircuit, AlertTriangle } from 'lucide-react';
import { T } from '../components/T';
import { motion, AnimatePresence } from 'framer-motion';

const StructuralOutcomes = lazy(() => import('../components/StructuralOutcomes'));
const InternationalBenchmark = lazy(() => import('../components/InternationalBenchmark'));
const TripartiteSimulator = lazy(() => import('../components/TripartiteSimulator'));
const GISMap = lazy(() => import('../components/GISMap'));
const TerritorialMap = lazy(() => import('../components/TerritorialMap'));
const FlowDynamics = lazy(() => import('../components/FlowDynamics'));
const SystemicDeepDives = lazy(() => import('../components/SystemicDeepDives'));
const EU27PESComparison = lazy(() => import('../components/EU27PESComparison'));
const EconometricCosts = lazy(() => import('../components/EconometricCosts'));
const MacroEconomics = lazy(() => import('../components/MacroEconomics'));
const DemographicFallout = lazy(() => import('../components/DemographicFallout'));
const SystemicCollapse = lazy(() => import('../components/SystemicCollapse'));
const LaborMarketAndCorrelations = lazy(() => import('../components/LaborMarketAndCorrelations'));
const MigrationAndRemittances = lazy(() => import('../components/MigrationAndRemittances'));
const ScrollyDataHub = lazy(() => import('../components/ScrollyDataHub'));
const DeveloperAPI = lazy(() => import('../components/DeveloperAPI'));
const DataCatalogCTA = lazy(() => import('../components/DataCatalogCTA'));
const AngloAmericanComparison = lazy(() => import('../components/AngloAmericanComparison'));
const ReligiousOptOut = lazy(() => import('../components/ReligiousOptOut'));
const MethodologyNotebooks = lazy(() => import('../components/MethodologyNotebooks'));
const StructuralDeepDives = lazy(() => import('../components/StructuralDeepDives'));
const CulturalPhenomenology = lazy(() => import('../components/CulturalPhenomenology'));
const MediaKitExport = lazy(() => import('../components/MediaKitExport'));


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
    { id: 'fallout', icon: BrainCircuit, it: 'Impatto Sociale', en: 'Social Impact' },
    { id: 'collapse', icon: AlertTriangle, it: 'Collasso di Sistema', en: 'Systemic Collapse' },
    { id: 'deepdives', icon: Search, it: 'Approfondimenti', en: 'Deep Dives' },
    { id: 'methodology', icon: Book, it: 'Metodologia', en: 'Methodology' },
    { id: 'data', icon: Database, it: 'Dati & API', en: 'Data Hub & API' }
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
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 lg:pt-16 pb-24 my-0 flex flex-col items-center">
            
            <div className="w-full space-y-40">
              <Suspense fallback={<div className="flex items-center justify-center h-96 w-full text-zinc-500"><div className="flex flex-col items-center gap-4"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-t-2 border-indigo-500"></div><span className="text-sm tracking-widest uppercase font-semibold text-zinc-400">Loading Content...</span></div></div>}>
                <section id="struttura" ref={el => sectionRefs.current['struttura'] = el} className="scroll-mt-24 space-y-32">
                  <StructuralOutcomes />
                  <AngloAmericanComparison />
                  <ReligiousOptOut />
                  <InternationalBenchmark />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                <section id="simulator" ref={el => sectionRefs.current['simulator'] = el} className="scroll-mt-24">
                  <TripartiteSimulator />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                <section id="map" ref={el => sectionRefs.current['map'] = el} className="scroll-mt-24 space-y-24">
                  <TerritorialMap />
                  <GISMap />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                <section id="analysis" ref={el => sectionRefs.current['analysis'] = el} className="scroll-mt-24 space-y-24">
                  <FlowDynamics />
                  <LaborMarketAndCorrelations />
                  <MigrationAndRemittances />
                  <SystemicDeepDives />
                  <EU27PESComparison />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                <section id="macro" ref={el => sectionRefs.current['macro'] = el} className="scroll-mt-24 space-y-24">
                  <EconometricCosts />
                  <MacroEconomics />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                <section id="fallout" ref={el => sectionRefs.current['fallout'] = el} className="scroll-mt-24 space-y-24">
                  <DemographicFallout />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                <section id="collapse" ref={el => sectionRefs.current['collapse'] = el} className="scroll-mt-24 space-y-24">
                  <SystemicCollapse />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                <section id="deepdives" ref={el => sectionRefs.current['deepdives'] = el} className="scroll-mt-24 space-y-24">
                  <StructuralDeepDives />
                  <CulturalPhenomenology />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                <section id="methodology" ref={el => sectionRefs.current['methodology'] = el} className="scroll-mt-24">
                  <MethodologyNotebooks />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />

                <section id="data" ref={el => sectionRefs.current['data'] = el} className="scroll-mt-24 space-y-24">
                  <ScrollyDataHub />
                  <DeveloperAPI />
                  <MediaKitExport />
                </section>
              </Suspense>
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
