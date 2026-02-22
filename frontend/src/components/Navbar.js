// components/Navbar.js
import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-left">
        <h2 className="logo"><Link to="/">SalesMind AI</Link></h2>
        <ul className="nav-links">
          <li><Link to="/leads">Leads</Link></li>
          <li><Link to="/b2b">B2B</Link></li>
          <li><Link to="/b2c">B2C</Link></li>
          <li><Link to="/dashboard">Dashboard</Link></li>
           <Link to="/pricing">Pricing</Link>
        </ul>
      </div>

      <div className="nav-right">
        <Link to="/login" className="nav-link">Sign In</Link>
        <Link to="/signup" className="btn nav-cta">Get Started</Link>
      </div>
    </nav>
  );
}

export default Navbar;
