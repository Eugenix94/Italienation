import React from 'react';
import { T } from '../components/T';
import { ShieldCheck, BookOpen, Database, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Methodology() {
  const FadeInSection = ({ children, delay = 0 }) => (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.5, delay }}
      className="w-full"
    >
      {children}
    </motion.div>
  );

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 space-y-16">
      
      {/* Header */}
      <div className="space-y-6 border-b border-zinc-800 pb-12">
        <div className="inline-flex items-center justify-center p-3 bg-indigo-500/10 rounded-xl mb-2">
          <BookOpen size={32} className="text-indigo-400" />
        </div>
        <h1 className="text-4xl md:text-5xl font-black text-white tracking-tight">
          <T it="Metodologia & Validazione Scientifica" en="Methodology & Scientific Validation" />
        </h1>
        <p className="text-zinc-400 text-xl font-light leading-relaxed">
          <T 
            it="Un resoconto trasparente della provenienza dei dati, dei modelli econometrici e dei limiti strutturali alla base dell'Osservatorio." 
            en="A transparent account of data provenance, econometric models, and structural limitations underpinning the Observatory." 
          />
        </p>
      </div>

      {/* Accountability */}
      <FadeInSection>
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <ShieldCheck className="text-emerald-500" />
            <T it="Accountability e Provenienza dei Dati" en="Data Accountability and Provenance" />
          </h2>
          <div className="prose prose-invert max-w-none text-zinc-300">
            <p>
              <T 
                it="L'intero ecosistema di Italienation è fondato su un principio rigoroso di accountability empirica. Nessun dato presentato nell'applicazione è frutto di simulazioni arbitrarie. Il sistema aggrega 681 dataset primari estratti direttamente dai database governativi." 
                en="The entire Italienation ecosystem is founded on a rigorous principle of empirical accountability. No data presented in the application is the result of arbitrary simulations. The system aggregates 681 primary datasets extracted directly from government databases." 
              />
            </p>
            <ul className="list-disc pl-5 space-y-2 mt-4 text-zinc-400">
              <li><strong>MIM (Ministero dell'Istruzione e del Merito):</strong> Dati su anagrafe studenti, edilizia scolastica (Scuola in Chiaro), costi dei libri di testo e composizione del corpo docenti.</li>
              <li><strong>INVALSI:</strong> Matrici ESCS (Economic, Social, and Cultural Status) per mappare l'estrazione socio-economica e microdati sui risultati in matematica e italiano per indirizzo.</li>
              <li><strong>MUR (Ministero dell'Università):</strong> Tassi di immatricolazione, abbandono al primo anno, e crediti (CFU) acquisiti incrociati per diploma di provenienza (AlmaLaurea).</li>
              <li><strong>ISTAT & Unioncamere:</strong> Transizione scuola-lavoro, tassi NEET (Not in Education, Employment, or Training), indagini Excelsior sul mismatch delle competenze.</li>
            </ul>
          </div>
        </div>
      </FadeInSection>

      {/* Econometric Logic */}
      <FadeInSection>
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <Database className="text-indigo-400" />
            <T it="Logica Causal-Strutturale del Modello O.E.D." en="Causal-Structural Logic of the O.E.D. Model" />
          </h2>
          <div className="prose prose-invert max-w-none text-zinc-300">
            <p>
              <T 
                it="Il simulatore O.E.D. (Origine, Educazione, Destinazione) mappa le disuguaglianze strutturali attraverso un modello probabilistico. L'Origin (Origine) è definita dall'indice ESCS. Abbiamo quantificato che la provenienza da una famiglia del primo quintile ESCS (es. genitori con licenza media) aumenta esponenzialmente la probabilità di essere iscritti a un Istituto Professionale, dove il tasso di bocciatura al primo anno (filtro selettivo) supera il 14.8%." 
                en="The O.E.D. (Origin, Education, Destination) simulator maps structural inequalities through a probabilistic model. Origin is defined by the ESCS index. We quantified that coming from a Q1 ESCS family (e.g., parents with middle school education) exponentially increases the probability of enrollment in a Vocational Institute, where the first-year retention rate (selective filter) exceeds 14.8%." 
              />
            </p>
            <p className="mt-4">
              <T 
                it="La Destinazione (Destination) viene poi tracciata misurando come il diploma acquisito determini rigidamente l'accesso terziario e il successo sul mercato del lavoro. Il paradosso italiano è evidente: a fronte di un tasso NEET giovanile del 19%, il 45% delle aziende (dati Excelsior) non riesce a reperire le competenze tecniche adeguate, a causa di una svalutazione sistemica dell'istruzione professionale." 
                en="Destination is then tracked by measuring how the acquired diploma rigidly dictates tertiary access and labor market success. The Italian paradox is stark: against a youth NEET rate of 19%, 45% of companies (Excelsior data) cannot find adequate technical skills, due to a systemic devaluation of vocational education." 
              />
            </p>
          </div>
        </div>
      </FadeInSection>

      {/* Limitations */}
      <FadeInSection>
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-white flex items-center gap-3">
            <AlertTriangle className="text-amber-500" />
            <T it="Limiti del Dataset e Blind Spots" en="Dataset Limitations and Blind Spots" />
          </h2>
          <div className="bg-amber-500/10 border border-amber-500/20 p-6 rounded-2xl prose prose-invert max-w-none text-amber-200/80">
            <p>
              <T 
                it="In ossequio al rigore accademico, riconosciamo i seguenti limiti strutturali nell'attuale architettura dei dati:" 
                en="In adherence to academic rigor, we acknowledge the following structural limitations in the current data architecture:" 
              />
            </p>
            <ul className="list-disc pl-5 mt-4 space-y-2">
              <li><strong>Granularità PNRR:</strong> I dati sui fondi PNRR (Scuola 4.0, Messa in sicurezza) spesso mancano di granularità a livello di singolo plesso per i comuni minori, impedendo una mappatura micro-territoriale perfetta.</li>
              <li><strong>Dispersione Implicita (Invalsi):</strong> La misurazione della 'dispersione implicita' (studenti che si diplomano senza competenze base) soffre del tasso di cheating nei test INVALSI al Sud, che l'istituto tenta di correggere statisticamente, ma che mantiene un margine di errore.</li>
              <li><strong>Dati longitudinali:</strong> Nonostante ISTAT fornisca indagini campionarie eccellenti sulle coorti, manca un vero e proprio anagrafe longitudinale universale (student tracking system) che segua il singolo individuo dalla scuola dell'infanzia fino ai 30 anni in modo anonimizzato continuo.</li>
            </ul>
          </div>
        </div>
      </FadeInSection>

    </div>
  );
}
