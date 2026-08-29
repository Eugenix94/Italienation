import React from 'react';
import { motion } from 'framer-motion';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, PieChart, Pie } from 'recharts';
import { Target, Clock, AlertTriangle, CheckCircle2, Euro, GraduationCap, Building2, Eye, TrendingUp } from 'lucide-react';
import SourceBadge from './SourceBadge';
import data from '../assets/pnrr_tracker.json';

const PNRRTracker = () => {
  const { lang } = useLanguage();
  const isIt = lang === 'it';

  const fp = data.financial_progress;
  const ed = data.education_focus;
  const ms = data.milestones;

  const missionData = data.allocation_by_mission.map(m => ({
    name: isIt ? m.name_it : m.name_en,
    shortName: m.id,
    value: m.eur_bn,
    color: m.color
  }));

  const spendingData = [
    { name: isIt ? 'Speso' : 'Spent', value: fp.spent_eur_bn, color: '#10b981' },
    { name: isIt ? 'Ricevuto (non speso)' : 'Received (unspent)', value: fp.received_from_eu_eur_bn - fp.spent_eur_bn, color: '#6366f1' },
    { name: isIt ? 'Da ricevere' : 'Remaining', value: fp.total_allocated_eur_bn - fp.received_from_eu_eur_bn, color: '#64748b' }
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload?.length) return null;
    const d = payload[0].payload;
    return (
      <div className="bg-zinc-900 border border-zinc-700 rounded-xl px-4 py-3 shadow-2xl text-sm">
        <p className="font-bold text-white">{d.name}</p>
        <p className="text-zinc-300">€{d.value.toFixed(1)} {isIt ? 'Mld' : 'B'}</p>
      </div>
    );
  };

  // Calculate days remaining
  const deadline = new Date('2026-08-31');
  const now = new Date();
  const daysRemaining = Math.max(0, Math.ceil((deadline - now) / (1000 * 60 * 60 * 24)));

  return (
    <div className="space-y-16">
      {/* HEADER */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-emerald-500/10 rounded-2xl"><Target className="text-emerald-400" size={28} /></div>
          <div>
            <h2 className="text-3xl font-black text-white">
              <T it="PNRR — Tracker di Esecuzione" en="PNRR — Execution Tracker" />
            </h2>
            <p className="text-zinc-400 text-sm mt-1">
              <T it="Piano Nazionale di Ripresa e Resilienza — €194,4 miliardi" en="National Recovery and Resilience Plan — €194.4 billion" />
            </p>
          </div>
        </div>
      </motion.div>

      {/* DEADLINE BANNER */}
      <motion.div initial={{ opacity: 0, scale: 0.95 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }}
        className="bg-gradient-to-r from-rose-500/10 via-amber-500/10 to-rose-500/10 border border-rose-500/30 rounded-2xl p-6"
      >
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertTriangle className="text-amber-400" size={24} />
            <div>
              <p className="text-white font-bold text-lg">
                <T it="SCADENZA DEFINITIVA: 31 Agosto 2026" en="FINAL DEADLINE: August 31, 2026" />
              </p>
              <p className="text-zinc-300 text-sm">
                <T it="Nessun nuovo progetto può essere proposto. Fase di chiusura cantieri in corso." en="No new projects can be proposed. Construction site closure phase underway." />
              </p>
            </div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-black text-amber-400">{daysRemaining}</div>
            <div className="text-xs text-zinc-400 uppercase tracking-wider"><T it="Giorni Rimasti" en="Days Left" /></div>
          </div>
        </div>
      </motion.div>

      {/* KEY METRICS */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { value: `€${fp.total_allocated_eur_bn}B`, label: isIt ? 'Allocazione Totale' : 'Total Allocation', icon: Euro, color: 'text-white', bg: 'bg-zinc-800' },
          { value: `€${fp.spent_eur_bn}B+`, label: isIt ? 'Speso (41%)' : 'Spent (41%)', icon: TrendingUp, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
          { value: `${ms.achieved_pct}%`, label: isIt ? 'Traguardi Raggiunti' : 'Milestones Achieved', icon: CheckCircle2, color: 'text-blue-400', bg: 'bg-blue-500/10' },
          { value: `${(fp.active_construction_sites/1000).toFixed(0)}k`, label: isIt ? 'Cantieri Attivi' : 'Active Sites', icon: Building2, color: 'text-amber-400', bg: 'bg-amber-500/10' }
        ].map((m, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }}
            className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-5"
          >
            <div className={`${m.bg} w-10 h-10 rounded-xl flex items-center justify-center mb-3`}>
              <m.icon className={m.color} size={20} />
            </div>
            <div className={`text-2xl font-black ${m.color}`}>{m.value}</div>
            <div className="text-xs text-zinc-400 mt-1">{m.label}</div>
          </motion.div>
        ))}
      </div>

      {/* ALLOCATION BY MISSION + SPENDING DONUT */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* MISSION BARS */}
        <motion.div initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
        >
          <h3 className="text-xl font-bold text-white mb-6">
            <T it="Allocazione per Missione" en="Allocation by Mission" />
          </h3>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={missionData} layout="vertical" margin={{ left: 10, right: 20, top: 5, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
              <XAxis type="number" tick={{ fill: '#a1a1aa', fontSize: 12 }} stroke="#3f3f46" tickFormatter={v => `€${v}B`} />
              <YAxis type="category" dataKey="shortName" tick={{ fill: '#d4d4d8', fontSize: 13, fontWeight: 700 }} stroke="#3f3f46" width={35} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" radius={[0, 8, 8, 0]}>
                {missionData.map((entry, i) => <Cell key={i} fill={entry.color} fillOpacity={0.85} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-2 mt-4">
            {data.allocation_by_mission.map((m, i) => (
              <span key={i} className="flex items-center gap-1.5 text-[11px] text-zinc-400">
                <span className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: m.color }} />
                {m.id}: {isIt ? m.name_it.split(',')[0] : m.name_en.split(',')[0]}
              </span>
            ))}
          </div>
        </motion.div>

        {/* SPENDING DONUT */}
        <motion.div initial={{ opacity: 0, x: 20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
        >
          <h3 className="text-xl font-bold text-white mb-6">
            <T it="Stato della Spesa" en="Spending Status" />
          </h3>
          <div className="flex flex-col items-center">
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={spendingData} cx="50%" cy="50%" innerRadius={70} outerRadius={110} paddingAngle={3} dataKey="value" startAngle={90} endAngle={-270}>
                  {spendingData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
            <div className="text-center -mt-4">
              <div className="text-3xl font-black text-emerald-400">€{fp.spent_eur_bn}B+</div>
              <div className="text-sm text-zinc-400"><T it="su €194,4 Mld allocati" en="of €194.4B allocated" /></div>
            </div>
            <div className="flex flex-wrap justify-center gap-4 mt-4">
              {spendingData.map((s, i) => (
                <span key={i} className="flex items-center gap-1.5 text-xs text-zinc-400">
                  <span className="w-3 h-3 rounded-sm" style={{ backgroundColor: s.color }} />
                  {s.name}: €{s.value.toFixed(1)}B
                </span>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* EDUCATION FOCUS */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="bg-gradient-to-br from-purple-500/5 to-indigo-500/5 border border-purple-500/20 rounded-3xl p-8"
      >
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-6">
          <GraduationCap className="text-purple-400" size={22} />
          <T it="Focus: Istruzione & Povertà Educativa" en="Focus: Education & Educational Poverty" />
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-3xl font-black text-purple-400">€{ed.total_m4_education_eur_bn}B</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Missione 4 — Totale Istruzione" en="Mission 4 — Total Education" /></div>
          </div>
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-3xl font-black text-amber-400">€{ed.nurseries_preschool_0_6_eur_bn}B</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Asili Nido & Materne (0-6 anni)" en="Nurseries & Preschools (0-6 years)" /></div>
          </div>
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-3xl font-black text-rose-400">€{ed.combating_dropout_poverty_eur_bn}B</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Contrasto Dispersione Scolastica" en="Combating School Dropout" /></div>
          </div>
        </div>
        <p className="text-sm text-zinc-300 leading-relaxed">
          {isIt ? ed.description_it : ed.description_en}
        </p>
      </motion.div>

      {/* MILESTONES */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
      >
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-6">
          <CheckCircle2 className="text-blue-400" size={22} />
          <T it="Stato Traguardi & Obiettivi" en="Milestones & Targets Status" />
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-4xl font-black text-blue-400">{ms.achieved_pct}%</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Raggiunti" en="Achieved" /></div>
          </div>
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-4xl font-black text-amber-400">{ms.measures_removed_replaced}</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Misure Rimosse/Sostituite" en="Measures Removed/Replaced" /></div>
          </div>
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-4xl font-black text-indigo-400">{ms.measures_technically_revised}</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Revisioni Tecniche" en="Technical Revisions" /></div>
          </div>
        </div>
        <p className="text-sm text-zinc-300 leading-relaxed">
          {isIt ? ms.description_it : ms.description_en}
        </p>
      </motion.div>

      {/* TIMELINE */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
      >
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-6">
          <Clock className="text-amber-400" size={22} />
          <T it="Timeline PNRR" en="PNRR Timeline" />
        </h3>
        <div className="relative">
          <div className="absolute left-4 top-0 bottom-0 w-px bg-zinc-700" />
          <div className="space-y-6">
            {data.timeline.map((event, i) => {
              const isPast = new Date(event.date + '-01') <= now;
              const isFinal = i === data.timeline.length - 1;
              return (
                <div key={i} className="relative pl-12">
                  <div className={`absolute left-2.5 w-3 h-3 rounded-full border-2 ${isFinal ? 'bg-rose-500 border-rose-400' : isPast ? 'bg-emerald-500 border-emerald-400' : 'bg-zinc-700 border-zinc-600'}`} />
                  <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4">
                    <span className={`text-xs font-mono font-bold ${isFinal ? 'text-rose-400' : isPast ? 'text-emerald-400' : 'text-zinc-400'}`}>{event.date}</span>
                    <span className={`text-sm ${isFinal ? 'text-rose-300 font-bold' : 'text-zinc-300'}`}>
                      {isIt ? event.event_it : event.event_en}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </motion.div>

      {/* EU OVERSIGHT */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="bg-gradient-to-br from-blue-500/5 to-cyan-500/5 border border-blue-500/20 rounded-3xl p-8"
      >
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-4">
          <Eye className="text-blue-400" size={22} />
          <T it="Sorveglianza & Oversight" en="Oversight & Monitoring" />
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <div className="text-xs text-blue-400 uppercase tracking-wider font-bold"><T it="Livello UE" en="EU Level" /></div>
            <p className="text-sm text-zinc-300 leading-relaxed">{isIt ? data.oversight.eu_mechanism_it : data.oversight.eu_mechanism_en}</p>
          </div>
          <div className="space-y-3">
            <div className="text-xs text-cyan-400 uppercase tracking-wider font-bold"><T it="Livello Nazionale" en="National Level" /></div>
            <p className="text-sm text-zinc-300 leading-relaxed">{isIt ? data.oversight.national_mechanism_it : data.oversight.national_mechanism_en}</p>
          </div>
        </div>
        {/* WARNING */}
        <div className="mt-6 p-4 bg-amber-500/5 border border-amber-500/20 rounded-xl">
          <div className="flex items-start gap-3">
            <AlertTriangle className="text-amber-400 mt-0.5 flex-shrink-0" size={18} />
            <p className="text-sm text-zinc-300 leading-relaxed">
              {isIt ? data.warnings.spending_gap_it : data.warnings.spending_gap_en}
            </p>
          </div>
        </div>
      </motion.div>

      {/* SOURCE BADGES */}
      <div className="flex flex-wrap gap-3">
        <SourceBadge label="Italia Domani" topicKey="italia_domani" />
        <SourceBadge label="Corte dei Conti" agency="Corte dei Conti" />
        <SourceBadge label="OpenPNRR" topicKey="openpnrr_openpolis" />
        <SourceBadge label="EU Commission RRF" topicKey="eu_commission_rrf" />
      </div>
    </div>
  );
};

export default PNRRTracker;
