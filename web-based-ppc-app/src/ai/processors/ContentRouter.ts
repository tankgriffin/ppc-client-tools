// Context-Aware Content Router for page-specific content extraction
// Routes and filters content based on page context and relevance

import { 
  PageContext, 
  PageType, 
  RelevantContent, 
  ContentSection, 
  PageInsights,
  ProcessedContent
} from '../types';
import { contentProcessor } from './ContentProcessor';
import { modelManager } from '../models/ModelManager';

class ContentRouter {
  private pageContexts: Map<PageType, PageContext> = new Map();

  constructor() {
    this.initializePageContexts();
  }

  private initializePageContexts() {
    // Executive Summary Context
    this.pageContexts.set(PageType.EXECUTIVE_SUMMARY, {
      pageType: PageType.EXECUTIVE_SUMMARY,
      focusKeywords: [
        'key findings', 'recommendations', 'roi', 'budget', 
        'timeline', 'success metrics', 'competitive advantage',
        'strategy', 'overview', 'summary', 'highlights'
      ],
      relevantPhases: ['phase1', 'phase4', 'phase5'],
      contentLength: 'brief',
      outputFormat: 'summary'
    });

    // Market Opportunities Context
    this.pageContexts.set(PageType.MARKET_OPPORTUNITIES, {
      pageType: PageType.MARKET_OPPORTUNITIES,
      focusKeywords: [
        'opportunity', 'market gap', 'potential', 'growth',
        'untapped market', 'niche', 'expansion', 'target audience',
        'market size', 'demand', 'trends', 'emerging'
      ],
      relevantPhases: ['phase1', 'phase3', 'phase4'],
      contentLength: 'detailed',
      outputFormat: 'insights'
    });

    // Competitive Analysis Context
    this.pageContexts.set(PageType.COMPETITIVE_ANALYSIS, {
      pageType: PageType.COMPETITIVE_ANALYSIS,
      focusKeywords: [
        'competitors', 'competition', 'market position', 'advantages', 
        'weaknesses', 'differentiation', 'market share', 'positioning',
        'competitive landscape', 'rivals', 'benchmarking'
      ],
      relevantPhases: ['phase2', 'phase3'],
      contentLength: 'detailed',
      outputFormat: 'insights'
    });

    // Strategic Positioning Context
    this.pageContexts.set(PageType.STRATEGIC_POSITIONING, {
      pageType: PageType.STRATEGIC_POSITIONING,
      focusKeywords: [
        'positioning', 'strategy', 'value proposition', 'branding',
        'unique selling point', 'differentiation', 'market position',
        'brand positioning', 'strategic direction', 'competitive advantage'
      ],
      relevantPhases: ['phase4', 'phase5'],
      contentLength: 'detailed',
      outputFormat: 'insights'
    });

    // Implementation Plan Context
    this.pageContexts.set(PageType.IMPLEMENTATION_PLAN, {
      pageType: PageType.IMPLEMENTATION_PLAN,
      focusKeywords: [
        'implementation', 'execution', 'timeline', 'budget allocation', 
        'campaign setup', 'phases', 'milestones', 'resources',
        'roadmap', 'plan', 'deployment', 'launch'
      ],
      relevantPhases: ['phase5'],
      contentLength: 'comprehensive',
      outputFormat: 'bullets'
    });
  }

  getPageContext(pageType: PageType): PageContext | null {
    return this.pageContexts.get(pageType) || null;
  }

  async getRelevantContent(context: PageContext, allPhases: any): Promise<RelevantContent> {
    const sections: ContentSection[] = [];
    let primaryContent = '';
    const supportingContent: string[] = [];
    
    // Process each relevant phase
    for (const phaseKey of context.relevantPhases) {
      const phaseData = allPhases[phaseKey];
      if (!phaseData?.response) continue;

      const phaseSections = await this.extractSectionsFromPhase(
        phaseKey, 
        phaseData.response, 
        context
      );
      
      sections.push(...phaseSections);
    }

    // Sort sections by relevance score
    sections.sort((a, b) => b.relevanceScore - a.relevanceScore);

    // Determine primary content (highest relevance)
    if (sections.length > 0) {
      primaryContent = sections[0].content;
      supportingContent.push(...sections.slice(1, 5).map(s => s.content));
    }

    const allContent = sections.map(s => s.content).join('\n\n');

    return {
      primaryContent,
      supportingContent,
      allContent,
      sections
    };
  }

