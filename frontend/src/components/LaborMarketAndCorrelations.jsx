import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Briefcase, EyeOff, Link, Percent, BookDashed } from 'lucide-react';
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { T } from "./T";
import SectionContext from "./SectionContext";
import DataTooltip from "./DataTooltip";
import MethodologyAlert from "./MethodologyAlert";
import SourceBadge from './SourceBadge';

export default function LaborMarketAndCorrelations() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/labor_market_econometrics.json`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading labor market metrics:", err);
        setLoading(false);
      });
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-screen text-zinc-400 bg-zinc-950">
        <T it="Caricamento metriche del lavoro..." en="Loading labor market metrics..." />
      </div>
    );
  }

  const { tax_wedge, undeclared_work, correlations } = data;

  return (
    <div className="min-h-screen bg-zinc-950 text-white font-sans overflow-x-hidden pt-24 pb-16 px-6 lg:px-8">
      
      {/* Background ambient lighting */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-rose-600/5 rounded-full blur-[120px]" />
        <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-amber-500/5 rounded-full blur-[120px]" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm font-medium mb-6">
              <Briefcase size={16} />
              <T it="Dinamiche Macroeconomiche" en="Macroeconomic Dynamics" />
            </div>
            <h1 className="text-4xl sm:text-5xl font-black tracking-tight mb-6 bg-gradient-to-br from-white to-zinc-500 bg-clip-text text-transparent">
              <T it="Il Mercato del Lavoro" en="The Labor Market" />
            </h1>
            <p className="text-lg text-zinc-400 leading-relaxed">
              <T 
                it="Analisi del cuneo fiscale, dell'economia sommersa (lavoro nero) e delle correlazioni strutturali tra l'istruzione tracciata e la precarietà lavorativa." 
                en="Analysis of the tax wedge, the shadow economy (undeclared work), and the structural correlations between tracked education and labor precarity." 
              />
            </p>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          
          {/* Tax Wedge Card */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="bg-zinc-900/50 border border-white/10 backdrop-blur-md rounded-3xl p-8 hover:border-rose-500/30 transition-colors"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-rose-500/20 rounded-xl">
                <Percent className="text-rose-400" size={24} />
              </div>
              <div>
                <h3 className="text-xl font-bold"><T it="Cuneo Fiscale (Tax Wedge)" en="Tax Wedge" /></h3>
                <p className="text-sm text-zinc-400"><T it="Il peso del prelievo fiscale sul lavoro" en="The burden of labor taxation" /></p>
              </div>
            </div>
            <p className="text-sm text-zinc-300 mb-8">
              <T 
                it="L'Italia presenta uno dei cunei fiscali più alti dell'area OCSE (45.1%). Questo divario massiccio tra il costo aziendale e la busta paga netta disincentiva l'assunzione regolare dei giovani e alimenta il lavoro nero." 
                en="Italy has one of the highest tax wedges in the OECD area (45.1%). This massive gap between corporate cost and net paycheck disincentivizes regular youth hiring and fuels undeclared work." 
              />
            </p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={tax_wedge} layout="vertical" margin={{ top: 0, right: 30, left: 10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                  <XAxis type="number" domain={[0, 60]} tickFormatter={(val) => `${val}%`} stroke="#71717a" />
                  <YAxis dataKey="country" type="category" stroke="#d4d4d8" width={80} tick={{ fontSize: 13 }} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff' }}
                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                  />
                  <Bar dataKey="wedge_pct" radius={[0, 4, 4, 0]} barSize={20}>
                    {tax_wedge.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.country === 'Italia' ? '#f43f5e' : entry.isAverage ? '#6366f1' : '#52525b'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-6 flex justify-end">
              <SourceBadge agency="OECD" year="2023" />
            </div>
          </motion.div>

          {/* Lavoro Nero Card */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-zinc-900/50 border border-white/10 backdrop-blur-md rounded-3xl p-8 hover:border-amber-500/30 transition-colors"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-amber-500/20 rounded-xl">
                <EyeOff className="text-amber-400" size={24} />
              </div>
              <div>
                <h3 className="text-xl font-bold"><T it="Lavoro Irregolare (Nero)" en="Undeclared Work" /></h3>
                <p className="text-sm text-zinc-400"><T it="Tasso di irregolarità occupazionale" en="Occupational irregularity rate" /></p>
              </div>
            </div>
            <p className="text-sm text-zinc-300 mb-8">
              <T 
                it="L'economia sommersa assorbe quote spaventose di lavoro giovanile, precludendo tutele contrattuali e accumulazione contributiva pensionistica. Il fenomeno è drammaticamente concentrato nel Mezzogiorno." 
                en="The shadow economy absorbs frightening quotas of youth labor, precluding contractual protections and pension contribution accumulation. The phenomenon is dramatically concentrated in the South." 
              />
            </p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={undeclared_work} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="region" stroke="#71717a" tick={{ fontSize: 11 }} interval={0} />
                  <YAxis tickFormatter={(val) => `${val}%`} stroke="#71717a" />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff' }}
                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                  />
                  <Bar dataKey="irregularity_pct" radius={[4, 4, 0, 0]} barSize={40}>
                    {undeclared_work.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.irregularity_pct > 20 ? '#fbbf24' : '#52525b'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-6 flex justify-end">
              <SourceBadge agency="ISTAT" topicKey="shadow" year="2023" />
            </div>
          </motion.div>

        </div>

        
        {/* Il Precariato Card - Full Width */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.25 }}
          className="bg-zinc-900/50 border border-white/10 backdrop-blur-md rounded-3xl p-8 hover:border-indigo-500/30 transition-colors mb-8"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 bg-amber-500/20 rounded-xl">
              <BookDashed className="text-amber-400" size={24} />
            </div>
            <div>
              <h3 className="text-xl font-bold"><T it="Il Precariato Docenti" en="Teacher Precarity" /></h3>
              <p className="text-sm text-zinc-400"><T it="L'impatto della discontinuità didattica sugli studenti" en="The impact of pedagogical discontinuity on students" /></p>
            </div>
          </div>
          <p className="text-sm text-zinc-300 mb-8 max-w-4xl leading-relaxed">
            <T it={precariatoData.structuralIssue.it} en={precariatoData.structuralIssue.en} />
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
            <div className="bg-zinc-950 p-5 rounded-2xl border border-zinc-800">
              <p className="text-xs text-zinc-500 uppercase font-bold mb-2"><T it="Docenti Precari" en="Precarious Teachers" /></p>
              <div className="flex items-end gap-2">
                <p className="text-3xl font-black text-amber-400">{(precariatoData.precariousTeachers / 1000)}K</p>
                <p className="text-sm font-bold text-amber-400/50 mb-1">({precariatoData.precariousPercentage}%)</p>
              </div>
            </div>
            <div className="bg-zinc-950 p-5 rounded-2xl border border-zinc-800 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-16 h-16 bg-emerald-500/10 blur-xl" />
              <p className="text-xs text-zinc-500 uppercase font-bold mb-2"><T it="Media Europea" en="EU Average" /></p>
              <div className="flex items-end gap-2">
                <p className="text-3xl font-black text-emerald-400">{precariatoData.euPrecariousPercentage}%</p>
              </div>
            </div>
            <div className="bg-zinc-950 p-5 rounded-2xl border border-zinc-800">
              <p className="text-xs text-zinc-500 uppercase font-bold mb-2"><T it="Età Media" en="Average Age" /></p>
              <div className="flex items-end gap-2">
                <p className="text-3xl font-black text-rose-400">{precariatoData.averageAge}</p>
                <p className="text-sm font-bold text-rose-400/50 mb-1">anni</p>
              </div>
            </div>
            <div className="bg-zinc-950 p-5 rounded-2xl border border-zinc-800 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-16 h-16 bg-emerald-500/10 blur-xl" />
              <p className="text-xs text-zinc-500 uppercase font-bold mb-2"><T it="Età Media EU" en="EU Average Age" /></p>
              <div className="flex items-end gap-2">
                <p className="text-3xl font-black text-emerald-400">{precariatoData.euAverageAge}</p>
                <p className="text-sm font-bold text-emerald-400/50 mb-1">anni</p>
              </div>
            </div>
          </div>
          
          <div className="bg-amber-950/20 border border-amber-900/30 rounded-xl p-4 flex items-center justify-between">
            <span className="text-amber-200 font-medium text-sm"><T it="Anni di continuità didattica media per studente (Stima):" en="Average years of teaching continuity per student (Est):" /></span>
            <span className="text-xl font-black text-amber-400">{precariatoData.averageContinuityYears} <span className="text-sm font-normal text-amber-400/60">anni / years</span></span>
          </div>

        </motion.div>

        {/* Correlations Card - Full Width */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="bg-zinc-900/50 border border-white/10 backdrop-blur-md rounded-3xl p-8 hover:border-indigo-500/30 transition-colors"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 bg-indigo-500/20 rounded-xl">
              <Link className="text-indigo-400" size={24} />
            </div>
            <div>
              <h3 className="text-xl font-bold"><T it="Correlazioni Econometriche" en="Econometric Correlations" /></h3>
              <p className="text-sm text-zinc-400"><T it="Impatto del tracciamento scolastico sul mercato del lavoro (Indice di Pearson)" en="Impact of school tracking on the labor market (Pearson Index)" /></p>
            </div>
          </div>
          <p className="text-sm text-zinc-300 mb-8 max-w-4xl">
            <T 
              it="L'analisi della matrice di correlazione di Pearson rivela un legame matematico inequivocabile: l'iscrizione a percorsi Tecnici/Professionali correla positivamente (+0.45) con l'assunzione precaria (contratti a termine under-30) e con la ricaduta nell'inattività (+0.45), dimostrando il fallimento della retorica 'studia per lavorare'." 
              en="Analysis of the Pearson correlation matrix reveals an unequivocal mathematical link: enrollment in Technical/Vocational tracks correlates positively (+0.45) with precarious hiring (under-30 fixed-term contracts) and with relapse into inactivity (+0.45), proving the failure of the 'study to work' rhetoric." 
            />
          </p>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={correlations} layout="vertical" margin={{ top: 0, right: 30, left: 100, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                <XAxis type="number" domain={[-1, 1]} stroke="#71717a" />
                <YAxis dataKey="factor" type="category" stroke="#d4d4d8" width={180} tick={{ fontSize: 13 }} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', borderRadius: '8px' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                />
                <ReferenceLine x={0} stroke="#71717a" />
                <Bar name="Correlazione Precariato" dataKey="correlation_precarious" fill="#ef4444" radius={[0, 4, 4, 0]} barSize={12} />
                <Bar name="Correlazione Inattività" dataKey="correlation_inactivity" fill="#f59e0b" radius={[0, 4, 4, 0]} barSize={12} />
                <Bar name="Correlazione Rischio NEET" dataKey="correlation_neet" fill="#6366f1" radius={[0, 4, 4, 0]} barSize={12} />
              </BarChart>
            </ResponsiveContainer>
          </div>
            <div className="flex justify-center gap-6 mt-4 text-xs">
              <span className="flex items-center gap-2"><div className="w-3 h-3 bg-red-500 rounded-full"/>Precariato (Contratti a termine)</span>
              <span className="flex items-center gap-2"><div className="w-3 h-3 bg-amber-500 rounded-full"/>Ricaduta Inattività</span>
              <span className="flex items-center gap-2"><div className="w-3 h-3 bg-indigo-500 rounded-full"/>Rischio NEET</span>
            </div>
            <div className="mt-6 flex justify-end">
              <SourceBadge agency="ISTAT" topicKey="mismatch" year="2023" />
            </div>
          </motion.div>
      </div>
    </div>
  );
}
