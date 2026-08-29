import React, { useState, useEffect, useRef, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Database, Table, BarChart2, ExternalLink, Download, ArrowDown, Sparkles, Layers, Info, Filter, Loader2, ChevronDown } from 'lucide-react';
import originLinks from '../assets/originLinks.json';
import { T } from './T';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function ScrollyDataHub() {
  const [masterData, setMasterData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [activeDataset, setActiveDataset] = useState(null);
  const [viewMode, setViewMode] = useState('chart'); // 'chart' or 'table'
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [displayRowsCount, setDisplayRowsCount] = useState(50);

  // References for scroll observation
  const cardRefs = useRef({});

  // Asynchronously fetch master_data_observatory.json from public directory
  useEffect(() => {
    let isMounted = true;
    
    // Determine public data path accommodating Vite base path
    const dataUrl = import.meta.env.BASE_URL 
      ? `${import.meta.env.BASE_URL.replace(/\/$/, '')}/data/master_data_observatory.json`
      : './data/master_data_observatory.json';

    fetch(dataUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (isMounted) {
          setMasterData(data);
          setLoading(false);
          // Set initial active dataset
          const firstCat = Object.values(data)[0];
          if (firstCat && firstCat.length > 0) {
            setActiveDataset(firstCat[0]);
          }
        }
      })
      .catch((err) => {
        console.error("Failed to load observatory datasets:", err);
        // Fallback retry with relative path
        fetch('./data/master_data_observatory.json')
          .then(r => r.json())
          .then(data => {
            if (isMounted) {
              setMasterData(data);
              setLoading(false);
              const firstCat = Object.values(data)[0];
              if (firstCat && firstCat.length > 0) setActiveDataset(firstCat[0]);
            }
          })
          .catch(e => {
            if (isMounted) {
              setError("Impossibile caricare il database degli osservatori. Riprova più tardi.");
              setLoading(false);
            }
          });
      });

    return () => { isMounted = false; };
  }, []);

  // Format dataset groups
  const masterCategories = useMemo(() => {
    if (!masterData) return [];
    return Object.entries(masterData).map(([cat, datasets]) => ({
      category: cat,
      datasets: datasets.map(d => ({ ...d, category: cat }))
    }));
  }, [masterData]);

  const allObservatoryDatasets = useMemo(() => {
    return masterCategories.flatMap(c => c.datasets);
  }, [masterCategories]);

  // Setup Intersection Observer for automatic scroll detection
  useEffect(() => {
    if (allObservatoryDatasets.length === 0) return;

    const observerOptions = {
      root: null,
      rootMargin: '-30% 0px -40% 0px',
      threshold: 0.25
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const datasetId = entry.target.getAttribute('data-dataset-id');
          const found = allObservatoryDatasets.find(d => d.id === datasetId);
          if (found) {
            setActiveDataset(found);
            setDisplayRowsCount(50); // Reset pagination on dataset switch
          }
        }
      });
    }, observerOptions);

    Object.values(cardRefs.current).forEach((el) => {
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [allObservatoryDatasets]);

  // Filter datasets
  const filteredCategories = useMemo(() => {
    return masterCategories.map(cat => ({
      ...cat,
      datasets: cat.datasets.filter(d => 
        (selectedCategory === 'ALL' || d.category === selectedCategory) &&
        (d.id.toLowerCase().includes(searchTerm.toLowerCase()) || 
         d.filename.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    })).filter(cat => cat.datasets.length > 0);
  }, [masterCategories, selectedCategory, searchTerm]);

  // Chart Renderer
  const renderChart = (dataset) => {
    if (!dataset || !dataset.data || dataset.data.length === 0) return null;

    const chartData = dataset.data.slice(0, 25);
    const keys = dataset.columns.slice(1, 4);
    const xKey = dataset.columns[0];
    const colors = ['#6366f1', '#10b981', '#f43f5e', '#f59e0b', '#ec4899'];

    const isMobile = typeof window !== 'undefined' && window.innerWidth < 640;

    return (
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 20, right: 20, left: 10, bottom: 65 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
          <XAxis 
            dataKey={xKey} 
            stroke="#71717a" 
            tick={{ fill: '#a1a1aa', fontSize: isMobile ? 8 : 10 }}
            angle={-35}
            textAnchor="end"
            interval={0}
          />
          <YAxis stroke="#71717a" tick={{ fill: '#a1a1aa', fontSize: 10 }} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '12px', boxShadow: '0 10px 25px rgba(0,0,0,0.5)' }}
            itemStyle={{ color: '#ffffff', fontWeight: 'bold' }}
            labelStyle={{ color: '#ffffff' }}
          />
          {keys.map((key, i) => (
            <Bar key={key} dataKey={key} fill={colors[i % colors.length]} radius={[6, 6, 0, 0]} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    );
  };

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center text-zinc-400 gap-4">
        <Loader2 className="animate-spin text-indigo-500" size={48} />
        <p className="text-sm font-medium">Caricamento del database open data in corso...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center text-rose-400 gap-4 text-center px-4">
        <Database size={48} />
        <h2 className="text-xl font-bold text-white">Errore di Caricamento</h2>
        <p className="text-sm text-zinc-400 max-w-md">{error}</p>
        <button onClick={() => window.location.reload()} className="px-6 py-2 bg-indigo-600 text-white rounded-xl font-bold text-xs hover:bg-indigo-500 transition">
          Ricarica Pagina
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#050510] text-white">
      
      {/* Hero Banner */}
      <div className="max-w-7xl mx-auto px-4 pt-10 pb-6">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-zinc-800/80 pb-6">
          <div>
            <div className="flex items-center gap-2 text-indigo-400 font-bold uppercase tracking-widest text-xs mb-2">
              <Sparkles size={16} />
              <T it="Esplorazione Scrollytelling Unificata" en="Unified Scrollytelling Exploration" />
            </div>
            <h1 className="text-3xl md:text-5xl font-black tracking-tight text-white mb-2">
              <T it="Hub Dati & Osservatorio" en="Data Hub & Observatory" />
            </h1>
            <p className="text-zinc-400 max-w-2xl text-sm leading-relaxed">
              <T 
                it="Scorri la pagina per esplorare la matrice dei dati ufficiali. Il pannello grafico a destra rimarrà agganciato e aggiornerà automaticamente la visualizzazione ad ogni passo." 
                en="Scroll down the page to explore the official dataset matrix. The interactive chart on the right will stay pinned and automatically update with each step." 
              />
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs text-zinc-400 bg-zinc-900/80 px-4 py-2.5 rounded-2xl border border-zinc-800/80">
            <ArrowDown className="animate-bounce text-indigo-400" size={16} />
            <span><T it="Scorri per navigare" en="Scroll down to navigate" /></span>
          </div>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center justify-between gap-4 mt-6">
          <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
            <button 
              onClick={() => setSelectedCategory('ALL')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${selectedCategory === 'ALL' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20' : 'bg-zinc-900/80 text-zinc-400 hover:bg-zinc-800'}`}
            >
              Tutti i Moduli ({allObservatoryDatasets.length})
            </button>
            {masterCategories.map(cat => (
              <button 
                key={cat.category}
                onClick={() => setSelectedCategory(cat.category)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${selectedCategory === cat.category ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20' : 'bg-zinc-900/80 text-zinc-400 hover:bg-zinc-800'}`}
              >
                {cat.category} ({cat.datasets.length})
              </button>
            ))}
          </div>

          <div className="relative min-w-[220px]">
            <input 
              type="text"
              placeholder="Filtra dataset..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-zinc-900/80 border border-zinc-800 rounded-xl px-4 py-1.5 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
            />
          </div>
        </div>
      </div>

      {/* Main Scrollytelling Split Grid */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: Bounded Scrolling Steps */}
          <div className="lg:col-span-6 space-y-12 pb-32 order-2 lg:order-1 h-[500px] lg:h-[calc(100vh-160px)] overflow-y-auto custom-scrollbar pr-4">
            {filteredCategories.map((catGroup) => (
              <div key={catGroup.category} className="space-y-6">
                <div className="sticky top-0 z-10 bg-[#050510]/95 backdrop-blur-md py-2 border-b border-zinc-800/80">
                  <span className="text-xs font-bold uppercase tracking-widest text-indigo-400 bg-indigo-950/60 px-3 py-1 rounded-full border border-indigo-800/40">
                    {catGroup.category}
                  </span>
                </div>

                <div className="space-y-6">
                  {catGroup.datasets.map((ds) => {
                    const isActive = activeDataset?.id === ds.id;

                    return (
                      <div 
                        key={ds.id}
                        data-dataset-id={ds.id}
                        ref={(el) => (cardRefs.current[ds.id] = el)}
                        onClick={() => {
                          setActiveDataset(ds);
                          setDisplayRowsCount(50);
                        }}
                        className={`cursor-pointer rounded-3xl p-6 border transition-all duration-300 ${
                          isActive 
                            ? 'bg-zinc-900/90 border-indigo-500/80 shadow-[0_0_35px_rgba(99,102,241,0.15)] ring-1 ring-indigo-500/50' 
                            : 'bg-zinc-950/60 border-zinc-800/80 hover:border-zinc-700 hover:bg-zinc-900/40'
                        }`}
                      >
                        <div className="flex justify-between items-start mb-3">
                          <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-400 bg-zinc-900 px-2.5 py-0.5 rounded-md border border-zinc-800">
                            {ds.id}
                          </span>
                          <span className="text-xs font-bold text-emerald-400 bg-emerald-950/40 px-2.5 py-0.5 rounded-full border border-emerald-800/30">
                            {ds.data.length} righe • {ds.columns.length} colonne
                          </span>
                        </div>

                        <h3 className={`text-lg font-bold mb-2 capitalize leading-snug ${isActive ? 'text-white' : 'text-zinc-300'}`}>
                          {ds.id.replace(/_/g, ' ')}
                        </h3>

                        <p className="text-xs text-zinc-400 mb-4 leading-relaxed font-mono truncate">
                          File: <span className="text-indigo-300">{ds.filename}</span>
                        </p>

                        {/* Column Badges */}
                        <div className="flex flex-wrap gap-1.5">
                          {ds.columns.slice(0, 4).map((col, cidx) => (
                            <span key={cidx} className="text-[10px] text-zinc-400 bg-zinc-900/80 px-2 py-0.5 rounded border border-zinc-800">
                              {col}
                            </span>
                          ))}
                          {ds.columns.length > 4 && (
                            <span className="text-[10px] text-zinc-400 px-1">
                              +{ds.columns.length - 4} altri
                            </span>
                          )}
                        </div>

                        <div className="mt-4 pt-3 border-t border-zinc-800/60 flex flex-col gap-3">
                          <div className="flex items-center justify-between text-xs font-bold">
                            <span className={isActive ? 'text-indigo-400' : 'text-zinc-400'}>
                              {isActive ? '✓ Attivo sul grafico' : 'Seleziona / Scorri'}
                            </span>
                            <span className="text-zinc-400 hover:text-white transition-colors">
                              Visualizza &rarr;
                            </span>
                          </div>
                          
                          {isActive && (
                            <div className="flex flex-col gap-2 pt-2 border-t border-zinc-800/40">
                              <span className="text-[10px] uppercase tracking-wider text-zinc-400 font-bold">Trasparenza Dati:</span>
                              <div className="flex flex-wrap gap-2">
                                <a 
                                  href="https://github.com/Eugenix94/Italienation" 
                                  target="_blank" rel="noopener noreferrer"
                                  className="flex items-center gap-1.5 px-2.5 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded border border-zinc-700 text-[10px] font-medium transition"
                                >
                                  <Download size={12}/> Repository GitHub (Dataset Elaborato)
                                </a>
                                <a 
                                  href="https://github.com/Eugenix94/Italienation/" 
                                  target="_blank" rel="noopener noreferrer"
                                  className="flex items-center gap-1.5 px-2.5 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded border border-zinc-700 text-[10px] font-medium transition"
                                >
                                  <ExternalLink size={12}/> Fonti Open Data (Matrice)
                                </a>
                                <a 
                                  href="https://github.com/Eugenix94/Italienation/tree/main/notebooks" 
                                  target="_blank" rel="noopener noreferrer"
                                  className="flex items-center gap-1.5 px-2.5 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded border border-zinc-700 text-[10px] font-medium transition"
                                >
                                  <Database size={12}/> Script Elaborazione
                                </a>
                                {originLinks[ds.id] && (
                                  <a 
                                    href={originLinks[ds.id]} 
                                    target="_blank" rel="noopener noreferrer"
                                    className="flex items-center gap-1.5 px-2.5 py-1.5 bg-indigo-900/50 hover:bg-indigo-800/60 text-indigo-300 rounded border border-indigo-700/50 text-[10px] font-medium transition"
                                  >
                                    <ExternalLink size={12}/> Fonte Dati Originale
                                  </a>
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Right Column: Sticky Interactive Viewer */}
          <div className="lg:col-span-6 sticky top-[140px] h-[50vh] lg:h-[calc(100vh-160px)] order-1 lg:order-2 z-20">
            <div className="bg-zinc-950/90 backdrop-blur-xl border border-zinc-800 rounded-3xl h-full flex flex-col overflow-hidden shadow-2xl">
              
              {activeDataset ? (
                <>
                  {/* Header */}
                  <div className="p-5 border-b border-zinc-800 bg-zinc-900/40 flex items-center justify-between flex-shrink-0">
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-400 bg-indigo-950/60 px-2 py-0.5 rounded-full border border-indigo-800/40">
                        {activeDataset.category}
                      </span>
                      <h2 className="text-lg font-black text-white capitalize mt-1 truncate max-w-[280px]">
                        {activeDataset.id.replace(/_/g, ' ')}
                      </h2>
                    </div>

                    {/* View Mode Switcher */}
                    <div className="flex bg-zinc-900 p-1 rounded-xl border border-zinc-800">
                      <button 
                        onClick={() => setViewMode('chart')}
                        className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition-all ${viewMode === 'chart' ? 'bg-indigo-600 text-white shadow-md' : 'text-zinc-400 hover:text-white'}`}
                      >
                        <BarChart2 size={14} /> Grafico
                      </button>
                      <button 
                        onClick={() => setViewMode('table')}
                        className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition-all ${viewMode === 'table' ? 'bg-indigo-600 text-white shadow-md' : 'text-zinc-400 hover:text-white'}`}
                      >
                        <Table size={14} /> Tabella
                      </button>
                    </div>
                  </div>

                  {/* Body Content */}
                  <div className="flex-1 p-5 overflow-hidden relative flex flex-col min-h-0">
                    {viewMode === 'chart' ? (
                      <div className="flex-1 flex flex-col h-full">
                        <div className="flex items-center justify-between mb-2 text-[11px] text-zinc-400 flex-shrink-0">
                          <span>Visualizzazione campionaria (primi 25 record)</span>
                          <span className="text-indigo-400 font-mono">Dati reali ISTAT/MIM</span>
                        </div>
                        <div className="flex-1 min-h-0">
                          {renderChart(activeDataset)}
                        </div>
                      </div>
                    ) : (
                      <div className="flex-1 flex flex-col h-full min-h-0">
                        <div className="flex-1 overflow-auto custom-scrollbar border border-zinc-800/60 rounded-xl">
                          <table className="w-full text-left text-xs whitespace-nowrap">
                            <thead className="bg-zinc-900 sticky top-0 z-10">
                              <tr>
                                <th className="px-3 py-2 font-bold text-zinc-400 border-b border-zinc-800 w-8">#</th>
                                {activeDataset.columns.map(col => (
                                  <th key={col} className="px-3 py-2 font-bold text-zinc-200 border-b border-zinc-800">{col}</th>
                                ))}
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-zinc-800/40">
                              {activeDataset.data.slice(0, displayRowsCount).map((row, idx) => (
                                <tr key={idx} className="hover:bg-zinc-900/60 transition-colors">
                                  <td className="px-3 py-2 text-zinc-400 font-mono">{idx + 1}</td>
                                  {activeDataset.columns.map(col => {
                                    const val = row[col];
                                    const isNum = !isNaN(val) && val !== '';
                                    return (
                                      <td key={col} className={`px-3 py-2 ${isNum ? 'font-mono text-indigo-300' : 'text-zinc-400'}`}>
                                        {isNum && String(val).includes('.') ? parseFloat(val).toFixed(2) : val}
                                      </td>
                                    );
                                  })}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>

                        {activeDataset.data.length > displayRowsCount && (
                          <div className="pt-3 flex justify-center flex-shrink-0">
                            <button 
                              onClick={() => setDisplayRowsCount(prev => prev + 50)}
                              className="flex items-center gap-1.5 text-xs text-indigo-400 font-bold bg-indigo-950/40 hover:bg-indigo-950/80 px-4 py-1.5 rounded-xl border border-indigo-800/30 transition-all"
                            >
                              <ChevronDown size={14} /> Mostra altre 50 righe (totale {activeDataset.data.length})
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Footer */}
                  <div className="p-3 border-t border-zinc-800 bg-zinc-900/30 flex items-center justify-between text-xs text-zinc-400 flex-shrink-0">
                    <span className="flex items-center gap-1.5 text-[11px]">
                      <Info size={13} className="text-indigo-400" />
                      Fonte: Institutional Mirror (Open Data)
                    </span>
                    <span className="font-mono text-[10px] text-zinc-400 truncate max-w-[200px]">
                      {activeDataset.filename}
                    </span>
                  </div>
                </>
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-zinc-400">
                  <Database size={48} className="mb-4 opacity-20" />
                  <p>Seleziona o scorri un dataset per iniziare la visualizzazione.</p>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}


