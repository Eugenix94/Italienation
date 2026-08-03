import React, { useState } from 'react';
import { T } from './T';
import { Download, FileText, Printer, Code } from 'lucide-react';
import { motion } from 'framer-motion';

export default function MediaKitExport() {
  const [showMarkdown, setShowMarkdown] = useState(false);

  const markdownContent = `# Italienation: Policy Brief & Executive Summary

## 1. The Core Thesis
The Italian public education system operates as a rigid **Institutional Equilibrium**. Rather than an equalizer, the system structurally amplifies the socioeconomic circumstances of birth. Because the state massively underinvests in education (3.9% GDP vs EU 4.7%), it relies on an "informal familial welfare state." 

## 2. Key Macroeconomic Costs (Annual)
- **Total Estimated Cost:** €259 Billion (13.5% of GDP)
- **NEET Phenomenon:** €36 Billion
- **School Dropout (Dispersione Scolastica):** €5.4 Billion
- **Brain Drain:** €8.2 Billion
- **Grade Retention (Bocciatura):** €1.8 Billion
- **Ripetizioni Black Market:** €800 Million (90% tax evasion rate)

## 3. Structural Failures (Summer 2026 Data)
- **Implicit Dropouts:** 6.3% (Students graduating without basic skills)
- **Explicit Dropouts:** 7.3% (INVALSI 2026 Report)
- **Textbook Costs:** ~€1,238 per student (vs FREE in Finland & Germany)
- **Market Fragmentation:** >42,000 active textbook editions (killing the second-hand market)
- **FSL (Formazione Scuola-Lavoro, ex PCTO):** 1.5M students laboring with €0 compensation.
- **Teacher Precarity:** 250,000 precarious teachers (29.4%) destroying pedagogical continuity.

## 4. Deep Dives
- **STEM Gender Gap:** Only 38.8% of Liceo Scientifico students are female, whereas 87.5% of Liceo Scienze Umane students are female.
- **Infrastructure Divide:** In Southern Italy, 85% of schools lack a cafeteria (Mensa), physically preventing Full-Time schooling.

---
*Synthesized by AI (Antigravity) for the Italienation Project.*
`;

  const generateMarkdown = () => {
    const blob = new Blob([markdownContent], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'policy_brief_italienation.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="w-full bg-zinc-900/40 border-t border-zinc-800 py-12 print:hidden">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 text-center space-y-8">
        
        <div className="space-y-4">
          <h2 className="text-3xl font-black text-white">
            <T it="Esporta Policy Brief" en="Export Policy Brief" />
          </h2>
          <p className="text-zinc-400 text-lg">
            <T 
              it="Scarica i dati sintetizzati per uso giornalistico, accademico e istituzionale." 
              en="Download the synthesized data for journalistic, academic, and institutional use." 
            />
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowMarkdown(!showMarkdown)}
            className="flex items-center gap-3 px-6 py-4 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl font-bold transition-colors w-full sm:w-auto justify-center border border-zinc-700 hover:border-zinc-600 shadow-xl"
          >
            <Code size={20} />
            <T it={showMarkdown ? "Nascondi Markdown" : "Vedi Markdown"} en={showMarkdown ? "Hide Markdown" : "View Markdown"} />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={generateMarkdown}
            className="flex items-center gap-3 px-6 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-colors w-full sm:w-auto justify-center shadow-lg shadow-indigo-500/20"
          >
            <Download size={20} />
            <T it="Scarica Markdown (MD)" en="Download Markdown (MD)" />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handlePrint}
            className="flex items-center gap-3 px-6 py-4 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl font-bold transition-colors w-full sm:w-auto justify-center border border-zinc-700 hover:border-zinc-600 shadow-xl"
          >
            <Printer size={20} />
            <T it="Stampa PDF" en="Print to PDF" />
          </motion.button>

        </div>
        
        {showMarkdown && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mt-8 text-left"
          >
            <div className="bg-zinc-950 p-6 rounded-2xl border border-zinc-800 shadow-2xl relative overflow-hidden group">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 to-purple-500"></div>
              <pre className="text-zinc-300 text-sm overflow-x-auto whitespace-pre-wrap font-mono">
                <code>{markdownContent}</code>
              </pre>
            </div>
          </motion.div>
        )}
        
      </div>
    </div>
  );
}
