import React, { useState, useMemo, useEffect } from 'react';
import oedData from '../assets/oed_international_migration_calculator.json';
import metricsData from '../assets/dashboard_metrics.json';
import { T } from './T';
import { motion, AnimatePresence } from 'framer-motion';
import { RefreshCcw, Home, GraduationCap, Map, BarChart2, Activity, AlertCircle, Sliders, MessageCircle, Wallet, Filter, TrendingDown } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const PROFILE_ICONS = {
  dropout: '🚫',
  vocational: '🔧',
  technical: '⚙️',
  academic: '🎓',
};

// Qualitative Narratives DB loaded from JSON
// ESCS Probabilities loaded from JSON

const MetricRing = ({ value, maxValue = 1, label, sublabel, color, format = 'pct', prevValue, size = 'normal' }) => {
  const displayVal = format === 'pct' ? `${(value * 100).toFixed(0)}%` : format === 'eur' ? `€${value?.toLocaleString()}` : value.toFixed(1);
  const fraction = format === 'pct' ? value : format === 'index' ? value / 10 : Math.min(value / 4000, 1);
  const delta = prevValue != null ? value - prevValue : null;

  const ringSize = size === 'large' ? 'w-24 h-24 sm:w-32 sm:h-32' : 'w-16 h-16 sm:w-20 sm:h-20';
  const textClass = size === 'large' ? 'text-2xl sm:text-3xl font-black' : 'text-lg sm:text-xl font-bold';

  return (
    <div className="flex flex-col items-center text-center">
      <div className={`relative ${ringSize} mb-3`}>
        <svg viewBox="0 0 120 120" className="w-full h-full drop-shadow-xl">
          <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
          <circle cx="60" cy="60" r="52" fill="none" stroke={color} strokeWidth="8"
            strokeDasharray={`${Math.max(0, fraction) * 327} 327`}
            strokeLinecap="round"
            style={{ transform: 'rotate(-90deg)', transformOrigin: 'center', transition: 'stroke-dasharray 1s cubic-bezier(0.4, 0, 0.2, 1)' }}
          />
        </svg>
        <span className={`absolute inset-0 flex items-center justify-center text-white drop-shadow-md ${textClass}`}>{displayVal}</span>
      </div>
      <h4 className="text-xs font-bold text-white mb-0.5 uppercase tracking-wider">{label}</h4>
      <p className="text-[10px] text-zinc-400">{sublabel}</p>
      {delta != null && (
        <span className={`mt-2 text-[10px] font-bold px-2 py-0.5 rounded-full shadow-lg ${delta < 0 ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20' : delta > 0 ? 'bg-rose-500/20 text-rose-400 border border-rose-500/20' : 'bg-zinc-700 text-zinc-400'}`}>
          {format === 'pct' ? `${delta > 0 ? '+' : ''}${(delta * 100).toFixed(0)}pp` :
           format === 'eur' ? `${delta > 0 ? '+' : ''}€${delta.toLocaleString()}` :
           `${delta > 0 ? '+' : ''}${delta.toFixed(1)}`}
        </span>
      )}
    </div>
  );
};

