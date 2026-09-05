import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { T } from './T';
import { useLanguage } from '../contexts/LanguageContext';
import { 
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Area, AreaChart, ReferenceLine
} from 'recharts';
import { Settings, TrendingUp, AlertTriangle, Scale, BookOpen, Building, PiggyBank } from 'lucide-react';
import MethodologyAlert from './MethodologyAlert';

const PolicySandbox = () => {
  const { lang } = useLanguage();
  const isIt = lang === 'it';

  // Baseline Italian macroeconomic parameters (2024 approx)
  const [params, setParams] = useState({
    corporateTax: 24.0, // Base IRES rate
    pensionAge: 67, // Nominal retirement age
    bureaucracyDelay: 100, // Index: 100 is current delay, 50 is half, etc.
    educationInvestment: 4.0 // % of GDP (currently low)
  });

  const [projectionData, setProjectionData] = useState([]);

  // Complex projection model simulating a 10-year horizon
  useEffect(() => {
    const years = [];
    let currentGDP = 100; // Index starting at 100
    let currentDebt = 137; // Approx 137% debt-to-GDP

    for (let i = 0; i <= 10; i++) {
      if (i === 0) {
        years.push({ year: `Anno ${i}`, gdp: currentGDP, debt: currentDebt });
        continue;
      }

      // Delta calculations based on policy levers
      // 1. Corporate Tax: Lowering it stimulates growth but increases short-term debt
      const taxDelta = (24.0 - params.corporateTax) * 0.15; 
      
      // 2. Pension Age: Raising it significantly lowers debt trajectory and boosts workforce GDP
      const pensionDelta = (params.pensionAge - 67) * 0.4;
      
      // 3. Bureaucracy: Slashing red tape (index < 100) unlocks massive GDP potential (FDI attraction)
      const bureaucracyDelta = (100 - params.bureaucracyDelay) * 0.05;

      // 4. Education: High investment yields delayed but compounding GDP growth (multiplier effect)
      const eduDelta = (params.educationInvestment - 4.0) * (i * 0.1); // Compounding effect over time

      // Aggregate Growth Rate
      // Base anemic Italian growth is ~0.8%
      let growthRate = 0.8 + taxDelta + pensionDelta + bureaucracyDelta + eduDelta;
      
      currentGDP = currentGDP * (1 + (growthRate / 100));

      // Debt dynamics
      // Deficit calculation: Lower taxes hurt short-term revenue, higher edu hurts short-term, but pensions save massive amounts. Growth reduces debt-to-GDP denominator.
      let primaryDeficit = 2.0; // Base structural deficit
      primaryDeficit -= (params.corporateTax - 24.0) * 0.2; // Higher tax reduces deficit initially
      primaryDeficit += (params.educationInvestment - 4.0) * 0.8; // Edu costs money
      primaryDeficit -= (params.pensionAge - 67) * 1.5; // Pension cuts save huge money

      // Add interest burden (simplified)
      const interestBurden = currentDebt * 0.04;
      const totalDeficit = primaryDeficit + interestBurden;

      // New Debt to GDP ratio
      // D(t) = D(t-1) + Deficit - Growth effect
      currentDebt = currentDebt + totalDeficit - (currentDebt * (growthRate/100));

      // Boundaries
      if (currentDebt < 0) currentDebt = 0;

      years.push({
        year: `Anno ${i}`,
        gdp: parseFloat(currentGDP.toFixed(1)),
        debt: parseFloat(currentDebt.toFixed(1))
      });
    }

    setProjectionData(years);
  }, [params]);


  const updateParam = (key, value) => {
    setParams(prev => ({ ...prev, [key]: parseFloat(value) }));
  };

  return (
    <div className="w-full text-white font-sans py-16">
      <section className="max-w-7xl mx-auto px-4 w-full flex flex-col items-center">
        
        {/* Header Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-16 text-center w-full"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-sm font-medium mb-6">
            <Settings size={16} />
            <T it="Simulatore Economico" en="Economic Simulator" />
          </div>
          <h2 className="text-4xl md:text-5xl font-black mb-6 tracking-tight">
            <T it="Sandbox di Politica Fiscale" en="Fiscal Policy Sandbox" />
          </h2>
          <p className="text-zinc-400 max-w-3xl mx-auto text-lg">
            <T 
              it="Modifica le leve macroeconomiche italiane e osserva l'impatto proiettato su 10 anni. Tagliare le tasse stimola la crescita, ma fa esplodere il debito senza tagli alle pensioni. Aumentare la spesa nell'istruzione costa nel breve termine, ma genera crescita composta. Trova l'equilibrio." 
              en="Tweak Italian macroeconomic levers and observe the projected 10-year impact. Cutting taxes stimulates growth but explodes debt without pension reform. Boosting education spending costs short-term capital but yields compounding growth. Find the equilibrium." 
            />
          </p>
        </motion.div>

        <div className="w-full flex flex-col xl:flex-row gap-8">
          
          {/* Left: The Levers (Controls) */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="w-full xl:w-1/3 bg-zinc-950/50 border border-zinc-800 p-8 rounded-3xl shadow-xl flex flex-col gap-8"
          >
            <h3 className="text-2xl font-bold flex items-center gap-3 mb-2">
              <Scale className="text-indigo-400" />
              <T it="Leve Strutturali" en="Structural Levers" />
            </h3>

            {/* Corporate Tax */}
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center">
                <label className="font-semibold text-zinc-300 flex items-center gap-2">
                  <Building size={16} className="text-amber-400" />
                  <T it="Tassazione Aziendale (IRES)" en="Corporate Tax (IRES)" />
                </label>
                <span className="font-mono text-amber-400 font-bold bg-amber-500/10 px-2 py-1 rounded">{params.corporateTax}%</span>
              </div>
              <input 
                type="range" min="10" max="35" step="0.5" 
                value={params.corporateTax} onChange={(e) => updateParam('corporateTax', e.target.value)}
                className="w-full accent-amber-500"
              />
              <p className="text-xs text-zinc-500">
                <T it="Base: 24.0%. Tasse più basse attraggono capitali ma riducono il gettito immediato." en="Base: 24.0%. Lower taxes attract capital but slash immediate revenue." />
              </p>
            </div>

            {/* Pension Age */}
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center">
                <label className="font-semibold text-zinc-300 flex items-center gap-2">
                  <PiggyBank size={16} className="text-rose-400" />
                  <T it="Età Pensionabile Reale" en="Effective Pension Age" />
                </label>
                <span className="font-mono text-rose-400 font-bold bg-rose-500/10 px-2 py-1 rounded">{params.pensionAge} Anni</span>
              </div>
              <input 
                type="range" min="60" max="72" step="1" 
                value={params.pensionAge} onChange={(e) => updateParam('pensionAge', e.target.value)}
                className="w-full accent-rose-500"
              />
              <p className="text-xs text-zinc-500">
                <T it="Base: 67. Aumentare l'età salva i conti INPS e forza la produttività." en="Base: 67. Raising the age saves the INPS budget and forces productivity." />
              </p>
            </div>

            {/* Bureaucracy */}
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center">
                <label className="font-semibold text-zinc-300 flex items-center gap-2">
                  <AlertTriangle size={16} className="text-red-500" />
                  <T it="Indice di Burocrazia" en="Bureaucracy Index" />
                </label>
                <span className="font-mono text-red-400 font-bold bg-red-500/10 px-2 py-1 rounded">{params.bureaucracyDelay} (Base 100)</span>
              </div>
              <input 
                type="range" min="20" max="150" step="5" 
                value={params.bureaucracyDelay} onChange={(e) => updateParam('bureaucracyDelay', e.target.value)}
                className="w-full accent-red-500"
              />
              <p className="text-xs text-zinc-500">
                <T it="100 = Attuale. Ridurre la burocrazia sblocca enormi investimenti esteri (FDI)." en="100 = Current. Slashing red tape unlocks massive Foreign Direct Investment (FDI)." />
              </p>
            </div>

            {/* Education */}
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center">
                <label className="font-semibold text-zinc-300 flex items-center gap-2">
                  <BookOpen size={16} className="text-emerald-400" />
                  <T it="Spesa Istruzione (% PIL)" en="Education Spend (% GDP)" />
                </label>
                <span className="font-mono text-emerald-400 font-bold bg-emerald-500/10 px-2 py-1 rounded">{params.educationInvestment.toFixed(1)}%</span>
              </div>
              <input 
                type="range" min="2" max="8" step="0.1" 
                value={params.educationInvestment} onChange={(e) => updateParam('educationInvestment', e.target.value)}
                className="w-full accent-emerald-500"
              />
              <p className="text-xs text-zinc-500">
                <T it="Base: 4.0%. La spesa alta crea deficit oggi, ma crescita massiccia tra 5-10 anni." en="Base: 4.0%. High spending creates deficit today, but massive compounding growth in 5-10 years." />
              </p>
            </div>

          </motion.div>


          {/* Right: The Charts */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="w-full xl:w-2/3 flex flex-col gap-8"
          >
            {/* GDP Growth Chart */}
            <div className="bg-zinc-950/50 border border-zinc-800 p-6 rounded-3xl shadow-xl h-80">
              <h4 className="text-xl font-bold mb-4 flex items-center gap-2">
                <TrendingUp className="text-emerald-400" />
                <T it="Proiezione PIL (Indice Base = 100)" en="GDP Projection (Base Index = 100)" />
              </h4>
              <ResponsiveContainer width="100%" height="80%">
                <AreaChart data={projectionData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorGdp" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="year" stroke="#888" fontSize={12} />
                  <YAxis domain={['auto', 'auto']} stroke="#888" fontSize={12} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', color: '#f4f4f5' }}
                    itemStyle={{ color: '#10b981', fontWeight: 'bold' }}
                  />
                  <ReferenceLine y={100} stroke="#52525b" strokeDasharray="3 3" />
                  <Area type="monotone" dataKey="gdp" name={isIt ? "PIL" : "GDP"} stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorGdp)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Debt to GDP Chart */}
            <div className="bg-zinc-950/50 border border-zinc-800 p-6 rounded-3xl shadow-xl h-80">
              <h4 className="text-xl font-bold mb-4 flex items-center gap-2">
                <AlertTriangle className="text-rose-400" />
                <T it="Rapporto Debito/PIL (%)" en="Debt-to-GDP Ratio (%)" />
              </h4>
              <ResponsiveContainer width="100%" height="80%">
                <LineChart data={projectionData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="year" stroke="#888" fontSize={12} />
                  <YAxis domain={['auto', 'auto']} stroke="#888" fontSize={12} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', color: '#f4f4f5' }}
                    itemStyle={{ color: '#f43f5e', fontWeight: 'bold' }}
                    formatter={(value) => [`${value}%`, 'Debito/PIL']}
                  />
                  <ReferenceLine y={137} stroke="#52525b" strokeDasharray="3 3" label={{ position: 'top', value: 'Base 2024', fill: '#71717a', fontSize: 10 }} />
                  <Line type="monotone" dataKey="debt" name={isIt ? "Debito/PIL" : "Debt/GDP"} stroke="#f43f5e" strokeWidth={3} dot={{ r: 4, fill: '#18181b', strokeWidth: 2 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

          </motion.div>
        </div>

        <div className="w-full mt-12">
          <MethodologyAlert 
            itText="Questo simulatore è un modello euristico semplificato per dimostrare le relazioni sistemiche inverse tra pressione fiscale, spesa pubblica, riforme strutturali e sostenibilità del debito. Non è un simulatore econometrico certificato, ma riflette le proiezioni standard del Fondo Monetario Internazionale (FMI) sull'impatto dei moltiplicatori fiscali."
            enText="This sandbox is a simplified heuristic model demonstrating the inverse systemic relationships between tax burden, public spending, structural reforms, and debt sustainability. It is not a certified econometric simulator, but it reflects standard IMF projections on the impact of fiscal multipliers."
          />
        </div>

      </section>
    </div>
  );
};

export default PolicySandbox;
