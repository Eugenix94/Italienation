import React from 'react';
import { ComposedChart, Bar, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';
import { T } from './T';
import SourceBadge from './SourceBadge';
import eurydiceData from '../assets/master_eurydice_comparison.json';

import { useLanguage } from '../contexts/LanguageContext';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-zinc-900 border border-zinc-700 p-4 rounded-lg shadow-xl">
        <p className="font-bold text-white mb-2">{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color || entry.fill }} className="text-sm font-medium">
            {entry.name}: {entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function InternationalBenchmark() {
  const { lang } = useLanguage();
  const isIt = lang === 'it';

  return (
    <div className="space-y-8">
      <div className="text-center max-w-3xl mx-auto mb-8">
        <h2 className="text-3xl font-bold text-white mb-4">
          <T it="Benchmark Internazionale (Eurydice)" en="International Benchmark (Eurydice)" />
        </h2>
        <p className="text-zinc-400 text-lg">
          <T 
            it="Comparazione europea sull'età di tracking (smistamento) e il relativo impatto sui tassi di dispersione (NEET)." 
            en="European comparison of tracking age and its associated impact on dropout rates (NEET)." 
          />
        </p>
        <p className="text-zinc-300 mt-4 leading-relaxed text-center">
          <T
            it="Il 'tracking age' è l'età in cui un sistema scolastico smista per la prima volta gli studenti in percorsi diversi (es. liceo, tecnico, professionale). La ricerca mostra che un tracking precoce è fortemente correlato a maggiore disuguaglianza e dispersione."
            en="'Tracking age' is the age at which a school system first sorts students into different paths (e.g., academic, technical, vocational). Research shows that early tracking strongly correlates with higher inequality and dropout rates."
          />
        </p>
      </div>
      <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl w-full">
        <div className="flex justify-end mb-4">
           <SourceBadge agency="Eurydice / Eurostat" year="2022" url="https://eurydice.eacea.ec.europa.eu/publications/teachers-and-school-heads-salaries-and-allowances-europe-20212022" />
        </div>
        <div className="h-[500px]">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={eurydiceData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
              <XAxis dataKey="Country" stroke="#888" />
              <YAxis yAxisId="left" stroke="#888" label={{ value: isIt ? 'Età di Tracking' : 'Tracking Age', angle: -90, position: 'insideLeft', fill: '#888' }} />
              <YAxis yAxisId="right" orientation="right" stroke="#f43f5e" label={{ value: isIt ? 'Tasso NEET (%)' : 'NEET Rate (%)', angle: 90, position: 'insideRight', fill: '#f43f5e' }} />
              <RechartsTooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Bar yAxisId="left" dataKey="TrackingAge" name={isIt ? "Età di Tracking (Anni)" : "Tracking Age (Years)"} fill="#4f46e5" radius={[4, 4, 0, 0]} />
              <Line yAxisId="right" type="monotone" dataKey="NEETRate_15_29" name={isIt ? "Tasso NEET (%)" : "NEET Rate (%)"} stroke="#f43f5e" strokeWidth={4} dot={{ r: 6 }} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      <div className="bg-indigo-500/10 border border-indigo-500/20 p-6 rounded-2xl mt-8">
        <h4 className="text-indigo-400 font-bold mb-2">
          <T it="Dato Chiave" en="Key Insight" />
        </h4>
        <p className="text-zinc-300">
          <T
            it="L'Italia smista gli studenti a 14 anni — tra i primissimi in Europa. I paesi che posticipano il tracking a 16+ anni (Finlandia, Svezia) hanno costantemente tassi di NEET inferiori e una maggiore mobilità sociale."
            en="Italy tracks students at age 14 — among the earliest in Europe. Countries that delay tracking until 16+ (Finland, Sweden) consistently have lower NEET rates and higher social mobility."
          />
        </p>
      </div>
    </div>
  );
}
