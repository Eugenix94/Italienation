import React from 'react';
import { motion } from 'framer-motion';
import { BrainCircuit, Home, Baby, ExternalLink } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
  ScatterChart,
  Scatter,
  ZAxis
} from 'recharts';
import { T } from './T';
import SourceBadge from './SourceBadge';
import falloutData from '../assets/demographic_fallout.json';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-zinc-900 border border-zinc-700 p-3 rounded-lg shadow-xl">
        <p className="font-bold text-white mb-2">{label || payload[0].payload.country || payload[0].payload.region}</p>
        {payload.map((entry, index) => (
          <p key={index} className="text-sm" style={{ color: entry.color || entry.fill }}>
            <span className="font-semibold">{entry.name}: </span>
            {entry.value}%
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function DemographicFallout() {
  const { anxiety_pisa, housing_overburden, motherhood_penalty } = falloutData;

  return (
    <div className="w-full text-white">
      {/* Header */}
      <div className="mb-12">
        <h2 className="text-3xl md:text-5xl font-bold mb-4 flex items-center gap-3">
          <BrainCircuit className="w-10 h-10 text-rose-500" />
          <T it="Ricadute Sociali e Demografiche" en="Social & Demographic Fallout" />
        </h2>
        <p className="text-zinc-300 max-w-3xl text-lg">
          <T 
            it="Un sistema educativo e lavorativo disfunzionale non produce solo danni economici, ma genera profonde fratture sociali. Dall'ansia scolastica, all'impossibilità di emancipazione abitativa, fino alla penalizzazione strutturale della maternità." 
            en="A dysfunctional educational and labor system doesn't just produce economic damage; it generates deep social fractures. From school anxiety, to the impossibility of housing emancipation, to the structural penalty of motherhood." 
          />
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        
        {/* 1. Mental Health (OECD PISA) */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 lg:col-span-2 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <BrainCircuit className="w-32 h-32 text-rose-500" />
          </div>
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4 relative z-10">
            <div>
              <h3 className="text-2xl font-bold text-white flex items-center gap-2">
                <T it="L'Ansia da Prestazione (PISA)" en="Performance Anxiety (PISA)" />
              </h3>
              <p className="text-zinc-300 text-sm mt-1 max-w-2xl">
                {anxiety_pisa.description}
              </p>
            </div>
            <a 
              href={anxiety_pisa.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm font-semibold bg-rose-500/10 text-rose-400 px-3 py-1.5 rounded-lg hover:bg-rose-500/20 transition-colors border border-rose-500/20"
            >
              <ExternalLink size={14} />
              OECD PISA Well-being
            </a>
          </div>

          <div className="h-[380px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={anxiety_pisa.data} layout="vertical" margin={{ top: 20, right: 30, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" horizontal={false} />
                <XAxis type="number" domain={[0, 70]} tick={{ fill: '#a1a1aa' }} unit="%" />
                <YAxis dataKey="country" type="category" tick={{ fill: '#e4e4e7', fontWeight: 600 }} width={80} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="anxiety_pct" name="Students Reporting High Anxiety" radius={[0, 4, 4, 0]} barSize={32}>
                  {anxiety_pisa.data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.country === 'Italy' ? '#f43f5e' : entry.country === 'OECD Avg' ? '#6366f1' : '#3f3f46'} />
                  ))}
                </Bar>
                <ReferenceLine x={37} stroke="#6366f1" strokeDasharray="3 3" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* 2. Housing Overburden (Eurostat) */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <Home className="w-24 h-24 text-amber-500" />
          </div>

          <div className="flex flex-col justify-between mb-8 gap-2 relative z-10">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <T it="Crisi Abitativa Giovanile" en="Youth Housing Crisis" />
            </h3>
            <p className="text-zinc-300 text-sm">
              {housing_overburden.description}
            </p>
            <a 
              href={housing_overburden.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex w-max items-center gap-2 text-sm font-semibold bg-amber-500/10 text-amber-400 px-2 py-1 rounded hover:bg-amber-500/20 transition-colors mt-2"
            >
              <ExternalLink size={12} />
              Eurostat ilc_lvho07a
            </a>
          </div>

          <div className="h-[350px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={housing_overburden.data} margin={{ top: 10, right: 10, left: -20, bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                <XAxis dataKey="country" tick={{ fill: '#a1a1aa', fontSize: 12 }} angle={-45} textAnchor="end" />
                <YAxis tick={{ fill: '#a1a1aa', fontSize: 12 }} unit="%" />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="overburden_pct" name="Housing Overburden Rate" radius={[4, 4, 0, 0]}>
                  {housing_overburden.data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.country === 'Italy' ? '#f59e0b' : entry.country === 'EU Avg' ? '#6366f1' : '#3f3f46'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* 3. Motherhood Penalty (ISTAT) */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <Baby className="w-24 h-24 text-emerald-500" />
          </div>

          <div className="flex flex-col justify-between mb-8 gap-2 relative z-10">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <T it="Penalizzazione della Maternità" en="The Motherhood Penalty" />
            </h3>
            <p className="text-zinc-300 text-sm">
              {motherhood_penalty.description}
            </p>
            <a 
              href={motherhood_penalty.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex w-max items-center gap-2 text-sm font-semibold bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded hover:bg-emerald-500/20 transition-colors mt-2"
            >
              <ExternalLink size={12} />
              ISTAT Rapporto Annuale
            </a>
          </div>

          <div className="h-[350px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={motherhood_penalty.data} margin={{ top: 10, right: 10, left: -20, bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                <XAxis dataKey="region" tick={{ fill: '#a1a1aa', fontSize: 12 }} angle={-45} textAnchor="end" />
                <YAxis tick={{ fill: '#a1a1aa', fontSize: 12 }} unit="%" domain={[0, 80]} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="female_emp_pct" name="Tasso Occupazione Femminile" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="tempo_pieno_coverage" name="Copertura Tempo Pieno" fill="#3f3f46" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="mt-8 bg-zinc-800/50 border border-emerald-500/30 p-4 rounded-xl">
            <p className="text-emerald-400 font-semibold text-sm mb-1">
              <T it="💡 Punto Chiave" en="💡 Key Insight" />
            </p>
            <p className="text-zinc-300 text-sm">
              <T 
                it="Nel Sud Italia, solo il 35% delle madri ha un'occupazione contro il 65% del Nord. La mancanza di infrastrutture per il tempo pieno a scuola costringe le donne a scegliere tra carriera e famiglia — un problema strutturale, non culturale." 
                en="In Southern Italy, only 35% of mothers are employed vs 65% in the North. The lack of full-time school (tempo pieno) infrastructure forces women to choose between career and family — a structural, not cultural, problem." 
              />
            </p>
          </div>
        </motion.div>

      </div>
    </div>
  );
}
