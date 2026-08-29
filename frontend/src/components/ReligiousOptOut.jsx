import React, { useState, useEffect } from 'react';
import { useLanguage } from "../contexts/LanguageContext";
import { T } from './T';
import { motion } from 'framer-motion';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart, Cell } from 'recharts';
import * as LucideIcons from 'lucide-react';
import SourceBadge from './SourceBadge';

export default function ReligiousOptOut() {
  const { lang } = useLanguage();
  const isIt = lang === "it";
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/religious_opt_out.json`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load religious opt-out data:", err);
        setError(err.message || 'Failed to load data');
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="w-full h-96 flex items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
    </div>
  );

  if (error || !data) return (
    <div className="w-full py-16 flex flex-col items-center justify-center text-zinc-400">
      <p className="text-lg font-medium">Failed to load data</p>
      <p className="text-sm mt-2">{error}</p>
    </div>
  );

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 py-12">
      
      {/* Header Section */}
      <div className="mb-12 border-b border-zinc-800 pb-8 flex flex-col md:flex-row justify-between items-start gap-6">
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-purple-500/20 rounded-xl border border-purple-500/30">
              <LucideIcons.BookX className="text-purple-400" size={28} />
            </div>
            <h2 className="text-4xl font-black text-white">
              <T it="Opt-out IRC" en="IRC Opt-out" />
            </h2>
          </div>
          <p className="text-zinc-400 max-w-2xl text-lg">
            <T 
              it="Analisi della scelta di non avvalersi dell'Insegnamento della Religione Cattolica (IRC), ottenuta tramite Accesso Civico (FOIA) e campagne open data." 
              en="Analysis of the choice to opt-out of Catholic Religious Instruction (IRC), obtained via FOIA requests and open data campaigns." 
            />
          </p>
        </div>
        <SourceBadge agency="UAAR / FOIA" topicKey="religione" year="2023" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        
        {/* National Trend Chart */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-zinc-950/50 border border-zinc-800 rounded-3xl p-6"
        >
          <h3 className="text-xl font-bold text-white mb-6">
            <T it="Trend Nazionale (2018-2023)" en="National Trend (2018-2023)" />
          </h3>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.national_trend}>
                <defs>
                  <linearGradient id="optOutColor" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#c084fc" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#c084fc" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="year" stroke="#71717a" tick={{fill: '#71717a'}} axisLine={false} tickLine={false} />
                <YAxis stroke="#71717a" tick={{fill: '#71717a'}} axisLine={false} tickLine={false} tickFormatter={(val) => `${val}%`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '12px' }}
                  itemStyle={{ color: '#c084fc', fontWeight: 'bold' }}
                  labelStyle={{ color: '#ffffff' }}
                />
                <Area type="monotone" dataKey="optOutPercentage" name={isIt ? "% Esonero" : "Opt-out %"} stroke="#c084fc" strokeWidth={3} fillOpacity={1} fill="url(#optOutColor)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Macro Regions Chart */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="bg-zinc-950/50 border border-zinc-800 rounded-3xl p-6"
        >
          <h3 className="text-xl font-bold text-white mb-6">
            <T it="Divario Territoriale" en="Territorial Divide" />
          </h3>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.macro_regions} layout="vertical" margin={{ top: 0, right: 30, left: 20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                <XAxis type="number" stroke="#71717a" tick={{fill: '#71717a'}} tickFormatter={(val) => `${val}%`} />
                <YAxis dataKey="region" type="category" stroke="#71717a" tick={{fill: '#71717a', fontSize: 12}} width={80} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '12px' }}
                  itemStyle={{ color: '#ffffff' }}
                  labelStyle={{ color: '#ffffff' }}
                  cursor={{fill: '#27272a', opacity: 0.4}}
                />
                <Bar dataKey="optOutPercentage" name={isIt ? "% Esonero" : "Opt-out %"} fill="#818cf8" radius={[0, 4, 4, 0]}>
                  {
                    data.macro_regions.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.optOutPercentage > 20 ? '#818cf8' : '#4f46e5'} />
                    ))
                  }
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

      </div>

      {/* Key Insights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {data.key_insights.map((insight, idx) => {
          const IconComponent = LucideIcons[insight.icon] || LucideIcons.Info;
          return (
            <motion.div 
              key={insight.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1 }}
              className="bg-white/[0.02] border border-white/5 p-6 rounded-2xl"
            >
              <div className="p-3 rounded-xl bg-white/5 w-fit mb-4">
                <IconComponent className="text-white" size={24} />
              </div>
              <h4 className="text-lg font-bold text-white mb-2">
                <T it={insight.itTitle} en={insight.enTitle} />
              </h4>
              <p className="text-zinc-400 text-sm leading-relaxed">
                <T it={insight.itDesc} en={insight.enDesc} />
              </p>
            </motion.div>
          );
        })}
      </div>

      {/* School Types Chart */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="bg-zinc-950/50 border border-zinc-800 rounded-3xl p-6 lg:p-10 flex flex-col md:flex-row gap-8 items-center"
      >
        <div className="w-full md:w-1/3">
          <h3 className="text-2xl font-black text-white mb-4">
            <T it="Impatto per Ciclo Scolastico" en="Impact by School Cycle" />
          </h3>
          <p className="text-zinc-400 mb-6">
            <T 
              it="Il tasso di non avvalentesi cresce esponenzialmente con l'età degli studenti. Nelle scuole superiori (Secondaria II grado), quasi un terzo degli studenti decide di non frequentare l'IRC." 
              en="The opt-out rate grows exponentially with students' age. In high schools (Secondary 2nd degree), almost a third of students choose not to attend IRC." 
            />
          </p>
        </div>
        
        <div className="w-full md:w-2/3 h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.school_types}>
              <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
              <XAxis dataKey="enName" stroke="#71717a" tick={{fill: '#71717a'}} />
              <YAxis stroke="#71717a" tick={{fill: '#71717a'}} tickFormatter={(val) => `${val}%`} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '12px' }}
                itemStyle={{ color: '#ffffff' }}
                labelStyle={{ color: '#ffffff' }}
                cursor={{fill: '#27272a', opacity: 0.4}}
              />
              <Bar dataKey="optOutPercentage" name={isIt ? "% Esonero" : "Opt-out %"} fill="#f43f5e" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
      
    </div>
  );
}
