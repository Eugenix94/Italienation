import React, { useState } from 'react';
import { T } from './T';
import { motion } from 'framer-motion';
import { BookOpen, GraduationCap, Map, Users, AlertTriangle, TrendingDown, Clock, Search } from 'lucide-react';

const glossaryTerms = [
  {
    id: 'escs',
    icon: Users,
    term: { it: 'Indice ESCS', en: 'ESCS Index' },
    subtitle: { it: 'Economic, Social and Cultural Status', en: 'Economic, Social and Cultural Status' },
    definition: {
      it: "Un indicatore sintetico utilizzato a livello internazionale (OCSE PISA) che misura il background socio-economico e culturale di uno studente. È calcolato in base al livello di istruzione dei genitori, alla loro occupazione e ai beni materiali e culturali presenti a casa (es. numero di libri, connessione internet).",
      en: "A synthetic indicator used internationally (OECD PISA) that measures a student's socio-economic and cultural background. It is calculated based on parents' education level, their occupation, and material and cultural possessions at home (e.g., number of books, internet connection)."
    },
    impact: {
      it: "In Italia, l'ESCS è il fattore primario che determina la scelta della scuola superiore, trasformando il sistema scolastico in un meccanismo di segregazione di classe.",
      en: "In Italy, ESCS is the primary factor determining high school choice, turning the school system into a mechanism for class segregation."
    }
  },
  {
    id: 'tripartite',
    icon: Map,
    term: { it: 'Sistema Tripartito', en: 'Tripartite System' },
    subtitle: { it: 'La divisione a 14 anni', en: 'The tracking at age 14' },
    definition: {
      it: "Il modello scolastico italiano che, alla fine della scuola media (14 anni), obbliga gli studenti a scegliere tra tre percorsi nettamente separati: Liceo (teorico/accademico), Istituto Tecnico (intermedio) e Istituto Professionale (lavoro manuale/pratico).",
      en: "The Italian school model that, at the end of middle school (age 14), forces students to choose between three strictly separated paths: Lyceum (theoretical/academic), Technical Institute (intermediate), and Vocational Institute (manual/practical work)."
    },
    impact: {
      it: "A differenza dei sistemi comprensivi (es. paesi anglosassoni) dove gli studenti restano insieme più a lungo, il sistema tripartito italiano cristallizza le disuguaglianze sociali in età precoce.",
      en: "Unlike comprehensive systems (e.g., Anglo-Saxon countries) where students stay together longer, the Italian tripartite system crystallizes social inequalities at an early age."
    }
  },
  {
    id: 'implicit-dropout',
    icon: AlertTriangle,
    term: { it: 'Dispersione Implicita', en: 'Implicit Dropout' },
    subtitle: { it: 'Diplomati senza competenze base', en: 'Graduates without basic skills' },
    definition: {
      it: "Studenti che ottengono regolarmente il diploma di maturità, ma che dai test INVALSI risultano non aver raggiunto le competenze minime di base (Matematica, Italiano, Inglese) previste dopo 13 anni di scuola.",
      en: "Students who formally obtain their high school diploma, but who, according to INVALSI standardized tests, have not reached the minimum basic skills (Math, Italian, English) expected after 13 years of schooling."
    },
    impact: {
      it: "Al Sud Italia e nelle Isole, la dispersione implicita supera spesso il 15%, creando un'illusione ottica sulle reali statistiche educative.",
      en: "In Southern Italy and the Islands, implicit dropout often exceeds 15%, creating an optical illusion regarding true educational statistics."
    }
  },
  {
    id: 'pcto',
    icon: Clock,
    term: { it: 'FSL / ex PCTO', en: 'FSL / ex PCTO' },
    subtitle: { it: 'Percorsi per le Competenze Trasversali e per l\'Orientamento', en: 'Pathways for Transversal Skills and Orientation' },
    definition: {
      it: "Ex Alternanza Scuola-Lavoro. Un monte ore obbligatorio (fino a 210 ore nei professionali) che gli studenti devono svolgere presso aziende o enti esterni. In Italia è obbligatorio e non retribuito.",
      en: "Formerly School-Work Alternance. A mandatory number of hours (up to 210 in vocational schools) that students must complete at external companies. In Italy, it is mandatory and entirely unpaid."
    },
    impact: {
      it: "In assenza di un forte tessuto industriale e di tutele, si trasforma spesso in lavoro gratuito o manodopera a basso costo, con gravi problemi di sicurezza.",
      en: "In the absence of a strong industrial fabric and labor protections, it often turns into free labor or cheap workforce, with serious safety issues."
    }
  },
  {
    id: 'bocciatura',
    icon: TrendingDown,
    term: { it: 'Bocciatura', en: 'Grade Retention (Bocciatura)' },
    subtitle: { it: 'Ripetenza scolastica', en: 'Grade repetition' },
    definition: {
      it: "La pratica di far ripetere l'intero anno scolastico a uno studente che non ha raggiunto la sufficienza in diverse materie. L'Italia è uno dei paesi europei che ne fa maggior uso.",
      en: "The practice of making a student repeat the entire school year if they fail multiple subjects. Italy is one of the European countries that uses it the most."
    },
    impact: {
      it: "Estremamente costosa (circa 7.000€ per studente/anno per lo Stato) e fortemente regressiva: colpisce quasi esclusivamente gli studenti degli Istituti Professionali e Tecnici.",
      en: "Extremely expensive (about €7,000 per student/year for the State) and highly regressive: it almost exclusively hits students in Vocational and Technical Institutes."
    }
  }
];

