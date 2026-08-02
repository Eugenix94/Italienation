import React, { useState, useEffect } from 'react';
import { T } from './T';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import * as LucideIcons from 'lucide-react';
import SourceBadge from './SourceBadge';

export default function StructuralDeepDives() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/structural_deep_dives.json`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load structural deep dives data:", err);
        setLoading(false);
      });
  }, []);

  if (loading || !data) return (
    <div className="w-full h-96 flex items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
    </div>
  );

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 py-12 space-y-16">
      
      {/* STEM Gender Gap */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="bg-zinc-900/50 rounded-2xl border border-zinc-800 p-6 md:p-8"
      >
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <LucideIcons.Users className="text-pink-500" size={24} />
            <h3 className="text-2xl font-bold text-white">
              <T it={data.stemGenderGap.title.it} en={data.stemGenderGap.title.en} />
            </h3>
          </div>
          <p className="text-zinc-400">
            <T it={data.stemGenderGap.description.it} en={data.stemGenderGap.description.en} />
          </p>
        </div>
        
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.stemGenderGap.data} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
              <XAxis dataKey="track" stroke="#a1a1aa" angle={-45} textAnchor="end" height={80} />
              <YAxis stroke="#a1a1aa" tickFormatter={(value) => `${value}%`} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#fff' }}
                itemStyle={{ color: '#e4e4e7' }}
                formatter={(value) => `${value}%`}
              />
              <Legend />
              <Bar dataKey="male" name="Maschi / Male" stackId="a" fill="#3b82f6" />
              <Bar dataKey="female" name="Femmine / Female" stackId="a" fill="#ec4899" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Infrastructure Safety */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="bg-zinc-900/50 rounded-2xl border border-zinc-800 p-6 md:p-8"
      >
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <LucideIcons.Building2 className="text-orange-500" size={24} />
            <h3 className="text-2xl font-bold text-white">
              <T it={data.infrastructureSafety.title.it} en={data.infrastructureSafety.title.en} />
            </h3>
          </div>
          <p className="text-zinc-400">
            <T it={data.infrastructureSafety.description.it} en={data.infrastructureSafety.description.en} />
          </p>
        </div>
        
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.infrastructureSafety.data} layout="vertical" margin={{ top: 20, right: 30, left: 80, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" horizontal={false} />
              <XAxis type="number" stroke="#a1a1aa" tickFormatter={(value) => `${value}%`} />
              <YAxis dataKey="area" type="category" stroke="#a1a1aa" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#fff' }}
                formatter={(value) => `${value}%`}
              />
              <Legend />
              <Bar dataKey="withoutCertificate" name="Senza Agibilità / No Cert." fill="#f97316" />
              <Bar dataKey="seismicRisk" name="Rischio Sismico / Seismic Risk" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Tertiary Dropouts */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="bg-zinc-900/50 rounded-2xl border border-zinc-800 p-6 md:p-8"
      >
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <LucideIcons.GraduationCap className="text-indigo-500" size={24} />
            <h3 className="text-2xl font-bold text-white">
              <T it={data.tertiaryDropouts.title.it} en={data.tertiaryDropouts.title.en} />
            </h3>
          </div>
          <p className="text-zinc-400">
            <T it={data.tertiaryDropouts.description.it} en={data.tertiaryDropouts.description.en} />
          </p>
        </div>
        
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.tertiaryDropouts.data} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
              <XAxis dataKey="diploma" stroke="#a1a1aa" />
              <YAxis stroke="#a1a1aa" tickFormatter={(value) => `${value}%`} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#fff' }}
                formatter={(value) => `${value}%`}
              />
              <Bar dataKey="dropoutRate" name="Tasso di Abbandono / Dropout Rate" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

    </div>
  );
}
