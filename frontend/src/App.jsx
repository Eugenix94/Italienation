import React, { useState } from 'react';
import OEDSimulator from './components/OEDSimulator';
import EurydiceChart from './components/EurydiceChart';
import KeyMetrics from './components/KeyMetrics';
import MigrationComparison from './components/MigrationComparison';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      {/* Hero */}
      <header className="hero">
        <div className="hero-glow" />
        <div className="hero-content">
          <span className="hero-badge">Open Research · Phase 1</span>
          <h1>Italienation</h1>
          <p className="hero-subtitle">
            The Origin–Education–Destination Framework:
            <br />How Italy's Education System Manufactures Inequality
          </p>
          <div className="hero-stats">
            <div className="hero-stat">
              <span className="hero-stat-value">19%</span>
              <span className="hero-stat-label">NEET Rate (15-29)</span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat">
              <span className="hero-stat-value">€48B</span>
              <span className="hero-stat-label">Annual Human Capital Loss</span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat">
              <span className="hero-stat-value">Age 14</span>
              <span className="hero-stat-label">Tracking Age (EU Outlier)</span>
            </div>
          </div>
          <a href="#simulator" className="hero-cta">Explore the OED Simulator ↓</a>
        </div>
      </header>

      {/* Intro Section */}
      <section className="section section-intro">
        <div className="container">
          <div className="intro-grid">
            <div className="intro-text">
              <h2>The Black Box</h2>
              <p>
                In sociology, the <strong>OED</strong> framework models how a student's social
                <em> Origin</em> (SES) filters through the <em>Education</em> system
                to determine their final socio-economic <em>Destination</em>.
              </p>
              <p>
                Italy's system acts as a <strong>rigid sorting mechanism</strong>. Rather than
                compensating for a disadvantaged Origin, early tracking at age 14 and punitive
                grading calcify it — ensuring that low-SES students are funneled towards NEET
                status or precarious labor.
              </p>
              <p>
                By contrast, systems like Germany's <em>Dual VET</em> and the Nordic
                <em> Comprehensive Model</em> use institutional safety nets to decouple
                Origin from Destination, treating educational failure as an <strong>event</strong>,
                not a <strong>terminal condition</strong>.
              </p>
            </div>
            <div className="intro-visual">
              <div className="oed-diagram">
                <div className="oed-node oed-origin">
                  <span className="oed-node-icon">🏠</span>
                  <span className="oed-node-label">Origin</span>
                  <span className="oed-node-desc">Family SES</span>
                </div>
                <div className="oed-arrow">→</div>
                <div className="oed-node oed-education">
                  <span className="oed-node-icon">🏫</span>
                  <span className="oed-node-label">Education</span>
                  <span className="oed-node-desc">System Filter</span>
                </div>
                <div className="oed-arrow">→</div>
                <div className="oed-node oed-destination">
                  <span className="oed-node-icon">🎯</span>
                  <span className="oed-node-label">Destination</span>
                  <span className="oed-node-desc">Life Outcome</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Metrics */}
      <KeyMetrics />

      {/* OED Simulator */}
      <section id="simulator" className="section section-simulator">
        <div className="container">
          <OEDSimulator />
        </div>
      </section>

      {/* Eurydice Comparison */}
      <section className="section section-eurydice">
        <div className="container">
          <EurydiceChart />
        </div>
      </section>

      {/* Migration Comparison */}
      <section className="section section-migration">
        <div className="container">
          <MigrationComparison />
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
