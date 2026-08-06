import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Building2, Search, ShieldCheck, Database, Building, UserCheck, ExternalLink } from 'lucide-react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { T } from './T';
import SourceBadge from './SourceBadge';
import pesData from '../assets/eu27_pes_comparison.json';

import L from 'leaflet';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
});

function MapUpdater({ center, zoom }) {
  const map = useMap();
  React.useEffect(() => {
    map.setView(center, zoom);
  }, [center, zoom, map]);
  return null;
}

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

const getGovernanceDetails = (gov) => {
  if (gov === 'Centralized') return {
    titleIt: "Modello Centralizzato", titleEn: "Centralized Model",
    descIt: "Gestione unificata delle politiche attive a livello nazionale", descEn: "Unified management of active policies at national level"
  };
  if (gov === 'Mixed/Federal') return {
    titleIt: "Modello Misto/Federale", titleEn: "Mixed/Federal Model",
    descIt: "Coordinamento centrale con forte autonomia regionale", descEn: "Central coordination with strong regional autonomy"
  };
  return {
    titleIt: "Modello Frammentato", titleEn: "Fragmented Model",
    descIt: "Gestione divisa con forte autonomia regionale e disparità territoriali", descEn: "Split management with strong regional autonomy and territorial disparities"
  };
};

const getDigitalDetails = (level) => {
  if (level === 'High') return {
    titleIt: "Digital-First", titleEn: "Digital-First",
    descIt: "Piattaforma unica per matching, formazione e sussidi", descEn: "Single platform for matching, training, and benefits"
  };
  if (level === 'Medium') return {
    titleIt: "Sistemi Multipli", titleEn: "Multiple Systems",
    descIt: "Sistemi informativi parzialmente digitalizzati ma limitati", descEn: "Partially digitized but limited IT systems"
  };
  return {
    titleIt: "Bassa Digitalizzazione", titleEn: "Low Digitalization",
    descIt: "Forte dipendenza da processi cartacei e fisici", descEn: "Strong reliance on paper and physical processes"
  };
};

const getActivationDetails = (level) => {
  if (level === 'High') return {
    titleIt: "Attivazione Forte", titleEn: "Strong Activation",
    descIt: "Stretto legame tra sussidi e condizionalità", descEn: "Tight link between benefits and conditionality"
  };
  if (level === 'Medium') return {
    titleIt: "Bassa Attivazione", titleEn: "Low Activation",
    descIt: "Scarsa capacità di matching e condizionalità debole", descEn: "Poor matching capacity and weak conditionality"
  };
  return {
    titleIt: "Senza Attivazione", titleEn: "No Activation",
    descIt: "Sussidi erogati senza reale presa in carico lavorativa", descEn: "Benefits distributed without real job-seeking assistance"
  };
};

const getIntegrationDetails = (level) => {
  if (level === 'Integrated') return {
    titleIt: "One-Stop-Shop", titleEn: "One-Stop-Shop",
    descIt: "Sportello unico per disoccupazione, welfare e orientamento", descEn: "Single front-office for unemployment, welfare, and guidance"
  };
  if (level === 'Coordinated') return {
    titleIt: "Coordinato", titleEn: "Coordinated",
    descIt: "Scambio dati tra enti di welfare e servizi per l'impiego", descEn: "Data exchange between welfare agencies and employment services"
  };
  return {
    titleIt: "Responsabilità Divise", titleEn: "Split Responsibilities",
    descIt: "Gestione divisa tra enti previdenziali (sussidi) e CPI (attivazione)", descEn: "Management split between social security (benefits) and PES (activation)"
  };
};

