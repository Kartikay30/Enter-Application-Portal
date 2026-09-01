// =============================================
// AuthContext.jsx - Global Authentication State
// =============================================
// Provides logged-in admin state and login/logout functions across all components.
// =============================================

import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('enter_admin_token'));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if saved token is valid on initial load
  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem('enter_admin_token');
      if (savedToken) {
        try {
          const profile = await authService.getMe();
          setUser(profile);
          setToken(savedToken);
        } catch (err) {
          console.error('Session expired or invalid token:', err);
          localStorage.removeItem('enter_admin_token');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  // Login handler
  const login = async (email, password) => {
    const data = await authService.login(email, password);
    localStorage.setItem('enter_admin_token', data.access_token);
    setToken(data.access_token);

    // Fetch user profile immediately
    const profile = await authService.getMe();
    setUser(profile);
    return profile;
  };

  // Logout handler
  const logout = () => {
    localStorage.removeItem('enter_admin_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isAuthenticated: !!token,
        loading,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
