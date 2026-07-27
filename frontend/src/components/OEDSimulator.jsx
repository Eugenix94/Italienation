import React, { useState } from 'react';
import oedData from '../assets/oed_international_migration_calculator.json';

const OEDSimulator = () => {
  const [country, setCountry] = useState('Italy');
  const [profile, setProfile] = useState('dropout');

  const countryData = oedData.countries[country];
  const outcomes = countryData.outcomes[profile];

  return (
    <div className="oed-simulator glass-panel">
      <h2>OED International Migration Simulator</h2>
      <p>Analyze how a student's Origin (SES) and Education (Track) dictates their Destination across different national systems.</p>
      
      <div className="simulator-controls">
        <div className="control-group">
          <label>Select Destination Country:</label>
          <select value={country} onChange={(e) => setCountry(e.target.value)} className="glass-select">
            {Object.keys(oedData.countries).map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
        <div className="control-group">
          <label>Select Student Profile:</label>
          <select value={profile} onChange={(e) => setProfile(e.target.value)} className="glass-select">
            {Object.keys(oedData.countries['Italy'].outcomes).map(p => (
              <option key={p} value={p}>{p.replace('_', ' ').toUpperCase()}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="simulator-results">
        <h3>System Context: {country}</h3>
        <p className="system-type">{countryData.system_type}</p>
        
        <div className="metrics-grid">
          <div className="metric-card" style={{ borderColor: outcomes.prob_neet > 0.4 ? 'var(--accent-professionale)' : 'var(--accent-north)' }}>
            <h4>NEET Risk</h4>
            <div className="metric-value">{(outcomes.prob_neet * 100).toFixed(0)}%</div>
          </div>
          
          <div className="metric-card" style={{ borderColor: outcomes.prob_tertiary_access < 0.1 ? 'var(--accent-professionale)' : 'var(--accent-liceo)' }}>
            <h4>Tertiary Access</h4>
            <div className="metric-value">{(outcomes.prob_tertiary_access * 100).toFixed(0)}%</div>
          </div>

          <div className="metric-card" style={{ borderColor: 'var(--accent-tecnico)' }}>
            <h4>Social Mobility Index</h4>
            <div className="metric-value">{outcomes.social_mobility_index} / 10</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OEDSimulator;
