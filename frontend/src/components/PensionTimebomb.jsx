import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, ReferenceLine } from 'recharts';
import { Baby, UserMinus, ShieldAlert, ArrowDownToLine } from 'lucide-react';
import SourceBadge from './SourceBadge';
import data from '../assets/pension_demographics.json';
import eu27Data from '../assets/eu27_comparative.json';

const PensionTimebomb = () => {
  const { lang } = useLanguage();
  const [showAllEU, setShowAllEU] = useState(false);
  const isIt = lang === 'it';

  const displayedEUData = useMemo(() => {
    const eu27ChartData = Object.entries(eu27Data.pension_spending_gdp_pct)
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


  const pensionData = [
    { name: 'Italy', val: data.pension_spending_gdp_pct.Italy },
    { name: 'France', val: data.pension_spending_gdp_pct.France },
    { name: 'Spain', val: data.pension_spending_gdp_pct.Spain },
    { name: 'EU Avg', val: data.pension_spending_gdp_pct.EU_Average },
    { name: 'Germany', val: data.pension_spending_gdp_pct.Germany }
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
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 text-sm font-medium mb-6">
            <ShieldAlert size={16} />
            <T it="Bomba a Orologeria INPS" en="INPS Timebomb" />
          </div>
          <h2 className="text-4xl md:text-5xl font-black mb-6 tracking-tight">
            <T it="Inverno Demografico & Pensioni" en="Demographic Winter & Pensions" />
          </h2>
          <p className="text-zinc-400 max-w-3xl mx-auto text-lg">
            <T 
              it="Il patto intergenerazionale italiano è matematicamente insostenibile. Una spesa pensionistica record che schiaccia un numero sempre minore di giovani lavoratori, costretti a finanziare il sistema a scapito della propria ricchezza futura." 
              en="The Italian intergenerational pact is mathematically unsustainable. Record pension spending crushing an ever-shrinking pool of young workers, who are forced to fund the system at the expense of their own future wealth." 
            />
          </p>
        </motion.div>

        <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
          >
            <h3 className="text-xl font-bold flex items-center gap-2 mb-6">
              <ArrowDownToLine className="text-rose-400" />
              <T it="Spesa Pensionistica (% PIL)" en="Pension Spending (% GDP)" />
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={pensionData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="name" stroke="#888" />
                  <YAxis type="number" stroke="#888" domain={[0, 18]} unit="%" />
                  <Tooltip 
                    cursor={{fill: '#ffffff05'}}
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', color: '#f4f4f5' }} 
                    formatter={(value) => [`${value}%`, 'Spesa / PIL']}
                  />
                  <Bar dataKey="val" radius={[4, 4, 0, 0]} barSize={40}>
                    {pensionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.name === 'Italy' ? '#f43f5e' : '#6366f1'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-sm text-zinc-400 mt-4">
              <T it="L'Italia destina la percentuale più alta del PIL alle pensioni tra i grandi paesi europei, sottraendo risorse vitali agli investimenti per i giovani (istruzione, innovazione)." en="Italy allocates the highest percentage of its GDP to pensions among major European countries, diverting vital resources away from youth investments (education, innovation)." />
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="flex flex-col gap-6"
          >
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 flex-1 flex flex-col justify-center">
              <h3 className="text-xl font-bold flex items-center gap-2 mb-2">
                <UserMinus className="text-amber-400" />
                <T it="Rapporto Lavoratori / Pensionati" en="Worker to Retiree Ratio" />
              </h3>
              <div className="flex items-end gap-4 mt-6">
                <div>
                  <div className="text-5xl font-black text-rose-500">{data.worker_to_retiree_ratio.Italy}</div>
                  <div className="text-sm font-bold text-zinc-400 uppercase mt-1"><T it="Italia" en="Italy" /></div>
                </div>
                <div className="text-3xl text-zinc-400 mb-1">VS</div>
                <div>
                  <div className="text-4xl font-black text-indigo-400">{data.worker_to_retiree_ratio.EU_Average}</div>
                  <div className="text-sm font-bold text-zinc-400 uppercase mt-1"><T it="Media EU" en="EU Avg" /></div>
                </div>
              </div>
              <p className="text-zinc-400 mt-6 leading-relaxed">
                <T 
                  it="Per mantenere in equilibrio un sistema pensionistico a ripartizione, servono almeno 3 lavoratori per ogni pensionato. L'Italia è a 1.6 e in caduta libera verso il collasso." 
                  en="To keep a pay-as-you-go pension system balanced, you need at least 3 workers per retiree. Italy is at 1.6 and in freefall towards collapse." 
                />
              </p>
            </div>
          </motion.div>
        </div>

        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 mt-12 mb-16 w-full"
        >
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Spesa Pensionistica — Confronto EU27" en="Pension Spending — EU27 Comparison" />
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
              <Bar dataKey="value" radius={[0, 6, 6, 0]} name={isIt ? "Spesa Pensionistica % PIL" : "Pension Spending % GDP"}>
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
          className="w-full bg-rose-500/5 border border-rose-500/20 rounded-3xl p-8 md:p-12 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-rose-500/10 blur-3xl rounded-full" />
          <h3 className="text-2xl font-bold flex items-center gap-3 mb-6 relative z-10">
            <Baby className="text-rose-400" size={32} />
            <T it="Il Fardello sui Giovani" en="The Burden on the Youth" />
          </h3>
          <p className="text-lg text-zinc-300 leading-relaxed relative z-10 max-w-4xl">
            {lang === 'it' ? data.youth_burden_description_it : data.youth_burden_description_en}
          </p>
          
          <div className="mt-8 flex flex-wrap gap-4 relative z-10">
            <SourceBadge label="Eurostat Pensions" topicKey="eurostat_pensions" />
            <SourceBadge label="INPS" agency="INPS" />
            <SourceBadge label="OECD Pensions at a Glance" topicKey="oecd_pensions_glance" />
          </div>
        </motion.div>

      </section>
    </div>
  );
};

export default PensionTimebomb;
