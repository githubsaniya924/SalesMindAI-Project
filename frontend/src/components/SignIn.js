import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import "./Auth.css"; // Using the common file

export default function SignIn() {
  const navigate = useNavigate();
  const [view, setView] = useState("login");
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError("");
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/login", formData);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.message || "Login failed.");
    }
  };

  return (
    <div className="signin-wrapper">
      <div className="floating-bg">
        <span className="float-card c1">✉️</span>
        <span className="float-card c2">📨</span>
        <span className="float-card c3">📩</span>
        <span className="float-card c4">✨</span>
      </div>

      <div className="signin-card">
        <div className="wizard">
          <img src="/wizard.png" alt="wizard" />
        </div>
        <div className="logo-circle">🌸</div>

        {view === "login" ? (
          <>
            <h1>Welcome Back</h1>
            <p className="subtitle">Sign in to continue the magic!</p>
            
            <button className="google-btn">
              <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="google" />
              Sign in with Google
            </button>
            <div className="divider">or</div>

            <form onSubmit={handleSubmit}>
              <input type="email" name="email" placeholder="Email" required onChange={handleChange} />
              <input type="password" name="password" placeholder="Password" required onChange={handleChange} />
              <div style={{ textAlign: 'right', marginBottom: '10px' }}>
                <span className="footer-text" style={{ fontSize: '12px' }} onClick={() => setView("forgot")}>
                  Forgot Password?
                </span>
              </div>
              {error && <p className="error" style={{ color: '#ef4444', fontSize: '13px' }}>{error}</p>}
              <button type="submit" className="primary-btn">Sign In</button>
            </form>
          </>
        ) : (
          <>
            <h1>Reset Password</h1>
            <p className="subtitle">Enter your email to get a link.</p>
            <form onSubmit={(e) => e.preventDefault()}>
              <input type="email" name="email" placeholder="Email" required onChange={handleChange} />
              {error && <p className="error">{error}</p>}
              {message && <p className="success" style={{ color: '#4ade80' }}>{message}</p>}
              <button type="submit" className="primary-btn">Send Reset Link</button>
              <p className="footer-text"><span onClick={() => setView("login")}>Back to Login</span></p>
            </form>
          </>
        )}

        <p className="footer-text">
          Don’t have an account? <span onClick={() => navigate("/signup")}>Sign up</span>
        </p>
      </div>
    </div>
  );
}