export default function EducationalGuide() {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredTerms = glossaryTerms.filter(term => 
    term.term.it.toLowerCase().includes(searchTerm.toLowerCase()) || 
    term.term.en.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-12 py-12">
      {/* Header Section */}
      <div className="max-w-4xl mx-auto text-center space-y-6">
        <div className="inline-flex items-center justify-center p-4 bg-indigo-500/10 rounded-full mb-4 border border-indigo-500/20">
          <BookOpen className="text-indigo-400" size={32} />
        </div>
        <h1 className="text-4xl md:text-5xl font-black text-white tracking-tight">
          <T it="Guida ai Dati" en="Data Guide" />
        </h1>
        <p className="text-xl text-zinc-400 leading-relaxed max-w-2xl mx-auto">
          <T 
            it="Comprendi il gergo tecnico e i meccanismi nascosti del sistema educativo italiano. Una lettura fondamentale prima di esplorare i dati del progetto." 
            en="Understand the technical jargon and hidden mechanisms of the Italian educational system. Essential reading before exploring the project's data." 
          />
        </p>
      </div>

      {/* Search Bar */}
      <div className="max-w-md mx-auto relative">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-zinc-400" size={20} />
        <input 
          type="text"
          placeholder={lang === 'it' ? "Cerca un termine..." : "Search a term..."}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full bg-zinc-900 border border-zinc-800 text-white rounded-2xl py-4 pl-12 pr-4 focus:outline-none focus:border-indigo-500 transition-colors"
        />
      </div>

      {/* Glossary Grid */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-4">
        {filteredTerms.map((term, index) => (
          <motion.div 
            key={term.id}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            viewport={{ once: true }}
            className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8 hover:bg-zinc-900 transition-colors flex flex-col h-full group"
          >
            <div className="flex items-start gap-4 mb-6">
              <div className="p-3 bg-zinc-800 rounded-xl group-hover:bg-indigo-500/20 group-hover:text-indigo-400 text-zinc-400 transition-colors shrink-0">
                <term.icon size={24} />
              </div>
              <div>
                <h3 className="text-xl font-bold text-white mb-1">
                  <T it={term.term.it} en={term.term.en} />
                </h3>
                <p className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">
                  <T it={term.subtitle.it} en={term.subtitle.en} />
                </p>
              </div>
            </div>
            
            <div className="flex-1 space-y-4">
              <p className="text-zinc-300 leading-relaxed text-sm">
                <T it={term.definition.it} en={term.definition.en} />
              </p>
              
              <div className="bg-indigo-500/5 border-l-2 border-indigo-500/30 p-4 rounded-r-xl">
                <p className="text-xs font-bold text-indigo-400 mb-1 uppercase tracking-wider">
                  <T it="Impatto Sistemico" en="Systemic Impact" />
                </p>
                <p className="text-zinc-400 text-sm leading-relaxed">
                  <T it={term.impact.it} en={term.impact.en} />
                </p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

    </div>
  );
}
