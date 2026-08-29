import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, LineChart, Line, Cell } from 'recharts';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import SourceBadge from './SourceBadge';
import { tracking_outcomes, invalsi_performance } from '../assets/dashboard_metrics.json';
import { motion } from 'framer-motion';
import { Home, GraduationCap, Briefcase, ArrowRight } from 'lucide-react';

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

// Phase tag component
const PhaseTag = ({ phase, icon: Icon, color, borderColor }) => (
  <span className={`inline-flex items-center gap-1.5 text-xs font-bold px-2.5 py-1 rounded-full bg-zinc-900 border ${borderColor} ${color}`}>
    <Icon size={12} />
    {phase}
  </span>
);

export default function StructuralOutcomes() {
  const { lang } = useLanguage();
  const isIt = lang === 'it';

  // Track colors for consistent identity
  const trackColors = {
    'Liceo': '#6366f1',
    'Istituto Tecnico': '#10b981',
    'Istituto Professionale': '#f43f5e'
  };

  return (
    <div className="space-y-16">
      {/* Section Header */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center max-w-4xl mx-auto"
      >
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-sm font-medium mb-6">
          <GraduationCap size={16} />
          <T it="Il Sistema Tripartito" en="The Tripartite System" />
        </div>
        <h2 className="text-3xl sm:text-4xl font-black text-white mb-4">
          <T it="Come l'Origine determina la Destinazione" en="How Origin determines Destination" />
        </h2>
        <p className="text-zinc-400 text-base sm:text-lg leading-relaxed">
          <T 
            it="A 14 anni, gli studenti italiani vengono divisi in tre percorsi — Liceo, Tecnico, Professionale — una scelta che correla fortemente con il reddito familiare (Origine), non con le attitudini personali. Ogni indirizzo riceve risorse diverse (Educazione), producendo esiti radicalmente diversi (Destinazione)." 
            en="At age 14, Italian students are sorted into three tracks — Liceo, Tecnico, Professionale — a choice that strongly correlates with family income (Origin), not personal aptitude. Each track receives different resources (Education), producing radically different outcomes (Destination)." 
          />
        </p>

        {/* Mini flow reminder */}
        <div className="flex items-center justify-center gap-2 mt-6 flex-wrap">
          <PhaseTag phase={isIt ? 'Origine' : 'Origin'} icon={Home} color="text-amber-400" borderColor="border-amber-500/30" />
          <ArrowRight size={14} className="text-zinc-600" />
          <PhaseTag phase={isIt ? 'Educazione' : 'Education'} icon={GraduationCap} color="text-indigo-400" borderColor="border-indigo-500/30" />
          <ArrowRight size={14} className="text-zinc-600" />
          <PhaseTag phase={isIt ? 'Destinazione' : 'Destination'} icon={Briefcase} color="text-rose-400" borderColor="border-rose-500/30" />
        </div>
      </motion.div>

      {/* === ORIGIN CHART === */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }} 
        whileInView={{ opacity: 1, y: 0 }} 
        viewport={{ once: true }}
        className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
      >
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
          <div className="flex items-center gap-3">
            <PhaseTag phase="O" icon={Home} color="text-amber-400" borderColor="border-amber-500/30" />
            <h3 className="text-xl font-bold text-white">
              <T it="Reddito Familiare Medio per Indirizzo" en="Average Family Income by Track" />
            </h3>
          </div>
          <SourceBadge agency="MUR / ISTAT" year="2023" />
        </div>
        <p className="text-sm text-zinc-400 mb-6">
          <T 
            it="La scelta della scuola superiore a 14 anni è fortemente predeterminata dal reddito familiare. I Licei attraggono figli di famiglie con redditi 2.5 volte superiori rispetto ai Professionali." 
            en="The high school choice at age 14 is heavily predetermined by family income. Licei attract children from families earning 2.5x more than Professionali." 
          />
        </p>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={tracking_outcomes} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
              <XAxis dataKey="track" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 13 }} />
              <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa' }} tickFormatter={(val) => `€${val/1000}k`} />
              <RechartsTooltip content={<CustomTooltip />} />
              <Bar dataKey="avg_income_origin" name={isIt ? 'Reddito Medio (€)' : 'Avg Income (€)'} radius={[8, 8, 0, 0]} barSize={60}>
                {tracking_outcomes.map((entry, i) => (
                  <Cell key={i} fill={trackColors[entry.track] || '#6366f1'} fillOpacity={0.85} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* === EDUCATION CHARTS === */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Resource Allocation */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} 
          whileInView={{ opacity: 1, y: 0 }} 
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
        >
          <div className="flex items-center gap-3 mb-4">
            <PhaseTag phase="E" icon={GraduationCap} color="text-indigo-400" borderColor="border-indigo-500/30" />
            <h3 className="text-lg font-bold text-white">
              <T it="Risorse Strutturali" en="Structural Resources" />
            </h3>
          </div>
          <p className="text-sm text-zinc-400 mb-6">
            <T 
              it="Precarietà docenti e sicurezza edifici: i Professionali soffrono 3x più precarietà." 
              en="Teacher precarity & building safety: Professionali suffer 3x more precarity." 
            />
          </p>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={tracking_outcomes} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="track" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 11 }} />
                <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa' }} tickFormatter={(val) => `${val}%`} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '12px' }} />
                <Bar dataKey="teacher_precarity_pct" name={isIt ? 'Precarietà Docenti (%)' : 'Teacher Precarity (%)'} fill="#f59e0b" radius={[4, 4, 0, 0]} />
                <Bar dataKey="building_safety_issues_pct" name={isIt ? 'Problemi Sicurezza (%)' : 'Building Safety Issues (%)'} fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* INVALSI Scores */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} 
          whileInView={{ opacity: 1, y: 0 }} 
          viewport={{ once: true }}
          className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
        >
          <div className="flex items-center gap-3 mb-4">
            <PhaseTag phase="E" icon={GraduationCap} color="text-indigo-400" borderColor="border-indigo-500/30" />
            <h3 className="text-lg font-bold text-white">
              <T it="Punteggi INVALSI Matematica" en="INVALSI Math Scores" />
            </h3>
          </div>
          <p className="text-sm text-zinc-400 mb-6">
            <T 
              it="60+ punti di gap tra Liceo e Professionale — stesso Paese, stessa età." 
              en="60+ point gap between Liceo and Professionale — same country, same age." 
            />
          </p>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={invalsi_performance} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="region_macro" stroke="#71717a" tick={{ fill: '#a1a1aa' }} />
                <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa' }} domain={[130, 250]} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '12px' }} />
                <Line type="monotone" dataKey="liceo_math_score" name={isIt ? "Liceo" : "Lyceum"} stroke="#6366f1" strokeWidth={3} dot={{ r: 5, fill: '#6366f1' }} />
                <Line type="monotone" dataKey="tecnico_math_score" name={isIt ? "Istituto Tecnico" : "Technical Institute"} stroke="#10b981" strokeWidth={3} dot={{ r: 5, fill: '#10b981' }} />
                <Line type="monotone" dataKey="professionale_math_score" name={isIt ? "Istituto Professionale" : "Vocational Institute"} stroke="#f43f5e" strokeWidth={3} dot={{ r: 5, fill: '#f43f5e' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* === DESTINATION CHART === */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }} 
        whileInView={{ opacity: 1, y: 0 }} 
        viewport={{ once: true }}
        className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
      >
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
          <div className="flex items-center gap-3">
            <PhaseTag phase="D" icon={Briefcase} color="text-rose-400" borderColor="border-rose-500/30" />
            <h3 className="text-xl font-bold text-white">
              <T it="Esiti: Università vs NEET" en="Outcomes: University vs NEET" />
            </h3>
          </div>
          <SourceBadge agency="AlmaDiploma / MUR" year="2023" />
        </div>
        <p className="text-sm text-zinc-400 mb-6">
          <T 
            it="82% dei liceali accede all'università, contro l'8% dei diplomati professionali. Parallelamente, il tasso NEET dei Professionali (22%) è 4x quello dei Licei (5%)." 
            en="82% of Liceo graduates access university, versus 8% of Professionali graduates. Meanwhile, the Professionali NEET rate (22%) is 4x that of Licei (5%)." 
          />
        </p>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={tracking_outcomes} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
              <XAxis dataKey="track" stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 13 }} />
              <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa' }} tickFormatter={(val) => `${val}%`} />
              <RechartsTooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '12px' }} />
              <Bar dataKey="university_access_pct" name={isIt ? 'Accesso Università (%)' : 'University Access (%)'} fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="neet_rate_pct" name={isIt ? 'Tasso NEET (%)' : 'NEET Rate (%)'} fill="#f43f5e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* KEY INSIGHT */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="bg-rose-500/10 border-l-4 border-rose-500 p-6 rounded-r-2xl"
      >
        <p className="text-rose-200 leading-relaxed">
          <strong><T it="Il circolo vizioso: " en="The vicious cycle: " /></strong>
          <T 
            it="L'Origine (reddito familiare) predetermina il percorso Educativo, il quale — attraverso risorse diseguali — produce Destinazioni radicalmente diverse. Non è una questione di talento individuale, ma di architettura sistemica. Le sezioni seguenti esplorano ogni dimensione di questo meccanismo e i suoi costi econometrici." 
            en="Origin (family income) predetermines the Educational path, which — through unequal resources — produces radically different Destinations. This is not a matter of individual talent, but of systemic architecture. The following sections explore every dimension of this mechanism and its econometric costs." 
          />
        </p>
      </motion.div>

      {/* SOURCE BADGES */}
      <div className="flex flex-wrap gap-3">
        <SourceBadge agency="ISTAT" year="2023" />
        <SourceBadge agency="INVALSI" year="2023" />
        <SourceBadge agency="MIM" year="2023" />
        <SourceBadge topicKey="tracking" label="Eurydice" />
      </div>
    </div>
  );
}
