import React from 'react';

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-[#09090b]/90 backdrop-blur-xl border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          
          {/* Logo */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <span className="text-white font-bold text-sm">IT</span>
            </div>
            <div className="flex flex-col">
              <span className="text-base font-bold text-white tracking-tight leading-none">Italienation</span>
            </div>
          </div>

          {/* Right Actions */}
          <div className="flex items-center space-x-3">
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

