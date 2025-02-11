import React from "react";
import { Navigate } from "react-router-dom";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const token = localStorage.getItem("token");
  
  if (!token) {
    // Redirect to login page if no token is found
    return <Navigate to="/login" replace />;
  }
  
  // Render children if authenticated
  return <>{children}</>;
}
