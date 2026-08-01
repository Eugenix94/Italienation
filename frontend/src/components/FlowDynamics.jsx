import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, ComposedChart, Line, AreaChart, Area } from 'recharts';
import { T } from './T';
import { bocciature_by_escs, university_dropouts_by_macroarea, job_market_mismatch, neet_demographics } from '../assets/dashboard_metrics.json';

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

export default function FlowDynamics() {
  return (
    <div className="space-y-12 pb-24 border-b border-zinc-800">
      <div className="text-center max-w-3xl mx-auto mb-12">
        <h2 className="text-3xl font-bold text-white mb-4">
          <T it="Dinamiche di Flusso: Dall'Abbandono al Lavoro" en="Flow Dynamics: From Dropout to the Labor Market" />
        </h2>
        <p className="text-zinc-400 text-lg">
          <T 
            it="L'impatto del background familiare sulle bocciature, i tassi di rinuncia universitaria e il paradosso del disallineamento lavorativo (skills mismatch)." 
            en="The impact of family background on grade retention, university dropout rates, and the paradox of labor market skills mismatch." 
          />
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* ESCS Composition & Retention by Track */}
        <div className="bg-white/[0.02] border border-white/5 p-4 sm:p-6 rounded-2xl lg:col-span-2">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-6">
            <h3 className="text-lg sm:text-xl font-bold text-white">
              <T it="Composizione Socioeconomica e Bocciature per Indirizzo" en="Socioeconomic Composition & Retention by Track" />
            </h3>
          </div>
          <p className="text-xs text-zinc-500 mb-4">
            <T 
              it="I Licei concentrano il 65% di studenti con alto ESCS. I Professionali ne hanno solo il 18% ma registrano tassi di bocciatura 3× più alti."
              en="Licei concentrate 65% of high-ESCS students. Professionali have only 18% but register retention rates 3× higher."
            />
          </p>
          <div className="h-[350px] sm:h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={bocciature_by_escs} margin={{ top: 20, right: 10, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="track" stroke="#888" tick={{ fontSize: 11 }} />
                <YAxis stroke="#888" tickFormatter={(val) => `${val}%`} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px', fontSize: '11px' }} />
                <Bar dataKey="high_escs_share_pct" name="% High ESCS Students" fill="#818cf8" radius={[4, 4, 0, 0]} />
                <Bar dataKey="retention_low_escs_pct" name="Retention Rate (Low ESCS)" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                <Bar dataKey="retention_high_escs_pct" name="Retention Rate (High ESCS)" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* University Dropouts */}
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
          <h3 className="text-xl font-bold text-white mb-6">
            <T it="Fallimento della Transizione Terziaria (1° Anno)" en="Tertiary Transition Failure (1st Year)" />
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={university_dropouts_by_macroarea} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="macroarea" stroke="#888" />
                <YAxis stroke="#888" tickFormatter={(val) => `${val}%`} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Bar dataKey="inactive_0cfu_pct" name="Studenti Fantasma (0 CFU)" fill="#6366f1" opacity={0.6} radius={[4, 4, 0, 0]} />
                <Line type="monotone" dataKey="dropout_pct" name="Rinuncia Formale (Dropout)" stroke="#f43f5e" strokeWidth={3} dot={{ r: 6 }} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Labor Market Mismatch */}
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
          <h3 className="text-xl font-bold text-white mb-6">
            <T it="Paradosso Excelsior: Mismatch tra Domanda e Offerta" en="Excelsior Paradox: Labor Supply-Demand Mismatch" />
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={job_market_mismatch} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="macroarea" stroke="#888" />
                <YAxis stroke="#888" tickFormatter={(val) => `${val}%`} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Bar dataKey="difficulty_finding_candidates_pct" name="Difficoltà Reperimento (%)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                <Bar dataKey="skills_mismatch_pct" name="Mismatch Qualitativo (%)" fill="#4f46e5" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* NEET Time Trend */}
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl lg:col-span-2">
          <h3 className="text-xl font-bold text-white mb-6">
            <T it="Andamento NEET per Genere (2018-2024)" en="NEET Trends by Gender (2018-2024)" />
          </h3>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={neet_demographics} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="year" stroke="#888" />
                <YAxis stroke="#888" tickFormatter={(val) => `${val}%`} domain={[10, 30]} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Area type="monotone" dataKey="female_pct" name="Female NEET (%)" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.2} />
                <Area type="monotone" dataKey="male_pct" name="Male NEET (%)" stroke="#10b981" fill="#10b981" fillOpacity={0.2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
