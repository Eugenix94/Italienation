import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, Legend } from 'recharts';
import { Activity, Clock, Users, ArrowRightLeft, Stethoscope, AlertTriangle } from 'lucide-react';
import SourceBadge from './SourceBadge';
import data from '../assets/healthcare_anatomy.json';
import eu27Data from '../assets/eu27_comparative.json';

const HealthcareAnatomy = () => {
  const { lang } = useLanguage();
  const [showAllEU, setShowAllEU] = useState(false);
  const isIt = lang === 'it';

  const displayedEUData = useMemo(() => {
    const eu27ChartData = Object.entries(eu27Data.healthcare_oop_pct)
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


  const spendingData = [
    { name: 'Italy', val: data.out_of_pocket_spending_pct.Italy },
    { name: 'France', val: data.out_of_pocket_spending_pct.France },
    { name: 'Germany', val: data.out_of_pocket_spending_pct.Germany },
    { name: 'EU Avg', val: data.out_of_pocket_spending_pct.EU_Average }
  ];

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
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-sm font-medium mb-6">
            <Activity size={16} />
            <T it="Collasso del Welfare" en="Welfare Collapse" />
          </div>
          <h2 className="text-4xl md:text-5xl font-black mb-6 tracking-tight">
            <T it="Anatomia Sanitaria (SSN)" en="Healthcare Anatomy (SSN)" />
          </h2>
          <p className="text-zinc-400 max-w-3xl mx-auto text-lg">
            <T 
              it="Il Servizio Sanitario Nazionale, un tempo fiore all'occhiello dell'Italia, sta affrontando una crisi strutturale senza precedenti. Tempi di attesa insostenibili, privatizzazione strisciante tramite la spesa 'out-of-pocket' e un esodo massiccio di medici verso il Nord Europa." 
              en="The National Health Service, once Italy's pride, is facing an unprecedented structural crisis. Unsustainable wait times, creeping privatization via 'out-of-pocket' spending, and a massive exodus of doctors to Northern Europe." 
            />
          </p>
        </motion.div>

        <div className="w-full flex flex-col lg:flex-row gap-8 mb-16">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="w-full lg:w-1/2 bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
          >
            <h3 className="text-xl font-bold flex items-center gap-2 mb-6">
              <AlertTriangle className="text-rose-400" />
              <T it="Spesa Privata (Out-of-Pocket) %" en="Out-of-Pocket Spending %" />
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={spendingData} layout="vertical" margin={{ top: 0, right: 30, left: 10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={true} vertical={false} />
                  <XAxis type="number" stroke="#888" domain={[0, 25]} unit="%" />
                  <YAxis dataKey="name" type="category" stroke="#888" width={80} />
                  <Tooltip 
                    cursor={{fill: '#ffffff05'}}
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', color: '#f4f4f5' }} 
                    formatter={(value) => [`${value}%`, 'Spesa Out-of-Pocket']}
                  />
                  <Bar dataKey="val" radius={[0, 4, 4, 0]} barSize={24}>
                    {spendingData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.name === 'Italy' ? '#f43f5e' : '#6366f1'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-sm text-zinc-400 mt-4">
              <T it="In Italia i cittadini pagano direttamente di tasca propria oltre il 21% delle spese sanitarie totali a causa dell'inefficienza del sistema pubblico, il doppio rispetto a Francia e Germania." en="In Italy, citizens pay out-of-pocket for over 21% of total healthcare expenses due to public system inefficiency, double the rate of France and Germany." />
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="w-full lg:w-1/2 flex flex-col gap-6"
          >
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 flex-1">
              <h3 className="text-xl font-bold flex items-center gap-2 mb-4">
                <Clock className="text-amber-400" />
                <T it="Liste d'Attesa" en="Wait Times" />
              </h3>
              <div className="text-5xl font-black text-amber-400 mb-4">{data.wait_times_months_specialist.Italy}+ <span className="text-xl text-zinc-400 font-medium">Mesi / Months</span></div>
              <p className="text-zinc-300">{data.wait_times_months_specialist.Notes}</p>
            </div>
          </motion.div>
        </div>

        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 mt-12 mb-16 w-full"
        >
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Spesa Out-of-Pocket — Confronto EU27" en="Out-of-Pocket Spending — EU27 Comparison" />
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
              <Bar dataKey="value" radius={[0, 6, 6, 0]} name={isIt ? "% Spesa Diretta" : "Out-of-Pocket %"}>
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
          className="w-full bg-indigo-500/5 border border-indigo-500/20 rounded-3xl p-8 md:p-12 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 blur-3xl rounded-full" />
          <h3 className="text-2xl font-bold flex items-center gap-3 mb-6 relative z-10">
            <Stethoscope className="text-indigo-400" size={32} />
            <T it="L'Esodo dei Medici (Brain Drain)" en="Doctor Brain Drain" />
          </h3>
          <div className="flex flex-col md:flex-row gap-8 relative z-10">
            <div className="md:w-1/3">
              <div className="text-6xl font-black text-white mb-2">{data.doctor_brain_drain.emigrated_doctors_last_10_years.toLocaleString()}</div>
              <div className="text-indigo-400 font-bold uppercase tracking-wider text-sm"><T it="Medici emigrati (Ultimi 10 anni)" en="Emigrated doctors (Last 10 years)" /></div>
            </div>
            <div className="md:w-2/3">
              <p className="text-lg text-zinc-300 leading-relaxed">
                {lang === 'it' ? data.doctor_brain_drain.impact_description_it : data.doctor_brain_drain.impact_description_en}
              </p>
            </div>
          </div>
          
          <div className="mt-8 flex flex-wrap gap-4 relative z-10">
            <SourceBadge label="Fondazione GIMBE" topicKey="fondazione_gimbe" />
            <SourceBadge label="OECD Health Data" topicKey="oecd_health_data" />
            <SourceBadge label="World Bank" topicKey="worldbank_out_of_pocket" />
            <SourceBadge label="FNOMCeO / Anaao" topicKey="fnomceo_anaao" />
          </div>
        </motion.div>

      </section>
    </div>
  );
};

export default HealthcareAnatomy;
