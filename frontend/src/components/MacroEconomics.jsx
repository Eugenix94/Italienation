import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import { T } from './T';
import { demographic_collapse, pnrr_spending, pension_gap } from '../assets/macro_metrics.json';

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

const COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#f43f5e'];

export default function MacroEconomics() {
  return (
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
  );
}
