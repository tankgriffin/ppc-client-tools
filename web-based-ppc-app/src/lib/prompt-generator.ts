// Claude Prompt Generation - Web App Implementation
import { BusinessIntelligence, ClaudePhases, ServicePackage } from '@/types';

export class ClaudePromptGenerator {
  
  public static generateAllPrompts(businessData: BusinessIntelligence): ClaudePhases {
    return {
      phase1: {
        prompt: this.generatePhase1Prompt(businessData),
        response: '',
        completed: false,
        lastModified: new Date(),
        insights: []
      },
      phase2: {
        prompt: this.generatePhase2Prompt(businessData),
        response: '',
        completed: false,
        lastModified: new Date(),
        insights: []
      },
      phase3: {
        prompt: this.generatePhase3Prompt(businessData),
        response: '',
        completed: false,
        lastModified: new Date(),
        insights: []
      },
      phase4: {
        prompt: this.generatePhase4Prompt(businessData),
        response: '',
        completed: false,
        lastModified: new Date(),
        insights: []
      },
      phase5: {
        prompt: this.generatePhase5Prompt(businessData),
        response: '',
        completed: false,
        lastModified: new Date(),
        insights: []
      }
    };
  }

  private static generatePhase1Prompt(data: BusinessIntelligence): string {
    const serviceContext = this.getServiceContext(data.servicePackage);
    
    return `# Phase 1: Business Intelligence Analysis

I need you to analyze this business and provide strategic insights for ${serviceContext.strategy} development.

## Business Context:
- **Business Name**: ${data.businessName}
- **Industry**: ${data.industry}
- **Location**: ${data.location} (Service Area: ${data.serviceArea})
- **Website**: ${data.website}

## Business Description:
${data.description}

## Services Offered:
${data.services}

## Unique Value Proposition:
${data.uniqueValue}

## Target Audience:
${data.targetAudience}

## Customer Pain Points:
${data.customerPainPoints}

## Current Marketing:
${data.currentMarketing}

## Campaign Objectives:
- Primary Goal: ${this.formatCampaignGoal(data.primaryGoal)}
- Budget Range: ${this.formatBudgetRange(data.budgetRange)}
- Success Metrics: ${data.successMetrics}

## Seasonal Considerations:
${data.seasonalTrends}

## Biggest Challenges:
${data.biggestChallenges}

## Analysis Required:

Please provide a comprehensive business intelligence analysis including:

1. **Market Position Assessment**
   - Industry landscape analysis for ${data.industry} in ${data.location}
   - Business maturity and growth potential assessment
   - Market opportunity size estimation
   - Competitive intensity evaluation

2. **Competitive Advantages Analysis**
   - Unique differentiators based on: ${data.uniqueValue}
   - Competitive moats and barriers to entry
   - Value proposition strengths and weaknesses
   - Sustainable competitive advantages

3. **Target Market Deep Dive**
   - Primary audience segment analysis: ${data.targetAudience}
   - Secondary audience opportunities
   - Customer journey mapping for ${this.formatCampaignGoal(data.primaryGoal)}
   - Pain point prioritization: ${data.customerPainPoints}

4. **${serviceContext.focus} Strategy Foundation**
   - Recommended ${serviceContext.channels} approach for ${this.formatBudgetRange(data.budgetRange)} budget
   - ${this.getPlatformGuidance(data.servicePackage)}
   - Budget allocation suggestions across ${serviceContext.channels}
   - Priority targeting strategies for ${this.formatCampaignGoal(data.primaryGoal)}

5. **Growth Opportunities**
   - Untapped market segments in ${data.serviceArea}
   - Service expansion possibilities beyond: ${data.services}
   - Geographic expansion potential
   - Revenue stream diversification opportunities

6. **Risk Assessment**
   - Market entry barriers and challenges
   - Competitive threats and responses
   - Economic and seasonal risks: ${data.seasonalTrends}
   - Operational risks and mitigation strategies

7. **Success Metrics Framework**
   - KPI alignment with ${data.successMetrics}
   - Leading vs lagging indicators
   - Benchmark establishment
   - ROI measurement framework

Please provide specific, actionable insights that will inform our ${serviceContext.strategy} development. Focus on opportunities that can be captured with a ${this.formatBudgetRange(data.budgetRange)} monthly budget targeting ${this.formatCampaignGoal(data.primaryGoal)} through ${serviceContext.tactics}.`;
  }

