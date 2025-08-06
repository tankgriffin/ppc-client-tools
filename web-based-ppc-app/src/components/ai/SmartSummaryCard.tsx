// Smart Summary Card Component - Displays AI-processed content with confidence indicators
// Based on AI Summarization PRD specifications

import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Sparkles, ExternalLink, Info } from 'lucide-react';
import { SmartSummaryCardProps } from '../../ai/types';
import { FormattedText } from '../FormattedText';

export function SmartSummaryCard({
  title,
  content,
  confidence,
  sources,
  actionable = false,
  onActionClick
}: SmartSummaryCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [showSources, setShowSources] = useState(false);

  const getConfidenceLevel = (confidence: number): { level: string; color: string; bgColor: string } => {
    if (confidence >= 0.8) {
      return { level: 'High', color: 'text-green-700', bgColor: 'bg-green-100' };
    } else if (confidence >= 0.6) {
      return { level: 'Medium', color: 'text-yellow-700', bgColor: 'bg-yellow-100' };
    } else {
      return { level: 'Low', color: 'text-red-700', bgColor: 'bg-red-100' };
    }
  };

  const confidenceInfo = getConfidenceLevel(confidence);
  const preview = content.length > 200 ? content.substring(0, 200) + '...' : content;
  
  // Build className strings separately to avoid template literal issues  
  const confidenceBadgeClasses = `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${confidenceInfo.bgColor} ${confidenceInfo.color}`;

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-blue-500" />
            <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          </div>
          <div className="flex items-center space-x-2">
            <span className={confidenceBadgeClasses}>
              <div className="w-2 h-2 rounded-full bg-current mr-1"></div>
              {confidenceInfo.level} Confidence
            </span>
            {actionable && (
              <button
                onClick={onActionClick}
                className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors"
              >
                <ExternalLink className="h-3 w-3 mr-1" />
                Take Action
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <div className="text-gray-700 leading-relaxed">
          <FormattedText 
            text={isExpanded ? content : preview}
            className="text-sm"
          />
        </div>

        {/* Expand/Collapse Button */}
        {content.length > 200 && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="mt-3 inline-flex items-center text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            {isExpanded ? (
              <>
                <ChevronUp className="h-4 w-4 mr-1" />
                Show Less
              </>
            ) : (
              <>
                <ChevronDown className="h-4 w-4 mr-1" />
                Show More
              </>
            )}
          </button>
        )}
      </div>

      {/* Footer */}
      <div className="px-4 py-3 bg-gray-50 border-t border-gray-100 rounded-b-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-500 flex items-center">
              <Sparkles className="h-3 w-3 mr-1" />
              AI Generated Summary
            </span>
            <div className="text-xs text-gray-400">•</div>
            <span className="text-xs text-gray-500">
              {Math.round(confidence * 100)}% confidence
            </span>
          </div>
          
          {sources.length > 0 && (
            <button
              onClick={() => setShowSources(!showSources)}
              className="inline-flex items-center text-xs text-gray-500 hover:text-gray-700"
            >
              <Info className="h-3 w-3 mr-1" />
              {sources.length} source{sources.length > 1 ? 's' : ''}
            </button>
          )}
        </div>

        {/* Sources Dropdown */}
        {showSources && sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs font-medium text-gray-700 mb-2">Sources:</p>
            <div className="space-y-1">
              {sources.map((source, index) => (
                <div key={index} className="text-xs text-gray-600 bg-white px-2 py-1 rounded border">
                  {source}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}