const DynamicCompareCard = ({ countryData, isItaly }) => {
  const gov = getGovernanceDetails(countryData.governance);
  const digi = getDigitalDetails(countryData.digitalMaturity);
  const act = getActivationDetails(countryData.activationIntensity);
  const int = getIntegrationDetails(countryData.benefitsIntegration);

  const baseColor = isItaly ? 'rose' : 'emerald';

  return (
    <motion.div 
      initial={{ opacity: 0, x: isItaly ? 20 : -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.4 }}
      className={`bg-zinc-900/40 border border-${baseColor}-500/20 rounded-xl p-6 relative overflow-hidden group`}
    >
      <div className="absolute top-0 right-0 p-4 opacity-10 transform translate-x-4 -translate-y-4 group-hover:scale-110 transition-transform">
        {isItaly ? <Building2 className="w-32 h-32 text-rose-500" /> : <ShieldCheck className="w-32 h-32 text-emerald-500" />}
      </div>
      
      <div className="flex items-center gap-3 mb-6 relative z-10">
        <span className="text-3xl">{countryData.flag}</span>
        <div>
          <h4 className="text-xl font-bold text-white">{countryData.country} {countryData.pesName}</h4>
          <p className={`text-${baseColor}-400 text-sm`}><T it={gov.titleIt} en={gov.titleEn} /></p>
        </div>
      </div>

      <ul className="space-y-4 relative z-10">
        <li className="flex gap-3">
          <Database className={`w-5 h-5 text-${baseColor}-400 shrink-0 mt-0.5`} />
          <div>
            <p className="font-semibold text-zinc-200"><T it={digi.titleIt} en={digi.titleEn} /></p>
            <p className="text-sm text-zinc-400"><T it={digi.descIt} en={digi.descEn} /></p>
          </div>
        </li>
        <li className="flex gap-3">
          <Building className={`w-5 h-5 text-${baseColor}-400 shrink-0 mt-0.5`} />
          <div>
            <p className="font-semibold text-zinc-200"><T it={int.titleIt} en={int.titleEn} /></p>
            <p className="text-sm text-zinc-400"><T it={int.descIt} en={int.descEn} /></p>
          </div>
        </li>
        <li className="flex gap-3">
          <UserCheck className={`w-5 h-5 text-${baseColor}-400 shrink-0 mt-0.5`} />
          <div>
            <p className="font-semibold text-zinc-200"><T it={act.titleIt} en={act.titleEn} /></p>
            <p className="text-sm text-zinc-400"><T it={act.descIt} en={act.descEn} /></p>
          </div>
        </li>
      </ul>

      {countryData.url && (
        <a 
          href={countryData.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className={`mt-6 flex items-center justify-center gap-2 w-full py-2.5 rounded-lg border border-${baseColor}-500/30 text-${baseColor}-400 hover:bg-${baseColor}-500/10 transition-colors text-sm font-bold`}
        >
          <ExternalLink className="w-4 h-4" />
          <T it="Visita il Sito Ufficiale" en="Visit Official Site" />
        </a>
      )}
    </motion.div>
  );
};

export default function EU27PESComparison() {
  const [filterGov, setFilterGov] = useState('All');
  const [compareCountry, setCompareCountry] = useState('Malta');

  const filteredData = filterGov === 'All' 
    ? pesData 
    : pesData.filter(d => d.governance === filterGov);

  const italyData = pesData.find(d => d.country === 'Italy');
  const compareData = pesData.find(d => d.country === compareCountry);

  const euCountries = pesData.filter(d => d.country !== 'Italy');

  return (
    <section className="w-full py-16 bg-zinc-950 text-white border-t border-zinc-800 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/10 via-zinc-950 to-zinc-950 pointer-events-none" />
      
      <div className="max-w-7xl mx-auto px-4 relative z-10">
        <div className="mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 flex items-center gap-3">
            <Building2 className="w-8 h-8 text-indigo-400" />
            <T it="Servizi Pubblici per l'Impiego EU27" en="EU27 Public Employment Services" />
          </h2>
          <p className="text-zinc-400 max-w-3xl text-lg mb-4">
            <T 
              it="Un'analisi comparativa dei 27 servizi pubblici per l'impiego europei. Seleziona un paese per confrontarne il modello di governance e le performance digitali con il frammentato sistema italiano." 
              en="A comparative analysis of the 27 European public employment services. Select a country to compare its governance model and digital performance against the fragmented Italian system." 
            />
          </p>
          <a 
            href="https://employment-social-affairs.ec.europa.eu/policies-and-activities/coordination-employment-and-social-policies/european-network-public-employment-services-pes-network_en" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-indigo-400 hover:text-indigo-300 font-semibold"
          >
            <ExternalLink className="w-4 h-4" />
            <T it="Rete Europea dei PES (Fonte Ufficiale EC)" en="European PES Network (Official EC Source)" />
          </a>
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

        {/* Map Visualization */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden shadow-2xl h-[400px] mb-8 relative z-0">
          <MapContainer center={[50.0, 15.0]} zoom={4} scrollWheelZoom={false} className="w-full h-full bg-zinc-900 z-0">
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; OpenStreetMap contributors &copy; CARTO'
            />
            {filteredData.map(country => {
              // Determine color based on Digital Maturity for visual distinction
              let color = '#3b82f6'; // default blue
              if (country.digitalMaturity === 'High') color = '#10b981'; // emerald
              if (country.digitalMaturity === 'Medium') color = '#f59e0b'; // amber
              if (country.digitalMaturity === 'Low') color = '#f43f5e'; // rose
              if (country.country === 'Italy') color = '#f43f5e';

              return (
                <CircleMarker
                  key={country.country}
                  center={[country.lat, country.lng]}
                  radius={country.country === compareCountry ? 12 : 8}
                  pathOptions={{
                    color: country.country === compareCountry ? '#fff' : color,
                    fillColor: color,
                    fillOpacity: country.country === compareCountry ? 0.9 : 0.6,
                    weight: country.country === compareCountry ? 3 : 1
                  }}
                  eventHandlers={{
                    click: () => {
                      if(country.country !== 'Italy') setCompareCountry(country.country);
                    },
                  }}
                >
                  <Popup className="custom-popup">
                    <div className="p-2 min-w-[200px]">
                      <h3 className="font-bold text-gray-900 mb-2 border-b pb-1 text-sm flex justify-between">
                        <span>{country.flag} {country.country}</span>
                        <span className="text-xs font-normal text-gray-500">{country.pesName}</span>
                      </h3>
                      <div className="text-xs space-y-1 mt-2 text-gray-800">
                        <p><strong>Gov:</strong> {country.governance}</p>
                        <p><strong>Digital:</strong> {country.digitalMaturity}</p>
                        <p><strong>Integration:</strong> {country.benefitsIntegration}</p>
                      </div>
                    </div>
                  </Popup>
                </CircleMarker>
              );
            })}
          </MapContainer>
        </div>

        {/* Table */}
        <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl overflow-hidden mb-16 backdrop-blur-sm">
          <div className="overflow-x-auto overflow-y-auto max-h-[500px] custom-scrollbar">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-zinc-900/90 text-zinc-300 border-b border-zinc-800 uppercase text-xs font-semibold sticky top-0 z-10 backdrop-blur-md shadow-sm">
                <tr>
                  <th className="px-6 py-4"><T it="Paese" en="Country" /></th>
                  <th className="px-6 py-4"><T it="Nome PES" en="PES Name" /></th>
                  <th className="px-6 py-4"><T it="Link" en="Link" /></th>
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
                  const isSelected = row.country === compareCountry;
                  
                  let rowClasses = "hover:bg-zinc-800/30 transition-colors";
                  if (isItaly) rowClasses = "bg-rose-500/5 hover:bg-rose-500/10 relative";
                  if (isSelected) rowClasses = "bg-emerald-500/5 hover:bg-emerald-500/10 relative";

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
                        {isSelected && <div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-500" />}
                        <span className="text-xl">{row.flag}</span>
                        <T it={row.country === 'Italy' ? 'Italia' : row.country === 'Spain' ? 'Spagna' : row.country === 'France' ? 'Francia' : row.country === 'Germany' ? 'Germania' : row.country} en={row.country} />
                      </td>
                      <td className="px-6 py-4 text-zinc-300">{row.pesName}</td>
                      <td className="px-6 py-4">
                        {row.url && (
                          <a href={row.url} target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300" title={`Visita ${row.pesName}`}>
                             <ExternalLink className="w-4 h-4" />
                          </a>
                        )}
                      </td>
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

        {/* Deep Dive Dynamic vs Italy */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
          <h3 className="text-2xl font-bold flex items-center gap-3">
            <T it="Confronto Diretto" en="Direct Comparison" />
          </h3>
          <div className="flex items-center gap-3 bg-zinc-900/80 backdrop-blur border border-emerald-500/20 p-2 px-4 rounded-xl shadow-lg">
            <span className="text-sm text-zinc-400 font-semibold uppercase tracking-wider"><T it="Confronta con:" en="Compare with:" /></span>
            <select 
              className="bg-transparent border-none text-emerald-400 font-bold focus:ring-0 outline-none cursor-pointer"
              value={compareCountry}
              onChange={(e) => setCompareCountry(e.target.value)}
            >
              {euCountries.map(c => (
                <option key={c.country} value={c.country} className="bg-zinc-900 text-white">
                  {c.flag} {c.country}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        <div className="grid md:grid-cols-2 gap-8">
          <AnimatePresence mode="wait">
            {compareData && (
              <DynamicCompareCard key={compareData.country} countryData={compareData} isItaly={false} />
            )}
          </AnimatePresence>
          <DynamicCompareCard countryData={italyData} isItaly={true} />
        </div>

      </div>
    </section>
  );
}
