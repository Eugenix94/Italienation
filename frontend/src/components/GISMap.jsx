import React, { useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
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

export default function GISMap() {
  const [viewMode, setViewMode] = useState('provincial'); // 'provincial' | 'macro'
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
        </div>
      </div>

      <div className="flex-1 grid lg:grid-cols-4 gap-6">
        
        {/* Sidebar */}
        <div className="lg:col-span-1 bg-zinc-950/90 backdrop-blur-xl border border-zinc-800 rounded-2xl p-4 shadow-2xl flex flex-col overflow-hidden h-[500px] lg:h-[600px]">
          
          {viewMode === 'provincial' ? (
            <div className="flex flex-col flex-1 overflow-hidden">
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
          ) : (
            <div className="flex flex-col flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
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
        </div>

        {/* Map Container */}
        <div className="lg:col-span-3 bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden relative shadow-2xl h-[500px] lg:h-[600px]">
          <MapContainer center={[41.8719, 12.5674]} zoom={6} scrollWheelZoom={false} className="w-full h-full bg-zinc-900">
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; OpenStreetMap contributors &copy; CARTO'
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
          </MapContainer>
        </div>
      </div>
    </div>
  );
}