  private async extractSectionsFromPhase(
    phaseKey: string, 
    response: string, 
    context: PageContext
  ): Promise<ContentSection[]> {
    const sections: ContentSection[] = [];
    const lines = response.split('\n');
    let currentSection = '';
    let currentContent: string[] = [];
    let sectionIndex = 0;

    const flushSection = () => {
      if (currentSection && currentContent.length > 0) {
        const content = currentContent.join('\n').trim();
        const relevanceScore = contentProcessor.scoreContentRelevance(content, context);
        
        if (relevanceScore >= 0.3) { // Only include moderately relevant content
          sections.push({
            id: `${phaseKey}-section-${sectionIndex++}`,
            title: currentSection,
            content,
            phase: `Phase ${phaseKey.slice(-1)}`,
            relevanceScore,
            type: this.determineSectionType(currentSection)
          });
        }
      }
    };

    lines.forEach(line => {
      const trimmedLine = line.trim();
      
      // Check for H1 or H2 headings
      if (trimmedLine.match(/^#{1,2}\s+(.+)/)) {
        flushSection();
        currentSection = trimmedLine.replace(/^#{1,2}\s+/, '');
        currentContent = [];
      } else if (currentSection && trimmedLine.length > 0) {
        currentContent.push(line);
      }
    });

    // Don't forget the last section
    flushSection();

    return sections;
  }

  private determineSectionType(title: string): 'heading' | 'paragraph' | 'list' | 'metric' {
    const lowerTitle = title.toLowerCase();
    
    if (lowerTitle.includes('metric') || lowerTitle.includes('kpi') || 
        lowerTitle.includes('measurement') || lowerTitle.includes('performance')) {
      return 'metric';
    }
    
    if (lowerTitle.includes('list') || lowerTitle.includes('summary') ||
        lowerTitle.includes('key') || lowerTitle.includes('main')) {
      return 'list';
    }
    
    return 'heading';
  }

  async scoreContentRelevance(content: string, context: PageContext): Promise<number> {
    try {
      // Use the content processor's relevance scoring
      const basicScore = contentProcessor.scoreContentRelevance(content, context);
      
      // Enhance with AI classification if models are ready
      if (modelManager.isReady()) {
        const classifications = await contentProcessor.classifyContent(
          content,
          context.focusKeywords
        );
        
        if (classifications.length > 0) {
          const avgClassificationScore = classifications.reduce((sum, c) => sum + c.confidence, 0) / classifications.length;
          return (basicScore * 0.7) + (avgClassificationScore * 0.3);
        }
      }
      
      return basicScore;
    } catch (error) {
      console.error('Error scoring content relevance:', error);
      return contentProcessor.scoreContentRelevance(content, context);
    }
  }

  async extractPageSpecificInsights(pageType: PageType, phases: any): Promise<PageInsights> {
    const context = this.getPageContext(pageType);
    if (!context) {
      throw new Error(`No context defined for page type: ${pageType}`);
    }

    const relevantContent = await this.getRelevantContent(context, phases);
    
    // Generate summary
    let summary = '';
    try {
      summary = await contentProcessor.generateSummary(
        relevantContent.primaryContent, 
        context.contentLength === 'brief' ? 150 : 
        context.contentLength === 'detailed' ? 250 : 350
      );
    } catch (error) {
      console.error('Failed to generate summary:', error);
      summary = relevantContent.primaryContent.substring(0, 200) + '...';
    }

    // Extract insights from all relevant content
    const insights = contentProcessor.extractInsights(relevantContent.allContent, context);
    
    // Categorize insights
    const keyFindings = insights
      .filter(i => i.type === 'finding')
      .slice(0, 5)
      .map(i => i.content);
    
    const recommendations = insights
      .filter(i => i.type === 'recommendation')
      .slice(0, 5)
      .map(i => i.content);

    // Extract metrics
    const metrics = contentProcessor.extractMetrics(relevantContent.allContent);

    // Extract competitors (simplified for now)
    const competitors = this.extractCompetitorInsights(relevantContent.allContent);

    // Extract risks (simplified for now)
    const risks = this.extractRiskInsights(relevantContent.allContent);

    return {
      summary,
      keyFindings,
      recommendations,
      metrics,
      competitors,
      risks
    };
  }

  private extractCompetitorInsights(content: string): any[] {
    // Simplified competitor extraction
    const entities = contentProcessor.extractEntities(content);
    const competitors = entities.filter(e => e.type === 'competitor');
    
    return competitors.slice(0, 3).map(comp => ({
      name: comp.text,
      strengths: ['Strong market presence'], // Placeholder
      weaknesses: ['Limited digital presence'], // Placeholder
      opportunities: ['Gap in specific market segment'], // Placeholder
      source: comp.context
    }));
  }

  private extractRiskInsights(content: string): any[] {
    // Simplified risk extraction
    const insights = contentProcessor.extractInsights(content, {
      pageType: PageType.RISK_ASSESSMENT,
      focusKeywords: ['risk', 'threat', 'challenge'],
      relevantPhases: [],
      contentLength: 'brief',
      outputFormat: 'insights'
    });
    
    const risks = insights.filter(i => i.type === 'threat');
    
    return risks.slice(0, 3).map(risk => ({
      risk: risk.content,
      impact: 'medium' as const,
      likelihood: 'medium' as const,
      mitigation: 'Develop mitigation strategy', // Placeholder
      source: risk.phase
    }));
  }

  async generateContextualSummary(contents: string[], context: PageContext): Promise<string> {
    try {
      const combinedContent = contents.join('\n\n');
      const maxLength = context.contentLength === 'brief' ? 150 : 
                      context.contentLength === 'detailed' ? 250 : 350;
      
      return await contentProcessor.generateSummary(combinedContent, maxLength);
    } catch (error) {
      console.error('Failed to generate contextual summary:', error);
      
      // Fallback to simple truncation
      const combinedContent = contents.join(' ');
      const maxLength = context.contentLength === 'brief' ? 150 : 250;
      return combinedContent.length > maxLength 
        ? combinedContent.substring(0, maxLength) + '...'
        : combinedContent;
    }
  }

  // Helper method to get content for specific page types
  async getContentForPage(pageType: string, phases: any): Promise<ProcessedContent | null> {
    try {
      // Map string pageType to enum
      const mappedPageType = this.mapStringToPageType(pageType);
      if (!mappedPageType) return null;

      const insights = await this.extractPageSpecificInsights(mappedPageType, phases);
      
      return {
        summary: insights.summary,
        insights: [], // Will be populated by individual insight extraction
        entities: [], // Will be populated by entity extraction
        relevanceScore: 0.8,
        confidence: 0.85,
        sources: Object.keys(phases),
        processedAt: new Date()
      };
    } catch (error) {
      console.error('Error getting content for page:', error);
      return null;
    }
  }

  private mapStringToPageType(pageType: string): PageType | null {
    const mapping: Record<string, PageType> = {
      'opportunities': PageType.MARKET_OPPORTUNITIES,
      'strategy': PageType.STRATEGIC_POSITIONING,
      'timeline': PageType.IMPLEMENTATION_PLAN,
      'metrics': PageType.EXECUTIVE_SUMMARY, // Use executive summary for metrics
      'overview': PageType.EXECUTIVE_SUMMARY
    };

    return mapping[pageType] || null;
  }
}

export const contentRouter = new ContentRouter();