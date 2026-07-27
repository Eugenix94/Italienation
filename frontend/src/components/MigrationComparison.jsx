import React from 'react';
import oedData from '../assets/oed_international_migration_calculator.json';

const MigrationComparison = () => {
  const countries = Object.entries(oedData.countries);

  return (
    <div className="migration">
      <div className="section-header">
        <span className="section-tag">Migration Thesis</span>
        <h2>What If You Migrated?</h2>
        <p>
          The same student profile — a <strong>dropout</strong> — experiences radically
          different life outcomes depending on the institutional design of the destination country.
          In Italy, it's a terminal condition. In Germany or the Nordics, it's a recoverable event.
        </p>
      </div>

      <div className="migration-grid">
        {countries.map(([name, data]) => {
          const dropout = data.outcomes.dropout;
          return (
            <div key={name} className={`migration-card ${name === 'Italy' ? 'migration-card-danger' : 'migration-card-safe'}`}>
              <div className="migration-card-header">
                <span className="migration-flag">
                  {name === 'Italy' ? '🇮🇹' : name === 'Germany' ? '🇩🇪' : '🇸🇪'}
                </span>
                <h3>{name}</h3>
                <span className={`migration-badge ${data.diploma_strictly_required_for_uni ? 'badge-danger' : 'badge-success'}`}>
                  {data.diploma_strictly_required_for_uni ? 'Closed System' : 'Open Pathways'}
                </span>
              </div>
              <p className="migration-system">{data.system_type}</p>
              <div className="migration-stats">
                <div className="migration-stat">
                  <span className="stat-val" style={{ color: dropout.prob_neet > 0.3 ? 'var(--color-danger)' : 'var(--color-success)' }}>
                    {(dropout.prob_neet * 100).toFixed(0)}%
                  </span>
                  <span className="stat-lbl">NEET Risk</span>
                </div>
                <div className="migration-stat">
                  <span className="stat-val" style={{ color: dropout.prob_tertiary_access < 0.1 ? 'var(--color-danger)' : 'var(--color-success)' }}>
                    {(dropout.prob_tertiary_access * 100).toFixed(0)}%
                  </span>
                  <span className="stat-lbl">Uni Access</span>
                </div>
                <div className="migration-stat">
                  <span className="stat-val">€{dropout.expected_monthly_income_eur?.toLocaleString()}</span>
                  <span className="stat-lbl">Income</span>
                </div>
              </div>
              <p className="migration-narrative">{dropout.narrative}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default MigrationComparison;
