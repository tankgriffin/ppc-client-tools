// Core data models for PPC Strategic Intelligence Web App
// Based on PRD specifications

export interface Project {
  id: string;
  name: string;
  industry: string;
  created: Date;
  lastModified: Date;
  completionStatus: ProjectStatus;
  businessData: BusinessIntelligence;
  claudePhases: ClaudePhases;
  assets: ProjectAsset[];
  analysis: ProcessedInsights;
  tabContent?: {
    [key: string]: string;
  };
}

export interface BusinessIntelligence {
  businessName: string;
  industry: string;
  website: string;
  location: string;
  serviceArea: string;
  description: string;
  services: string;
  uniqueValue: string;
  targetAudience: string;
  customerPainPoints: string;
  competitors: string[];
  servicePackage: ServicePackage;
  primaryGoal: CampaignGoal;
  budgetRange: BudgetRange;
  successMetrics: string;
  seasonalTrends: string;
  currentMarketing: string;
  biggestChallenges: string;
}

export interface ClaudePhases {
  phase1: ClaudePhase; // Business Intelligence
  phase2: ClaudePhase; // Competitive Landscape
  phase3: ClaudePhase; // Market Gaps
  phase4: ClaudePhase; // Strategic Positioning
  phase5: ClaudePhase; // Content Strategy
}

export interface ClaudePhase {
  prompt: string;
  response: string;
  completed: boolean;
  lastModified: Date;
  insights: ExtractedInsight[];
}

export interface ProcessedInsights {
  executiveSummary: string;
  competitiveAdvantages: string[];
  marketOpportunities: MarketOpportunity[];
  implementationRoadmap: RoadmapItem[];
  riskAssessment: RiskItem[];
  keyMetrics: MetricItem[];
}

export interface ProjectAsset {
  id: string;
  name: string;
  type: AssetType;
  content: string; // base64 for images, text for documents
  uploadedAt: Date;
}

export interface ExtractedInsight {
  id: string;
  type: InsightType;
  content: string;
  priority: Priority;
  category: string;
  source: PhaseNumber;
}

export interface MarketOpportunity {
  id: string;
  title: string;
  description: string;
  impact: ImpactLevel;
  effort: EffortLevel;
  timeline: string;
  keyMetrics: string[];
}

export interface RoadmapItem {
  id: string;
  title: string;
  description: string;
  phase: ImplementationPhase;
  duration: string;
  dependencies: string[];
  resources: string[];
  milestones: Milestone[];
}

export interface RiskItem {
  id: string;
  title: string;
  description: string;
  likelihood: RiskLevel;
  impact: RiskLevel;
  mitigation: string;
  category: RiskCategory;
}

export interface MetricItem {
  id: string;
  name: string;
  value: number | string;
  unit: string;
  benchmark: string;
  trend: TrendDirection;
  category: MetricCategory;
}

export interface Milestone {
  id: string;
  title: string;
  dueDate: Date;
  completed: boolean;
  description: string;
}

// Enums and Union Types
export enum ProjectStatus {
  DRAFT = 'draft',
  IN_PROGRESS = 'in_progress',
  ANALYSIS = 'analysis',
  COMPLETED = 'completed',
  ARCHIVED = 'archived'
}

export enum ServicePackage {
  PPC_ONLY = 'ppc_only',
  SEO_ONLY = 'seo_only',
  PPC_SEO_COMBINED = 'ppc_seo_combined'
}

export enum CampaignGoal {
  LEAD_GENERATION = 'lead_generation',
  SALES = 'sales',
  BRAND_AWARENESS = 'brand_awareness',
  WEBSITE_TRAFFIC = 'website_traffic',
  LOCAL_VISIBILITY = 'local_visibility',
  ECOMMERCE = 'ecommerce'
}

export enum BudgetRange {
  UNDER_1K = 'under_1k',
  RANGE_1K_5K = '1k_5k',
  RANGE_5K_10K = '5k_10k',
  RANGE_10K_25K = '10k_25k',
  RANGE_25K_50K = '25k_50k',
  OVER_50K = 'over_50k'
}

export enum AssetType {
  IMAGE = 'image',
  DOCUMENT = 'document',
  LOGO = 'logo',
  BRAND_ASSET = 'brand_asset'
}

export enum InsightType {
  OPPORTUNITY = 'opportunity',
  THREAT = 'threat',
  RECOMMENDATION = 'recommendation',
  FINDING = 'finding',
  COMPETITOR_INTEL = 'competitor_intel'
}

export enum Priority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum PhaseNumber {
  PHASE_1 = 1,
  PHASE_2 = 2,
  PHASE_3 = 3,
  PHASE_4 = 4,
  PHASE_5 = 5
}

export enum ImpactLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  VERY_HIGH = 'very_high'
}

export enum EffortLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  VERY_HIGH = 'very_high'
}

export enum ImplementationPhase {
  IMMEDIATE = 'immediate',
  SHORT_TERM = 'short_term',
  MEDIUM_TERM = 'medium_term',
  LONG_TERM = 'long_term'
}

