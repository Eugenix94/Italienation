import React, { useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Map as MapIcon, Layers } from 'lucide-react';
import { T } from './T';
import SourceBadge from './SourceBadge';
import provinceData from '../assets/province_school_counts.json';
import dashboardMetrics from '../assets/dashboard_metrics.json';

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

const macroAreas = [
  { id: 'Nord', name: 'Nord', lat: 45.4, lng: 10.5, color: '#4f46e5' },
  { id: 'Centro', name: 'Centro', lat: 43.0, lng: 12.5, color: '#10b981' },
  { id: 'Sud e Isole', name: 'Sud e Isole', lat: 39.5, lng: 15.0, color: '#f43f5e' }
];

const europeData = [
  { id: 'IT', name: 'Italia', lat: 41.8719, lng: 12.5674, color: '#f43f5e', trackAge: 14, neet: '19.0%', pcto: '0€ (Unpaid)', dropout: '11.5%', type: 'Early Tracking' },
  { id: 'DE', name: 'Germania', lat: 51.1657, lng: 10.4515, color: '#10b981', trackAge: 10, neet: '8.6%', pcto: '€900/mo (Dual)', dropout: '12.2%', type: 'Dual VET' },
  { id: 'FI', name: 'Finlandia', lat: 61.9241, lng: 25.7482, color: '#4f46e5', trackAge: 16, neet: '9.3%', pcto: 'Free Books & Meals', dropout: '7.3%', type: 'Comprehensive' },
  { id: 'FR', name: 'Francia', lat: 46.2276, lng: 2.2137, color: '#f59e0b', trackAge: 15, neet: '11.2%', pcto: 'Alternance', dropout: '7.6%', type: 'Comprehensive' },
  { id: 'SE', name: 'Svezia', lat: 60.1282, lng: 18.6435, color: '#3b82f6', trackAge: 16, neet: '6.1%', pcto: 'Comprehensive', dropout: '8.4%', type: 'Comprehensive' },
  { id: 'ES', name: 'Spagna', lat: 40.4637, lng: -3.7492, color: '#f43f5e', trackAge: 16, neet: '12.7%', pcto: 'Unpaid/Low', dropout: '13.9%', type: 'Comprehensive (Late)' },
  { id: 'PL', name: 'Polonia', lat: 51.9194, lng: 19.1451, color: '#10b981', trackAge: 15, neet: '10.9%', pcto: 'VET Supported', dropout: '4.8%', type: 'Comprehensive' },
  { id: 'NL', name: 'Paesi Bassi', lat: 52.1326, lng: 5.2913, color: '#8b5cf6', trackAge: 12, neet: '4.2%', pcto: 'Paid VET', dropout: '5.3%', type: 'Early Tracking (Fluid)' },
  { id: 'AT', name: 'Austria', lat: 47.5162, lng: 14.5501, color: '#10b981', trackAge: 10, neet: '9.1%', pcto: '€800/mo (Dual)', dropout: '8.1%', type: 'Dual VET' },
  { id: 'GR', name: 'Grecia', lat: 39.0742, lng: 21.8243, color: '#f43f5e', trackAge: 15, neet: '15.4%', pcto: 'Unpaid', dropout: '4.1%', type: 'Comprehensive' }
];

