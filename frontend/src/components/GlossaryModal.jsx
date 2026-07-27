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
        title="Glossary of Terms"
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
                  <T it="Glossario Metriche" en="Metrics Glossary" />
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <h3 className="text-xl font-bold text-indigo-400">NEET Rate</h3>
                    <p className="text-zinc-300">
                      <T 
                        it="Percentuale della popolazione giovanile (15-29 anni) non inserita in percorsi di istruzione, formazione o lavoro (Not in Education, Employment, or Training)." 
                        en="Percentage of the youth population (aged 15-29) who are Not in Education, Employment, or Training." 
                      />
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-indigo-400">O.E.D. Framework</h3>
                    <p className="text-zinc-300">
                      <T 
                        it="Paradigma sociologico che quantifica l'effetto dell'Origine (status socio-economico familiare) e dell'Educazione (percorso scolastico) sulla Destinazione (esito occupazionale e reddituale)." 
                        en="Sociological paradigm quantifying the effect of Origin (family socio-economic status) and Education (schooling track) on Destination (occupational and income outcomes)." 
                      />
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-indigo-400"><T it="Sistema Tripartito" en="Tripartite System" /></h3>
                    <p className="text-zinc-300">
                      <T 
                        it="Modello educativo caratterizzato da uno smistamento precoce (tracking) degli studenti in percorsi accademici, tecnici o professionali." 
                        en="Educational model characterized by early tracking of students into distinct academic, technical, or vocational pathways." 
                      />
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-indigo-400"><T it="Indice di Segregazione Sociale" en="Social Segregation Index" /></h3>
                    <p className="text-zinc-300">
                      <T 
                        it="Misura statistica della concentrazione di studenti provenienti da contesti socio-economici simili all'interno degli stessi istituti o indirizzi scolastici." 
                        en="Statistical measure of the concentration of students from similar socio-economic backgrounds within the same schools or educational tracks." 
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
