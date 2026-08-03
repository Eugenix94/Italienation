import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { motion } from 'framer-motion';
import { MapPin, Info, AlertTriangle } from 'lucide-react';
import { T } from './T';
import ediliziaData from '../../public/data/edilizia_scolastica.json';

export default function TerritorialMap() {
  const [geoData, setGeoData] = useState(null);
  const [regionalData, setRegionalData] = useState({});
  const [activeRegion, setActiveRegion] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson').then(r => r.json()),
      fetch(`${import.meta.env.BASE_URL}data/territorial_data.json`).then(r => r.json())
    ])
    .then(([geo, territorial]) => {
      setGeoData(geo);
      setRegionalData(territorial.regionalData);
      setLoading(false);
    })
    .catch(err => {
      console.error("Error loading map data:", err);
      setLoading(false);
    });
  }, []);

  const getRegionStyle = (feature) => {
    // Attempt to match feature name with our dictionary
    const name = feature.properties.reg_name;
    // Handle specific mappings if openpolis names differ
    let dataName = name;
    if (name === "Valle d'Aosta/Vallée d'Aoste") dataName = "Valle d'Aosta";
    if (name === "Trentino-Alto Adige/Südtirol") dataName = "Trentino-Alto Adige";
    
    const regionInfo = regionalData[dataName];
    return {
      fillColor: regionInfo ? regionInfo.color : '#cbd5e1',
      weight: 1,
      opacity: 1,
      color: '#18181b', // zinc-900 borders
      fillOpacity: 0.8
    };
  };

  const onEachRegion = (feature, layer) => {
    const name = feature.properties.reg_name;
    let dataName = name;
    if (name === "Valle d'Aosta/Vallée d'Aoste") dataName = "Valle d'Aosta";
    if (name === "Trentino-Alto Adige/Südtirol") dataName = "Trentino-Alto Adige";
    
    layer.on({
      mouseover: (e) => {
        const layer = e.target;
        layer.setStyle({
          weight: 2,
          color: '#fff',
          fillOpacity: 1
        });
        layer.bringToFront();
        setActiveRegion({ name: dataName, data: regionalData[dataName] });
      },
      mouseout: (e) => {
        const layer = e.target;
        layer.setStyle(getRegionStyle(feature));
        setActiveRegion(null);
      }
    });
  };

  return (
    <div className="w-full max-w-7xl mx-auto py-12 px-4 space-y-8">
      
      {/* Header */}
      <motion.div 
        className="text-center space-y-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <MapPin size={48} className="mx-auto text-indigo-400 mb-4" />
        <h2 className="text-4xl md:text-5xl font-black text-white tracking-tight">
          <T it="Il Divario Territoriale" en="The Territorial Divide" />
        </h2>
        <p className="text-xl text-zinc-400 max-w-3xl mx-auto">
          <T 
            it="La crisi del sistema educativo italiano non è uniforme. Analisi del tasso di abbandono scolastico e del fenomeno NEET per regione." 
            en="The Italian education crisis is not uniform. Analysis of the early school leaving rate and the NEET phenomenon by region." 
          />
        </p>
      </motion.div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pt-8">
        
        {/* Map Container */}
        <motion.div 
          className="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-2xl overflow-hidden h-[600px] shadow-2xl relative"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          {loading ? (
            <div className="flex h-full items-center justify-center text-zinc-500">
              <T it="Caricamento Mappa..." en="Loading Map..." />
            </div>
          ) : (
            <MapContainer 
              center={[41.8719, 12.5674]} 
              zoom={6} 
              scrollWheelZoom={false}
              className="h-full w-full bg-zinc-950"
              zoomControl={false}
            >
              {geoData && (
                <GeoJSON 
                  data={geoData} 
                  style={getRegionStyle}
                  onEachFeature={onEachRegion}
                />
              )}
            </MapContainer>
          )}

          {/* Map Legend Overlay */}
          <div className="absolute bottom-6 left-6 z-[400] bg-zinc-900/90 backdrop-blur border border-zinc-700 p-4 rounded-xl">
            <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2">
              <T it="Abbandono Scolastico" en="School Dropout" />
            </h4>
            <div className="flex items-center gap-1">
              <div className="w-4 h-4 rounded-sm" style={{ backgroundColor: '#fff7ec' }}></div>
              <div className="w-4 h-4 rounded-sm" style={{ backgroundColor: '#fdd49e' }}></div>
              <div className="w-4 h-4 rounded-sm" style={{ backgroundColor: '#fc8d59' }}></div>
              <div className="w-4 h-4 rounded-sm" style={{ backgroundColor: '#e34a33' }}></div>
              <div className="w-4 h-4 rounded-sm" style={{ backgroundColor: '#7f0000' }}></div>
            </div>
            <div className="flex justify-between text-xs text-zinc-500 mt-1">
              <span>8%</span>
              <span>18%+</span>
            </div>
          </div>
        </motion.div>

        {/* Info Panel */}
        <div className="space-y-6">
          <motion.div 
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 h-full flex flex-col"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            {activeRegion ? (
              <div className="space-y-6">
                <h3 className="text-3xl font-bold text-white border-b border-zinc-800 pb-4">
                  {activeRegion.name}
                </h3>
                
                <div className="space-y-4">
                  <div className="bg-zinc-800/50 p-4 rounded-xl border border-zinc-700/50">
                    <div className="text-sm text-zinc-400 mb-1">
                      <T it="Dispersione Scolastica" en="Early School Leaving" />
                    </div>
                    <div className="text-3xl font-bold text-white">
                      {activeRegion.data?.dropout}%
                    </div>
                    {activeRegion.data?.dropout > 13 && (
                      <div className="flex items-center gap-2 mt-2 text-rose-400 text-sm">
                        <AlertTriangle size={14} />
                        <T it="Sopra la media UE" en="Above EU average" />
                      </div>
                    )}
                  </div>

                  <div className="bg-zinc-800/50 p-4 rounded-xl border border-zinc-700/50">
                    <div className="text-sm text-zinc-400 mb-1">
                      <T it="Tasso NEET (15-29 anni)" en="NEET Rate (15-29 yrs)" />
                    </div>
                    <div className="text-3xl font-bold text-white">
                      {activeRegion.data?.neet}%
                    </div>
                  </div>
                </div>

                <div className="pt-4 flex items-start gap-3 text-sm text-zinc-500">
                  <Info size={16} className="mt-0.5 shrink-0" />
                  <p>
                    <T 
                      it="Il divario tra le regioni del Nord e del Sud evidenzia una frattura strutturale nel sistema educativo nazionale, che amplifica le disuguaglianze socio-economiche preesistenti." 
                      en="The gap between Northern and Southern regions highlights a structural fracture in the national education system, amplifying pre-existing socio-economic inequalities." 
                    />
                  </p>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-zinc-500 space-y-4 text-center">
                <MapPin size={48} className="opacity-20" />
                <p className="text-lg">
                  <T it="Passa il mouse su una regione per visualizzare i dati." en="Hover over a region to view the data." />
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
