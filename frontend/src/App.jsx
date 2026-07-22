import React, { useRef, createRef } from 'react';
import { useIntersectionObserver } from './hooks/useIntersectionObserver';
import ScrollyVisual from './components/ScrollyVisual';

function App() {
  const stepCount = 5;
  const refs = useRef([...Array(stepCount)].map(() => createRef()));
  const activeIndex = useIntersectionObserver(refs.current, { threshold: 0.6 });

  return (
    <div className="App">
      <header style={{ padding: 'var(--section-padding)', textAlign: 'center' }}>
        <h1>The Black Box</h1>
        <p style={{ margin: '0 auto', fontSize: '1.5rem', color: 'var(--text-secondary)' }}>
          The Machinery of Inequality in the Italian Educational System.
        </p>
      </header>

      <section className="scrolly-container">
        
        {/* Left Column: The Narrative Text */}
        <div className="scrolly-text">
          
          <div ref={refs.current[0]} className={`scrolly-step glass-panel ${activeIndex === 0 ? 'is-active' : ''}`} style={{ marginBottom: '50vh' }}>
            <h2>1. The Precursor (Age 0)</h2>
            <p>
              The cybernetic pipeline of inequality does not begin at age 14; it begins at birth. 
              Recent ISTAT data reveals a devastating structural gap in early childhood education (Asili Nido).
            </p>
            <span className="stat-highlight north">39% Coverage in the North</span>
            <span className="stat-highlight south">19% Coverage in the South</span>
            <p>Southern children enter primary school already cognitively and infrastructurally disadvantaged. The tracking doesn't create the inequality; it formalizes a socio-economic gap that began at Age 0.</p>
          </div>

          <div ref={refs.current[1]} className={`scrolly-step glass-panel ${activeIndex === 1 ? 'is-active' : ''}`} style={{ marginBottom: '50vh' }}>
            <h2>2. The Tripartite Bifurcation (Age 14)</h2>
            <p>
              The true systemic filter occurs at age 14. The bifurcation of human capital is the legal DNA of the Italian state, architected by the Riforma Gentile (1923).
            </p>
            <p>The Modello 4+2 (Legge 121/2024) further compresses vocational schooling from 5 to 4 years, cementing the <span style={{color: 'var(--accent-liceo)'}}>Liceo</span> as a shielded path to university while forcibly exposing <span style={{color: 'var(--accent-professionale)'}}>Vocational</span> students to immediate local labor market volatilities.</p>
          </div>

          <div ref={refs.current[2]} className={`scrolly-step glass-panel ${activeIndex === 2 ? 'is-active' : ''}`} style={{ marginBottom: '50vh' }}>
            <h2>3. The Economic Paywall</h2>
            <p>While public education is legally "free," a hard economic paywall exists at the classroom level.</p>
            <span className="stat-highlight" style={{color: '#ff4444'}}>€1,200+ Annually</span>
            <p>Families spend an average of €591 on mandatory textbooks and €647 on materials. This out-of-pocket cost is a devastating financial barrier that state aid (Bonus Libri) routinely fails to cover.</p>
          </div>

          <div ref={refs.current[3]} className={`scrolly-step glass-panel ${activeIndex === 3 ? 'is-active' : ''}`} style={{ marginBottom: '50vh' }}>
            <h2>4. The Shadow Economy</h2>
            <p>
              Instead of immediate grade retention, the system utilizes the Debito Formativo (educational debt). This activates a massive cybernetic shadow economy.
            </p>
            <span className="stat-highlight" style={{color: '#ffd700'}}>~€1 Billion Annually</span>
            <p>High-SES families buy their way out of the debt via private summer tutoring (ripetizioni), while low-SES students face recovery exams unsupported. If they fail, they use Scuole Paritarie as a "pay-to-win" bypass valve.</p>
          </div>

          <div ref={refs.current[4]} className={`scrolly-step glass-panel ${activeIndex === 4 ? 'is-active' : ''}`} style={{ marginBottom: '10vh' }}>
            <h2>5. The Output: Dual Brain Drain</h2>
            <p>
              Surviving the filters and attaining a diploma is often a false "Success State."
            </p>
            <p>AlmaDiploma data reveals a structural Diploma-to-NEET pipeline for vocational students. For the high-performing elite, the cybernetic output is territorial extraction: <br/><br/>
            <strong>Internal Hemorrhaging</strong> (35,000 top students moving South-to-North) and <strong>International Brain Drain</strong> (emigrating to Northern Europe for high wage premiums).</p>
          </div>

        </div>

        {/* Right Column: The Dynamic Visualizer */}
        <div className="scrolly-visual">
          <ScrollyVisual activeIndex={activeIndex} />
        </div>

      </section>
    </div>
  );
}

export default App;
