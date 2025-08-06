// Content Processing Pipeline for AI-powered text analysis
// Handles text cleaning, entity extraction, and content structuring

import nlp from 'compromise';
import { stemmer } from 'stemmer';
import { 
  ProcessedContent, 
  Insight, 
  Entity, 
  ContentSection, 
  PageContext,
  ExtractedMetric,
  CompetitorInsight,
  RiskInsight
} from '../types';
import { PROCESSING_RULES } from '../config';
import { modelManager } from '../models/ModelManager';

class ContentProcessor {
  private sentenceCache = new Map<string, string[]>();

  cleanText(text: string): string {
    if (!text || typeof text !== 'string') {
      return '';
    }

    let cleaned = text;

    // Apply cleaning patterns from config
    PROCESSING_RULES.textCleaning.removePatterns.forEach(pattern => {
      cleaned = cleaned.replace(pattern, ' ');
    });

    if (PROCESSING_RULES.textCleaning.normalizeWhitespace) {
      // Normalize whitespace
      cleaned = cleaned.replace(/\s+/g, ' ');
      cleaned = cleaned.replace(/\n\s*\n/g, '\n');
      cleaned = cleaned.trim();
    }

    return cleaned;
  }

  segmentSentences(text: string): string[] {
    const cacheKey = text.substring(0, 100); // Use first 100 chars as cache key
    if (this.sentenceCache.has(cacheKey)) {
      return this.sentenceCache.get(cacheKey)!;
    }

    const cleaned = this.cleanText(text);
    const doc = nlp(cleaned);
    const sentences = doc.sentences().out('array') as string[];

    // Filter sentences by length rules
    const filtered = sentences.filter(sentence => {
      const length = sentence.trim().length;
      return length >= PROCESSING_RULES.textCleaning.minSentenceLength &&
             length <= PROCESSING_RULES.textCleaning.maxSentenceLength;
    });

    this.sentenceCache.set(cacheKey, filtered);
    return filtered;
  }

  extractKeywords(text: string): string[] {
    const doc = nlp(text);
    
    // Extract nouns, adjectives, and organizations
    const nouns = doc.nouns().out('array') as string[];
    const adjectives = doc.adjectives().out('array') as string[];
    const organizations = doc.organizations().out('array') as string[];
    
    // Combine and deduplicate
    const allKeywords = [...nouns, ...adjectives, ...organizations];
    const uniqueKeywords = Array.from(new Set(allKeywords));
    
    // Stem keywords for better matching
    const stemmedKeywords = uniqueKeywords.map(keyword => 
      stemmer(keyword.toLowerCase())
    );

    return Array.from(new Set(stemmedKeywords));
  }

  extractEntities(text: string): Entity[] {
    const doc = nlp(text);
    const entities: Entity[] = [];

    // Extract organizations (competitors)
    const organizations = doc.organizations().out('array') as string[];
    organizations.forEach(org => {
      entities.push({
        text: org,
        type: 'competitor',
        confidence: 0.8,
        context: this.getEntityContext(text, org)
      });
    });

    // Extract monetary values (budget)
    const money = doc.money().out('array') as string[];
    money.forEach(amount => {
      entities.push({
        text: amount,
        type: 'budget',
        confidence: 0.9,
        context: this.getEntityContext(text, amount)
      });
    });

    // Extract time periods (timeline)
    const dates = doc.dates().out('array') as string[];
    dates.forEach(date => {
      entities.push({
        text: date,
        type: 'timeline',
        confidence: 0.7,
        context: this.getEntityContext(text, date)
      });
    });

    // Extract percentages and numbers (metrics)
    const percentageRegex = /\b\d+(?:\.\d+)?%\b/g;
    const percentages = text.match(percentageRegex) || [];
    percentages.forEach(percentage => {
      entities.push({
        text: percentage,
        type: 'metric',
        confidence: 0.9,
        context: this.getEntityContext(text, percentage)
      });
    });

    // Extract recommendation indicators
    const recommendationPatterns = [
      /recommend(?:ed|ation|s)?\s+([^.!?]+)/gi,
      /should\s+([^.!?]+)/gi,
      /need(?:s)?\s+to\s+([^.!?]+)/gi
    ];

    recommendationPatterns.forEach(pattern => {
      const matches = text.match(pattern) || [];
      matches.forEach(match => {
        entities.push({
          text: match.trim(),
          type: 'recommendation',
          confidence: 0.8,
          context: this.getEntityContext(text, match)
        });
      });
    });

    return entities;
  }

