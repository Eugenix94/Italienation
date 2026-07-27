import React from 'react';
import { NavLink } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import { BookOpen, LineChart, Database, Globe } from 'lucide-react';
import { T } from './T';

export default function Navbar() {
  const { lang, toggleLang } = useLanguage();

  return (
    <nav className="sticky top-0 z-50 bg-[#09090b]/80 backdrop-blur-xl border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          
          {/* Logo & Brand */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <span className="text-white font-bold text-sm">IT</span>
            </div>
            <span className="text-lg font-bold text-white tracking-tight">Italienation</span>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex space-x-8">
            <NavLink 
              to="/" 
              className={({isActive}) => `flex items-center space-x-2 text-sm font-medium transition-colors ${isActive ? 'text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
            >
              <BookOpen size={16} />
              <span><T it="Il Manifesto" en="The Manifesto" /></span>
            </NavLink>
            <NavLink 
              to="/simulator" 
              className={({isActive}) => `flex items-center space-x-2 text-sm font-medium transition-colors ${isActive ? 'text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
            >
              <LineChart size={16} />
              <span><T it="Simulatore OED" en="OED Simulator" /></span>
            </NavLink>
            <NavLink 
              to="/catalog" 
              className={({isActive}) => `flex items-center space-x-2 text-sm font-medium transition-colors ${isActive ? 'text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
            >
              <Database size={16} />
              <span><T it="Directory Dati" en="Data Directory" /></span>
            </NavLink>
          </div>

          {/* Right Actions */}
          <div className="flex items-center space-x-4">
            <button 
              onClick={toggleLang}
              className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-bold border border-zinc-700 transition"
              aria-label="Cambia lingua / Change language"
            >
              <Globe size={14} />
              <span>{lang === 'it' ? 'EN' : 'IT'}</span>
            </button>
            <a 
              href="https://github.com/Eugenix94/Italienation" 
              target="_blank" 
              rel="noopener noreferrer"
              className="hidden sm:flex px-4 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-lg shadow-indigo-500/20"
            >
              GitHub
            </a>
          </div>

        </div>
      </div>
    </nav>
  );
}
