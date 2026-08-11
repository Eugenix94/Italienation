import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, Banknote, Users, Building, GraduationCap, ExternalLink } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LineChart,
  Line,
  AreaChart,
  Area,
  Legend,
  PieChart,
  Pie
} from 'recharts';
import { T } from './T';
import SourceBadge from './SourceBadge';
import collapseData from '../assets/systemic_collapse.json';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-zinc-900 border border-zinc-700 p-3 rounded-lg shadow-xl z-50">
        <p className="font-bold text-white mb-2">{label || payload[0].payload.country || payload[0].payload.year || payload[0].payload.category || payload[0].payload.metric}</p>
        {payload.map((entry, index) => (
          <p key={index} className="text-sm" style={{ color: entry.color || entry.fill }}>
            <span className="font-semibold">{entry.name}: </span>
            {entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function SystemicCollapse() {
  const { pnrr_education, youth_abstention, overeducation, school_infrastructure, demographic_winter } = collapseData;

  return (
    <div className="w-full text-white">
      {/* Header */}
      <div className="mb-12 text-center max-w-3xl mx-auto flex flex-col items-center">
        <h2 className="text-3xl md:text-5xl font-bold mb-4 flex items-center justify-center gap-3 text-center">
          <AlertTriangle className="w-10 h-10 text-rose-500" />
          <T it="Il Collasso di Sistema" en="The Systemic Collapse" />
        </h2>
        <p className="text-zinc-400 max-w-3xl text-lg mb-6 text-center">
          <T 
            it="Un'analisi delle traiettorie terminali del sistema Italia: dai fondi PNRR sprecati, al disimpegno politico giovanile, fino alla bomba a orologeria demografica che minaccia la tenuta stessa dello Stato sociale." 
            en="An analysis of the terminal trajectories of the Italian system: from wasted PNRR funds, to youth political disengagement, to the demographic time bomb threatening the very survival of the welfare state." 
          />
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* 1. PNRR Illusion */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <Banknote className="w-24 h-24 text-emerald-500" />
          </div>
          
          <div className="flex flex-col justify-between mb-6 gap-2 relative z-10">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <T it="L'Illusione PNRR (Scuola)" en="The PNRR Illusion (Education)" />
            </h3>
            <p className="text-zinc-400 text-xs">
              {pnrr_education.description}
            </p>
            <a 
              href={pnrr_education.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex w-max items-center gap-2 text-xs font-semibold bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded hover:bg-emerald-500/20 transition-colors mt-2"
            >
              <ExternalLink size={12} />
              OpenPNRR
            </a>
          </div>

          <div className="h-[250px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pnrr_education.data} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                <XAxis dataKey="category" tick={{ fill: '#a1a1aa', fontSize: 11 }} />
                <YAxis tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="allocated" name="Allocati (Mld €)" fill="#3f3f46" radius={[4, 4, 0, 0]} />
                <Bar dataKey="spent" name="Spesi (Mld €)" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* 2. Disenfranchised Youth */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <Users className="w-24 h-24 text-indigo-500" />
          </div>

          <div className="flex flex-col justify-between mb-6 gap-2 relative z-10">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <T it="L'Astensionismo Giovanile" en="Youth Disenfranchisement" />
            </h3>
            <p className="text-zinc-400 text-xs">
              {youth_abstention.description}
            </p>
            <a 
              href={youth_abstention.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex w-max items-center gap-2 text-xs font-semibold bg-indigo-500/10 text-indigo-400 px-2 py-1 rounded hover:bg-indigo-500/20 transition-colors mt-2"
            >
              <ExternalLink size={12} />
              Ministero dell'Interno
            </a>
          </div>

          <div className="h-[250px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={youth_abstention.data} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                <XAxis dataKey="year" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <YAxis tick={{ fill: '#a1a1aa', fontSize: 12 }} unit="%" />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line type="monotone" dataKey="turnout_pct" name="Affluenza 18-24enni" stroke="#6366f1" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="fuorisede_pct" name="Studenti Fuorisede (Barriera al Voto)" stroke="#f43f5e" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* 3. The Devalued Degree */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <GraduationCap className="w-24 h-24 text-amber-500" />
          </div>

          <div className="flex flex-col justify-between mb-6 gap-2 relative z-10">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <T it="La Svalutazione della Laurea" en="The Devalued Degree" />
            </h3>
            <p className="text-zinc-400 text-xs">
              {overeducation.description}
            </p>
            <a 
              href={overeducation.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex w-max items-center gap-2 text-xs font-semibold bg-amber-500/10 text-amber-400 px-2 py-1 rounded hover:bg-amber-500/20 transition-colors mt-2"
            >
              <ExternalLink size={12} />
              Eurostat lfsa_eoed
            </a>
          </div>

          <div className="h-[250px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={overeducation.data} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                <XAxis dataKey="country" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <YAxis yAxisId="left" tick={{ fill: '#a1a1aa', fontSize: 12 }} unit="%" domain={[0, 40]} />
                <YAxis yAxisId="right" orientation="right" tick={{ fill: '#f43f5e', fontSize: 12 }} unit="€" />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar yAxisId="left" dataKey="overeducation_pct" name="Tasso di Sovraistruzione" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                <Bar yAxisId="right" dataKey="wage_penalty_eur" name="Penalizzazione Salariale/Mese" fill="#f43f5e" radius={[0, 0, 4, 4]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* 4. Crumbling Infrastructure */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <Building className="w-24 h-24 text-rose-500" />
          </div>

          <div className="flex flex-col justify-between mb-6 gap-2 relative z-10">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <T it="Edilizia Scolastica al Collasso" en="Crumbling Infrastructure" />
            </h3>
            <p className="text-zinc-400 text-xs">
              {school_infrastructure.description}
            </p>
            <a 
              href={school_infrastructure.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex w-max items-center gap-2 text-xs font-semibold bg-rose-500/10 text-rose-400 px-2 py-1 rounded hover:bg-rose-500/20 transition-colors mt-2"
            >
              <ExternalLink size={12} />
              Legambiente (Ecosistema Scuola)
            </a>
          </div>

          <div className="h-[250px] w-full mt-4 flex justify-center items-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={school_infrastructure.data}
                  dataKey="value"
                  nameKey="metric"
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                >
                  {school_infrastructure.data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
                <Legend layout="vertical" verticalAlign="middle" align="right" wrapperStyle={{ fontSize: '11px', width: '40%' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* 5. Demographic Winter */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 lg:col-span-2 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <Users className="w-32 h-32 text-purple-500" />
          </div>

          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4 relative z-10">
            <div>
              <h3 className="text-2xl font-bold text-white flex items-center gap-2">
                <T it="L'Inverno Demografico (2020-2050)" en="The Demographic Winter (2020-2050)" />
              </h3>
              <p className="text-zinc-400 text-sm mt-1 max-w-2xl">
                {demographic_winter.description}
              </p>
            </div>
            <a 
              href={demographic_winter.source_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-xs font-semibold bg-purple-500/10 text-purple-400 px-3 py-1.5 rounded-lg hover:bg-purple-500/20 transition-colors border border-purple-500/20"
            >
              <ExternalLink size={14} />
              ISTAT DCIS_PREVDEM1
            </a>
          </div>

          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={demographic_winter.data} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                <XAxis dataKey="year" tick={{ fill: '#a1a1aa' }} />
                <YAxis tick={{ fill: '#a1a1aa' }} unit="M" />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="workers_mln" name="Popolazione Attiva (15-64) - Milioni" stackId="1" stroke="#a855f7" fill="#a855f7" fillOpacity={0.6} />
                <Area type="monotone" dataKey="retirees_mln" name="Pensionati (65+) - Milioni" stackId="2" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.6} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

      </div>
    </div>
  );
}
