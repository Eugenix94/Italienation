import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { T } from './T';
import { BookOpen, Menu } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const isHome = location.pathname === '/';

  return (
    <nav className="sticky top-0 z-50 bg-[#09090b]/90 backdrop-blur-xl border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          
          {/* Logo & Menu Toggle */}
          <div className="flex items-center space-x-2 sm:space-x-4">
            {isHome && (
              <button 
                onClick={() => window.dispatchEvent(new Event('toggle-sidebar'))}
                className="p-2 -ml-2 text-zinc-400 hover:text-white rounded-lg hover:bg-white/5 transition-colors focus:outline-none"
                aria-label="Open navigation sidebar"
              >
                <Menu size={22} />
              </button>
            )}
            <Link to="/" className="flex items-center space-x-3 cursor-pointer">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                <span className="text-white font-bold text-sm">IT</span>
              </div>
              <div className="flex flex-col">
                <span className="text-base font-bold text-white tracking-tight leading-none">Italienation</span>
              </div>
            </Link>
          </div>

          {/* Right Actions */}
          <div className="flex items-center space-x-3">
            <Link 
              to="/guide"
              className="flex items-center gap-2 px-4 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 text-white text-xs font-bold transition shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-[#09090b]"
            >
              <BookOpen size={14} aria-hidden="true" />
              <T it="Guida ai Dati" en="Data Guide" />
            </Link>
            
            <a 
              href="https://github.com/Eugenix94/Italienation" 
              target="_blank" 
              rel="noopener noreferrer"
              className="hidden sm:flex px-4 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-lg shadow-indigo-500/20 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-[#09090b]"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}

