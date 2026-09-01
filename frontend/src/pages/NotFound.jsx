// =============================================
// NotFound.jsx - 404 Error Page
// =============================================

import React from 'react';
import { Link } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center text-center px-4 space-y-4">
      <div className="text-7xl font-extrabold bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">
        404
      </div>
      <h2 className="text-2xl font-bold text-white">Page Not Found</h2>
      <p className="text-slate-400 text-sm max-w-sm">
        The page you are looking for doesn't exist or has been moved.
      </p>
      <Link
        to="/"
        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold transition-all shadow-lg shadow-indigo-500/25"
      >
        <Home className="w-4 h-4" />
        <span>Return to Careers Portal</span>
      </Link>
    </div>
  );
}
