// AI Configuration for PPC Strategic Intelligence Web App
// Based on AI Summarization PRD specifications

import { AIConfig, ProcessingRules } from './types';

export const AI_CONFIG: AIConfig = {
  models: {
    summarization: {
      model: 'Xenova/distilbart-cnn-6-12',
      options: {
        max_length: 200,
        min_length: 50,
        do_sample: false,
        early_stopping: true
      }
    },
    classification: {
      model: 'Xenova/distilbert-base-uncased-mnli',
      options: {
        hypothesis_template: 'This content is about {}.'
      }
    },
    embedding: {
      model: 'Xenova/all-MiniLM-L6-v2',
      options: {
        pooling: 'mean',
        normalize: true
      }
    }
  },
  performance: {
    maxModelCacheSize: 500 * 1024 * 1024, // 500MB
    maxResultCacheSize: 50 * 1024 * 1024,  // 50MB
    modelLoadTimeout: 30000, // 30 seconds
    processingTimeout: 10000  // 10 seconds
  }
};

export const PROCESSING_RULES: ProcessingRules = {
  textCleaning: {
    removePatterns: [
      /\*\*([^*]+)\*\*/g, // Remove markdown bold
      /\*([^*]+)\*/g,     // Remove markdown italic  
      /#{1,6}\s/g,        // Remove markdown headers
      /```[\s\S]*?```/g,  // Remove code blocks
      /^\s*[-*+]\s+/gm,   // Remove bullet points
      /^\s*\d+\.\s+/gm,   // Remove numbered lists
      /\[([^\]]+)\]\([^)]+\)/g, // Remove markdown links
    ],
    normalizeWhitespace: true,
    minSentenceLength: 10,
    maxSentenceLength: 500
  },
  
  relevanceScoring: {
    keywordMatch: 0.4,      // 40% weight for keyword matching
    semanticSimilarity: 0.4, // 40% weight for semantic similarity
    entityRelevance: 0.2     // 20% weight for entity relevance
  },
  
  summarization: {
    maxSummaryRatio: 0.3,    // Summary should be max 30% of original
    minSummaryLength: 50,
    maxSummaryLength: 300,
    preserveKeyInsights: true
  }
};

export const CACHE_CONFIG = {
  modelCacheTTL: 7 * 24 * 60 * 60 * 1000,    // 7 days
  resultCacheTTL: 24 * 60 * 60 * 1000,       // 24 hours
  maxCacheEntries: 100,
  compressionEnabled: true
};

// Browser compatibility check
export const checkBrowserCompatibility = (): { supported: boolean; issues: string[] } => {
  const issues: string[] = [];

  // Check WebAssembly support
  if (typeof WebAssembly === 'undefined') {
    issues.push('WebAssembly not supported');
  }

  // Check Worker support for background processing
  if (typeof Worker === 'undefined') {
    issues.push('Web Workers not supported');
  }

  // Check IndexedDB for caching
  if (!window.indexedDB) {
    issues.push('IndexedDB not supported');
  }

  // Check minimum memory (rough estimate)
  if (navigator.deviceMemory && navigator.deviceMemory < 2) {
    issues.push('Insufficient device memory (minimum 2GB recommended)');
  }

  return {
    supported: issues.length === 0,
    issues
  };
};