  private static generatePhase2Prompt(data: BusinessIntelligence): string {
    const competitorsList = data.competitors.map(comp => `- ${comp}`).join('\n');
    const serviceContext = this.getServiceContext(data.servicePackage);
    
    return `# Phase 2: Competitive Landscape Mapping

Based on the business intelligence from Phase 1, I need you to analyze the competitive landscape for ${serviceContext.strategy} planning.

## Business Context (from Phase 1):
- **Business**: ${data.businessName} - ${data.description}
- **Industry**: ${data.industry}
- **Location**: ${data.location}
- **Services**: ${data.services}
- **Unique Value**: ${data.uniqueValue}
- **Target Audience**: ${data.targetAudience}
- **Budget Range**: ${this.formatBudgetRange(data.budgetRange)}

## Known Competitors:
${competitorsList}

## Competitive Analysis Required:

Please provide a comprehensive competitive landscape analysis including:

1. **Direct Competitor Identification**
   - Who are the main direct competitors in ${data.industry}?
   - What are their primary service offerings vs our services: ${data.services}?
   - How do they position themselves in the ${data.location} market?
   - What are their estimated market shares?

2. **Indirect Competitor Analysis**
   - Who are the indirect competitors and substitute services?
   - What adjacent industries compete for the same customers: ${data.targetAudience}?
   - What alternative solutions do customers consider?
   - What DIY or self-service options exist?

3. **Competitive Positioning Map**
   - How do competitors position on price vs. quality spectrum?
   - What are the main positioning themes in ${data.industry}?
   - Where are the positioning gaps we can exploit?
   - How does our unique value fit: ${data.uniqueValue}?

4. **Competitor ${serviceContext.focus} Strategy Analysis**
   - ${this.getCompetitorAnalysisQuestions(data.servicePackage, data.services)}
   - What messaging themes do they probably use across ${serviceContext.channels}?
   - What are their likely campaign objectives and budget ranges?
   - ${this.getCompetitorTacticsQuestions(data.servicePackage)}

5. **Competitive Advantages Analysis**
   - What advantages do competitors have over us?
   - What are their key weaknesses we can exploit?
   - How can we differentiate based on: ${data.uniqueValue}?
   - What competitive gaps exist in serving: ${data.targetAudience}?

6. **Market Share and Growth Analysis**
   - Who are the market leaders in ${data.location}?
   - What's the competitive intensity and saturation level?
   - Where are the growth opportunities with ${this.formatBudgetRange(data.budgetRange)} budget?
   - What market segments are underserved?

7. **Competitive Threat Assessment**
   - Which competitors pose the biggest threat to our ${this.formatCampaignGoal(data.primaryGoal)} goal?
   - What competitive responses should we expect to our ${serviceContext.strategy}?
   - How can we defend against competitive attacks?
   - What first-mover advantages can we capture?

8. **Competitive Intelligence for ${serviceContext.focus}**
   - What can we learn from competitor websites and marketing efforts?
   - What messaging themes are overused vs underutilized in ${serviceContext.channels}?
   - What seasonal patterns do competitors follow?
   - What technology and tools do they likely use for ${serviceContext.tactics}?

Please provide specific, actionable insights for ${serviceContext.strategy} development that help us outperform competitors with strategic positioning and execution.`;
  }

