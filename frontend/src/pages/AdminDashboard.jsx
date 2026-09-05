// =============================================
// AdminDashboard.jsx - Main Hiring & ATS Management Dashboard
// =============================================
// Features:
//   - Manage Jobs (Create, Edit, Delete, Toggle Status)
//   - Review Candidates with all captured details
//   - Filter Candidates by Job
//   - Filter Candidates by Stage (Applied, R1, R2, R3, Reject, Approved)
//   - Move Candidates across Pipeline Stages instantly
//   - Download and Inspect Resumes
// =============================================

import React, { useState, useEffect, useMemo } from 'react';
import {
  Users, Briefcase, Plus, Search, Filter, RefreshCw, FileText, Download,
  Edit2, Trash2, CheckCircle2, XCircle, Clock, ChevronRight, Eye, Sparkles, Building2, MapPin, AlertTriangle
} from 'lucide-react';
import { jobService } from '../services/jobService';
import { applicationService } from '../services/applicationService';
import { HIRING_STAGES } from '../utils/constants';
import StageBadge from '../components/StageBadge';
import JobModal from '../components/JobModal';
import CandidateModal from '../components/CandidateModal';
import StageReasonModal from '../components/StageReasonModal';
import Toast from '../components/Toast';

export default function AdminDashboard() {
  // Tab State: 'candidates' | 'jobs'
  const [activeTab, setActiveTab] = useState('candidates');

  // Data States
  const [jobs, setJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  // Filters State
  const [selectedJobFilter, setSelectedJobFilter] = useState('');
  const [selectedStageFilter, setSelectedStageFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // Modal States
  const [isJobModalOpen, setIsJobModalOpen] = useState(false);
  const [jobToEdit, setJobToEdit] = useState(null);
  const [jobToDelete, setJobToDelete] = useState(null);
  const [isDeletingJob, setIsDeletingJob] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [isCandidateModalOpen, setIsCandidateModalOpen] = useState(false);
  const [pendingStageChange, setPendingStageChange] = useState(null);

  // Toast Notification
  const [toast, setToast] = useState({ message: '', type: 'success' });

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast({ message: '', type: 'success' }), 4000);
  };

  // Load all dashboard data
  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [jobsData, appsData, statsData] = await Promise.all([
        jobService.getJobs(false), // All jobs (active + closed)
        applicationService.getApplications({
          jobId: selectedJobFilter ? parseInt(selectedJobFilter) : null,
          stage: selectedStageFilter || null,
          search: searchQuery || null
        }),
        applicationService.getStats()
      ]);
      setJobs(jobsData);
      setApplications(appsData);
      setStats(statsData);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      showToast('Failed to load dashboard data. Check backend connection.', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on filter changes
  useEffect(() => {
    loadDashboardData();
  }, [selectedJobFilter, selectedStageFilter]);

  // Handle Search input with debounce or trigger
  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadDashboardData();
  };

  // Handle Stage selection from candidate row dropdown -> opens Reason pop-up modal
  const handleStageDropdownSelect = (candidate, newStage) => {
    if (candidate.stage === newStage) return;
    setPendingStageChange({
      candidate,
      targetStage: newStage
    });
  };

  // Confirm stage change with admin reason note and persist to database
  const handleConfirmStageChange = async (appId, newStage, reason) => {
    try {
      await applicationService.updateStage(appId, newStage, reason);
      showToast(`Candidate moved to ${newStage} with decision reason recorded.`);
      // Update local state smoothly
      setApplications((prev) =>
        prev.map((app) => (app.id === appId ? { ...app, stage: newStage, stage_reason: reason } : app))
      );
      // Refresh stats
      const updatedStats = await applicationService.getStats();
      setStats(updatedStats);
    } catch (err) {
      console.error('Failed to update stage:', err);
      showToast(err?.response?.data?.detail || 'Failed to update candidate stage.', 'error');
      throw err;
    }
  };

  // Open Delete Job Confirmation Modal
  const handleOpenDeleteJob = (job) => {
    setJobToDelete(job);
  };

  // Confirm and Execute Delete Job
  const handleConfirmDeleteJob = async () => {
    if (!jobToDelete) return;
    try {
      setIsDeletingJob(true);
      await jobService.deleteJob(jobToDelete.id);
      
      // Optimistic state update
      setJobs((prev) => prev.filter((j) => j.id !== jobToDelete.id));
      showToast(`Job "${jobToDelete.title}" deleted successfully.`);
      setJobToDelete(null);
      
      // Reload fresh stats & jobs
      loadDashboardData();
    } catch (err) {
      console.error('Failed to delete job:', err);
      showToast(err.response?.data?.detail || 'Failed to delete job.', 'error');
    } finally {
      setIsDeletingJob(false);
    }
  };

  const handleOpenEditJob = (job) => {
    setJobToEdit(job);
    setIsJobModalOpen(true);
  };

  const handleOpenCreateJob = () => {
    setJobToEdit(null);
    setIsJobModalOpen(true);
  };

  const handleOpenCandidateModal = (candidate) => {
    setSelectedCandidate(candidate);
    setIsCandidateModalOpen(true);
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      
      {/* Toast Alert */}
      <Toast message={toast.message} type={toast.type} onClose={() => setToast({ message: '' })} />

      {/* Top Header & Quick Action */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-2.5">
            <span>Hiring Management Dashboard</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-medium">
              Admin ATS
            </span>
          </h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Manage active job openings, review candidate resumes, and advance candidates through the hiring pipeline.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadDashboardData}
            title="Refresh Data"
            className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-indigo-400' : ''}`} />
          </button>

          <button
            onClick={handleOpenCreateJob}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold shadow-lg shadow-indigo-500/25 transition-all cursor-pointer"
          >
            <Plus className="w-4 h-4" />
            <span>Post New Job</span>
          </button>
        </div>
      </div>

      {/* KPI Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Total Candidates */}
        <div className="glass-panel rounded-2xl p-5 border border-slate-800 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Users className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">Total Applicants</p>
            <h3 className="text-2xl font-bold text-white mt-0.5">{stats ? stats.total : '—'}</h3>
          </div>
        </div>

        {/* Applied (Initial) */}
        <div className="glass-panel rounded-2xl p-5 border border-slate-800 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">New (Applied)</p>
            <h3 className="text-2xl font-bold text-white mt-0.5">{stats ? stats.applied : '—'}</h3>
          </div>
        </div>

        {/* In Interview (R1, R2, R3) */}
        <div className="glass-panel rounded-2xl p-5 border border-slate-800 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">In Pipeline (R1-R3)</p>
            <h3 className="text-2xl font-bold text-white mt-0.5">
              {stats ? stats.r1 + stats.r2 + stats.r3 : '—'}
            </h3>
          </div>
        </div>

        {/* Approved */}
        <div className="glass-panel rounded-2xl p-5 border border-slate-800 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">Approved / Hired</p>
            <h3 className="text-2xl font-bold text-emerald-400 mt-0.5">{stats ? stats.approved : '—'}</h3>
          </div>
        </div>

      </div>

      {/* Tabs Navigation */}
      <div className="flex border-b border-slate-800">
        <button
          onClick={() => setActiveTab('candidates')}
          className={`flex items-center gap-2 py-3 px-5 text-sm font-semibold border-b-2 transition-all cursor-pointer ${
            activeTab === 'candidates'
              ? 'border-indigo-500 text-indigo-400 bg-indigo-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
          }`}
        >
          <Users className="w-4 h-4" />
          <span>Candidate Applications ({applications.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('jobs')}
          className={`flex items-center gap-2 py-3 px-5 text-sm font-semibold border-b-2 transition-all cursor-pointer ${
            activeTab === 'jobs'
              ? 'border-indigo-500 text-indigo-400 bg-indigo-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
          }`}
        >
          <Briefcase className="w-4 h-4" />
          <span>Job Openings Management ({jobs.length})</span>
        </button>
      </div>

      {/* ======================================================== */}
      {/* TAB 1: CANDIDATES & PIPELINE MANAGEMENT                 */}
      {/* ======================================================== */}
      {activeTab === 'candidates' && (
        <div className="space-y-6">
          
          {/* Multi-Filters & Search Bar */}
          <div className="glass-panel rounded-2xl p-4 border border-slate-800 flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
            
            {/* Search Input */}
            <form onSubmit={handleSearchSubmit} className="relative flex-1">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search candidate by name or email..."
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-700/80 text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 text-xs sm:text-sm"
              />
              <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
            </form>

            <div className="flex flex-wrap items-center gap-3">
              
              {/* Filter by Job Dropdown */}
              <div className="flex items-center gap-2 min-w-[200px] flex-1 sm:flex-initial">
                <Filter className="w-4 h-4 text-slate-500 shrink-0 hidden sm:inline" />
                <select
                  value={selectedJobFilter}
                  onChange={(e) => setSelectedJobFilter(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl bg-slate-950/80 border border-slate-700/80 text-white text-xs sm:text-sm focus:outline-none focus:border-indigo-500 cursor-pointer"
                >
                  <option value="">All Jobs ({jobs.length})</option>
                  {jobs.map((job) => (
                    <option key={job.id} value={job.id}>
                      {job.title}
                    </option>
                  ))}
                </select>
              </div>

              {/* Filter by Stage Dropdown */}
              <div className="min-w-[180px] flex-1 sm:flex-initial">
                <select
                  value={selectedStageFilter}
                  onChange={(e) => setSelectedStageFilter(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl bg-slate-950/80 border border-slate-700/80 text-white text-xs sm:text-sm focus:outline-none focus:border-indigo-500 cursor-pointer"
                >
                  <option value="">All Hiring Stages</option>
                  {HIRING_STAGES.map((stg) => (
                    <option key={stg} value={stg}>
                      {stg}
                    </option>
                  ))}
                </select>
              </div>

              {/* Reset Filters */}
              {(selectedJobFilter || selectedStageFilter || searchQuery) && (
                <button
                  onClick={() => {
                    setSelectedJobFilter('');
                    setSelectedStageFilter('');
                    setSearchQuery('');
                  }}
                  className="px-3 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium transition-colors"
                >
                  Reset
                </button>
              )}

            </div>
          </div>

          {/* Applications Table / Cards */}
          <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
            {loading ? (
              <div className="p-12 text-center text-slate-400 space-y-3">
                <RefreshCw className="w-6 h-6 mx-auto animate-spin text-indigo-400" />
                <p className="text-sm">Loading candidate applications...</p>
              </div>
            ) : applications.length === 0 ? (
              <div className="p-12 text-center text-slate-400 space-y-3">
                <Users className="w-10 h-10 mx-auto text-slate-600" />
                <p className="text-base font-semibold text-white">No applications match your criteria.</p>
                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                  Try adjusting the job or stage filters above, or submit an application through the candidate portal.
                </p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-slate-300">
                  <thead className="text-xs uppercase bg-slate-950/70 text-slate-400 border-b border-slate-800 tracking-wider">
                    <tr>
                      <th className="px-6 py-4">Candidate</th>
                      <th className="px-6 py-4">Applied Role</th>
                      <th className="px-6 py-4">Current Stage</th>
                      <th className="px-6 py-4">Move Stage</th>
                      <th className="px-6 py-4">Resume</th>
                      <th className="px-6 py-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {applications.map((app) => (
                      <tr key={app.id} className="hover:bg-slate-850/40 transition-colors">
                        
                        {/* Candidate Details */}
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-9 h-9 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 font-bold text-sm">
                              {app.full_name?.charAt(0) || 'C'}
                            </div>
                            <div>
                              <div className="font-semibold text-white">{app.full_name}</div>
                              <div className="text-xs text-slate-400">{app.email}</div>
                              <div className="text-xs text-slate-500">{app.phone}</div>
                            </div>
                          </div>
                        </td>

                        {/* Applied Job */}
                        <td className="px-6 py-4">
                          <span className="font-medium text-slate-200 block">{app.job_title}</span>
                          <span className="text-xs text-slate-500">
                            {app.created_at ? new Date(app.created_at).toLocaleDateString() : 'Recent'}
                          </span>
                        </td>

                        {/* Current Stage Badge */}
                        <td className="px-6 py-4">
                          <div className="space-y-1">
                            <StageBadge stage={app.stage} />
                            {app.stage_reason && (
                              <p className="text-[11px] text-slate-400 line-clamp-1 max-w-[160px] italic" title={app.stage_reason}>
                                "{app.stage_reason}"
                              </p>
                            )}
                          </div>
                        </td>

                        {/* Quick Stage Transition Dropdown -> Prompts Reason Modal */}
                        <td className="px-6 py-4">
                          <select
                            value={app.stage}
                            onChange={(e) => handleStageDropdownSelect(app, e.target.value)}
                            className="px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs font-medium text-slate-200 focus:outline-none focus:border-indigo-500 cursor-pointer hover:border-slate-600 transition-colors"
                          >
                            {HIRING_STAGES.map((stg) => (
                              <option key={stg} value={stg}>
                                {stg}
                              </option>
                            ))}
                          </select>
                        </td>

                        {/* Resume Download */}
                        <td className="px-6 py-4">
                          <a
                            href={applicationService.getResumeUrl(app.id)}
                            target="_blank"
                            rel="noreferrer"
                            download={app.resume_filename || 'resume.pdf'}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-medium transition-colors"
                          >
                            <Download className="w-3.5 h-3.5" />
                            <span className="truncate max-w-[120px]">
                              {app.resume_filename ? 'Download' : 'Resume'}
                            </span>
                          </a>
                        </td>

                        {/* View Full Profile Action */}
                        <td className="px-6 py-4 text-right">
                          <button
                            onClick={() => handleOpenCandidateModal(app)}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors cursor-pointer"
                          >
                            <Eye className="w-3.5 h-3.5 text-indigo-400" />
                            <span>Details</span>
                          </button>
                        </td>

                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

        </div>
      )}

      {/* ======================================================== */}
      {/* TAB 2: JOBS MANAGEMENT (CRUD)                            */}
      {/* ======================================================== */}
      {activeTab === 'jobs' && (
        <div className="space-y-6">
          
          <div className="flex items-center justify-between">
            <p className="text-sm text-slate-400">
              Showing {jobs.length} published jobs. Candidates can select any active job on the application page.
            </p>
            <button
              onClick={handleOpenCreateJob}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs sm:text-sm font-semibold shadow-lg shadow-indigo-500/25 transition-all cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>Add Job</span>
            </button>
          </div>

          {/* Jobs Table */}
          <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden shadow-xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-300">
                <thead className="text-xs uppercase bg-slate-950/70 text-slate-400 border-b border-slate-800 tracking-wider">
                  <tr>
                    <th className="px-6 py-4">Job Title</th>
                    <th className="px-6 py-4">Department</th>
                    <th className="px-6 py-4">Location</th>
                    <th className="px-6 py-4">Type</th>
                    <th className="px-6 py-4">Status</th>
                    <th className="px-6 py-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {jobs.map((job) => (
                    <tr key={job.id} className="hover:bg-slate-850/40 transition-colors">
                      
                      <td className="px-6 py-4">
                        <div className="font-semibold text-white">{job.title}</div>
                        <div className="text-xs text-slate-400 line-clamp-1 max-w-sm mt-0.5">
                          {job.description}
                        </div>
                      </td>

                      <td className="px-6 py-4 text-slate-300 font-medium">
                        {job.department}
                      </td>

                      <td className="px-6 py-4 text-slate-400">
                        {job.location}
                      </td>

                      <td className="px-6 py-4">
                        <span className="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                          {job.job_type}
                        </span>
                      </td>

                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
                            job.status === 'Active'
                              ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30'
                              : 'bg-slate-800 text-slate-400 border-slate-700'
                          }`}
                        >
                          <span
                            className={`w-1.5 h-1.5 rounded-full ${
                              job.status === 'Active' ? 'bg-emerald-400' : 'bg-slate-500'
                            }`}
                          />
                          {job.status}
                        </span>
                      </td>

                      <td className="px-6 py-4 text-right space-x-2">
                        <button
                          onClick={() => handleOpenEditJob(job)}
                          title="Edit Job"
                          className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-indigo-300 hover:text-white transition-colors cursor-pointer"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleOpenDeleteJob(job)}
                          title="Delete Job"
                          className="p-2 rounded-lg bg-slate-800 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition-colors cursor-pointer"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>

                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      )}

      {/* Modal Dialogs */}
      <JobModal
        isOpen={isJobModalOpen}
        onClose={() => setIsJobModalOpen(false)}
        jobToEdit={jobToEdit}
        onJobSaved={() => {
          showToast(jobToEdit ? 'Job updated successfully!' : 'New job created successfully!');
          loadDashboardData();
        }}
      />

      <CandidateModal
        isOpen={isCandidateModalOpen}
        onClose={() => setIsCandidateModalOpen(false)}
        candidate={selectedCandidate}
        onStageUpdated={(appId, newStage, reason) => {
          setApplications((prev) =>
            prev.map((a) => (a.id === appId ? { ...a, stage: newStage, stage_reason: reason } : a))
          );
          applicationService.getStats().then(setStats);
        }}
      />

      {/* Pop-up Modal for Selection/Rejection/Stage Reason */}
      <StageReasonModal
        isOpen={!!pendingStageChange}
        onClose={() => setPendingStageChange(null)}
        candidate={pendingStageChange?.candidate}
        targetStage={pendingStageChange?.targetStage}
        onConfirm={handleConfirmStageChange}
      />

      {/* Delete Job Confirmation Modal */}
      {jobToDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
          <div className="relative w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 space-y-6">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 shrink-0">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Delete Job Opening?</h3>
                <p className="text-sm text-slate-400 mt-1">
                  Are you sure you want to permanently delete <span className="text-white font-medium">"{jobToDelete.title}"</span>?
                </p>
                <p className="text-xs text-slate-500 mt-2">
                  Existing candidates who applied for this role will be safely preserved in your ATS pipeline.
                </p>
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                disabled={isDeletingJob}
                onClick={() => setJobToDelete(null)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-colors cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={isDeletingJob}
                onClick={handleConfirmDeleteJob}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white text-xs font-semibold shadow-lg shadow-rose-600/25 transition-all cursor-pointer"
              >
                {isDeletingJob ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    <span>Deleting...</span>
                  </>
                ) : (
                  <>
                    <Trash2 className="w-3.5 h-3.5" />
                    <span>Delete Job</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
