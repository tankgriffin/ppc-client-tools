#!/usr/bin/env python3
"""
Claude Prompt Generator Engine
Dynamic prompt generation system for different research phases
"""

import os
import json
from datetime import datetime
from pathlib import Path

try:
    from jinja2 import Template, Environment, FileSystemLoader
except ImportError:
    print("Jinja2 not available, using basic string formatting")
    Template = None

class PromptGenerator:
    """Dynamic prompt generation system for Claude research phases"""
    
    def __init__(self, template_dir=None):
        self.template_dir = template_dir or os.path.join(os.path.dirname(__file__), 'templates')
        self.templates = {}
        self.context = {}
        
        # Initialize Jinja2 environment if available
        if Template:
            self.env = Environment(
                loader=FileSystemLoader(self.template_dir) if os.path.exists(self.template_dir) else None,
                trim_blocks=True,
                lstrip_blocks=True
            )
        else:
            self.env = None
    
    def set_context(self, context_data):
        """Set the context data for prompt generation"""
        self.context = context_data
    
    def generate_phase1_prompt(self, business_data):
        """Generate Phase 1: Business Intelligence Analysis prompt"""
        template_content = """
# Phase 1: Business Intelligence Analysis

I need you to analyze this business and provide strategic insights for PPC campaign development.

## Business Context:
- **Business Name**: {{business_name}}
- **Industry**: {{industry}}
- **Location**: {{location}} (Service Area: {{service_area}})
- **Website**: {{website}}

## Business Description:
{{description}}

## Services Offered:
{{services}}

## Unique Value Proposition:
{{unique_value}}

## Target Audience:
{{target_audience}}

## Customer Pain Points:
{{customer_pain_points}}

## Customer Demographics:
{{customer_demographics}}

## Current Marketing:
{{current_marketing}}

## Campaign Objectives:
- Primary Goal: {{primary_goal}}
- Budget Range: {{budget_range}}
- Success Metrics: {{success_metrics}}

## Seasonal Considerations:
{{seasonal_trends}}

## Biggest Challenges:
{{biggest_challenges}}

## Analysis Required:

Please provide a comprehensive business intelligence analysis including:

1. **Market Position Assessment**
   - Industry landscape analysis for {{industry}} in {{location}}
   - Business maturity and growth potential assessment
   - Market opportunity size estimation
   - Competitive intensity evaluation

2. **Competitive Advantages Analysis**
   - Unique differentiators based on: {{unique_value}}
   - Competitive moats and barriers to entry
   - Value proposition strengths and weaknesses
   - Sustainable competitive advantages

3. **Target Market Deep Dive**
   - Primary audience segment analysis: {{target_audience}}
   - Secondary audience opportunities
   - Customer journey mapping for {{primary_goal}}
   - Pain point prioritization: {{customer_pain_points}}

4. **PPC Campaign Strategy Foundation**
   - Recommended campaign types for {{budget_range}} budget
   - Platform prioritization (Google Ads vs Meta vs others)
   - Budget allocation suggestions across campaigns
   - Priority targeting strategies for {{primary_goal}}

5. **Growth Opportunities**
   - Untapped market segments in {{service_area}}
   - Service expansion possibilities beyond: {{services}}
   - Geographic expansion potential
   - Revenue stream diversification opportunities

6. **Risk Assessment**
   - Market entry barriers and challenges
   - Competitive threats and responses
   - Economic and seasonal risks: {{seasonal_trends}}
   - Operational risks and mitigation strategies

7. **Success Metrics Framework**
   - KPI alignment with {{success_metrics}}
   - Leading vs lagging indicators
   - Benchmark establishment
   - ROI measurement framework

Please provide specific, actionable insights that will inform our PPC strategy development. Focus on opportunities that can be captured with a {{budget_range}} monthly budget targeting {{primary_goal}}.
"""
        
        if Template:
            template = Template(template_content)
            return template.render(**business_data)
        else:
            # Fallback to basic string formatting
            return template_content.format(**business_data)
    
    def generate_phase2_prompt(self, business_data):
        """Generate Phase 2: Competitive Landscape Mapping prompt"""
        competitors_list = "\n".join(f"- {comp}" for comp in business_data.get('competitors', []))
        
        template_content = f"""
# Phase 2: Competitive Landscape Mapping

Based on the business intelligence from Phase 1, I need you to analyze the competitive landscape for PPC campaign planning.

## Business Context (from Phase 1):
- **Business**: {business_data.get('business_name', '')} - {business_data.get('description', '')}
- **Industry**: {business_data.get('industry', '')}
- **Location**: {business_data.get('location', '')}
- **Services**: {business_data.get('services', '')}
- **Unique Value**: {business_data.get('unique_value', '')}
- **Target Audience**: {business_data.get('target_audience', '')}
- **Budget Range**: {business_data.get('budget_range', '')}

## Known Competitors:
{competitors_list}

## Competitive Analysis Required:

Please provide a comprehensive competitive landscape analysis including:

1. **Direct Competitor Identification**
   - Who are the main direct competitors in {business_data.get('industry', '')}?
   - What are their primary service offerings vs our services: {business_data.get('services', '')}?
   - How do they position themselves in the {business_data.get('location', '')} market?
   - What are their estimated market shares?

2. **Indirect Competitor Analysis**
   - Who are the indirect competitors and substitute services?
   - What adjacent industries compete for the same customers: {business_data.get('target_audience', '')}?
   - What alternative solutions do customers consider?
   - What DIY or self-service options exist?

3. **Competitive Positioning Map**
   - How do competitors position on price vs. quality spectrum?
   - What are the main positioning themes in {business_data.get('industry', '')}?
   - Where are the positioning gaps we can exploit?
   - How does our unique value fit: {business_data.get('unique_value', '')}?

4. **Competitor PPC Strategy Analysis**
   - What keywords are competitors likely targeting for {business_data.get('services', '')}?
   - What ad messaging themes do they probably use?
   - What are their likely campaign objectives and budget ranges?
   - What landing page strategies might they employ?

5. **Competitive Advantages Analysis**
   - What advantages do competitors have over us?
   - What are their key weaknesses we can exploit?
   - How can we differentiate based on: {business_data.get('unique_value', '')}?
   - What competitive gaps exist in serving: {business_data.get('target_audience', '')}?

6. **Market Share and Growth Analysis**
   - Who are the market leaders in {business_data.get('location', '')}?
   - What's the competitive intensity and saturation level?
   - Where are the growth opportunities with {business_data.get('budget_range', '')} budget?
   - What market segments are underserved?

7. **Competitive Threat Assessment**
   - Which competitors pose the biggest threat to our {business_data.get('primary_goal', '')} goal?
   - What competitive responses should we expect to our PPC campaigns?
   - How can we defend against competitive attacks?
   - What first-mover advantages can we capture?

8. **Competitive Intelligence for PPC**
   - What can we learn from competitor websites and marketing?
   - What messaging themes are overused vs underutilized?
   - What seasonal patterns do competitors follow?
   - What technology and tools do they likely use?

Please provide specific, actionable insights for PPC campaign development that help us outperform competitors with strategic positioning and execution.
"""
        
        return template_content
    
    def generate_phase3_prompt(self, business_data):
        """Generate Phase 3: Market Gap Identification prompt"""
        template_content = f"""
# Phase 3: Market Gap Identification

Building on the business intelligence and competitive analysis, I need you to identify specific market gaps and opportunities for PPC exploitation.

## Business Context:
- **Business**: {business_data.get('business_name', '')}
- **Industry**: {business_data.get('industry', '')} in {business_data.get('location', '')}
- **Services**: {business_data.get('services', '')}
- **Target Audience**: {business_data.get('target_audience', '')}
- **Unique Value**: {business_data.get('unique_value', '')}
- **Primary Goal**: {business_data.get('primary_goal', '')}
- **Budget Range**: {business_data.get('budget_range', '')}

## Market Gap Analysis Required:

Please identify and analyze market gaps and opportunities that can be exploited through strategic PPC campaigns:

1. **Service Delivery Gaps**
   - What service aspects are underserved in {business_data.get('industry', '')}?
   - What customer needs are not being met by current offerings?
   - What service combinations or packages are missing?
   - What quality levels are underrepresented?

2. **Geographic and Location Gaps**
   - What areas within {business_data.get('service_area', business_data.get('location', ''))} are underserved?
   - Where are competitors weak or completely absent?
   - What location-specific opportunities exist?
   - What travel/distance advantages can we leverage?

3. **Audience and Demographic Gaps**
   - What customer segments within {business_data.get('target_audience', '')} are underserved?
   - What age groups, income levels, or lifestyle segments are competitors missing?
   - What psychographic groups are being overlooked?
   - What niche audiences could we target?

4. **Messaging and Communication Gaps**
   - What messages are competitors in {business_data.get('industry', '')} not using?
   - What emotional triggers are being missed for {business_data.get('target_audience', '')}?
   - What value propositions are unexplored?
   - What pain points are not being addressed: {business_data.get('customer_pain_points', '')}?

5. **Channel and Platform Gaps**
   - What digital marketing channels are underutilized in {business_data.get('industry', '')}?
   - What social media platforms are competitors not using effectively?
   - What advertising formats or placements are missed?
   - What touchpoints in the customer journey are neglected?

6. **Timing and Seasonal Gaps**
   - What seasonal opportunities are missed: {business_data.get('seasonal_trends', '')}?
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
   - What educational content is missing for {business_data.get('target_audience', '')}?
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
- **Budget allocation recommendations for {business_data.get('budget_range', '')}**
- **Expected ROI and timeline for {business_data.get('primary_goal', '')}**

Focus on gaps that can be immediately exploited through strategic PPC campaigns with our available budget and resources.
"""
        
        return template_content
    
    def generate_phase4_prompt(self, business_data):
        """Generate Phase 4: Strategic Positioning Development prompt"""
        template_content = f"""
# Phase 4: Strategic Positioning Development

Based on the comprehensive analysis from previous phases, I need you to develop a strategic positioning strategy specifically optimized for PPC campaign success.

## Business Context Summary:
- **Business**: {business_data.get('business_name', '')}
- **Industry**: {business_data.get('industry', '')} in {business_data.get('location', '')}
- **Services**: {business_data.get('services', '')}
- **Target Audience**: {business_data.get('target_audience', '')}
- **Unique Value**: {business_data.get('unique_value', '')}
- **Budget Range**: {business_data.get('budget_range', '')}
- **Primary Goal**: {business_data.get('primary_goal', '')}
- **Success Metrics**: {business_data.get('success_metrics', '')}

## Strategic Positioning Development Required:

Please develop a comprehensive positioning strategy optimized for PPC performance:

1. **Core Positioning Statement**
   - Primary positioning theme that differentiates us in {business_data.get('industry', '')}
   - Unique value proposition that resonates with {business_data.get('target_audience', '')}
   - Competitive differentiation based on: {business_data.get('unique_value', '')}
   - Alignment with {business_data.get('primary_goal', '')} campaign objectives

2. **Positioning Pillars Framework**
   - 3-5 key positioning pillars that support our main position
   - Supporting evidence and proof points for each pillar
   - How each pillar differentiates from main competitors
   - Relevance ranking for {business_data.get('target_audience', '')}

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
   - Primary audience positioning for {business_data.get('target_audience', '')}
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
   - Lead generation campaign positioning ({business_data.get('primary_goal', '')})
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
    - Phase 1: Core positioning launch ({business_data.get('budget_range', '')} budget)
    - Phase 2: Positioning refinement and optimization
    - Phase 3: Positioning expansion and scaling
    - Success metrics tracking aligned with: {business_data.get('success_metrics', '')}

11. **Crisis and Competitive Response Positioning**
    - Positioning defense strategies
    - Rapid response positioning for competitive moves
    - Crisis communication positioning
    - Positioning recovery and reinforcement tactics

12. **Local and Geographic Positioning**
    - Location-specific positioning for {business_data.get('location', '')}
    - Regional advantages and local credibility
    - Community connection and local expertise positioning
    - Geographic expansion positioning framework

Please provide specific, immediately actionable positioning strategies that can be implemented across all PPC campaigns to maximize {business_data.get('primary_goal', '')} results within our {business_data.get('budget_range', '')} budget.
"""
        
        return template_content
    
    def generate_phase5_prompt(self, business_data):
        """Generate Phase 5: Content & Campaign Strategy prompt"""
        template_content = f"""
# Phase 5: Content & Campaign Strategy

Based on all previous strategic analysis, I need you to develop comprehensive, immediately actionable content and campaign strategies for PPC implementation.

## Complete Business Context:
- **Business**: {business_data.get('business_name', '')}
- **Industry**: {business_data.get('industry', '')} in {business_data.get('location', '')}
- **Services**: {business_data.get('services', '')}
- **Target Audience**: {business_data.get('target_audience', '')}
- **Unique Value**: {business_data.get('unique_value', '')}
- **Budget Range**: {business_data.get('budget_range', '')}
- **Primary Goal**: {business_data.get('primary_goal', '')}
- **Success Metrics**: {business_data.get('success_metrics', '')}

## Comprehensive Implementation Strategy Required:

Please develop detailed, actionable strategies for immediate PPC campaign implementation:

1. **Complete Campaign Architecture**
   - Campaign types recommendation (Search, Display, Performance Max, Video, Shopping)
   - Campaign structure and naming conventions
   - Budget allocation across campaigns for {business_data.get('budget_range', '')}
   - Bidding strategy recommendations for {business_data.get('primary_goal', '')}
   - Geographic targeting strategy for {business_data.get('location', '')}

2. **Advanced Keyword Strategy**
   - Primary keyword themes for {business_data.get('services', '')}
   - Secondary and long-tail keyword opportunities
   - Local keyword variations for {business_data.get('location', '')}
   - Seasonal keyword calendar: {business_data.get('seasonal_trends', '')}
   - Negative keyword strategy and exclusions
   - Keyword grouping for optimal ad relevance

3. **Comprehensive Ad Copy Strategy**
   - 10+ headline variations (30 characters each)
   - 10+ description variations (90 characters each)
   - Compelling call-to-action options
   - Ad extension strategies (sitelinks, callouts, structured snippets)
   - Emotional vs. rational copy balance
   - Industry-specific messaging for {business_data.get('industry', '')}

4. **Landing Page Optimization Strategy**
   - Landing page requirements for {business_data.get('primary_goal', '')}
   - Content structure and layout recommendations
   - Conversion optimization elements
   - A/B testing opportunities and priorities
   - Mobile optimization requirements
   - Page speed and technical requirements

5. **Advanced Audience Targeting Strategy**
   - Demographics targeting for {business_data.get('target_audience', '')}
   - Interest and behavior targeting
   - Custom audience creation strategies
   - Lookalike audience development
   - Retargeting campaign structure
   - Audience exclusions and negative targeting

6. **Content Calendar and Creative Strategy**
   - 3-month content calendar with weekly themes
   - Monthly content pillars aligned with {business_data.get('services', '')}
   - Seasonal content planning: {business_data.get('seasonal_trends', '')}
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
   - Conversion tracking setup for {business_data.get('primary_goal', '')}
   - Key performance indicators aligned with: {business_data.get('success_metrics', '')}
   - Attribution modeling recommendations
   - ROI measurement and reporting structure
   - Optimization schedule and methodology

9. **Budget Management and Pacing**
   - Daily budget allocation for {business_data.get('budget_range', '')}
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

Please provide specific, actionable strategies with exact implementation steps, recommended settings, and expected outcomes. Focus on tactics that can be immediately implemented to achieve {business_data.get('primary_goal', '')} with our {business_data.get('budget_range', '')} budget.

Include specific examples of:
- Ad headlines and descriptions
- Keyword lists and groupings
- Audience targeting parameters
- Landing page elements
- Conversion tracking codes
- Campaign settings and configurations

This should be a complete blueprint for PPC campaign success.
"""
        
        return template_content
    
    def generate_all_prompts(self, business_data):
        """Generate all 5 phase prompts"""
        prompts = {
            'phase1': self.generate_phase1_prompt(business_data),
            'phase2': self.generate_phase2_prompt(business_data),
            'phase3': self.generate_phase3_prompt(business_data),
            'phase4': self.generate_phase4_prompt(business_data),
            'phase5': self.generate_phase5_prompt(business_data)
        }
        return prompts
    
    def save_prompts_to_files(self, prompts, output_dir):
        """Save generated prompts to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        filenames = {
            'phase1': 'phase1_business_intelligence_prompt.md',
            'phase2': 'phase2_competitive_landscape_prompt.md',
            'phase3': 'phase3_market_gaps_prompt.md',
            'phase4': 'phase4_strategic_positioning_prompt.md',
            'phase5': 'phase5_content_strategy_prompt.md'
        }
        
        saved_files = []
        for phase, prompt_content in prompts.items():
            filename = filenames[phase]
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(prompt_content)
            
            saved_files.append(filepath)
        
        return saved_files
    
    def create_custom_prompt(self, template_content, business_data):
        """Create a custom prompt from template content"""
        if Template:
            template = Template(template_content)
            return template.render(**business_data)
        else:
            # Basic string formatting fallback
            try:
                return template_content.format(**business_data)
            except KeyError:
                # Return template as-is if formatting fails
                return template_content
    
    def get_template_variables(self, template_content):
        """Extract template variables from content"""
        variables = set()
        
        if Template:
            # Use Jinja2 to parse template variables
            try:
                template = Template(template_content)
                variables = template.environment.parse(template_content).find_all()
            except:
                pass
        
        # Fallback: simple regex to find {{variable}} patterns
        import re
        matches = re.findall(r'\{\{([^}]+)\}\}', template_content)
        for match in matches:
            variables.add(match.strip())
        
        return list(variables)

# Example usage and testing
if __name__ == "__main__":
    # Example business data
    sample_business_data = {
        'business_name': 'Reality Events',
        'industry': 'Event Decoration',
        'location': 'Brisbane',
        'service_area': 'Brisbane and Gold Coast',
        'website': 'https://realityevents.com.au',
        'description': 'Balloon garland hiring company specializing in events like birthdays, anniversaries, and corporate events',
        'services': 'Balloon garlands, balloon walls, balloon arches, event styling',
        'unique_value': 'Premium quality balloons with custom color matching and professional installation',
        'target_audience': 'Event planners, families celebrating special occasions, corporate event coordinators',
        'customer_pain_points': 'Lack of time to set up decorations, desire for professional-looking events, stress of event planning',
        'customer_demographics': 'Ages 25-55, household income $60k+, values quality and convenience',
        'competitors': ['Balloon Room & Co', 'Rainbow Events', 'Pretty The Party'],
        'primary_goal': 'Lead Generation',
        'budget_range': '$2500-$5000',
        'success_metrics': 'Cost per lead under $50, 20+ qualified leads per month',
        'seasonal_trends': 'Peak seasons: December (Christmas), March-May (Easter, Mother\'s Day), September-November (Spring events)',
        'current_marketing': 'Social media, word of mouth, Google My Business',
        'biggest_challenges': 'Seasonal fluctuations, competition from DIY options, time-intensive setup process'
    }
    
    # Create generator and test
    generator = PromptGenerator()
    prompts = generator.generate_all_prompts(sample_business_data)
    
    print("Generated prompts for all 5 phases:")
    for phase, prompt in prompts.items():
        print(f"\n{'='*50}")
        print(f"PHASE {phase.upper()}")
        print(f"{'='*50}")
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)