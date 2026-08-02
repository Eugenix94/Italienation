const fs = require('fs');

const file = 'frontend/src/views/UnifiedHome.jsx';
let content = fs.readFileSync(file, 'utf8');

// Add useEffect and useRef to imports if not there
if (!content.includes('useEffect')) {
  content = content.replace(/import React, \{ useState \} from 'react';/, "import React, { useState, useEffect, useRef } from 'react';");
} else if (!content.includes('useRef')) {
  content = content.replace(/import React, \{ useState, useEffect \} from 'react';/, "import React, { useState, useEffect, useRef } from 'react';");
}

// Replace the activeTab setter in the button with a scrollIntoView function call
content = content.replace(
  /onClick=\{\(\) => setActiveTab\(tab\.id\)\}/g,
  'onClick={() => scrollToSection(tab.id)}'
);

// Add the observer logic inside the component
const observerLogic = `
  const sectionRefs = useRef({});

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // When a section comes into view (at least 30% visible), set it as active
            setActiveTab(entry.target.id);
          }
        });
      },
      {
        rootMargin: '-20% 0px -60% 0px', // Trigger when section is in the upper part of the viewport
        threshold: 0.1
      }
    );

    Object.values(sectionRefs.current).forEach((section) => {
      if (section) observer.observe(section);
    });

    return () => observer.disconnect();
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
`;

if (!content.includes('const sectionRefs = useRef({});')) {
  content = content.replace(
    /const tabs = \[/,
    observerLogic + '\n  const tabs = ['
  );
}

// Now replace the conditional rendering with stacked sections
const oldAnimatePresence = /<AnimatePresence mode="wait">\s*<motion\.div[\s\S]*?className="w-full"\s*>[\s\S]*?<\/AnimatePresence>/;

const newSections = `
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
`;

content = content.replace(oldAnimatePresence, newSections);

// If AnimatePresence is no longer used we could remove it but keeping it is fine.
fs.writeFileSync(file, content);
console.log('Updated UnifiedHome.jsx for Scrollytelling');