  private getEntityContext(text: string, entity: string): string {
    const entityIndex = text.toLowerCase().indexOf(entity.toLowerCase());
    if (entityIndex === -1) return '';

    const contextStart = Math.max(0, entityIndex - 50);
    const contextEnd = Math.min(text.length, entityIndex + entity.length + 50);
    
    return text.substring(contextStart, contextEnd).trim();
  }

  async generateSummary(text: string, maxLength: number = 200): Promise<string> {
    try {
      const summarizer = await modelManager.getSummarizer();
      
      // Clean and prepare text for summarization
      const cleanedText = this.cleanText(text);
      
      // Ensure text is not too short or too long
      if (cleanedText.length < PROCESSING_RULES.summarization.minSummaryLength) {
        return cleanedText;
      }

      // Truncate if too long (models have input limits)
      const maxInputLength = 1000;
      const inputText = cleanedText.length > maxInputLength 
        ? cleanedText.substring(0, maxInputLength) + '...'
        : cleanedText;

      const result = await summarizer(inputText, {
        max_length: Math.min(maxLength, PROCESSING_RULES.summarization.maxSummaryLength),
        min_length: PROCESSING_RULES.summarization.minSummaryLength,
        do_sample: false
      });

      // Handle the result based on the model output format
      const summary = Array.isArray(result) ? result[0]?.summary_text : result.summary_text;
      
      return summary || cleanedText.substring(0, maxLength);
    } catch (error) {
      console.error('Summarization failed:', error);
      // Fallback to simple truncation
      const cleaned = this.cleanText(text);
      return cleaned.length > maxLength 
        ? cleaned.substring(0, maxLength) + '...'
        : cleaned;
    }
  }

  async classifyContent(text: string, labels: string[]): Promise<{ label: string; confidence: number }[]> {
    try {
      const classifier = await modelManager.getClassifier();
      
      const result = await classifier(text, labels);
      
      // Handle different possible result formats
      if (Array.isArray(result)) {
        return result.map(item => ({
          label: item.label,
          confidence: item.score
        }));
      } else if (result.labels && result.scores) {
        return result.labels.map((label: string, index: number) => ({
          label,
          confidence: result.scores[index]
        }));
      }
      
      return [];
    } catch (error) {
      console.error('Classification failed:', error);
      return [];
    }
  }

  scoreContentRelevance(content: string, context: PageContext): number {
    const keywords = this.extractKeywords(content);
    const focusKeywords = context.focusKeywords.map(kw => stemmer(kw.toLowerCase()));
    
    // Keyword matching score
    const keywordMatches = keywords.filter(keyword => 
      focusKeywords.some(focus => 
        keyword.includes(focus) || focus.includes(keyword)
      )
    ).length;
    
    const keywordScore = Math.min(1, keywordMatches / focusKeywords.length);
    
    // Content length penalty/bonus based on context requirements
    const lengthScore = this.calculateLengthScore(content, context.contentLength);
    
    // Entity relevance (presence of metrics, competitors, etc.)
    const entities = this.extractEntities(content);
    const entityScore = Math.min(1, entities.length / 5); // Normalize to 0-1
    
    // Weighted combination
    const relevanceScore = 
      (keywordScore * PROCESSING_RULES.relevanceScoring.keywordMatch) +
      (lengthScore * 0.3) + // 30% for length appropriateness
      (entityScore * PROCESSING_RULES.relevanceScoring.entityRelevance);
    
    return Math.min(1, relevanceScore);
  }

  private calculateLengthScore(content: string, requiredLength: 'brief' | 'detailed' | 'comprehensive'): number {
    const length = content.length;
    
    switch (requiredLength) {
      case 'brief':
        return length < 200 ? 1 : Math.max(0, 1 - (length - 200) / 500);
      case 'detailed':
        return length >= 200 && length <= 800 ? 1 : Math.max(0, 1 - Math.abs(length - 500) / 500);
      case 'comprehensive':
        return length > 500 ? 1 : length / 500;
      default:
        return 0.5;
    }
  }

