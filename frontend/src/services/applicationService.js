// =============================================
// applicationService.js - Candidate Applications API Requests
// =============================================
// Handles candidate application submission with multipart file upload,
// admin filtering, stage transitions, and resume downloads.
// =============================================

import api from './api';

export const applicationService = {
  // Submit new candidate application (multipart form data with resume file)
  submitApplication: async ({ jobId, fullName, email, phone, briefNote, resumeFile }) => {
    const formData = new FormData();
    formData.append('job_id', jobId);
    formData.append('full_name', fullName);
    formData.append('email', email);
    formData.append('phone', phone);
    if (briefNote) formData.append('brief_note', briefNote);
    if (resumeFile) formData.append('resume', resumeFile);

    const response = await api.post('/api/applications', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  // Get applications with optional query filters (Admin only)
  getApplications: async ({ jobId = null, stage = null, search = null } = {}) => {
    const params = {};
    if (jobId) params.job_id = jobId;
    if (stage) params.stage = stage;
    if (search) params.search = search;

    const response = await api.get('/api/applications', { params });
    return response.data;
  },

  // Get application stats summary (Admin only)
  getStats: async () => {
    const response = await api.get('/api/applications/stats');
    return response.data;
  },

  // Get single application by ID (Admin only)
  getApplicationById: async (applicationId) => {
    const response = await api.get(`/api/applications/${applicationId}`);
    return response.data;
  },

  // Update candidate hiring stage (Admin only)
  updateStage: async (applicationId, stage) => {
    const response = await api.patch(`/api/applications/${applicationId}/stage`, { stage });
    return response.data;
  },

  // Get resume download URL
  getResumeUrl: (applicationId) => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || '';
    return `${baseUrl}/api/applications/${applicationId}/resume`;
  }
};
