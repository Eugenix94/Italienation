import React, { useState, useEffect, useRef, Suspense, lazy } from 'react';
import Hero from '../components/Hero';
import ExecutiveSummary from '../components/ExecutiveSummary';

import { BookOpen, LineChart, Map, Layers, Database, BarChart2, Book, Search, ChevronRight, Menu, X, BrainCircuit, AlertTriangle, TrendingDown } from 'lucide-react';
import { T } from '../components/T';
import { motion, AnimatePresence } from 'framer-motion';

// Lazy load components
const MacroExplorer = lazy(() => import('../components/MacroExplorer'));
const PolicySandbox = lazy(() => import('../components/PolicySandbox'));
const StructuralOutcomes = lazy(() => import('../components/StructuralOutcomes'));
const InternationalBenchmark = lazy(() => import('../components/InternationalBenchmark'));
const GradeRetention = lazy(() => import('../components/GradeRetention'));
const TripartiteSimulator = lazy(() => import('../components/TripartiteSimulator'));
const GISMap = lazy(() => import('../components/GISMap'));
const TerritorialMap = lazy(() => import('../components/TerritorialMap'));
const FlowDynamics = lazy(() => import('../components/FlowDynamics'));
const SystemicDeepDives = lazy(() => import('../components/SystemicDeepDives'));
const EU27PESComparison = lazy(() => import('../components/EU27PESComparison'));
const EconometricCosts = lazy(() => import('../components/EconometricCosts'));
const DemographicFallout = lazy(() => import('../components/DemographicFallout'));
const SystemicCollapse = lazy(() => import('../components/SystemicCollapse'));
const LaborMarketAndCorrelations = lazy(() => import('../components/LaborMarketAndCorrelations'));
const MigrationAndRemittances = lazy(() => import('../components/MigrationAndRemittances'));
const ScrollyDataHub = lazy(() => import('../components/ScrollyDataHub'));
const DeveloperAPI = lazy(() => import('../components/DeveloperAPI'));
import DataCatalogCTA from '../components/DataCatalogCTA';
const AngloAmericanComparison = lazy(() => import('../components/AngloAmericanComparison'));
const ReligiousOptOut = lazy(() => import('../components/ReligiousOptOut'));
const MethodologyNotebooks = lazy(() => import('../components/MethodologyNotebooks'));
const StructuralDeepDives = lazy(() => import('../components/StructuralDeepDives'));
const CulturalPhenomenology = lazy(() => import('../components/CulturalPhenomenology'));
const MediaKitExport = lazy(() => import('../components/MediaKitExport'));
const MigrationGovernance = lazy(() => import('../components/MigrationGovernance'));
const DigitalAndHousing = lazy(() => import('../components/DigitalAndHousing'));
const GenderAndInnovation = lazy(() => import('../components/GenderAndInnovation'));
const EducationalGuide = lazy(() => import('../components/EducationalGuide'));