  extractInsights(content: string, context: PageContext): Insight[] {
    const insights: Insight[] = [];
    const sentences = this.segmentSentences(content);
    
    sentences.forEach((sentence, index) => {
      const relevanceScore = this.scoreContentRelevance(sentence, context);
      
      if (relevanceScore >= 0.6) { // Only include high-relevance insights
        const insightType = this.determineInsightType(sentence);
        const keywords = this.extractKeywords(sentence);
        
        insights.push({
          id: `insight_${Date.now()}_${index}`,
          type: insightType,
          content: sentence.trim(),
          relevanceScore,
          confidence: relevanceScore * 0.9, // Slight confidence penalty
          source: context.pageType,
          phase: context.relevantPhases[0] || 'unknown',
          keywords
        });
      }
    });

    // Sort by relevance score and limit results
    return insights
      .sort((a, b) => b.relevanceScore - a.relevanceScore)
      .slice(0, 10); // Limit to top 10 insights
  }

  private determineInsightType(text: string): 'opportunity' | 'threat' | 'recommendation' | 'finding' {
    const lowercaseText = text.toLowerCase();
    
    // Recommendation indicators
    if (/\b(recommend|should|need to|must|ought to)\b/.test(lowercaseText)) {
      return 'recommendation';
    }
    
    // Opportunity indicators
    if (/\b(opportunity|potential|growth|advantage|benefit|improve)\b/.test(lowercaseText)) {
      return 'opportunity';
    }
    
    // Threat indicators
    if (/\b(risk|threat|challenge|problem|issue|weakness|concern)\b/.test(lowercaseText)) {
      return 'threat';
    }
    
    // Default to finding
    return 'finding';
  }

  extractMetrics(text: string): ExtractedMetric[] {
    const metrics: ExtractedMetric[] = [];
    
    // Extract percentage metrics
    const percentageRegex = /(\w+(?:\s+\w+)*)\s*:?\s*(\d+(?:\.\d+)?%)/g;
    let match;
    while ((match = percentageRegex.exec(text)) !== null) {
      metrics.push({
        name: match[1].trim(),
        value: match[2],
        type: 'performance',
        confidence: 0.9,
        source: text.substring(Math.max(0, match.index - 30), match.index + match[0].length + 30)
      });
    }
    
    // Extract monetary values
    const moneyRegex = /(\w+(?:\s+\w+)*)\s*:?\s*\$?([\d,]+(?:\.\d{2})?)/g;
    while ((match = moneyRegex.exec(text)) !== null) {
      if (!match[2].includes('%')) { // Avoid double-matching percentages
        metrics.push({
          name: match[1].trim(),
          value: `$${match[2]}`,
          type: 'budget',
          confidence: 0.8,
          source: text.substring(Math.max(0, match.index - 30), match.index + match[0].length + 30)
        });
      }
    }
    
    // Extract time-based metrics
    const timeRegex = /(\w+(?:\s+\w+)*)\s*:?\s*(\d+)\s*(days?|weeks?|months?|years?)/g;
    while ((match = timeRegex.exec(text)) !== null) {
      metrics.push({
        name: match[1].trim(),
        value: `${match[2]} ${match[3]}`,
        type: 'timeline',
        confidence: 0.8,
        source: text.substring(Math.max(0, match.index - 30), match.index + match[0].length + 30)
      });
    }
    
    return metrics;
  }

  processPhaseResponse(phaseId: string, response: string): ProcessedContent {
    const processedAt = new Date();
    const cleanedText = this.cleanText(response);
    
    // Extract basic information
    const entities = this.extractEntities(cleanedText);
    const keywords = this.extractKeywords(cleanedText);
    
    // Create a basic page context for processing
    const basicContext: PageContext = {
      pageType: 'executive-summary' as any,
      focusKeywords: keywords.slice(0, 10),
      relevantPhases: [phaseId],
      contentLength: 'detailed',
      outputFormat: 'summary'
    };
    
    const insights = this.extractInsights(cleanedText, basicContext);
    const relevanceScore = 0.8; // Default relevance for phase content
    const confidence = 0.85; // Default confidence
    
    return {
      summary: cleanedText.substring(0, 300) + (cleanedText.length > 300 ? '...' : ''),
      insights,
      entities,
      relevanceScore,
      confidence,
      sources: [phaseId],
      processedAt
    };
  }
}

export const contentProcessor = new ContentProcessor();