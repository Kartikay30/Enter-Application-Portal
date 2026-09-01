// =============================================
// authService.js - Authentication API Requests
// =============================================
// Handles admin login and session validation.
// =============================================

import api from './api';

export const authService = {
  // Login with email & password -> returns { access_token, token_type }
  login: async (email, password) => {
    const response = await api.post('/api/auth/login', { email, password });
    return response.data;
  },

  // Register a new admin account -> returns { id, email, role }
  register: async (email, password, confirmPassword) => {
    const response = await api.post('/api/auth/register', {
      email,
      password,
      confirm_password: confirmPassword
    });
    return response.data;
  },

  // Get current logged-in admin profile
  getMe: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  }
};
