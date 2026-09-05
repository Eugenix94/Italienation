import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { RotateCcw, AlertTriangle, Euro } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';

export default function GradeRetention() {
  const { lang } = useLanguage();
  const isIt = lang === 'it';

  const data = useMemo(() => [
    {
      id: 'liceo',
      name_it: 'Liceo',
      name_en: 'Liceo (Academic)',
      rate: 3.8,
      color: '#818cf8', // indigo-400
    },
    {
      id: 'tecnico',
      name_it: 'Ist. Tecnico',
      name_en: 'Technical Inst.',
      rate: 10.2,
      color: '#fbbf24', // amber-400
    },
    {
      id: 'professionale',
      name_it: 'Ist. Professionale',
      name_en: 'Vocational Inst.',
      rate: 18.4,
      color: '#f43f5e', // rose-500
    }
  ], []);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-zinc-900/95 border border-zinc-700/50 p-4 rounded-xl shadow-2xl backdrop-blur-xl">
          <p className="font-bold text-white mb-1">
            {isIt ? data.name_it : data.name_en}
          </p>
          <div className="flex items-center gap-2 text-rose-400 font-mono text-lg">
            <RotateCcw size={16} />
            <span>{data.rate}% <T it="Bocciati (1° anno)" en="Retained (1st year)" /></span>
          </div>
          <p className="text-zinc-400 text-xs mt-2 max-w-[200px]">
            {data.id === 'professionale' && (isIt ? "Quasi 1 studente su 5 perde l'anno, con altissimo rischio di abbandono." : "Almost 1 in 5 students lose the year, with very high dropout risk.")}
            {data.id === 'liceo' && (isIt ? "Tasso in linea con la media europea (3%)." : "Rate in line with the EU average (3%).")}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full max-w-7xl mx-auto space-y-12">
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs font-semibold uppercase tracking-wider">
          <AlertTriangle size={14} />
          <T it="Dispersione Scolastica" en="School Dropout Risk" />
        </div>
        <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
          <T it="La Fabbrica delle Bocciature" en="The Grade Retention Factory" />
        </h2>
        <p className="text-zinc-400 text-sm sm:text-base leading-relaxed max-w-3xl mx-auto">
          <T 
            it="L'Italia è uno dei pochi Paesi UE ad abusare della bocciatura (grade retention) come strumento punitivo. Costo sistemico: ~€1.8 Miliardi all'anno. I dati del primo anno scolastico (MIUR) mostrano un chiaro pregiudizio di classe: il tasso di bocciatura negli Istituti Professionali è quasi 5 volte superiore a quello dei Licei."
            en="Italy is one of the few EU countries that heavily abuses grade retention as a punitive tool. Systemic cost: ~€1.8 Billion per year. First-year data (MIUR) shows a clear class bias: the retention rate in Vocational schools is almost 5 times higher than in Academic Licei."
          />
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* CHART PORTION */}
        <div className="col-span-1 lg:col-span-2 bg-zinc-900/50 border border-zinc-800/50 rounded-2xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <RotateCcw size={120} />
          </div>
          <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
            <T it="Tasso di Bocciatura (1° Anno Superiore)" en="Retention Rate (1st Year High School)" />
          </h3>
          
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data}
                layout="vertical"
                margin={{ top: 20, right: 30, left: 40, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" horizontal={true} vertical={false} opacity={0.5} />
                <XAxis type="number" domain={[0, 25]} tick={{fill: '#a1a1aa'}} stroke="#52525b" tickFormatter={(v) => `${v}%`} />
                <YAxis dataKey={isIt ? 'name_it' : 'name_en'} type="category" tick={{fill: '#e4e4e7', fontWeight: 600}} stroke="#52525b" width={120} />
                <Tooltip content={<CustomTooltip />} cursor={{fill: 'rgba(255,255,255,0.02)'}} />
                
                {/* Reference line for EU average */}
                <ReferenceLine x={3.0} stroke="#22d3ee" strokeDasharray="3 3" label={{ position: 'top', value: isIt ? 'Media UE (~3%)' : 'EU Avg (~3%)', fill: '#22d3ee', fontSize: 12 }} />

                <Bar dataKey="rate" radius={[0, 6, 6, 0]} maxBarSize={60}>
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="mt-4 flex justify-between items-center text-xs text-zinc-500">
            <span>Source: Ministero dell'Istruzione (MIM), Open Data 2024</span>
            <div className="flex items-center gap-1 text-rose-400/80">
              <Euro size={14} />
              <span>~€12,000 <T it="costo per studente trattenuto" en="cost per retained student" /></span>
            </div>
          </div>
        </div>

        {/* ANALYSIS PORTION */}
        <div className="col-span-1 flex flex-col justify-center space-y-6 bg-rose-500/5 border border-rose-500/20 rounded-2xl p-6">
          <div className="space-y-2">
            <h4 className="font-bold text-rose-400 text-lg flex items-center gap-2">
              <AlertTriangle size={18} />
              <T it="L'Effetto Cicatrice" en="The Scarring Effect" />
            </h4>
            <p className="text-zinc-300 text-sm leading-relaxed">
              <T 
                it="La bocciatura è statisticamente il principale predittore dell'abbandono scolastico precoce. Invece di 'recuperare', il 70% dei bocciati al professionale abbandonerà la scuola entro il terzo anno." 
                en="Grade retention is statistically the main predictor of early school leaving. Instead of 'catching up', 70% of those retained in vocational schools will drop out by their third year." 
              />
            </p>
          </div>

          <div className="space-y-2">
            <h4 className="font-bold text-rose-400 text-lg flex items-center gap-2">
              <Euro size={18} />
              <T it="Il Costo Nascosto" en="The Hidden Cost" />
            </h4>
            <p className="text-zinc-300 text-sm leading-relaxed">
              <T 
                it="150.000 bocciature all'anno costano allo Stato ~1.8 Miliardi di Euro per finanziare un anno extra di docenza, infrastrutture e ritardato ingresso nel mercato del lavoro." 
                en="150,000 retentions per year cost the State ~1.8 Billion Euros to fund an extra year of teaching, infrastructure, and delayed entry into the labor market." 
              />
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}
