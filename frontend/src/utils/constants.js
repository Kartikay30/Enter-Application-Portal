// =============================================
// constants.js - Global App Constants & Stage Colors
// =============================================
// Defines all hiring pipeline stages, badge color styles, and helper constants.
// =============================================

export const HIRING_STAGES = [
  'Applied',
  'R1',
  'R1 Reject',
  'R2',
  'R2 Reject',
  'R3',
  'R3 Reject',
  'Reject',
  'Approved'
];

export const STAGE_CONFIG = {
  'Applied': {
    label: 'Applied (Initial)',
    badgeBg: 'bg-blue-500/15',
    badgeText: 'text-blue-400',
    badgeBorder: 'border-blue-500/30',
    dotColor: 'bg-blue-400'
  },
  'R1': {
    label: 'Round 1 (R1)',
    badgeBg: 'bg-indigo-500/15',
    badgeText: 'text-indigo-400',
    badgeBorder: 'border-indigo-500/30',
    dotColor: 'bg-indigo-400'
  },
  'R1 Reject': {
    label: 'R1 Rejected',
    badgeBg: 'bg-rose-500/15',
    badgeText: 'text-rose-400',
    badgeBorder: 'border-rose-500/30',
    dotColor: 'bg-rose-400'
  },
  'R2': {
    label: 'Round 2 (R2)',
    badgeBg: 'bg-purple-500/15',
    badgeText: 'text-purple-400',
    badgeBorder: 'border-purple-500/30',
    dotColor: 'bg-purple-400'
  },
  'R2 Reject': {
    label: 'R2 Rejected',
    badgeBg: 'bg-rose-500/15',
    badgeText: 'text-rose-400',
    badgeBorder: 'border-rose-500/30',
    dotColor: 'bg-rose-400'
  },
  'R3': {
    label: 'Round 3 (R3)',
    badgeBg: 'bg-amber-500/15',
    badgeText: 'text-amber-400',
    badgeBorder: 'border-amber-500/30',
    dotColor: 'bg-amber-400'
  },
  'R3 Reject': {
    label: 'R3 Rejected',
    badgeBg: 'bg-rose-500/15',
    badgeText: 'text-rose-400',
    badgeBorder: 'border-rose-500/30',
    dotColor: 'bg-rose-400'
  },
  'Reject': {
    label: 'Rejected',
    badgeBg: 'bg-red-500/15',
    badgeText: 'text-red-400',
    badgeBorder: 'border-red-500/30',
    dotColor: 'bg-red-400'
  },
  'Approved': {
    label: 'Approved (Hired)',
    badgeBg: 'bg-emerald-500/15',
    badgeText: 'text-emerald-400',
    badgeBorder: 'border-emerald-500/30',
    dotColor: 'bg-emerald-400'
  }
};
