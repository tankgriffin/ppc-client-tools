// useAI Hook - Manages AI model loading and content processing
// Based on AI Summarization PRD specifications

import { useState, useEffect, useCallback } from 'react';
import { UseAIResult, ProcessedContent, PageContext, AIError, ModelStatus } from '../ai/types';
// Temporarily disable heavy AI imports to avoid ONNX runtime issues
// import { modelManager } from '../ai/models/ModelManager';
// import { contentProcessor } from '../ai/processors/ContentProcessor';
// import { contentRouter } from '../ai/processors/ContentRouter'; // Will be used for future features
import { cacheManager } from '../ai/cache/CacheManager';
import { FallbackProcessor } from '../ai/fallback/FallbackProcessor';

export function useAI(): UseAIResult {
  const [isLoading, setIsLoading] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<AIError | null>(null);
  const [modelStatus, setModelStatus] = useState<Record<string, ModelStatus>>({});

  // Initialize AI models
  const initializeAI = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      console.log('Initializing AI system...');
      
      // For now, skip the heavy AI models and use fallback processing only
      // This ensures the application works while we resolve ONNX runtime issues
      console.log('Using fallback text processing (AI models disabled for browser compatibility)');
      setError({
        code: 'MODELS_DISABLED',
        message: 'Using optimized text processing (full AI models disabled for compatibility)',
        recoverable: false
      });
      
      // Set as "ready" since we have fallback processing
      setIsReady(true);
      setModelStatus({
        summarization: 'unloaded',
        classification: 'unloaded', 
        embedding: 'unloaded'
      });
      
    } catch (err) {
      console.error('Failed to initialize AI system:', err);
      setError({
        code: 'INIT_FAILED',
        message: err instanceof Error ? err.message : 'Failed to initialize AI',
        recoverable: true
      });
      setIsReady(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Process content with AI
  const processContent = useCallback(async (
    content: string, 
    context: PageContext
  ): Promise<ProcessedContent> => {
    try {
      if (!content || content.trim().length === 0) {
        throw new Error('No content provided for processing');
      }

      // Check cache first
      const cacheKey = cacheManager.generateCacheKey(content, context);
      const cachedResult = await cacheManager.getCachedResult(cacheKey);
      
      if (cachedResult) {
        console.log('Returning cached AI result');
        return cachedResult;
      }

      console.log('Processing content with AI...');
      
      // For now, always use fallback processing to avoid ONNX runtime issues
      console.log('Using optimized text processing');
      const result = await FallbackProcessor.processContent(content, context);

      // Cache the result
      try {
        await cacheManager.cacheProcessingResult(cacheKey, result);
      } catch (cacheError) {
        console.warn('Failed to cache AI result:', cacheError);
      }

      return result;
    } catch (err) {
      console.error('Content processing failed:', err);
      throw {
        code: 'PROCESSING_FAILED',
        message: err instanceof Error ? err.message : 'Failed to process content',
        recoverable: true
      };
    }
  }, [isReady]);

  // Clear cache
  const clearCache = useCallback(async () => {
    try {
      await cacheManager.clearAllCache();
      console.log('AI cache cleared');
    } catch (err) {
      console.error('Failed to clear AI cache:', err);
    }
  }, []);

  // Monitor model status
  useEffect(() => {
    const updateStatus = () => {
      setModelStatus(modelManager.getModelStatus());
      setIsReady(modelManager.isReady());
    };

    // Update status immediately
    updateStatus();

    // Set up periodic status checks
    const interval = setInterval(updateStatus, 2000);

    return () => clearInterval(interval);
  }, []);

  // Auto-initialize on mount
  useEffect(() => {
    // Only initialize if not already loading or ready
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