import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import api from "../api/axios";

const ProtectedRoute = ({ children }) => {
  const [authorized, setAuthorized] = useState(null);

  useEffect(() => {
    api.get("/auth/check")
      .then(() => setAuthorized(true))
      .catch(() => setAuthorized(false));
  }, []);

  if (authorized === null) return <div>Loading...</div>;

  return authorized ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