export default function GISMap() {
  const [searchTerm, setSearchTerm] = useState('');
  
  const filteredProvinces = (provinceData || [])
    .filter(p => p && p.name && p.name.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => (a.name || '').localeCompare(b.name || ''));

  const views = [
    { mode: 'provincial', titleIt: 'Vista Provinciale', titleEn: 'Provincial View' },
    { mode: 'macro', titleIt: 'Macro-Aree', titleEn: 'Macro-Areas' },
    { mode: 'europe', titleIt: 'Europa', titleEn: 'Europe' }
  ];

  return (
    <div className="w-full flex flex-col pt-4 space-y-16">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-2">
        <div className="flex items-center gap-3 text-indigo-400">
          <MapIcon size={32} />
          <div>
            <h1 className="text-3xl font-black text-white">
              <T it="Mappa GIS Nazionale" en="National GIS Map" />
            </h1>
            <p className="text-zinc-400 text-sm mt-1">
              <T 
                it="Diseguaglianze territoriali ed esiti formativi. Tutti i dati provengono da ISTAT, INVALSI, MUR ed Eurostat." 
                en="Territorial inequalities and educational outcomes. All data is sourced from ISTAT, INVALSI, MUR and Eurostat." 
              />
            </p>
          </div>
        </div>
      </div>

      {views.map(view => {
        const center = view.mode === 'europe' ? [51.0, 15.0] : [41.8719, 12.5674];
        const zoom = view.mode === 'europe' ? 4 : 6;
        
        return (
          <div key={view.mode} className="flex flex-col space-y-4">
            <h2 className="text-2xl font-bold text-white border-b border-zinc-800 pb-2">
              <T it={view.titleIt} en={view.titleEn} />
            </h2>
            
            <div className="grid lg:grid-cols-4 gap-6">
              {/* Sidebar */}
              <div className="lg:col-span-1 bg-zinc-950/90 backdrop-blur-xl border border-zinc-800 rounded-2xl p-4 shadow-2xl flex flex-col overflow-hidden h-[500px] lg:h-[600px]">
                
                {view.mode === 'provincial' && (
                  <div className="flex flex-col flex-1 overflow-hidden">
                    <div className="mb-4 p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl space-y-3">
                      <p className="text-xs text-indigo-200">
                        <T it="Il monopolio liceale urbano (evidenziato dai pallini rossi) costringe gli studenti periferici a ripiegare su istituti tecnici e professionali. Questa non è una libera scelta, ma una segregazione formativa basata sul CAP di residenza, dove i centri città attraggono risorse pubbliche mentre le periferie assorbono la totalità della dispersione scolastica locale." en="The urban Liceo monopoly (highlighted by red dots) forces peripheral students to fall back on technical and vocational institutes. This is not a free choice, but a zip-code based educational segregation, where city centers attract public resources while suburbs absorb the entirety of local school dropout rates." />
                      </p>
                      <div className="flex justify-end">
                        <SourceBadge agency="ISTAT" topicKey="tracking" year="2023" />
                      </div>
                    </div>
                    <input 
                      type="text"
                      placeholder="Cerca provincia..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full bg-zinc-900 border border-zinc-700 rounded-xl px-4 py-2 text-white mb-4 text-sm focus:outline-none focus:border-indigo-500"
                    />
                    <div className="flex-1 overflow-y-auto custom-scrollbar space-y-2 pr-2">
                      {filteredProvinces.map(p => {
                        const hasMonopoly = p.liceo_count > (p.tecnico_count + p.professionale_count) * 2;
                        return (
                          <div key={p.id} className="w-full text-left p-3 rounded-xl border bg-zinc-900/50 border-zinc-800">
                            <div className="font-bold text-white mb-1 flex justify-between items-center">
                              {p.name}
                              {hasMonopoly && <span className="w-2 h-2 rounded-full bg-rose-500" title="High Liceo Skew"></span>}
                            </div>
                            <div className="text-xs text-zinc-400 flex justify-between mt-2">
                              <span className="text-indigo-400">L: {p.liceo_count}</span>
                              <span className="text-emerald-400">T: {p.tecnico_count}</span>
                              <span className="text-amber-400">P: {p.professionale_count}</span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {view.mode === 'macro' && (
                  <div className="flex flex-col flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
                    <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl space-y-3">
                      <p className="text-xs text-emerald-200">
                        <T it="L'analisi macro-regionale rivela che il divario Nord-Sud non è semplicemente geografico, ma è il risultato di un deficit infrastrutturale cronico. Il Mezzogiorno sconta la mancanza di palestre, mense e tempo pieno, il che si traduce in punteggi INVALSI drammaticamente inferiori. Questa mancanza di supporto si ripercuote direttamente sui tassi di rinuncia universitaria (Dropout), che superano il 20% nei percorsi Professionali del Sud." en="Macro-regional analysis reveals that the North-South divide is not simply geographic, but the result of a chronic infrastructural deficit. The South suffers from a lack of gyms, cafeterias, and full-time schooling, which translates to drastically lower INVALSI scores. This lack of support directly impacts university dropout rates, which exceed 20% in Southern Vocational tracks." />
                      </p>
                      <div className="flex justify-end gap-2 flex-wrap">
                        <SourceBadge agency="INVALSI" topicKey="scores" year="2023" />
                        <SourceBadge agency="MUR" topicKey="dropouts" year="2022" />
                      </div>
                    </div>
                    <h3 className="text-white font-bold mb-2 flex items-center gap-2">
                      <Layers size={18} className="text-indigo-400"/>
                      <T it="Dati Macro-Area" en="Macro-Area Data" />
                    </h3>
                    {dashboardMetrics.invalsi_performance.map(perf => (
                      <div key={perf.region_macro} className="bg-zinc-900 border border-zinc-800 p-4 rounded-xl">
                        <h4 className="font-bold text-white mb-3 text-lg">{perf.region_macro}</h4>
                        
                        <div className="space-y-3">
                          <div>
                            <div className="flex justify-between text-xs mb-1">
                              <span className="text-zinc-400"><T it="Punteggio INVALSI (Matematica Licei)" en="INVALSI Score (Liceo Math)" /></span>
                              <span className="font-bold text-indigo-400">{perf.liceo_math_score}</span>
                            </div>
                            <div className="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                              <div className="bg-indigo-500 h-full" style={{ width: `${(perf.liceo_math_score/250)*100}%` }}></div>
                            </div>
                          </div>
                          
                          <div>
                            <div className="flex justify-between text-xs mb-1">
                              <span className="text-zinc-400"><T it="Punteggio INVALSI (Matematica Professionali)" en="INVALSI Score (Prof. Math)" /></span>
                              <span className="font-bold text-rose-400">{perf.professionale_math_score}</span>
                            </div>
                            <div className="w-full bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                              <div className="bg-rose-500 h-full" style={{ width: `${(perf.professionale_math_score/250)*100}%` }}></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {view.mode === 'europe' && (
                  <div className="flex flex-col flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
                    <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl mb-2 space-y-3">
                      <p className="text-xs text-rose-200">
                        <T it="I dati Eurostat confermano l'eccezione italiana: l'Italia traccia i destini scolastici a soli 14 anni, un unicum in Europa. I sistemi comprensivi nordici (come Svezia e Finlandia) ritardano la scelta a 16 anni, riducendo drasticamente i bias socio-economici e abbattendo la dispersione. Parallelamente, i sistemi duali centro-europei (Germania) offrono salari formativi (circa 900€), mentre l'Italia impone percorsi di PCTO gratuiti e spesso non tutelati. Il risultato matematico di queste anomalie è il triste record europeo italiano di giovani NEET (Not in Education, Employment, or Training)." en="Eurostat data confirms the Italian anomaly: Italy tracks educational destinies at just 14 years old, unique in Europe. Nordic comprehensive systems (like Sweden and Finland) delay the choice to 16, drastically reducing socio-economic bias and cutting dropout rates. Meanwhile, Central European dual systems (Germany) offer training wages (around €900), whereas Italy imposes free, often unprotected PCTO programs. The mathematical result of these structural anomalies is Italy's sad European record for NEETs (Not in Education, Employment, or Training)." />
                      </p>
                      <div className="flex justify-end gap-2 flex-wrap">
                        <SourceBadge agency="Eurostat" topicKey="neet" year="2023" />
                        <SourceBadge agency="Eurydice" topicKey="tracking" year="2022" />
                      </div>
                    </div>
                    {europeData.map(country => (
                      <div key={country.id} className="bg-zinc-900 border border-zinc-800 p-4 rounded-xl">
                        <div className="flex items-center gap-2 mb-3">
                          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: country.color }}></div>
                          <h4 className="font-bold text-white text-lg">{country.name}</h4>
                        </div>
                        
                        <div className="space-y-2 text-xs">
                          <div className="flex justify-between border-b border-zinc-800 pb-1">
                            <span className="text-zinc-400"><T it="Età di Tracking" en="Tracking Age" /></span>
                            <span className="font-bold text-zinc-300">{country.trackAge}</span>
                          </div>
                          <div className="flex justify-between border-b border-zinc-800 pb-1">
                            <span className="text-zinc-400"><T it="Tasso NEET" en="NEET Rate" /></span>
                            <span className="font-bold text-rose-400">{country.neet}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-zinc-400"><T it="Modello Lavoro-Studio" en="Work-Study Model" /></span>
                            <span className="font-bold text-emerald-400">{country.pcto}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Map Container */}
              <div className="lg:col-span-3 bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden relative shadow-2xl h-[500px] lg:h-[600px]">
                <MapContainer center={center} zoom={zoom} scrollWheelZoom={false} className="w-full h-full bg-zinc-900">
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; OpenStreetMap contributors'
                    className="map-tiles"
                  />
                  
                  {view.mode === 'provincial' && provinceData.map(p => {
                    const totalSchools = p.liceo_count + p.tecnico_count + p.professionale_count;
                    const liceoRatio = totalSchools > 0 ? p.liceo_count / totalSchools : 0;
                    const isLiceoDominant = liceoRatio > 0.55;
                    const radius = Math.max(5, Math.min(20, totalSchools / 6));

                    return (
                      <CircleMarker
                        key={p.id}
                        center={[p.lat, p.lng]}
                        radius={radius}
                        pathOptions={{
                          color: isLiceoDominant ? '#f43f5e' : '#6366f1',
                          fillColor: isLiceoDominant ? '#f43f5e' : '#6366f1',
                          fillOpacity: 0.5,
                          weight: 1
                        }}
                      >
                        <Popup className="custom-popup">
                          <div className="bg-white text-gray-900 rounded-lg p-2 min-w-[200px]" style={{ color: '#1a1a2e' }}>
                            <h3 className="font-bold text-gray-900 mb-2 border-b border-gray-200 pb-1 text-sm uppercase">{p.name}</h3>
                            <div className="text-xs space-y-1 text-gray-800">
                              <p><strong>Licei:</strong> {p.liceo_count}</p>
                              <p><strong>Tecnici:</strong> {p.tecnico_count}</p>
                              <p><strong>Professionali:</strong> {p.professionale_count}</p>
                            </div>
                          </div>
                        </Popup>
                      </CircleMarker>
                    );
                  })}

                  {view.mode === 'macro' && macroAreas.map(area => {
                    const dropoutData = dashboardMetrics.university_dropouts_by_macroarea.find(d => d.macroarea === area.id);
                    return (
                      <CircleMarker
                        key={area.id}
                        center={[area.lat, area.lng]}
                        radius={40}
                        pathOptions={{
                          color: area.color,
                          fillColor: area.color,
                          fillOpacity: 0.3,
                          weight: 2
                        }}
                      >
                        <Popup className="custom-popup">
                          <div className="bg-white text-gray-900 rounded-lg p-2 min-w-[200px]" style={{ color: '#1a1a2e' }}>
                            <h3 className="font-bold text-gray-900 mb-2 border-b border-gray-200 pb-1 text-sm uppercase">{area.name}</h3>
                            {dropoutData && (
                              <div className="text-xs space-y-2 mt-2">
                                <p className="text-rose-600 font-bold"><T it="Rinuncia Università:" en="University Dropout:" /> {dropoutData.dropout_pct}%</p>
                                <p className="text-indigo-600 font-bold"><T it="Studenti Fantasma (0 CFU):" en="Ghost Students (0 CFU):" /> {dropoutData.inactive_0cfu_pct}%</p>
                              </div>
                            )}
                          </div>
                        </Popup>
                      </CircleMarker>
                    );
                  })}

                  {view.mode === 'europe' && europeData.map(country => {
                    return (
                      <CircleMarker
                        key={country.id}
                        center={[country.lat, country.lng]}
                        radius={25}
                        pathOptions={{
                          color: country.color,
                          fillColor: country.color,
                          fillOpacity: 0.6,
                          weight: 2
                        }}
                      >
                        <Popup className="custom-popup">
                          <div className="bg-white text-gray-900 rounded-lg p-2 min-w-[200px]" style={{ color: '#1a1a2e' }}>
                            <h3 className="font-bold text-gray-900 mb-2 border-b border-gray-200 pb-1 text-sm uppercase">{country.name}</h3>
                            <div className="text-xs space-y-2 mt-2 text-gray-800">
                              <p><strong>Tracking Age:</strong> {country.trackAge}</p>
                              <p><strong>NEET:</strong> {country.neet}</p>
                              <p><strong>Work-Study:</strong> {country.pcto}</p>
                            </div>
                          </div>
                        </Popup>
                      </CircleMarker>
                    );
                  })}
                </MapContainer>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
