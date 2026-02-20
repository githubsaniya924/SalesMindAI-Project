import React from "react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
const PricingPage = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("userId"); // Check if user is logged in

  useEffect(() => {
    const storedUserId = localStorage.getItem("userId");
    if (!storedUserId) {
      // If no user ID, redirect them to login immediately
      alert("Please login to access the payment page.");
      navigate("/login");
    }
  }, [navigate]);

  const plans = [
    {
      name: "Starter",
      price: "$1",
      duration: "1 Month",
      features: ["40 Leads per day", "Email Support", "Standard Speed"],
      id: "basic_1_month"
    },
    {
      name: "Growth",
      price: "$4",
      duration: "3 Months",
      features: ["40 Leads per day", "Priority Support", "Faster Processing", "Save 20%"],
      id: "pro_3_month",
      highlight: true
    }
  ];

const handleBuyNow = (planId) => {
  const userId = localStorage.getItem("userId");

  // Save the intent regardless so we remember what they wanted
  localStorage.setItem("pendingPlan", planId);

  if (userId) {
    // USER IS ALREADY LOGGED IN: Go straight to payment
    navigate("/payment");
  } else {
    // USER IS A GUEST: Force them to sign in first
    alert("Please sign in to proceed with your purchase.");
    navigate("/signIn"); 
  }
};

// Your button would look like this:

  return (
    <div style={{ padding: "60px 20px", textAlign: "center", backgroundColor: "#f9f9f9" }}>
      <h1 style={{ fontSize: "2.5rem", marginBottom: "10px" }}>Simple, Transparent Pricing</h1>
      <p style={{ color: "#666", marginBottom: "40px" }}>Choose the plan that fits your lead generation needs.</p>

      <div style={{ display: "flex", justifyContent: "center", gap: "20px", flexWrap: "wrap" }}>
        {plans.map((plan) => (
          <div key={plan.id} style={{
            border: plan.highlight ? "2px solid #007bff" : "1px solid #ddd",
            borderRadius: "12px",
            padding: "30px",
            width: "300px",
            backgroundColor: "#fff",
            boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
            position: "relative"
          }}>
            {plan.highlight && <span style={{
              position: "absolute", top: "-15px", left: "50%", transform: "translateX(-50%)",
              backgroundColor: "#007bff", color: "#fff", padding: "5px 15px", borderRadius: "20px", fontSize: "12px"
            }}>MOST POPULAR</span>}

            <h2 style={{ margin: "10px 0" }}>{plan.name}</h2>
            <div style={{ fontSize: "3rem", fontWeight: "bold" }}>{plan.price}</div>
            <div style={{ color: "#888", marginBottom: "20px" }}>{plan.duration}</div>
            
            <ul style={{ listStyle: "none", padding: 0, textAlign: "left", marginBottom: "30px" }}>
              {plan.features.map(feat => (
                <li key={feat} style={{ marginBottom: "10px" }}>✅ {feat}</li>
              ))}
            </ul>

            <button 
  onClick={() => handleBuyNow(plan.id)} // Pass the plan.id here!
  style={{
    width: "100%", padding: "12px", borderRadius: "6px", border: "none",
    backgroundColor: plan.highlight ? "#007bff" : "#333",
    color: "#fff", cursor: "pointer", fontWeight: "bold", fontSize: "16px"
  }}
>
  {isLoggedIn ? "Buy Now" : "Sign in to Get Started"}
</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PricingPage;