export default function UnifiedHome() {
  const [activeTab, setActiveTab] = useState('costo');
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
      const yOffset = -80; 
      const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  };

  const tabs = [
    { id: 'costo', icon: TrendingDown, it: 'Il Costo Italia', en: 'The Price Tag' },
    { id: 'oed', icon: BookOpen, it: 'Il Capitale Umano', en: 'Human Capital Pipeline' },
    { id: 'frizioni', icon: BarChart2, it: 'Inefficienze Strutturali', en: 'Systemic Bottlenecks' },
    { id: 'sintomi', icon: AlertTriangle, it: 'Sintomi & Destinazione', en: 'Fallout & Destination' },
    { id: 'soluzioni', icon: BrainCircuit, it: 'Interventi & Policy', en: 'Policy Sandbox' },
    { id: 'metodologia', icon: Database, it: 'Dati & Metodologia', en: 'Methodology & Data' }
  ];

  return (
    <div className="w-full min-h-screen bg-[#050510] text-white flex flex-col relative">
      <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-b from-indigo-900/10 via-purple-900/5 to-transparent rounded-full blur-[120px] pointer-events-none" />

      {/* HERO SECTION */}
      <section id="manifesto" className="relative z-10">
        <Hero />
      </section>

      {/* EXECUTIVE SUMMARY */}
      <div className="relative z-10">
        <ExecutiveSummary onExploreClick={() => {
            setActiveTab('costo');
            const el = document.getElementById('costo');
            if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.pageYOffset - 80, behavior: 'smooth' });
        }} />
      </div>

      <div className="flex flex-col flex-1 relative z-10 w-full">
        
        {/* NAVIGATION SIDEBAR DRAWER */}
        <AnimatePresence>
          {isSidebarOpen && (
            <>
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setIsSidebarOpen(false)}
                className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[70]"
                aria-hidden="true"
              />
              <motion.nav 
                initial={{ x: '-100%' }}
                animate={{ x: 0 }}
                exit={{ x: '-100%' }}
                transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                aria-label="Main dashboard navigation" 
                className="fixed inset-y-0 left-0 w-80 max-w-[85vw] bg-[#050510]/95 backdrop-blur-xl border-r border-white/5 z-[80] shadow-2xl flex flex-col"
              >
                <div className="p-6 border-b border-white/5 flex items-center justify-between sticky top-0 bg-[#050510]/95 backdrop-blur-xl z-10">
                  <h3 className="text-lg font-black tracking-widest uppercase bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400 flex items-center gap-2">
                    <Layers size={18} className="text-indigo-400" />
                    <span><T it="Esplora" en="Explore" /></span>
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
                
                {/* 1. THE PRICE TAG (THE HOOK) */}
                <section id="costo" ref={el => sectionRefs.current['costo'] = el} className="scroll-mt-24 space-y-24">
                  <EconometricCosts />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                {/* 2. HUMAN CAPITAL PIPELINE */}
                <section id="oed" ref={el => sectionRefs.current['oed'] = el} className="scroll-mt-24 space-y-24">
                  <div className="text-center space-y-3 max-w-2xl mx-auto">
                    <span className="text-xs font-black tracking-widest text-purple-400 uppercase">
                      <T it="La Radice del Problema" en="The Root Cause" />
                    </span>
                    <h2 className="text-3xl sm:text-4xl font-black text-white">
                      <T it="Il Capitale Umano (O.E.D.)" en="The Human Capital Pipeline" />
                    </h2>
                    <p className="text-zinc-400 text-sm sm:text-base">
                      <T 
                        it="Il 90% del costo nasce qui. Come l'origine socio-economica determina i percorsi educativi e limita il potenziale della forza lavoro."
                        en="90% of the cost starts here. How socio-economic origins dictate educational pathways and throttle workforce potential."
                      />
                    </p>
                  </div>
                  
                  <ScrollyDataHub />
                  <TripartiteSimulator />
                  <GradeRetention />
                  <EducationalGuide />
                  <StructuralOutcomes />
                  <AngloAmericanComparison />
                  <ReligiousOptOut />
                  <InternationalBenchmark />
                  <StructuralDeepDives />
                  <CulturalPhenomenology />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                {/* 3. SYSTEMIC BOTTLENECKS */}
                <section id="frizioni" ref={el => sectionRefs.current['frizioni'] = el} className="scroll-mt-24 space-y-24">
                  <div className="text-center space-y-3 max-w-2xl mx-auto">
                    <span className="text-xs font-black tracking-widest text-amber-400 uppercase">
                      <T it="Gli Attriti del Sistema" en="Systemic Friction" />
                    </span>
                    <h2 className="text-3xl sm:text-4xl font-black text-white">
                      <T it="Inefficienze Strutturali" en="Systemic Bottlenecks" />
                    </h2>
                    <p className="text-zinc-400 text-sm sm:text-base">
                      <T 
                        it="Il capitale umano sfavorito incontra un ecosistema ostile: burocrazia, giustizia lenta, crisi demografica e alti costi energetici."
                        en="Disadvantaged human capital meets a hostile ecosystem: bureaucracy, slow justice, demographic crisis, and high energy costs."
                      />
                    </p>
                  </div>
                  
                  <MacroExplorer />
                  <SystemicCollapse />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                {/* 4. FALLOUT & DESTINATION */}
                <section id="sintomi" ref={el => sectionRefs.current['sintomi'] = el} className="scroll-mt-24 space-y-24">
                  <div className="text-center space-y-3 max-w-2xl mx-auto">
                    <span className="text-xs font-black tracking-widest text-rose-400 uppercase">
                      <T it="Le Conseguenze" en="The Fallout" />
                    </span>
                    <h2 className="text-3xl sm:text-4xl font-black text-white">
                      <T it="Sintomi & Destinazione" en="Symptoms & Destination" />
                    </h2>
                    <p className="text-zinc-400 text-sm sm:text-base">
                      <T 
                        it="Il risultato finale: lavoro nero, fuga di cervelli, NEET e un divario territoriale insostenibile tra Nord e Sud."
                        en="The end result: shadow economy, brain drain, NEETs, and an unsustainable territorial divide between North and South."
                      />
                    </p>
                  </div>
                  
                  <FlowDynamics />
                  <LaborMarketAndCorrelations />
                  <MigrationAndRemittances />
                  <MigrationGovernance />
                  <SystemicDeepDives />
                  <EU27PESComparison />
                  <DemographicFallout />
                  <TerritorialMap />
                  <GISMap />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />
                
                {/* 5. INTERVENTIONS / POLICY SANDBOX */}
                <section id="soluzioni" ref={el => sectionRefs.current['soluzioni'] = el} className="scroll-mt-24 space-y-24">
                  <div className="text-center space-y-3 max-w-2xl mx-auto">
                    <span className="text-xs font-black tracking-widest text-emerald-400 uppercase">
                      <T it="Modellare il Futuro" en="Modeling the Future" />
                    </span>
                    <h2 className="text-3xl sm:text-4xl font-black text-white">
                      <T it="Laboratorio di Simulazione & Policy" en="Simulation & Policy Lab" />
                    </h2>
                    <p className="text-zinc-400 text-sm sm:text-base">
                      <T 
                        it="Possiamo invertire la rotta? Testa le leve macroeconomiche e scopri l'impatto potenziale di riforme mirate."
                        en="Can we reverse the trend? Test macroeconomic levers and discover the potential impact of targeted reforms."
                      />
                    </p>
                  </div>
                  
                  <PolicySandbox />
                  <DigitalAndHousing />
                  <GenderAndInnovation />
                </section>
                <div className="border-t border-zinc-800/50 my-8" />

                {/* 6. METHODOLOGY & DATA */}
                <section id="metodologia" ref={el => sectionRefs.current['metodologia'] = el} className="scroll-mt-24 space-y-24">
                  <div className="text-center space-y-3 max-w-2xl mx-auto">
                    <span className="text-xs font-black tracking-widest text-cyan-400 uppercase">
                      <T it="Trasparenza & Open Data" en="Transparency & Open Data" />
                    </span>
                    <h2 className="text-3xl sm:text-4xl font-black text-white">
                      <T it="Dati & Metodologia" en="Methodology & Data Hub" />
                    </h2>
                  </div>
                  
                  <MethodologyNotebooks />
                  <DeveloperAPI />
                  <MediaKitExport />
                </section>
              </Suspense>
            </div>

          </div>

          <div className="mt-20">
            <DataCatalogCTA />
          </div>

        </div>
      </div>
    </div>
  );
}
