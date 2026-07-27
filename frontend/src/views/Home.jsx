import React from 'react';
import { T } from '../components/T';
import { ArrowRight, Search, Map, GraduationCap, AlertOctagon } from 'lucide-react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import EurydiceComparison from '../components/EurydiceComparison';

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-16 space-y-32">
      
      {/* The Hook (Hero) */}
      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center space-y-8"
      >
        <div className="inline-block px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-sm font-semibold mb-4">
          <T it="Un'Indagine Basata sui Dati" en="A Data-Driven Investigation" />
        </div>
        <h1 className="text-5xl sm:text-7xl font-black tracking-tight leading-tight text-white">
          <T 
            it="Il tuo futuro è già stato deciso." 
            en="Your future has already been decided." 
          />
        </h1>
        <p className="text-zinc-300 text-xl sm:text-2xl leading-relaxed max-w-3xl mx-auto font-light">
          <T 
            it="In Italia, a soli 14 anni, i ragazzi fanno una scelta scolastica che determinerà se andranno all'università o se diventeranno disoccupati. Ma è davvero una scelta libera?" 
            en="In Italy, at just 14 years old, children make a school choice that determines whether they go to university or become unemployed. But is it really a free choice?" 
          />
        </p>
      </motion.section>

      {/* Act I */}
      <motion.section 
        initial={{ opacity: 0, x: -30 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        className="relative flex flex-col md:flex-row gap-12 items-center"
      >
        <div className="md:w-1/3">
          <div className="text-8xl font-black text-white/5 absolute -top-10 -left-6 z-0 pointer-events-none">1</div>
          <div className="relative z-10 w-24 h-24 rounded-full bg-indigo-600 flex items-center justify-center shadow-[0_0_50px_rgba(79,70,229,0.4)]">
            <Map size={40} className="text-white" />
          </div>
        </div>
        <div className="md:w-2/3 space-y-6 relative z-10">
          <h2 className="text-4xl font-bold text-white">
            <T it="Atto I: L'Illusione della Scelta" en="Act I: The Illusion of Choice" />
          </h2>
          <p className="text-xl text-zinc-300 leading-relaxed">
            <T 
              it="Ti dicono che scegli il Liceo o l'Istituto Professionale in base al tuo talento. I nostri dati dimostrano il contrario." 
              en="They tell you that you choose between a Lyceum or a Vocational school based on your talent. Our data proves otherwise." 
            />
          </p>
          <div className="bg-white/5 border border-indigo-500/30 p-6 rounded-2xl">
            <p className="text-lg text-white font-medium">
              <T 
                it="Se nasci in un quartiere ricco, hai l'80% di probabilità di finire al Liceo. Se nasci in un quartiere povero, finirai quasi certamente in un Professionale o Tecnico." 
                en="If you are born in a wealthy neighborhood, you have an 80% chance of ending up in a Lyceum. If you are born in a poor neighborhood, you will almost certainly end up in a Vocational or Technical school." 
              />
            </p>
          </div>
        </div>
      </motion.section>

      {/* Act II */}
      <motion.section 
        initial={{ opacity: 0, x: 30 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        className="relative flex flex-col md:flex-row-reverse gap-12 items-center"
      >
        <div className="md:w-1/3 flex justify-end">
          <div className="text-8xl font-black text-white/5 absolute -top-10 -right-6 z-0 pointer-events-none">2</div>
          <div className="relative z-10 w-24 h-24 rounded-full bg-rose-600 flex items-center justify-center shadow-[0_0_50px_rgba(225,29,72,0.4)]">
            <AlertOctagon size={40} className="text-white" />
          </div>
        </div>
        <div className="md:w-2/3 space-y-6 relative z-10 text-left md:text-right">
          <h2 className="text-4xl font-bold text-white">
            <T it="Atto II: La Doppia Penalizzazione" en="Act II: The Double Penalty" />
          </h2>
          <p className="text-xl text-zinc-300 leading-relaxed">
            <T 
              it="Una volta smistati i ragazzi più poveri nei Professionali, lo Stato li punisce una seconda volta." 
              en="Once the poorest children are sorted into Vocational schools, the State punishes them a second time." 
            />
          </p>
          <div className="bg-white/5 border border-rose-500/30 p-6 rounded-2xl text-left inline-block w-full">
            <p className="text-lg text-white font-medium mb-4">
              <T 
                it="I dati del Ministero mostrano che le scuole Professionali ricevono sistematicamente le risorse peggiori:" 
                en="Ministry data shows that Vocational schools systematically receive the worst resources:" 
              />
            </p>
            <ul className="space-y-2 text-zinc-300 list-disc pl-5">
              <li><T it="Edifici vecchi, non sicuri e con barriere architettoniche." en="Old, unsafe buildings with architectural barriers." /></li>
              <li><T it="Insegnanti precari che cambiano ogni anno, impedendo la continuità." en="Precarious teachers who change every year, preventing continuity." /></li>
            </ul>
          </div>
        </div>
      </motion.section>

      {/* Act III */}
      <motion.section 
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        className="relative flex flex-col md:flex-row gap-12 items-center"
      >
        <div className="md:w-1/3">
          <div className="text-8xl font-black text-white/5 absolute -top-10 -left-6 z-0 pointer-events-none">3</div>
          <div className="relative z-10 w-24 h-24 rounded-full bg-amber-500 flex items-center justify-center shadow-[0_0_50px_rgba(245,158,11,0.4)]">
            <GraduationCap size={40} className="text-white" />
          </div>
        </div>
        <div className="md:w-2/3 space-y-6 relative z-10">
          <h2 className="text-4xl font-bold text-white">
            <T it="Atto III: Il Risultato (NEET)" en="Act III: The Destination (NEET)" />
          </h2>
          <p className="text-xl text-zinc-300 leading-relaxed">
            <T 
              it="Questa divisione a 14 anni non è un incidente. È una catena di montaggio che produce disuguaglianza." 
              en="This division at age 14 is not an accident. It is an assembly line that manufactures inequality." 
            />
          </p>
          <div className="bg-amber-500/10 border border-amber-500/30 p-6 rounded-2xl">
            <p className="text-2xl font-bold text-amber-400 mb-2">19%</p>
            <p className="text-lg text-white">
              <T 
                it="Quasi un giovane su cinque in Italia finisce per non studiare e non lavorare (NEET). Non perché sono pigri, ma perché il sistema li ha inseriti in un percorso a ostacoli insuperabile." 
                en="Almost one in five young people in Italy ends up not studying and not working (NEET). Not because they are lazy, but because the system put them in an unbeatable obstacle course." 
              />
            </p>
          </div>
        </div>
      </motion.section>

      {/* Eurydice Integration */}
      <motion.section
        initial={{ opacity: 0, scale: 0.95 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.6 }}
      >
        <EurydiceComparison />
      </motion.section>

      {/* Call to Action */}
      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center pb-24 relative z-10"
      >
        <div className="bg-white/[0.03] border border-white/10 p-12 rounded-3xl backdrop-blur-xl">
          <h3 className="text-3xl font-bold mb-6 text-white">
            <T it="Mettiamo alla prova il sistema." en="Let's put the system to the test." />
          </h3>
          <p className="text-zinc-400 mb-8 max-w-xl mx-auto text-lg">
            <T 
              it="Usa il nostro Simulatore OED interattivo. Scegli un profilo studente e guarda come i numeri del Ministero determinano il suo destino matematicamente." 
              en="Use our interactive OED Simulator. Choose a student profile and watch how the Ministry's numbers mathematically determine their fate." 
            />
          </p>
          <Link to="/simulator" className="inline-flex items-center gap-3 px-8 py-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition shadow-[0_0_30px_rgba(79,70,229,0.5)] text-lg">
            <T it="Vai al Simulatore Matematico" en="Launch the Mathematical Simulator" />
            <ArrowRight size={20} />
          </Link>
        </div>
      </motion.section>

    </div>
  );
}
