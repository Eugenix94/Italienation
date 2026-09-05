import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, PieChart, Pie } from 'recharts';
import { Zap, Construction, ServerCrash, Clock, AlertTriangle } from 'lucide-react';
import SourceBadge from './SourceBadge';
import data from '../assets/energy_infrastructure.json';
import eu27Data from '../assets/eu27_comparative.json';

const EnergyAndPNRR = () => {
  const { lang } = useLanguage();
  const [showAllEU, setShowAllEU] = useState(false);
  const isIt = lang === 'it';

  const displayedEUData = useMemo(() => {
    const eu27ChartData = Object.entries(eu27Data.electricity_eur_mwh)
      .map(([country, value]) => ({ country, value }))
      .sort((a, b) => b.value - a.value);

    if (showAllEU) return eu27ChartData;

    const top5 = eu27ChartData.slice(0, 5);
    const bottom5 = eu27ChartData.slice(-5);
    const italy = eu27ChartData.find(d => d.country === 'Italy');
    const combined = [...top5];
    if (italy && !combined.some(d => d.country === 'Italy')) {
      combined.push(italy);
    }
    bottom5.forEach(d => {
      if (!combined.some(c => c.country === d.country)) {
        combined.push(d);
      }
    });
    return combined.sort((a, b) => b.value - a.value);
  }, [showAllEU]);


  const energyData = [
    { name: 'Italy', val: data.electricity_cost_business_eur_mwh.Italy },
    { name: 'France', val: data.electricity_cost_business_eur_mwh.France },
    { name: 'Germany', val: data.electricity_cost_business_eur_mwh.Germany },
    { name: 'Spain', val: data.electricity_cost_business_eur_mwh.Spain }
  ].sort((a, b) => b.val - a.val);

  return (
    <div className="w-full text-white font-sans py-16">
      <section className="max-w-7xl mx-auto px-4 w-full flex flex-col items-center">
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 text-center w-full"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-sm font-medium mb-6">
            <Construction size={16} />
            <T it="Competitività & Infrastrutture" en="Competitiveness & Infrastructure" />
          </div>
          <h2 className="text-4xl md:text-5xl font-black mb-6 tracking-tight">
            <T it="Energia & Costi Logistici" en="Energy & Logistics Costs" />
          </h2>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
            <T 
              it="Perché l'industria arranca? Analizziamo i costi dell'energia superiori alla media europea e il deficit logistico-digitale." 
              en="Why is industry struggling? We analyze above-average energy costs and the digital-logistics deficit." 
            />
          </p>
        </motion.div>

        <div className="w-full max-w-3xl mx-auto mb-16">
          
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
          >
            <h3 className="text-xl font-bold flex items-center gap-2 mb-6">
              <Zap className="text-amber-400" />
              <T it="Costo Energia (Imprese, EUR/MWh)" en="Energy Cost (Business, EUR/MWh)" />
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={energyData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="name" stroke="#888" />
                  <YAxis type="number" stroke="#888" domain={[0, 250]} />
                  <Tooltip 
                    cursor={{fill: '#ffffff05'}}
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', color: '#f4f4f5' }} 
                    formatter={(value) => [`€${value}`, 'EUR / MWh']}
                  />
                  <Bar dataKey="val" radius={[4, 4, 0, 0]} barSize={40}>
                    {energyData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.name === 'Italy' ? '#f59e0b' : '#64748b'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-sm text-zinc-400 mt-4">
              <T it="La profonda dipendenza dell'Italia dalle importazioni di gas e l'assenza di un mix energetico diversificato rendono le nostre imprese strutturalmente meno competitive." en="Italy's deep dependence on gas imports and the lack of a diversified energy mix make our businesses structurally less competitive." />
            </p>
          </motion.div>
        </div>

        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 mt-12 mb-16 w-full"
        >
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Costi Elettricità — Confronto EU27" en="Electricity Costs — EU27 Comparison" />
            </h3>
            <div className="inline-flex rounded-lg bg-zinc-800/80 p-1 border border-zinc-700/50 self-start sm:self-auto">
              <button
                type="button"
                onClick={() => setShowAllEU(false)}
                className={`px-3 py-1 text-xs font-semibold rounded-md transition cursor-pointer ${!showAllEU ? 'bg-indigo-600 text-white shadow' : 'text-zinc-400 hover:text-white'}`}
              >
                <T it="Focus: Top/Flop + Italia" en="Focus: Leaders/Laggards + Italy" />
              </button>
              <button
                type="button"
                onClick={() => setShowAllEU(true)}
                className={`px-3 py-1 text-xs font-semibold rounded-md transition cursor-pointer ${showAllEU ? 'bg-indigo-600 text-white shadow' : 'text-zinc-400 hover:text-white'}`}
              >
                <T it="Tutti i 27 Paesi" en="All 27 Countries" />
              </button>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={showAllEU ? 700 : 400}>
            <BarChart data={displayedEUData} layout="vertical" margin={{ left: 90, right: 20, top: 5, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
              <XAxis type="number" tick={{ fill: '#a1a1aa', fontSize: 12 }} stroke="#3f3f46" />
              <YAxis type="category" dataKey="country" tick={{ fill: '#d4d4d8', fontSize: 11 }} stroke="#3f3f46" width={85} />
              <Tooltip contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }} itemStyle={{ color: '#ffffff' }} labelStyle={{ color: '#ffffff' }} />
              <Bar dataKey="value" radius={[0, 6, 6, 0]} name={isIt ? "Prezzo Elettricità (EUR/MWh)" : "Electricity Price (EUR/MWh)"}>
                {displayedEUData.map((entry, i) => (
                  <Cell key={i} fill={entry.country === 'Italy' ? '#f43f5e' : '#64748b'} fillOpacity={entry.country === 'Italy' ? 1 : 0.7} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="w-full bg-emerald-500/5 border border-emerald-500/20 rounded-3xl p-8 md:p-12 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 blur-3xl rounded-full" />
          <h3 className="text-2xl font-bold flex items-center gap-3 mb-6 relative z-10">
            <ServerCrash className="text-emerald-400" size={32} />
            <T it="Il Gap Infrastrutturale" en="The Infrastructure Gap" />
          </h3>
          <p className="text-lg text-zinc-300 leading-relaxed relative z-10 max-w-4xl">
            {lang === 'it' ? data.infrastructure_gap.description_it : data.infrastructure_gap.description_en}
          </p>
          
          <div className="mt-8 flex flex-wrap gap-4 relative z-10">
            <SourceBadge label="Eurostat Energy" topicKey="eurostat_energy_electricity" />
            <SourceBadge label="OpenPNRR / Corte dei Conti" topicKey="openpnrr_openpolis" />
            <SourceBadge label="Trading Economics" topicKey="trading_economics_electricity" />
          </div>
        </motion.div>

      </section>
    </div>
  );
};

export default EnergyAndPNRR;
