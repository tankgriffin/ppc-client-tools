// Simple Page Content Hook - Clean implementation for page-specific content processing

import { useState, useEffect, useCallback } from 'react';
import { useSimpleAI } from './useSimpleAI';
import { 
  SimpleProcessedContent, 
  SimplePageContext 
} from '../components/ai-lite/SimpleFallbackProcessor';

interface UseSimplePageContentResult {
  content: SimpleProcessedContent | null;
  isProcessing: boolean;
  error: any;
  refresh: () => Promise<void>;
}

// Page context definitions
const PAGE_CONTEXTS: Record<string, SimplePageContext> = {
  opportunities: {
    pageType: 'opportunities',
    focusKeywords: [
      'opportunity', 'market gap', 'potential', 'growth',
      'untapped market', 'niche', 'expansion', 'target audience',
      'market size', 'demand', 'trends', 'emerging'
    ],
    relevantPhases: ['phase1', 'phase3', 'phase4'],
    contentLength: 'detailed',
    outputFormat: 'insights'
  },
  strategy: {
    pageType: 'strategy',
    focusKeywords: [
      'positioning', 'strategy', 'value proposition', 'branding',
      'unique selling point', 'differentiation', 'market position',
      'brand positioning', 'strategic direction', 'competitive advantage'
    ],
    relevantPhases: ['phase4', 'phase5'],
    contentLength: 'detailed',
    outputFormat: 'insights'
  },
  timeline: {
    pageType: 'timeline',
    focusKeywords: [
      'implementation', 'execution', 'timeline', 'budget allocation', 
      'campaign setup', 'phases', 'milestones', 'resources',
      'roadmap', 'plan', 'deployment', 'launch'
    ],
    relevantPhases: ['phase5'],
    contentLength: 'comprehensive',
    outputFormat: 'bullets'
  },
  metrics: {
    pageType: 'metrics',
    focusKeywords: [
      'key findings', 'recommendations', 'roi', 'budget', 
      'timeline', 'success metrics', 'competitive advantage',
      'strategy', 'overview', 'summary', 'highlights'
    ],
    relevantPhases: ['phase1', 'phase4', 'phase5'],
    contentLength: 'brief',
    outputFormat: 'summary'
  }
};

export function useSimplePageContent(
  phases: any, 
  pageType: string,
  refreshTrigger?: string
): UseSimplePageContentResult {
  const [processedContent, setProcessedContent] = useState<SimpleProcessedContent | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<any>(null);

  const { isReady, processContent } = useSimpleAI();

  const processPageContent = useCallback(async () => {
    if (!phases || Object.keys(phases).length === 0) {
      setProcessedContent(null);
      return;
    }

    const context = PAGE_CONTEXTS[pageType];
    if (!context) {
      setProcessedContent(null);
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);

      console.log(`Processing page content for: ${pageType}`);
      
      // Extract relevant content from phases
      const relevantContent = extractRelevantContent(phases, context);
      
      if (relevantContent) {
        const result = await processContent(relevantContent, context);
        setProcessedContent(result);
      } else {
        setProcessedContent(null);
      }
    } catch (err) {
      console.error('Page content processing failed:', err);
      setError({
        code: 'PAGE_PROCESSING_FAILED',
        message: err instanceof Error ? err.message : 'Failed to process page content',
        recoverable: true
      });
      setProcessedContent(null);
    } finally {
      setIsProcessing(false);
    }
  }, [phases, pageType, processContent]);

  const refresh = useCallback(async () => {
    await processPageContent();
  }, [processPageContent]);

  // Auto-process when phases or page type changes
  useEffect(() => {
    if (isReady && phases) {
      processPageContent();
    }
  }, [phases, pageType, isReady, processPageContent]);

  // Handle manual refresh triggers
  useEffect(() => {
    if (refreshTrigger && isReady) {
      processPageContent();
    }
  }, [refreshTrigger, isReady, processPageContent]);

  return {
    content: processedContent,
    isProcessing,
    error,
    refresh
  };
}

function extractRelevantContent(phases: any, context: SimplePageContext): string {
  let relevantContent = '';
  
  // Extract content from relevant phases
  for (const phaseKey of context.relevantPhases) {
    const phaseData = phases[phaseKey];
    if (phaseData?.response) {
      relevantContent += phaseData.response + '\n\n';
    }
  }
  
  // If no relevant phases have content, use all available content
  if (!relevantContent.trim()) {
    const allPhases = Object.values(phases);
    for (const phase of allPhases) {
      if ((phase as any)?.response) {
        relevantContent += (phase as any).response + '\n\n';
      }
    }
  }
  
  return relevantContent.trim();
}