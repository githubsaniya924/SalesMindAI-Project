// components/Footer.js
import "./Footer.css";
import { Link } from "react-router-dom";

function Footer() {
  return (
    <footer className="main-footer">
      <div className="container footer-grid">
        {/* Brand Section */}
        <div className="footer-brand">
          <div className="brand-icon">
            {/* Replace with your logo SVG */}
            <svg viewBox="0 0 100 100" className="footer-logo-svg">
               <path d="M50 0 L60 40 L100 50 L60 60 L50 100 L40 60 L0 50 L40 40 Z" fill="currentColor" />
            </svg>
          </div>
          <div className="brand-legal">
            <p>SalesMind AI © 2026</p>
            <Link to="/privacy">Privacy Policy</Link>
            <Link to="/terms">Terms</Link>
            <Link to="/do-not-sell">Don't Sell My Info</Link>
          </div>
        </div>

        {/* Links Columns */}
        <div className="footer-links-wrapper">
          <div className="footer-col">
            <h4>Get started</h4>
            <Link to="/signup">Sign up for free</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/demo">Request a demo</Link>
            
            <h4 className="mt-2">Use Cases</h4>
            <Link to="/b2b">B2B Database</Link>
            <Link to="/scoring">Lead Scoring</Link>
            <Link to="/outreach">Sales Engagement</Link>
          </div>

          <div className="footer-col">
            <h4>Solutions</h4>
            <Link to="/outbound">Outbound</Link>
            <Link to="/inbound">Inbound</Link>
            <Link to="/enrichment">Data Enrichment</Link>
            
            <h4 className="mt-2">Resources</h4>
            <Link to="/academy">Academy</Link>
            <Link to="/insights">Insights</Link>
            <Link to="/docs">API Docs ↗</Link>
          </div>

          <div className="footer-col">
            <h4>Platform</h4>
            <Link to="/data">SalesMind Data</Link>
            <Link to="/ai">SalesMind AI</Link>
            <Link to="/integrations">Integrations</Link>
            
            <h4 className="mt-2">Company</h4>
            <Link to="/about">About Us</Link>
            <Link to="/careers">Careers</Link>
            <Link to="/contact">Contact Us</Link>
          </div>

          <div className="footer-col">
            <h4>Prospect anywhere</h4>
            <p className="small-text">Get verified emails and phone numbers instantly while you work.</p>
            <Link to="/extension" className="btn-footer-outline">Chrome Extension</Link>
            
            <h4 className="mt-2">Social</h4>
            <div className="social-links">
                <Link to="#">LinkedIn</Link>
                <Link to="#">YouTube</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;