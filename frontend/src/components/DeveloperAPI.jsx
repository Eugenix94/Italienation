import React, { useState, useEffect } from 'react';
import { Terminal, Copy, Database, Check, Server, FileJson, ArrowRight, Loader2 } from 'lucide-react';
import { T } from './T';
import originLinks from '../assets/originLinks.json';

export default function DeveloperAPI() {
  const [copied, setCopied] = useState(false);
  const [indexData, setIndexData] = useState({ datasets: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    
    // Determine public data path accommodating Vite base path
    const dataUrl = import.meta.env.BASE_URL 
      ? `${import.meta.env.BASE_URL.replace(/\/$/, '')}/data/master_data_observatory.json`
      : './data/master_data_observatory.json';

    fetch(dataUrl)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then(data => {
        if (!isMounted) return;
        
        // Parse the master data to create the endpoint catalog
        const datasetsList = [];
        
        Object.entries(data).forEach(([category, datasets]) => {
          datasets.forEach(ds => {
            datasetsList.push({
              id: ds.id,
              endpoint: `https://github.com/Eugenix94/Italienation/blob/main/frontend/public/data/master_data_observatory.json`,
              source_url: originLinks[ds.id],
              category: category,
              rows: ds.data.length
            });
          });
        });
        
        setIndexData({ datasets: datasetsList });
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load catalog:", err);
        // Fallback for local dev
        fetch('./data/master_data_observatory.json')
          .then(r => r.json())
          .then(data => {
            if (!isMounted) return;
            const datasetsList = [];
            Object.entries(data).forEach(([category, datasets]) => {
              datasets.forEach(ds => {
                datasetsList.push({
                  id: ds.id,
                  endpoint: `https://github.com/Eugenix94/Italienation/blob/main/frontend/public/data/master_data_observatory.json`,
                  source_url: originLinks[ds.id],
                  category: category,
                  rows: ds.data.length
                });
              });
            });
            setIndexData({ datasets: datasetsList });
            setLoading(false);
          })
          .catch(() => {
             if (isMounted) setLoading(false);
          });
      });

    return () => { isMounted = false; };
  }, []);

  const copyCode = () => {
    navigator.clipboard.writeText(`fetch('https://eugenix94.github.io/Italienation/api/v1/index.json')\n  .then(response => response.json())\n  .then(data => console.log(data));`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-12 space-y-12">
      {/* Coming Soon Banner */}
      <div className="bg-amber-500/10 border border-amber-500/30 rounded-2xl p-6 flex items-start gap-4">
        <div className="text-3xl">🚧</div>
        <div>
          <h2 className="text-lg font-bold text-amber-400 mb-1">
            <T it="API in Fase di Sviluppo" en="API Under Development" />
          </h2>
          <p className="text-sm text-amber-200/70">
            <T 
              it="Questa API REST non è ancora disponibile. Attualmente, tutti i dataset sono accessibili come file JSON/CSV statici nel repository GitHub. Questa pagina documenta l'architettura prevista." 
              en="This REST API is not yet live. Currently, all datasets are accessible as static JSON/CSV files in the GitHub repository. This page documents the planned architecture." 
            />
          </p>
          <a 
            href="https://github.com/Eugenix94/Italienation/tree/main/processed_data" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="inline-flex items-center gap-2 mt-3 px-4 py-2 bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 text-sm font-medium rounded-lg transition"
          >
            <T it="📂 Accedi ai dati su GitHub" en="📂 Access Data on GitHub" />
          </a>
        </div>
      </div>
      <div className="space-y-4">
        <div className="flex items-center gap-3 text-indigo-400">
          <Terminal size={32} />
          <h1 className="text-3xl font-black text-white">
            <T it="API per Sviluppatori" en="Developer API" />
          </h1>
        </div>
        <p className="text-zinc-400 max-w-3xl text-lg leading-relaxed">
          <T 
            it="L'intero archivio dati di Italienation è disponibile come API statica pubblica. Giornalisti, ricercatori e data scientist possono accedere programmaticamente a tutti i 32 dataset elaborati senza alcuna chiave API o autenticazione." 
            en="The entire Italienation data archive is available as a public static API. Journalists, researchers, and data scientists can programmatically access all 32 processed datasets without any API key or authentication." 
          />
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Left Column: Documentation */}
        <div className="space-y-6 h-[500px] overflow-y-auto custom-scrollbar pr-2 pb-6">
          <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-2xl shadow-xl">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Server size={20} className="text-indigo-400" />
              <T it="Come Utilizzare l'API" en="How to Use the API" />
            </h2>
            <p className="text-sm text-zinc-400 mb-6">
              <T it="L'API è ospitata staticamente. Tutte le risposte sono in formato JSON standard." en="The API is statically hosted. All responses are in standard JSON format." />
            </p>
            
            <div className="space-y-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-2 block">Base URL</span>
                <code className="block w-full bg-black border border-zinc-800 p-3 rounded-lg text-emerald-400 font-mono text-sm break-all">
                  https://eugenix94.github.io/Italienation/api/v1/
                </code>
              </div>
              
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-zinc-400 mb-2 block">Endpoints Principali / Core Endpoints</span>
                <ul className="space-y-2 font-mono text-sm text-zinc-300 bg-black border border-zinc-800 p-4 rounded-lg overflow-x-auto custom-scrollbar">
                  <li className="flex items-center gap-2"><ArrowRight size={14} className="text-indigo-500 min-w-[14px]"/> /index.json <span className="text-zinc-400 text-xs ml-auto">Indice unificato</span></li>
                  <li className="flex items-center gap-2"><ArrowRight size={14} className="text-indigo-500 min-w-[14px]"/> Repository GitHub (Dataset Elaborato)</li>
                  <li className="flex items-center gap-2"><ArrowRight size={14} className="text-emerald-500 min-w-[14px]"/> Fonte Istituzionale (URL Diretto / Provenienza)</li>
                  <li className="flex items-center gap-2 text-zinc-400 text-xs mt-2 italic">Tutti i link istituzionali garantiscono la conformità della provenienza.</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-2xl shadow-xl relative group">
            <button 
              onClick={copyCode}
              className="absolute top-4 right-4 p-2 bg-zinc-800 hover:bg-zinc-700 rounded-lg text-zinc-400 transition"
            >
              {copied ? <Check size={16} className="text-emerald-400" /> : <Copy size={16} />}
            </button>
            <h2 className="text-sm font-bold text-white mb-4 uppercase tracking-wider">
              <T it="Esempio di Fetch (JavaScript)" en="Fetch Example (JavaScript)" />
            </h2>
            <pre className="text-sm text-zinc-300 font-mono overflow-x-auto custom-scrollbar pb-2">
{`fetch('https://eugenix94.github.io/Italienation/api/v1/index.json')
  .then(response => response.json())
  .then(data => {
    console.log("Available Datasets:", data.datasets.length);
    // Fetch a specific dataset
    return fetch('https://eugenix94.github.io/Italienation/api/v1/education/istat_bocciati_rimandati_rates.json');
  })
  .then(res => res.json())
  .then(dataset => console.log(dataset));`}
            </pre>
          </div>
        </div>

        {/* Right Column: Index List */}
        <div className="bg-zinc-950/90 border border-zinc-800 rounded-2xl flex flex-col h-[500px] shadow-2xl">
          <div className="p-6 border-b border-zinc-800 bg-zinc-900/50 rounded-t-2xl flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Database size={18} className="text-indigo-400" />
              <T it="Catalogo Fonti Istituzionali" en="Institutional Sources Catalog" />
            </h2>
            <span className="bg-indigo-500/20 text-indigo-400 px-3 py-1 rounded-full text-xs font-bold border border-indigo-500/30">
              {indexData.datasets.length} Datasets
            </span>
          </div>
          <div className="flex-1 overflow-auto custom-scrollbar p-4 space-y-2">
            {indexData.datasets.map(ds => (
              <div key={ds.id} className="flex flex-col p-3 bg-white/[0.02] hover:bg-white/[0.05] border border-white/5 rounded-xl transition group">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <FileJson size={16} className="text-zinc-400 group-hover:text-indigo-400 transition" />
                    <div className="text-sm font-bold text-zinc-300 group-hover:text-white transition">{ds.id}</div>
                  </div>
                  <div className="flex gap-2 mt-2 sm:mt-0">
                    <span className="px-2 py-1 bg-zinc-800 rounded text-[10px] text-zinc-400 uppercase">{ds.category}</span>
                    <span className="px-2 py-1 bg-zinc-800 rounded text-[10px] text-zinc-400">{ds.rows} rows</span>
                  </div>
                </div>
                
                <div className="pl-7 space-y-1.5">
                  <a href={ds.endpoint} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-xs text-zinc-400 font-mono hover:text-indigo-400 transition break-all">
                    <ArrowRight size={12} className="text-zinc-400 shrink-0" />
                    <span>[GitHub] {ds.endpoint}</span>
                  </a>
                  {ds.source_url && (
                    <a href={ds.source_url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-xs text-emerald-500/70 font-mono hover:text-emerald-400 transition break-all">
                      <ArrowRight size={12} className="text-emerald-400 shrink-0" />
                      <span>[Fonte Istituzionale] {ds.source_url}</span>
                    </a>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex flex-col items-center justify-center py-12 text-zinc-400 gap-3">
                <Loader2 className="animate-spin text-indigo-500" size={32} />
                <T it="Caricamento catalogo endpoints..." en="Loading endpoints catalog..." />
              </div>
            )}
            {!loading && indexData.datasets.length === 0 && (
              <div className="text-center py-10 text-zinc-400">
                <T it="Nessun dataset trovato." en="No datasets found." />
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
