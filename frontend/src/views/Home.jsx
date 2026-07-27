import React from 'react';
import { T } from '../components/T';
import { ArrowRight, BookOpen, AlertTriangle, Building2, Database } from 'lucide-react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12 space-y-24">
      
      {/* Hero Section */}
      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center space-y-6"
      >
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-black tracking-tight leading-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400">
          <T 
            it="Il futuro di uno studente in Italia non è casuale. È misurabile." 
            en="A student's future in Italy is not random. It is measurable." 
          />
        </h1>
        <p className="text-zinc-400 text-lg sm:text-xl leading-relaxed max-w-2xl mx-auto">
          <T 
            it="Questo osservatorio unisce per la prima volta 681 dataset ufficiali da ISTAT, Ministero dell'Istruzione, MUR, Eurostat, OCSE e INVALSI in un unico punto di accesso aperto e verificabile." 
            en="This observatory unifies 681 official datasets from ISTAT, Ministry of Education, MUR, Eurostat, OECD and INVALSI into a single open, verifiable access point." 
          />
        </p>
        <div className="pt-8 flex justify-center gap-4">
          <Link to="/simulator" className="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition flex items-center gap-2 shadow-lg shadow-indigo-500/25">
            <T it="Avvia Simulatore OED" en="Launch OED Simulator" />
            <ArrowRight size={18} />
          </Link>
          <Link to="/catalog" className="px-6 py-3 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white font-bold transition flex items-center gap-2 border border-zinc-700">
            <T it="Sfoglia Dati (681)" en="Browse Data (681)" />
            <Database size={18} />
          </Link>
        </div>
      </motion.section>

      {/* The Tripartite Illusion */}
      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.6 }}
        className="relative space-y-8 bg-white/[0.02] backdrop-blur-xl p-8 sm:p-12 rounded-3xl border border-white/10 shadow-2xl overflow-hidden group hover:border-white/20 transition-all"
      >
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
        <div className="relative z-10 flex items-center gap-4 text-indigo-400 mb-6">
          <BookOpen size={24} />
          <h2 className="text-2xl font-bold text-white">
            <T it="L'Illusione della Scelta Tripartita" en="The Tripartite Illusion" />
          </h2>
        </div>
        <div className="prose prose-invert max-w-none space-y-6 text-zinc-300">
          <p className="text-lg">
            <T 
              it="Il sistema educativo italiano si basa su una divisione a 14 anni in tre canali: Licei, Istituti Tecnici e Istituti Professionali. Formalmente, è una scelta basata sulle attitudini. Nei dati, è una segregazione basata sul reddito." 
              en="The Italian educational system is based on a division at age 14 into three channels: Lyceums, Technical Institutes, and Vocational Institutes. Formally, it's a choice based on aptitude. In the data, it's segregation based on income." 
            />
          </p>
          <p>
            <T 
              it="Incrociando i dati del Ministero dell'Economia (MEF) con le iscrizioni del MIM, scopriamo che la probabilità di frequentare un liceo scala perfettamente con l'imponibile IRPEF del quartiere di provenienza." 
              en="By crossing Ministry of Economy (MEF) tax data with MIM enrollment data, we discover that the probability of attending a lyceum scales perfectly with the taxable income of the student's neighborhood." 
            />
          </p>
        </div>
      </motion.section>

      {/* The Double Penalty */}
      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.6 }}
        className="relative space-y-8 bg-white/[0.02] backdrop-blur-xl p-8 sm:p-12 rounded-3xl border border-white/10 shadow-2xl overflow-hidden group hover:border-white/20 transition-all"
      >
        <div className="absolute inset-0 bg-gradient-to-br from-rose-500/5 to-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
        <div className="relative z-10 flex items-center gap-4 text-rose-400 mb-6">
          <AlertTriangle size={24} />
          <h2 className="text-2xl font-bold text-white">
            <T it="La Doppia Penalizzazione Strutturale" en="The Structural Double Penalty" />
          </h2>
        </div>
        <div className="prose prose-invert max-w-none space-y-6 text-zinc-300">
          <p>
            <T 
              it="Non solo gli studenti di classe operaia vengono indirizzati verso gli istituti tecnici e professionali, ma lo Stato sotto-finanzia attivamente queste stesse strutture." 
              en="Not only are working-class students funneled into technical and vocational institutes, but the State actively underfunds these exact structures." 
            />
          </p>
          <ul className="space-y-4 my-6">
            <li className="flex items-start gap-3">
              <Building2 className="mt-1 text-zinc-500 shrink-0" size={18} />
              <span>
                <strong className="text-white"><T it="Edilizia (Edifici):" en="Infrastructure (Buildings):" /></strong>{' '}
                <T 
                  it="I dati sulle barriere architettoniche e l'agibilità dimostrano che i professionali operano nelle strutture più fatiscenti." 
                  en="Architectural barrier and safety data show that vocational schools operate in the most dilapidated structures." 
                />
              </span>
            </li>
            <li className="flex items-start gap-3">
              <BookOpen className="mt-1 text-zinc-500 shrink-0" size={18} />
              <span>
                <strong className="text-white"><T it="Precariato (Docenti):" en="Precarity (Teachers):" /></strong>{' '}
                <T 
                  it="Gli insegnanti di ruolo vincono concorsi e chiedono trasferimento nei Licei. Il risultato è un turnover devastante nei professionali, dove si concentra il precariato (supplenze annuali)." 
                  en="Tenured teachers win competitions and request transfers to Lyceums. The result is devastating turnover in vocational schools, where precarious annual substitute teaching is concentrated." 
                />
              </span>
            </li>
          </ul>
        </div>
      </motion.section>

      {/* Call to Action */}
      <motion.section 
        initial={{ opacity: 0, scale: 0.95 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="text-center pb-12 relative z-10"
      >
        <h3 className="text-2xl font-bold mb-6">
          <T it="Vuoi vedere i numeri in azione?" en="Want to see the numbers in action?" />
        </h3>
        <Link to="/simulator" className="inline-flex px-8 py-4 rounded-xl bg-white text-black font-bold hover:bg-zinc-200 transition shadow-xl">
          <T it="Vai al Simulatore Matematico" en="Go to the Mathematical Simulator" />
        </Link>
      </motion.section>

    </div>
  );
}

