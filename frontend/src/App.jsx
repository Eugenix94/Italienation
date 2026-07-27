import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LanguageProvider } from './contexts/LanguageContext';
import Navbar from './components/Navbar';
import Home from './views/Home';
import SimulatorView from './views/SimulatorView';
import DataCatalog from './views/DataCatalog';
import Footer from './components/Footer';

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter basename={import.meta.env.DEV ? "/" : "/Italienation/"}>
        <div className="min-h-screen bg-[#050510] text-white flex flex-col font-sans relative overflow-hidden">
          
          {/* Global Aesthetic Glow Background */}
          <div className="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-indigo-600/10 rounded-full blur-[120px] pointer-events-none" />
          <div className="fixed bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/10 rounded-full blur-[120px] pointer-events-none" />
          
          <div className="relative z-10 flex flex-col flex-1">
            <Navbar />
            <main className="flex-1 w-full">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/simulator" element={<SimulatorView />} />
              <Route path="/catalog" element={<DataCatalog />} />
            </Routes>
          </main>
          </div>
        </div>  {/* Footer is rendered inside SimulatorView, but we can put a global one here if needed. We'll leave it in SimulatorView to match previous design, or we can move it here. Let's let SimulatorView handle it for now to avoid double footers on the simulator. */}
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
