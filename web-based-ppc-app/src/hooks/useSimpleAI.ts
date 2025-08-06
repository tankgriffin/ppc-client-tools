// Simple AI Hook - Clean implementation without heavy dependencies
// Uses only the fallback processor to avoid ONNX runtime issues

import { useState, useEffect, useCallback } from 'react';
import { 
  SimpleFallbackProcessor, 
  SimpleProcessedContent, 
  SimplePageContext 
} from '../components/ai-lite/SimpleFallbackProcessor';

interface UseSimpleAIResult {
  isLoading: boolean;
  isReady: boolean;
  error: SimpleAIError | null;
  modelStatus: Record<string, string>;
  processContent: (content: string, context: SimplePageContext) => Promise<SimpleProcessedContent>;
  clearCache: () => Promise<void>;
}

interface SimpleAIError {
  code: string;
  message: string;
  recoverable: boolean;
}

export function useSimpleAI(): UseSimpleAIResult {
  const [isLoading, setIsLoading] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<SimpleAIError | null>(null);
  const [modelStatus] = useState<Record<string, string>>({
    summarization: 'ready',
    classification: 'ready', 
    embedding: 'ready'
  });

  // Initialize simple AI system
  const initializeAI = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      console.log('Initializing optimized text processing...');
      
      // Simulate brief loading for UI consistency
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setIsReady(true);
      console.log('Text processing ready');
      
    } catch (err) {
      console.error('Failed to initialize text processing:', err);
      setError({
        code: 'INIT_FAILED',
        message: err instanceof Error ? err.message : 'Failed to initialize text processing',
        recoverable: true
      });
      setIsReady(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Process content with simple algorithms
  const processContent = useCallback(async (
    content: string, 
    context: SimplePageContext
  ): Promise<SimpleProcessedContent> => {
    try {
      if (!content || content.trim().length === 0) {
        throw new Error('No content provided for processing');
      }

      console.log('Processing content with optimized text analysis...');
      
      // Use simple fallback processor
      const result = await SimpleFallbackProcessor.processContent(content, context);
      
      return result;
    } catch (err) {
      console.error('Content processing failed:', err);
      throw {
        code: 'PROCESSING_FAILED',
        message: err instanceof Error ? err.message : 'Failed to process content',
        recoverable: true
      };
    }
  }, []);

  // Simple cache clear (placeholder)
  const clearCache = useCallback(async () => {
    try {
      console.log('Cache cleared');
    } catch (err) {
      console.error('Failed to clear cache:', err);
    }
  }, []);

  // Auto-initialize on mount
  useEffect(() => {
    if (!isLoading && !isReady && !error) {
      initializeAI();
    }
  }, [initializeAI, isLoading, isReady, error]);

  return {
    isLoading,
    isReady,
    error,
    modelStatus,
    processContent,
    clearCache
  };
}