  private static generatePhase3Prompt(data: BusinessIntelligence): string {
    const serviceContext = this.getServiceContext(data.servicePackage);
    
    return `# Phase 3: Market Gap Identification

Building on the business intelligence and competitive analysis, I need you to identify specific market gaps and opportunities for ${serviceContext.strategy} exploitation.

## Business Context:
- **Business**: ${data.businessName}
- **Industry**: ${data.industry} in ${data.location}
- **Services**: ${data.services}
- **Target Audience**: ${data.targetAudience}
- **Unique Value**: ${data.uniqueValue}
- **Primary Goal**: ${this.formatCampaignGoal(data.primaryGoal)}
- **Budget Range**: ${this.formatBudgetRange(data.budgetRange)}

## Market Gap Analysis Required:

Please identify and analyze market gaps and opportunities that can be exploited through strategic ${serviceContext.strategy}:

1. **Service Delivery Gaps**
   - What service aspects are underserved in ${data.industry}?
   - What customer needs are not being met by current offerings?
   - What service combinations or packages are missing?
   - What quality levels are underrepresented?

2. **Geographic and Location Gaps**
   - What areas within ${data.serviceArea} are underserved?
   - Where are competitors weak or completely absent?
   - What location-specific opportunities exist?
   - What travel/distance advantages can we leverage?

3. **Audience and Demographic Gaps**
   - What customer segments within ${data.targetAudience} are underserved?
   - What age groups, income levels, or lifestyle segments are competitors missing?
   - What psychographic groups are being overlooked?
   - What niche audiences could we target?

4. **Messaging and Communication Gaps**
   - What messages are competitors in ${data.industry} not using?
   - What emotional triggers are being missed for ${data.targetAudience}?
   - What value propositions are unexplored?
   - What pain points are not being addressed: ${data.customerPainPoints}?

5. **Channel and Platform Gaps**
   - What digital marketing channels are underutilized in ${data.industry}?
   - What social media platforms are competitors not using effectively?
   - What advertising formats or placements are missed?
   - What touchpoints in the customer journey are neglected?

6. **Timing and Seasonal Gaps**
   - What seasonal opportunities are missed: ${data.seasonalTrends}?
   - What time-of-day or day-of-week targeting is underutilized?
   - What event-driven opportunities exist?
   - What urgency or scarcity angles are unused?

7. **Price Point and Value Gaps**
   - What price points are underserved in the market?
   - What value tiers are missing between competitors?
   - What pricing strategies are unexplored?
   - What payment or financing options are unavailable?

8. **Technology and Experience Gaps**
   - What technological advantages can we leverage?
   - What digital experiences are competitors not providing?
   - What automation or convenience features are missing?
   - What mobile or online capabilities are underutilized?

9. **Content and Education Gaps**
   - What educational content is missing for ${data.targetAudience}?
   - What frequently asked questions are not being answered?
   - What how-to or tutorial content is absent?
   - What industry expertise is not being showcased?

10. **Trust and Credibility Gaps**
    - What trust signals are competitors not using?
    - What credibility markers are missing in the market?
    - What transparency or guarantee opportunities exist?
    - What social proof angles are underutilized?

For each gap identified, please provide:
- **Specific opportunity description**
- **Market size and potential estimation**
- **Implementation difficulty and requirements**
- **Competitive advantage potential**
- **PPC campaign implications and strategies**
- **Budget allocation recommendations for ${this.formatBudgetRange(data.budgetRange)}**
- **Expected ROI and timeline for ${this.formatCampaignGoal(data.primaryGoal)}**

Focus on gaps that can be immediately exploited through strategic PPC campaigns with our available budget and resources.`;
  }

