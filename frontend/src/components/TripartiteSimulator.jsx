import React, { useState, useEffect } from 'react';
import { T } from './T';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, Briefcase, GraduationCap, Clock, Euro, Users, AlertTriangle, ArrowRight } from 'lucide-react';
import { Loader2 } from 'lucide-react';

export default function TripartiteSimulator() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTrack, setActiveTrack] = useState('liceo');

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/tripartite_curriculum.json`)
      .then(res => res.json())
      .then(d => {
        setData(d.tracks);
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

  const track = data.find(t => t.id === activeTrack);

  return (
    <div className="space-y-8 py-8">
      
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-12">
        <h2 className="text-3xl font-bold text-white mb-4">
          <T it="Simulatore dell'Esperienza Tripartita" en="Tripartite Experience Simulator" />
        </h2>
        <p className="text-zinc-400 text-lg">
          <T 
            it="Seleziona un percorso per esplorare le differenze curriculari, i costi e il destino statistico degli studenti a partire dai 14 anni." 
            en="Select a track to explore the curricular differences, costs, and statistical destiny of students starting at age 14." 
          />
        </p>
      </div>

      {/* Track Selector */}
      <div className="flex flex-col sm:flex-row gap-4 max-w-4xl mx-auto justify-center px-4">
        {data.map((t) => (
          <button
            key={t.id}
            onClick={() => setActiveTrack(t.id)}
            className={`flex-1 p-6 rounded-2xl border transition-all ${
              activeTrack === t.id
                ? 'bg-indigo-600/10 border-indigo-500 shadow-[0_0_30px_rgba(99,102,241,0.15)] scale-[1.02]'
                : 'bg-zinc-900 border-zinc-800 hover:bg-zinc-800'
            }`}
          >
            <h3 className={`text-xl font-bold mb-2 ${activeTrack === t.id ? 'text-white' : 'text-zinc-300'}`}>
              <T it={t.name.it} en={t.name.en} />
            </h3>
            <p className="text-xs text-zinc-500 line-clamp-2">
              <T it={t.description.it} en={t.description.en} />
            </p>
          </button>
        ))}
      </div>

      {/* Track Details Dashboard */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTrack}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="max-w-6xl mx-auto px-4 mt-12 grid grid-cols-1 lg:grid-cols-3 gap-6"
        >
          {/* Main Info Column */}
          <div className="lg:col-span-2 space-y-6">
            
            <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8">
              <div className="flex items-center gap-3 mb-6">
                <BookOpen className="text-indigo-400" size={24} />
                <h3 className="text-2xl font-bold text-white"><T it="Piano di Studi" en="Curriculum" /></h3>
              </div>
              
              <div className="space-y-3">
                {track.curriculum.map((subj, idx) => (
                  <div key={idx} className="flex items-center justify-between p-4 bg-zinc-950 rounded-xl border border-white/5">
                    <span className="font-medium text-zinc-200"><T it={subj.subject.it} en={subj.subject.en} /></span>
                    <div className="flex items-center gap-2">
                      <span className="text-indigo-400 font-bold">{subj.hours}</span>
                      <span className="text-xs text-zinc-500 uppercase tracking-wider"><T it="ore/sett" en="hrs/wk" /></span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-indigo-950/20 border border-indigo-500/20 rounded-3xl p-8">
              <div className="flex items-center gap-3 mb-4">
                <Users className="text-indigo-400" size={24} />
                <h3 className="text-xl font-bold text-white"><T it="Composizione Sociale" en="Social Composition" /></h3>
              </div>
              <p className="text-zinc-300 leading-relaxed">
                <T it={track.demographics.it} en={track.demographics.en} />
              </p>
            </div>

          </div>

          {/* Stats Column */}
          <div className="space-y-6">
            
            <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 flex items-center gap-4">
              <div className="p-4 bg-rose-500/10 rounded-2xl">
                <Euro className="text-rose-400" size={32} />
              </div>
              <div>
                <p className="text-xs text-zinc-500 uppercase tracking-wider font-bold mb-1"><T it="Costo Libri (Annuo)" en="Textbook Cost (Yearly)" /></p>
                <p className="text-3xl font-black text-white">€{track.textbookCost}</p>
              </div>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 flex items-center gap-4">
              <div className="p-4 bg-amber-500/10 rounded-2xl">
                <Briefcase className="text-amber-400" size={32} />
              </div>
              <div>
                <p className="text-xs text-zinc-500 uppercase tracking-wider font-bold mb-1"><T it="Ore Lavoro FSL" en="FSL Labor Hours" /></p>
                <p className="text-3xl font-black text-white">{track.fslHours} <span className="text-base text-zinc-500 font-normal">ore</span></p>
              </div>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 flex items-center gap-4">
              <div className="p-4 bg-red-500/10 rounded-2xl">
                <AlertTriangle className="text-red-400" size={32} />
              </div>
              <div>
                <p className="text-xs text-zinc-500 uppercase tracking-wider font-bold mb-1"><T it="Dispersione Implicita" en="Implicit Dropout" /></p>
                <p className="text-3xl font-black text-white">{track.implicitDropout}</p>
              </div>
            </div>

            <div className="bg-emerald-950/20 border border-emerald-500/20 rounded-3xl p-8 flex items-center gap-4">
              <div className="p-4 bg-emerald-500/20 rounded-2xl">
                <GraduationCap className="text-emerald-400" size={32} />
              </div>
              <div>
                <p className="text-xs text-emerald-500/70 uppercase tracking-wider font-bold mb-1"><T it="Iscrizione Università" en="Uni Enrollment" /></p>
                <p className="text-3xl font-black text-emerald-400">{track.universityEnrollment}</p>
              </div>
            </div>

          </div>
        </motion.div>
      </AnimatePresence>

    </div>
  );
}
