// =============================================
// CandidateModal.jsx - Candidate Full Profile & Stage Manager
// =============================================
// Shows candidate details, brief note, resume download, and stage changer.
// =============================================

import React, { useState } from 'react';
import { X, User, Mail, Phone, Briefcase, FileText, Download, Clock, ArrowRight, CheckCircle2 } from 'lucide-react';
import { HIRING_STAGES } from '../utils/constants';
import StageBadge from './StageBadge';
import { applicationService } from '../services/applicationService';

export default function CandidateModal({ isOpen, onClose, candidate, onStageUpdated }) {
  const [currentStage, setCurrentStage] = useState(candidate?.stage || 'Applied');
  const [updating, setUpdating] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  if (!isOpen || !candidate) return null;

  const handleStageChange = async (newStage) => {
    try {
      setUpdating(true);
      setSuccessMsg('');
      await applicationService.updateStage(candidate.id, newStage);
      setCurrentStage(newStage);
      setSuccessMsg(`Candidate moved to ${newStage}`);
      onStageUpdated(candidate.id, newStage);
    } catch (err) {
      console.error('Failed to update stage:', err);
    } finally {
      setUpdating(false);
    }
  };

  const resumeUrl = applicationService.getResumeUrl(candidate.id);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 font-bold text-lg">
              {candidate.full_name?.charAt(0) || 'C'}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-bold text-white">{candidate.full_name}</h3>
                <StageBadge stage={currentStage} />
              </div>
              <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
                <Briefcase className="w-3.5 h-3.5 text-indigo-400" />
                <span>{candidate.job_title || 'General Position'}</span>
                <span className="text-slate-600">•</span>
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                <span>Applied {candidate.created_at ? new Date(candidate.created_at).toLocaleDateString() : 'Recently'}</span>
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* Quick Contact Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-4 rounded-xl bg-slate-950/60 border border-slate-800">
            <div className="flex items-center gap-2.5 text-sm text-slate-300">
              <Mail className="w-4 h-4 text-slate-500 shrink-0" />
              <a href={`mailto:${candidate.email}`} className="text-indigo-400 hover:underline truncate">
                {candidate.email}
              </a>
            </div>
            <div className="flex items-center gap-2.5 text-sm text-slate-300">
              <Phone className="w-4 h-4 text-slate-500 shrink-0" />
              <a href={`tel:${candidate.phone}`} className="hover:text-white truncate">
                {candidate.phone}
              </a>
            </div>
          </div>

          {/* Hiring Pipeline Stage Mover */}
          <div className="p-4 rounded-xl bg-indigo-950/20 border border-indigo-500/20 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-indigo-300">
                Move Pipeline Stage
              </span>
              {successMsg && (
                <span className="flex items-center gap-1 text-xs text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  {successMsg}
                </span>
              )}
            </div>

            <div className="flex flex-wrap gap-2">
              {HIRING_STAGES.map((stg) => {
                const isCurrent = currentStage === stg;
                return (
                  <button
                    key={stg}
                    disabled={updating}
                    onClick={() => handleStageChange(stg)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                      isCurrent
                        ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/25 ring-2 ring-indigo-400'
                        : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/50'
                    } disabled:opacity-50`}
                  >
                    {stg}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Brief Note / Cover Letter */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <FileText className="w-3.5 h-3.5 text-indigo-400" />
              <span>Candidate's Note / Intro</span>
            </h4>
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-sm text-slate-200 leading-relaxed whitespace-pre-line">
              {candidate.brief_note ? candidate.brief_note : (
                <span className="text-slate-500 italic">No note provided by the candidate.</span>
              )}
            </div>
          </div>

          {/* Activity / Audit Log Timeline */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-indigo-400" />
              <span>Activity & Status History Log</span>
            </h4>
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300 space-y-2">
              <div className="flex items-start gap-2.5">
                <div className="w-2 h-2 rounded-full bg-emerald-400 mt-1 shrink-0" />
                <div className="flex-1 flex justify-between">
                  <span>Candidate applied for <strong className="text-white">{candidate.job_title}</strong></span>
                  <span className="text-slate-500">{candidate.created_at ? new Date(candidate.created_at).toLocaleString() : 'Recently'}</span>
                </div>
              </div>
              <div className="flex items-start gap-2.5 pt-1 border-t border-slate-800/80">
                <div className="w-2 h-2 rounded-full bg-indigo-400 mt-1 shrink-0" />
                <div className="flex-1 flex justify-between">
                  <span>Current Status in Pipeline: <strong className="text-indigo-300">{currentStage}</strong></span>
                  <span className="text-slate-500">{candidate.updated_at ? new Date(candidate.updated_at).toLocaleString() : 'Recently'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Resume Download Card */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <Download className="w-3.5 h-3.5 text-indigo-400" />
              <span>Resume Attachment</span>
            </h4>
            <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950/60 border border-slate-800">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-sm font-medium text-white">
                    {candidate.resume_filename || 'Candidate_Resume.pdf'}
                  </p>
                  <p className="text-xs text-slate-500">Click download to inspect document</p>
                </div>
              </div>

              <a
                href={resumeUrl}
                target="_blank"
                rel="noreferrer"
                download={candidate.resume_filename || 'resume.pdf'}
                className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 text-xs font-semibold transition-all hover:scale-105"
              >
                <Download className="w-4 h-4" />
                <span>Download Resume</span>
              </a>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-slate-800 bg-slate-950/50 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-sm font-medium transition-colors"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
}
