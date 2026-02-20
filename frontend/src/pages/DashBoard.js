import React, { useState, useEffect, useRef } from "react"; // Added useRef
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import Navbar from "../components/Navbar";
import "./DashBoard.css";

export default function Dashboard() {
  const [stats, setStats] = useState({
    total_leads: 0, b2b_count: 0, b2c_count: 0, emails_sent: 0, new_leads: 0
  });

  const location = useLocation();
  const navigate = useNavigate();
  const paymentProcessed = useRef(false); // Prevents double activation

  const userObj = JSON.parse(localStorage.getItem("user") || "{}");
  const firstName = userObj.name || localStorage.getItem("userName") || "User";

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/leads/stats")
      .then(res => setStats(res.data))
      .catch(err => console.error("Error fetching stats:", err));
  }, []);

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const sessionId = queryParams.get("session_id");
    const userId = queryParams.get("user_id");
    const plan = queryParams.get("plan");

    // Only run if we have all params and haven't already run in this session
    if (sessionId && userId && plan && !paymentProcessed.current) {
      paymentProcessed.current = true; // Mark as started

      const activateSubscription = async () => {
        try {
          console.log("Confirming payment for User:", userId, "Plan:", plan);
          
          const response = await axios.post("http://localhost:5000/api/payments/confirm", {
            user_id: parseInt(userId),
            plan: plan
          });

          if (response.status === 200) {
            alert("Subscription Activated! You now have access to more leads. ✅");
            
            // 1. Update the local user object so the UI knows they are 'paid'
            const updatedUser = { ...userObj, is_paid: true };
            localStorage.setItem("user", JSON.stringify(updatedUser));
            
            // 2. Clean URL so refreshing the page doesn't trigger the logic again
            navigate("/dashboard", { replace: true });
          }
        } catch (error) {
          console.error("Error activating subscription:", error);
          alert("There was an issue activating your plan. Please contact support.");
        }
      };

      activateSubscription();
    }
  }, [location, navigate, userObj]);

  return (
    <div className="dashboard-wrapper">
      <Navbar />
      <div className="dashboard-container">
        <h1>Welcome Back, {firstName} 👋</h1>
        
        {/* Analytics Grid */}
        <div className="analytics-grid">
          <div className="stat-card">
            <span className="stat-label">Total Leads</span>
            <p className="stat-value">{stats.total_leads}</p>
            <span className="stat-footer" style={{ color: "#34d399" }}>↑ Generated Automatically</span>
          </div>
          
          <div className="stat-card">
            <span className="stat-label">Personalized Emails</span>
            <p className="stat-value" style={{ color: "#818cf8" }}>{stats.emails_sent}</p>
            <span className="stat-footer" style={{ color: "#818cf8" }}>AI Outreach Active</span>
          </div>

          <div className="stat-card">
            <span className="stat-label">B2B vs B2C</span>
            <p className="stat-value" style={{ fontSize: "1.8rem" }}>
              {stats.b2b_count} <span style={{color: 'rgba(255,255,255,0.1)'}}>/</span> {stats.b2c_count}
            </p>
            <span className="stat-footer" style={{ color: "#94a3b8" }}>Segmented Leads</span>
          </div>
        </div>

        {/* Actions Grid */}
        <div className="actions-section">
          <h3>Next Steps for You</h3>
          <div className="actions-grid">
            <button className="action-btn" onClick={() => navigate('/b2b')}>
              <span style={{fontSize: '1.5rem'}}>🔍</span> Start a guided B2B search
            </button>
            <button className="action-btn" onClick={() => navigate('/b2c')}>
              <span style={{fontSize: '1.5rem'}}>✨</span> Generate B2C Consumer Leads
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}