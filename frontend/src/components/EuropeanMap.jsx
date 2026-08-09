import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';

export default function EuropeanMap() {
  const [geoData, setGeoData] = useState(null);
  const { lang } = useLanguage();

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}europe.geo.json`)
      .then((res) => res.json())
      .then((data) => setGeoData(data))
      .catch((err) => console.error("Could not load map data", err));
  }, []);

  const retentionCountries = ['ITA', 'FRA', 'ESP', 'DEU', 'BEL', 'NLD', 'PRT', 'CHE', 'AUT', 'GRC'];
  const progressiveCountries = ['GBR', 'NOR', 'SWE', 'FIN', 'DNK', 'ISL', 'EST'];

  const getStyle = (feature) => {
    const iso = feature.properties.ISO3;
    if (retentionCountries.includes(iso)) {
      return { fillColor: '#f43f5e', weight: 1, opacity: 1, color: 'white', fillOpacity: 0.7 }; // Rose (Retention)
    }
    if (progressiveCountries.includes(iso)) {
      return { fillColor: '#10b981', weight: 1, opacity: 1, color: 'white', fillOpacity: 0.7 }; // Emerald (Progressive)
    }
    return { fillColor: '#3f3f46', weight: 1, opacity: 1, color: '#52525b', fillOpacity: 0.4 }; // Zinc (Other)
  };

  const onEachFeature = (feature, layer) => {
    const iso = feature.properties.ISO3;
    const name = feature.properties.NAME;
    
    let popupContent = `<b>${name}</b><br/>`;
    
    if (retentionCountries.includes(iso)) {
      popupContent += lang === 'it' 
        ? `<span style="color: #e11d48; font-weight: bold;">Bocciatura / Early Tracking</span><br/>Bassa Mobilità Sociale`
        : `<span style="color: #e11d48; font-weight: bold;">Grade Retention / Early Tracking</span><br/>Low Social Mobility`;
    } else if (progressiveCountries.includes(iso)) {
      popupContent += lang === 'it'
        ? `<span style="color: #059669; font-weight: bold;">Progressione Automatica / Comprensivo</span><br/>Alta Mobilità Sociale`
        : `<span style="color: #059669; font-weight: bold;">Automatic Progression / Comprehensive</span><br/>High Social Mobility`;
    } else {
      popupContent += lang === 'it' ? `Dati misti / non classificato` : `Mixed data / Unclassified`;
    }

    layer.bindPopup(popupContent);
  };

  if (!geoData) {
    return <div className="h-[500px] w-full flex items-center justify-center bg-zinc-900 rounded-2xl animate-pulse text-zinc-500">Loading Map...</div>;
  }

  return (
    <div className="w-full mb-12 flex flex-col gap-4">
      <div className="text-center">
        <h3 className="text-2xl font-bold text-white mb-2">
          <T it="Mappa Europea: Bocciatura e Modelli Scolastici" en="European Map: Grade Retention & School Models" />
        </h3>
        <p className="text-zinc-400 max-w-2xl mx-auto text-sm">
          <T 
            it="I paesi del Nord Europa hanno abolito la bocciatura (Progressione Automatica) per favorire la mobilità sociale. I paesi mediterranei mantengono modelli punitivi." 
            en="Northern European countries abolished grade retention (Automatic Progression) to boost social mobility. Mediterranean countries maintain punitive models." 
          />
        </p>
      </div>
      
      <div className="relative h-[500px] w-full rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
        <MapContainer 
          center={[52.0, 10.0]} 
          zoom={4} 
          scrollWheelZoom={false} 
          style={{ height: '100%', width: '100%', background: '#18181b' }}
        >
          <GeoJSON 
            data={geoData} 
            style={getStyle} 
            onEachFeature={onEachFeature} 
          />
        </MapContainer>
        
        {/* Legend */}
        <div className="absolute bottom-4 left-4 z-[400] bg-zinc-900/90 backdrop-blur-md p-4 rounded-xl border border-white/10 text-xs text-white">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-4 h-4 rounded-full bg-rose-500"></div>
            <span><T it="Bocciatura (Bassa Mobilità)" en="Grade Retention (Low Mobility)" /></span>
          </div>
          <div className="flex items-center gap-2 mb-2">
            <div className="w-4 h-4 rounded-full bg-emerald-500"></div>
            <span><T it="Progressione (Alta Mobilità)" en="Progression (High Mobility)" /></span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-zinc-600"></div>
            <span><T it="Altro / Non classificato" en="Other / Unclassified" /></span>
          </div>
        </div>
      </div>
    </div>
  );
}
