import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { ArrowUp, Globe } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function FloatingActionBar() {
  const { lang, toggleLang } = useLanguage();
  const [isVisible, setIsVisible] = useState(false);

  // Show "Up" button only when scrolled down a bit
  useEffect(() => {
    const toggleVisibility = () => {
      if (window.scrollY > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };
    window.addEventListener('scroll', toggleVisibility);
    return () => window.removeEventListener('scroll', toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3">
      {/* Language Toggle */}
      <button
        onClick={toggleLang}
        className="w-12 h-12 flex items-center justify-center rounded-full bg-zinc-900 border border-zinc-700 text-zinc-300 hover:text-white hover:border-indigo-500 hover:bg-indigo-500/20 shadow-lg shadow-black/50 transition-all backdrop-blur-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-[#09090b]"
        aria-label={lang === 'it' ? 'Cambia lingua' : 'Toggle Language'}
        title={lang === 'it' ? 'Passa all\'Inglese' : 'Switch to Italian'}
      >
        <div className="flex flex-col items-center justify-center leading-none">
          <Globe size={16} className="mb-0.5" aria-hidden="true" />
          <span className="text-[10px] font-bold">{lang === 'it' ? 'EN' : 'IT'}</span>
        </div>
      </button>

      {/* Scroll to Top */}
      <AnimatePresence>
        {isVisible && (
          <motion.button
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            onClick={scrollToTop}
            className="w-12 h-12 flex items-center justify-center rounded-full bg-indigo-600 text-white hover:bg-indigo-500 shadow-[0_0_15px_rgba(79,70,229,0.5)] transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-[#09090b]"
            aria-label={lang === 'it' ? 'Torna all\'inizio' : 'Scroll to top'}
            title={lang === 'it' ? 'Torna all\'inizio' : 'Scroll to top'}
          >
            <ArrowUp size={20} aria-hidden="true" />
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  );
}
