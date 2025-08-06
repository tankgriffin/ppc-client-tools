// AI Status Indicator Component - Shows AI processing status and model loading
// Based on AI Summarization PRD specifications

import React from 'react';
import { Loader2, CheckCircle, AlertCircle, Sparkles, RefreshCw, Download } from 'lucide-react';
import { AIStatusProps } from '../../ai/types';

export function AIStatusIndicator({
  status,
  progress = 0,
  modelInfo,
  onRetry
}: AIStatusProps) {
  const getStatusConfig = () => {
    switch (status) {
      case 'loading':
        return {
          icon: Download,
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          message: 'Loading AI models...',
          showProgress: true
        };
      case 'processing':
        return {
          icon: Loader2,
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          message: 'Processing content...',
          showProgress: true,
          spinning: true
        };
      case 'ready':
        return {
          icon: CheckCircle,
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          message: 'AI ready'
        };
      case 'error':
        return {
          icon: AlertCircle,
          color: 'text-red-600',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
          message: 'AI unavailable'
        };
      default:
        return {
          icon: Sparkles,
          color: 'text-gray-600',
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200',
          message: 'AI not loaded'
        };
    }
  };

  const config = getStatusConfig();
  const IconComponent = config.icon;

  // Build className strings separately to avoid template literal issues
  const containerClasses = `inline-flex items-center px-3 py-2 rounded-lg border ${config.bgColor} ${config.borderColor}`;
  const iconClasses = `h-4 w-4 ${config.color}${config.spinning ? ' animate-spin' : ''}`;
  const textClasses = `text-sm font-medium ${config.color}`;
  const progressBarClasses = 'bg-blue-600 h-2 rounded-full transition-all duration-300';

  return (
    <div className={containerClasses}>
      <div className="flex items-center space-x-2">
        <IconComponent className={iconClasses} />
        <span className={textClasses}>
          {config.message}
        </span>
      </div>

      {/* Progress Bar */}
      {config.showProgress && progress > 0 && (
        <div className="ml-3 w-20 bg-gray-200 rounded-full h-2">
          <div 
            className={progressBarClasses}
            style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
          ></div>
        </div>
      )}

      {/* Progress Percentage */}
      {config.showProgress && progress > 0 && (
        <span className="ml-2 text-xs text-gray-500">
          {Math.round(progress)}%
        </span>
      )}

      {/* Model Info */}
      {modelInfo && status === 'ready' && (
        <div className="ml-3 text-xs text-gray-500">
          {modelInfo.loadTime && (
            <span>Loaded in {Math.round(modelInfo.loadTime / 1000)}s</span>
          )}
        </div>
      )}

      {/* Error Info */}
      {status === 'error' && modelInfo?.error && (
        <div className="ml-2 text-xs text-red-600 max-w-xs truncate" title={modelInfo.error}>
          {modelInfo.error}
        </div>
      )}

      {/* Retry Button */}
      {status === 'error' && onRetry && (
        <button
          onClick={onRetry}
          className="ml-2 inline-flex items-center text-xs text-red-600 hover:text-red-800 font-medium"
        >
          <RefreshCw className="h-3 w-3 mr-1" />
          Retry
        </button>
      )}
    </div>
  );
}

// Compact version for smaller spaces
export function CompactAIStatus({ status }: { status: string }) {
  const getStatusIcon = () => {
    switch (status) {
      case 'loading':
        return <Download className="h-3 w-3 text-blue-500" />;
      case 'processing':
        return <Loader2 className="h-3 w-3 text-blue-500 animate-spin" />;
      case 'ready':
        return <CheckCircle className="h-3 w-3 text-green-500" />;
      case 'error':
        return <AlertCircle className="h-3 w-3 text-red-500" />;
      default:
        return <Sparkles className="h-3 w-3 text-gray-400" />;
    }
  };

  return (
    <div className="inline-flex items-center" title={`AI Status: ${status}`}>
      {getStatusIcon()}
    </div>
  );
}