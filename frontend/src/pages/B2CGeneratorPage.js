import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import "./B2BandB2C.css";

export default function B2CGeneratorPage() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false); // Now used
  const [filter, setFilter] = useState("all");    // Now used

  useEffect(() => { fetchLeads(); }, []);

  const fetchLeads = async () => {
    setLoading(true); // Start loading state
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/leads");
      setLeads(res.data.filter(lead => lead.lead_type === "b2c"));
    } catch (err) { 
      console.error(err); 
    } finally {
      setLoading(false); // End loading state
    }
  };

  // Logic to handle the filter selection
  const filteredLeads = leads.filter(l => 
    filter === "all" || l.status?.toLowerCase() === filter.toLowerCase()
  );

  return (
    <div className="dark-theme-wrapper">
      <Navbar />
      <div className="leads-page-container">
        
        <div className="leads-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px'}}>
          <div>
            <h2>B2C Consumer Hub</h2>
            <p style={{color: '#94a3b8', fontSize: '0.95rem'}}>AI-driven consumer mapping and outreach.</p>
          </div>
          <button className="btn-primary" style={{padding: '12px 24px', borderRadius: '10px'}} disabled={loading}>
             {loading ? "Processing..." : "✨ Generate New Leads"}
          </button>
        </div>

        <div className="glass-card" style={{display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap'}}>
          <span style={{color: '#94a3b8', fontSize: '0.9rem'}}>Showing {filteredLeads.length} Leads</span>
          <select className="glass-input" value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All Consumers</option>
            <option value="new">Unprocessed</option>
            <option value="sent">Outreach Complete</option>
          </select>
        </div>

        <div className="table-wrapper glass-card" style={{padding: '0'}}>
          <table className="leads-table">
            <thead>
              <tr>
                <th>Consumer Details</th>
                <th>Location</th>
                <th>Interests</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="4" style={{textAlign: 'center', padding: '40px', color: '#94a3b8'}}>
                    Updating consumer database...
                  </td>
                </tr>
              ) : filteredLeads.map((lead, i) => (
                <tr key={i}>
                  <td>
                    <div style={{fontWeight: '600', color: '#f8fafc'}}>{lead.name}</div>
                    <div style={{fontSize: '0.85rem', color: '#64748b'}}>{lead.email}</div>
                  </td>
                  <td style={{color: '#cbd5e1'}}>{lead.location || "Global"}</td>
                  <td>
                    <span style={{background: 'rgba(139, 92, 246, 0.1)', color: '#a78bfa', padding: '4px 8px', borderRadius: '6px', fontSize: '0.8rem'}}>
                      {lead.interests || "General"}
                    </span>
                  </td>
                  <td>
                    <span className={`status-badge ${lead.status === 'sent' ? 'status-sent' : 'status-new'}`}>
                      {lead.status?.toUpperCase() || "NEW"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}