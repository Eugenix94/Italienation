import React from 'react';
import OEDSimulator from './components/OEDSimulator';
import EurydiceChart from './components/EurydiceChart';

function App() {
  return (
    <div className="App dashboard-layout">
      <header className="dashboard-header">
        <h1>The Black Box: OED Framework</h1>
        <p className="subtitle">
          Origin, Education, Destination: The Cybernetics of Italian Inequality
        </p>
      </header>

      <main className="dashboard-main">
        <section className="dashboard-intro glass-panel">
          <h2>The Origin-Education-Destination Paradigm</h2>
          <p>
            In sociology, the OED framework models how a student's social <strong>Origin</strong> (SES) filters through the <strong>Education</strong> system to determine their final socio-economic <strong>Destination</strong>.
          </p>
          <p>
            Italy's system acts as a rigid sorting mechanism. Rather than compensating for a disadvantaged Origin, early tracking and punitive grading calcify it, ensuring that low-SES students are funneled towards the NEET status or precarious labor. 
            By contrast, international systems (like Germany and the Nordics) utilize institutional safety nets to decouple Origin from Destination.
          </p>
        </section>

        <div className="dashboard-grid">
          <div className="dashboard-col">
            <OEDSimulator />
          </div>
          <div className="dashboard-col">
            <EurydiceChart />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
