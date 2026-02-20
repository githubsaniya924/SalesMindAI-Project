import { v4 as uuidv4 } from "uuid";

import { useState, useEffect } from "react";
import axios from "axios";

export default function B2BGeneratorPage() {

  // 🔐 SESSION ID (not a hook → OK here)
  let sessionId = localStorage.getItem("anon_session_id");

  if (!sessionId) {
    sessionId = uuidv4();
    localStorage.setItem("anon_session_id", sessionId);
  }

  // ---------------- STATES ----------------
  const [industry, setIndustry] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const [showSignupPopup, setShowSignupPopup] = useState(false);
  const [trialCount, setTrialCount] = useState(
    Number(localStorage.getItem("trialCount")) || 0
  );

  // ✅ ADD THIS STATE HERE
  const [leads, setLeads] = useState([]);

  // ---------------- EFFECT ----------------
  // ✅ ADD useEffect HERE (after useState)
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/leads/by-session", {
      params: { session_id: sessionId }
    }).then(res => setLeads(res.data));
  }, [sessionId]);

  // ---------------- FUNCTIONS ----------------
  const startGeneration = async () => {
    if (!industry) {
        setStatus("Please enter an industry.");
        return;
    }

    const token = localStorage.getItem("access_token");
    
    // 🛡️ Create config dynamically to avoid sending "Bearer null"
    const config = {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
    };

    try {
        setLoading(true);
        setStatus("");

        const res = await axios.post(
            "http://127.0.0.1:5000/api/leads/generate_on_demand",
            {
                industry,
                session_id: sessionId,
                anonymous_trials: trialCount // 👈 Pass this for the backend check
            },
            config // 👈 Pass the dynamic headers
        );

        // ... rest of your success logic
      const newCount = trialCount + 1;
      setTrialCount(newCount);
      localStorage.setItem("trialCount", newCount);

      setStatus(`Task started! Task ID: ${res.data.task_id}`);
      setTimeout(() => {
      axios.get("http://127.0.0.1:5000/api/leads/by-session", {
        params: { session_id: sessionId }
      }).then(res => setLeads(res.data));
    }, 3000);

    } catch (err) {
      if (err.response?.status === 403) {
        localStorage.setItem("signup_reason", "trial_exhausted");
        setShowSignupPopup(true);
      } else {
        setStatus("Failed to start lead generation.");
      }
    } finally {
      setLoading(false);
    }
  };

  // ---------------- UI ----------------
  return (
    <div style={{ padding: "40px", maxWidth: "500px" }}>
      <h2>B2B Lead Generation</h2>

      <input
        type="text"
        placeholder="Industry (software, finance...)"
        value={industry}
        onChange={(e) => setIndustry(e.target.value)}
      />

      <button onClick={startGeneration} disabled={loading}>
        {loading ? "Generating..." : "Generate Leads"}
      </button>

     
      {status && <p>{status}</p>}

      <button onClick={() => {
  window.open(
    `http://127.0.0.1:5000/api/leads/download?session_id=${sessionId}`
  );
}}>
  Download Leads
</button>


      {/* 🔽 LEADS LIST (15 max + scroll) */}
     <div style={{
  maxHeight: "400px",
  overflowY: "auto",
  border: "1px solid #ddd",
  marginTop: "20px",
  padding: "10px"
}}>
  {leads.slice(0, 15).map((lead, i) => (
    <div key={i} style={{ padding: "8px", borderBottom: "1px solid #eee" }}>
      <b>{lead.email}</b>
      <div>{lead.company}</div>
      <small>{lead.job_title}</small>
    </div>
  ))}
</div>


      {/* 🔔 SIGNUP POPUP */}
      {showSignupPopup && (
        <div className="popup-overlay">
          <div className="popup-card">
            <h3>Free trials completed 🚀</h3>
            <p>You have used all 3 free B2B lead generations.</p>

            <button onClick={() => {
  localStorage.setItem("signup_reason", "trial_exhausted");
  window.location.href = "/signup";
}}>
  Sign Up to Continue
</button>

            <button onClick={() => setShowSignupPopup(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>

    
  );
}
