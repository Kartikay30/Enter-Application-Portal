// =============================================
// jobService.js - Jobs API Requests
// =============================================
// Handles fetching jobs for candidates, and CRUD operations for Admin.
// =============================================

import api from './api';

export const jobService = {
  // Get all jobs (pass activeOnly=true for candidate dropdown)
  getJobs: async (activeOnly = false) => {
    const response = await api.get('/api/jobs', {
      params: { active_only: activeOnly }
    });
    return response.data;
  },

  // Get single job details
  getJobById: async (jobId) => {
    const response = await api.get(`/api/jobs/${jobId}`);
    return response.data;
  },

  // Create a new job (Admin only)
  createJob: async (jobData) => {
    const response = await api.post('/api/jobs', jobData);
    return response.data;
  },

  // Update an existing job (Admin only)
  updateJob: async (jobId, jobData) => {
    const response = await api.put(`/api/jobs/${jobId}`, jobData);
    return response.data;
  },

  // Delete a job (Admin only)
  deleteJob: async (jobId) => {
    const response = await api.delete(`/api/jobs/${jobId}`);
    return response.data;
  }
};
