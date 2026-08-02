import React, { useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Map as MapIcon, Layers } from 'lucide-react';
import { T } from './T';
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
  { id: 'IT', name: 'Italia', lat: 41.8719, lng: 12.5674, color: '#f43f5e', trackAge: 14, neet: '19.0%', pcto: '0€ (Unpaid)' },
  { id: 'DE', name: 'Germania', lat: 51.1657, lng: 10.4515, color: '#10b981', trackAge: 10, neet: '8.6%', pcto: '€900/mo (Dual)' },
  { id: 'FI', name: 'Finlandia', lat: 61.9241, lng: 25.7482, color: '#4f46e5', trackAge: 16, neet: '9.3%', pcto: 'Free Books & Meals' },
  { id: 'FR', name: 'Francia', lat: 46.2276, lng: 2.2137, color: '#f59e0b', trackAge: 15, neet: '11.2%', pcto: 'Alternance' },
  { id: 'SE', name: 'Svezia', lat: 60.1282, lng: 18.6435, color: '#3b82f6', trackAge: 16, neet: '6.1%', pcto: 'Comprehensive' }
];

function MapUpdater({ center, zoom }) {
  const map = useMap();
  React.useEffect(() => {
    map.setView(center, zoom);
  }, [center, zoom, map]);
  return null;
}

