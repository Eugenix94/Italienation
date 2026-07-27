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
        <div className="min-h-screen bg-[#09090b] text-white flex flex-col font-sans">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/simulator" element={<SimulatorView />} />
              <Route path="/catalog" element={<DataCatalog />} />
            </Routes>
          </main>
          {/* Footer is rendered inside SimulatorView, but we can put a global one here if needed. We'll leave it in SimulatorView to match previous design, or we can move it here. Let's let SimulatorView handle it for now to avoid double footers on the simulator. */}
        </div>
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
