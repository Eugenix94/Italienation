import React from 'react';

const Footer = () => (
  <footer className="site-footer">
    <div className="container">
      <div className="footer-grid">
        <div className="footer-col">
          <h4>Italienation</h4>
          <p>An open-research project mapping systemic inequality in the Italian educational pipeline using the Origin–Education–Destination (OED) framework.</p>
        </div>
        <div className="footer-col">
          <h4>Data Sources</h4>
          <ul>
            <li>ISTAT – Istituto Nazionale di Statistica</li>
            <li>INVALSI – National Assessment Reports</li>
            <li>Eurostat – EU Statistical Office</li>
            <li>OECD – Education at a Glance</li>
            <li>Eurydice – European Commission</li>
            <li>AlmaDiploma / AlmaLaurea</li>
          </ul>
        </div>
        <div className="footer-col">
          <h4>Open Science</h4>
          <ul>
            <li><a href="https://github.com/Eugenix94/Italienation" target="_blank" rel="noopener noreferrer">GitHub Repository</a></li>
            <li><a href="https://osf.io/fh7qr/overview" target="_blank" rel="noopener noreferrer">OSF Public Project</a></li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom">
        <p>© 2026 Italienation Project · Released under CC-BY-4.0 · Data verified against official institutional sources</p>
      </div>
    </div>
  </footer>
);

export default Footer;
