import React from 'react';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import SourceBadge from './SourceBadge';
import { motion } from 'framer-motion';
import { Lightbulb, Scale } from 'lucide-react';
import data from '../assets/gender_innovation.json';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-zinc-900 border border-zinc-700 p-4 rounded-lg shadow-xl">
        <p className="font-bold text-white mb-2">{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color || entry.fill }} className="text-sm font-medium">
            {entry.name}: {entry.value}%
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function GenderAndInnovation() {
  const { lang } = useLanguage();
  const isIt = lang === 'it';

  return (
    <div className="w-full max-w-4xl mx-auto space-y-16">
      
      {/* SECTION HEADER */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center space-y-4"
      >
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-fuchsia-500/10 text-fuchsia-400 border border-fuchsia-500/20 text-sm font-medium mb-2">
          <Scale size={16} />
          <T it="Disuguaglianze & Sviluppo" en="Inequalities & Development" />
        </div>
        <h2 className="text-3xl sm:text-4xl font-black text-white">
          <T it="Gender Gap e Stagnazione dell'Innovazione" en="Gender Gap and Innovation Stagnation" />
        </h2>
        <p className="text-zinc-400 text-base sm:text-lg max-w-2xl mx-auto">
          <T 
            it="La mancata parità di genere si traduce in un colossale spreco di capitale umano, mentre i bassi investimenti in R&S limitano la creazione di ecosistemi ad alto valore aggiunto in grado di trattenere i talenti." 
            en="The lack of gender parity translates into a colossal waste of human capital, while low R&D investments limit the creation of high value-added ecosystems capable of retaining talent." 
          />
        </p>
      </motion.div>

      {/* CHARTS CONTAINER */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* GENDER GAP CHART */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-6 relative overflow-hidden"
        >
          <div className="flex justify-between items-start mb-6">
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Scale size={20} className="text-fuchsia-400" />
                <T it="Gender Pay Gap per Settore" en="Gender Pay Gap by Sector" />
              </h3>
              <p className="text-sm text-zinc-400 mt-1">
                <T it="Divario retributivo vs Partecipazione femminile" en="Pay gap vs Female participation" />
              </p>
            </div>
            <SourceBadge agency="Eurostat" topicKey="eurostat_gender" />
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.gender_gap} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="sector" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Bar 
                  dataKey="pay_gap_pct" 
                  name={isIt ? "Divario Retributivo" : "Pay Gap"} 
                  fill="#d946ef" 
                  radius={[4, 4, 0, 0]} 
                />
                <Bar 
                  dataKey="female_participation_pct" 
                  name={isIt ? "Partecipazione" : "Participation"} 
                  fill="#8b5cf6" 
                  radius={[4, 4, 0, 0]} 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* INNOVATION & R&D CHART */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-6 relative overflow-hidden"
        >
          <div className="flex justify-between items-start mb-6">
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Lightbulb size={20} className="text-amber-400" />
                <T it="Ecosistema Innovazione" en="Innovation Ecosystem" />
              </h3>
              <p className="text-sm text-zinc-400 mt-1">
                <T it="Spesa R&S su PIL vs Numero Startup Attive" en="R&D spending on GDP vs Active Startups" />
              </p>
            </div>
            <SourceBadge agency="OECD/Registro Imprese" topicKey="oecd_rd" />
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.innovation_rd} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRd" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#fbbf24" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#fbbf24" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="year" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                
                {/* Due assi Y per scale diverse (Percentuale vs Assoluto) */}
                <YAxis yAxisId="left" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 12 }} domain={[1.0, 2.0]} />
                
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Area 
                  yAxisId="left"
                  type="monotone" 
                  dataKey="rd_gdp_pct" 
                  name={isIt ? "Spesa R&S (% PIL)" : "R&D Spend (% GDP)"} 
                  stroke="#fbbf24" 
                  fillOpacity={1} 
                  fill="url(#colorRd)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
      
    </div>
  );
}
