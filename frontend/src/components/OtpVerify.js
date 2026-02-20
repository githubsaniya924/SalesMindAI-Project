import { useEffect, useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import "./OtpVerify.css";

export default function VerifyOtp() {
  const navigate = useNavigate();

  const [otp, setOtp] = useState("");
  const [message, setMessage] = useState("");
  const [secondsLeft, setSecondsLeft] = useState(300);
  const [expired, setExpired] = useState(false);
  const [loading, setLoading] = useState(false);

  const email = sessionStorage.getItem("signupEmail");

  useEffect(() => {
    if (!email) {
      navigate("/signup");
    }
  }, [email, navigate]);

  useEffect(() => {
    if (secondsLeft <= 0) {
      setExpired(true);
      return;
    }

    const timer = setInterval(() => {
      setSecondsLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [secondsLeft]);

  const formatTime = () => {
    const min = Math.floor(secondsLeft / 60);
    const sec = secondsLeft % 60;
    return `${min}:${sec < 10 ? "0" : ""}${sec}`;
  };

  const verifyOtp = async () => {
    if (expired) return;

    if (otp.length !== 6) {
      setMessage("Please enter a valid 6-digit OTP.");
      return;
    }

    try {
      setLoading(true);

      await api.post("/verify-otp", {
        email,
        otp,
      });

      sessionStorage.removeItem("signupEmail");
      navigate("/dashboard");
    } catch (err) {
      setMessage(err.response?.data?.message || "Verification failed.");
    } finally {
      setLoading(false);
    }
  };

  const resendOtp = async () => {
    try {
      await api.post("/resend-otp", { email });

      setSecondsLeft(300);
      setExpired(false);
      setMessage("OTP resent successfully.");
    } catch {
      setMessage("Failed to resend OTP.");
    }
  };

  return (
    <div className="otp-wrapper">
      <div className="otp-card">
        <h2>Verify Your Email</h2>
        <p>Enter the 6-digit OTP sent to <b>{email}</b></p>

        <input
          type="text"
          maxLength="6"
          value={otp}
          onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
          disabled={expired || loading}
        />

        <div className="timer">
          {expired ? (
            <span style={{ color: "red" }}>OTP expired</span>
          ) : (
            <>Expires in <b>{formatTime()}</b></>
          )}
        </div>

        <button onClick={verifyOtp} disabled={expired || loading}>
          {loading ? "Verifying..." : "Verify OTP"}
        </button>

        <button onClick={resendOtp} disabled={!expired}>
          Resend OTP
        </button>

        {message && <p>{message}</p>}
      </div>
    </div>
  );
}
