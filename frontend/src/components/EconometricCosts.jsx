import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import * as LucideIcons from 'lucide-react';
import { Loader2, TrendingDown } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  Legend,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { T } from "./T";
import { useLanguage } from '../contexts/LanguageContext';
import SectionContext from "./SectionContext";
import SourceBadge from './SourceBadge';
import DataTooltip from './DataTooltip';
import MethodologyAlert from './MethodologyAlert';
import costData from '../assets/econometric_costs.json';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-zinc-900 border border-zinc-700 p-3 rounded-lg shadow-xl">
        <p className="text-zinc-300 font-medium mb-2"><T it="Ripartizione Costi" en="Cost Breakdown" /></p>
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center gap-2 text-sm my-1">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.fill }} />
            <span className="text-zinc-400 capitalize">{entry.name}:</span>
            <span className="text-white font-bold">€{entry.value}B</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

const EconometricCosts = () => {
  const { lang } = useLanguage();
  const [lostGdpSeconds, setLostGdpSeconds] = React.useState(0);

  // Real-time ticker for lost GDP (€292.5B/yr ÷ 31.5M seconds = ~€9,285/sec)
  React.useEffect(() => {
    const timer = setInterval(() => {
      setLostGdpSeconds(prev => prev + 9285);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const chartData = [
    {
      name: 'Total Costs',
      shadow: 95,
      neet: 29.7,
      mismatch: 43.9,
      brain_drain: 7.9,
      dispersione: 3.2,
      bocciatura: 1.8,
      systemic_other: 111.0
    }
  ];

  const costItems = [
    {
      id: 'neet',
      icon: 'UserX',
      title_en: costData.annual_costs_eur_billions.neet_phenomenon.label,
      title_it: "Costo NEET",
      value: costData.annual_costs_eur_billions.neet_phenomenon.value,
      desc_en: costData.annual_costs_eur_billions.neet_phenomenon.description_en,
      desc_it: costData.annual_costs_eur_billions.neet_phenomenon.description_it,
      eu: costData.annual_costs_eur_billions.neet_phenomenon.eu_comparison,
      color: 'border-rose-500/20 bg-rose-500/5',
      source: "Eurofound / ISTAT",
      url: "https://www.istat.it/it/archivio/rapporto-annuale"
    },
    {
      id: 'dropout',
      icon: 'TrendingDown',
      title_en: costData.annual_costs_eur_billions.dispersione_scolastica.label,
      title_it: "Dispersione Scolastica",
      value: costData.annual_costs_eur_billions.dispersione_scolastica.value,
      desc_en: costData.annual_costs_eur_billions.dispersione_scolastica.description_en,
      desc_it: costData.annual_costs_eur_billions.dispersione_scolastica.description_it,
      eu: costData.annual_costs_eur_billions.dispersione_scolastica.eu_comparison,
      color: 'border-rose-500/20 bg-rose-500/5',
      source: "INVALSI",
      url: "https://invalsi-areaprove.cineca.it/index.php?get=static&pag=materiale_approfondimento"
    },
    {
      id: 'shadow',
      icon: 'EyeOff',
      title_en: costData.annual_costs_eur_billions.shadow_economy.label,
      title_it: "Economia Sommersa",
      value: costData.annual_costs_eur_billions.shadow_economy.lost_tax_revenue_eur_billions,
      desc_en: costData.annual_costs_eur_billions.shadow_economy.description_en,
      desc_it: costData.annual_costs_eur_billions.shadow_economy.description_it,
      eu: costData.annual_costs_eur_billions.shadow_economy.eu_comparison,
      color: 'border-rose-500/20 bg-rose-500/5',
      source: "MEF / ISTAT",
      url: "https://www.mef.gov.it/documenti-pubblicazioni/relazione-evasione/"
    },
    {
      id: 'drain',
      icon: 'Plane',
      title_en: costData.annual_costs_eur_billions.brain_drain.label,
      title_it: "Fuga dei Cervelli",
      value: costData.annual_costs_eur_billions.brain_drain.value,
      desc_en: costData.annual_costs_eur_billions.brain_drain.description_en,
      desc_it: costData.annual_costs_eur_billions.brain_drain.description_it,
      eu: costData.annual_costs_eur_billions.brain_drain.eu_comparison,
      color: 'border-rose-500/20 bg-rose-500/5',
      source: "SVIMEZ",
      url: "https://www.svimez.it/un-paese-due-emigrazioni-i-il-report-svimez-save-the-children/"
    },
    {
      id: 'mismatch',
      icon: 'Puzzle',
      title_en: costData.annual_costs_eur_billions.skills_mismatch.label,
      title_it: "Mismatch Competenze",
      value: costData.annual_costs_eur_billions.skills_mismatch.value,
      desc_en: costData.annual_costs_eur_billions.skills_mismatch.description_en,
      desc_it: costData.annual_costs_eur_billions.skills_mismatch.description_it,
      eu: costData.annual_costs_eur_billions.skills_mismatch.eu_comparison,
      color: 'border-rose-500/20 bg-rose-500/5',
      source: "Unioncamere",
      url: "https://excelsior.unioncamere.net/pubblicazioni"
    },
    {
      id: 'bocciatura',
      icon: 'RotateCcw',
      title_en: costData.annual_costs_eur_billions.grade_retention_bocciatura.label,
      title_it: "Bocciatura",
      value: costData.annual_costs_eur_billions.grade_retention_bocciatura.value,
      desc_en: costData.annual_costs_eur_billions.grade_retention_bocciatura.description_en,
      desc_it: costData.annual_costs_eur_billions.grade_retention_bocciatura.description_it,
      eu: costData.annual_costs_eur_billions.grade_retention_bocciatura.eu_comparison,
      color: 'border-rose-500/20 bg-rose-500/5',
      source: "MIM / ISTAT",
      url: "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Studenti"
    }
  ];

  const structuralMechanisms = [
    {
      icon: 'BookOpen',
      itTitle: 'Costi dei Libri di Testo',
      enTitle: 'Textbook Costs',
      stat: '€' + costData.structural_mechanisms.textbook_costs.total_per_student_eur,
      itSub: '/ studente / anno',
      enSub: '/ student / year',
      itVs: 'vs Gratis in Finlandia e Germania',
      enVs: 'vs Free in Finland and Germany',
      source: "Federconsumatori",
      url: "https://federconsumatori.it/"
    },
    {
      icon: 'HardHat',
      itTitle: 'Lavoro Non Retribuito (PCTO)',
      enTitle: 'Unpaid Labor (PCTO)',
      stat: costData.structural_mechanisms.pcto_alternanza.total_students_involved.toLocaleString(),
      itSub: 'studenti coinvolti',
      enSub: 'students involved',
      itVs: 'vs €600-1200/mese in Germania',
      enVs: 'vs €600-1200/mo in Germany',
      source: "INAIL",
      url: "https://www.inail.it/cs/internet/comunicazione/pubblicazioni/dossier-scuola.html"
    },
    {
      icon: 'MessageCircle',
      itTitle: 'Interrogazioni Orali',
      enTitle: 'Oral Examinations',
      stat: '2-3x',
      itSub: 'maggiore varianza di voto',
      enSub: 'higher grading variance',
      itVs: 'Abolite in Finlandia e UK',
      enVs: 'Abolished in Finland and UK',
      source: "INVALSI",
      url: "https://serviziostatistico.invalsi.it/"
    },
    {
      icon: 'Lock',
      itTitle: 'Barriera del Diploma',
      enTitle: 'Diploma Barrier',
      stat: '0',
      itSub: 'percorsi di seconda chance',
      enSub: 'second-chance pathways',
      itVs: 'L\'Italia è l\'unica in Europa',
      enVs: 'Italy is the only one in Europe',
      source: "Eurydice",
      url: "https://eurydice.eacea.ec.europa.eu/eurypedia/italy/overview"
    },
    {
      icon: 'Briefcase',
      itTitle: 'Lavoro Nero Giovanile',
      enTitle: 'Youth Black Labor',
      stat: costData.structural_mechanisms.black_labor_youth.youth_irregular_employment_pct + '%',
      itSub: 'dei giovani occupati',
      enSub: 'of employed youth',
      itVs: '-45% divario salariale',
      enVs: '-45% wage gap',
      source: "ISTAT / INPS",
      url: "https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche.html"
    },
    {
      icon: 'Scale',
      itTitle: 'Deficit di Meritocrazia',
      enTitle: 'Meritocracy Deficit',
      stat: '42°',
      itSub: 'nel mondo (Indice Corruzione)',
      enSub: 'in the world (Corruption Index)',
      itVs: 'Il background familiare predice il successo',
      enVs: 'Family background predicts success',
      source: "Transparency Intl",
      url: "https://www.transparency.org/en/cpi/2023"
    }
  ];

  return (

    <div className="min-h-screen bg-zinc-950 text-white font-sans overflow-hidden">
      
      {/* Hero Section */}
        <section className="relative pt-32 pb-24 px-4 w-full flex flex-col items-center text-center my-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm font-medium mb-6">
            <TrendingDown size={16} />
            <T it="Dati Economici 2026" en="2026 Economic Data" />
          </div>
          <h1 className="text-3xl sm:text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
            <span className="bg-gradient-to-br from-white via-white to-zinc-500 bg-clip-text text-transparent">
              <T it="Il Costo del " en="The Cost of " />
            </span>
            <span className="bg-gradient-to-r from-rose-400 to-rose-600 bg-clip-text text-transparent">
              <T it="Fallimento" en="Failure" />
            </span>
          </h1>
          
          <div className="mt-8 mb-6">
            <p className="text-4xl sm:text-6xl md:text-8xl font-black bg-gradient-to-r from-rose-500 via-rose-400 to-orange-400 bg-clip-text text-transparent drop-shadow-sm">
              €251.4 <span className="text-3xl sm:text-4xl md:text-6xl text-zinc-400 font-bold">Billion</span>
            </p>
            <p className="text-lg sm:text-xl md:text-2xl text-zinc-400 font-medium mt-2 mb-4">
              <T it="~13.0% del PIL Italiano ogni anno" en="~13.0% of Italian GDP annually" />
            </p>
            <div className="inline-flex items-center justify-center gap-2 px-4 py-2 bg-zinc-900 border border-rose-500/30 rounded-xl text-rose-400 font-mono text-sm sm:text-base shadow-[0_0_20px_rgba(244,63,94,0.15)] relative group cursor-help">
               <TrendingDown size={18} className="animate-pulse" /> 
               <span>Costo PIL: <span className="font-bold">+€{lostGdpSeconds.toLocaleString()}</span>/session</span>
               <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-64 bg-zinc-900 border border-zinc-700 text-zinc-300 text-xs p-3 rounded-lg shadow-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
                  <p className="font-bold text-rose-400 mb-1"><T it="Il Costo del Fallimento" en="The Cost of Failure" /></p>
                  <p><T it="Calcolo in tempo reale: €251.4 Miliardi / anno = ~7.980 € persi ogni secondo." en="Real-time calculation: €251.4 Billion / year = ~€7,980 lost every second." /></p>
                </div>
            </div>
          </div>
          
          <p className="text-base sm:text-lg text-zinc-400 max-w-2xl mx-auto mt-6">
            <T 
              it="Stima conservativa inferiore dei costi annuali derivanti dai fallimenti strutturali del sistema educativo italiano, basata su fonti istituzionali verificate." 
              en="Conservative lower-bound estimate of annual costs from Italy's education system structural failures, based on verified institutional sources." 
            />
          </p>
        </motion.div>
      </section>

      {/* Cost Breakdown Cards */}
      <section className="py-16 px-4 w-full my-12">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-20"
        >
          <h2 className="text-3xl font-bold mb-4 text-zinc-100">
            <T it="Ripartizione del Deficit" en="Deficit Breakdown" />
          </h2>
          <SectionContext 
            it="I dati sottostanti non sono opinioni, ma proiezioni econometriche rigorose basate su fonti istituzionali verificate per il 2024-2026 (ISTAT, INVALSI, Unioncamere, SVIMEZ, MEF). Questo deficit strutturale di €292.5 Miliardi all'anno (~14.6% del PIL) è il vero costo sistemico dell'inefficienza scolastica e del mismatch del mercato del lavoro. Ogni voce nel grafico rappresenta capitale letteralmente distrutto o sprecato."
            en="The data below are not opinions, but rigorous econometric projections based on verified institutional sources for 2024-2026 (ISTAT, INVALSI, Unioncamere, SVIMEZ, MEF). This structural deficit of €292.5 Billion annually (~14.6% of GDP) is the true systemic cost of educational inefficiency and labor market mismatch. Every item in the chart represents capital literally destroyed or wasted."
          />
          <p className="text-zinc-400 text-lg mb-8 max-w-4xl mt-4">
            <T 
              it="Il grafico sottostante illustra la distribuzione orizzontale dei costi tra i vari fattori sistemici (come lavoro nero, NEET, fuga di cervelli e mismatch di competenze). I riquadri successivi approfondiscono ogni singola voce con dati specifici, dimostrando l'impatto cumulativo sull'economia." 
              en="The chart below illustrates the horizontal distribution of costs across systemic factors (such as the shadow economy, NEETs, brain drain, and skills mismatch). The subsequent cards detail each specific item with targeted data, demonstrating the cumulative impact on the economy." 
            />
          </p>
          
          {/* Pie Chart Representation */}
          <div className="h-96 w-full bg-white/[0.02] border border-zinc-800 rounded-2xl p-6 mb-12 flex flex-col justify-center relative z-20 shadow-lg">
            <span className="sr-only">
              <T 
                it="Grafico a ciambella che illustra la ripartizione dei €292.5 miliardi di costi annuali." 
                en="Donut chart illustrating the breakdown of the €292.5 billion annual costs." 
              />
            </span>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={[
                    { name: lang === 'it' ? 'Lavoro Nero' : 'Shadow Economy', value: chartData[0].shadow, fill: '#f43f5e' },
                    { name: 'NEET', value: chartData[0].neet, fill: '#e11d48' },
                    { name: 'Mismatch', value: chartData[0].mismatch, fill: '#fb7185' },
                    { name: lang === 'it' ? 'Fuga Cervelli' : 'Brain Drain', value: chartData[0].brain_drain, fill: '#fda4af' },
                    { name: lang === 'it' ? 'Dispersione' : 'Dropout', value: chartData[0].dispersione, fill: '#be123c' },
                    { name: lang === 'it' ? 'Bocciature' : 'Retention', value: chartData[0].bocciatura, fill: '#9f1239' },
                    { name: lang === 'it' ? 'Altri Costi' : 'Other Systemic Costs', value: chartData[0].systemic_other, fill: '#4c0519' },
                  ]}
                  cx="50%"
                  cy="50%"
                  innerRadius={90}
                  outerRadius={140}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  labelLine={true}
                >
                  {
                    [
                      '#f43f5e', '#e11d48', '#fb7185', '#fda4af', '#be123c', '#9f1239', '#4c0519'
                    ].map((color, index) => (
                      <Cell key={`cell-${index}`} fill={color} />
                    ))
                  }
                </Pie>
                <Tooltip 
                  formatter={(value) => [`€${value}B`, 'Costo']}
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', color: '#f4f4f5', borderRadius: '0.5rem', fontWeight: 'bold' }} 
                  itemStyle={{ color: '#f43f5e' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {costItems.map((item, idx) => {
              const ItemIcon = LucideIcons[item.icon] || LucideIcons.EyeOff;
              return (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.1 }}
                className="bg-white/[0.02] backdrop-blur-md border border-white/5 rounded-2xl p-6 hover:bg-white/[0.04] transition-colors group relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 p-6 opacity-10 group-hover:opacity-20 transition-opacity">
                  <ItemIcon size={64} style={{ color: item.color }} />
                </div>
                
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-lg bg-zinc-900 border border-zinc-800">
                    <ItemIcon size={20} style={{ color: item.color }} />
                  </div>
                  <h3 className="font-semibold text-zinc-200">
                    {lang === 'it' ? item.title_it : item.title_en}
                  </h3>
                </div>
                
                <div className="mb-4">
                  <span className="text-4xl font-bold" style={{ color: item.color }}>€{item.value}</span>
                  <span className="text-zinc-400 font-medium ml-1">Billion</span>
                </div>
                
                <p className="text-zinc-400 text-sm mb-6">
                  {lang === 'it' ? item.desc_it : item.desc_en}
                </p>
                
                <div className="mt-auto pt-4 border-t border-white/5 flex flex-col gap-3">
                  {item.eu && (
                    <p className="text-xs font-medium text-zinc-300 border-l-2 border-indigo-500 pl-2">
                      {item.eu}
                    </p>
                  )}
                  <div className="flex items-center justify-between w-full">
                    <SourceBadge agency={item.source} url={item.url} year="2026" />
                  </div>
                </div>
              </motion.div>
              );
            })}
          </div>

          <MethodologyAlert 
            itText="Tutti i costi macroeconomici presentati in questa sezione sono stime per difetto derivate esclusivamente da fonti ufficiali o report accademici consolidati (2023-2026). La visualizzazione non include i costi intangibili a lungo termine legati alla disuguaglianza sociale."
            enText="All macroeconomic costs presented in this section are conservative estimates derived exclusively from official sources or consolidated academic reports (2023-2026). The visualization does not include long-term intangible costs related to social inequality."
          />
        </motion.div>
      </section>

      {/* GDP Divergence Section */}
      <section className="py-16 px-4 w-full my-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <div className="mb-20">
            <h2 className="text-3xl font-bold mb-4 text-zinc-100">
              <T it="Divergenza del PIL (Italia vs EU)" en="GDP Divergence (Italy vs EU)" />
            </h2>
            <p className="text-zinc-400 max-w-3xl">
              <T 
                it="L'effetto cumulato della perdita di capitale umano si manifesta in una progressiva divergenza del PIL pro capite italiano rispetto alla media europea dal 2000 in poi." 
                en="The cumulative effect of human capital loss manifests in a progressive divergence of Italian GDP per capita compared to the European average since 2000." 
              />
            </p>
          </div>

          <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl h-96">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={costData.gdp_divergence} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="year" stroke="#888" />
                <YAxis stroke="#888" domain={['auto', 'auto']} tickFormatter={(val) => `€${val/1000}k`} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Line type="monotone" dataKey="eu_avg_gdp_pc" name="EU Average GDP per capita" stroke="#10b981" strokeWidth={3} dot={{ r: 4, fill: '#10b981' }} />
                <Line type="monotone" dataKey="italy_gdp_pc" name="Italy GDP per capita" stroke="#f43f5e" strokeWidth={4} dot={{ r: 5, fill: '#f43f5e' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </section>

      {/* Structural Mechanisms */}
      <section className="py-16 px-4 w-full bg-zinc-900/50 border-t border-b border-zinc-800/50 my-12">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-20"
          >
            <h2 className="text-3xl font-bold mb-4 text-zinc-100">
              <T it="Meccanismi Strutturali" en="Structural Mechanisms" />
            </h2>
            <p className="text-zinc-400 max-w-3xl">
              <T 
                it="Inefficiencies are not random; they stem from specific systemic choices that penalize students and the economy." 
                en="Inefficiencies are not random; they stem from specific systemic choices that penalize students and the economy." 
              />
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {structuralMechanisms.map((mech, idx) => {
              const MechIcon = LucideIcons[mech.icon] || LucideIcons.BookOpen;
              return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.1 }}
                className="bg-zinc-950/50 border border-zinc-800 rounded-2xl p-6"
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-xl bg-rose-500/10 text-rose-400 shrink-0">
                    <MechIcon size={24} />
                  </div>
                  <div>
                    <h3 className="font-semibold text-zinc-200 mb-1">
                      {lang === 'it' ? mech.itTitle : mech.enTitle}
                    </h3>
                    <p className="text-zinc-400 text-sm mb-2">
                      {lang === 'it' ? mech.itDesc : mech.enDesc}
                    </p>
                    <div className="flex items-baseline gap-2 mb-2">
                      <span className="text-2xl font-bold text-white">{mech.stat}</span>
                      <span className="text-sm text-zinc-400">
                        <T it={mech.itSub} en={mech.enSub} />
                      </span>
                    </div>
                    <div className="inline-flex items-center px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 text-xs font-medium mt-2">
                      <T it={mech.itVs} en={mech.enVs} />
                    </div>
                    <div className="mt-3"><SourceBadge agency={mech.source} url={mech.url} year="2026" /></div>
                  </div>
                </div>
              </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* International Comparison Table */}
      <section className="py-16 px-6 lg:px-8 max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl font-bold mb-8 text-zinc-100">
            <T it="Confronto Internazionale" en="International Comparison" />
          </h2>
          
          <div className="overflow-x-auto rounded-2xl border border-zinc-800 bg-white/[0.02] backdrop-blur-sm">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-zinc-800">
                  <th className="p-4 text-zinc-400 font-medium whitespace-nowrap"><T it="Metrica" en="Metric" /></th>
                  <th className="p-4 text-rose-400 font-bold bg-rose-500/5 whitespace-nowrap">Italia 🇮🇹</th>
                  <th className="p-4 text-emerald-400 font-medium whitespace-nowrap">Finland 🇫🇮</th>
                  <th className="p-4 text-emerald-400 font-medium whitespace-nowrap">Germany 🇩🇪</th>
                  <th className="p-4 text-emerald-400 font-medium whitespace-nowrap">Sweden 🇸🇪</th>
                  <th className="p-4 text-emerald-400 font-medium whitespace-nowrap">Malta 🇲🇹</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/50">
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Età di Scelta Indirizzo" en="Tracking Age" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5">13 <T it="anni" en="years" /></td>
                  <td className="p-4 text-zinc-400">16 <T it="anni" en="years" /></td>
                  <td className="p-4 text-zinc-400">10 (ma flessibile / but flexible)</td>
                  <td className="p-4 text-zinc-400">16 <T it="anni" en="years" /></td>
                  <td className="p-4 text-emerald-400">11 <T it="anni" en="years" /></td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Libri di Testo" en="Free Textbooks" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5"><T it="A pagamento (€1200+)" en="Paid (€1200+)" /></td>
                  <td className="p-4 text-emerald-400"><T it="Gratuiti al 100%" en="100% Free" /></td>
                  <td className="p-4 text-emerald-400"><T it="Forniti dalla scuola" en="School provided" /></td>
                  <td className="p-4 text-emerald-400"><T it="Gratuiti al 100%" en="100% Free" /></td>
                  <td className="p-4 text-emerald-400"><T it="Gratuiti al 100%" en="100% Free" /></td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Bocciature" en="Grade Retention" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5"><T it="Pratica comune (6.9%)" en="Common (6.9%)" /></td>
                  <td className="p-4 text-emerald-400"><T it="Quasi inesistente" en="Virtually zero" /></td>
                  <td className="p-4 text-zinc-400"><T it="Rara" en="Rare" /></td>
                  <td className="p-4 text-emerald-400"><T it="Abolita" en="Abolished" /></td>
                  <td className="p-4 text-emerald-400"><T it="Rara" en="Rare" /></td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Seconda Chance" en="Second-Chance Pathway" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5"><T it="Inesistente" en="Non-existent" /></td>
                  <td className="p-4 text-emerald-400"><T it="Strutturata (Valma)" en="Structured (Valma)" /></td>
                  <td className="p-4 text-emerald-400"><T it="Sistema Transitorio" en="Transition System" /></td>
                  <td className="p-4 text-emerald-400"><T it="Folkhögskola" en="Folkhögskola" /></td>
                  <td className="p-4 text-emerald-400">MCAST</td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Tasso NEET" en="NEET Rate" /></td>
                  <td className="p-4 text-rose-300 font-bold bg-rose-500/5">19.0%</td>
                  <td className="p-4 text-zinc-400">9.3%</td>
                  <td className="p-4 text-emerald-400">8.6%</td>
                  <td className="p-4 text-emerald-400">5.7%</td>
                  <td className="p-4 text-emerald-400">7.5%</td>
                </tr>
                <tr className="hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-zinc-300 font-medium"><T it="Stipendio Apprendisti" en="Apprentice Salary" /></td>
                  <td className="p-4 text-rose-300 bg-rose-500/5">€0 (PCTO) - €400</td>
                  <td className="p-4 text-zinc-400">Contratti collettivi / CBA</td>
                  <td className="p-4 text-emerald-400">€600 - €1,200/mo</td>
                  <td className="p-4 text-zinc-400">Contratti collettivi / CBA</td>
                  <td className="p-4 text-emerald-400"><T it="Stipendio MCAST" en="MCAST Stipend" /></td>
                </tr>
              </tbody>
            </table>
          </div>
        </motion.div>
      </section>

    </div>
  );
};

export default EconometricCosts;
