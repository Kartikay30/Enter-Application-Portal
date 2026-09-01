// =============================================
// api.js - Centralized Axios Instance & Interceptors
// =============================================
// Automatically injects the JWT Bearer token into headers for admin requests.
// Handles baseURL and response error formatting.
// =============================================

import axios from 'axios';

// Vite proxy forwards /api to http://localhost:8000/api
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request Interceptor: Attach JWT Token if user is logged in
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('enter_admin_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401 Unauthorized globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // If token expired or invalid while accessing protected route, clear it
      if (window.location.pathname.startsWith('/admin/dashboard')) {
        localStorage.removeItem('enter_admin_token');
        window.location.href = '/admin/login?expired=true';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
