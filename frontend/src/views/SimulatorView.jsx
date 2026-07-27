import React from 'react';
import OEDSimulator from '../components/OEDSimulator';
import EurydiceChart from '../components/EurydiceChart';
import KeyMetrics from '../components/KeyMetrics';
import MigrationComparison from '../components/MigrationComparison';
import Footer from '../components/Footer';
import { T } from '../components/T';

export default function SimulatorView() {
  return (
    <div className="App">
      {/* Hero */}
      <header className="hero">
        <div className="hero-glow" />
        <div className="hero-content">
          <span className="hero-badge">
            <T it="Ricerca Aperta · Fase 2" en="Open Research · Phase 2" />
          </span>
          <h1>Italienation</h1>
          <p className="hero-subtitle">
            <T 
              it="Il Modello Origine-Educazione-Destinazione (OED): Come la scuola italiana produce disuguaglianza." 
              en="The Origin–Education–Destination Framework: How Italy's Education System Manufactures Inequality" 
            />
          </p>
          <div className="hero-stats">
            <div className="hero-stat">
              <span className="hero-stat-value">19%</span>
              <span className="hero-stat-label"><T it="Tasso NEET (15-29)" en="NEET Rate (15-29)" /></span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat">
              <span className="hero-stat-value">€48B</span>
              <span className="hero-stat-label"><T it="Perdita Capitale Umano" en="Annual Human Capital Loss" /></span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat">
              <span className="hero-stat-value">14 <T it="anni" en="yrs" /></span>
              <span className="hero-stat-label"><T it="Età di Scelta (Anomalia UE)" en="Tracking Age (EU Outlier)" /></span>
            </div>
          </div>
        </div>
      </header>

      {/* Intro Section */}
      <section className="section section-intro">
        <div className="container">
          <div className="intro-grid">
            <div className="intro-text">
              <h2><T it="La Scatola Nera" en="The Black Box" /></h2>
              <p>
                <T 
                  it="In sociologia, il modello OED spiega come l'Origine sociale di uno studente passi attraverso il sistema Educativo per determinare la sua Destinazione socio-economica." 
                  en="In sociology, the OED framework models how a student's social Origin (SES) filters through the Education system to determine their final socio-economic Destination." 
                />
              </p>
              <p>
                <T 
                  it="Il sistema italiano agisce come un meccanismo di selezione rigido. Invece di compensare lo svantaggio, la scelta precoce a 14 anni lo calcifica, spingendo gli studenti fragili verso il lavoro precario o la condizione di NEET." 
                  en="Italy's system acts as a rigid sorting mechanism. Rather than compensating for a disadvantaged Origin, early tracking at age 14 calcifies it — ensuring that low-SES students are funneled towards NEET status or precarious labor." 
                />
              </p>
            </div>
            <div className="intro-visual">
              <div className="oed-diagram">
                <div className="oed-node oed-origin">
                  <span className="oed-node-icon">🏠</span>
                  <span className="oed-node-label"><T it="Origine" en="Origin" /></span>
                  <span className="oed-node-desc"><T it="Famiglia SES" en="Family SES" /></span>
                </div>
                <div className="oed-arrow">→</div>
                <div className="oed-node oed-education">
                  <span className="oed-node-icon">🏫</span>
                  <span className="oed-node-label"><T it="Educazione" en="Education" /></span>
                  <span className="oed-node-desc"><T it="Filtro Scolastico" en="System Filter" /></span>
                </div>
                <div className="oed-arrow">→</div>
                <div className="oed-node oed-destination">
                  <span className="oed-node-icon">🎯</span>
                  <span className="oed-node-label"><T it="Destinazione" en="Destination" /></span>
                  <span className="oed-node-desc"><T it="Esito di Vita" en="Life Outcome" /></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <KeyMetrics />

      <section id="simulator" className="section section-simulator">
        <div className="container">
          <OEDSimulator />
        </div>
      </section>

      <section className="section section-eurydice">
        <div className="container">
          <EurydiceChart />
        </div>
      </section>

      <section className="section section-migration">
        <div className="container">
          <MigrationComparison />
        </div>
      </section>

      <Footer />
    </div>
  );
}
