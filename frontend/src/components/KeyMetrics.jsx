import React from 'react';

const metrics = [
  { value: '1,300,000', label: 'Italian NEETs (15-29)', color: 'var(--color-danger)', icon: '📊' },
  { value: '19.8%', label: 'Implicit Dropouts (INVALSI)', color: 'var(--color-warning)', icon: '📉' },
  { value: '3.9%', label: 'GDP on Education (EU avg: 4.7%)', color: 'var(--color-danger)', icon: '💰' },
  { value: '~€1B', label: 'Shadow Tutoring Economy', color: 'var(--color-warning)', icon: '👻' },
  { value: '4.5 yrs', label: 'Avg. Wait for Stable Contract (South)', color: 'var(--color-accent)', icon: '⏳' },
  { value: '67.4%', label: 'Youth Living with Parents (18-34)', color: 'var(--color-accent)', icon: '🏠' },
];

const KeyMetrics = () => (
  <section className="section section-metrics">
    <div className="container">
      <div className="section-header">
        <span className="section-tag">The Numbers</span>
        <h2>Italy's Educational Crisis at a Glance</h2>
      </div>
      <div className="key-metrics-grid">
        {metrics.map((m, i) => (
          <div key={i} className="key-metric" style={{ '--metric-color': m.color }}>
            <span className="key-metric-icon">{m.icon}</span>
            <span className="key-metric-value">{m.value}</span>
            <span className="key-metric-label">{m.label}</span>
          </div>
        ))}
      </div>
    </div>
  </section>
);

export default KeyMetrics;
