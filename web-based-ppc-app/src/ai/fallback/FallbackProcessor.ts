// Fallback AI processor that works without heavy models
// Provides basic content processing using simple algorithms

import { ProcessedContent, PageContext, Insight, Entity } from '../types';

export class FallbackProcessor {
  static async processContent(content: string, context: PageContext): Promise<ProcessedContent> {
    // Simple text processing without AI models
    const cleanedContent = this.cleanText(content);
    const insights = this.extractBasicInsights(cleanedContent, context);
    const entities = this.extractBasicEntities(cleanedContent);
    const summary = this.generateSimpleSummary(cleanedContent, context);
    
    return {
      summary,
      insights,
      entities,
      relevanceScore: 0.7, // Default relevance
      confidence: 0.6, // Lower confidence for fallback
      sources: context.relevantPhases,
      processedAt: new Date()
    };
  }

  private static cleanText(text: string): string {
    if (!text) return '';
    
    // Remove markdown formatting
    let cleaned = text
      .replace(/\*\*([^*]+)\*\*/g, '$1') // Remove bold
      .replace(/\*([^*]+)\*/g, '$1')     // Remove italic
      .replace(/#{1,6}\s+/g, '')         // Remove headers
      .replace(/```[\s\S]*?```/g, '')    // Remove code blocks
      .replace(/^\s*[-*+]\s+/gm, '')     // Remove bullet points
      .replace(/^\s*\d+\.\s+/gm, '');    // Remove numbered lists
    
    // Normalize whitespace
    cleaned = cleaned.replace(/\s+/g, ' ').trim();
    
    return cleaned;
  }

  private static generateSimpleSummary(content: string, context: PageContext): string {
    if (!content) return 'No content available for summarization.';
    
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 20);
    const maxLength = this.getMaxLength(context.contentLength);
    
    // Simple extractive summarization - take first few sentences
    let summary = '';
    for (const sentence of sentences) {
      if (summary.length + sentence.length < maxLength) {
        summary += sentence.trim() + '. ';
      } else {
        break;
      }
    }
    
    return summary.trim() || content.substring(0, maxLength) + '...';
  }

  private static getMaxLength(contentLength: 'brief' | 'detailed' | 'comprehensive'): number {
    switch (contentLength) {
      case 'brief': return 150;
      case 'detailed': return 250;
      case 'comprehensive': return 350;
      default: return 200;
    }
  }

  private static extractBasicInsights(content: string, context: PageContext): Insight[] {
    const insights: Insight[] = [];
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 20);
    
    sentences.forEach((sentence, index) => {
      const trimmed = sentence.trim();
      if (this.isRelevantToContext(trimmed, context)) {
        const type = this.determineInsightType(trimmed);
        const relevanceScore = this.calculateBasicRelevance(trimmed, context);
        
        if (relevanceScore >= 0.5) {
          insights.push({
            id: `fallback_insight_${Date.now()}_${index}`,
            type,
            content: trimmed,
            relevanceScore,
            confidence: 0.6,
            source: context.pageType,
            phase: context.relevantPhases[0] || 'unknown',
            keywords: this.extractBasicKeywords(trimmed)
          });
        }
      }
    });

    return insights.slice(0, 5); // Limit to top 5
  }

  private static isRelevantToContext(text: string, context: PageContext): boolean {
    const lowercaseText = text.toLowerCase();
    return context.focusKeywords.some(keyword => 
      lowercaseText.includes(keyword.toLowerCase())
    );
  }

  private static calculateBasicRelevance(text: string, context: PageContext): number {
    const lowercaseText = text.toLowerCase();
    const keywordMatches = context.focusKeywords.filter(keyword =>
      lowercaseText.includes(keyword.toLowerCase())
    ).length;
    
    return Math.min(1, keywordMatches / Math.max(1, context.focusKeywords.length));
  }

  private static determineInsightType(text: string): 'opportunity' | 'threat' | 'recommendation' | 'finding' {
    const lowercaseText = text.toLowerCase();
    
    if (/\b(recommend|should|need to|must|ought to)\b/.test(lowercaseText)) {
      return 'recommendation';
    }
    
    if (/\b(opportunity|potential|growth|advantage|benefit)\b/.test(lowercaseText)) {
      return 'opportunity';
    }
    
    if (/\b(risk|threat|challenge|problem|issue|weakness)\b/.test(lowercaseText)) {
      return 'threat';
    }
    
    return 'finding';
  }

  private static extractBasicKeywords(text: string): string[] {
    // Simple keyword extraction - find important words
    const words = text.toLowerCase()
      .replace(/[^\w\s]/g, '')
      .split(/\s+/)
      .filter(word => word.length > 3);
    
    // Remove common stop words
    const stopWords = new Set(['this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'were', 'said']);
    const keywords = words.filter(word => !stopWords.has(word));
    
    return Array.from(new Set(keywords)).slice(0, 5);
  }

  private static extractBasicEntities(content: string): Entity[] {
    const entities: Entity[] = [];
    
    // Extract monetary values
    const moneyMatches = content.match(/\$[\d,]+(?:\.\d{2})?/g) || [];
    moneyMatches.forEach(match => {
      entities.push({
        text: match,
        type: 'budget',
        confidence: 0.8,
        context: this.getEntityContext(content, match)
      });
    });
    
    // Extract percentages
    const percentageMatches = content.match(/\d+(?:\.\d+)?%/g) || [];
    percentageMatches.forEach(match => {
      entities.push({
        text: match,
        type: 'metric',
        confidence: 0.9,
        context: this.getEntityContext(content, match)
      });
    });
    
    // Extract time periods
    const timeMatches = content.match(/\d+\s+(days?|weeks?|months?|years?)/g) || [];
    timeMatches.forEach(match => {
      entities.push({
        text: match,
        type: 'timeline',
        confidence: 0.7,
        context: this.getEntityContext(content, match)
      });
    });
    
    return entities;
  }

  private static getEntityContext(text: string, entity: string): string {
    const index = text.indexOf(entity);
    if (index === -1) return '';
    
    const start = Math.max(0, index - 50);
    const end = Math.min(text.length, index + entity.length + 50);
    
    return text.substring(start, end).trim();
  }
}