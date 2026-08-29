import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLanguage } from '../contexts/LanguageContext';
import { T } from './T';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, Legend
} from 'recharts';
import { Clock, Landmark, Building2, User, Coins, AlertTriangle, ChevronDown } from 'lucide-react';
import fiscalData from '../assets/fiscal_anatomy.json';
import MethodologyAlert from './MethodologyAlert';

const FiscalAnatomy = () => {
  const { lang } = useLanguage();
  const [selectedCountry, setSelectedCountry] = useState('Italy');

  const countries = Object.keys(fiscalData.fiscal_research.countries).sort();
  
  // Data for the complexity chart, sorted from highest hours to lowest
  const complexityData = countries
    .map(country => ({
      name: country,
      hours: fiscalData.fiscal_research.countries[country].tax_complexity.time_to_comply_hours,
      level: fiscalData.fiscal_research.countries[country].tax_complexity.burden_level
    }))
    .sort((a, b) => b.hours - a.hours);

  const selectedData = fiscalData.fiscal_research.countries[selectedCountry];

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
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-sm font-medium mb-6">
            <Landmark size={16} />
            <T it="Dinamiche Sistemiche EU-27" en="EU-27 Systemic Dynamics" />
          </div>
          <h2 className="text-4xl md:text-5xl font-black mb-6 tracking-tight">
            <T it="Anatomia Fiscale & Attrito" en="Fiscal Anatomy & Friction" />
          </h2>
          <p className="text-zinc-400 max-w-3xl mx-auto text-lg">
            <T 
              it="Per comprendere la stagnazione economica, dobbiamo guardare oltre le singole aliquote e analizzare l'intero ecosistema fiscale europeo: la complessità aziendale, la tassazione sul patrimonio, il prelievo sui redditi e l'enorme carico burocratico (costo di conformità) che frena la competitività." 
              en="To understand economic stagnation, we must look beyond individual tax rates and analyze the entire European fiscal ecosystem: corporate complexity, wealth taxation, personal income levies, and the immense bureaucratic burden (compliance cost) that drags on competitiveness." 
            />
          </p>
        </motion.div>

        {/* Bureaucratic Friction Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="w-full mb-20"
        >
          <h3 className="text-2xl font-bold mb-8 text-center flex items-center justify-center gap-3">
            <Clock className="text-rose-400" />
            <T it="Attrito Burocratico: Tempo per la Conformità Fiscale" en="Bureaucratic Friction: Time to Comply with Taxes" />
          </h3>
          <div className="bg-zinc-950/50 border border-zinc-800 rounded-2xl p-6 h-[800px] w-full shadow-2xl relative">
            <div className="absolute top-6 left-6 text-zinc-400 text-sm max-w-xs z-10 hidden md:block">
              <T it="Ore annuali stimate spese dalle medie imprese per preparare, dichiarare e pagare le tasse." en="Estimated annual hours spent by medium-sized businesses preparing, filing, and paying taxes." />
            </div>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={complexityData} margin={{ top: 40, right: 30, left: 20, bottom: 20 }} layout="vertical" barSize={16}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={true} vertical={false} />
                <XAxis type="number" stroke="#888" domain={[0, 'dataMax + 20']} />
                <YAxis dataKey="name" type="category" stroke="#888" width={90} tick={{ fontSize: 12 }} />
                <Tooltip 
                  cursor={{fill: '#ffffff05'}}
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#3f3f46', color: '#f4f4f5', borderRadius: '0.5rem', fontWeight: 'bold' }} 
                  formatter={(value, name, props) => [
                    lang === 'it' ? `${value} ore (Onere: ${props.payload.level})` : `${value} hours (Burden: ${props.payload.level})`, 
                    lang === 'it' ? 'Tempo di Conformità' : 'Time to Comply'
                  ]}
                />
                <Bar dataKey="hours" name={lang === 'it' ? 'Ore/Anno' : 'Hours/Year'} radius={[0, 4, 4, 0]}>
                  {
                    complexityData.map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`} 
                        fill={entry.name === 'Italy' ? '#f43f5e' : entry.hours < 120 ? '#10b981' : entry.hours > 200 ? '#ef4444' : '#6366f1'} 
                      />
                    ))
                  }
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Deep Dive Explorer */}
        <div className="w-full">
          <h3 className="text-2xl font-bold mb-8 text-center">
            <T it="Esploratore dei Regimi Fiscali EU-27" en="EU-27 Tax Regime Explorer" />
          </h3>
          
          {/* Custom Select Dropdown */}
          <div className="flex justify-center mb-10 w-full">
            <div className="relative w-full max-w-md">
              <select
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
                className="w-full appearance-none bg-zinc-900 border-2 border-zinc-700 text-white font-bold text-lg px-6 py-4 rounded-xl shadow-[0_0_20px_rgba(79,70,229,0.2)] focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all cursor-pointer"
              >
                {countries.map((country) => (
                  <option key={country} value={country} className="bg-zinc-900 text-white">
                    {country}
                  </option>
                ))}
              </select>
              <div className="absolute right-4 top-1/2 transform -translate-y-1/2 pointer-events-none text-zinc-400">
                <ChevronDown size={24} />
              </div>
            </div>
          </div>

          {/* Deep Dive Content */}
          <AnimatePresence mode="wait">
            <motion.div
              key={selectedCountry}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="w-full flex flex-col lg:flex-row gap-8"
            >
              {/* Left Column: The Philosophy */}
              <div className="w-full lg:w-1/3 flex flex-col gap-6">
                <div className={`p-8 rounded-3xl border ${selectedCountry === 'Italy' ? 'bg-rose-500/5 border-rose-500/20' : 'bg-indigo-500/5 border-indigo-500/20'} h-full flex flex-col justify-center relative overflow-hidden`}>
                  {selectedCountry === 'Italy' && <div className="absolute top-0 right-0 w-32 h-32 bg-rose-500/10 blur-3xl rounded-full" />}
                  <h4 className="text-xl font-black mb-4 uppercase tracking-widest text-zinc-100">
                    <T it="Il Fenomeno" en="The Phenomenon" />
                  </h4>
                  <p className="text-zinc-300 leading-relaxed text-lg">
                    {lang === 'it' ? selectedData.phenomenon_it : selectedData.phenomenon_en}
                  </p>
                </div>
              </div>

              {/* Right Column: The Data Grid */}
              <div className="w-full lg:w-2/3 grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Corporate Tax */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 hover:bg-zinc-800/50 transition-colors">
                  <div className="flex items-center gap-3 mb-4 text-zinc-400">
                    <Building2 className="text-indigo-400" />
                    <h4 className="font-bold uppercase tracking-wider text-sm"><T it="Tassazione Aziendale (CIT)" en="Corporate Tax (CIT)" /></h4>
                  </div>
                  <div className="text-4xl font-black text-white mb-4">{selectedData.corporate_tax.headline_rate}%</div>
                  <p className="text-sm text-zinc-400 leading-relaxed">
                    <strong className="text-zinc-200"><T it="Complessità:" en="Complexity:" /></strong> {selectedData.corporate_tax.complexity}
                  </p>
                </div>

                {/* Personal Income Tax */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 hover:bg-zinc-800/50 transition-colors">
                  <div className="flex items-center gap-3 mb-4 text-zinc-400">
                    <User className="text-emerald-400" />
                    <h4 className="font-bold uppercase tracking-wider text-sm"><T it="Imposta sul Reddito (PIT)" en="Personal Income Tax (PIT)" /></h4>
                  </div>
                  <div className="text-4xl font-black text-white mb-2"><T it="Fino al" en="Up to" /> {selectedData.personal_income_tax.top_marginal_rate}%</div>
                  <p className="text-sm text-zinc-400 leading-relaxed mt-4">
                    <strong className="text-zinc-200"><T it="Addizionali:" en="Surcharges:" /></strong> {selectedData.personal_income_tax.surcharges}
                  </p>
                </div>

                {/* Capital Gains */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 hover:bg-zinc-800/50 transition-colors">
                  <div className="flex items-center gap-3 mb-4 text-zinc-400">
                    <Coins className="text-amber-400" />
                    <h4 className="font-bold uppercase tracking-wider text-sm"><T it="Plusvalenze & Dividendi" en="Capital Gains & Dividends" /></h4>
                  </div>
                  <div className="text-3xl font-black text-white mb-4">{selectedData.capital_gains_dividend_tax.rate}</div>
                  <p className="text-sm text-zinc-400 leading-relaxed">
                    <strong className="text-zinc-200"><T it="Note:" en="Notes:" /></strong> {selectedData.capital_gains_dividend_tax.notes}
                  </p>
                </div>

                {/* Wealth & Property */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 hover:bg-zinc-800/50 transition-colors">
                  <div className="flex items-center gap-3 mb-4 text-zinc-400">
                    <Landmark className={selectedData.wealth_property_tax.presence ? "text-rose-400" : "text-zinc-400"} />
                    <h4 className="font-bold uppercase tracking-wider text-sm"><T it="Patrimoniale & Immobili" en="Wealth & Property Tax" /></h4>
                  </div>
                  <div className="flex items-center gap-2 mb-4">
                    {selectedData.wealth_property_tax.presence ? (
                      <span className="px-3 py-1 bg-rose-500/20 text-rose-400 text-sm font-bold rounded-lg uppercase"><T it="Attiva" en="Active" /></span>
                    ) : (
                      <span className="px-3 py-1 bg-zinc-800 text-zinc-400 text-sm font-bold rounded-lg uppercase"><T it="Nessuna / Solo Locale" en="None / Local Only" /></span>
                    )}
                  </div>
                  <p className="text-sm text-zinc-400 leading-relaxed">
                    {selectedData.wealth_property_tax.details}
                  </p>
                </div>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>

        <div className="w-full mt-12">
          <MethodologyAlert 
            itText="Dati strutturali fiscali estratti da report OCSE, World Bank, PwC Paying Taxes e normative governative nazionali per l'anno 2024/2025. Le aliquote effettive possono variare in base a deduzioni specifiche, trattati internazionali e scaglioni di reddito."
            enText="Structural fiscal data extracted from OECD, World Bank, PwC Paying Taxes reports, and national government regulations for 2024/2025. Effective rates may vary based on specific deductions, international treaties, and income brackets."
          />
        </div>

      </section>
    </div>
  );
};

export default FiscalAnatomy;
