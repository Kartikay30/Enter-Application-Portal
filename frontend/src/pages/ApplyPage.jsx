// =============================================
// ApplyPage.jsx - Public Candidate Job Application Portal
// =============================================
// Open link where candidates can apply for any active job.
// Captures: Name, Phone, Email, Job (from dropdown), Brief note, Resume file.
// =============================================

import React, { useState, useEffect } from 'react';
import { Briefcase, User, Mail, Phone, FileText, UploadCloud, CheckCircle2, Sparkles, AlertCircle, ArrowRight, ShieldCheck } from 'lucide-react';
import { jobService } from '../services/jobService';
import { applicationService } from '../services/applicationService';

export default function ApplyPage() {
  const [jobs, setJobs] = useState([]);
  const [loadingJobs, setLoadingJobs] = useState(true);

  // Form State
  const [formData, setFormData] = useState({
    job_id: '',
    full_name: '',
    email: '',
    phone: '',
    brief_note: ''
  });
  const [resumeFile, setResumeFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [submittedApp, setSubmittedApp] = useState(null);

  // Fetch active jobs on mount
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoadingJobs(true);
        const data = await jobService.getJobs(true); // activeOnly = true
        setJobs(data);
        if (data.length > 0) {
          setFormData((prev) => ({ ...prev, job_id: data[0].id.toString() }));
        }
      } catch (err) {
        console.error('Failed to load jobs:', err);
        setErrorMessage('Unable to load open positions. Please make sure the backend is running.');
      } finally {
        setLoadingJobs(false);
      }
    };

    fetchJobs();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const validExtensions = ['.pdf', '.doc', '.docx'];
      const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
      if (!validExtensions.includes(fileExt)) {
        setErrorMessage('Please upload a valid PDF, DOC, or DOCX resume document.');
        setResumeFile(null);
        return;
      }
      // Validate file size (10 MB max)
      if (file.size > 10 * 1024 * 1024) {
        setErrorMessage('File size must be under 10 MB.');
        setResumeFile(null);
        return;
      }
      setErrorMessage('');
      setResumeFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    // Validation
    if (!formData.job_id) {
      setErrorMessage('Please select a job position.');
      return;
    }
    if (!formData.full_name.trim()) {
      setErrorMessage('Please enter your full name.');
      return;
    }
    if (!formData.email.trim()) {
      setErrorMessage('Please enter your email address.');
      return;
    }
    if (!formData.phone.trim()) {
      setErrorMessage('Please enter your phone number.');
      return;
    }
    if (!resumeFile) {
      setErrorMessage('Please upload your resume (PDF or DOCX).');
      return;
    }

    try {
      setSubmitting(true);
      const result = await applicationService.submitApplication({
        jobId: parseInt(formData.job_id),
        fullName: formData.full_name,
        email: formData.email,
        phone: formData.phone,
        briefNote: formData.brief_note,
        resumeFile: resumeFile
      });
      setSubmittedApp(result);
    } catch (err) {
      console.error('Failed to submit application:', err);
      setErrorMessage(err.response?.data?.detail || 'Failed to submit application. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleReset = () => {
    setSubmittedApp(null);
    setFormData({
      job_id: jobs.length > 0 ? jobs[0].id.toString() : '',
      full_name: '',
      email: '',
      phone: '',
      brief_note: ''
    });
    setResumeFile(null);
    setErrorMessage('');
  };

  // Selected job object for description preview
  const selectedJobObj = jobs.find((j) => j.id.toString() === formData.job_id);

  return (
    <div className="min-h-[calc(100vh-4rem)] py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      
      {/* Ambient background glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-10 right-10 w-80 h-80 bg-violet-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="max-w-4xl mx-auto relative">
        
        {/* Header Title */}
        <div className="text-center mb-10 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold tracking-wide uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Join Our Mission</span>
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white">
            Build the Future at <span className="bg-gradient-to-r from-indigo-400 to-violet-300 bg-clip-text text-transparent">Enter</span>
          </h1>
          <p className="max-w-2xl mx-auto text-slate-400 text-sm sm:text-base">
            Select an open role, submit your resume, and start your journey with our world-class engineering team.
          </p>
        </div>

        {/* Success Confirmation Screen */}
        {submittedApp ? (
          <div className="glass-panel rounded-3xl p-8 sm:p-12 text-center border border-emerald-500/30 shadow-2xl animate-in zoom-in-95 duration-300">
            <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-2">
              Application Submitted Successfully!
            </h2>
            <p className="text-slate-300 max-w-md mx-auto mb-6 text-sm">
              Thank you, <strong className="text-white">{submittedApp.full_name}</strong>! Your application for{' '}
              <strong className="text-indigo-300">{submittedApp.job_title}</strong> has been received by our hiring team.
            </p>

            <div className="max-w-sm mx-auto p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-left text-xs text-slate-400 space-y-1.5 mb-8">
              <div className="flex justify-between">
                <span>Application ID:</span>
                <span className="font-mono text-indigo-300">#{submittedApp.id}</span>
              </div>
              <div className="flex justify-between">
                <span>Status:</span>
                <span className="text-emerald-400 font-semibold">{submittedApp.stage} (Initial)</span>
              </div>
              <div className="flex justify-between">
                <span>Resume:</span>
                <span className="text-white truncate max-w-[180px]">{submittedApp.resume_filename}</span>
              </div>
            </div>

            <button
              onClick={handleReset}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-500/25"
            >
              <span>Submit Another Application</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        ) : (
          
          /* Application Form */
          <div className="glass-panel rounded-3xl p-6 sm:p-10 shadow-2xl border border-slate-800">
            
            {errorMessage && (
              <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start gap-3">
                <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-rose-400" />
                <span>{errorMessage}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              
              {/* 1. Job Selection Dropdown */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                  Select Job Position <span className="text-rose-400">*</span>
                </label>
                
                {loadingJobs ? (
                  <div className="h-12 rounded-xl bg-slate-900/60 animate-pulse border border-slate-800" />
                ) : (
                  <div className="relative">
                    <select
                      name="job_id"
                      value={formData.job_id}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 rounded-xl bg-slate-950/90 border border-slate-700/80 text-white font-medium focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm appearance-none cursor-pointer"
                      required
                    >
                      {jobs.map((job) => (
                        <option key={job.id} value={job.id}>
                          {job.title} — {job.department} ({job.location})
                        </option>
                      ))}
                    </select>
                    <Briefcase className="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
                  </div>
                )}

                {/* Selected Job Mini Info Banner */}
                {selectedJobObj && (
                  <div className="mt-2.5 p-3 rounded-xl bg-indigo-950/30 border border-indigo-500/20 text-xs text-slate-300 flex items-center justify-between">
                    <span>
                      <strong className="text-indigo-300">{selectedJobObj.title}</strong> • {selectedJobObj.location} • {selectedJobObj.job_type}
                    </span>
                    <span className="text-slate-400 hidden sm:inline">{selectedJobObj.department}</span>
                  </div>
                )}
              </div>

              {/* 2. Personal Information Fields */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                
                {/* Full Name */}
                <div className="sm:col-span-2">
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                    Full Name <span className="text-rose-400">*</span>
                  </label>
                  <div className="relative">
                    <input
                      type="text"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleInputChange}
                      placeholder="e.g. Rahul Sharma"
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-700/80 text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
                      required
                    />
                    <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  </div>
                </div>

                {/* Email Address */}
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                    Email Address <span className="text-rose-400">*</span>
                  </label>
                  <div className="relative">
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      placeholder="e.g. rahul@example.com"
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-700/80 text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
                      required
                    />
                    <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  </div>
                </div>

                {/* Phone Number */}
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                    Phone Number <span className="text-rose-400">*</span>
                  </label>
                  <div className="relative">
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      placeholder="e.g. +91 98765 43210"
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-700/80 text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm"
                      required
                    />
                    <Phone className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  </div>
                </div>

              </div>

              {/* 3. Resume File Upload */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                  Upload Resume (PDF / DOCX) <span className="text-rose-400">*</span>
                </label>
                
                <div className="relative border-2 border-dashed border-slate-700 hover:border-indigo-500/60 rounded-2xl p-6 text-center bg-slate-950/50 transition-all group cursor-pointer">
                  <input
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    required
                  />
                  
                  {resumeFile ? (
                    <div className="flex items-center justify-center gap-3">
                      <div className="p-2.5 rounded-xl bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                        <FileText className="w-6 h-6" />
                      </div>
                      <div className="text-left">
                        <p className="text-sm font-semibold text-white">{resumeFile.name}</p>
                        <p className="text-xs text-slate-400">
                          {(resumeFile.size / (1024 * 1024)).toFixed(2)} MB • Click or drag to replace
                        </p>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <div className="w-12 h-12 mx-auto rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform">
                        <UploadCloud className="w-6 h-6" />
                      </div>
                      <p className="text-sm font-medium text-slate-200">
                        <span className="text-indigo-400">Click to upload</span> or drag and drop
                      </p>
                      <p className="text-xs text-slate-500">
                        Supports PDF, DOC, DOCX up to 10MB
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* 4. Brief Note / Cover Letter */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                  A Brief Note / Why Enter? (Optional)
                </label>
                <textarea
                  name="brief_note"
                  rows={4}
                  value={formData.brief_note}
                  onChange={handleInputChange}
                  placeholder="Share a short introduction, your key achievements, or what excites you about this role..."
                  className="w-full px-4 py-3 rounded-xl bg-slate-950/80 border border-slate-700/80 text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-sm resize-none"
                />
              </div>

              {/* 5. Submit Button */}
              <div className="pt-2">
                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold text-sm shadow-xl shadow-indigo-500/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed group cursor-pointer"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>{submitting ? 'Submitting Application...' : 'Submit Application'}</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>

              {/* Security guarantee footnote */}
              <div className="flex items-center justify-center gap-1.5 text-xs text-slate-500 pt-2">
                <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
                <span>Your application and resume details are securely protected and encrypted.</span>
              </div>

            </form>
          </div>
        )}

      </div>
    </div>
  );
}
