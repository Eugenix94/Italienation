import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { T } from './T';
import SourceBadge from './SourceBadge';
import { tracking_outcomes, invalsi_performance } from '../assets/dashboard_metrics.json';

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

export default function StructuralOutcomes() {
  return (
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
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Reddito Familiare Medio per Indirizzo (Origine)" en="Average Family Income by Track (Origin)" />
            </h3>
            <SourceBadge agency="MUR / ISTAT" year="2023" />
          </div>
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
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Esiti Occupazionali e Accademici (Destinazione)" en="Occupational and Academic Outcomes (Destination)" />
            </h3>
            <SourceBadge agency="AlmaDiploma / MUR" year="2023" />
          </div>
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
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Allocazione Risorse Strutturali (Educazione)" en="Structural Resource Allocation (Education)" />
            </h3>
            <SourceBadge agency="MIUR" year="2023" />
          </div>
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
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Punteggi INVALSI Matematica per Area e Indirizzo" en="INVALSI Math Scores by Macro-Area and Track" />
            </h3>
            <SourceBadge agency="INVALSI" year="2023" />
          </div>
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
  );
}
