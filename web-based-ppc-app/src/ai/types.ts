// AI-related type definitions for PPC Strategic Intelligence Web App
// Based on AI Summarization PRD specifications

export enum PageType {
  EXECUTIVE_SUMMARY = 'executive-summary',
  COMPETITIVE_ANALYSIS = 'competitive-analysis', 
  MARKET_OPPORTUNITIES = 'market-opportunities',
  STRATEGIC_POSITIONING = 'strategic-positioning',
  IMPLEMENTATION_PLAN = 'implementation-plan',
  BUDGET_ALLOCATION = 'budget-allocation',
  RISK_ASSESSMENT = 'risk-assessment',
  KEYWORD_STRATEGY = 'keyword-strategy'
}

export interface PageContext {
  pageType: PageType;
  focusKeywords: string[];
  relevantPhases: string[];
  contentLength: 'brief' | 'detailed' | 'comprehensive';
  outputFormat: 'summary' | 'bullets' | 'insights' | 'metrics';
}

export interface ProcessedContent {
  summary: string;
  insights: Insight[];
  entities: Entity[];
  relevanceScore: number;
  confidence: number;
  sources: string[];
  processedAt: Date;
}

export interface Insight {
  id: string;
  type: 'opportunity' | 'threat' | 'recommendation' | 'finding';
  content: string;
  relevanceScore: number;
  confidence: number;
  source: string;
  phase: string;
  keywords: string[];
}

export interface Entity {
  text: string;
  type: 'competitor' | 'metric' | 'recommendation' | 'timeline' | 'budget' | 'keyword';
  confidence: number;
  context: string;
}

export interface RelevantContent {
  primaryContent: string;
  supportingContent: string[];
  allContent: string;
  sections: ContentSection[];
}

export interface ContentSection {
  id: string;
  title: string;
  content: string;
  phase: string;
  relevanceScore: number;
  type: 'heading' | 'paragraph' | 'list' | 'metric';
}

export interface ContentCategory {
  category: string;
  confidence: number;
  keywords: string[];
}

export interface PageInsights {
  summary: string;
  keyFindings: string[];
  recommendations: string[];
  metrics: ExtractedMetric[];
  competitors: CompetitorInsight[];
  risks: RiskInsight[];
}

export interface ExtractedMetric {
  name: string;
  value: string;
  type: 'budget' | 'timeline' | 'performance' | 'roi';
  confidence: number;
  source: string;
}

export interface CompetitorInsight {
  name: string;
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  source: string;
}

export interface RiskInsight {
  risk: string;
  impact: 'low' | 'medium' | 'high';
  likelihood: 'low' | 'medium' | 'high';
  mitigation: string;
  source: string;
}

export type ModelStatus = 'unloaded' | 'loading' | 'ready' | 'error';

export interface ModelInfo {
  name: string;
  status: ModelStatus;
  size: number;
  loadTime?: number;
  error?: string;
}

export interface CacheStats {
  modelCacheSize: number;
  resultCacheSize: number;
  totalEntries: number;
  hitRate: number;
  lastCleanup: Date;
}

export interface AIConfig {
  models: {
    summarization: {
      model: string;
      options: {
        max_length: number;
        min_length: number;
        do_sample: boolean;
        early_stopping: boolean;
      };
    };
    classification: {
      model: string;
      options: {
        hypothesis_template: string;
      };
    };
    embedding: {
      model: string;
      options: {
        pooling: string;
        normalize: boolean;
      };
    };
  };
  performance: {
    maxModelCacheSize: number;
    maxResultCacheSize: number;
    modelLoadTimeout: number;
    processingTimeout: number;
  };
}

export interface ProcessingRules {
  textCleaning: {
    removePatterns: RegExp[];
    normalizeWhitespace: boolean;
    minSentenceLength: number;
    maxSentenceLength: number;
  };
  relevanceScoring: {
    keywordMatch: number;
    semanticSimilarity: number;
    entityRelevance: number;
  };
  summarization: {
    maxSummaryRatio: number;
    minSummaryLength: number;
    maxSummaryLength: number;
    preserveKeyInsights: boolean;
  };
}

export interface AIError {
  code: string;
  message: string;
  details?: any;
  recoverable: boolean;
}

// Hook interfaces
export interface UseAIResult {
  isLoading: boolean;
  isReady: boolean;
  error: AIError | null;
  modelStatus: Record<string, ModelStatus>;
  processContent: (content: string, context: PageContext) => Promise<ProcessedContent>;
  clearCache: () => Promise<void>;
}

export interface UseSmartContentResult {
  content: ProcessedContent | null;
  isProcessing: boolean;
  error: AIError | null;
  refresh: () => Promise<void>;
}

// Component interfaces
export interface SmartSummaryProps {
  researchData: any; // ClaudePhases from existing types
  pageContext: PageContext;
  maxItems?: number;
  refreshTrigger?: string;
  showSources?: boolean;
  interactive?: boolean;
}

export interface SmartSummaryCardProps {
  title: string;
  content: string;
  confidence: number;
  sources: string[];
  actionable?: boolean;
  onActionClick?: () => void;
}

export interface InsightsSidebarProps {
  currentPageType: PageType;
  allPhases: any; // ClaudePhases
  onInsightClick: (insight: Insight) => void;
  maxInsights?: number;
}

export interface AIStatusProps {
  status: ModelStatus;
  progress?: number;
  modelInfo?: ModelInfo;
  onRetry?: () => void;
}

export interface ContentExplorerProps {
  phases: any; // ClaudePhases
  searchQuery?: string;
  filterByRelevance?: boolean;
  groupByTopic?: boolean;
  onContentSelect?: (content: ContentSection) => void;
}