  private static generatePhase4Prompt(data: BusinessIntelligence): string {
    return `# Phase 4: Strategic Positioning Development

Based on the comprehensive analysis from previous phases, I need you to develop a strategic positioning strategy specifically optimized for PPC campaign success.

## Business Context Summary:
- **Business**: ${data.businessName}
- **Industry**: ${data.industry} in ${data.location}
- **Services**: ${data.services}
- **Target Audience**: ${data.targetAudience}
- **Unique Value**: ${data.uniqueValue}
- **Budget Range**: ${this.formatBudgetRange(data.budgetRange)}
- **Primary Goal**: ${this.formatCampaignGoal(data.primaryGoal)}
- **Success Metrics**: ${data.successMetrics}

## Strategic Positioning Development Required:

Please develop a comprehensive positioning strategy optimized for PPC performance:

1. **Core Positioning Statement**
   - Primary positioning theme that differentiates us in ${data.industry}
   - Unique value proposition that resonates with ${data.targetAudience}
   - Competitive differentiation based on: ${data.uniqueValue}
   - Alignment with ${this.formatCampaignGoal(data.primaryGoal)} campaign objectives

2. **Positioning Pillars Framework**
   - 3-5 key positioning pillars that support our main position
   - Supporting evidence and proof points for each pillar
   - How each pillar differentiates from main competitors
   - Relevance ranking for ${data.targetAudience}

3. **Multi-Layered Messaging Architecture**
   - Primary brand message (30 characters or less for headlines)
   - Secondary supporting messages (90 characters for descriptions)
   - Tertiary detail messages for landing pages
   - Emotional vs. rational messaging balance optimization

4. **Competitive Positioning Strategy**
   - Head-to-head positioning against direct competitors
   - Flanking strategies for indirect competition
   - Defensive positioning for competitive attacks
   - Blue ocean positioning for uncontested market space

5. **Audience-Specific Positioning**
   - Primary audience positioning for ${data.targetAudience}
   - Secondary audience positioning variations
   - Positioning for different customer journey stages
   - Demographic and psychographic positioning adjustments

6. **Platform-Optimized Positioning**
   - Google Ads positioning strategy (search intent focus)
   - Meta/Facebook positioning strategy (social context focus)
   - LinkedIn positioning strategy (if B2B applicable)
   - Platform-specific positioning adaptations

7. **Campaign-Type Positioning Framework**
   - Brand awareness campaign positioning
   - Lead generation campaign positioning (${this.formatCampaignGoal(data.primaryGoal)})
   - Sales conversion campaign positioning
   - Retargeting campaign positioning

8. **Positioning Proof Points Strategy**
   - Credentials and certifications to highlight
   - Customer testimonial themes and selection
   - Case studies and success stories framework
   - Awards, recognition, and authority signals

9. **Positioning Testing and Optimization**
   - Key positioning elements to A/B test
   - Positioning variations for different audience segments
   - Performance metrics for positioning effectiveness
   - Optimization schedule and methodology

10. **Positioning Implementation Roadmap**
    - Phase 1: Core positioning launch (${this.formatBudgetRange(data.budgetRange)} budget)
    - Phase 2: Positioning refinement and optimization
    - Phase 3: Positioning expansion and scaling
    - Success metrics tracking aligned with: ${data.successMetrics}

11. **Crisis and Competitive Response Positioning**
    - Positioning defense strategies
    - Rapid response positioning for competitive moves
    - Crisis communication positioning
    - Positioning recovery and reinforcement tactics

12. **Local and Geographic Positioning**
    - Location-specific positioning for ${data.location}
    - Regional advantages and local credibility
    - Community connection and local expertise positioning
    - Geographic expansion positioning framework

Please provide specific, immediately actionable positioning strategies that can be implemented across all PPC campaigns to maximize ${this.formatCampaignGoal(data.primaryGoal)} results within our ${this.formatBudgetRange(data.budgetRange)} budget.`;
  }

