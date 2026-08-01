import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import * as LucideIcons from 'lucide-react';
import { Loader2 } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { T } from './T';
import SourceBadge from './SourceBadge';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-zinc-900 border border-zinc-700 p-3 rounded-lg shadow-xl">
        <p className="text-zinc-300 font-medium mb-2"><T it="Ripartizione Costi" en="Cost Breakdown" /></p>
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center gap-2 text-sm my-1">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.fill }} />
            <span className="text-zinc-400 capitalize">{entry.name}:</span>
            <span className="text-white font-bold">€{entry.value}B</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

const EconometricCosts = () => {
  const [lostGdpSeconds, setLostGdpSeconds] = React.useState(0);

  // Real-time ticker for lost GDP (€259B/yr ÷ 31.5M seconds = ~€8,213/sec)
  React.useEffect(() => {
    const timer = setInterval(() => {
      setLostGdpSeconds(prev => prev + 8213);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-zinc-950 text-white font-sans overflow-hidden">
      
      {/* Hero Section */}
      <section className="relative pt-32 pb-16 px-6 lg:px-8 max-w-7xl mx-auto flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm font-medium mb-6">
            <TrendingDown size={16} />
            <T it="Dati Economici 2023" en="2023 Economic Data" />
          </div>
          <h1 className="text-3xl sm:text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
            <span className="bg-gradient-to-br from-white via-white to-zinc-500 bg-clip-text text-transparent">
              <T it="Il Costo del " en="The Cost of " />
            </span>
            <span className="bg-gradient-to-r from-rose-400 to-rose-600 bg-clip-text text-transparent">
              <T it="Fallimento" en="Failure" />
            </span>
          </h1>
          
          <div className="mt-8 mb-6">
            <p className="text-4xl sm:text-6xl md:text-8xl font-black bg-gradient-to-r from-rose-500 via-rose-400 to-orange-400 bg-clip-text text-transparent drop-shadow-sm">
              €259 <span className="text-3xl sm:text-4xl md:text-6xl text-zinc-400 font-bold">Billion</span>
            </p>
            <p className="text-lg sm:text-xl md:text-2xl text-zinc-400 font-medium mt-2 mb-4">
              <T it="~13.5% del PIL Italiano ogni anno" en="~13.5% of Italian GDP annually" />
            </p>
            <div className="inline-flex items-center justify-center gap-2 px-4 py-2 bg-zinc-900 border border-rose-500/30 rounded-xl text-rose-400 font-mono text-sm sm:text-base shadow-[0_0_20px_rgba(244,63,94,0.15)] relative group cursor-help">
               <TrendingDown size={18} className="animate-pulse" /> 
               <span>Costo PIL: <span className="font-bold">+€{lostGdpSeconds.toLocaleString()}</span>/session</span>
               <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-64 bg-zinc-900 border border-zinc-700 text-zinc-300 text-xs p-3 rounded-lg shadow-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
                  <p className="font-bold text-rose-400 mb-1"><T it="Il Costo del Fallimento" en="The Cost of Failure" /></p>
                  <p><T it="Calcolo in tempo reale: €259 Miliardi / anno = ~8.213 € persi ogni secondo." en="Real-time calculation: €259 Billion / year = ~€8,213 lost every second." /></p>
                </div>
            </div>
          </div>
          
          <p className="text-base sm:text-lg text-zinc-500 max-w-2xl mx-auto mt-6">
            <T 
              it="Stima conservativa inferiore dei costi annuali derivanti dai fallimenti strutturali del sistema educativo italiano, basata su fonti istituzionali verificate." 
              en="Conservative lower-bound estimate of annual costs from Italy's education system structural failures, based on verified institutional sources." 
            />
          </p>
        </motion.div>
      </section>

      {/* Cost Breakdown Cards */}
      <section className="py-16 px-6 lg:px-8 max-w-7xl mx-auto">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-12"
        >
          <h2 className="text-3xl font-bold mb-8 text-zinc-100">
            <T it="Ripartizione del Deficit" en="Deficit Breakdown" />
          </h2>
          
          {/* Horizontal Bar Chart */}
          <div className="h-24 w-full bg-white/[0.02] border border-white/5 rounded-2xl p-4 mb-10">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                layout="vertical"
                data={chartData}
                margin={{ top: 0, right: 0, left: 0, bottom: 0 }}
              >
                <XAxis type="number" hide />
                <YAxis dataKey="name" type="category" hide />
                <Tooltip content={<CustomTooltip />} cursor={{fill: 'transparent'}} />
                <Bar dataKey="shadow" stackId="a" fill="#f43f5e" name="Shadow Economy" radius={[4, 0, 0, 4]} />
                <Bar dataKey="neet" stackId="a" fill="#e11d48" name="NEET" />
                <Bar dataKey="mismatch" stackId="a" fill="#fb7185" name="Skills Mismatch" />
                <Bar dataKey="brain_drain" stackId="a" fill="#fda4af" name="Brain Drain" />
                <Bar dataKey="dispersione" stackId="a" fill="#be123c" name="Dropout" />
                <Bar dataKey="bocciatura" stackId="a" fill="#9f1239" name="Retention" />
                <Bar dataKey="systemic_other" stackId="a" fill="#4c0519" name="Other Systemic Costs" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {costItems.map((item, idx) => {
              const ItemIcon = LucideIcons[item.icon] || LucideIcons.EyeOff;
              return (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.1 }}
                className="bg-white/[0.02] backdrop-blur-md border border-white/5 rounded-2xl p-6 hover:bg-white/[0.04] transition-colors group relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
                  <ItemIcon size={64} style={{ color: item.color }} />
                </div>
                
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-lg bg-zinc-900 border border-zinc-800">
                    <ItemIcon size={20} style={{ color: item.color }} />
                  </div>
                  <h3 className="font-semibold text-zinc-200">
                    <T it={item.itTitle} en={item.enTitle} />
                  </h3>
                </div>
                
                <div className="mb-4">
                  <span className="text-4xl font-bold" style={{ color: item.color }}>€{item.value}</span>
                  <span className="text-zinc-500 font-medium ml-1">Billion</span>
                </div>
                
                <p className="text-zinc-400 text-sm mb-6">
                  <T it={item.itDesc} en={item.enDesc} />
                </p>
                
                <div className="mt-auto pt-4 border-t border-white/5 flex items-center justify-between">
                  <p className="text-xs font-medium text-zinc-300">
                    <T it={item.itCompare} en={item.enCompare} />
                  </p>
                  <SourceBadge agency={item.source} topicKey={item.id} year="2026" />
                </div>
              </motion.div>
              );
            })}
          </div>
        </motion.div>
      </section>

      {/* Structural Mechanisms */}
      <section className="py-16 px-6 lg:px-8 bg-zinc-900/50 border-t border-b border-zinc-800/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-12"
          >
            <h2 className="text-3xl font-bold mb-4 text-zinc-100">
              <T it="Meccanismi Strutturali" en="Structural Mechanisms" />
            </h2>
            <p className="text-zinc-400 max-w-3xl">
              <T 
                it="Le inefficienze non sono casuali, ma derivano da precise scelte sistemiche che penalizzano gli studenti e l'economia." 
                en="Inefficiencies are not random; they stem from specific systemic choices that penalize students and the economy." 
              />
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {structuralMechanisms.map((mech, idx) => {
              const MechIcon = LucideIcons[mech.icon] || LucideIcons.BookOpen;
              return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.1 }}
                className="bg-zinc-950/50 border border-zinc-800 rounded-2xl p-6"
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-xl bg-rose-500/10 text-rose-400 shrink-0">
                    <MechIcon size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-zinc-200 mb-1">
                      <T it={mech.itTitle} en={mech.enTitle} />
                    </h3>
                    <div className="flex items-baseline gap-2 mb-2">
                      <span className="text-2xl font-bold text-white">{mech.stat}</span>
                      <span className="text-sm text-zinc-400">
                        <T it={mech.itSub} en={mech.enSub} />
                      </span>
                    </div>
                    <div className="inline-flex items-center px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 text-xs font-medium mt-2">
                      <T it={mech.itVs} en={mech.enVs} />
                    </div>
                  </div>
                </div>
              </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* International Comparison Table */}
      <section className="py-16 px-6 lg:px-8 max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl font-bold mb-8 text-zinc-100">
            <T it="Confronto Internazionale" en="International Comparison" />
          </h2>
          
          <div className="overflow-x-auto rounded-2xl border border-zinc-800 bg-white/[0.02] backdrop-blur-sm">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-zinc-800">
                  <th className="p-4 text-zinc-400 font-medium whitespace-nowrap"><T it="Metrica" en="Metric" /></th>
                  <th className="p-4 text-rose-400 font-bold bg-rose-500/5 whitespace-nowrap">Italia 🇮🇹</th>
                  <th className="p-4 text-emerald-400 font-medium whitespace-nowrap">Finland 🇫🇮</th>
                  <th className="p-4 text-emerald-400 font-medium whitespace-nowrap">Germany 🇩🇪</th>
                  <th className="p-4 text-emerald-400 font-medium whitespace-nowrap">Sweden 🇸🇪</th>
                  <th className="p-4 text-emerald-400 font-medium whitespace-nowrap">Malta 🇲🇹</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/50">
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Età di Scelta Indirizzo" en="Tracking Age" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5">13 <T it="anni" en="years" /></td>
                  <td className="p-4 text-zinc-400">16 <T it="anni" en="years" /></td>
                  <td className="p-4 text-zinc-400">10 (ma flessibile / but flexible)</td>
                  <td className="p-4 text-zinc-400">16 <T it="anni" en="years" /></td>
                  <td className="p-4 text-emerald-400">11 <T it="anni" en="years" /></td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Libri di Testo" en="Free Textbooks" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5"><T it="A pagamento (€1200+)" en="Paid (€1200+)" /></td>
                  <td className="p-4 text-emerald-400"><T it="Gratuiti al 100%" en="100% Free" /></td>
                  <td className="p-4 text-emerald-400"><T it="Forniti dalla scuola" en="School provided" /></td>
                  <td className="p-4 text-emerald-400"><T it="Gratuiti al 100%" en="100% Free" /></td>
                  <td className="p-4 text-emerald-400"><T it="Gratuiti al 100%" en="100% Free" /></td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Bocciature" en="Grade Retention" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5"><T it="Pratica comune (6.9%)" en="Common (6.9%)" /></td>
                  <td className="p-4 text-emerald-400"><T it="Quasi inesistente" en="Virtually zero" /></td>
                  <td className="p-4 text-zinc-400"><T it="Rara" en="Rare" /></td>
                  <td className="p-4 text-emerald-400"><T it="Abolita" en="Abolished" /></td>
                  <td className="p-4 text-emerald-400"><T it="Rara" en="Rare" /></td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Seconda Chance" en="Second-Chance Pathway" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5"><T it="Inesistente" en="Non-existent" /></td>
                  <td className="p-4 text-emerald-400"><T it="Strutturata (Valma)" en="Structured (Valma)" /></td>
                  <td className="p-4 text-emerald-400"><T it="Sistema Transitorio" en="Transition System" /></td>
                  <td className="p-4 text-emerald-400"><T it="Folkhögskola" en="Folkhögskola" /></td>
                  <td className="p-4 text-emerald-400">MCAST</td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Tasso NEET" en="NEET Rate" /></td>
                  <td className="p-4 text-rose-300 font-bold bg-rose-500/5">19.0%</td>
                  <td className="p-4 text-zinc-400">9.3%</td>
                  <td className="p-4 text-emerald-400">8.6%</td>
                  <td className="p-4 text-emerald-400">5.7%</td>
                  <td className="p-4 text-emerald-400">7.5%</td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Stipendio Apprendisti" en="Apprentice Salary" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5">€0 (PCTO) - €400</td>
                  <td className="p-4 text-zinc-400">Contratti collettivi / CBA</td>
                  <td className="p-4 text-emerald-400">€600 - €1,200/mo</td>
                  <td className="p-4 text-zinc-400">Contratti collettivi / CBA</td>
                  <td className="p-4 text-emerald-400"><T it="Stipendio MCAST" en="MCAST Stipend" /></td>
                </tr>
              </tbody>
            </table>
          </div>
        </motion.div>
      </section>

    </div>
  );
};

export default EconometricCosts;
