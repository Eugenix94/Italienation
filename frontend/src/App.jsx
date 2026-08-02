import React, { Suspense, lazy } from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import { LanguageProvider } from './contexts/LanguageContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ErrorBoundary from './components/ErrorBoundary';
import FloatingActionBar from './components/FloatingActionBar';
import EducationalGuide from './components/EducationalGuide';
import LaborMarketAndCorrelations from './components/LaborMarketAndCorrelations';
import { Loader2 } from 'lucide-react';

const UnifiedHome = lazy(() => import('./views/UnifiedHome'));

const PageLoader = () => (
  <div className="flex flex-col items-center justify-center min-h-[60vh] text-zinc-400 gap-4">
    <Loader2 className="animate-spin text-indigo-500" size={40} />
    <span className="text-xs font-semibold tracking-wider uppercase">Caricamento piattaforma...</span>
  </div>
);

function App() {
  return (
    <LanguageProvider>
      <HashRouter>
        <div className="min-h-screen bg-[#050510] text-white flex flex-col font-sans relative overflow-hidden">
          
          {/* Global Aesthetic Glow Background */}
          <div className="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none" />
          <div className="fixed bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/10 rounded-full blur-[120px] pointer-events-none" />
          
          <div className="relative z-10 flex flex-col flex-1">
            <Navbar />
            <main className="flex-1 w-full">
              <ErrorBoundary>
                <Suspense fallback={<PageLoader />}>
                  <Routes>
                    <Route path="/" element={<UnifiedHome />} />
                    <Route path="/guide" element={<EducationalGuide />} />
                    <Route path="/labor" element={<LaborMarketAndCorrelations />} />
                    <Route path="*" element={<UnifiedHome />} />
                  </Routes>
                </Suspense>
              </ErrorBoundary>
            </main>
            <Footer />
            <FloatingActionBar />
          </div>
        </div>
      </HashRouter>
    </LanguageProvider>
  );
}

export default App;


