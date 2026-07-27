import React, { useState } from 'react';
import { Book, X } from 'lucide-react';
import { T } from './T';
import { motion, AnimatePresence } from 'framer-motion';

export default function GlossaryModal() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button 
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 bg-indigo-600 hover:bg-indigo-500 text-white p-4 rounded-full shadow-2xl shadow-indigo-500/50 flex items-center justify-center transition-all hover:scale-105"
        title="Concepts Dictionary"
      >
        <Book size={24} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
          >
            <motion.div 
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="bg-zinc-900 border border-zinc-700 rounded-2xl w-full max-w-2xl max-h-[80vh] overflow-y-auto shadow-2xl relative"
            >
              <button 
                onClick={() => setIsOpen(false)}
                className="absolute top-4 right-4 text-zinc-400 hover:text-white bg-zinc-800 p-2 rounded-full"
              >
                <X size={20} />
              </button>

              <div className="p-8 space-y-6">
                <h2 className="text-3xl font-bold border-b border-zinc-700 pb-4">
                  <T it="Dizionario dei Concetti" en="Concepts Dictionary" />
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <h3 className="text-xl font-bold text-indigo-400">NEET</h3>
                    <p className="text-zinc-300">
                      <T 
                        it="Giovani tra i 15 e i 29 anni che non studiano, non lavorano e non sono in formazione (Not in Education, Employment, or Training). In Italia il tasso supera il 19%." 
                        en="Young people aged 15-29 who are Not in Education, Employment, or Training. In Italy, this rate exceeds 19%." 
                      />
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-indigo-400"><T it="Modello O.E.D." en="O.E.D. Framework" /></h3>
                    <p className="text-zinc-300">
                      <T 
                        it="Origine (la ricchezza della tua famiglia) → Educazione (la scuola in cui vieni messo) → Destinazione (il tuo futuro lavoro)." 
                        en="Origin (your family's wealth) → Education (the school you are sorted into) → Destination (your future career outcome)." 
                      />
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-rose-400"><T it="Sistema Tripartito" en="Tripartite System" /></h3>
                    <p className="text-zinc-300">
                      <T 
                        it="Il sistema italiano che costringe i bambini a scegliere a soli 14 anni tra Liceo (per i ricchi), Tecnico (per la classe media) e Professionale (per i poveri)." 
                        en="The Italian system that forces 14-year-olds to choose between Lyceum (for the wealthy), Technical (for the middle class), and Vocational (for the working class)." 
                      />
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-rose-400"><T it="Doppia Penalizzazione" en="Double Penalty" /></h3>
                    <p className="text-zinc-300">
                      <T 
                        it="Quando gli studenti più poveri vengono mandati nelle scuole peggiori (Istituti Professionali) che hanno gli edifici più rotti e gli insegnanti più precari. Lo Stato punisce chi ha già meno." 
                        en="When the poorest students are sent to the worst schools (Vocational) which have the most broken buildings and precarious teachers. The State punishes those who already have less." 
                      />
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
