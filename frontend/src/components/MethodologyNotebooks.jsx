import React, { useState } from 'react';
import { T } from './T';
import { Book, Code, Activity, Map, ArrowRight } from 'lucide-react';

const notebooks = [
  { id: '00_interactive_data_playground_local_and_processed.html', title: 'Data Playground', category: 'Data', icon: Code },
  { id: '00_master_capstone_oted_66_domains.html', title: 'Master Capstone (66 Domains)', category: 'Synthesis', icon: Book },
  { id: '01_holistic_master_statistical_analysis.html', title: 'Holistic Statistical Analysis', category: 'Data', icon: Activity },
  { id: '02_origin_early_childhood_and_educational_poverty.html', title: 'Early Childhood Poverty', category: 'Origin', icon: Book },
  { id: '03_origin_textbook_burden_and_household_spending.html', title: 'Textbook Burden', category: 'Origin', icon: Book },
  { id: '04_tracking_tripartite_system_provenance.html', title: 'Tripartite System Provenance', category: 'Tracking', icon: Book },
  { id: '05_tracking_middle_to_upper_transition_and_barriers.html', title: 'Transition Barriers', category: 'Tracking', icon: Book },
  { id: '06_tracking_repeaters_and_implicit_dropout.html', title: 'Repeaters & Implicit Dropout', category: 'Tracking', icon: Book },
  { id: '07_geospatial_tripartite_distribution.html', title: 'Geospatial Tripartite Distribution', category: 'Map', icon: Map },
  { id: '07_transition_neet_youth_unemployment_panel.html', title: 'NEET & Youth Unemployment', category: 'Transition', icon: Book },
  { id: '08_transition_social_mobility_and_intermittency.html', title: 'Social Mobility', category: 'Transition', icon: Book },
  { id: '09_destination_fiscal_landscape_and_siope_delays.html', title: 'Fiscal Landscape & Delays', category: 'Destination', icon: Book },
  { id: '10_destination_territorial_expenditure_and_deficits.html', title: 'Territorial Expenditure', category: 'Destination', icon: Book },
  { id: '11_destination_tfp_stagnation_and_human_capital.html', title: 'TFP Stagnation & Human Capital', category: 'Destination', icon: Book },
  { id: '12_geospatial_territorial_maps_nuts2_nuts3.html', title: 'Territorial Maps (NUTS)', category: 'Map', icon: Map },
  { id: '13_international_benchmarks_eurydice_oecd_wb.html', title: 'International Benchmarks', category: 'Benchmark', icon: Activity },
  { id: '14_data_inventory_and_schematic_explorer.html', title: 'Data Inventory', category: 'Data', icon: Code },
  { id: '15_deep_cross_domain_econometric_synthesis.html', title: 'Econometric Synthesis', category: 'Synthesis', icon: Activity },
  { id: '16_institutional_expansion_and_comparative_synthesis.html', title: 'Institutional Expansion', category: 'Synthesis', icon: Book },
  { id: '17_curricular_fragmentation_and_cultural_capital_synthesis.html', title: 'Curricular Fragmentation', category: 'Synthesis', icon: Book },
  { id: '18_geospatial_catania_case_study_and_national_map.html', title: 'Catania Case Study', category: 'Map', icon: Map }
];

export default function MethodologyNotebooks() {
  const [activeNotebook, setActiveNotebook] = useState(notebooks[0].id);

  return (
    <div className="flex flex-col lg:flex-row h-full w-full min-h-[800px] border border-white/10 rounded-2xl overflow-hidden bg-zinc-950">
      {/* Sidebar List */}
      <div className="w-full lg:w-1/4 xl:w-1/5 bg-zinc-900 border-r border-white/5 overflow-y-auto max-h-[800px]">
        <div className="p-4 border-b border-white/5 sticky top-0 bg-zinc-900 z-10">
          <h2 className="text-xl font-bold text-white mb-1"><T it="Quaderni di Ricerca" en="Research Notebooks" /></h2>
          <p className="text-xs text-zinc-400"><T it="I notebook Jupyter interattivi" en="The interactive Jupyter notebooks" /></p>
        </div>
        <div className="p-2 space-y-1">
          {notebooks.map((nb) => (
            <button
              key={nb.id}
              onClick={() => setActiveNotebook(nb.id)}
              className={`w-full text-left px-3 py-3 rounded-xl flex items-start gap-3 transition-colors ${
                activeNotebook === nb.id 
                  ? 'bg-indigo-500/10 border border-indigo-500/30' 
                  : 'hover:bg-white/5 border border-transparent'
              }`}
            >
              <nb.icon size={18} className={`shrink-0 mt-0.5 ${activeNotebook === nb.id ? 'text-indigo-400' : 'text-zinc-500'}`} />
              <div className="flex-1 min-w-0">
                <p className={`text-sm truncate ${activeNotebook === nb.id ? 'font-bold text-indigo-100' : 'font-medium text-zinc-300'}`}>
                  {nb.title}
                </p>
                <p className="text-[10px] uppercase tracking-wider text-zinc-500 mt-0.5">{nb.category}</p>
              </div>
              {activeNotebook === nb.id && <ArrowRight size={14} className="text-indigo-500 shrink-0 mt-1" />}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content Iframe */}
      <div className="w-full lg:w-3/4 xl:w-4/5 h-[800px] bg-white relative">
        {/* Loading overlay logic could go here if needed, but iframes are self-managing mostly */}
        <div className="absolute top-0 left-0 w-full p-2 bg-zinc-900 border-b border-zinc-800 text-xs text-zinc-400 flex items-center gap-2 z-10 shadow-lg">
          <Code size={14} />
          <span><T it="Visualizzatore Notebook:" en="Notebook Viewer:" /> {activeNotebook}</span>
        </div>
        <iframe
          src={`${import.meta.env.BASE_URL}notebooks/${activeNotebook}`}
          className="w-full h-full pt-8 border-none"
          title="Jupyter Notebook"
          sandbox="allow-scripts allow-same-origin"
        />
      </div>
    </div>
  );
}
