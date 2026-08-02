import React, { useState, useEffect } from 'react';
import { T } from './T';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, Briefcase, GraduationCap, Clock, Euro, Users, AlertTriangle, ChevronRight } from 'lucide-react';
import { Loader2 } from 'lucide-react';

export default function TripartiteSimulator() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const [activeMacro, setActiveMacro] = useState('liceo');
  const [activeSpecific, setActiveSpecific] = useState('liceo_classico');

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/tripartite_curriculum.json`)
      .then(res => res.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load curriculum data:", err);
        setLoading(false);
      });
  }, []);

  if (loading || !data) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="animate-spin text-indigo-500" size={32} />
      </div>
    );
  }

  // Handle Macro Track Selection
  const handleMacroSelect = (macroId) => {
    setActiveMacro(macroId);
    // Auto-select the first specific track in that category
    const firstSpecific = data.specificTracks.find(t => t.macroTrackId === macroId);
    if (firstSpecific) {
      setActiveSpecific(firstSpecific.id);
    }
  };

  const currentSpecificTracks = data.specificTracks.filter(t => t.macroTrackId === activeMacro);
  const track = data.specificTracks.find(t => t.id === activeSpecific) || currentSpecificTracks[0];

  return (
    <div className="space-y-8 py-8">
      
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <h2 className="text-3xl font-bold text-white mb-4">
          <T it="Simulatore dell'Esperienza Tripartita" en="Tripartite Experience Simulator" />
        </h2>
        <p className="text-zinc-400 text-lg">
          <T 
            it="Esplora i curricula specifici, i costi occulti e l'impatto statistico di ogni singolo indirizzo scolastico italiano." 
            en="Explore the specific curricula, hidden costs, and statistical impact of every single Italian high school track." 
          />
        </p>
      </div>

      {/* Tier 1: Macro Track Selector */}
      <div className="flex flex-col sm:flex-row gap-4 max-w-4xl mx-auto justify-center px-4 mb-6">
        {data.macroTracks.map((m) => (
          <button
            key={m.id}
            onClick={() => handleMacroSelect(m.id)}
            className={`flex-1 p-4 rounded-xl border transition-all ${
              activeMacro === m.id
                ? 'bg-indigo-600/20 border-indigo-500 shadow-[0_0_20px_rgba(99,102,241,0.15)]'
                : 'bg-zinc-900 border-zinc-800 hover:bg-zinc-800'
            }`}
          >
            <h3 className={`text-lg font-bold ${activeMacro === m.id ? 'text-white' : 'text-zinc-400'}`}>
              <T it={m.name.it} en={m.name.en} />
            </h3>
            <p className={`text-xs ${activeMacro === m.id ? 'text-indigo-300' : 'text-zinc-600'}`}>
              <T it={m.description.it} en={m.description.en} />
            </p>
          </button>
        ))}
      </div>

      {/* Tier 2: Specific Track Selector */}
      <div className="max-w-6xl mx-auto px-4 mb-12">
        <div className="flex flex-wrap justify-center gap-2 p-2 bg-zinc-900/50 rounded-2xl border border-zinc-800/50">
          {currentSpecificTracks.map((t) => (
            <button
              key={t.id}
              onClick={() => setActiveSpecific(t.id)}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
                activeSpecific === t.id
                  ? 'bg-indigo-500 text-white shadow-md'
                  : 'text-zinc-400 hover:text-white hover:bg-zinc-800'
              }`}
            >
              <T it={t.name.it} en={t.name.en} />
            </button>
          ))}
        </div>
      </div>

      {/* Track Details Dashboard */}
      {track && (
        <AnimatePresence mode="wait">
          <motion.div
            key={activeSpecific}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -15 }}
            transition={{ duration: 0.2 }}
            className="max-w-6xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-3 gap-6"
          >
            {/* Main Info Column */}
            <div className="lg:col-span-2 space-y-6">
              
              <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-6 sm:p-8">
                <div className="mb-6">
                  <h3 className="text-2xl font-bold text-white mb-2">
                    <T it={track.name.it} en={track.name.en} />
                  </h3>
                  <p className="text-zinc-400 text-sm leading-relaxed">
                    <T it={track.description.it} en={track.description.en} />
                  </p>
                </div>

                <div className="flex items-center gap-3 mb-4 mt-8">
                  <BookOpen className="text-indigo-400" size={20} />
                  <h4 className="text-lg font-bold text-white"><T it="Piano di Studi (Triennio)" en="Curriculum (Triennum)" /></h4>
                </div>
                
                <div className="space-y-2">
                  {track.curriculum.map((subj, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-zinc-950 rounded-lg border border-white/5 hover:border-white/10 transition-colors">
                      <span className="font-medium text-zinc-300 text-sm"><T it={subj.subject.it} en={subj.subject.en} /></span>
                      <div className="flex items-center gap-2 bg-indigo-500/10 px-3 py-1 rounded-md">
                        <span className="text-indigo-400 font-bold">{subj.hours}</span>
                        <span className="text-[10px] text-indigo-400/70 uppercase tracking-wider"><T it="ore/sett" en="hrs/wk" /></span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-indigo-950/20 border border-indigo-500/20 rounded-3xl p-6 sm:p-8">
                <div className="flex items-center gap-3 mb-3">
                  <Users className="text-indigo-400" size={20} />
                  <h4 className="text-lg font-bold text-white"><T it="Composizione Sociale" en="Social Composition" /></h4>
                </div>
                <p className="text-indigo-200/80 leading-relaxed text-sm">
                  <T it={track.demographics.it} en={track.demographics.en} />
                </p>
              </div>

            </div>

            {/* Stats Column */}
            <div className="space-y-4">
              
              <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-6 flex items-center gap-4">
                <div className="p-3 bg-rose-500/10 rounded-xl">
                  <Euro className="text-rose-400" size={24} />
                </div>
                <div>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-wider font-bold mb-1"><T it="Costo Libri (Annuo)" en="Textbook Cost (Yearly)" /></p>
                  <p className="text-2xl font-black text-white">€{track.textbookCost}</p>
                </div>
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-6 flex items-center gap-4">
                <div className="p-3 bg-amber-500/10 rounded-xl">
                  <Briefcase className="text-amber-400" size={24} />
                </div>
                <div>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-wider font-bold mb-1"><T it="Ore Lavoro FSL/PCTO" en="FSL/PCTO Labor Hours" /></p>
                  <p className="text-2xl font-black text-white">{track.fslHours}</p>
                </div>
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-6 flex items-center gap-4">
                <div className="p-3 bg-red-500/10 rounded-xl">
                  <AlertTriangle className="text-red-400" size={24} />
                </div>
                <div>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-wider font-bold mb-1"><T it="Dispersione Implicita" en="Implicit Dropout" /></p>
                  <p className="text-2xl font-black text-white">{track.implicitDropout}</p>
                </div>
              </div>

              <div className="bg-emerald-950/20 border border-emerald-500/20 rounded-3xl p-6 flex items-center gap-4">
                <div className="p-3 bg-emerald-500/20 rounded-xl">
                  <GraduationCap className="text-emerald-400" size={24} />
                </div>
                <div>
                  <p className="text-[10px] text-emerald-500/70 uppercase tracking-wider font-bold mb-1"><T it="Iscrizione Università" en="Uni Enrollment" /></p>
                  <p className="text-2xl font-black text-emerald-400">{track.universityEnrollment}</p>
                </div>
              </div>

            </div>
          </motion.div>
        </AnimatePresence>
      )}
    </div>
  );
}
