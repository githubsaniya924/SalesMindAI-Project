// components/Home.js
import "./Home.css";
import Navbar from "./Navbar";
import Footer from "./Footer";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faEnvelope, 
  faCommentDots, 
  faMagnifyingGlass, 
  faDatabase, 
  faMicrochip 
} from '@fortawesome/free-solid-svg-icons';

function Home() {
  return (
    <div className="glass-theme">
      
      {/* NAVBAR */}
      <Navbar />

      {/* ================= HERO SECTION ================= */}
      <section className="hero-section">
        
        {/* Background Decorative Code */}
        <div className="bg-code-snippet top-right">
          <code>
            {`regsties: (2355s = 180%, satarat=111...)`}<br/>
            {`fngstiet: (2sstes=1008...)`}
          </code>
        </div>

        <div className="bg-code-snippet bottom-left">
          <code>
            {`rrgtetias: badercp=flter=180%...`}<br/>
            {`hensbiut=00.0;`}
          </code>
        </div>

        <div className="container hero-grid">

          {/* LEFT CONTENT */}
          <div className="hero-text">
            <h1 className="display-bold">
              Your buyers hate <br />
              <span>cold sales.</span>
            </h1>

            <p className="hero-desc">
              AI-powered lead generation, outreach, and analytics —
              built to help you close smarter, faster.
            </p>

            <div className="hero-btns">
              <Link to="/signup" className="btn purple-btn">
                Start Free
              </Link>

              <Link to="/dashboard" className="btn glass-btn">
                View Dashboard
              </Link>
            </div>
          </div>

          {/* RIGHT VISUAL */}
          <div className="hero-visual-container">

            <div className="glass-icon main-envelope float">
              <FontAwesomeIcon icon={faEnvelope} size="3x" color="#b496ff" />
            </div>

            <div className="glass-icon chat float-alt">
              <FontAwesomeIcon icon={faCommentDots} />
            </div>

            <div className="glass-icon search float">
              <FontAwesomeIcon icon={faMagnifyingGlass} />
            </div>

          </div>
        </div>
      </section>

      {/* ================= STATS SECTION ================= */}
      <section className="stats-strip">
        <div className="container stats-grid">
          <div className="stat-item">
            <span className="stat-val">75%</span>
            <p>more meetings booked</p>
          </div>

          <div className="stat-item">
            <span className="stat-val">70 hours</span>
            <p>saved per week</p>
          </div>

          <div className="stat-item">
            <span className="stat-val">50%</span>
            <p>cost savings</p>
          </div>
        </div>
      </section>

      {/* ================= FEATURE SECTION ================= */}
      <section className="feature-block">
        <div className="container split-grid">

          {/* FEATURE VISUAL */}
          <div className="feature-visual-placeholder glass-card">
            <div className="workflow-mockup">
              <div className="node glass-node">Enrich Data</div>
              <div className="node glass-node">AI Sequence</div>
            </div>
          </div>

          {/* FEATURE TEXT */}
          <div className="feature-text">
            <span className="label">BUILD</span>
            <h2>Launch personalized campaigns in minutes</h2>
            <p>
              Instantly pinpoint the right buyers using simple AI prompts
              to automate full-funnel campaigns.
            </p>

            <ul className="feature-list">
              <li>
                <FontAwesomeIcon icon={faDatabase} className="list-icon" />
                <span><strong>Real-time data</strong> to pinpoint perfect leads</span>
              </li>

              <li>
                <FontAwesomeIcon icon={faMicrochip} className="list-icon" />
                <span><strong>AI Assistant</strong> to build lists with natural language</span>
              </li>

              <li>
                <FontAwesomeIcon icon={faEnvelope} className="list-icon" />
                <span><strong>Deliverability tools</strong> to keep your domain safe</span>
              </li>
            </ul>
          </div>

        </div>
      </section>

      {/* ================= CTA SECTION ================= */}
      <section className="cta-section">
        <div className="container">
          <h2>Start selling smarter today</h2>
          <Link to="/b2b" className="btn purple-btn large">
            Generate B2B Leads
          </Link>
        </div>
      </section>

      {/* FOOTER */}
      <Footer />

    </div>
  );
}

export default Home;