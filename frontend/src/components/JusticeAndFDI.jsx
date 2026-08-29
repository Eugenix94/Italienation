import React from 'react';
import { motion } from 'framer-motion';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';
import { Scale, Briefcase, FileSignature, TrendingDown } from 'lucide-react';
import SourceBadge from './SourceBadge';
import data from '../assets/justice_fdi.json';
import eu27Data from '../assets/eu27_comparative.json';

const JusticeAndFDI = () => {
  const { lang } = useLanguage();

  const eu27ChartData = Object.entries(eu27Data.civil_trial_days)
    .map(([country, value]) => ({ country, value }))
    .sort((a, b) => b.value - a.value);

  const trialData = [
    { name: 'Italy', val: data.civil_trial_length_days.Italy },
    { name: 'France', val: data.civil_trial_length_days.France },
    { name: 'Germany', val: data.civil_trial_length_days.Germany },
    { name: 'EU Avg', val: data.civil_trial_length_days.EU_Average }
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
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 text-sm font-medium mb-6">
            <Scale size={16} />
            <T it="Deterrenza Economica" en="Economic Deterrence" />
          </div>
          <h2 className="text-4xl md:text-5xl font-black mb-6 tracking-tight">
            <T it="Giustizia Civile & Investimenti Esteri (IDE)" en="Civil Justice & Foreign Direct Investment (FDI)" />
          </h2>
          <p className="text-zinc-400 max-w-3xl mx-auto text-lg">
            <T 
              it="Il capitale globale fugge dall'incertezza. Un sistema giudiziario civile estremamente lento e una burocrazia ostile agiscono come un muro invisibile contro gli investimenti esteri (IDE), bloccando la crescita e l'innovazione in Italia." 
              en="Global capital flees uncertainty. An extremely slow civil justice system and hostile bureaucracy act as an invisible wall against Foreign Direct Investment (FDI), stalling growth and innovation in Italy." 
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
              <TrendingDown className="text-amber-400" />
              <T it="Durata dei Processi Civili (Giorni, 1° Grado)" en="Length of Civil Trials (Days, 1st Instance)" />
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trialData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="name" stroke="#888" />
                  <YAxis type="number" stroke="#888" domain={[0, 600]} />
                  <Tooltip 
                    cursor={{fill: '#ffffff05'}}
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', color: '#f4f4f5' }} 
                    formatter={(value) => [`${value} Giorni / Days`, 'Durata / Length']}
                  />
                  <Bar dataKey="val" radius={[4, 4, 0, 0]} barSize={40}>
                    {trialData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.name === 'Italy' ? '#f59e0b' : '#6366f1'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-sm text-zinc-400 mt-4">
              <T it="I tempi lunghi della giustizia civile impediscono alle aziende di recuperare crediti o risolvere dispute in tempi certi, distruggendo la fiducia del mercato." en="Lengthy civil justice timelines prevent businesses from recovering debts or resolving disputes in a predictable timeframe, destroying market trust." />
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="w-full lg:w-1/2 flex flex-col gap-6"
          >
            <div className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 flex-1 flex flex-col justify-center">
              <h3 className="text-xl font-bold flex items-center gap-2 mb-2">
                <FileSignature className="text-rose-400" />
                <T it="Costo per far rispettare un contratto (% del valore)" en="Cost to Enforce a Contract (% of claim)" />
              </h3>
              <div className="flex items-end gap-4 mt-6">
                <div>
                  <div className="text-5xl font-black text-rose-500">{data.contract_enforcement_cost_pct_claim.Italy}%</div>
                  <div className="text-sm font-bold text-zinc-400 uppercase mt-1"><T it="Italia" en="Italy" /></div>
                </div>
                <div className="text-3xl text-zinc-400 mb-1">VS</div>
                <div>
                  <div className="text-4xl font-black text-emerald-400">{data.contract_enforcement_cost_pct_claim.Germany}%</div>
                  <div className="text-sm font-bold text-zinc-400 uppercase mt-1"><T it="Germania" en="Germany" /></div>
                </div>
              </div>
              <p className="text-zinc-400 mt-6 leading-relaxed">
                <T 
                  it="In Italia, le spese legali e burocratiche bruciano quasi un terzo del valore della disputa. Un disincentivo enorme a firmare contratti commerciali." 
                  en="In Italy, legal and bureaucratic fees burn almost a third of the dispute's value. A massive disincentive to sign commercial contracts." 
                />
              </p>
            </div>
          </motion.div>
        </div>

        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 mt-12 mb-16 w-full"
        >
          <h3 className="text-xl font-bold text-white mb-6">
            <T it="Durata Processi Civili — Confronto EU27" en="Civil Trial Duration — EU27 Comparison" />
          </h3>
          <ResponsiveContainer width="100%" height={700}>
            <BarChart data={eu27ChartData} layout="vertical" margin={{ left: 90, right: 20, top: 5, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
              <XAxis type="number" tick={{ fill: '#a1a1aa', fontSize: 12 }} stroke="#3f3f46" />
              <YAxis type="category" dataKey="country" tick={{ fill: '#d4d4d8', fontSize: 11 }} stroke="#3f3f46" width={85} />
              <Tooltip contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }} itemStyle={{ color: '#ffffff' }} labelStyle={{ color: '#ffffff' }} />
              <Bar dataKey="value" radius={[0, 6, 6, 0]} name={isIt ? "Durata Processo Civile (Giorni)" : "Civil Trial Duration (Days)"}>
                {eu27ChartData.map((entry, i) => (
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
          className="w-full bg-amber-500/5 border border-amber-500/20 rounded-3xl p-8 md:p-12 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-amber-500/10 blur-3xl rounded-full" />
          <h3 className="text-2xl font-bold flex items-center gap-3 mb-6 relative z-10">
            <Briefcase className="text-amber-400" size={32} />
            <T it="La Fuga dei Capitali (IDE)" en="The Flight of Capital (FDI)" />
          </h3>
          <p className="text-lg text-zinc-300 leading-relaxed relative z-10 max-w-4xl">
            {lang === 'it' ? data.fdi_deterrence_factor.description_it : data.fdi_deterrence_factor.description_en}
          </p>
          
          <div className="mt-8 flex flex-wrap gap-4 relative z-10">
            <SourceBadge label="CEPEJ Justice Scoreboard" topicKey="cepej_justice_scoreboard" />
            <SourceBadge label="World Bank Doing Business" topicKey="worldbank_doing_business" />
          </div>
        </motion.div>

      </section>
    </div>
  );
};

export default JusticeAndFDI;
