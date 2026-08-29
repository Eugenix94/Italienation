import React, { useState, useEffect } from 'react';
import { T } from './T';
import SourceBadge from './SourceBadge';
import * as LucideIcons from 'lucide-react';
import { Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function AngloAmericanComparison() {
  const [comparisonData, setComparisonData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/anglo_american_data.json`)
      .then(res => res.json())
      .then(data => {
        setComparisonData(data.comparisonData);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load Anglo-American data:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="animate-spin text-indigo-500" size={32} />
      </div>
    );
  }

  return (
    <div className="space-y-8 py-12">
      <div className="text-center max-w-3xl mx-auto mb-12">
        <h2 className="text-3xl font-bold text-white mb-4">
          <T it="Complessità dell'Orientamento: Italia vs Modello Anglosassone" en="Orientation Complexity: Italy vs Anglo-American Model" />
        </h2>
        <p className="text-zinc-400 text-lg mb-6">
          <T 
            it="Un confronto tra la rigidità del modello a binari paralleli italiano e la flessibilità del modello comprensivo anglosassone." 
            en="A comparison between the rigidity of the Italian parallel-track model and the flexibility of the Anglo-American comprehensive model." 
          />
        </p>
        <div className="flex justify-center">
          <SourceBadge agency="Eurydice / OECD" year="2023" />
        </div>
      </div>

      <div className="bg-white/[0.02] border border-white/5 rounded-3xl p-1 overflow-hidden shadow-2xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-1 bg-zinc-900 rounded-2xl overflow-hidden text-sm sm:text-base">
          
          {/* Header */}
          <div className="hidden md:flex p-6 items-center font-bold text-zinc-400 uppercase tracking-widest text-xs">
            <T it="Metrica di Confronto" en="Comparison Metric" />
          </div>
          <div className="p-6 flex items-center justify-center gap-3 bg-zinc-800/30 font-bold text-white text-lg sm:text-xl border-b border-rose-500/20">
            <span className="w-3 h-3 rounded-full bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.5)]"></span>
            <T it="Sistema Italiano" en="Italian System" />
          </div>
          <div className="p-6 flex items-center justify-center gap-3 bg-zinc-800/30 font-bold text-white text-lg sm:text-xl border-b border-emerald-500/20">
            <span className="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></span>
            <T it="Modello Anglosassone" en="Anglo-American Model" />
          </div>

          {/* Rows */}
          {comparisonData.map((row, i) => {
            const Icon = LucideIcons[row.iconName] || LucideIcons.Layers;
            return (
              <React.Fragment key={i}>
                <div className="p-6 flex flex-col md:flex-row items-start md:items-center gap-4 bg-zinc-950/50">
                  <div className="w-10 h-10 rounded-xl bg-zinc-900 flex items-center justify-center text-zinc-400 shrink-0 border border-zinc-800">
                    <Icon size={18} />
                  </div>
                  <span className="font-bold text-white"><T it={row.metric.it} en={row.metric.en} /></span>
                </div>
                
                <div className="p-6 bg-rose-950/10 border-l-2 border-rose-500/20 flex flex-col justify-center">
                  <span className="md:hidden text-xs font-bold text-rose-500 mb-2"><T it="Italia" en="Italy" /></span>
                  <div className="flex items-start gap-3">
                    <AlertCircle size={16} className="text-rose-400 mt-1 shrink-0" />
                    <p className="text-zinc-300 leading-relaxed"><T it={row.italy.it} en={row.italy.en} /></p>
                  </div>
                </div>

                <div className="p-6 bg-emerald-950/10 border-l-2 border-emerald-500/20 flex flex-col justify-center">
                  <span className="md:hidden text-xs font-bold text-emerald-500 mb-2"><T it="Modello Anglosassone" en="Anglo Model" /></span>
                  <div className="flex items-start gap-3">
                    <CheckCircle2 size={16} className="text-emerald-400 mt-1 shrink-0" />
                    <p className="text-zinc-300 leading-relaxed"><T it={row.anglo.it} en={row.anglo.en} /></p>
                  </div>
                </div>
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
}
