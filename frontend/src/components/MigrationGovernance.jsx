import React from 'react';
import { motion } from 'framer-motion';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, ScatterChart, Scatter, ZAxis } from 'recharts';
import { Globe, Users, GraduationCap, ArrowUpRight, ArrowDownRight, TrendingDown, DollarSign, ShieldCheck } from 'lucide-react';
import SourceBadge from './SourceBadge';
import data from '../assets/migration_governance.json';

const MigrationGovernance = () => {
  const { lang } = useLanguage();
  const isIt = lang === 'it';

  const immigrationData = data.immigration_into_italy.top_nationalities.map(n => ({
    name: n.country,
    nameIt: n.country_it,
    population: n.population,
    wgi: n.wgi_governance_pctl,
    gdp: n.gdp_per_capita_usd,
    type: n.migration_type,
    flag: n.flag
  }));

  const emigrationData = data.emigration_from_italy.top_destinations.map(n => ({
    name: n.country,
    nameIt: n.country_it,
    registered: n.aire_registered,
    wgi: n.wgi_governance_pctl,
    flag: n.flag
  }));

  const bd = data.emigration_from_italy.brain_drain;

  const wgiLabel = (pctl) => {
    if (pctl >= 80) return { text: isIt ? 'Eccellente' : 'Excellent', color: 'text-emerald-400' };
    if (pctl >= 60) return { text: isIt ? 'Buona' : 'Good', color: 'text-blue-400' };
    if (pctl >= 40) return { text: isIt ? 'Moderata' : 'Moderate', color: 'text-amber-400' };
    if (pctl >= 20) return { text: isIt ? 'Debole' : 'Weak', color: 'text-orange-400' };
    return { text: isIt ? 'Critica' : 'Critical', color: 'text-rose-400' };
  };

  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload?.length) return null;
    const d = payload[0].payload;
    const gov = wgiLabel(d.wgi);
    return (
      <div className="bg-zinc-900 border border-zinc-700 rounded-xl px-4 py-3 shadow-2xl text-sm">
        <p className="font-bold text-white">{d.flag} {isIt ? d.nameIt : d.name}</p>
        <p className="text-zinc-300">{isIt ? 'Popolazione' : 'Population'}: {(d.population || d.registered)?.toLocaleString()}</p>
        <p className="text-zinc-300">WGI Governance: <span className={gov.color}>{d.wgi}° {isIt ? 'percentile' : 'percentile'}</span></p>
        {d.gdp && <p className="text-zinc-300">GDP/capita: ${d.gdp.toLocaleString()}</p>}
        {d.type && <p className="text-zinc-400 text-xs mt-1 capitalize">{d.type}</p>}
      </div>
    );
  };

  return (
    <div className="space-y-16">
      {/* HEADER */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-cyan-500/10 rounded-2xl"><Globe className="text-cyan-400" size={28} /></div>
          <div>
            <h2 className="text-3xl font-black text-white">
              <T it="Migrazione & Governance" en="Migration & Governance" />
            </h2>
            <p className="text-zinc-400 text-sm mt-1">
              <T it="Analisi dei flussi migratori e della qualità della governance dei paesi di origine/destinazione" en="Analysis of migration flows and governance quality of origin/destination countries" />
            </p>
          </div>
        </div>
      </motion.div>

      {/* KEY METRICS */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { value: '5.3M', label: isIt ? 'Residenti Stranieri' : 'Foreign Residents', icon: Users, color: 'text-cyan-400', bg: 'bg-cyan-500/10' },
          { value: '6.38M', label: isIt ? 'Italiani all\'Estero (AIRE)' : 'Italians Abroad (AIRE)', icon: ArrowUpRight, color: 'text-amber-400', bg: 'bg-amber-500/10' },
          { value: `${bd.pct_with_degree}%`, label: isIt ? 'Laureati tra emigrati' : 'Graduates among emigrants', icon: GraduationCap, color: 'text-rose-400', bg: 'bg-rose-500/10' },
          { value: '$12.4B', label: isIt ? 'Rimesse in Uscita' : 'Remittance Outflows', icon: DollarSign, color: 'text-indigo-400', bg: 'bg-indigo-500/10' }
        ].map((m, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }}
            className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-5"
          >
            <div className={`${m.bg} w-10 h-10 rounded-xl flex items-center justify-center mb-3`}>
              <m.icon className={m.color} size={20} />
            </div>
            <div className={`text-2xl font-black ${m.color}`}>{m.value}</div>
            <div className="text-xs text-zinc-400 mt-1">{m.label}</div>
          </motion.div>
        ))}
      </div>

      {/* IMMIGRATION CHART */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
      >
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-2">
          <ArrowDownRight className="text-cyan-400" size={22} />
          <T it="Immigrazione in Italia — Top 15 Nazionalità" en="Immigration into Italy — Top 15 Nationalities" />
        </h3>
        <p className="text-zinc-400 text-sm mb-6">
          <T it="Dimensione = popolazione residente. Colore = qualità della governance (WGI World Bank)" en="Size = resident population. Color = governance quality (WGI World Bank)" />
        </p>
        <ResponsiveContainer width="100%" height={420}>
          <BarChart data={immigrationData} layout="vertical" margin={{ left: 80, right: 20, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
            <XAxis type="number" tick={{ fill: '#a1a1aa', fontSize: 12 }} stroke="#3f3f46" tickFormatter={v => `${(v/1000).toFixed(0)}k`} />
            <YAxis type="category" dataKey={isIt ? 'nameIt' : 'name'} tick={{ fill: '#d4d4d8', fontSize: 12 }} stroke="#3f3f46" width={75} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="population" radius={[0, 6, 6, 0]} name={isIt ? 'Residenti' : 'Residents'}>
              {immigrationData.map((entry, i) => {
                let color = '#64748b';
                if (entry.wgi >= 80) color = '#10b981';
                else if (entry.wgi >= 60) color = '#3b82f6';
                else if (entry.wgi >= 40) color = '#f59e0b';
                else if (entry.wgi >= 20) color = '#f97316';
                else color = '#ef4444';
                return <Cell key={i} fill={color} fillOpacity={0.8} />;
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <div className="flex flex-wrap gap-3 mt-4 text-xs">
          {[
            { color: 'bg-emerald-500', label: 'WGI ≥ 80' },
            { color: 'bg-blue-500', label: 'WGI 60-79' },
            { color: 'bg-amber-500', label: 'WGI 40-59' },
            { color: 'bg-orange-500', label: 'WGI 20-39' },
            { color: 'bg-red-500', label: 'WGI < 20' }
          ].map((l, i) => (
            <span key={i} className="flex items-center gap-1.5 text-zinc-400">
              <span className={`w-3 h-3 rounded-sm ${l.color}`} /> {l.label}
            </span>
          ))}
        </div>
      </motion.div>

      {/* EMIGRATION CHART */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
      >
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-2">
          <ArrowUpRight className="text-amber-400" size={22} />
          <T it="Emigrazione dall'Italia — Top 10 Destinazioni (AIRE)" en="Emigration from Italy — Top 10 Destinations (AIRE)" />
        </h3>
        <p className="text-zinc-400 text-sm mb-6">
          <T it="6,38 milioni di italiani registrati all'estero. Badge = qualità governance del paese ospitante" en="6.38 million Italians registered abroad. Badge = host country governance quality" />
        </p>
        <ResponsiveContainer width="100%" height={380}>
          <BarChart data={emigrationData} layout="vertical" margin={{ left: 100, right: 20, top: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
            <XAxis type="number" tick={{ fill: '#a1a1aa', fontSize: 12 }} stroke="#3f3f46" tickFormatter={v => `${(v/1000).toFixed(0)}k`} />
            <YAxis type="category" dataKey={isIt ? 'nameIt' : 'name'} tick={{ fill: '#d4d4d8', fontSize: 12 }} stroke="#3f3f46" width={95} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="registered" radius={[0, 6, 6, 0]} name={isIt ? 'Registrati AIRE' : 'AIRE Registered'}>
              {emigrationData.map((entry, i) => {
                let color = '#64748b';
                if (entry.wgi >= 80) color = '#10b981';
                else if (entry.wgi >= 60) color = '#3b82f6';
                else if (entry.wgi >= 40) color = '#f59e0b';
                else color = '#f97316';
                return <Cell key={i} fill={color} fillOpacity={0.8} />;
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* BRAIN DRAIN */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
      >
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-6">
          <TrendingDown className="text-rose-400" size={22} />
          <T it="Fuga dei Cervelli — Il Deficit di Capitale Umano" en="Brain Drain — The Human Capital Deficit" />
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-4xl font-black text-rose-400">{bd.recent_emigrants_2024.toLocaleString()}</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Emigrati nel 2024" en="Emigrants in 2024" /></div>
          </div>
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-4xl font-black text-amber-400">{bd.pct_with_degree}%</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Con laurea" en="With university degree" /></div>
          </div>
          <div className="bg-black/30 rounded-2xl p-6 text-center border border-zinc-800">
            <div className="text-4xl font-black text-indigo-400">-{bd.net_graduate_loss_2024.toLocaleString()}</div>
            <div className="text-sm text-zinc-400 mt-2"><T it="Perdita netta laureati/anno" en="Net graduate loss/year" /></div>
            <div className="text-xs text-zinc-400 mt-1">
              {bd.graduate_departures_2024.toLocaleString()} {isIt ? 'partenze' : 'departures'} vs {bd.graduate_returns_2024.toLocaleString()} {isIt ? 'rientri' : 'returns'}
            </div>
          </div>
        </div>
        <div className="mt-6 p-4 bg-rose-500/5 border border-rose-500/20 rounded-xl">
          <p className="text-sm text-zinc-300 leading-relaxed">
            <T 
              it="I fattori principali della fuga dei cervelli italiana: salari più bassi della media UE, alta disoccupazione giovanile, e la prevalenza di contratti precari che scoraggiano i giovani laureati dal restare."
              en="The main drivers of Italy's brain drain: lower salaries vs EU average, high youth unemployment, and the prevalence of precarious contracts that discourage young graduates from staying."
            />
          </p>
        </div>
      </motion.div>

      {/* ITALY'S POSITION */}
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
        className="bg-zinc-900/50 border border-zinc-800 rounded-3xl p-8"
      >
        <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-6">
          <ShieldCheck className="text-indigo-400" size={22} />
          <T it="La Posizione dell'Italia nel Mondo" en="Italy's Global Position" />
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-black/30 rounded-2xl p-6 border border-zinc-800">
            <div className="text-xs text-zinc-400 uppercase tracking-wider font-bold mb-2">MIPEX</div>
            <div className="text-3xl font-black text-amber-400">{data.italy_global_position.mipex_score}<span className="text-zinc-400 text-lg">/{data.italy_global_position.mipex_max}</span></div>
            <div className="text-sm text-zinc-400 mt-1">{isIt ? data.italy_global_position.mipex_status_it : data.italy_global_position.mipex_status_en}</div>
          </div>
          <div className="bg-black/30 rounded-2xl p-6 border border-zinc-800">
            <div className="text-xs text-zinc-400 uppercase tracking-wider font-bold mb-2"><T it="Tasso Asilo (1ª istanza)" en="Asylum Rate (1st instance)" /></div>
            <div className="text-3xl font-black text-rose-400">{data.italy_global_position.asylum_acceptance_rate_first_instance}%</div>
            <div className="text-sm text-zinc-400 mt-1"><T it="vs media UE" en="vs EU avg" /> {data.italy_global_position.eu_avg_asylum_acceptance}%</div>
          </div>
          <div className="bg-black/30 rounded-2xl p-6 border border-zinc-800">
            <div className="text-xs text-zinc-400 uppercase tracking-wider font-bold mb-2"><T it="Governance WGI" en="WGI Governance" /></div>
            <div className="text-3xl font-black text-blue-400">{data.italy_global_position.italy_wgi_governance_pctl}°</div>
            <div className="text-sm text-zinc-400 mt-1"><T it="Percentile mondiale" en="World percentile" /></div>
          </div>
        </div>
      </motion.div>

      {/* SOURCE BADGES */}
      <div className="flex flex-wrap gap-3">
        <SourceBadge label="ISTAT Demographics" topicKey="istat_demographics" />
        <SourceBadge label="World Bank WGI" topicKey="worldbank_wgi" />
        <SourceBadge label="AIRE / Migrantes" topicKey="aire_esteri" />
        <SourceBadge label="MIPEX" topicKey="mipex_italy" />
        <SourceBadge label="Eurostat Asylum" topicKey="eurostat_asylum" />
      </div>
    </div>
  );
};

export default MigrationGovernance;