export enum RiskLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum RiskCategory {
  TECHNICAL = 'technical',
  MARKET = 'market',
  COMPETITIVE = 'competitive',
  BUDGET = 'budget',
  TIMELINE = 'timeline',
  REGULATORY = 'regulatory'
}

export enum TrendDirection {
  UP = 'up',
  DOWN = 'down',
  STABLE = 'stable',
  VOLATILE = 'volatile'
}

export enum MetricCategory {
  PERFORMANCE = 'performance',
  COMPETITIVE = 'competitive',
  MARKET = 'market',
  FINANCIAL = 'financial',
  OPERATIONAL = 'operational'
}

// Form and UI Types
export interface FormField {
  id: string;
  label: string;
  type: FieldType;
  required: boolean;
  placeholder?: string;
  options?: SelectOption[];
  validation?: ValidationRule[];
  helpText?: string;
}

export interface SelectOption {
  value: string;
  label: string;
  description?: string;
}

export interface ValidationRule {
  type: ValidationType;
  value?: any;
  message: string;
}

export enum FieldType {
  TEXT = 'text',
  TEXTAREA = 'textarea',
  SELECT = 'select',
  MULTISELECT = 'multiselect',
  NUMBER = 'number',
  EMAIL = 'email',
  URL = 'url',
  DATE = 'date',
  CHECKBOX = 'checkbox',
  RADIO = 'radio',
  FILE = 'file'
}

export enum ValidationType {
  REQUIRED = 'required',
  MIN_LENGTH = 'minLength',
  MAX_LENGTH = 'maxLength',
  EMAIL = 'email',
  URL = 'url',
  PATTERN = 'pattern'
}

// Navigation and UI State
export interface NavigationItem {
  id: string;
  label: string;
  href: string;
  icon?: string;
  badge?: string;
  children?: NavigationItem[];
}

export interface PageState {
  loading: boolean;
  error: string | null;
  saved: boolean;
  lastSaved?: Date;
}

// Export and Document Types
export interface ExportOptions {
  format: ExportFormat;
  includeCharts: boolean;
  includeAssets: boolean;
  sections: ExportSection[];
  template: DocumentTemplate;
}

export enum ExportFormat {
  DOCX = 'docx',
  PDF = 'pdf',
  JSON = 'json',
  MARKDOWN = 'markdown'
}

export enum ExportSection {
  EXECUTIVE_SUMMARY = 'executive_summary',
  BUSINESS_INTELLIGENCE = 'business_intelligence',
  COMPETITIVE_ANALYSIS = 'competitive_analysis',
  MARKET_OPPORTUNITIES = 'market_opportunities',
  STRATEGIC_POSITIONING = 'strategic_positioning',
  CONTENT_STRATEGY = 'content_strategy',
  IMPLEMENTATION_ROADMAP = 'implementation_roadmap',
  RISK_ASSESSMENT = 'risk_assessment',
  APPENDICES = 'appendices'
}

export enum DocumentTemplate {
  STANDARD = 'standard',
  EXECUTIVE = 'executive',
  TECHNICAL = 'technical',
  PRESENTATION = 'presentation'
}

// Chart and Visualization Types
export interface ChartData {
  id: string;
  title: string;
  type: ChartType;
  data: any[];
  config: ChartConfig;
}

export interface ChartConfig {
  xAxis?: string;
  yAxis?: string;
  colorScheme?: string[];
  showLegend?: boolean;
  showGrid?: boolean;
  animate?: boolean;
}

export enum ChartType {
  BAR = 'bar',
  LINE = 'line',
  PIE = 'pie',
  SCATTER = 'scatter',
  AREA = 'area',
  RADAR = 'radar',
  TREEMAP = 'treemap',
  SANKEY = 'sankey'
}

// Storage and Persistence Types
export interface StorageConfig {
  autoSaveInterval: number; // milliseconds
  maxStorageSize: number; // bytes
  compressionEnabled: boolean;
  backupEnabled: boolean;
}

export interface BackupData {
  version: string;
  timestamp: Date;
  projects: Project[];
  settings: UserSettings;
}

export interface UserSettings {
  theme: Theme;
  language: string;
  autoSave: boolean;
  notifications: boolean;
  defaultIndustry?: string;
  recentProjects: string[];
}

export enum Theme {
  LIGHT = 'light',
  DARK = 'dark',
  SYSTEM = 'system'
}

// API and Integration Types (for future use)
export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: Date;
}

export interface IntegrationConfig {
  name: string;
  enabled: boolean;
  apiKey?: string;
  settings: Record<string, any>;
}

// Utility Types
export type PartialProject = Partial<Project> & Pick<Project, 'id' | 'name'>;
export type CreateProjectData = Omit<Project, 'id' | 'created' | 'lastModified'>;
export type UpdateProjectData = Partial<Omit<Project, 'id' | 'created'>>;

export type PhaseKey = keyof ClaudePhases;
export type PhaseData = ClaudePhases[PhaseKey];

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type RequireAtLeastOne<T, Keys extends keyof T = keyof T> = 
  Pick<T, Exclude<keyof T, Keys>> & 
  { [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>> }[Keys];