import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import axios from "axios";

export default function PaymentPage() {
  const navigate = useNavigate();

  useEffect(() => {
    // Move the function INSIDE the useEffect to solve the warning
    const makePayment = async (plan) => {
      const storedUserId = localStorage.getItem("userId");

      if (!storedUserId) {
        alert("User ID not found. Please log in again.");
        navigate("/signIn");
        return;
      }

      try {
        const response = await axios.post("http://localhost:5000/api/payments/create-checkout-session", {
          user_id: parseInt(storedUserId),
          plan: plan
        });

        if (response.data.url) {
          localStorage.removeItem("pendingPlan"); 
          window.location.href = response.data.url;
        } else {
          throw new Error("Stripe URL not provided by backend.");
        }
      } catch (error) {
        console.error("Payment Initiation Error:", error);
        alert("Payment Initiation Error. Please try again.");
      }
    };

    const pendingPlan = localStorage.getItem("pendingPlan");
  const userId = localStorage.getItem("userId");

  // CRITICAL: Only trigger if BOTH exist and we haven't already started
  if (pendingPlan && userId) {
    console.log(`Processing payment for User ${userId} on plan ${pendingPlan}`);
    makePayment(pendingPlan);
  } else if (!userId) {
    // If they tried to skip to this page without logging in, kick them out
    navigate("/signIn");
  }
}, [navigate]); // Only 'navigate' is needed as a dependency now

  // Separate function for the manual buttons
  const handleManualPayment = async (plan) => {
    const storedUserId = localStorage.getItem("userId");
    try {
      const response = await axios.post("http://localhost:5000/api/payments/create-checkout-session", {
        user_id: parseInt(storedUserId),
        plan: plan
      });
      if (response.data.url) window.location.href = response.data.url;
    } catch (e) {
      alert("Error starting payment.");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "600px", margin: "0 auto" }}>
      <h2 style={{ textAlign: "center" }}>Complete Your Purchase 💳</h2>
      <p style={{ textAlign: "center", color: "#666" }}>
        Please wait a moment while we redirect you to secure checkout...
      </p>

      <div style={{ marginTop: "30px" }}>
        <div style={{ border: "1px solid #ddd", borderRadius: "8px", padding: "20px", marginBottom: "15px", textAlign: "center" }}>
          <h3>Starter</h3>
          <p style={{ fontSize: "1.2rem", fontWeight: "bold" }}>$1 / Month</p>
          <button 
            onClick={() => handleManualPayment("basic_1_month")}
            style={{ padding: "10px 20px", backgroundColor: "#007bff", color: "#fff", border: "none", borderRadius: "5px", cursor: "pointer" }}
          >
            Pay $1
          </button>
        </div>

        <div style={{ border: "2px solid #007bff", borderRadius: "8px", padding: "20px", textAlign: "center", backgroundColor: "#f0f7ff" }}>
          <h3>Growth</h3>
          <p style={{ fontSize: "1.2rem", fontWeight: "bold" }}>$4 / 3 Months</p>
          <button 
            onClick={() => handleManualPayment("pro_3_month")}
            style={{ padding: "10px 20px", backgroundColor: "#28a745", color: "#fff", border: "none", borderRadius: "5px", cursor: "pointer" }}
          >
            Pay $4
          </button>
        </div>
      </div>
    </div>
  );
}