import React from 'react';
import { useLanguage } from "../contexts/LanguageContext";
import { T } from "./T";
import SectionContext from "./SectionContext";
import DataTooltip from "./DataTooltip";
import SourceBadge from './SourceBadge';
import { motion } from 'framer-motion';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, PieChart, Pie, Cell } from 'recharts';
import { Globe, HardHat, Brain, Scale, TrendingDown, ShieldCheck, AlertTriangle, BookOpen, BookMarked, Euro } from 'lucide-react';
import data from '../assets/deep_dives_data.json';

const SectionHeader = ({ icon: Icon, titleIt, titleEn, descIt, descEn, agency = "ISTAT", topicKey, year = "2026", url }) => (
  <div className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-zinc-800/80 pb-4">
    <div>
      <div className="flex items-center gap-3 mb-2">
        <div className="p-3 bg-indigo-500/20 rounded-xl border border-indigo-500/30">
          <Icon className="text-indigo-400" size={28} />
        </div>
        <h2 className="text-3xl font-black text-white">
          <T it={titleIt} en={titleEn} />
        </h2>
      </div>
      <p className="text-zinc-400 max-w-2xl text-sm">
        <T it={descIt} en={descEn} />
      </p>
    </div>
    <div className="flex-shrink-0">
      <SourceBadge agency={agency} topicKey={topicKey} year={year} url={url} />
    </div>
  </div>
);

