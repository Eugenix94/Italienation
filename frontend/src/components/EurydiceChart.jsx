import React from 'react';
import eurydiceData from '../assets/master_eurydice_comparison.json';

const EurydiceChart = () => {
  // Sort data by TrackingAge
  const sortedData = [...eurydiceData]
    .filter(d => d.TrackingAge > 0)
    .sort((a, b) => a.TrackingAge - b.TrackingAge);

  return (
    <div className="eurydice-chart glass-panel">
      <h2>The European Tracking Divide</h2>
      <p>Age of first definitive educational selection (Source: Eurydice 2024-2025)</p>
      
      <div className="chart-container">
        {sortedData.map((country, idx) => {
          // Normalize bar width based on a max age of 18
          const barWidth = (country.TrackingAge / 18) * 100;
          const isItaly = country.CountryCode === 'IT';
          
          return (
            <div key={idx} className="chart-row">
              <div className="chart-label">{country.Country}</div>
              <div className="chart-bar-wrapper">
                <div 
                  className="chart-bar" 
                  style={{ 
                    width: `${barWidth}%`, 
                    backgroundColor: isItaly ? 'var(--accent-professionale)' : 'var(--accent-liceo)'
                  }}
                >
                  <span className="chart-value">{country.TrackingAge} yrs</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      <div className="chart-insight">
        <strong>Insight:</strong> Italy is a severe outlier, forcing definitive socio-economic sorting at age 14, whereas comprehensive systems (Nordics) delay this until 16 or later.
      </div>
    </div>
  );
};

export default EurydiceChart;
