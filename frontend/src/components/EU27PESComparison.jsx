import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Building2, Search, ArrowRight, ShieldCheck, Database, Building, UserCheck } from 'lucide-react';
import { T } from './T';
import SourceBadge from './SourceBadge';
import pesData from '../assets/eu27_pes_comparison.json';

const getBadgeColor = (value, type) => {
  if (type === 'governance') {
    if (value === 'Centralized') return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    if (value === 'Mixed/Federal') return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    if (value === 'Decentralized') return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
  } else if (type === 'integration') {
    if (value === 'Integrated') return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    if (value === 'Coordinated') return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    if (value === 'Fragmented') return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
  } else {
    // High/Medium/Low
    if (value === 'High') return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    if (value === 'Medium') return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    if (value === 'Low') return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
  }
  return 'bg-zinc-800 text-zinc-300 border-zinc-700';
};

const ValueBadge = ({ value, type }) => (
  <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${getBadgeColor(value, type)}`}>
    <T it={value === 'Centralized' ? 'Centralizzato' : value === 'Mixed/Federal' ? 'Misto' : value === 'Decentralized' ? 'Decentrato' : value === 'Integrated' ? 'Integrato' : value === 'Coordinated' ? 'Coordinato' : value === 'Fragmented' ? 'Frammentato' : value === 'High' ? 'Alto' : value === 'Medium' ? 'Medio' : value === 'Low' ? 'Basso' : value} en={value} />
  </span>
);

export default function EU27PESComparison() {
  const [filterGov, setFilterGov] = useState('All');

  const filteredData = filterGov === 'All' 
    ? pesData 
    : pesData.filter(d => d.governance === filterGov);

  return (
    <section className="w-full py-16 bg-zinc-950 text-white border-t border-zinc-800 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/10 via-zinc-950 to-zinc-950 pointer-events-none" />
      
      <div className="max-w-7xl mx-auto px-4 relative z-10">
        <div className="mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 flex items-center gap-3">
            <Building2 className="w-8 h-8 text-indigo-400" />
            <T it="Servizi Pubblici per l'Impiego EU27" en="EU27 Public Employment Services" />
          </h2>
          <p className="text-zinc-400 max-w-3xl text-lg">
            <T 
              it="Un'analisi comparativa dei 27 servizi pubblici per l'impiego europei. Malta (Jobsplus) opera con un modello centralizzato di stile britannico, offrendo alta integrazione digitale, in netto contrasto con il sistema italiano dei CPI, frammentato su base regionale e con bassa intensità di attivazione." 
              en="A comparative analysis of the 27 European public employment services. Malta (Jobsplus) operates a British-style centralized model, offering high digital integration, in stark contrast to Italy's CPI system, which is regionally fragmented with low activation intensity." 
            />
          </p>
        </div>

        {/* Controls */}
        <div className="mb-6 flex flex-wrap gap-4 items-center justify-between">
          <div className="flex items-center gap-3 bg-zinc-900/50 p-2 rounded-lg border border-zinc-800">
            <Search className="w-4 h-4 text-zinc-400 ml-2" />
            <select 
              className="bg-transparent border-none text-sm text-zinc-200 focus:ring-0 outline-none pr-4"
              value={filterGov}
              onChange={(e) => setFilterGov(e.target.value)}
            >
              <option value="All">All Governance Models</option>
              <option value="Centralized">Centralized</option>
              <option value="Mixed/Federal">Mixed / Federal</option>
              <option value="Decentralized">Decentralized</option>
            </select>
          </div>
          <SourceBadge agency="EU PES Network" topicKey="pes" />
        </div>

        {/* Table */}
        <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl overflow-hidden mb-16 backdrop-blur-sm">
          <div className="overflow-x-auto overflow-y-auto max-h-[500px] custom-scrollbar">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-zinc-900/90 text-zinc-300 border-b border-zinc-800 uppercase text-xs font-semibold sticky top-0 z-10 backdrop-blur-md shadow-sm">
                <tr>
                  <th className="px-6 py-4"><T it="Paese" en="Country" /></th>
                  <th className="px-6 py-4"><T it="Nome PES" en="PES Name" /></th>
                  <th className="px-6 py-4"><T it="Governance" en="Governance" /></th>
                  <th className="px-6 py-4"><T it="Maturità Digitale" en="Digital Maturity" /></th>
                  <th className="px-6 py-4"><T it="Attivazione" en="Activation Intensity" /></th>
                  <th className="px-6 py-4"><T it="Servizi Imprese" en="Employer Svcs" /></th>
                  <th className="px-6 py-4"><T it="Integrazione Sussidi" en="Benefits Integration" /></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/50">
                {filteredData.map((row, idx) => {
                  const isItaly = row.country === 'Italy';
                  const isMalta = row.country === 'Malta';
                  
                  let rowClasses = "hover:bg-zinc-800/30 transition-colors";
                  if (isItaly) rowClasses = "bg-rose-500/5 hover:bg-rose-500/10 relative";
                  if (isMalta) rowClasses = "bg-emerald-500/5 hover:bg-emerald-500/10 relative";

                  return (
                    <motion.tr 
                      key={row.country}
                      initial={{ opacity: 0, y: 10 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: Math.min(idx * 0.02, 0.5) }}
                      className={rowClasses}
                    >
                      <td className="px-6 py-4 font-medium flex items-center gap-2">
                        {isItaly && <div className="absolute left-0 top-0 bottom-0 w-1 bg-rose-500" />}
                        {isMalta && <div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-500" />}
                        <span className="text-xl">{row.flag}</span>
                        <T it={row.country === 'Italy' ? 'Italia' : row.country === 'Spain' ? 'Spagna' : row.country === 'France' ? 'Francia' : row.country === 'Germany' ? 'Germania' : row.country} en={row.country} />
                      </td>
                      <td className="px-6 py-4 text-zinc-300">{row.pesName}</td>
                      <td className="px-6 py-4"><ValueBadge value={row.governance} type="governance" /></td>
                      <td className="px-6 py-4"><ValueBadge value={row.digitalMaturity} type="level" /></td>
                      <td className="px-6 py-4"><ValueBadge value={row.activationIntensity} type="level" /></td>
                      <td className="px-6 py-4"><ValueBadge value={row.employerServices} type="level" /></td>
                      <td className="px-6 py-4"><ValueBadge value={row.benefitsIntegration} type="integration" /></td>
                    </motion.tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Deep Dive Malta vs Italy */}
        <h3 className="text-2xl font-bold mb-8 flex items-center gap-3">
          <T it="Confronto Diretto: Jobsplus vs CPI" en="Direct Comparison: Jobsplus vs CPI" />
        </h3>
        
        <div className="grid md:grid-cols-2 gap-8">
          {/* Malta Card */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="bg-zinc-900/40 border border-emerald-500/20 rounded-xl p-6 relative overflow-hidden group"
          >
            <div className="absolute top-0 right-0 p-4 opacity-10 transform translate-x-4 -translate-y-4 group-hover:scale-110 transition-transform">
              <ShieldCheck className="w-32 h-32 text-emerald-500" />
            </div>
            
            <div className="flex items-center gap-3 mb-6 relative z-10">
              <span className="text-3xl">🇲🇹</span>
              <div>
                <h4 className="text-xl font-bold text-white">Malta Jobsplus</h4>
                <p className="text-emerald-400 text-sm"><T it="Modello Centralizzato" en="Centralized Model" /></p>
              </div>
            </div>

            <ul className="space-y-4 relative z-10">
              <li className="flex gap-3">
                <Database className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-zinc-200"><T it="Digital-First" en="Digital-First" /></p>
                  <p className="text-sm text-zinc-400"><T it="Piattaforma unica per matching, formazione e sussidi" en="Single platform for matching, training, and benefits" /></p>
                </div>
              </li>
              <li className="flex gap-3">
                <Building className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-zinc-200"><T it="One-Stop-Shop" en="One-Stop-Shop" /></p>
                  <p className="text-sm text-zinc-400"><T it="Sportello unico ispirato al modello britannico (Jobcentre Plus)" en="Single front-office inspired by the UK model (Jobcentre Plus)" /></p>
                </div>
              </li>
              <li className="flex gap-3">
                <UserCheck className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-zinc-200"><T it="Attivazione Integrata" en="Integrated Activation" /></p>
                  <p className="text-sm text-zinc-400"><T it="Stretto legame tra erogazione dei sussidi e ricerca attiva di lavoro" en="Tight link between benefit distribution and active job search" /></p>
                </div>
              </li>
            </ul>
          </motion.div>

          {/* Italy Card */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="bg-zinc-900/40 border border-rose-500/20 rounded-xl p-6 relative overflow-hidden group"
          >
            <div className="absolute top-0 right-0 p-4 opacity-10 transform translate-x-4 -translate-y-4 group-hover:scale-110 transition-transform">
              <Building2 className="w-32 h-32 text-rose-500" />
            </div>
            
            <div className="flex items-center gap-3 mb-6 relative z-10">
              <span className="text-3xl">🇮🇹</span>
              <div>
                <h4 className="text-xl font-bold text-white">Italia CPI</h4>
                <p className="text-rose-400 text-sm"><T it="Modello Frammentato" en="Fragmented Model" /></p>
              </div>
            </div>

            <ul className="space-y-4 relative z-10">
              <li className="flex gap-3">
                <Database className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-zinc-200"><T it="Sistemi Multipli" en="Multiple Systems" /></p>
                  <p className="text-sm text-zinc-400"><T it="20 sistemi informativi regionali con interoperabilità limitata" en="20 regional IT systems with limited interoperability" /></p>
                </div>
              </li>
              <li className="flex gap-3">
                <Building className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-zinc-200"><T it="Responsabilità Divise" en="Split Responsibilities" /></p>
                  <p className="text-sm text-zinc-400"><T it="Gestione divisa tra INPS (sussidi) e CPI regionali (attivazione)" en="Management split between INPS (benefits) and regional CPIs (activation)" /></p>
                </div>
              </li>
              <li className="flex gap-3">
                <UserCheck className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-zinc-200"><T it="Bassa Attivazione" en="Low Activation" /></p>
                  <p className="text-sm text-zinc-400"><T it="Scarsa capacità di matching e condizionalità debole" en="Poor matching capacity and weak conditionality" /></p>
                </div>
              </li>
            </ul>
          </motion.div>
        </div>

      </div>
    </section>
  );
}
