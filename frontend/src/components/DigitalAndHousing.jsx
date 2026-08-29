import React from 'react';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import SourceBadge from './SourceBadge';
import { motion } from 'framer-motion';
import { Wifi, Home as HomeIcon } from 'lucide-react';
import data from '../assets/digital_housing.json';

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

export default function DigitalAndHousing() {
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
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-sm font-medium mb-2">
          <Wifi size={16} />
          <T it="Infrastruttura & Autonomia" en="Infrastructure & Autonomy" />
        </div>
        <h2 className="text-3xl sm:text-4xl font-black text-white">
          <T it="Divario Digitale e Crisi Abitativa" en="Digital Divide and Housing Crisis" />
        </h2>
        <p className="text-zinc-400 text-base sm:text-lg max-w-2xl mx-auto">
          <T 
            it="L'economia moderna richiede connettività e mobilità. Tuttavia, il divario infrastrutturale Nord-Sud e l'inaccessibilità degli alloggi bloccano l'emancipazione giovanile, esacerbando la fuga di cervelli." 
            en="The modern economy requires connectivity and mobility. However, the North-South infrastructure gap and housing unaffordability block youth emancipation, exacerbating the brain drain." 
          />
        </p>
      </motion.div>

      {/* CHARTS CONTAINER */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* DIGITAL DIVIDE CHART */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-6 relative overflow-hidden"
        >
          <div className="flex justify-between items-start mb-6">
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <Wifi size={20} className="text-cyan-400" />
                <T it="Divario Digitale per Area" en="Digital Divide by Area" />
              </h3>
              <p className="text-sm text-zinc-400 mt-1">
                <T it="Accesso banda larga vs Competenze digitali base" en="Broadband access vs Basic digital skills" />
              </p>
            </div>
            <SourceBadge agency="Eurostat" topicKey="eurostat_desi" />
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.digital_divide} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="region" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Bar 
                  dataKey="broadband_access_pct" 
                  name={isIt ? "Accesso Banda Larga" : "Broadband Access"} 
                  fill="#06b6d4" 
                  radius={[4, 4, 0, 0]} 
                />
                <Bar 
                  dataKey="digital_skills_pct" 
                  name={isIt ? "Competenze Base" : "Basic Skills"} 
                  fill="#3b82f6" 
                  radius={[4, 4, 0, 0]} 
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* HOUSING AFFORDABILITY CHART */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-6 relative overflow-hidden"
        >
          <div className="flex justify-between items-start mb-6">
            <div>
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <HomeIcon size={20} className="text-rose-400" />
                <T it="Crisi Abitativa e Autonomia" en="Housing Crisis and Autonomy" />
              </h3>
              <p className="text-sm text-zinc-400 mt-1">
                <T it="Sovraccarico affitto vs Giovani (18-34) coi genitori" en="Rent overburden vs Youth (18-34) with parents" />
              </p>
            </div>
            <SourceBadge agency="Eurostat" topicKey="eurostat_housing" />
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.housing_affordability} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRent" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorYouth" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="year" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 12 }} domain={[20, 80]} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Area 
                  type="monotone" 
                  dataKey="youth_with_parents_pct" 
                  name={isIt ? "Giovani in Casa" : "Youth w/ Parents"} 
                  stroke="#8b5cf6" 
                  fillOpacity={1} 
                  fill="url(#colorYouth)" 
                />
                <Area 
                  type="monotone" 
                  dataKey="rent_overburden_pct" 
                  name={isIt ? "Sovraccarico Affitto" : "Rent Overburden"} 
                  stroke="#f43f5e" 
                  fillOpacity={1} 
                  fill="url(#colorRent)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
      
    </div>
  );
}