export default function GISMap() {
  const [viewMode, setViewMode] = useState('provincial'); // 'provincial' | 'macro' | 'europe'
  const [searchTerm, setSearchTerm] = useState('');
  
  const filteredProvinces = (provinceData || [])
    .filter(p => p && p.name && p.name.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => (a.name || '').localeCompare(b.name || ''));

  return (
    <div className="w-full h-full flex flex-col pt-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-3 text-indigo-400">
          <MapIcon size={32} />
          <div>
            <h1 className="text-3xl font-black text-white">
              <T it="Mappa GIS Nazionale" en="National GIS Map" />
            </h1>
            <p className="text-zinc-400 text-sm mt-1">
              <T 
                it="Diseguaglianze territoriali ed esiti formativi." 
                en="Territorial inequalities and educational outcomes." 
              />
            </p>
          </div>
        </div>
        
        {/* View Mode Toggle */}
        <div className="flex bg-zinc-900 border border-zinc-800 rounded-lg p-1">
          <button 
            onClick={() => setViewMode('provincial')}
            className={`px-4 py-2 text-sm font-bold rounded-md transition-all ${
              viewMode === 'provincial' ? 'bg-indigo-600 text-white shadow-lg' : 'text-zinc-400 hover:text-white'
            }`}
          >
            <T it="Vista Provinciale" en="Provincial View" />
          </button>
          <button 
            onClick={() => setViewMode('macro')}
            className={`px-4 py-2 text-sm font-bold rounded-md transition-all ${
              viewMode === 'macro' ? 'bg-indigo-600 text-white shadow-lg' : 'text-zinc-400 hover:text-white'
            }`}
          >
            <T it="Macro-Aree" en="Macro-Areas" />
          </button>
          <button 
            onClick={() => setViewMode('europe')}
            className={`px-4 py-2 text-sm font-bold rounded-md transition-all ${
              viewMode === 'europe' ? 'bg-indigo-600 text-white shadow-lg' : 'text-zinc-400 hover:text-white'
            }`}
          >
            <T it="Europa" en="Europe" />
          </button>
        </div>
      </div>

      <div className="flex-1 grid lg:grid-cols-4 gap-6">
        
        {/* Sidebar */}
        <div className="lg:col-span-1 bg-zinc-950/90 backdrop-blur-xl border border-zinc-800 rounded-2xl p-4 shadow-2xl flex flex-col overflow-hidden h-[500px] lg:h-[600px]">
          
          {viewMode === 'provincial' && (
            <div className="flex flex-col flex-1 overflow-hidden">
              <div className="mb-4 p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
                <p className="text-xs text-indigo-200">
                  <T it="Il monopolio liceale urbano (pallini rossi) spinge gli studenti periferici verso istituti tecnici, creando una segregazione formativa basata sul CAP. I centri città attraggono risorse, le periferie assorbono la dispersione." en="The urban Liceo monopoly (red dots) pushes peripheral students toward technical institutes, creating zip-code based educational segregation. City centers attract resources, suburbs absorb dropout rates." />
                </p>
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
                      <div className="text-xs text-zinc-500 flex justify-between mt-2">
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

          {viewMode === 'macro' && (
            <div className="flex flex-col flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
                <p className="text-xs text-emerald-200">
                  <T it="Il divario Nord-Sud non è solo geografico, ma strutturale. Il Mezzogiorno sconta carenze infrastrutturali gravissime (palestre, mense, tempo pieno), traducendosi in punteggi INVALSI drammaticamente inferiori e tassi di rinuncia universitaria che superano il 20% nei Professionali." en="The North-South divide is structural, not just geographic. The South suffers from severe infrastructure deficits (gyms, cafeterias, full-time school), translating to drastically lower INVALSI scores and university dropout rates exceeding 20% in Vocational tracks." />
                </p>
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

          {viewMode === 'europe' && (
            <div className="flex flex-col flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
               <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl mb-2">
                <p className="text-xs text-rose-200">
                  <T it="L'Italia traccia i destini a soli 14 anni. Sistemi comprensivi (Svezia, Finlandia) ritardano la scelta a 16 anni, azzerando i bias socio-economici. I sistemi duali (Germania) offrono salari formativi (900€), mentre l'Italia impone PCTO gratuiti e pericolosi. Risultato? Record EU di NEET." en="Italy tracks destinies at just 14. Comprehensive systems (Sweden, Finland) delay the choice to 16, nullifying socio-economic bias. Dual systems (Germany) offer training wages (€900), while Italy imposes free, dangerous PCTO labor. Result? EU record for NEETs." />
                </p>
              </div>
              {europeData.map(country => (
                <div key={country.id} className="bg-zinc-900 border border-zinc-800 p-4 rounded-xl">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: country.color }}></div>
                    <h4 className="font-bold text-white text-lg">{country.name}</h4>
                  </div>
                  
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between border-b border-zinc-800 pb-1">
                      <span className="text-zinc-500"><T it="Età di Tracking" en="Tracking Age" /></span>
                      <span className="font-bold text-zinc-300">{country.trackAge}</span>
                    </div>
                    <div className="flex justify-between border-b border-zinc-800 pb-1">
                      <span className="text-zinc-500"><T it="Tasso NEET" en="NEET Rate" /></span>
                      <span className="font-bold text-rose-400">{country.neet}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-zinc-500"><T it="Modello Lavoro-Studio" en="Work-Study Model" /></span>
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
          <MapContainer center={[41.8719, 12.5674]} zoom={6} scrollWheelZoom={false} className="w-full h-full bg-zinc-900">
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; OpenStreetMap contributors &copy; CARTO'
            />
            <MapUpdater 
              center={viewMode === 'europe' ? [51.0, 15.0] : [41.8719, 12.5674]} 
              zoom={viewMode === 'europe' ? 4 : 6} 
            />
            
            {viewMode === 'provincial' && provinceData.map(p => {
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
                    <div className="p-1 min-w-[200px]">
                      <h3 className="font-bold text-gray-900 mb-2 border-b pb-1 text-sm uppercase">{p.name}</h3>
                      <div className="text-xs space-y-1">
                        <p><strong>Licei:</strong> {p.liceo_count}</p>
                        <p><strong>Tecnici:</strong> {p.tecnico_count}</p>
                        <p><strong>Professionali:</strong> {p.professionale_count}</p>
                      </div>
                    </div>
                  </Popup>
                </CircleMarker>
              );
            })}

            {viewMode === 'macro' && macroAreas.map(area => {
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
                    <div className="p-2 min-w-[200px]">
                      <h3 className="font-bold text-gray-900 mb-2 border-b pb-1 text-sm uppercase">{area.name}</h3>
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

            {viewMode === 'europe' && europeData.map(country => {
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
                    <div className="p-2 min-w-[200px]">
                      <h3 className="font-bold text-gray-900 mb-2 border-b pb-1 text-sm uppercase">{country.name}</h3>
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
}
