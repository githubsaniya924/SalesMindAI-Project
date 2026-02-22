import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "../components/Auth.css"; // Reuse your existing beautiful styles

export default function ResetPassword() {
  const { token } = useParams(); // Grabs the token from the URL
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleReset = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      await axios.post("http://localhost:5000/api/reset-password", {
        token: token,
        new_password: password,
      });
      setMessage("Password updated successfully! Redirecting to login...");
      setTimeout(() => navigate("/login"), 3000);
    } catch (err) {
      setError(err.response?.data?.error || "Reset failed. Token may be expired.");
    }
  };

  return (
    <div className="signin-wrapper">
      <div className="signin-card">
        <div className="ring"></div>
        <div className="signin-logo">🔑</div>
        <h1>New Password</h1>
        <p className="subtitle">Enter a strong password to secure your account</p>

        <form onSubmit={handleReset}>
          <input
            type="password"
            placeholder="New Password"
            required
            onChange={(e) => setPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="Confirm New Password"
            required
            onChange={(e) => setConfirmPassword(e.target.value)}
          />

          {error && <p className="error">{error}</p>}
          {message && <p className="success-msg">{message}</p>}

          <button type="submit" className="signin-btn">Update Password</button>
        </form>
      </div>
    </div>
  );
}