// =============================================
// StageBadge.jsx - Visual Status Tag for Candidates
// =============================================
// Displays a candidate's current stage with color-coded theme.
// =============================================

import React from 'react';
import { STAGE_CONFIG } from '../utils/constants';

export default function StageBadge({ stage, size = 'sm' }) {
  const config = STAGE_CONFIG[stage] || {
    label: stage || 'Unknown',
    badgeBg: 'bg-slate-800',
    badgeText: 'text-slate-300',
    badgeBorder: 'border-slate-700',
    dotColor: 'bg-slate-400'
  };

  const isSmall = size === 'sm';

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border font-medium ${config.badgeBg} ${config.badgeText} ${config.badgeBorder} ${
        isSmall ? 'px-2.5 py-0.5 text-xs' : 'px-3 py-1 text-sm'
      }`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${config.dotColor} animate-pulse`} />
      <span>{config.label}</span>
    </span>
  );
}
