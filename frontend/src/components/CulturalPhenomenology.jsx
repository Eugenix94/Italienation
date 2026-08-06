import React, { useState, useEffect } from 'react';
import { T } from './T';
import SourceBadge from './SourceBadge';
import { motion } from 'framer-motion';
import { MessageCircle, Users, Scale, Briefcase, GraduationCap } from 'lucide-react';
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, Radar, LineChart, Line } from 'recharts';

export default function CulturalPhenomenology() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/cultural_metrics.json`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading cultural metrics:", err);
        setLoading(false);
      });
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-64 text-zinc-500">
        <T it="Caricamento metriche culturali..." en="Loading cultural metrics..." />
      </div>
    );
  }

  const { nepotism_perception, oral_exams_variance, social_mobility_index, first_job_connections } = data;

  return (
    <div className="space-y-16 relative">
      
      {/* Glow Effects */}
      <div className="absolute top-1/2 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute top-1/2 right-1/4 w-96 h-96 bg-rose-500/5 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-0 left-1/2 w-[800px] h-[400px] bg-emerald-500/5 rounded-full blur-[120px] pointer-events-none -translate-x-1/2" />

      <div className="text-center max-w-3xl mx-auto relative z-10">
        <h3 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-zinc-400 mb-6 tracking-tight">
          <T it="Fenomenologia Culturale" en="Cultural Phenomenology" />
        </h3>
        <p className="text-zinc-400 text-lg leading-relaxed">
          <T 
            it="L'impatto dei meccanismi culturali non scritti: dalle valutazioni soggettive (interrogazioni) al deficit di meritocrazia strutturale, fino all'immobilità sociale." 
            en="The impact of unwritten cultural mechanisms: from subjective evaluations (oral exams) to the structural meritocracy deficit and social immobility." 
          />
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative z-10">
        
        {/* 1. Oral Exams Card */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="group bg-gradient-to-br from-white/[0.05] to-transparent border border-white/10 backdrop-blur-2xl rounded-3xl p-8 hover:border-indigo-500/40 hover:shadow-[0_0_40px_rgba(99,102,241,0.15)] hover:-translate-y-1 transition-all duration-500"
        >
          <div className="flex items-center gap-5 mb-8">
            <div className="p-4 bg-indigo-500/20 rounded-2xl ring-1 ring-indigo-500/30 shadow-[0_0_20px_rgba(99,102,241,0.2)] group-hover:bg-indigo-500/30 transition-colors duration-500">
              <MessageCircle className="text-indigo-300" size={32} />
            </div>
            <div>
              <h4 className="text-2xl font-bold text-white tracking-tight"><T it="Interrogazioni Orali" en="Oral Examinations" /></h4>
              <p className="text-sm font-medium text-indigo-400/80 uppercase tracking-widest mt-1"><T it="L'anomalia valutativa" en="The evaluative anomaly" /></p>
            </div>
          </div>
          
          <p className="text-zinc-300 mb-8 leading-relaxed text-[15px]">
            <T 
              it="L'Italia è uno dei pochissimi paesi OCSE a utilizzare le interrogazioni orali per la valutazione quotidiana. La ricerca educativa dimostra che queste generano uno stress psicologico estremo e una varianza valutativa soggettiva (bias) fino a 2.5 volte superiore rispetto ai test scritti anonimizzati." 
              en="Italy is one of the very few OECD countries to use oral exams for daily grading. Educational research shows these generate extreme psychological stress and subjective grading variance (bias) up to 2.5 times higher than anonymized written tests." 
            />
          </p>

          <div className="h-72 bg-black/20 rounded-2xl border border-white/5 p-4 relative">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={oral_exams_variance}>
                <PolarGrid stroke="#3f3f46" strokeDasharray="3 3" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#d4d4d8', fontSize: 13, fontWeight: 500 }} />
                <Radar name="Varianza Orale" dataKey="oralVar" stroke="#818cf8" strokeWidth={2} fill="#818cf8" fillOpacity={0.4} />
                <Radar name="Varianza Scritta" dataKey="writtenVar" stroke="#34d399" strokeWidth={2} fill="#34d399" fillOpacity={0.4} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: 'rgba(24, 24, 27, 0.9)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '16px', color: '#fff', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center gap-6 mt-6 text-sm font-semibold">
            <span className="flex items-center gap-2 text-indigo-300"><div className="w-3 h-3 bg-indigo-500 rounded-full shadow-[0_0_10px_rgba(99,102,241,0.5)]" /><T it="Varianza Orale" en="Oral Variance" /></span>
            <span className="flex items-center gap-2 text-emerald-400"><div className="w-3 h-3 bg-emerald-500 rounded-full shadow-[0_0_10px_rgba(16,185,129,0.5)]" /><T it="Varianza Scritta" en="Written Variance" /></span>
          </div>
          <div className="flex justify-center mt-8">
            <SourceBadge agency="OECD / INVALSI" year="2023" />
          </div>
        </motion.div>

        {/* 2. Nepotism Card */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
          viewport={{ once: true }}
          className="group bg-gradient-to-br from-white/[0.05] to-transparent border border-white/10 backdrop-blur-2xl rounded-3xl p-8 hover:border-rose-500/40 hover:shadow-[0_0_40px_rgba(244,63,94,0.15)] hover:-translate-y-1 transition-all duration-500"
        >
          <div className="flex items-center gap-5 mb-8">
            <div className="p-4 bg-rose-500/20 rounded-2xl ring-1 ring-rose-500/30 shadow-[0_0_20px_rgba(244,63,94,0.2)] group-hover:bg-rose-500/30 transition-colors duration-500">
              <Users className="text-rose-300" size={32} />
            </div>
            <div>
              <h4 className="text-2xl font-bold text-white tracking-tight"><T it="Il Fattore Nepotismo" en="The Nepotism Factor" /></h4>
              <p className="text-sm font-medium text-rose-400/80 uppercase tracking-widest mt-1"><T it="Percezione di meritocrazia" en="Meritocracy perception" /></p>
            </div>
          </div>
          
          <p className="text-zinc-300 mb-8 leading-relaxed text-[15px]">
            <T 
              it="L'illusione della meritocrazia si scontra con la realtà socio-lavorativa. L'Italia registra la percentuale più alta in Europa di cittadini che ritengono 'essenziale' avere aderenze politiche o raccomandazioni per avere successo, deprimendo la motivazione allo studio." 
              en="The illusion of meritocracy clashes with reality. Italy records the highest percentage in Europe of citizens who believe it is 'essential' to have political connections or recommendations to succeed, depressing study motivation." 
            />
          </p>

          <div className="h-72 bg-black/20 rounded-2xl border border-white/5 p-4 relative">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={nepotism_perception} layout="vertical" margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                <XAxis type="number" stroke="#a1a1aa" domain={[0, 100]} tickFormatter={(val) => `${val}%`} tick={{ fill: '#71717a' }} />
                <YAxis dataKey="country" type="category" stroke="#d4d4d8" width={80} tick={{ fill: '#e4e4e7', fontWeight: 500 }} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: 'rgba(24, 24, 27, 0.9)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '16px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}
                  itemStyle={{ color: '#fff', fontWeight: 'bold' }}
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                />
                <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={24}>
                  {nepotism_perception.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.country === 'Italia' ? '#fb7185' : entry.euAvg ? '#818cf8' : '#52525b'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center mt-6">
            <SourceBadge agency="Eurobarometro" year="2023" />
          </div>
        </motion.div>

        {/* 3. Job Connections Card */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
          viewport={{ once: true }}
          className="group bg-gradient-to-br from-white/[0.05] to-transparent border border-white/10 backdrop-blur-2xl rounded-3xl p-8 hover:border-amber-500/40 hover:shadow-[0_0_40px_rgba(245,158,11,0.15)] hover:-translate-y-1 transition-all duration-500"
        >
          <div className="flex items-center gap-5 mb-8">
            <div className="p-4 bg-amber-500/20 rounded-2xl ring-1 ring-amber-500/30 shadow-[0_0_20px_rgba(245,158,11,0.2)] group-hover:bg-amber-500/30 transition-colors duration-500">
              <Briefcase className="text-amber-300" size={32} />
            </div>
            <div>
              <h4 className="text-2xl font-bold text-white tracking-tight"><T it="Il Mercato Relazionale" en="The Relational Market" /></h4>
              <p className="text-sm font-medium text-amber-400/80 uppercase tracking-widest mt-1"><T it="Primo lavoro tramite conoscenze" en="First job via connections" /></p>
            </div>
          </div>
          
          <p className="text-zinc-300 mb-8 leading-relaxed text-[15px]">
            <T 
              it="Confermando la percezione di nepotismo, l'Italia detiene il primato Europeo per l'ingresso nel mercato del lavoro tramite reti informali e familiari (34%), a causa del fallimento sistemico dei Centri per l'Impiego." 
              en="Confirming the perception of nepotism, Italy holds the European record for labor market entry via informal and family networks (34%), due to the systemic failure of Public Employment Services." 
            />
          </p>

          <div className="h-72 bg-black/20 rounded-2xl border border-white/5 p-4 relative pt-8">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={first_job_connections} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="country" stroke="#a1a1aa" tick={{ fill: '#d4d4d8', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis stroke="#a1a1aa" tickFormatter={(val) => `${val}%`} tick={{ fill: '#71717a' }} axisLine={false} tickLine={false} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: 'rgba(24, 24, 27, 0.9)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '16px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}
                  itemStyle={{ color: '#fff', fontWeight: 'bold' }}
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                />
                <Bar dataKey="value" radius={[6, 6, 0, 0]} barSize={40}>
                  {first_job_connections.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.country === 'Italia' ? '#fbbf24' : '#52525b'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center mt-6">
            <SourceBadge agency="Eurobarometro" year="2024" />
          </div>
        </motion.div>

        {/* 4. Social Mobility Card */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
          viewport={{ once: true }}
          className="group bg-gradient-to-br from-white/[0.05] to-transparent border border-white/10 backdrop-blur-2xl rounded-3xl p-8 hover:border-emerald-500/40 hover:shadow-[0_0_40px_rgba(16,185,129,0.15)] hover:-translate-y-1 transition-all duration-500"
        >
          <div className="flex items-center gap-5 mb-8">
            <div className="p-4 bg-emerald-500/20 rounded-2xl ring-1 ring-emerald-500/30 shadow-[0_0_20px_rgba(16,185,129,0.2)] group-hover:bg-emerald-500/30 transition-colors duration-500">
              <Scale className="text-emerald-300" size={32} />
            </div>
            <div>
              <h4 className="text-2xl font-bold text-white tracking-tight"><T it="Immobilità Sociale" en="Social Immobility" /></h4>
              <p className="text-sm font-medium text-emerald-400/80 uppercase tracking-widest mt-1"><T it="Indice di Mobilità Sociale" en="Social Mobility Index" /></p>
            </div>
          </div>
          
          <p className="text-zinc-300 mb-8 leading-relaxed text-[15px]">
            <T 
              it="L'effetto combinato di un sistema scolastico tracciato (tripartizione) e di un mercato del lavoro relazionale produce il peggior indice di mobilità sociale intergenerazionale d'Europa. Il destino socio-economico in Italia è ampiamente predeterminato dalla nascita." 
              en="The combined effect of a tracked school system (tripartition) and a relational labor market produces the worst intergenerational social mobility index in Europe. Socio-economic destiny in Italy is largely predetermined by birth." 
            />
          </p>

          <div className="h-72 bg-black/20 rounded-2xl border border-white/5 p-4 relative pt-8">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={social_mobility_index} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="country" stroke="#a1a1aa" tick={{ fill: '#d4d4d8', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis domain={[0, 10]} stroke="#a1a1aa" tick={{ fill: '#71717a' }} axisLine={false} tickLine={false} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: 'rgba(24, 24, 27, 0.9)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '16px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}
                  itemStyle={{ color: '#fff', fontWeight: 'bold' }}
                />
                <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={4} dot={{ fill: '#064e3b', stroke: '#34d399', strokeWidth: 2, r: 6 }} activeDot={{ r: 8, stroke: '#6ee7b7' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center mt-6">
            <SourceBadge agency="World Bank Global Database" year="2023" />
          </div>
        </motion.div>

      </div>
    </div>
  );
}
