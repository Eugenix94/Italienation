import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import { T } from './T';
import SourceBadge from './SourceBadge';
import { demographic_collapse, pnrr_spending, pension_gap, tfp_stagnation, dependency_ratio, tax_wedge_comparison, real_gdp_growth, brain_drain_migration } from '../assets/macro_metrics.json';

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

import { useLanguage } from '../contexts/LanguageContext';

export default function MacroEconomics() {
  const { lang } = useLanguage();
  const isIt = lang === 'it';
  return (
    <div className="space-y-16 pb-24 border-b border-zinc-800">
      <div className="text-center max-w-3xl mx-auto mb-12">
        <h2 className="text-3xl font-bold text-white mb-4">
          <T it="Macro-Economia e Demografia" en="Macro-Economics and Demographics" />
        </h2>
        <p className="text-zinc-400 text-lg mb-6">
          <T 
            it="Contesto macro-strutturale: crollo demografico, distribuzione dei fondi PNRR e divari pensionistici." 
            en="Macro-structural context: demographic collapse, PNRR fund distribution, and pension gaps." 
          />
        </p>
        <p className="text-zinc-300 text-base leading-relaxed">
          <T 
            it="Questi indicatori macroeconomici non sono entità astratte: sono le conseguenze dirette e le cause scatenanti del fallimento del sistema educativo. Il mancato investimento nel capitale umano si traduce in stagnazione della produttività, crisi fiscale, e impossibilità di sostenere il patto intergenerazionale." 
            en="These macroeconomic indicators are not abstract entities: they are the direct consequences and root causes of the educational system's failure. The lack of investment in human capital translates into productivity stagnation, fiscal crises, and the impossibility of sustaining the intergenerational pact." 
          />
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl lg:col-span-2">
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Collasso Demografico e Chiusura Scuole" en="Demographic Collapse and School Closures" />
            </h3>
            <SourceBadge agency="ISTAT / MUR" year="2023" url="https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z07,1.0/POP/IT1,22_289,1.0" />
          </div>
          <div className="h-[450px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={demographic_collapse} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="year" stroke="#888" />
                <YAxis yAxisId="left" stroke="#888" label={{ value: isIt ? 'Nascite (Migliaia)' : 'Births (Thousands)', angle: -90, position: 'insideLeft', fill: '#888' }} />
                <YAxis yAxisId="right" orientation="right" stroke="#f43f5e" label={{ value: isIt ? 'Chiusure Scolastiche' : 'School Closures', angle: 90, position: 'insideRight', fill: '#f43f5e' }} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Area yAxisId="left" type="monotone" dataKey="births_thousands" name={isIt ? 'Nascite (k)' : 'Births (k)'} stroke="#10b981" fill="#10b981" fillOpacity={0.2} />
                <Area yAxisId="right" type="monotone" dataKey="school_closures" name={isIt ? 'Chiusure Cumulative' : 'Cumulative Closures'} stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Distribuzione Spesa PNRR Istruzione" en="PNRR Education Spending Distribution" />
            </h3>
            <SourceBadge agency="OpenPNRR" year="2024" url="https://openpnrr.it/temi/istruzione-e-ricerca" />
          </div>
          <div className="h-[380px]">
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
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-6">
            <h3 className="text-xl font-bold text-white">
              <T it="Divario Pensionistico Proiettato" en="Projected Pension Gap" />
            </h3>
            <SourceBadge agency="INPS / Cnel" year="2023" url="https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche/dati-pensioni-e-beneficiari.html" />
          </div>
          <div className="h-[380px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pension_gap} margin={{ top: 20, right: 30, left: 20, bottom: 5 }} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                <XAxis type="number" stroke="#888" tickFormatter={(val) => `€${val}`} />
                <YAxis type="category" dataKey="track" stroke="#888" width={120} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Bar dataKey="expected_pension_eur" name={isIt ? 'Pensione Mensile Attesa (€)' : 'Expected Monthly Pension (€)'} fill="#4f46e5" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-12 mt-8">
        {/* TFP Stagnation */}
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-2">
            <h3 className="text-xl font-bold text-white">
              <T it="Stagnazione Produttività (TFP)" en="Total Factor Productivity (TFP) Stagnation" />
            </h3>
            <SourceBadge agency="Bank of Italy / OECD" year="2024" url="https://data-explorer.oecd.org/vis?lc=en&df[ds]=DisseminateFinalDMZ&df[id]=DSD_EAM%40DF_MFP&df[ag]=OECD.ECO.MAC" />
          </div>
          <p className="text-sm text-zinc-300 mb-8">
            <T it="Indice base 100 nel 2000. Il capitale umano non valorizzato frena la crescita." en="Index base 100 in 2000. Unutilized human capital stifles growth." />
          </p>
          <div className="h-[380px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={tfp_stagnation} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="year" stroke="#888" />
                <YAxis domain={[95, 125]} stroke="#888" />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Area type="monotone" dataKey="germany" name={isIt ? 'Germania' : 'Germany'} stroke="#10b981" fill="none" strokeWidth={3} />
                <Area type="monotone" dataKey="france" name={isIt ? 'Francia' : 'France'} stroke="#3b82f6" fill="none" strokeWidth={3} />
                <Area type="monotone" dataKey="italy" name={isIt ? 'Italia' : 'Italy'} stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.2} strokeWidth={4} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Dependency Ratio */}
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-2">
            <h3 className="text-xl font-bold text-white">
              <T it="Rapporto di Dipendenza Pensionistica" en="Pension Dependency Ratio" />
            </h3>
            <SourceBadge agency="ISTAT" year="2024" url="https://demo.istat.it/app/?i=POS&l=it" />
          </div>
          <p className="text-sm text-zinc-300 mb-8">
            <T it="Lavoratori attivi per pensionato. Soglia critica di sostenibilità a 1.5" en="Active workers per retiree. Critical sustainability threshold at 1.5" />
          </p>
          <div className="h-[380px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={dependency_ratio} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="year" stroke="#888" />
                <YAxis domain={[0.5, 2.5]} stroke="#888" />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Area type="monotone" dataKey="sustainability_threshold" name={isIt ? 'Soglia Sostenibilità' : 'Sustainability Threshold'} stroke="#f59e0b" strokeDasharray="5 5" fill="none" strokeWidth={2} />
                <Area type="monotone" dataKey="workers_per_retiree" name={isIt ? 'Lavoratori per Pensionato' : 'Workers per Retiree'} stroke="#4f46e5" fill="#4f46e5" fillOpacity={0.3} strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 mt-8">
        {/* Cuneo Fiscale */}
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-2">
            <h3 className="text-xl font-bold text-white">
              <T it="Cuneo Fiscale (Tax Wedge)" en="Tax Wedge (Cuneo Fiscale)" />
            </h3>
            <SourceBadge agency="OECD" year="2023" url="https://data-explorer.oecd.org/vis?lc=en&df[ds]=DisseminateFinalDMZ&df[id]=DSD_EARNINGS%40TAXWEDGE&df[ag]=OECD.ELS.SAE" />
          </div>
          <p className="text-sm text-zinc-300 mb-8">
            <T it="Percentuale di prelievo fiscale sul lavoro. Uno dei più alti in area OCSE." en="Percentage of tax burden on labor. One of the highest in the OECD area." />
          </p>
          <div className="h-[380px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={tax_wedge_comparison} margin={{ top: 20, right: 30, left: 0, bottom: 40 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="country" stroke="#888" tick={{ fontSize: 12 }} interval={0} angle={-45} textAnchor="end" />
                <YAxis stroke="#888" domain={[0, 50]} tickFormatter={(val) => `${val}%`} />
                <RechartsTooltip content={<CustomTooltip />} />
                <Bar dataKey="tax_wedge_pct" name={isIt ? 'Cuneo Fiscale (%)' : 'Tax Wedge (%)'} radius={[4, 4, 0, 0]}>
                  {tax_wedge_comparison.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.country === 'Italy' ? '#f43f5e' : entry.country === 'EU Avg' ? '#3b82f6' : '#4f46e5'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Real GDP Growth */}
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-2">
            <h3 className="text-xl font-bold text-white">
              <T it="Stagnazione PIL Reale" en="Real GDP Stagnation" />
            </h3>
            <SourceBadge agency="World Bank" year="2024" url="https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG" />
          </div>
          <p className="text-sm text-zinc-300 mb-8">
            <T it="PIL reale pro capite (Indice 100 = 2000). 25 anni di mancata crescita." en="Real GDP per capita (Index 100 = 2000). 25 years of lost growth." />
          </p>
          <div className="h-[380px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={real_gdp_growth} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="year" stroke="#888" />
                <YAxis domain={[85, 135]} stroke="#888" />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Area type="monotone" dataKey="eu_avg" name={isIt ? 'Media EU' : 'EU Average'} stroke="#3b82f6" fill="none" strokeWidth={3} />
                <Area type="monotone" dataKey="italy" name={isIt ? 'Italia' : 'Italy'} stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.2} strokeWidth={4} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Brain Drain */}
        <div className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl">
          <div className="flex flex-col xl:flex-row xl:justify-between xl:items-start gap-2 mb-2">
            <h3 className="text-xl font-bold text-white">
              <T it="Fuga dei Cervelli" en="Brain Drain (Net Migration)" />
            </h3>
            <SourceBadge agency="SVIMEZ / ISTAT" year="2023" url="https://demo.istat.it/app/?i=TRF&l=it" />
          </div>
          <p className="text-sm text-zinc-300 mb-8">
            <T it="Laureati italiani emigrati (in migliaia). L'istruzione come export a perdere." en="Emigrated Italian graduates (in thousands). Education as a loss-making export." />
          </p>
          <div className="h-[380px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={brain_drain_migration} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="year" stroke="#888" />
                <YAxis stroke="#888" />
                <RechartsTooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Area type="monotone" dataKey="graduates_emigrated_thousands" name={isIt ? 'Laureati Emigrati (k)' : 'Emigrated Graduates (k)'} stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
