import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LeadUploadPage from "./pages/LeadUploadPage";
import B2BGeneratorPage from "./pages/B2BGeneratorPage";
import B2CGeneratorPage from "./pages/B2CGeneratorPage";
import Dashboard from "./pages/DashBoard";
import SignInPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";
import OtpVerifyPage from "./pages/OtpVerifyPage";
import PricingPage from "./pages/PricingPage";
import PaymentPage from "./pages/PaymentPage";
import ProtectedRoute from "./utils/ProtectedRoute";
import ResetPassword from "./pages/ResetPassword";
import Chatbot from "./components/Chatbot";

function App() {
  return (
    <BrowserRouter>
      <Chatbot />
      <Routes>
        <Route path="/login" element={<SignInPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/verify-otp" element={<OtpVerifyPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/leads" element={<LeadUploadPage />} />
        <Route path="/b2b" element={<B2BGeneratorPage />} />
        <Route path="/b2c" element={<B2CGeneratorPage />} />
   
       <Route path="/pricing" element={<PricingPage />} />
       <Route path="/payment" element={<ProtectedRoute><PaymentPage /></ProtectedRoute> } />
       <Route path="/dashboard" element={<ProtectedRoute><Dashboard /> </ProtectedRoute>} />
      <Route path="/reset-password/:token" element={<ResetPassword />} />
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;
