import React, { useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  ScatterChart, Scatter, Cell, LineChart, Line, ComposedChart, AreaChart, Area, PieChart, Pie
} from 'recharts';
import metricsData from '../assets/dashboard_metrics.json';
import macroData from '../assets/macro_metrics.json';
import eurydiceData from '../assets/master_eurydice_comparison.json';
import { Database, Activity, Globe, TrendingDown } from 'lucide-react';
import { T } from '../components/T';
import { Link } from 'react-router-dom';

export default function Home() {
  const [activeTab, setActiveTab] = useState('structural');

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

  return (
    <div className="max-w-7xl mx-auto px-4 py-12 space-y-12">
      
      {/* Header */}
      <div className="text-center space-y-4 mb-8">
        <div className="inline-flex items-center justify-center p-4 bg-indigo-500/10 rounded-full mb-4">
          <Database size={32} className="text-indigo-400" />
        </div>
        <h1 className="text-4xl md:text-5xl font-black text-white">
          <T it="Osservatorio Dati Universale" en="Universal Data Observatory" />
        </h1>
        <p className="text-zinc-400 text-lg max-w-2xl mx-auto">
          <T 
            it="Visualizzazione interattiva neutrale di 681 dataset istituzionali (MIM, ISTAT, Eurostat, OCSE)." 
            en="Neutral interactive visualization of 681 institutional datasets (MIM, ISTAT, Eurostat, OECD)." 
          />
        </p>
        <div className="pt-4">
          <Link to="/catalog" className="text-indigo-400 hover:text-indigo-300 underline font-medium">
            <T it="Accedi all'archivio dati grezzi →" en="Access raw data archive →" />
          </Link>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap justify-center gap-4 border-b border-zinc-800 pb-4">
        <button 
          onClick={() => setActiveTab('structural')}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all ${activeTab === 'structural' ? 'bg-indigo-600 text-white shadow-[0_0_20px_rgba(79,70,229,0.3)]' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'}`}
        >
          <Activity size={18} />
          <T it="Struttura O.E.D." en="O.E.D. Structure" />
        </button>
        <button 
          onClick={() => setActiveTab('international')}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all ${activeTab === 'international' ? 'bg-indigo-600 text-white shadow-[0_0_20px_rgba(79,70,229,0.3)]' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'}`}
        >
          <Globe size={18} />
          <T it="Benchmark Internazionale" en="International Benchmark" />
        </button>
        <button 
          onClick={() => setActiveTab('macro')}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all ${activeTab === 'macro' ? 'bg-indigo-600 text-white shadow-[0_0_20px_rgba(79,70,229,0.3)]' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'}`}
        >
          <TrendingDown size={18} />
          <T it="Macro-Economia" en="Macro-Economics" />
        </button>
      </div>

      {/* TAB 1: STRUCTURAL */}
      {activeTab === 'structural' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
            <h2 className="text-xl font-bold text-white mb-6">
              <T it="Reddito Familiare Medio per Indirizzo (Origine)" en="Average Family Income by Track (Origin)" />
            </h2>
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
            <h2 className="text-xl font-bold text-white mb-6">
              <T it="Esiti Occupazionali e Accademici (Destinazione)" en="Occupational and Academic Outcomes (Destination)" />
            </h2>
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
            <h2 className="text-xl font-bold text-white mb-6">
              <T it="Allocazione Risorse Strutturali (Educazione)" en="Structural Resource Allocation (Education)" />
            </h2>
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
            <h2 className="text-xl font-bold text-white mb-6">
              <T it="Punteggi INVALSI Matematica per Area e Indirizzo" en="INVALSI Math Scores by Macro-Area and Track" />
            </h2>
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
      )}

      {/* TAB 2: INTERNATIONAL */}
      {activeTab === 'international' && (
        <div className="grid grid-cols-1 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl w-full">
            <h2 className="text-xl font-bold text-white mb-6">
              <T it="Eurydice: Età di Smistamento vs Tasso NEET" en="Eurydice: Tracking Age vs NEET Rate" />
            </h2>
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
      )}

      {/* TAB 3: MACRO-ECONOMICS */}
      {activeTab === 'macro' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
          
          {/* Demographic Collapse */}
          <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl lg:col-span-2">
            <h2 className="text-xl font-bold text-white mb-6">
              <T it="Collasso Demografico e Chiusura Scuole" en="Demographic Collapse and School Closures" />
            </h2>
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

          {/* PNRR Spending */}
          <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
            <h2 className="text-xl font-bold text-white mb-6">
              <T it="Distribuzione Spesa PNRR Istruzione" en="PNRR Education Spending Distribution" />
            </h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pnrr_spending} dataKey="allocation_pct" nameKey="category" cx="50%" cy="50%" outerRadius={100} label={(entry) => `${entry.allocation_pct}%`}>
                    {pnrr_spending.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <RechartsTooltip content={<CustomTooltip />} />
                  <Legend layout="horizontal" verticalAlign="bottom" align="center" />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Pension Gap */}
          <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
            <h2 className="text-xl font-bold text-white mb-6">
              <T it="Divario Pensionistico Proiettato" en="Projected Pension Gap" />
            </h2>
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
      )}

    </div>
  );
}
