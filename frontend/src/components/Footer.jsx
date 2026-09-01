// =============================================
// Footer.jsx - Simple Modern Footer
// =============================================

import React from 'react';
import { Sparkles, Shield, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="w-full border-t border-slate-850 bg-slate-950 py-6 text-center text-xs text-slate-500">
      <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-indigo-400" />
          <span className="font-semibold text-slate-300">Enter Recruitment Platform</span>
          <span className="text-slate-600">|</span>
          <span>Confidential Assignment</span>
        </div>
        <div className="flex items-center gap-1 text-slate-400">
          <span>AI Fullstack Hiring System</span>
        </div>
      </div>
    </footer>
  );
}
