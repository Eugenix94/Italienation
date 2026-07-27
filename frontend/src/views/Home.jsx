import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  ScatterChart, Scatter, ZAxis, Cell, LineChart, Line
} from 'recharts';
import metricsData from '../assets/dashboard_metrics.json';
import { Database } from 'lucide-react';
import { T } from '../components/T';
import { Link } from 'react-router-dom';

export default function Home() {
  const { tracking_outcomes, international_comparison, invalsi_performance } = metricsData;

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-zinc-900 border border-zinc-700 p-4 rounded-lg shadow-xl">
          <p className="font-bold text-white mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12 space-y-16">
      
      <div className="text-center space-y-4 mb-16">
        <div className="inline-flex items-center justify-center p-4 bg-indigo-500/10 rounded-full mb-4">
          <Database size={32} className="text-indigo-400" />
        </div>
        <h1 className="text-4xl md:text-5xl font-black text-white">
          <T it="Esploratore Dati OED" en="OED Data Explorer" />
        </h1>
        <p className="text-zinc-400 text-lg max-w-2xl mx-auto">
          <T 
            it="Visualizzazione interattiva delle metriche strutturali del sistema educativo italiano, basata su 681 dataset ufficiali." 
            en="Interactive visualization of structural metrics within the Italian educational system, based on 681 official datasets." 
          />
        </p>
        <div className="pt-4">
          <Link to="/catalog" className="text-indigo-400 hover:text-indigo-300 underline font-medium">
            <T it="Sfoglia i 681 dataset grezzi →" en="Browse the 681 raw datasets →" />
          </Link>
        </div>
      </div>

      {/* Origin & Destination (Income & Outcomes) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Chart 1: Income by Track */}
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

        {/* Chart 2: NEET & Uni by Track */}
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

      </div>

      {/* Education Pipeline (Resources) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* Chart 3: Resource Allocation */}
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

        {/* Chart 4: Territorial Divide INVALSI */}
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

      {/* International Comparison Scatter */}
      <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
        <h2 className="text-xl font-bold text-white mb-6">
          <T it="Confronto Internazionale: Età di Smistamento vs Segregazione" en="International Comparison: Tracking Age vs Social Segregation" />
        </h2>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis type="number" dataKey="tracking_age" name="Tracking Age" stroke="#888" domain={[9, 19]} label={{ value: 'Tracking Age (Years)', position: 'insideBottom', offset: -10, fill: '#888' }} />
              <YAxis type="number" dataKey="social_segregation_index" name="Social Segregation Index" stroke="#888" domain={[0, 10]} label={{ value: 'Segregation Index (0-10)', angle: -90, position: 'insideLeft', fill: '#888' }} />
              <RechartsTooltip cursor={{strokeDasharray: '3 3'}} content={<CustomTooltip />} />
              <Scatter name="Countries" data={international_comparison} fill="#8884d8">
                {international_comparison.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.country === 'Italy' ? '#f43f5e' : '#4f46e5'} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}
