import { createContext, useContext, useState } from "react";
import apiClient from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  async function login(email, password) {
    const response = await apiClient.post("/api/v1/auth/login", { email, password });
    const { access_token, refresh_token } = response.data;

    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);

    const me = await apiClient.get("/api/v1/auth/me");
    setUser(me.data);
    return me.data;
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
  }

  async function loadCurrentUser() {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    setLoading(true);
    try {
      const me = await apiClient.get("/api/v1/auth/me");
      setUser(me.data);
    } catch (err) {
      logout();
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loadCurrentUser, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
