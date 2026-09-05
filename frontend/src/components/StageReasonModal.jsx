// =============================================
// StageReasonModal.jsx - Reason/Feedback Pop-up for Stage Transition
// =============================================
// Requires admin to provide a reason/feedback note when advancing,
// rejecting, or selecting a candidate, and saves it to the database.
// =============================================

import React, { useState, useEffect } from 'react';
import { X, MessageSquare, CheckCircle2, AlertTriangle, ArrowRight, Sparkles, User, Briefcase } from 'lucide-react';
import StageBadge from './StageBadge';

export default function StageReasonModal({
  isOpen,
  onClose,
  candidate,
  targetStage,
  onConfirm
}) {
  const [reason, setReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Reset reason or prefill with current reason if moving stage
  useEffect(() => {
    if (isOpen) {
      setReason('');
      setError('');
    }
  }, [isOpen, targetStage, candidate]);

  if (!isOpen || !candidate || !targetStage) return null;

  const isReject = targetStage.toLowerCase().includes('reject');
  const isApproved = targetStage === 'Approved';

  // Quick preset suggestions based on the stage
  const presetSuggestions = isReject
    ? [
        'Lacks required experience in core tech stack',
        'Did not meet problem-solving / coding benchmarks in technical round',
        'Role requirements changed / position filled',
        'Candidate communication or culture fit mismatch'
      ]
    : isApproved
    ? [
        'Outstanding technical interview performance; strong fit for team',
        'Exceptional portfolio and demonstrated mastery of required technologies',
        'Top candidate among all applicants; verified positive references'
      ]
    : [
        'Strong resume screening; advanced to Round 1 technical evaluation',
        'Cleared initial screening with solid fundamentals; scheduled next round',
        'Impressive project portfolio; moving forward to technical panel'
      ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!reason.trim()) {
      setError('Please provide a reason or note for this decision.');
      return;
    }

    try {
      setIsSubmitting(true);
      setError('');
      await onConfirm(candidate.id, targetStage, reason.trim());
      onClose();
    } catch (err) {
      console.error('Error submitting stage reason:', err);
      setError(err?.response?.data?.detail || 'Failed to update candidate stage.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col">
        
        {/* Header with Stage Badge Transition */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-slate-800 bg-slate-950/60">
          <div className="flex items-center gap-3">
            <div
              className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-base border ${
                isReject
                  ? 'bg-rose-500/10 border-rose-500/25 text-rose-400'
                  : isApproved
                  ? 'bg-emerald-500/10 border-emerald-500/25 text-emerald-400'
                  : 'bg-indigo-500/10 border-indigo-500/25 text-indigo-400'
              }`}
            >
              {isReject ? <AlertTriangle className="w-5 h-5" /> : isApproved ? <CheckCircle2 className="w-5 h-5" /> : <MessageSquare className="w-5 h-5" />}
            </div>
            <div>
              <h3 className="text-base font-bold text-white">
                {isReject ? 'Candidate Rejection Reason' : isApproved ? 'Candidate Selection Reason' : 'Stage Movement Reason'}
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Record official evaluation notes saved to database
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            disabled={isSubmitting}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          
          {/* Candidate Summary Card */}
          <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 flex items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="w-7 h-7 rounded-lg bg-indigo-500/15 border border-indigo-500/25 flex items-center justify-center text-indigo-400 font-bold shrink-0">
                {candidate.full_name?.charAt(0) || 'C'}
              </div>
              <div className="truncate">
                <div className="font-semibold text-white truncate">{candidate.full_name}</div>
                <div className="text-slate-400 truncate">{candidate.job_title || 'Role'}</div>
              </div>
            </div>

            {/* Stage Transition Indicator */}
            <div className="flex items-center gap-1.5 shrink-0">
              <StageBadge stage={candidate.stage} />
              <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
              <StageBadge stage={targetStage} />
            </div>
          </div>

          {/* Reason Input Area */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
                {isReject
                  ? 'Rejection Feedback / Notes *'
                  : isApproved
                  ? 'Hiring / Selection Notes *'
                  : 'Stage Progression Notes *'}
              </label>
              <span className="text-[11px] text-slate-500">Saved in audit history</span>
            </div>

            <textarea
              required
              rows={4}
              value={reason}
              onChange={(e) => {
                setReason(e.target.value);
                if (error) setError('');
              }}
              placeholder={
                isReject
                  ? 'Explain why the candidate is being rejected at this stage...'
                  : isApproved
                  ? 'Detail the rationale for final selection and hiring...'
                  : 'Add interview feedback or notes on why candidate is advancing...'
              }
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors leading-relaxed"
            />
          </div>

          {/* Quick Preset Badges */}
          <div className="space-y-1.5">
            <div className="flex items-center gap-1 text-[11px] font-medium text-slate-400">
              <Sparkles className="w-3 h-3 text-indigo-400" />
              <span>Quick Preset Suggestions (click to use):</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {presetSuggestions.map((suggestion, idx) => (
                <button
                  type="button"
                  key={idx}
                  onClick={() => {
                    setReason(suggestion);
                    if (error) setError('');
                  }}
                  className="text-left text-[11px] px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition-colors cursor-pointer"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-xs text-rose-400 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3 pt-2 border-t border-slate-800/80">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-colors cursor-pointer disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !reason.trim()}
              className={`inline-flex items-center gap-2 px-5 py-2 rounded-xl text-xs font-semibold text-white shadow-lg transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed ${
                isReject
                  ? 'bg-rose-600 hover:bg-rose-500 shadow-rose-600/20'
                  : isApproved
                  ? 'bg-emerald-600 hover:bg-emerald-500 shadow-emerald-600/20'
                  : 'bg-indigo-600 hover:bg-indigo-500 shadow-indigo-600/20'
              }`}
            >
              {isSubmitting ? (
                <span>Saving to DB...</span>
              ) : (
                <>
                  <span>Confirm & Save Reason</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>

        </form>

      </div>
    </div>
  );
}
