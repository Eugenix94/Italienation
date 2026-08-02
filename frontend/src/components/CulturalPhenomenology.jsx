import React from 'react';
import { T } from './T';
import { motion } from 'framer-motion';
import { MessageCircle, Users, AlertTriangle, Scale } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, Radar } from 'recharts';

export default function CulturalPhenomenology() {
  const nepotismData = [
    { country: 'Italia', value: 83, euAvg: false },
    { country: 'EU Avg', value: 53, euAvg: true },
    { country: 'Francia', value: 58, euAvg: false },
    { country: 'Germania', value: 45, euAvg: false },
    { country: 'Svezia', value: 24, euAvg: false }
  ];

  const oralExamData = [
    { subject: 'Italiano', writtenVar: 2.1, oralVar: 4.8 },
    { subject: 'Matematica', writtenVar: 1.5, oralVar: 3.9 },
    { subject: 'Storia', writtenVar: 2.3, oralVar: 5.1 },
    { subject: 'Inglese', writtenVar: 1.8, oralVar: 4.2 }
  ];

  return (
    <div className="space-y-16 relative">
      
      {/* Glow Effects */}
      <div className="absolute top-1/2 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute top-1/2 right-1/4 w-96 h-96 bg-rose-500/5 rounded-full blur-[100px] pointer-events-none" />

      <div className="text-center max-w-3xl mx-auto relative z-10">
        <h3 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-zinc-400 mb-6 tracking-tight">
          <T it="Fenomenologia Culturale" en="Cultural Phenomenology" />
        </h3>
        <p className="text-zinc-400 text-lg leading-relaxed">
          <T 
            it="L'impatto dei meccanismi culturali non scritti: dalle valutazioni soggettive (interrogazioni) al deficit di meritocrazia (raccomandazioni)." 
            en="The impact of unwritten cultural mechanisms: from subjective evaluations (oral exams) to the meritocracy deficit (nepotism)." 
          />
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative z-10">
        
        {/* Oral Exams Card */}
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
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={oralExamData}>
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
        </motion.div>

        {/* Nepotism Card */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15, ease: [0.22, 1, 0.36, 1] }}
          viewport={{ once: true }}
          className="group bg-gradient-to-br from-white/[0.05] to-transparent border border-white/10 backdrop-blur-2xl rounded-3xl p-8 hover:border-rose-500/40 hover:shadow-[0_0_40px_rgba(244,63,94,0.15)] hover:-translate-y-1 transition-all duration-500"
        >
          <div className="flex items-center gap-5 mb-8">
            <div className="p-4 bg-rose-500/20 rounded-2xl ring-1 ring-rose-500/30 shadow-[0_0_20px_rgba(244,63,94,0.2)] group-hover:bg-rose-500/30 transition-colors duration-500">
              <Users className="text-rose-300" size={32} />
            </div>
            <div>
              <h4 className="text-2xl font-bold text-white tracking-tight"><T it="Il Fattore Nepotismo" en="The Nepotism Factor" /></h4>
              <p className="text-sm font-medium text-rose-400/80 uppercase tracking-widest mt-1"><T it="Il deficit di meritocrazia" en="The meritocracy deficit" /></p>
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
              <BarChart data={nepotismData} layout="vertical" margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                <XAxis type="number" stroke="#a1a1aa" domain={[0, 100]} tickFormatter={(val) => `${val}%`} tick={{ fill: '#71717a' }} />
                <YAxis dataKey="country" type="category" stroke="#d4d4d8" width={80} tick={{ fill: '#e4e4e7', fontWeight: 500 }} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: 'rgba(24, 24, 27, 0.9)', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '16px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}
                  itemStyle={{ color: '#fff', fontWeight: 'bold' }}
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                />
                <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={24}>
                  {nepotismData.map((entry, index) => (
                    <cell key={`cell-${index}`} fill={entry.country === 'Italia' ? '#fb7185' : entry.euAvg ? '#818cf8' : '#52525b'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-center text-xs text-zinc-400 mt-6 uppercase tracking-wider font-semibold">
            <T it="% che ritiene essenziale avere 'raccomandazioni'" en="% believing 'knowing the right people' is essential" />
          </p>
        </motion.div>

      </div>
    </div>
  );
}