export default function SystemicDeepDives() {
  const { lang } = useLanguage();
  const isIt = lang === "it";
  return (
    <div className="min-h-screen pt-24 pb-12 px-6">
      <div className="max-w-6xl mx-auto space-y-24">
        
        {/* Header */}
        <SectionContext 
          domainIt="Meccaniche Strutturali" 
          domainEn="Structural Mechanics"
          titleIt="Deep Dive Sistemici" 
          titleEn="Systemic Deep Dives"
          thesisIt="Le inefficienze del sistema scolastico italiano non sono casuali, ma derivano da precise scelte di governance, meccanismi di valutazione soggettiva e distorsioni di mercato che penalizzano sistematicamente gli studenti."
          thesisEn="The inefficiencies of the Italian school system are not random, but stem from specific governance choices, subjective evaluation mechanisms, and market distortions that systematically penalize students."
          takeaways={[
            {it: "Il verticalismo burocratico blocca l'innovazione", en: "Bureaucratic verticalism blocks innovation"},
            {it: "Il mercato dei libri di testo è un oligopolio inelastico", en: "The textbook market is an inelastic oligopoly"},
            {it: "Le valutazioni soggettive generano dispersione", en: "Subjective evaluations drive dropout rates"}
          ]}
        />

        {/* Section 1: Malta vs Catania */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
          <SectionHeader 
            icon={Globe} 
            titleIt="Micro-Localizzazione: Catania vs Malta" 
            titleEn="Micro-Localization: Catania vs Malta"
            descIt="Malta rappresenta un'economia insulare vicina con una popolazione paragonabile a Catania (metropolitana). Confrontare questi due ecosistemi rivela il peso dei divari sistemici."
            descEn="Malta represents a nearby island economy with a population comparable to Catania (metro). Comparing these two ecosystems reveals the weight of systemic divides."
            agency="OECD"
            topicKey="malta"
            year="2026"
          />
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-zinc-900/80 backdrop-blur border border-rose-500/30 rounded-3xl p-8 relative overflow-hidden shadow-2xl">
              <div className="absolute top-0 right-0 w-32 h-32 bg-rose-500/10 rounded-full blur-3xl" />
              <h3 className="text-xl font-bold text-white mb-6 border-b border-zinc-800 pb-2">Catania (IT)</h3>
              <div className="space-y-6">
                <div>
                  <p className="text-xs text-zinc-400 font-bold uppercase tracking-wider mb-1"><T it="Popolazione" en="Population" /></p>
                  <p className="text-2xl font-black text-zinc-200">{data.malta_vs_catania.catania.population}</p>
                </div>
                <div>
                  <p className="text-xs text-zinc-400 font-bold uppercase tracking-wider mb-1"><T it="Tasso NEET" en="NEET Rate" /></p>
                  <div className="flex items-end gap-2">
                    <p className="text-4xl font-black text-rose-400">{data.malta_vs_catania.catania.neet_rate}%</p>
                    <TrendingDown className="text-rose-400 mb-2" />
                  </div>
                </div>
                <div>
                  <p className="text-xs text-zinc-400 font-bold uppercase tracking-wider mb-1"><T it="Spesa Educazione (% PIL)" en="Education Spend (% GDP)" /></p>
                  <p className="text-2xl font-black text-rose-400">{data.malta_vs_catania.catania.education_gdp_pct}%</p>
                </div>
                <div>
                  <p className="text-xs text-zinc-400 font-bold uppercase tracking-wider mb-1"><T it="Copertura TPL (Mobilità)" en="TPL Coverage (Mobility)" /></p>
                  <p className="text-2xl font-black text-rose-400">{data.malta_vs_catania.catania.transport_coverage}%</p>
                  <p className="text-xs text-rose-400/70 mt-1"><T it="Barriera geografica altissima per la scelta scolastica." en="Massive geographic barrier for school choice." /></p>
                </div>
              </div>
            </div>

            <div className="bg-zinc-900/80 backdrop-blur border border-emerald-500/30 rounded-3xl p-8 relative overflow-hidden shadow-2xl">
              <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl" />
              <h3 className="text-xl font-bold text-white mb-6 border-b border-zinc-800 pb-2">Malta (EU)</h3>
              <div className="space-y-6">
                <div>
                  <p className="text-xs text-zinc-400 font-bold uppercase tracking-wider mb-1"><T it="Popolazione" en="Population" /></p>
                  <p className="text-2xl font-black text-zinc-200">{data.malta_vs_catania.malta.population}</p>
                </div>
                <div>
                  <p className="text-xs text-zinc-400 font-bold uppercase tracking-wider mb-1"><T it="Tasso NEET" en="NEET Rate" /></p>
                  <div className="flex items-end gap-2">
                    <p className="text-4xl font-black text-emerald-400">{data.malta_vs_catania.malta.neet_rate}%</p>
                  </div>
                </div>
                <div>
                  <p className="text-xs text-zinc-400 font-bold uppercase tracking-wider mb-1"><T it="Spesa Educazione (% PIL)" en="Education Spend (% GDP)" /></p>
                  <p className="text-2xl font-black text-emerald-400">{data.malta_vs_catania.malta.education_gdp_pct}%</p>
                </div>
                <div>
                  <p className="text-xs text-zinc-400 font-bold uppercase tracking-wider mb-1"><T it="Copertura TPL (Mobilità)" en="TPL Coverage (Mobility)" /></p>
                  <p className="text-2xl font-black text-emerald-400">{data.malta_vs_catania.malta.transport_coverage}%</p>
                  <p className="text-xs text-emerald-400/70 mt-1"><T it="Mobilità garantita annulla l'attrito territoriale." en="Guaranteed mobility nullifies territorial friction." /></p>
                </div>
              </div>
            </div>
          </div>
        </motion.section>

        {/* Section 2: PCTO vs Dual System */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
          <SectionHeader 
            icon={HardHat} 
            titleIt="Formazione Scuola-Lavoro / FSL (ex PCTO)" 
            titleEn="School-Work Formation / FSL (ex PCTO)"
            descIt="Il lavoro gratuito sotto copertura formativa produce infortuni senza inserimento lavorativo."
            descEn="Unpaid labor under educational coverage produces injuries without job insertion."
            agency="INAIL"
            topicKey="pcto"
            year="2026"
          />
          <div className="bg-zinc-950 border border-zinc-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col md:flex-row">
            <div className="flex-1 p-8 border-b md:border-b-0 md:border-r border-zinc-800 relative bg-gradient-to-br from-rose-950/20 to-transparent">
              <div className="flex items-center gap-3 mb-6">
                <AlertTriangle className="text-rose-500" />
                <h3 className="text-2xl font-black text-white">FSL / ex PCTO (Italy)</h3>
              </div>
              <ul className="space-y-4">
                <li className="flex justify-between items-center border-b border-zinc-800/50 pb-2">
                  <span className="text-sm text-zinc-400"><T it="Compensazione Mensile" en="Monthly Compensation" /></span>
                  <span className="text-xl font-bold text-rose-400">€0</span>
                </li>
                <li className="flex justify-between items-center border-b border-zinc-800/50 pb-2">
                  <span className="text-sm text-zinc-400"><T it="Denunce Infortunio (INAIL)" en="Injury Reports (INAIL)" /></span>
                  <span className="text-xl font-bold text-rose-400">{data.pcto_vs_dual.italy_pcto.inail_injury_reports_annual}+</span>
                </li>
                <li className="flex justify-between items-center border-b border-zinc-800/50 pb-2">
                  <span className="text-sm text-zinc-400"><T it="Garanzia Inserimento Lavoro" en="Job Insertion Guarantee" /></span>
                  <span className="text-lg font-bold text-rose-400"><T it="Nessuna" en="None" /></span>
                </li>
              </ul>
            </div>
            
            <div className="flex-1 p-8 relative bg-gradient-to-br from-emerald-950/20 to-transparent">
              <div className="flex items-center gap-3 mb-6">
                <ShieldCheck className="text-emerald-500" />
                <h3 className="text-2xl font-black text-white">Dual System (Germany)</h3>
              </div>
              <ul className="space-y-4">
                <li className="flex justify-between items-center border-b border-zinc-800/50 pb-2">
                  <span className="text-sm text-zinc-400"><T it="Compensazione Mensile" en="Monthly Compensation" /></span>
                  <span className="text-xl font-bold text-emerald-400">€{data.pcto_vs_dual.germany_dual.compensation_eur_month}</span>
                </li>
                <li className="flex justify-between items-center border-b border-zinc-800/50 pb-2">
                  <span className="text-sm text-zinc-400"><T it="Denunce Infortunio" en="Injury Reports" /></span>
                  <span className="text-sm font-bold text-emerald-400 text-right max-w-[120px]"><T it="Regolamentato (Diritto Lavoro)" en="Regulated (Labor Law)" /></span>
                </li>
                <li className="flex justify-between items-center border-b border-zinc-800/50 pb-2">
                  <span className="text-sm text-zinc-400"><T it="Garanzia Inserimento Lavoro" en="Job Insertion Guarantee" /></span>
                  <span className="text-lg font-bold text-emerald-400">Sì / Yes</span>
                </li>
              </ul>
            </div>
          </div>
        </motion.section>

        {/* Section 3: Subjective Evaluation */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
          <SectionHeader 
            icon={Brain} 
            titleIt="La Distorsione dell'Interrogazione Orale" 
            titleEn="The Oral Exam Distortion"
            descIt="L'Italia è l'unico grande paese UE a mantenere l'interrogazione orale ad alto valore come metodo primario di valutazione continua."
            descEn="Italy is the only major EU country to maintain high-stakes oral exams as the primary continuous assessment method."
            agency="Eurydice"
            topicKey="orals"
            year="2026"
          />
          <div className="bg-zinc-900/50 p-6 rounded-3xl border border-zinc-800 h-64 sm:h-96">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.subjective_evaluation} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="type" stroke="#71717a" tick={{fill: '#a1a1aa', fontSize: 12}} />
                <YAxis stroke="#71717a" tick={{fill: '#a1a1aa', fontSize: 12}} />
                <Tooltip 
                  contentStyle={{backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px'}} 
                  itemStyle={{ color: '#ffffff' }}
                  labelStyle={{ color: '#ffffff' }}
                />
                <Legend />
                <Bar dataKey="grading_variance" name="Varianza Voto (Soggettività)" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                <Bar dataKey="psychological_distress_index" name="Indice Distress Psicologico" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.section>

        {/* Section 4: Governance */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
          <SectionHeader 
            icon={Scale} 
            titleIt="Deficit di Governance e Meritocrazia" 
            titleEn="Governance & Meritocracy Deficit"
            descIt="Indici comparativi di governance istituzionale."
            descEn="Comparative institutional governance indicators."
            agency="World Bank"
            topicKey="governance"
            year="2026"
          />
          <div className="bg-zinc-950 p-4 md:p-8 rounded-3xl border border-zinc-800 flex justify-center items-center h-[300px] sm:h-[500px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data.governance_wgi}>
                <PolarGrid stroke="#27272a" />
                <PolarAngleAxis dataKey="country" tick={{fill: '#e4e4e7', fontSize: 14, fontWeight: 'bold'}} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar name="Accountability" dataKey="accountability" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.4} />
                <Radar name="Rule of Law" dataKey="rule_of_law" stroke="#10b981" fill="#10b981" fillOpacity={0.4} />
                <Radar name="Horizontalism" dataKey="horizontalism" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.4} />
                <Tooltip 
                  contentStyle={{backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px'}} 
                  itemStyle={{ color: '#ffffff' }}
                  labelStyle={{ color: '#ffffff' }}
                />
                <Legend wrapperStyle={{paddingTop: '20px'}} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </motion.section>
        {/* Section 5: Textbook Economics */}
        <motion.section initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
          <SectionHeader 
            icon={BookOpen} 
            titleIt="Economia dei Libri di Testo (Caro Scuola)" 
            titleEn="Textbook Economics (Expensive Schooling)"
            descIt="Un mercato di €800M l'anno dominato da un oligopolio. L'asimmetria di scelta (i docenti scelgono, le famiglie pagano) e il meccanismo delle 'nuove edizioni' bloccano la concorrenza e uccidono il mercato dell'usato."
            descEn="An €800M/year market dominated by an oligopoly. The asymmetry of choice (teachers choose, families pay) and the 'new editions' loop block competition and kill the used books market."
            agency="AGCM & AIE"
            topicKey="textbooks"
            year="2026"
          />
          <div className="grid md:grid-cols-2 gap-8">
            {/* Pie Chart of Oligopoly */}
            <div className="bg-zinc-900/50 p-6 rounded-3xl border border-zinc-800 flex flex-col h-[400px]">
              <h3 className="text-xl font-bold text-white mb-2"><T it="Oligopolio Editoriale" en="Publisher Oligopoly" /></h3>
              <p className="text-sm text-zinc-400 mb-4"><T it="Quote di mercato (Il top 4 controlla ~80%)" en="Market shares (Top 4 control ~80%)" /></p>
              <div className="flex-1 w-full h-full min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={data.textbook_oligopoly}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="share"
                    >
                      {data.textbook_oligopoly && data.textbook_oligopoly.map((entry, index) => {
                        const colors = ['#f43f5e', '#8b5cf6', '#10b981', '#f59e0b', '#06b6d4'];
                        return <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />;
                      })}
                    </Pie>
                    <Tooltip 
                      contentStyle={{backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px'}}
                      itemStyle={{ color: '#ffffff' }}
                      labelStyle={{ color: '#ffffff' }}
                      formatter={(value) => `${value}%`}
                    />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Asymmetry of choice and New Editions Loop */}
            <div className="flex flex-col gap-6">
              <div className="bg-gradient-to-br from-rose-900/30 to-zinc-900/50 p-6 rounded-3xl border border-rose-500/20 flex-1 flex items-start gap-4">
                <div className="p-3 bg-rose-500/20 rounded-xl shrink-0"><BookMarked className="text-rose-400" /></div>
                <div>
                  <h4 className="text-lg font-bold text-white mb-2">
                    <DataTooltip 
                      titleIt="Asimmetria Informativa e di Scelta" 
                      titleEn="Asymmetry of Choice and Information" 
                      descIt="In economia, è un fallimento del mercato. Chi sceglie il prodotto (il docente) non ne sopporta il costo, mentre chi paga (la famiglia) non ha potere decisionale. Questo annulla l'elasticità della domanda al prezzo." 
                      descEn="In economics, this is a market failure. The decision maker (teacher) bears no cost, while the payer (family) has no decision power. This nullifies price elasticity of demand." 
                      source="AGCM (Autorità Garante della Concorrenza)"
                    >
                      <T it="Asimmetria di Scelta" en="Asymmetry of Choice" />
                    </DataTooltip>
                  </h4>
                  <p className="text-sm text-zinc-300 leading-relaxed">
                    <T 
                      it="I docenti adottano i testi, ma le famiglie li pagano. Questa anomalia (rilevata dall'Antitrust AGCM) impedisce la competizione sui prezzi, permettendo rincari costanti (+13% in un decennio)." 
                      en="Teachers adopt textbooks, but families pay for them. This anomaly (noted by Antitrust AGCM) prevents price competition, allowing constant markups (+13% in a decade)." 
                    />
                  </p>
                </div>
              </div>

              <div className="bg-gradient-to-br from-indigo-900/30 to-zinc-900/50 p-6 rounded-3xl border border-indigo-500/20 flex-1 flex items-start gap-4">
                <div className="p-3 bg-indigo-500/20 rounded-xl shrink-0"><Euro className="text-indigo-400" /></div>
                <div>
                  <h4 className="text-lg font-bold text-white mb-2"><T it="Il Trucco delle 'Nuove Edizioni'" en="The 'New Editions' Loophole" /></h4>
                  <p className="text-sm text-zinc-300 leading-relaxed mb-3">
                    <T 
                      it="Il 35-40% dei testi per il 1° anno subisce minime 'nuove edizioni' superficiali (impaginazione, capitoli spostati)." 
                      en="35-40% of first-year textbooks get minor superficial 'new editions' (layout, reshuffled chapters)." 
                    />
                  </p>
                  <div className="inline-block bg-indigo-500/20 px-3 py-1 rounded-full border border-indigo-500/30">
                    <span className="text-indigo-300 text-xs font-semibold">
                      <T it="Uccide il mercato dell'usato (danno da €150M)" en="Kills the used book market (€150M damage)" />
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.section>

      </div>
    </div>
  );
}
