import React from "react";
import { Navigate } from "react-router-dom";
import { isLoggedIn } from "../resources/auth";

const ProtectedRoute = ({ children }) => {
  return isLoggedIn() ? children : <Navigate to="/login" replace />;
};

export default ProtectedRoute;