export default function OEDSimulator() {
  const [simData, setSimData] = useState(null);
  const [originCountry, setOriginCountry] = useState('Italy');
  const [escs, setEscs] = useState('low');
  const [profile, setProfile] = useState('vocational');
  const [migrationEnabled, setMigrationEnabled] = useState(false);
  const [destCountry, setDestCountry] = useState('Sweden');
  
  // POLICY INTERVENTION STATE
  const [textbookSubsidy, setTextbookSubsidy] = useState(0); // 0 to 100
  const [pnrrShift, setPnrrShift] = useState(0); // 0 to 100
  const [hasIntegrativeYear, setHasIntegrativeYear] = useState(false); // 5th Year IeFP
  const [openUniversityAccess, setOpenUniversityAccess] = useState(0); // 0 to 100

  const countries = Object.keys(oedData.countries);
  const originData = oedData.countries[originCountry];

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/simulator_probabilities.json`)
      .then(res => res.json())
      .then(data => setSimData(data))
      .catch(err => console.error("Failed to load simulator data:", err));
  }, []);

  const migrationDestinations = useMemo(() => {
    const paths = oedData.migration_pathways?.[originCountry];
    return paths ? Object.keys(paths) : [];
  }, [originCountry]);

  useEffect(() => {
    if (migrationEnabled && migrationDestinations.length > 0 && !migrationDestinations.includes(destCountry)) {
      setDestCountry(migrationDestinations[0]);
    }
    if (migrationDestinations.length === 0) {
      setMigrationEnabled(false);
    }
  }, [originCountry, migrationEnabled, migrationDestinations, destCountry]);

  const resetSim = () => {
    setOriginCountry('Italy');
    setEscs('low');
    setProfile('vocational');
    setMigrationEnabled(false);
    setTextbookSubsidy(0);
    setPnrrShift(0);
    setHasIntegrativeYear(false);
    setOpenUniversityAccess(0);
  };

  const isPolicyActive = textbookSubsidy > 0 || pnrrShift > 0 || hasIntegrativeYear || openUniversityAccess > 0;

  const getTrackProbability = (trackKey) => {
    if (!simData) return 0;
    const probs = simData.ESCS_PROBABILITIES[originCountry] || simData.DEFAULT_ESCS_PROB;
    let baseProb = probs[escs][trackKey];

    // Policy Simulation: Subsidized Textbooks shift Low ESCS students away from Vocational to Academic
    if (escs === 'low' && originCountry === 'Italy') {
      const shiftFactor = (textbookSubsidy / 100) * 0.15; // Max 15% shift
      if (trackKey === 'vocational') baseProb -= shiftFactor;
      if (trackKey === 'dropout') baseProb -= shiftFactor * 0.5;
      if (trackKey === 'academic') baseProb += shiftFactor * 1.5;
    }

    return Math.max(0, Math.min(1, baseProb));
  };

  // Get Adjusted Outcomes based on Policy Shift
  const getOutcomes = () => {
    const base = originData?.outcomes?.[profile];
    if (!base) return null;
    
    let adjNeet = base.prob_neet;
    let adjTertiary = base.prob_tertiary_access;

    // IeFP 5th Year Integrative Barrier Logic
    if (profile === 'vocational' && originCountry === 'Italy') {
      if (hasIntegrativeYear) {
        adjTertiary = 0.15; // Unlocked but low probability
      } else {
        adjTertiary = 0.006; // Hard capped at 0.6%
      }
    }

    if (originCountry !== 'Italy') {
       return { ...base, prob_neet: adjNeet, prob_tertiary_access: adjTertiary };
    }

    // Policy Simulation: Open University Access (Abolish Diploma Barrier)
    if (openUniversityAccess > 0) {
      if (profile === 'dropout' || (profile === 'vocational' && !hasIntegrativeYear)) {
         // Impact: up to 35% of them enter tertiary education/short-cycles, reducing NEET proportionally
         const impact = (openUniversityAccess / 100);
         const tertiaryBoost = 0.35 * impact; 
         adjTertiary = adjTertiary + tertiaryBoost;
         
         // NEET drops roughly by the same amount they enter tertiary
         adjNeet = adjNeet - tertiaryBoost; 
      }
    }

    // Policy Simulation: Shifting PNRR to Teachers drops NEET and boosts Tertiary access (better teaching quality)
    if (pnrrShift > 0) {
      const impact = (pnrrShift / 100) * 0.3; // Up to 30% relative reduction in NEET
      adjNeet = adjNeet * (1 - impact);
      adjTertiary = adjTertiary * (1 + (impact * 0.5));
    }

    return {
      ...base,
      prob_neet: Math.max(0, adjNeet),
      prob_tertiary_access: Math.min(1, adjTertiary)
    };
  };

  const originOutcomes = getOutcomes();
  const rawOriginOutcomes = originData?.outcomes?.[profile];

  const migrationData = migrationEnabled
    ? oedData.migration_pathways?.[originCountry]?.[destCountry]?.[profile]
    : null;

  // Track outcomes for radar chart
  const trackMap = { 'academic': 'Liceo', 'technical': 'Istituto Tecnico', 'vocational': 'Istituto Professionale', 'dropout': 'Dropout' };
  const currentTrackName = trackMap[profile] || 'Liceo';
  const trackData = metricsData.tracking_outcomes.find(t => t.track === currentTrackName) || metricsData.tracking_outcomes[0];
  const radarData = [
    { subject: 'Teacher Precarity', A: trackData.teacher_precarity_pct, fullMark: 50 },
    { subject: 'Building Issues', A: trackData.building_safety_issues_pct, fullMark: 50 },
    { subject: 'NEET Risk', A: trackData.neet_rate_pct, fullMark: 50 },
  ];

  // Pipeline Data (ESCS -> Track -> Destination)
  const pipelineData = [
    { name: 'Dropout', prob: getTrackProbability('dropout') * 100, fill: '#f43f5e' },
    { name: 'Vocational', prob: getTrackProbability('vocational') * 100, fill: '#f59e0b' },
    { name: 'Technical', prob: getTrackProbability('technical') * 100, fill: '#818cf8' },
    { name: 'Academic', prob: getTrackProbability('academic') * 100, fill: '#10b981' }
  ];

  return (
    <div className="flex flex-col lg:flex-row gap-6 items-start w-full">
      
      {/* LEFT COLUMN: Unified Interactive Controls */}
      <div className="w-full lg:w-[380px] bg-zinc-950/90 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 shadow-2xl flex-shrink-0 sticky top-24 space-y-8 z-10">
        
        <div className="flex justify-between items-center border-b border-zinc-800 pb-4">
          <h2 className="text-xl font-black text-white flex items-center gap-2">
            <Sliders className="text-indigo-400" />
            <T it="OED Engine" en="OED Engine" />
          </h2>
          <button onClick={resetSim} className="text-zinc-500 hover:text-white transition-colors" title="Reset">
            <RefreshCcw size={18} />
          </button>
        </div>

        {/* Origin */}
        <div className="space-y-3">
          <label className="text-xs font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-2">
            <Home size={14} /> <T it="1. Origine & Status" en="1. Origin & Status" />
          </label>
          <select 
            value={originCountry} 
            onChange={e => setOriginCountry(e.target.value)} 
            className="w-full bg-zinc-900 border border-zinc-700 rounded-xl px-3 py-2 text-white font-bold mb-2 focus:ring-2 focus:ring-indigo-500 outline-none"
          >
            {countries.map(c => (
              <option key={c} value={c}>{oedData.countries[c].flag} {c}</option>
            ))}
          </select>
          <div className="grid grid-cols-2 gap-2">
            <button onClick={() => setEscs('low')} className={`p-2 rounded-xl border font-bold text-xs transition-all ${escs === 'low' ? 'bg-rose-500/20 border-rose-500 text-rose-300 shadow-[0_0_15px_rgba(244,63,94,0.3)]' : 'bg-zinc-800 border-zinc-700 text-zinc-400 hover:border-zinc-600'}`}>
              <T it="ESCS Basso (Q1)" en="Low ESCS (Q1)" />
            </button>
            <button onClick={() => setEscs('high')} className={`p-2 rounded-xl border font-bold text-xs transition-all ${escs === 'high' ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 shadow-[0_0_15px_rgba(16,185,129,0.3)]' : 'bg-zinc-800 border-zinc-700 text-zinc-400 hover:border-zinc-600'}`}>
              <T it="ESCS Alto (Q5)" en="High ESCS (Q5)" />
            </button>
          </div>
        </div>

        {/* Education Profile */}
        <div className="space-y-3">
          <label className="text-xs font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-2">
            <GraduationCap size={14} /> <T it="2. Percorso Formativo" en="2. Educational Track" />
          </label>
          <div className="grid grid-cols-2 gap-2">
            {Object.keys(originData.outcomes).map(key => {
              const prob = getTrackProbability(key);
              return (
                <button key={key} onClick={() => setProfile(key)} className={`p-2 rounded-xl border text-left transition-all relative overflow-hidden ${profile === key ? 'bg-indigo-600/20 border-indigo-500 shadow-[0_0_15px_rgba(99,102,241,0.2)]' : 'bg-zinc-800 border-zinc-700 hover:border-zinc-600'}`}>
                  <div className="flex justify-between items-start mb-1">
                    <span className="text-xl">{PROFILE_ICONS[key]}</span>
                    <span className={`text-xs font-black ${prob > 0.4 ? 'text-rose-400' : 'text-emerald-400'}`}>{(prob*100).toFixed(0)}%</span>
                  </div>
                  <div className={`text-xs font-bold ${profile === key ? 'text-indigo-300' : 'text-zinc-300'}`}>
                    <T it={key.charAt(0).toUpperCase() + key.slice(1)} en={key.charAt(0).toUpperCase() + key.slice(1)} />
                  </div>
                </button>
              )
            })}
          </div>
        </div>

        {/* Policy Sandbox (Only for Italy) */}
        {originCountry === 'Italy' && (
          <div className="space-y-4 pt-4 border-t border-zinc-800">
            <label className="text-xs font-bold uppercase tracking-wider text-emerald-500 flex items-center gap-2">
              <Filter size={14} /> <T it="Policy Sandbox (IT)" en="Policy Sandbox (IT)" />
            </label>
            
            <div>
              <div className="flex justify-between items-end mb-1">
                <span className="text-[10px] font-bold text-zinc-400"><T it="Sussidio Libri" en="Textbook Subsidy" /></span>
                <span className="text-[10px] text-emerald-400 font-mono">{textbookSubsidy}%</span>
              </div>
              <input type="range" min="0" max="100" value={textbookSubsidy} onChange={(e) => setTextbookSubsidy(Number(e.target.value))} className="w-full accent-emerald-500 h-1.5 bg-zinc-700 rounded-lg appearance-none cursor-pointer" />
            </div>

            <div>
              <div className="flex justify-between items-end mb-1">
                <span className="text-[10px] font-bold text-zinc-400"><T it="Accesso Universitario Aperto" en="Open Uni Access" /></span>
                <span className="text-[10px] text-emerald-400 font-mono">{openUniversityAccess}%</span>
              </div>
              <input type="range" min="0" max="100" value={openUniversityAccess} onChange={(e) => setOpenUniversityAccess(Number(e.target.value))} className="w-full accent-emerald-500 h-1.5 bg-zinc-700 rounded-lg appearance-none cursor-pointer" />
            </div>
            
            <div>
              <div className="flex justify-between items-end mb-1">
                <span className="text-[10px] font-bold text-zinc-400"><T it="Shift PNRR (a Docenti)" en="PNRR Shift (to Teachers)" /></span>
                <span className="text-[10px] text-emerald-400 font-mono">{pnrrShift}%</span>
              </div>
              <input type="range" min="0" max="100" value={pnrrShift} onChange={(e) => setPnrrShift(Number(e.target.value))} className="w-full accent-emerald-500 h-1.5 bg-zinc-700 rounded-lg appearance-none cursor-pointer" />
            </div>

            {profile === 'vocational' && (
              <label className="flex items-center gap-2 cursor-pointer mt-2">
                <input type="checkbox" checked={hasIntegrativeYear} onChange={(e) => setHasIntegrativeYear(e.target.checked)} className="rounded border-zinc-700 text-emerald-500 bg-zinc-900 focus:ring-0 focus:ring-offset-0" />
                <span className="text-[10px] font-bold text-zinc-300"><T it="5° Anno Integrativo (Sblocca Uni)" en="5th Integrative Year (Unlocks Uni)" /></span>
              </label>
            )}
          </div>
        )}

        {/* Destination / Migration */}
        {migrationDestinations.length > 0 && (
          <div className="space-y-3 pt-4 border-t border-zinc-800">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold uppercase tracking-wider text-zinc-500 flex items-center gap-2">
                <Map size={14} /> <T it="3. Migrazione" en="3. Migration" />
              </label>
              <button onClick={() => setMigrationEnabled(!migrationEnabled)} className={`relative w-8 h-4 rounded-full transition-all ${migrationEnabled ? 'bg-indigo-500' : 'bg-zinc-700'}`}>
                <span className={`absolute top-0.5 w-3 h-3 rounded-full bg-white shadow-md transition-all ${migrationEnabled ? 'left-4.5' : 'left-0.5'}`} />
              </button>
            </div>
            {migrationEnabled && (
              <select 
                value={destCountry} 
                onChange={e => setDestCountry(e.target.value)} 
                className="w-full bg-indigo-900/20 border border-indigo-500/50 rounded-xl px-3 py-2 text-indigo-300 font-bold mb-2 focus:ring-2 focus:ring-indigo-500 outline-none"
              >
                {migrationDestinations.map(c => (
                  <option key={c} value={c}>{oedData.countries[c].flag} {c}</option>
                ))}
              </select>
            )}
          </div>
        )}

      </div>

      {/* RIGHT COLUMN: Real-Time Results Dashboard */}
      <div className="w-full flex-1 space-y-6">
        
        {/* Main Outcomes Header */}
        <div className="bg-zinc-950/90 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
          {isPolicyActive && (
            <div className="absolute top-0 right-0 bg-emerald-500 text-white text-[10px] font-bold px-3 py-1 rounded-bl-xl uppercase tracking-wider shadow-lg">
              <T it="Policy Attiva" en="Policy Active" />
            </div>
          )}
          
          <div className="flex flex-col md:flex-row gap-6 justify-between items-center mb-8">
            <div>
              <h2 className="text-2xl sm:text-3xl font-black text-white flex items-center gap-3">
                <span className="text-4xl">{originData.flag}</span>
                <T it={`Esiti: ${originData.outcomes[profile].label}`} en={`Outcomes: ${originData.outcomes[profile].label}`} />
              </h2>
              <p className="text-sm text-zinc-400 mt-1">
                <T it="Risultati calcolati in tempo reale dal modello probabilistico OED." en="Results calculated in real-time by the OED probabilistic model." />
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <MetricRing 
              size="large"
              value={originOutcomes.prob_neet} 
              prevValue={isPolicyActive ? rawOriginOutcomes.prob_neet : null} 
              label="NEET" 
              sublabel="Risk %" 
              color={originOutcomes.prob_neet > 0.2 ? '#f43f5e' : '#10b981'} 
              format="pct" 
            />
            <MetricRing 
              size="large"
              value={originOutcomes.prob_tertiary_access} 
              prevValue={isPolicyActive ? rawOriginOutcomes.prob_tertiary_access : null} 
              label="University" 
              sublabel="Access %" 
              color={originOutcomes.prob_tertiary_access < 0.3 ? '#f43f5e' : '#10b981'} 
              format="pct" 
            />
            <MetricRing 
              size="large"
              value={originOutcomes.social_mobility_index} 
              label="Mobility" 
              sublabel="Index (0-10)" 
              color={originOutcomes.social_mobility_index < 5 ? '#f43f5e' : '#10b981'} 
              format="index" 
            />
            <MetricRing 
              size="large"
              value={originOutcomes.expected_monthly_income_eur} 
              label="Income" 
              sublabel="€/mo" 
              color="#4f46e5" 
              format="eur" 
            />
          </div>
        </div>

        {/* Migratory Outcomes (Conditional) */}
        {migrationEnabled && migrationData && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="bg-indigo-950/40 backdrop-blur-xl border border-indigo-500/30 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 bg-indigo-500 text-white text-[10px] font-bold px-3 py-1 rounded-bl-xl uppercase tracking-wider shadow-lg">
              <T it="Brain Drain Sim" en="Brain Drain Sim" />
            </div>
            <h3 className="text-xl sm:text-2xl font-black text-indigo-300 mb-6 flex items-center gap-3">
              <span className="text-3xl">{oedData.countries[destCountry].flag}</span>
              <T it={`Nuovi Esiti in ${destCountry}`} en={`New Outcomes in ${destCountry}`} />
            </h3>
            <div className="bg-indigo-900/20 rounded-xl p-4 mb-8 border border-indigo-500/20">
              <p className="text-sm font-bold text-indigo-200">
                <T it="Pathway di Accesso:" en="Access Pathway:" /> <span className="text-white">{migrationData.pathway}</span>
              </p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <MetricRing value={migrationData.new_prob_neet} prevValue={originOutcomes.prob_neet} label="NEET" sublabel="Risk %" color={migrationData.new_prob_neet > 0.2 ? '#f43f5e' : '#10b981'} format="pct" />
              <MetricRing value={migrationData.new_prob_tertiary_access} prevValue={originOutcomes.prob_tertiary_access} label="University" sublabel="Access %" color={migrationData.new_prob_tertiary_access < 0.3 ? '#f43f5e' : '#10b981'} format="pct" />
              <MetricRing value={migrationData.new_mobility_index} prevValue={originOutcomes.social_mobility_index} label="Mobility" sublabel="Index (0-10)" color={migrationData.new_mobility_index < 5 ? '#f43f5e' : '#10b981'} format="index" />
              <MetricRing value={migrationData.new_expected_income_eur} prevValue={originOutcomes.expected_monthly_income_eur} label="Income" sublabel="€/mo" color="#4f46e5" format="eur" />
            </div>
          </motion.div>
        )}

        {/* Deep Analysis Row */}
        <div className="grid lg:grid-cols-2 gap-6">
          
          {/* Structural Pipeline */}
          <div className="bg-zinc-950/90 border border-zinc-800 rounded-3xl p-6 shadow-2xl flex flex-col">
            <h3 className="text-sm font-bold text-zinc-300 mb-2 flex items-center gap-2 uppercase tracking-wider">
              <Activity size={16} className="text-indigo-400" />
              <T it="Probabilità di Track (Pipeline)" en="Track Probability (Pipeline)" />
            </h3>
            <p className="text-[11px] text-zinc-500 mb-4 flex-shrink-0">
              <T it={`Distribuzione attesa per uno studente con ESCS ${escs === 'low' ? 'Basso' : 'Alto'} in ${originCountry}.`} en={`Expected distribution for a ${escs === 'low' ? 'Low' : 'High'} ESCS student in ${originCountry}.`} />
            </p>
            <div className="flex-1 min-h-[150px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={pipelineData} layout="vertical" margin={{ top: 0, right: 30, left: 0, bottom: 0 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" width={80} stroke="#71717a" tick={{fontSize: 10, fill: '#a1a1aa'}} />
                  <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{backgroundColor: '#18181b', borderColor: '#27272a', fontSize: '12px', borderRadius: '8px'}} formatter={(val) => `${val.toFixed(1)}%`} />
                  <Bar dataKey="prob" radius={[0, 4, 4, 0]}>
                    {pipelineData.map((entry, index) => (
                      <cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Qualitative Data / Structural Deficits */}
          {originCountry === 'Italy' ? (
             <div className="bg-zinc-950/90 border border-zinc-800 rounded-3xl p-6 shadow-2xl flex flex-col">
              <h3 className="text-sm font-bold text-zinc-300 mb-2 flex items-center gap-2 uppercase tracking-wider">
                <AlertCircle size={16} className="text-rose-400" />
                <T it="Deficit Strutturali del Percorso" en="Track Structural Deficits" />
              </h3>
              <div className="flex-1 min-h-[150px] mb-4">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                    <PolarGrid stroke="#27272a" />
                    <PolarAngleAxis dataKey="subject" tick={{fontSize: 9, fill: '#a1a1aa'}} />
                    <PolarRadiusAxis angle={30} domain={[0, 50]} stroke="#52525b" tick={false} axisLine={false} />
                    <Radar name={currentTrackName} dataKey="A" stroke="#818cf8" fill="#818cf8" fillOpacity={0.4} />
                    <Tooltip contentStyle={{backgroundColor: '#18181b', borderColor: '#27272a', fontSize: '12px'}} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
              <div className="bg-zinc-900 border-l-2 border-indigo-500 p-3 rounded-r-lg">
                <p className="text-[11px] italic text-zinc-400">
                  <T it={simData.NARRATIVES.education.it} en={simData.NARRATIVES.education.en} />
                </p>
              </div>
            </div>
          ) : (
            <div className="bg-zinc-950/90 border border-zinc-800 rounded-3xl p-6 shadow-2xl flex flex-col">
              <h3 className="text-sm font-bold text-zinc-300 mb-4 flex items-center gap-2 uppercase tracking-wider">
                <MessageCircle size={16} className="text-emerald-400" />
                <T it="Caratteristiche Sistema" en="System Features" />
              </h3>
              <ul className="space-y-3">
                {originData.key_features.map((feature, i) => (
                  <li key={i} className="text-sm text-zinc-300 flex items-start gap-2">
                    <span className="text-emerald-500 mt-1">•</span> {feature}
                  </li>
                ))}
              </ul>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
