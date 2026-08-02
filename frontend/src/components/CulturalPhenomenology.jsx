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
    <div className="space-y-12">
      
      <div className="text-center max-w-3xl mx-auto">
        <h3 className="text-3xl font-bold text-white mb-4">
          <T it="Fenomenologia Culturale" en="Cultural Phenomenology" />
        </h3>
        <p className="text-zinc-400">
          <T 
            it="L'impatto dei meccanismi culturali non scritti: dalle valutazioni soggettive (interrogazioni) al deficit di meritocrazia (raccomandazioni)." 
            en="The impact of unwritten cultural mechanisms: from subjective evaluations (oral exams) to the meritocracy deficit (nepotism)." 
          />
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Oral Exams Card */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="p-4 bg-indigo-500/10 rounded-2xl">
              <MessageCircle className="text-indigo-400" size={32} />
            </div>
            <div>
              <h4 className="text-xl font-bold text-white"><T it="Interrogazioni Orali" en="Oral Examinations" /></h4>
              <p className="text-sm text-zinc-500"><T it="L'anomalia valutativa italiana" en="The Italian evaluative anomaly" /></p>
            </div>
          </div>
          
          <p className="text-zinc-300 mb-8 leading-relaxed text-sm">
            <T 
              it="L'Italia è uno dei pochissimi paesi OCSE a utilizzare le interrogazioni orali per la valutazione quotidiana. La ricerca educativa dimostra che queste generano uno stress psicologico estremo e una varianza valutativa soggettiva (bias) fino a 2.5 volte superiore rispetto ai test scritti anonimizzati." 
              en="Italy is one of the very few OECD countries to use oral exams for daily grading. Educational research shows these generate extreme psychological stress and subjective grading variance (bias) up to 2.5 times higher than anonymized written tests." 
            />
          </p>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={oralExamData}>
                <PolarGrid stroke="#3f3f46" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <Radar name="Varianza Orale" dataKey="oralVar" stroke="#6366f1" fill="#6366f1" fillOpacity={0.5} />
                <Radar name="Varianza Scritta" dataKey="writtenVar" stroke="#10b981" fill="#10b981" fillOpacity={0.5} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '12px', color: '#fff' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center gap-4 mt-4 text-xs font-semibold">
            <span className="flex items-center gap-2 text-indigo-400"><div className="w-3 h-3 bg-indigo-500/50 rounded-sm" /><T it="Varianza Orale" en="Oral Variance" /></span>
            <span className="flex items-center gap-2 text-emerald-400"><div className="w-3 h-3 bg-emerald-500/50 rounded-sm" /><T it="Varianza Scritta" en="Written Variance" /></span>
          </div>
        </motion.div>

        {/* Nepotism Card */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          viewport={{ once: true }}
          className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8"
        >
          <div className="flex items-center gap-4 mb-6">
            <div className="p-4 bg-rose-500/10 rounded-2xl">
              <Users className="text-rose-400" size={32} />
            </div>
            <div>
              <h4 className="text-xl font-bold text-white"><T it="Raccomandazioni e Nepotismo" en="Nepotism & Recommendations" /></h4>
              <p className="text-sm text-zinc-500"><T it="Il deficit di meritocrazia" en="The meritocracy deficit" /></p>
            </div>
          </div>
          
          <p className="text-zinc-300 mb-8 leading-relaxed text-sm">
            <T 
              it="L'illusione della meritocrazia scolastica si scontra con la realtà del mercato del lavoro. Secondo i dati Eurobarometro, l'Italia registra la percentuale più alta in Europa di cittadini che ritengono 'essenziale' conoscere le persone giuste per avere successo, deprimendo la motivazione allo studio (learned helplessness)." 
              en="The illusion of school meritocracy clashes with the reality of the labor market. According to Eurobarometer data, Italy records the highest percentage in Europe of citizens who believe it is 'essential' to know the right people to succeed, depressing study motivation (learned helplessness)." 
            />
          </p>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={nepotismData} layout="vertical" margin={{ top: 0, right: 30, left: 20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                <XAxis type="number" stroke="#a1a1aa" domain={[0, 100]} tickFormatter={(val) => `${val}%`} />
                <YAxis dataKey="country" type="category" stroke="#a1a1aa" width={70} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '12px' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a' }}
                />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {nepotismData.map((entry, index) => (
                    <cell key={`cell-${index}`} fill={entry.country === 'Italia' ? '#f43f5e' : entry.euAvg ? '#6366f1' : '#3f3f46'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-center text-xs text-zinc-500 mt-4 uppercase tracking-wider font-semibold">
            <T it="% che ritiene essenziale avere 'raccomandazioni'" en="% believing 'knowing the right people' is essential" />
          </p>
        </motion.div>

      </div>
    </div>
  );
}
