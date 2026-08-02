import React from 'react';
import { AlertCircle, ExternalLink } from 'lucide-react';
import { T } from './T';

export default function MethodologyAlert({ 
  itText, 
  enText, 
  linkUrl, 
  linkText 
}) {
  return (
    <div className="w-full bg-indigo-900/10 border border-indigo-500/20 rounded-xl p-4 flex items-start gap-3 my-6">
      <div className="p-2 bg-indigo-500/20 rounded-lg shrink-0 mt-0.5">
        <AlertCircle className="w-4 h-4 text-indigo-400" />
      </div>
      <div className="flex-1">
        <h4 className="text-sm font-semibold text-indigo-300 mb-1">
          <T it="Nota Metodologica" en="Methodological Note" />
        </h4>
        <p className="text-xs text-zinc-400 leading-relaxed">
          <T it={itText} en={enText} />
        </p>
        {linkUrl && (
          <a 
            href={linkUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 mt-2 text-xs font-medium text-indigo-400 hover:text-indigo-300 transition-colors"
          >
            {linkText || 'Fonte Originale / Source'}
            <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>
    </div>
  );
}
