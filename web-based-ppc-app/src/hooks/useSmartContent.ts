// useSmartContent Hook - Manages smart content processing for specific pages
// Based on AI Summarization PRD specifications

import { useState, useEffect, useCallback } from 'react';
import { UseSmartContentResult, ProcessedContent, PageContext, AIError } from '../ai/types';
import { useAI } from './useAI';
import { contentRouter } from '../ai/processors/ContentRouter';

interface UseSmartContentProps {
  content: string;
  pageContext: PageContext;
  refreshTrigger?: string;
  autoRefresh?: boolean;
}

export function useSmartContent({
  content,
  pageContext,
  refreshTrigger,
  autoRefresh = true
}: UseSmartContentProps): UseSmartContentResult {
  const [processedContent, setProcessedContent] = useState<ProcessedContent | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<AIError | null>(null);
  
  const { isReady, processContent } = useAI();

  // Process content function
  const processCurrentContent = useCallback(async () => {
    if (!content || content.trim().length === 0) {
      setProcessedContent(null);
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);

      console.log(`Processing content for page: ${pageContext.pageType}`);
      const result = await processContent(content, pageContext);
      setProcessedContent(result);
    } catch (err) {
      console.error('Smart content processing failed:', err);
      setError(err as AIError);
      setProcessedContent(null);
    } finally {
      setIsProcessing(false);
    }
  }, [content, pageContext, processContent]);

  // Refresh function for manual triggering
  const refresh = useCallback(async () => {
    await processCurrentContent();
  }, [processCurrentContent]);

  // Auto-process when content or context changes
  useEffect(() => {
    if (autoRefresh && isReady && content) {
      processCurrentContent();
    }
  }, [content, pageContext, isReady, autoRefresh, processCurrentContent]);

  // Handle manual refresh triggers
  useEffect(() => {
    if (refreshTrigger && isReady) {
      processCurrentContent();
    }
  }, [refreshTrigger, isReady, processCurrentContent]);

  return {
    content: processedContent,
    isProcessing,
    error,
    refresh
  };
}

// Hook for processing multiple phases content for a specific page
export function usePageContent(
  phases: any, 
  pageType: string,
  refreshTrigger?: string
): UseSmartContentResult {
  const [processedContent, setProcessedContent] = useState<ProcessedContent | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<AIError | null>(null);

  const { isReady } = useAI();

  const processPageContent = useCallback(async () => {
    if (!phases || Object.keys(phases).length === 0) {
      setProcessedContent(null);
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);

      console.log(`Processing page content for: ${pageType}`);
      const result = await contentRouter.getContentForPage(pageType, phases);
      setProcessedContent(result);
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
  }, [phases, pageType]);

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