  private static generatePhase5Prompt(data: BusinessIntelligence): string {
    const serviceContext = this.getServiceContext(data.servicePackage);
    
    return `# Phase 5: Content & Campaign Strategy

Based on all previous strategic analysis, I need you to develop comprehensive, immediately actionable content and campaign strategies for ${serviceContext.strategy} implementation.

## Complete Business Context:
- **Business**: ${data.businessName}
- **Industry**: ${data.industry} in ${data.location}
- **Services**: ${data.services}
- **Target Audience**: ${data.targetAudience}
- **Unique Value**: ${data.uniqueValue}
- **Service Package**: ${this.formatServicePackage(data.servicePackage)}
- **Budget Range**: ${this.formatBudgetRange(data.budgetRange)}
- **Primary Goal**: ${this.formatCampaignGoal(data.primaryGoal)}
- **Success Metrics**: ${data.successMetrics}

## Comprehensive Implementation Strategy Required:

Please develop detailed, actionable strategies for immediate ${serviceContext.strategy} implementation:

1. **Complete ${serviceContext.focus} Architecture**
   - ${this.getCampaignArchitectureRecommendations(data.servicePackage)}
   - ${serviceContext.focus} structure and naming conventions
   - Budget allocation across ${serviceContext.channels} for ${this.formatBudgetRange(data.budgetRange)}
   - ${this.getBiddingStrategyRecommendations(data.servicePackage, data.primaryGoal)}
   - Geographic targeting strategy for ${data.location}

2. **Advanced ${this.getKeywordStrategyTitle(data.servicePackage)}**
   - ${this.getKeywordRecommendations(data.servicePackage, data.services)}
   - ${this.getKeywordOpportunities(data.servicePackage)}
   - Local keyword variations for ${data.location}
   - Seasonal keyword calendar: ${data.seasonalTrends}
   - ${this.getKeywordOptimization(data.servicePackage)}
   - ${this.getKeywordGrouping(data.servicePackage)}

3. **Comprehensive Ad Copy Strategy**
   - 10+ headline variations (30 characters each)
   - 10+ description variations (90 characters each)
   - Compelling call-to-action options
   - Ad extension strategies (sitelinks, callouts, structured snippets)
   - Emotional vs. rational copy balance
   - Industry-specific messaging for ${data.industry}

4. **Landing Page Optimization Strategy**
   - Landing page requirements for ${this.formatCampaignGoal(data.primaryGoal)}
   - Content structure and layout recommendations
   - Conversion optimization elements
   - A/B testing opportunities and priorities
   - Mobile optimization requirements
   - Page speed and technical requirements

5. **Advanced Audience Targeting Strategy**
   - Demographics targeting for ${data.targetAudience}
   - Interest and behavior targeting
   - Custom audience creation strategies
   - Lookalike audience development
   - Retargeting campaign structure
   - Audience exclusions and negative targeting

6. **Content Calendar and Creative Strategy**
   - 3-month content calendar with weekly themes
   - Monthly content pillars aligned with ${data.services}
   - Seasonal content planning: ${data.seasonalTrends}
   - Event-driven content opportunities
   - Visual content themes and requirements
   - Video content strategy and concepts

7. **Multi-Platform Creative Strategy**
   - Google Ads creative requirements and specifications
   - Meta/Facebook creative strategy and formats
   - LinkedIn creative approach (if applicable)
   - Creative testing and optimization schedule
   - Brand consistency guidelines across platforms

8. **Conversion Tracking and Measurement**
   - Conversion tracking setup for ${this.formatCampaignGoal(data.primaryGoal)}
   - Key performance indicators aligned with: ${data.successMetrics}
   - Attribution modeling recommendations
   - ROI measurement and reporting structure
   - Optimization schedule and methodology

9. **Budget Management and Pacing**
   - Daily budget allocation for ${this.formatBudgetRange(data.budgetRange)}
   - Campaign priority and budget distribution
   - Seasonal budget adjustments
   - Performance-based budget reallocation
   - Scaling strategy for successful campaigns

10. **Launch and Optimization Timeline**
    - Week 1-2: Campaign setup and initial launch
    - Week 3-4: Initial optimization and refinement
    - Month 2: Performance analysis and scaling
    - Month 3: Advanced optimization and expansion
    - Ongoing: Continuous improvement and growth

11. **Competitive Response and Defense Strategy**
    - Competitive monitoring and alerts
    - Response strategies for competitive moves
    - Market position defense
    - Opportunity capitalization when competitors falter

12. **Advanced Tactics and Growth Strategies**
    - Automation and smart bidding implementation
    - Cross-campaign and cross-platform synergies
    - Expansion opportunities and new markets
    - Partnership and collaboration opportunities

Please provide specific, actionable strategies with exact implementation steps, recommended settings, and expected outcomes. Focus on tactics that can be immediately implemented to achieve ${this.formatCampaignGoal(data.primaryGoal)} with our ${this.formatBudgetRange(data.budgetRange)} budget.

Include specific examples of:
- Ad headlines and descriptions
- Keyword lists and groupings
- Audience targeting parameters
- Landing page elements
- Conversion tracking codes
- Campaign settings and configurations

This should be a complete blueprint for PPC campaign success.`;
  }

