// AI Module Exports
// Central export file for all AI-related functionality

// Types
export * from './types';

// Configuration
export { AI_CONFIG, PROCESSING_RULES, CACHE_CONFIG, checkBrowserCompatibility } from './config';

// Core Components (temporarily disabled for browser compatibility)
// export { modelManager } from './models/ModelManager';
// export { contentProcessor } from './processors/ContentProcessor';
// export { contentRouter } from './processors/ContentRouter';
export { cacheManager } from './cache/CacheManager';

// React Components (re-export from components)
export { SmartSummaryCard } from '../components/ai/SmartSummaryCard';
export { AIStatusIndicator, CompactAIStatus } from '../components/ai/AIStatusIndicator';

// React Hooks (re-export from hooks)
export { useAI } from '../hooks/useAI';
export { useSmartContent, usePageContent } from '../hooks/useSmartContent';