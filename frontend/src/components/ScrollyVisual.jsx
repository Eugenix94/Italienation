import React from 'react';

const ScrollyVisual = ({ activeIndex }) => {
  
  // Define visual states for each step
  const renderVisual = () => {
    switch(activeIndex) {
      case 0:
        return (
          <div className="viz-container">
            <div style={{ position: 'absolute', top: '20%', left: '30%', textAlign: 'center' }}>
              <div style={{ width: '80px', height: '80px', borderRadius: '50%', background: 'var(--accent-north)', margin: '0 auto', opacity: 0.8 }}></div>
              <p style={{ marginTop: '1rem', fontWeight: 'bold' }}>North (39%)</p>
            </div>
            <div style={{ position: 'absolute', bottom: '20%', right: '30%', textAlign: 'center' }}>
              <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--accent-south)', margin: '0 auto', opacity: 0.8 }}></div>
              <p style={{ marginTop: '1rem', fontWeight: 'bold' }}>South (19%)</p>
            </div>
            <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: '100%', height: '2px', background: 'rgba(255,255,255,0.1)' }}></div>
            <h3 style={{ position: 'absolute', top: '10%', left: '10%', opacity: 0.5 }}>Asili Nido Coverage</h3>
          </div>
        );
      case 1:
        return (
          <div className="viz-container">
            <svg width="100%" height="100%" viewBox="0 0 400 400">
              <path d="M 50 200 C 150 200, 200 100, 350 100" fill="transparent" stroke="var(--accent-liceo)" strokeWidth="8" strokeLinecap="round" style={{transition: 'all 1s'}}/>
              <path d="M 50 200 C 150 200, 200 200, 350 200" fill="transparent" stroke="var(--accent-tecnico)" strokeWidth="8" strokeLinecap="round" style={{transition: 'all 1s'}}/>
              <path d="M 50 200 C 150 200, 200 300, 350 300" fill="transparent" stroke="var(--accent-professionale)" strokeWidth="8" strokeLinecap="round" style={{transition: 'all 1s'}}/>
              <circle cx="50" cy="200" r="12" fill="white" />
              <text x="360" y="105" fill="var(--text-primary)" fontSize="14">Liceo</text>
              <text x="360" y="205" fill="var(--text-primary)" fontSize="14">Tecnico</text>
              <text x="360" y="305" fill="var(--text-primary)" fontSize="14">Professionale</text>
            </svg>
             <h3 style={{ position: 'absolute', top: '10%', left: '10%', opacity: 0.5 }}>The Tripartite Filter</h3>
          </div>
        );
      case 2:
        return (
          <div className="viz-container">
             <div className="glass-panel" style={{ width: '60%', textAlign: 'left', padding: '2rem' }}>
                <h3 style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1rem' }}>Family Receipt</h3>
                <div style={{ display: 'flex', justifyContent: 'space-between', margin: '1rem 0' }}>
                  <span>Mandatory Textbooks</span>
                  <span>€ 591.44</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', margin: '1rem 0' }}>
                  <span>Corredo / Materials</span>
                  <span>€ 647.00</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', margin: '1rem 0', fontWeight: 'bold', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1rem', color: '#ff4444' }}>
                  <span>TOTAL COST</span>
                  <span>€ 1,238.44</span>
                </div>
             </div>
          </div>
        );
      case 3:
        return (
          <div className="viz-container">
            <div style={{ position: 'absolute', top: '30%', left: '20%', width: '150px', height: '150px', border: '2px solid rgba(255,255,255,0.1)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <span style={{ textAlign: 'center', opacity: 0.7 }}>Debito<br/>Formativo</span>
            </div>
            <div style={{ position: 'absolute', top: '20%', right: '20%', width: '100px', height: '100px', background: 'rgba(255, 215, 0, 0.2)', border: '2px solid #ffd700', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', animation: 'pulse 2s infinite' }}>
              <span style={{ textAlign: 'center', fontWeight: 'bold', color: '#ffd700' }}>Ripetizioni<br/>(€1B)</span>
            </div>
            <svg width="100%" height="100%" style={{ position: 'absolute', top: 0, left: 0, zIndex: -1 }}>
               <path d="M 170 150 Q 250 50, 300 120" fill="transparent" stroke="#ffd700" strokeWidth="4" strokeDasharray="5,5" />
            </svg>
          </div>
        );
      case 4:
        return (
          <div className="viz-container">
            <svg width="100%" height="100%">
              {/* Internal Drain */}
              <path d="M 200 300 Q 150 150, 100 100" fill="transparent" stroke="var(--accent-liceo)" strokeWidth="3" opacity="0.6"/>
              <path d="M 200 300 Q 250 150, 300 100" fill="transparent" stroke="var(--accent-liceo)" strokeWidth="3" opacity="0.6"/>
              {/* International Drain */}
              <path d="M 100 100 Q 150 50, 200 0" fill="transparent" stroke="#00ff00" strokeWidth="3" strokeDasharray="4,4" opacity="0.8"/>
              <path d="M 300 100 Q 250 50, 200 0" fill="transparent" stroke="#00ff00" strokeWidth="3" strokeDasharray="4,4" opacity="0.8"/>
              
              <circle cx="200" cy="300" r="30" fill="var(--bg-glass)" stroke="rgba(255,255,255,0.2)"/>
              <text x="200" y="305" fill="white" textAnchor="middle" fontSize="12">South</text>

              <circle cx="100" cy="100" r="25" fill="var(--bg-glass)" stroke="rgba(255,255,255,0.2)"/>
              <text x="100" y="105" fill="white" textAnchor="middle" fontSize="12">North</text>
              
              <circle cx="300" cy="100" r="25" fill="var(--bg-glass)" stroke="rgba(255,255,255,0.2)"/>
              <text x="300" y="105" fill="white" textAnchor="middle" fontSize="12">North</text>
            </svg>
            <h3 style={{ position: 'absolute', bottom: '10%', left: '10%', opacity: 0.5 }}>Territorial Extraction</h3>
          </div>
        );
      default:
        return <div className="viz-container"><p>Scroll down...</p></div>;
    }
  };

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center' }}>
      {renderVisual()}
    </div>
  );
};

export default ScrollyVisual;