  private static getServiceContext(servicePackage: ServicePackage) {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return {
          strategy: 'PPC campaign',
          channels: 'paid advertising campaigns',
          focus: 'PPC-specific',
          tactics: 'paid search, display, and social advertising'
        };
      case ServicePackage.SEO_ONLY:
        return {
          strategy: 'SEO campaign',
          channels: 'organic search optimization',
          focus: 'SEO-specific',
          tactics: 'content optimization, technical SEO, and link building'
        };
      case ServicePackage.PPC_SEO_COMBINED:
        return {
          strategy: 'integrated PPC and SEO campaign',
          channels: 'both paid advertising and organic search optimization',
          focus: 'integrated digital marketing',
          tactics: 'coordinated paid and organic search strategies'
        };
      default:
        return {
          strategy: 'digital marketing campaign',
          channels: 'digital marketing',
          focus: 'digital marketing',
          tactics: 'digital marketing strategies'
        };
    }
  }

  private static getPlatformGuidance(servicePackage: ServicePackage): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return 'Platform prioritization (Google Ads vs Meta vs LinkedIn vs others)';
      case ServicePackage.SEO_ONLY:
        return 'SEO platform and tool recommendations (Google Search Console, content management systems, analytics tools)';
      case ServicePackage.PPC_SEO_COMBINED:
        return 'Integrated platform strategy (coordinating paid and organic across Google, Meta, content platforms)';
      default:
        return 'Platform recommendations';
    }
  }

  private static getCompetitorAnalysisQuestions(servicePackage: ServicePackage, services: string): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return `What keywords are competitors likely targeting for ${services}?`;
      case ServicePackage.SEO_ONLY:
        return `What organic keywords and content topics are competitors targeting for ${services}?`;
      case ServicePackage.PPC_SEO_COMBINED:
        return `What keywords are competitors targeting both organically and through paid search for ${services}?`;
      default:
        return `What targeting strategies are competitors using for ${services}?`;
    }
  }

  private static getCompetitorTacticsQuestions(servicePackage: ServicePackage): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return 'What landing page and ad creative strategies might they employ?';
      case ServicePackage.SEO_ONLY:
        return 'What content marketing and link building strategies might they employ?';
      case ServicePackage.PPC_SEO_COMBINED:
        return 'What integrated content, landing page, and cross-channel strategies might they employ?';
      default:
        return 'What marketing strategies might they employ?';
    }
  }

  private static formatServicePackage(servicePackage: ServicePackage): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return 'PPC Only';
      case ServicePackage.SEO_ONLY:
        return 'SEO Only';
      case ServicePackage.PPC_SEO_COMBINED:
        return 'PPC + SEO Combined';
      default:
        return 'Digital Marketing';
    }
  }

  private static getCampaignArchitectureRecommendations(servicePackage: ServicePackage): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return 'Campaign types recommendation (Search, Display, Performance Max, Video, Shopping)';
      case ServicePackage.SEO_ONLY:
        return 'SEO campaign structure recommendations (content clusters, technical optimization phases, link building campaigns)';
      case ServicePackage.PPC_SEO_COMBINED:
        return 'Integrated campaign architecture (coordinated PPC and SEO campaigns, shared keyword targeting, content syndication)';
      default:
        return 'Campaign recommendations';
    }
  }

  private static getBiddingStrategyRecommendations(servicePackage: ServicePackage, primaryGoal: string): string {
    const formattedGoal = this.formatCampaignGoal(primaryGoal);
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return `Bidding strategy recommendations for ${formattedGoal}`;
      case ServicePackage.SEO_ONLY:
        return `Content priority and optimization strategy for ${formattedGoal}`;
      case ServicePackage.PPC_SEO_COMBINED:
        return `Integrated bidding and content strategy for ${formattedGoal}`;
      default:
        return `Strategy recommendations for ${formattedGoal}`;
    }
  }

  private static getKeywordStrategyTitle(servicePackage: ServicePackage): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return 'Keyword Strategy';
      case ServicePackage.SEO_ONLY:
        return 'Keyword & Content Strategy';
      case ServicePackage.PPC_SEO_COMBINED:
        return 'Integrated Keyword Strategy';
      default:
        return 'Keyword Strategy';
    }
  }

  private static getKeywordRecommendations(servicePackage: ServicePackage, services: string): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return `Primary PPC keyword themes for ${services}`;
      case ServicePackage.SEO_ONLY:
        return `Primary SEO keyword themes and content topics for ${services}`;
      case ServicePackage.PPC_SEO_COMBINED:
        return `Primary keyword themes for both PPC and SEO targeting for ${services}`;
      default:
        return `Primary keyword themes for ${services}`;
    }
  }

  private static getKeywordOpportunities(servicePackage: ServicePackage): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return 'Secondary and long-tail PPC keyword opportunities';
      case ServicePackage.SEO_ONLY:
        return 'Secondary content topics and long-tail SEO opportunities';
      case ServicePackage.PPC_SEO_COMBINED:
        return 'Secondary keywords for both paid and organic opportunities';
      default:
        return 'Secondary keyword opportunities';
    }
  }

  private static getKeywordOptimization(servicePackage: ServicePackage): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return 'Negative keyword strategy and exclusions';
      case ServicePackage.SEO_ONLY:
        return 'Content gap analysis and keyword cannibalization prevention';
      case ServicePackage.PPC_SEO_COMBINED:
        return 'Integrated keyword optimization and cannibalization prevention';
      default:
        return 'Keyword optimization strategy';
    }
  }

  private static getKeywordGrouping(servicePackage: ServicePackage): string {
    switch (servicePackage) {
      case ServicePackage.PPC_ONLY:
        return 'Keyword grouping for optimal ad relevance';
      case ServicePackage.SEO_ONLY:
        return 'Content cluster organization for topic authority';
      case ServicePackage.PPC_SEO_COMBINED:
        return 'Keyword grouping for coordinated paid and organic campaigns';
      default:
        return 'Keyword organization strategy';
    }
  }

  private static formatCampaignGoal(goal: string): string {
    const goalMap: Record<string, string> = {
      'lead_generation': 'Lead Generation',
      'sales': 'Sales',
      'brand_awareness': 'Brand Awareness',
      'website_traffic': 'Website Traffic',
      'local_visibility': 'Local Visibility',
      'ecommerce': 'E-commerce'
    };
    return goalMap[goal] || goal;
  }

  private static formatBudgetRange(range: string): string {
    const rangeMap: Record<string, string> = {
      'under_1k': '$500-$1000',
      '1k_5k': '$1000-$5000',
      '5k_10k': '$5000-$10000',
      '10k_25k': '$10000-$25000',
      '25k_50k': '$25000-$50000',
      'over_50k': '$50000+'
    };
    return rangeMap[range] || range;
  }
}