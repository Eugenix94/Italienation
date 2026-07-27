import React, { useState, useEffect } from 'react';
import oedData from '../assets/oed_international_migration_calculator.json';

const PROFILE_ICONS = {
  dropout: '🚫',
  vocational: '🔧',
  technical: '⚙️',
  liceo: '🎓',
};

const OEDSimulator = () => {
  const [country, setCountry] = useState('Italy');
  const [profile, setProfile] = useState('dropout');
  const [animate, setAnimate] = useState(false);

  const countryData = oedData.countries[country];
  const outcomes = countryData?.outcomes?.[profile];

  useEffect(() => {
    setAnimate(false);
    const timer = setTimeout(() => setAnimate(true), 50);
    return () => clearTimeout(timer);
  }, [country, profile]);

  if (!outcomes) return null;

  const neetColor = outcomes.prob_neet > 0.4 ? 'var(--color-danger)' : outcomes.prob_neet > 0.2 ? 'var(--color-warning)' : 'var(--color-success)';
  const tertiaryColor = outcomes.prob_tertiary_access < 0.1 ? 'var(--color-danger)' : outcomes.prob_tertiary_access < 0.3 ? 'var(--color-warning)' : 'var(--color-success)';
  const mobilityColor = outcomes.social_mobility_index < 4 ? 'var(--color-danger)' : outcomes.social_mobility_index < 6 ? 'var(--color-warning)' : 'var(--color-success)';

  return (
    <div className="simulator">
      <div className="section-header">
        <span className="section-tag">Interactive Tool</span>
        <h2>OED International Migration Simulator</h2>
        <p>Select a student profile and destination country to see how institutional design shapes life outcomes.</p>
      </div>

      <div className="simulator-controls">
        <div className="control-group">
          <label>Student Profile</label>
          <div className="profile-selector">
            {Object.entries(countryData.outcomes).map(([key, val]) => (
              <button
                key={key}
                className={`profile-btn ${profile === key ? 'active' : ''}`}
                onClick={() => setProfile(key)}
              >
                <span className="profile-icon">{PROFILE_ICONS[key]}</span>
                <span className="profile-name">{val.label.split('(')[0].trim()}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="control-group">
          <label>Destination Country</label>
          <div className="country-selector">
            {Object.keys(oedData.countries).map(c => (
              <button
                key={c}
                className={`country-btn ${country === c ? 'active' : ''}`}
                onClick={() => setCountry(c)}
              >
                {c === 'Italy' ? '🇮🇹' : c === 'Germany' ? '🇩🇪' : '🇸🇪'} {c}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="simulator-system-badge">
        <span className={`badge ${countryData.diploma_strictly_required_for_uni ? 'badge-danger' : 'badge-success'}`}>
          {countryData.diploma_strictly_required_for_uni ? '🔒 Diploma Required for University' : '🔓 Alternative Pathways Available'}
        </span>
        <span className="system-label">{countryData.system_type}</span>
      </div>

      <div className={`metrics-grid ${animate ? 'animate-in' : ''}`}>
        <div className="metric-card" style={{ '--accent': neetColor }}>
          <div className="metric-ring">
            <svg viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
              <circle cx="60" cy="60" r="52" fill="none" stroke={neetColor} strokeWidth="8"
                strokeDasharray={`${outcomes.prob_neet * 327} 327`}
                strokeLinecap="round"
                style={{ transform: 'rotate(-90deg)', transformOrigin: 'center', transition: 'stroke-dasharray 1s ease-out' }}
              />
            </svg>
            <span className="metric-ring-value">{(outcomes.prob_neet * 100).toFixed(0)}%</span>
          </div>
          <h4>NEET Risk</h4>
          <p className="metric-subtitle">Not in Education, Employment, or Training</p>
        </div>

        <div className="metric-card" style={{ '--accent': tertiaryColor }}>
          <div className="metric-ring">
            <svg viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
              <circle cx="60" cy="60" r="52" fill="none" stroke={tertiaryColor} strokeWidth="8"
                strokeDasharray={`${outcomes.prob_tertiary_access * 327} 327`}
                strokeLinecap="round"
                style={{ transform: 'rotate(-90deg)', transformOrigin: 'center', transition: 'stroke-dasharray 1s ease-out' }}
              />
            </svg>
            <span className="metric-ring-value">{(outcomes.prob_tertiary_access * 100).toFixed(0)}%</span>
          </div>
          <h4>Tertiary Access</h4>
          <p className="metric-subtitle">Probability of reaching university</p>
        </div>

        <div className="metric-card" style={{ '--accent': mobilityColor }}>
          <div className="metric-ring">
            <svg viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
              <circle cx="60" cy="60" r="52" fill="none" stroke={mobilityColor} strokeWidth="8"
                strokeDasharray={`${(outcomes.social_mobility_index / 10) * 327} 327`}
                strokeLinecap="round"
                style={{ transform: 'rotate(-90deg)', transformOrigin: 'center', transition: 'stroke-dasharray 1s ease-out' }}
              />
            </svg>
            <span className="metric-ring-value">{outcomes.social_mobility_index}</span>
          </div>
          <h4>Mobility Index</h4>
          <p className="metric-subtitle">Social mobility score (0-10)</p>
        </div>

        <div className="metric-card metric-card-income" style={{ '--accent': 'var(--color-accent)' }}>
          <div className="income-value">€{outcomes.expected_monthly_income_eur?.toLocaleString()}</div>
          <h4>Expected Monthly Income</h4>
          <p className="metric-subtitle">Post-education earnings estimate</p>
        </div>
      </div>

      <div className="narrative-box">
        <h4>📖 System Analysis</h4>
        <p>{outcomes.narrative}</p>
      </div>

      {countryData.key_features && (
        <div className="features-list">
          <h4>Key System Features</h4>
          <ul>
            {countryData.key_features.map((f, i) => <li key={i}>{f}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
};

export default OEDSimulator;
