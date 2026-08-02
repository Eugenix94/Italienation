import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Globe, Users, TrendingUp, Briefcase } from 'lucide-react';
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import { T } from './T';
import SourceBadge from './SourceBadge';

export default function MigrationAndRemittances() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/migration_and_remittances.json`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading migration data:", err);
        setLoading(false);
      });
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-[400px] text-zinc-400 bg-zinc-950">
        <T it="Caricamento dati migratori..." en="Loading migration data..." />
      </div>
    );
  }

  const { istat_non_observed_economy, inapp_migrant_exploitation, remittances } = data;

  return (
    <div className="w-full bg-zinc-950 text-white font-sans relative overflow-hidden py-16 px-6 lg:px-8 border-t border-zinc-800/50">
      
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-emerald-900/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="mb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-medium mb-4">
              <Globe size={16} />
              <T it="Fattori di Spinta Migratori" en="Migration Push Factors" />
            </div>
            <h2 className="text-3xl sm:text-5xl font-black tracking-tight mb-6">
              <T it="Rimesse e Lavoro Sommerso" en="Remittances & Undeclared Work" />
            </h2>
            <p className="text-lg text-zinc-400 max-w-3xl leading-relaxed">
              <T 
                it="L'economia sommersa italiana funge da polo attrattivo e al contempo da trappola di sfruttamento per la forza lavoro migrante. I dati INAPP ed ELA rivelano tassi drammatici di lavoro nero, che alimentano le rimesse censite da Banca d'Italia in una dinamica speculare all'emigrazione italiana del Novecento." 
                en="Italy's underground economy acts as both a magnet and an exploitation trap for migrant labor. INAPP and ELA data reveal dramatic rates of undeclared work, fueling the remittances recorded by the Bank of Italy in a dynamic mirroring early 20th-century Italian emigration." 
              />
            </p>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-8">
          
          {/* ISTAT Macro Card */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="lg:col-span-4 bg-zinc-900/50 border border-white/10 backdrop-blur-md rounded-3xl p-8 flex flex-col justify-center"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-indigo-500/20 rounded-xl">
                <TrendingUp className="text-indigo-400" size={24} />
              </div>
              <h3 className="text-xl font-bold"><T it="Economia Non Osservata" en="Non-Observed Economy" /></h3>
            </div>
            
            <div className="space-y-8">
              <div>
                <p className="text-sm text-zinc-400 uppercase tracking-wider font-bold mb-1">
                  <T it="Valore Sommerso (2023)" en="Underground Value (2023)" />
                </p>
                <p className="text-5xl font-black text-indigo-400">
                  €{istat_non_observed_economy.year_2023.underground_economy_billions}B
                </p>
                <p className="text-sm text-zinc-400 mt-2">
                  ~{istat_non_observed_economy.year_2023.gdp_share_pct}% <T it="del PIL Nazionale" en="of National GDP" />
                </p>
              </div>
              
              <div>
                <p className="text-sm text-zinc-400 uppercase tracking-wider font-bold mb-1">
                  <T it="Unità di Lavoro Irregolare" en="Irregular Work Units" />
                </p>
                <p className="text-4xl font-black text-white">
                  {istat_non_observed_economy.year_2023.irregular_workers_millions}M
                </p>
                <p className="text-sm text-rose-400 mt-2 font-medium">
                  +145,000 <T it="rispetto al 2022" en="compared to 2022" />
                </p>
              </div>
            </div>
            <div className="mt-8">
              <SourceBadge label="ISTAT 2024" url="https://www.istat.it/en/press-release/non-observed-economy-in-national-accounts-years-2020-2023/" />
            </div>
          </motion.div>

          {/* INAPP Migrant Exploitation Chart */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="lg:col-span-8 bg-zinc-900/50 border border-white/10 backdrop-blur-md rounded-3xl p-8"
          >
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-rose-500/20 rounded-xl">
                  <Users className="text-rose-400" size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-bold"><T it="Sfruttamento Migrante & Lavoro Nero" en="Migrant Exploitation & Black Labor" /></h3>
                  <p className="text-sm text-zinc-400"><T it="Indagine su 2.000+ lavoratori migranti nelle province ad alto rischio" en="Survey of 2,000+ migrant workers in high-risk provinces" /></p>
                </div>
              </div>
            </div>
            
            <div className="h-64" aria-hidden="false">
              <span className="sr-only">
                <T 
                  it="Grafico a barre orizzontali che mostra che il 51% dei migranti intervistati lavora senza contratto e il 55% è sottopagato." 
                  en="Horizontal bar chart showing that 51% of surveyed migrants work without a contract and 55% are underpaid." 
                />
              </span>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={inapp_migrant_exploitation} layout="vertical" margin={{ top: 0, right: 30, left: 140, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                  <XAxis type="number" domain={[0, 60]} tickFormatter={(val) => `${val}%`} stroke="#71717a" />
                  <YAxis dataKey="category" type="category" stroke="#d4d4d8" width={130} tick={{ fontSize: 11 }} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff' }}
                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={24}>
                    {inapp_migrant_exploitation.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.value > 50 ? '#f43f5e' : entry.value > 25 ? '#fbbf24' : '#52525b'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-6 flex flex-wrap gap-4">
              <SourceBadge label="INAPP 2024" url="https://www.inapp.gov.it/en/press-and-media/press-releases/26-11-2024-indagine-sullesposizione-al-lavoro-sommerso" />
              <SourceBadge label="EU Labour Authority" url="https://www.ela.europa.eu/sites/default/files/2024-02/IT_UDW_Factsheet_2017-Italy.pdf" />
            </div>
          </motion.div>

        </div>

        {/* Remittances Text Banner */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="bg-emerald-950/30 border border-emerald-500/20 rounded-3xl p-8"
        >
          <div className="flex flex-col md:flex-row gap-8 items-center">
            <div className="shrink-0 p-6 bg-emerald-900/50 rounded-2xl border border-emerald-500/30">
              <Globe className="text-emerald-400 w-16 h-16" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">
                <T it="Il Flusso delle Rimesse: Paralleli Storici" en="The Flow of Remittances: Historical Parallels" />
              </h3>
              <p className="text-emerald-100/70 text-lg leading-relaxed mb-6">
                <T it={remittances.description_it} en={remittances.description_en} />
              </p>
              <div className="flex flex-wrap gap-4">
                <SourceBadge label="Banca d'Italia Open Data" url="https://www.bancaditalia.it/statistiche/tematiche/rapporti-estero/rimesse-immigrati/index.html" />
                <SourceBadge label="Fondazione ISMU" url="https://www.ismu.org/rimesse-dei-migranti-banca-dati-sulle-migrazioni/" />
                <SourceBadge label="World Bank" url="https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/brief/migration-remittances-data" />
              </div>
            </div>
          </div>
        </motion.div>

      </div>
    </div>
  );
}
