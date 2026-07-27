import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  ScatterChart, Scatter, Cell, LineChart, Line, ComposedChart, AreaChart, Area, PieChart, Pie
} from 'recharts';
import { motion } from 'framer-motion';
import metricsData from '../assets/dashboard_metrics.json';
import macroData from '../assets/macro_metrics.json';
import eurydiceData from '../assets/master_eurydice_comparison.json';
import { Database, MousePointerClick } from 'lucide-react';
import { T } from '../components/T';
import { Link } from 'react-router-dom';
import OEDSimulator from '../components/OEDSimulator';

export default function Home() {
  const { tracking_outcomes, invalsi_performance } = metricsData;
  const { demographic_collapse, pnrr_spending, pension_gap } = macroData;
  const COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#f43f5e'];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-zinc-900 border border-zinc-700 p-4 rounded-lg shadow-xl">
          <p className="font-bold text-white mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color || entry.fill }} className="text-sm font-medium">
              {entry.name}: {entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const FadeInSection = ({ children, delay = 0 }) => (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6, delay }}
      className="w-full"
    >
      {children}
    </motion.div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 py-12 space-y-32">
      
      {/* 1. Header & Hero */}
      <div className="text-center space-y-6 pt-12 pb-24 border-b border-zinc-800">
        <div className="inline-flex items-center justify-center p-4 bg-indigo-500/10 rounded-full mb-4">
          <Database size={32} className="text-indigo-400" />
        </div>
        <h1 className="text-5xl md:text-7xl font-black text-white tracking-tight">
          <T it="Osservatorio Dati Universale" en="Universal Data Observatory" />
        </h1>
        <p className="text-zinc-400 text-xl md:text-2xl max-w-3xl mx-auto font-light leading-relaxed">
          <T 
            it="Esplorazione interattiva e neutrale delle metriche strutturali del sistema educativo italiano, basata su 681 dataset istituzionali verificati." 
            en="Interactive and neutral exploration of structural metrics within the Italian educational system, based on 681 verified institutional datasets." 
          />
        </p>
        <div className="pt-8 animate-bounce text-zinc-500 flex flex-col items-center">
          <MousePointerClick size={24} className="mb-2" />
          <span className="text-sm uppercase tracking-widest"><T it="Scorri per esplorare" en="Scroll to explore" /></span>
        </div>
      </div>

      {/* 2. The OED Simulator */}
      <FadeInSection>
        <div className="space-y-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-white mb-4">
              <T it="Simulatore O.E.D. (Origine, Educazione, Destinazione)" en="O.E.D. Simulator (Origin, Education, Destination)" />
            </h2>
            <p className="text-zinc-400 text-lg">
              <T 
                it="Simulatore probabilistico basato sui dati ISTAT e AlmaDiploma per calcolare l'impatto dell'estrazione sociale sulle probabilità di successo accademico." 
                en="Probabilistic simulator based on ISTAT and AlmaDiploma data to calculate the impact of social origin on academic success probabilities." 
              />
            </p>
          </div>
          <OEDSimulator />
        </div>
      </FadeInSection>

      {/* 3. Structural Outcomes */}
      <FadeInSection>
        <div className="space-y-12">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">
              <T it="Metriche Strutturali del Sistema Tripartito" en="Structural Metrics of the Tripartite System" />
            </h2>
            <p className="text-zinc-400 text-lg">
              <T 
                it="Dati aggregati su risorse, background socio-economico ed esiti per i tre principali indirizzi scolastici italiani." 
                en="Aggregated data on resources, socio-economic background, and outcomes across the three main Italian school tracks." 
              />
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
              <h3 className="text-xl font-bold text-white mb-6">
                <T it="Reddito Familiare Medio per Indirizzo (Origine)" en="Average Family Income by Track (Origin)" />
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={tracking_outcomes} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                    <XAxis dataKey="track" stroke="#888" tick={{fill: '#888'}} />
                    <YAxis stroke="#888" tickFormatter={(val) => `€${val/1000}k`} />
                    <RechartsTooltip content={<CustomTooltip />} />
                    <Bar dataKey="avg_income_origin" name="Avg Income (€)" fill="#4f46e5" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
              <h3 className="text-xl font-bold text-white mb-6">
                <T it="Esiti Occupazionali e Accademici (Destinazione)" en="Occupational and Academic Outcomes (Destination)" />
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={tracking_outcomes} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                    <XAxis dataKey="track" stroke="#888" />
                    <YAxis stroke="#888" tickFormatter={(val) => `${val}%`} />
                    <RechartsTooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Bar dataKey="university_access_pct" name="University Access (%)" fill="#10b981" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="neet_rate_pct" name="NEET Rate (%)" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
              <h3 className="text-xl font-bold text-white mb-6">
                <T it="Allocazione Risorse Strutturali (Educazione)" en="Structural Resource Allocation (Education)" />
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={tracking_outcomes} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                    <XAxis dataKey="track" stroke="#888" />
                    <YAxis stroke="#888" tickFormatter={(val) => `${val}%`} />
                    <RechartsTooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Bar dataKey="teacher_precarity_pct" name="Teacher Precarity (%)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="building_safety_issues_pct" name="Building Safety Issues (%)" fill="#6366f1" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
              <h3 className="text-xl font-bold text-white mb-6">
                <T it="Punteggi INVALSI Matematica per Area e Indirizzo" en="INVALSI Math Scores by Macro-Area and Track" />
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={invalsi_performance} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                    <XAxis dataKey="region_macro" stroke="#888" />
                    <YAxis stroke="#888" domain={[130, 250]} />
                    <RechartsTooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Line type="monotone" dataKey="liceo_math_score" name="Liceo" stroke="#4f46e5" strokeWidth={3} dot={{ r: 6 }} />
                    <Line type="monotone" dataKey="tecnico_math_score" name="Tecnico" stroke="#10b981" strokeWidth={3} dot={{ r: 6 }} />
                    <Line type="monotone" dataKey="professionale_math_score" name="Professionale" stroke="#f43f5e" strokeWidth={3} dot={{ r: 6 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      </FadeInSection>

      {/* 4. International Benchmark */}
      <FadeInSection>
        <div className="space-y-8">
          <div className="text-center max-w-3xl mx-auto mb-8">
            <h2 className="text-3xl font-bold text-white mb-4">
              <T it="Benchmark Internazionale (Eurydice)" en="International Benchmark (Eurydice)" />
            </h2>
            <p className="text-zinc-400 text-lg">
              <T 
                it="Comparazione europea sull'età di tracking (smistamento) e il relativo impatto sui tassi di dispersione (NEET)." 
                en="European comparison of tracking age and its associated impact on dropout rates (NEET)." 
              />
            </p>
          </div>
          <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl w-full">
            <div className="h-[500px]">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={eurydiceData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="Country" stroke="#888" />
                  <YAxis yAxisId="left" stroke="#888" label={{ value: 'Tracking Age', angle: -90, position: 'insideLeft', fill: '#888' }} />
                  <YAxis yAxisId="right" orientation="right" stroke="#f43f5e" label={{ value: 'NEET Rate (%)', angle: 90, position: 'insideRight', fill: '#f43f5e' }} />
                  <RechartsTooltip content={<CustomTooltip />} />
                  <Legend wrapperStyle={{ paddingTop: '20px' }} />
                  <Bar yAxisId="left" dataKey="TrackingAge" name="Tracking Age (Years)" fill="#4f46e5" radius={[4, 4, 0, 0]} />
                  <Line yAxisId="right" type="monotone" dataKey="NEETRate_15_29" name="NEET Rate (%)" stroke="#f43f5e" strokeWidth={4} dot={{ r: 6 }} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </FadeInSection>

      {/* 5. Macro-Economics */}
      <FadeInSection>
        <div className="space-y-12 pb-24 border-b border-zinc-800">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">
              <T it="Macro-Economia e Demografia" en="Macro-Economics and Demographics" />
            </h2>
            <p className="text-zinc-400 text-lg">
              <T 
                it="Contesto macro-strutturale: crollo demografico, distribuzione dei fondi PNRR e divari pensionistici." 
                en="Macro-structural context: demographic collapse, PNRR fund distribution, and pension gaps." 
              />
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl lg:col-span-2">
              <h3 className="text-xl font-bold text-white mb-6">
                <T it="Collasso Demografico e Chiusura Scuole" en="Demographic Collapse and School Closures" />
              </h3>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={demographic_collapse} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="year" stroke="#888" />
                    <YAxis yAxisId="left" stroke="#888" label={{ value: 'Births (Thousands)', angle: -90, position: 'insideLeft', fill: '#888' }} />
                    <YAxis yAxisId="right" orientation="right" stroke="#f43f5e" label={{ value: 'School Closures', angle: 90, position: 'insideRight', fill: '#f43f5e' }} />
                    <RechartsTooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Area yAxisId="left" type="monotone" dataKey="births_thousands" name="Births (k)" stroke="#10b981" fill="#10b981" fillOpacity={0.2} />
                    <Area yAxisId="right" type="monotone" dataKey="school_closures" name="Cumulative Closures" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.2} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
              <h3 className="text-xl font-bold text-white mb-6">
                <T it="Distribuzione Spesa PNRR Istruzione" en="PNRR Education Spending Distribution" />
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={pnrr_spending} dataKey="allocation_pct" nameKey="category" cx="50%" cy="50%" outerRadius={100} label={(entry) => `${entry.allocation_pct}%`}>
                      {pnrr_spending.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <RechartsTooltip content={<CustomTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
              <h3 className="text-xl font-bold text-white mb-6">
                <T it="Divario Pensionistico Proiettato" en="Projected Pension Gap" />
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={pension_gap} margin={{ top: 20, right: 30, left: 20, bottom: 5 }} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                    <XAxis type="number" stroke="#888" tickFormatter={(val) => `€${val}`} />
                    <YAxis type="category" dataKey="track" stroke="#888" width={120} />
                    <RechartsTooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Bar dataKey="expected_pension_eur" name="Expected Monthly Pension (€)" fill="#4f46e5" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      </FadeInSection>

      {/* 6. Footer / CTA to Catalog */}
      <FadeInSection>
        <div className="text-center space-y-6 pb-24">
          <Database size={48} className="mx-auto text-indigo-500 mb-6 opacity-50" />
          <h2 className="text-4xl font-bold text-white">
            <T it="I Dati Sono Pubblici" en="The Data is Public" />
          </h2>
          <p className="text-zinc-400 text-xl max-w-2xl mx-auto">
            <T 
              it="Tutti i 681 dataset, i metadati e i notebook Jupyter utilizzati per generare queste metriche sono disponibili in open-source." 
              en="All 681 datasets, metadata, and Jupyter notebooks used to generate these metrics are available open-source." 
            />
          </p>
          <div className="pt-8">
            <Link 
              to="/catalog" 
              className="inline-block bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-4 px-8 rounded-xl transition-all shadow-lg shadow-indigo-500/20"
            >
              <T it="Accedi al Catalogo Completo (56 MB)" en="Access Full Data Catalog (56 MB)" />
            </Link>
          </div>
        </div>
      </FadeInSection>

    </div>
  );
}
