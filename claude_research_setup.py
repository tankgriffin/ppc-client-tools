#!/usr/bin/env python3
"""
Claude AI Research Setup Script
Replaces manual competitor research with AI-powered strategic intelligence
Usage: python3 claude_research_setup.py "Client Name"
"""

import os
import sys
import json
import time
import re
from datetime import datetime
from pathlib import Path

try:
    import click
    from jinja2 import Template
    import yaml
except ImportError:
    print("❌ Missing required dependencies. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "click", "jinja2", "pyyaml", "rich"])
    import click
    from jinja2 import Template
    import yaml

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Rich library not available, using basic output")
    Console = None

class ClaudeResearchSetup:
    def __init__(self, client_name):
        self.client_name = client_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.console = Console() if Console else None
        
        # Find existing client folder or create sanitized name
        self.folder_name = self.find_existing_folder(client_name)
        
        # Create necessary directories
        self.setup_directories()
        
        # Business intelligence data
        self.business_data = {}
        
        # Generated prompts
        self.generated_prompts = {}

    def find_existing_folder(self, client_name):
        """Find existing client folder or return sanitized name"""
        sanitized = client_name.lower().replace(' ', '_')
        variations = [sanitized, client_name.replace(' ', '_'), client_name.replace(' ', '-')]
        
        for variation in variations:
            if os.path.exists(variation):
                self.print_info(f"📁 Found existing folder: {variation}")
                return variation
        
        self.print_info(f"📁 Creating new folder: {sanitized}")
        return sanitized

    def setup_directories(self):
        """Create necessary directories for Claude research"""
        dirs_to_create = [
            f"{self.folder_name}/02_market_research/claude_research",
            f"{self.folder_name}/02_market_research/claude_research/phase_outputs",
            f"{self.folder_name}/02_market_research/market_intelligence",
            f"{self.folder_name}/03_business_intel/ai_insights",
            f"{self.folder_name}/templates"
        ]
        
        for dir_path in dirs_to_create:
            os.makedirs(dir_path, exist_ok=True)

    def print_header(self, text):
        """Print formatted header"""
        if self.console:
            self.console.print(Panel(text, style="bold blue"))
        else:
            print(f"\n{'='*70}")
            print(f"🎯 {text}")
            print('='*70)

    def print_info(self, text):
        """Print formatted info"""
        if self.console:
            self.console.print(text, style="cyan")
        else:
            print(f"💡 {text}")

    def print_success(self, text):
        """Print formatted success"""
        if self.console:
            self.console.print(text, style="green")
        else:
            print(f"✅ {text}")

    def print_warning(self, text):
        """Print formatted warning"""
        if self.console:
            self.console.print(text, style="yellow")
        else:
            print(f"⚠️  {text}")

    def collect_business_intelligence(self):
        """Interactive CLI to gather comprehensive business context"""
        self.print_header(f"Claude AI Research Setup for {self.client_name}")
        
        self.print_info("This interactive setup will collect business intelligence and generate customized Claude prompts")
        self.print_info("Please provide detailed information for the best results\n")

        # Basic Business Information
        self.print_header("📊 Business Information")
        
        if self.console:
            self.business_data['business_name'] = Prompt.ask("Business Name", default=self.client_name)
            self.business_data['industry'] = Prompt.ask("Industry/Sector", default="Event Services")
            self.business_data['website'] = Prompt.ask("Website URL", default="")
            self.business_data['location'] = Prompt.ask("Primary Location/City", default="")
            self.business_data['service_area'] = Prompt.ask("Service Area/Region", default="")
        else:
            self.business_data['business_name'] = input(f"Business Name [{self.client_name}]: ") or self.client_name
            self.business_data['industry'] = input("Industry/Sector [Event Services]: ") or "Event Services"
            self.business_data['website'] = input("Website URL: ")
            self.business_data['location'] = input("Primary Location/City: ")
            self.business_data['service_area'] = input("Service Area/Region: ")

        # Detailed Business Description
        self.print_header("📝 Business Description")
        self.print_info("Provide a detailed description of the business, services, and what makes it unique")
        
        if self.console:
            self.business_data['description'] = Prompt.ask("Business Description (detailed)")
            self.business_data['services'] = Prompt.ask("Main Services Offered")
            self.business_data['unique_value'] = Prompt.ask("What makes this business unique?")
        else:
            print("Business Description (detailed):")
            self.business_data['description'] = input("> ")
            print("Main Services Offered:")
            self.business_data['services'] = input("> ")
            print("What makes this business unique?:")
            self.business_data['unique_value'] = input("> ")

        # Target Audience
        self.print_header("🎯 Target Audience")
        
        if self.console:
            self.business_data['target_audience'] = Prompt.ask("Primary Target Audience")
            self.business_data['customer_pain_points'] = Prompt.ask("Customer Pain Points/Problems Solved")
            self.business_data['customer_demographics'] = Prompt.ask("Customer Demographics (age, income, etc.)")
        else:
            print("Primary Target Audience:")
            self.business_data['target_audience'] = input("> ")
            print("Customer Pain Points/Problems Solved:")
            self.business_data['customer_pain_points'] = input("> ")
            print("Customer Demographics (age, income, etc.):")
            self.business_data['customer_demographics'] = input("> ")

        # Competitive Context
        self.print_header("🏢 Competitive Context")
        
        competitors = []
        self.print_info("Enter competitor information (press Enter on empty line to finish)")
        
        while True:
            if self.console:
                competitor = Prompt.ask("Competitor Name/Website", default="")
            else:
                competitor = input("Competitor Name/Website: ").strip()
            
            if not competitor:
                break
            competitors.append(competitor)
        
        self.business_data['competitors'] = competitors

        # Client Type Selection
        self.print_header("🎯 Client Type & Services")
        
        print("What type of digital marketing services will this client need?")
        print("1. PPC Only (Google Ads, Meta Ads, etc.)")
        print("2. SEO Only (Organic search optimization)")
        print("3. Both PPC and SEO (Integrated approach)")
        while True:
            client_type_choice = input("Enter choice (1-3): ").strip()
            if client_type_choice.isdigit() and 1 <= int(client_type_choice) <= 3:
                client_types = ["PPC_ONLY", "SEO_ONLY", "BOTH"]
                self.business_data['client_type'] = client_types[int(client_type_choice)-1]
                break
            else:
                print("Please select a valid option (1-3)")

        # Campaign Objectives
        self.print_header("📈 Campaign Objectives")
        
        # Always use fallback for better compatibility
        print("Primary Campaign Goal:")
        print("1. Lead Generation  2. Sales  3. Brand Awareness  4. Website Traffic")
        while True:
            goal_choice = input("Enter choice (1-4): ").strip()
            if goal_choice.isdigit() and 1 <= int(goal_choice) <= 4:
                goals = ["Lead Generation", "Sales", "Brand Awareness", "Website Traffic"]
                self.business_data['primary_goal'] = goals[int(goal_choice)-1]
                break
            else:
                print("Please select a valid option (1-4)")
        
        print("\nMonthly Budget Range:")
        print("1. $500-$1000  2. $1000-$2500  3. $2500-$5000  4. $5000+")
        while True:
            budget_choice = input("Enter choice (1-4): ").strip()
            if budget_choice.isdigit() and 1 <= int(budget_choice) <= 4:
                budgets = ["$500-$1000", "$1000-$2500", "$2500-$5000", "$5000+"]
                self.business_data['budget_range'] = budgets[int(budget_choice)-1]
                break
            else:
                print("Please select a valid option (1-4)")
        
        self.business_data['success_metrics'] = input("Key Success Metrics: ")

        # Additional Context
        self.print_header("🔍 Additional Context")
        
        if self.console:
            self.business_data['seasonal_trends'] = Prompt.ask("Seasonal Trends/Patterns", default="None")
            self.business_data['current_marketing'] = Prompt.ask("Current Marketing Channels", default="None")
            self.business_data['biggest_challenges'] = Prompt.ask("Biggest Business Challenges", default="None")
        else:
            self.business_data['seasonal_trends'] = input("Seasonal Trends/Patterns [None]: ") or "None"
            self.business_data['current_marketing'] = input("Current Marketing Channels [None]: ") or "None"
            self.business_data['biggest_challenges'] = input("Biggest Business Challenges [None]: ") or "None"

        self.print_success("Business intelligence collection complete!")
        return self.business_data

    def generate_claude_prompts(self):
        """Generate customized Claude prompts based on client type"""
        client_type = self.business_data.get('client_type', 'BOTH')
        
        if client_type == 'PPC_ONLY':
            self.print_header("🧠 Generating PPC-Focused Claude Prompts")
        elif client_type == 'SEO_ONLY':
            self.print_header("🧠 Generating SEO-Focused Claude Prompts")
        else:
            self.print_header("🧠 Generating Integrated PPC + SEO Claude Prompts")
        
        # Define phase templates based on client type
        client_type = self.business_data.get('client_type', 'BOTH')
        
        # PPC-ONLY PHASE TEMPLATES (1-5)
        if client_type == 'PPC_ONLY':
            templates = {
                'phase1': """# Phase 1: Business Intelligence Analysis (PPC Focus)

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
   - Industry landscape analysis
   - Business maturity and growth potential
   - Market opportunity size for paid advertising

2. **Competitive Advantages**
   - Unique differentiators for PPC messaging
   - Competitive moats that can be leveraged in ads
   - Value proposition strengths for ad copy

3. **Target Market Analysis**
   - Primary audience segments for PPC targeting
   - Secondary audience opportunities for expansion
   - Customer journey mapping for PPC touchpoints

4. **PPC Campaign Strategy Foundation**
   - Recommended campaign types (Search, Display, Video, Shopping)
   - Budget allocation suggestions across platforms
   - Priority targeting strategies and audience segments

5. **Growth Opportunities**
   - Untapped market segments for PPC expansion
   - Service expansion possibilities through paid ads
   - Geographic expansion potential via PPC

6. **Risk Assessment**
   - Potential PPC challenges and mitigation strategies
   - Competitive threats in paid advertising
   - Market risks affecting PPC performance

Please provide actionable insights that will inform our PPC strategy development.""",

                'phase2': """# Phase 2: Competitive Landscape Analysis (PPC Focus)

Based on the business intelligence from Phase 1, I need you to analyze the competitive landscape specifically for PPC campaign planning.

## Business Context (from Phase 1):
- **Business**: {{business_name}} - {{description}}
- **Industry**: {{industry}}
- **Location**: {{location}}
- **Services**: {{services}}
- **Unique Value**: {{unique_value}}

## Known Competitors:
{% for competitor in competitors %}
- {{competitor}}
{% endfor %}

## Target Audience:
{{target_audience}}

## Budget Range:
{{budget_range}}

## Campaign Objective:
{{primary_goal}}

## Competitive Analysis Required:

Please conduct a comprehensive competitive landscape analysis focused on PPC advertising:

1. **Competitor PPC Strategy Assessment**
   - Estimated competitor ad spend and platform presence
   - Primary keywords they likely target
   - Ad messaging themes and value propositions
   - Landing page strategies and conversion funnels

2. **Market Positioning Analysis**
   - How competitors position themselves in paid ads
   - Unique selling propositions used in ad copy
   - Pricing strategies reflected in advertising
   - Service differentiation in PPC messaging

3. **PPC Opportunity Gaps**
   - Underserved keywords with commercial intent
   - Audience segments competitors aren't targeting
   - Geographic markets with less competition
   - Times/seasons when competition is lighter

4. **Competitive Threats**
   - Direct competitors with strong PPC presence
   - Indirect competitors entering the space
   - Larger players with bigger budgets
   - New market entrants to watch

5. **Strategic Advantages**
   - Areas where {{business_name}} can outcompete
   - Unique value propositions for ad differentiation
   - Local market advantages for geo-targeting
   - Service specializations for niche targeting

6. **PPC Platform Recommendations**
   - Best platforms based on competitor analysis
   - Campaign types with least competition
   - Optimal bidding strategies vs competitors
   - Budget allocation to outmaneuver competition

Focus on actionable insights that will help {{business_name}} compete effectively in the paid advertising space.""",

                'phase3': """# Phase 3: Market Gap Analysis (PPC Focus)

Building on the insights from Phases 1 and 2, I need you to identify specific market gaps and opportunities for PPC campaigns.

## Business Context:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Services**: {{services}}
- **Target Audience**: {{target_audience}}
- **Budget**: {{budget_range}}
- **Primary Goal**: {{primary_goal}}

## Previous Analysis Context:
We've completed business intelligence analysis and competitive landscape mapping. Now we need to identify specific market gaps where {{business_name}} can gain competitive advantage through strategic PPC campaigns.

## Market Gap Analysis Required:

Please provide a detailed analysis of market gaps and PPC opportunities:

1. **Keyword Gap Analysis**
   - High-intent keywords with low competition
   - Long-tail keyword opportunities competitors miss
   - Local search terms with commercial intent
   - Seasonal keywords with opportunity windows

2. **Audience Segment Gaps**
   - Underserved demographic segments
   - Psychographic profiles competitors ignore
   - Income levels or life stages not targeted
   - Geographic micro-markets with potential

3. **Service/Product Gaps**
   - Services {{business_name}} offers that competitors don't highlight
   - Unique specializations for niche PPC targeting
   - Premium services that justify higher CPCs
   - Bundled offerings competitors don't promote

4. **Platform and Format Gaps**
   - PPC platforms competitors aren't using effectively
   - Ad formats (video, shopping, display) with opportunities
   - Device targeting gaps (mobile vs desktop)
   - Time-of-day or day-of-week opportunities

5. **Local Market Advantages**
   - Geographic areas with less PPC competition
   - Local events or trends for timely campaigns
   - Community connections for social proof in ads
   - Regional preferences competitors miss

6. **Customer Journey Gaps**
   - Awareness stage keyword opportunities
   - Consideration phase content gaps
   - Decision stage conversion opportunities
   - Post-purchase upsell and retention gaps

7. **Messaging and Positioning Gaps**
   - Emotional appeals competitors don't use
   - Rational benefits not highlighted by others
   - Trust signals and credibility factors
   - Problem-solution angles overlooked

For each gap identified, please suggest specific PPC strategies and tactics to capitalize on these opportunities.""",

                'phase4': """# Phase 4: Strategic Positioning for PPC Campaigns

Based on the comprehensive analysis from Phases 1-3, I need you to develop a strategic positioning framework specifically designed for PPC campaign success.

## Business Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Unique Value**: {{unique_value}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}
- **Budget Range**: {{budget_range}}

## Strategic Context:
We've analyzed the business intelligence, competitive landscape, and market gaps. Now we need to synthesize these insights into a clear strategic positioning that will drive PPC campaign messaging, targeting, and optimization.

## Strategic Positioning Development Required:

Please develop a comprehensive PPC-focused strategic positioning framework:

1. **Core PPC Value Proposition**
   - Primary message for all PPC campaigns
   - Unique selling proposition for ad headlines
   - Competitive differentiation for ad copy
   - Emotional and rational benefits balance

2. **Target Audience Segmentation for PPC**
   - Primary audience segment (80% of budget focus)
   - Secondary audience segments for expansion
   - Audience personas with PPC targeting details
   - Customer journey stage targeting strategies

3. **Keyword Strategy Foundation**
   - Primary keyword themes for core campaigns
   - Long-tail keyword strategies for niche targeting
   - Branded vs non-branded keyword approaches
   - Negative keyword strategies to avoid waste

4. **Campaign Architecture Strategy**
   - Recommended campaign structure and organization
   - Ad group themes and keyword clustering
   - Landing page strategy and user experience
   - Conversion tracking and attribution setup

5. **Competitive Positioning in Ads**
   - How to position against direct competitors
   - Indirect competitor differentiation strategies
   - Premium positioning vs value positioning
   - Local market advantages to emphasize

6. **Platform-Specific Positioning**
   - Google Ads positioning and messaging
   - Meta/Facebook Ads social proof angles
   - LinkedIn positioning for B2B (if applicable)
   - Platform-specific value propositions

7. **Budget Allocation Strategy**
   - Campaign prioritization based on ROI potential
   - Geographic targeting and budget distribution
   - Seasonal budget allocation recommendations
   - Growth vs maintenance campaign balance

8. **Success Metrics and KPIs**
   - Primary success metrics for {{primary_goal}}
   - Secondary metrics for optimization
   - Conversion tracking requirements
   - ROI benchmarks and targets

This strategic positioning should serve as the foundation for all PPC campaign development and optimization decisions.""",

                'phase5': """# Phase 5: PPC Campaign Content Strategy

Based on the strategic positioning developed in Phase 4, I need you to create a comprehensive content strategy specifically for PPC campaigns.

## Strategic Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}
- **Budget Range**: {{budget_range}}
- **Unique Value**: {{unique_value}}

## Campaign Context:
We've established the strategic positioning for PPC campaigns. Now we need to translate this strategy into specific content themes, ad copy frameworks, and campaign execution plans.

## PPC Content Strategy Development Required:

Please develop a comprehensive PPC content strategy:

1. **Ad Copy Framework**
   - Headline formulas for different campaign types
   - Description templates for various audiences
   - Call-to-action variations for different goals
   - Ad extensions strategy (sitelinks, callouts, etc.)

2. **Campaign-Specific Content Themes**
   - Search campaign messaging hierarchy
   - Display campaign visual and text concepts
   - Video campaign storytelling approaches
   - Shopping campaign product positioning

3. **Audience-Targeted Messaging**
   - Primary audience segment ad copy variations
   - Secondary audience customized messaging
   - Demographic-specific value propositions
   - Geographic targeting message customization

4. **Keyword-Aligned Content**
   - High-intent keyword ad copy matching
   - Long-tail keyword specific messaging
   - Branded keyword protective strategies
   - Competitor keyword positioning angles

5. **Landing Page Content Strategy**
   - Campaign-specific landing page recommendations
   - Conversion optimization content elements
   - Form optimization and lead capture
   - Mobile-specific content considerations

6. **Creative Asset Requirements**
   - Image specifications and concepts for display
   - Video script outlines and key messages
   - Logo variations and brand assets needed
   - Seasonal creative adaptation plans

7. **Testing and Optimization Framework**
   - A/B testing priorities for ad copy elements
   - Landing page testing roadmap
   - Creative rotation and refresh schedule
   - Performance optimization content updates

8. **Campaign Launch Roadmap**
   - Phase 1: Core campaigns and essential content
   - Phase 2: Expansion campaigns and testing
   - Phase 3: Optimization and scaling content
   - Timeline and priority recommendations

9. **Content Calendar Integration**
   - Seasonal campaign content planning
   - Industry event and holiday optimization
   - Product/service launch campaign support
   - Regular refresh and update schedule

10. **Performance Tracking and Content Iteration**
    - Content performance metrics to monitor
    - Copy testing insights to implement
    - Landing page optimization priorities
    - Long-term content evolution strategy

This content strategy should provide a complete roadmap for PPC campaign creation, launch, and ongoing optimization."""
            }

        # SEO-ONLY PHASE TEMPLATES (1-6)
        elif client_type == 'SEO_ONLY':
            templates = {
                'phase1': """# Phase 1: Business Intelligence Analysis (SEO Focus)

I need you to analyze this business and provide strategic insights for SEO strategy development.

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
   - Industry landscape analysis
   - Business maturity and growth potential
   - Market opportunity size for organic search

2. **SEO Competitive Advantages**
   - Unique differentiators for content marketing
   - Authority building opportunities
   - Value proposition strengths for organic visibility

3. **Target Market Analysis**
   - Primary audience segments for content targeting
   - Secondary audience opportunities for expansion
   - Customer journey mapping for organic touchpoints

4. **SEO Strategy Foundation**
   - Recommended content types and themes
   - Authority building priorities
   - Technical SEO considerations

5. **Growth Opportunities**
   - Untapped market segments for organic growth
   - Service expansion possibilities through content
   - Geographic expansion potential via local SEO

6. **Risk Assessment**
   - Potential SEO challenges and algorithm risks
   - Competitive threats in organic search
   - Market risks affecting organic performance

Please provide actionable insights that will inform our SEO strategy development.""",

                'phase2': """# Phase 2: Competitive Landscape Analysis (SEO Focus)

Based on the business intelligence from Phase 1, I need you to analyze the competitive landscape specifically for SEO strategy planning.

## Business Context (from Phase 1):
- **Business**: {{business_name}} - {{description}}
- **Industry**: {{industry}}
- **Location**: {{location}}
- **Services**: {{services}}
- **Unique Value**: {{unique_value}}

## Known Competitors:
{% for competitor in competitors %}
- {{competitor}}
{% endfor %}

## Target Audience:
{{target_audience}}

## Budget Range:
{{budget_range}}

## Campaign Objective:
{{primary_goal}}

## Competitive Analysis Required:

Please conduct a comprehensive competitive landscape analysis focused on SEO and organic search:

1. **Competitor SEO Strategy Assessment**
   - Estimated organic traffic and keyword rankings
   - Content strategy themes and approaches
   - Backlink profile strength and authority
   - Technical SEO implementation quality

2. **Market Positioning Analysis**
   - How competitors position themselves in content
   - Unique selling propositions in organic results
   - Content differentiation strategies
   - Authority signals and trust factors

3. **SEO Opportunity Gaps**
   - Underserved keywords with search volume
   - Content topics competitors aren't covering
   - Geographic markets with less competition
   - Niche areas with authority building potential

4. **Competitive Threats**
   - Direct competitors with strong domain authority
   - Indirect competitors ranking for key terms
   - Larger players with content teams
   - Authority sites encroaching on the space

5. **Strategic Advantages**
   - Areas where {{business_name}} can outcompete
   - Unique expertise for content authority
   - Local market advantages for geographic SEO
   - Service specializations for niche ranking

6. **Content and Authority Recommendations**
   - Best content types based on competitor analysis
   - Link building opportunities competitors miss
   - Social proof and E-A-T improvements needed
   - Technical SEO advantages to pursue

Focus on actionable insights that will help {{business_name}} compete effectively in organic search results.""",

                'phase3': """# Phase 3: Market Gap Analysis (SEO Focus)

Building on the insights from Phases 1 and 2, I need you to identify specific market gaps and opportunities for SEO strategy.

## Business Context:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Services**: {{services}}
- **Target Audience**: {{target_audience}}
- **Budget**: {{budget_range}}
- **Primary Goal**: {{primary_goal}}

## Previous Analysis Context:
We've completed business intelligence analysis and competitive landscape mapping. Now we need to identify specific market gaps where {{business_name}} can gain competitive advantage through strategic SEO efforts.

## Market Gap Analysis Required:

Please provide a detailed analysis of market gaps and SEO opportunities:

1. **Keyword Gap Analysis**
   - High-volume keywords with low competition
   - Long-tail keyword opportunities competitors miss
   - Local search terms with ranking potential
   - Seasonal keywords with opportunity windows

2. **Content Gap Analysis**
   - Topics competitors aren't covering comprehensively
   - Question-based content opportunities
   - How-to and educational content needs
   - Industry trend coverage gaps

3. **Service/Expertise Gaps**
   - Services {{business_name}} offers that lack content
   - Unique specializations for authority building
   - Premium services that justify in-depth content
   - Bundled offerings needing organic visibility

4. **Local SEO Opportunities**
   - Geographic areas with less organic competition
   - Local events or trends for timely content
   - Community connections for local authority
   - Regional preferences competitors miss

5. **Technical SEO Gaps**
   - Site speed and performance opportunities
   - Mobile optimization advantages
   - Schema markup implementation gaps
   - User experience improvements

6. **Customer Journey Content Gaps**
   - Awareness stage content opportunities
   - Consideration phase information needs
   - Decision stage comparison content
   - Post-purchase support and education

7. **Authority Building Gaps**
   - Industry expertise demonstration opportunities
   - Thought leadership content themes
   - Trust signal and credibility improvements
   - Expert positioning in search results

For each gap identified, please suggest specific SEO strategies and content approaches to capitalize on these opportunities.""",

                'phase4': """# Phase 4: Strategic Positioning for SEO Strategy

Based on the comprehensive analysis from Phases 1-3, I need you to develop a strategic positioning framework specifically designed for SEO success.

## Business Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Unique Value**: {{unique_value}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}
- **Budget Range**: {{budget_range}}

## Strategic Context:
We've analyzed the business intelligence, competitive landscape, and market gaps. Now we need to synthesize these insights into a clear strategic positioning that will drive SEO strategy, content creation, and authority building.

## Strategic Positioning Development Required:

Please develop a comprehensive SEO-focused strategic positioning framework:

1. **Core SEO Value Proposition**
   - Primary expertise theme for content authority
   - Unique positioning in search results
   - Competitive differentiation for organic visibility
   - Authority signals to emphasize

2. **Target Audience Segmentation for SEO**
   - Primary audience segment for content focus
   - Secondary audience segments for expansion
   - Search behavior patterns and intent mapping
   - Content journey optimization strategies

3. **Keyword Strategy Foundation**
   - Primary keyword themes for authority building
   - Long-tail keyword strategies for traffic
   - Branded vs industry keyword approaches
   - Local SEO keyword prioritization

4. **Content Strategy Architecture**
   - Core content pillars and themes
   - Content cluster organization and structure
   - Internal linking strategy framework
   - Content depth and expertise demonstration

5. **Competitive Positioning in Search**
   - How to outrank direct competitors
   - Indirect competitor differentiation strategies
   - Authority positioning vs accessibility balance
   - Local market advantages to leverage

6. **Technical SEO Positioning**
   - Site architecture and user experience focus
   - Page speed and performance priorities
   - Mobile-first optimization approach
   - Schema markup and rich snippets strategy

7. **Authority Building Strategy**
   - Expertise, Authoritativeness, Trustworthiness (E-A-T)
   - Industry thought leadership positioning
   - Local authority and community engagement
   - Link-worthy content and resource development

8. **Success Metrics and KPIs**
   - Primary success metrics for {{primary_goal}}
   - Organic traffic and ranking targets
   - Authority building measurement
   - Local SEO performance indicators

This strategic positioning should serve as the foundation for all SEO strategy development and content optimization decisions.""",

                'phase5': """# Phase 5: SEO Content Strategy and Keyword Research

Based on the strategic positioning developed in Phase 4, I need you to create a comprehensive content strategy and keyword research plan for SEO success.

## Strategic Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}
- **Budget Range**: {{budget_range}}
- **Unique Value**: {{unique_value}}

## SEO Context:
We've established the strategic positioning for SEO success. Now we need to translate this strategy into specific content themes, keyword targets, and SEO execution plans.

## SEO Content Strategy Development Required:

Please develop a comprehensive SEO content strategy:

1. **Keyword Research and Mapping**
   - Primary keyword targets with search volume and difficulty
   - Long-tail keyword opportunities for quick wins
   - Local SEO keyword variations and geo-targeting
   - Seasonal keyword opportunities and timing

2. **Content Pillar Strategy**
   - Core content pillars based on business expertise
   - Supporting content cluster organization
   - Internal linking strategy between content pieces
   - Authority building content hierarchy

3. **Content Type Optimization**
   - Blog post themes and formats for ranking
   - Service page optimization strategies
   - Resource and tool development for link building
   - FAQ and question-based content for featured snippets

4. **Search Intent Mapping**
   - Informational content for awareness stage
   - Commercial investigation content for consideration
   - Transactional content for decision stage
   - Navigational content for brand searches

5. **Technical Content Requirements**
   - Title tag and meta description optimization
   - Header structure and keyword placement
   - Image optimization and alt text strategy
   - Schema markup implementation plan

6. **Local SEO Content Strategy**
   - Location-specific content and landing pages
   - Google Business Profile optimization content
   - Local citation and directory content
   - Community engagement content themes

7. **Content Production Framework**
   - Content creation priority and timeline
   - Content depth and quality standards
   - Expert contributor and interview strategies
   - Content update and refresh schedule

8. **Link Building Content Strategy**
   - Link-worthy asset development plan
   - Resource page and tool creation
   - Industry relationship building content
   - Guest posting and collaboration opportunities

9. **Performance Tracking and Optimization**
   - Content performance metrics to monitor
   - Keyword ranking tracking priorities
   - User engagement and conversion optimization
   - Content gap analysis and iteration

10. **Content Calendar and Execution**
    - Editorial calendar with seasonal considerations
    - Content production workflow and responsibilities
    - Quality assurance and SEO optimization checklist
    - Publication and promotion strategy

This content strategy should provide a complete roadmap for SEO content creation, optimization, and ongoing improvement.""",

                'phase6': """# Phase 6: SEO Technical Foundation and Link Building Strategy

Building on the content strategy from Phase 5, I need you to develop the technical SEO foundation and authority building strategy for long-term organic growth.

## Strategic Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Website**: {{website}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}

## SEO Context:
We've established content strategy and keyword targeting. Now we need to build the technical foundation and authority signals that will support sustainable organic rankings and traffic growth.

## Technical SEO and Authority Strategy Required:

Please develop a comprehensive technical SEO and link building strategy:

1. **Technical SEO Foundation**
   - Site architecture and URL structure optimization
   - Page speed and Core Web Vitals improvement
   - Mobile-first optimization requirements
   - Crawlability and indexation strategy

2. **On-Page SEO Framework**
   - Title tag and meta description templates
   - Header structure and keyword optimization
   - Internal linking strategy and implementation
   - Schema markup priorities and setup

3. **Local SEO Technical Requirements**
   - Google Business Profile optimization
   - Local citation building and NAP consistency
   - Location page structure and optimization
   - Local schema markup implementation

4. **Link Building Strategy**
   - Domain authority building priorities
   - Industry-relevant link acquisition targets
   - Local link building opportunities
   - Content-driven link earning strategies

5. **Authority Building Plan**
   - Expertise, Authoritativeness, Trustworthiness (E-A-T) signals
   - Industry thought leadership development
   - Expert contributor and interview programs
   - Awards, certifications, and credibility signals

6. **Competitive Authority Analysis**
   - Competitor backlink profile analysis
   - Link gap opportunities identification
   - Authority site relationship building
   - Industry publication collaboration targets

7. **Content Distribution and Promotion**
   - Social media SEO integration
   - Industry forum and community engagement
   - Email marketing for content amplification
   - Influencer and expert outreach strategy

8. **Monitoring and Measurement**
   - Technical SEO audit schedule and tools
   - Link building progress tracking
   - Authority signal measurement
   - Competitive monitoring and alerts

9. **Risk Management and Guidelines**
   - Google algorithm update preparation
   - Link quality assessment and guidelines
   - Penalty prevention and recovery planning
   - White-hat SEO best practices enforcement

10. **Implementation Roadmap**
    - Technical SEO priority implementation
    - Link building campaign timeline
    - Authority building milestone targets
    - Long-term sustainability planning

This technical and authority strategy should provide the foundation for sustainable organic growth and competitive positioning in search results."""
            }

        # PPC + SEO INTEGRATED PHASE TEMPLATES (1-8)
        else:  # BOTH
            templates = {
                'phase1': """# Phase 1: Business Intelligence Analysis (Integrated PPC + SEO)

I need you to analyze this business and provide strategic insights for integrated digital marketing campaign development across both PPC and SEO channels.

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

Please provide a comprehensive business intelligence analysis for integrated PPC and SEO strategy:

1. **Market Position Assessment**
   - Industry landscape analysis
   - Business maturity and growth potential
   - Market opportunity size for both paid and organic channels

2. **Competitive Advantages**
   - Unique differentiators for both PPC messaging and content authority
   - Competitive moats that can be leveraged across channels
   - Value proposition strengths for ads and organic results

3. **Target Market Analysis**
   - Primary audience segments for integrated targeting
   - Secondary audience opportunities for channel expansion
   - Customer journey mapping across paid and organic touchpoints

4. **Integrated Channel Strategy Foundation**
   - Synergies between PPC and SEO efforts
   - Budget allocation recommendations across channels
   - Priority targeting strategies for maximum impact

5. **Growth Opportunities**
   - Cross-channel amplification opportunities
   - Service expansion possibilities through integrated marketing
   - Geographic expansion potential via both channels

6. **Risk Assessment**
   - Channel-specific challenges and mitigation strategies
   - Competitive threats across paid and organic search
   - Market risks affecting integrated performance

Please provide actionable insights that will inform our integrated PPC and SEO strategy development.""",

                'phase2': """# Phase 2: Competitive Landscape Analysis (Integrated PPC + SEO)

Based on the business intelligence from Phase 1, I need you to analyze the competitive landscape for both PPC and SEO strategy planning.

## Business Context (from Phase 1):
- **Business**: {{business_name}} - {{description}}
- **Industry**: {{industry}}
- **Location**: {{location}}
- **Services**: {{services}}
- **Unique Value**: {{unique_value}}

## Known Competitors:
{% for competitor in competitors %}
- {{competitor}}
{% endfor %}

## Target Audience:
{{target_audience}}

## Budget Range:
{{budget_range}}

## Campaign Objective:
{{primary_goal}}

## Competitive Analysis Required:

Please conduct a comprehensive competitive landscape analysis for integrated PPC and SEO:

1. **Cross-Channel Competitor Assessment**
   - Competitors' integrated digital marketing strategies
   - PPC vs SEO investment balance and effectiveness
   - Cross-channel messaging consistency and themes
   - Overall digital presence and authority

2. **PPC Competitive Analysis**
   - Estimated competitor ad spend and platform presence
   - Primary keywords they target in paid search
   - Ad messaging themes and value propositions
   - Landing page strategies and conversion approaches

3. **SEO Competitive Analysis**
   - Organic search visibility and keyword rankings
   - Content strategy themes and authority signals
   - Backlink profile strength and domain authority
   - Technical SEO implementation quality

4. **Integrated Opportunity Gaps**
   - Keywords underserved in both paid and organic
   - Audience segments not targeted across channels
   - Geographic markets with less integrated competition
   - Seasonal opportunities for coordinated campaigns

5. **Strategic Advantages for Integration**
   - Areas where {{business_name}} can outcompete across channels
   - Unique value propositions for integrated messaging
   - Local market advantages for both PPC and SEO
   - Service specializations for comprehensive targeting

6. **Channel Synergy Recommendations**
   - Best practices for PPC and SEO coordination
   - Data sharing opportunities between channels
   - Budget optimization across paid and organic
   - Performance amplification through integration

Focus on actionable insights that will help {{business_name}} compete effectively across both paid advertising and organic search.""",

                'phase3': """# Phase 3: Market Gap Analysis (Integrated PPC + SEO)

Building on the insights from Phases 1 and 2, I need you to identify specific market gaps and opportunities for integrated PPC and SEO strategy.

## Business Context:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Services**: {{services}}
- **Target Audience**: {{target_audience}}
- **Budget**: {{budget_range}}
- **Primary Goal**: {{primary_goal}}

## Previous Analysis Context:
We've completed business intelligence analysis and competitive landscape mapping. Now we need to identify specific market gaps where {{business_name}} can gain competitive advantage through coordinated PPC and SEO efforts.

## Market Gap Analysis Required:

Please provide a detailed analysis of market gaps and integrated opportunities:

1. **Cross-Channel Keyword Gaps**
   - High-value keywords underserved in both paid and organic
   - PPC testing opportunities for SEO keyword validation
   - SEO content gaps that could benefit from PPC support
   - Long-tail opportunities across both channels

2. **Audience Segment Gaps**
   - Demographics underserved across both channels
   - Customer journey stages needing integrated support
   - Geographic micro-markets for coordinated targeting
   - Seasonal audience patterns for synchronized campaigns

3. **Content and Messaging Gaps**
   - Value propositions not leveraged across channels
   - Content themes missing from both PPC and SEO
   - Trust signals and credibility factors underutilized
   - Local market advantages not maximized

4. **Platform and Format Integration Gaps**
   - Cross-platform opportunities for message reinforcement
   - Data sharing gaps between PPC and SEO efforts
   - Attribution and tracking integration opportunities
   - Performance optimization synergies

5. **Local Market Integration Advantages**
   - Geographic areas needing coordinated presence
   - Local events and trends for synchronized campaigns
   - Community connections for cross-channel authority
   - Regional preferences for integrated messaging

6. **Customer Journey Integration Gaps**
   - Awareness stage coordination opportunities
   - Consideration phase cross-channel support
   - Decision stage integrated conversion optimization
   - Post-conversion retention and expansion synergies

7. **Budget and Resource Optimization Gaps**
   - Budget allocation inefficiencies to address
   - Resource sharing opportunities between channels
   - Testing and learning integration possibilities
   - ROI maximization through channel coordination

For each gap identified, please suggest specific integrated strategies that leverage both PPC and SEO for maximum impact.""",

                'phase4': """# Phase 4: Strategic Positioning for Integrated PPC + SEO

Based on the comprehensive analysis from Phases 1-3, I need you to develop a strategic positioning framework for coordinated PPC and SEO success.

## Business Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Unique Value**: {{unique_value}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}
- **Budget Range**: {{budget_range}}

## Strategic Context:
We've analyzed the business intelligence, competitive landscape, and market gaps. Now we need to synthesize these insights into a unified strategic positioning that will drive coordinated PPC and SEO campaigns.

## Integrated Strategic Positioning Required:

Please develop a comprehensive framework for integrated PPC and SEO positioning:

1. **Unified Value Proposition**
   - Core message consistent across both channels
   - Channel-specific adaptations while maintaining consistency
   - Competitive differentiation for both paid and organic results
   - Brand authority signals reinforced across channels

2. **Integrated Audience Strategy**
   - Primary audience segments for coordinated targeting
   - Channel-specific audience customization approaches
   - Customer journey mapping across paid and organic touchpoints
   - Cross-channel attribution and behavior analysis

3. **Coordinated Keyword Strategy**
   - Shared keyword themes for maximum market coverage
   - PPC testing to inform SEO content priorities
   - SEO insights to optimize PPC targeting and bidding
   - Complementary keyword approaches to avoid cannibalization

4. **Cross-Channel Campaign Architecture**
   - Integrated campaign structure and organization
   - Data sharing and performance optimization workflows
   - Landing page strategy for both traffic sources
   - Conversion tracking and attribution coordination

5. **Competitive Positioning Across Channels**
   - Unified competitive differentiation messaging
   - Channel-specific competitive advantages
   - Market dominance strategy through integrated presence
   - Risk mitigation through diversified channel approach

6. **Budget and Resource Allocation Strategy**
   - Optimal budget split between PPC and SEO
   - Resource sharing and efficiency maximization
   - Performance-based budget reallocation framework
   - ROI optimization through integrated measurement

7. **Authority and Trust Building**
   - Coordinated brand authority development
   - Cross-channel trust signal reinforcement
   - Integrated content and advertising alignment
   - Long-term brand positioning sustainability

8. **Performance Integration Framework**
   - Unified success metrics and KPIs
   - Cross-channel performance attribution
   - Integrated reporting and optimization insights
   - Continuous improvement through channel synergies

This strategic positioning should serve as the foundation for all coordinated PPC and SEO campaign development and optimization decisions.""",

                'phase5': """# Phase 5: Integrated Content Strategy for PPC + SEO

Based on the strategic positioning developed in Phase 4, I need you to create a comprehensive content strategy that maximizes synergies between PPC campaigns and SEO efforts.

## Strategic Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}
- **Budget Range**: {{budget_range}}
- **Unique Value**: {{unique_value}}

## Integration Context:
We've established unified strategic positioning. Now we need to translate this into coordinated content that serves both PPC performance and SEO authority building while maximizing cross-channel synergies.

## Integrated Content Strategy Required:

Please develop a comprehensive content strategy for PPC and SEO coordination:

1. **Unified Message Architecture**
   - Core messaging themes consistent across channels
   - Channel-specific adaptations for format requirements
   - Brand voice and tone guidelines for all content
   - Value proposition reinforcement across touchpoints

2. **Cross-Channel Content Planning**
   - Content themes that serve both PPC landing pages and SEO
   - Blog content that supports PPC campaign messaging
   - Landing page content optimized for both conversion and SEO
   - Resource content that builds authority and generates leads

3. **Keyword-Content Integration**
   - PPC keyword testing to inform SEO content priorities
   - SEO keyword research to optimize PPC targeting
   - Content gap analysis across both channel needs
   - Long-tail content strategy supporting paid campaigns

4. **Performance-Driven Content Development**
   - PPC conversion data informing content creation
   - SEO engagement metrics guiding ad copy development
   - A/B testing insights shared between channels
   - User behavior analysis driving content optimization

5. **Landing Page and Conversion Optimization**
   - Integrated landing page strategy for both traffic sources
   - Conversion rate optimization benefiting both channels
   - Form optimization and lead capture coordination
   - Mobile experience optimization across touchpoints

6. **Authority Building Content for Ad Performance**
   - Trust signal content that improves PPC Quality Scores
   - Expert positioning content supporting ad credibility
   - Social proof and testimonial integration
   - Industry leadership content enhancing brand authority

7. **Content Distribution and Amplification**
   - SEO content promoted through PPC for maximum reach
   - Social media integration supporting both channels
   - Email marketing coordination with paid and organic strategies
   - Influencer content supporting integrated campaigns

8. **Seasonal and Campaign Content Coordination**
   - Integrated editorial calendar for both channels
   - Event and holiday content planning across PPC and SEO
   - Product launch content supporting integrated promotion
   - Crisis communication content for brand protection

9. **Local Content Integration**
   - Location-specific content serving both local SEO and geo-targeted ads
   - Community engagement content supporting local authority
   - Local event content for timely campaign coordination
   - Regional preference integration across channels

10. **Content Performance and Optimization**
    - Integrated analytics and reporting for content performance
    - Cross-channel content testing and optimization
    - Content refresh strategy benefiting both channels
    - ROI measurement and content investment prioritization

This integrated content strategy should maximize the effectiveness of both PPC campaigns and SEO efforts while creating powerful synergies between channels.""",

                'phase6': """# Phase 6: SEO Foundation and Technical Integration

Building on the integrated content strategy, I need you to develop the SEO technical foundation that will support coordinated PPC and SEO performance.

## Strategic Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Website**: {{website}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}

## Integration Context:
We need to build technical SEO foundations that not only support organic rankings but also enhance PPC campaign performance through improved site quality, user experience, and conversion optimization.

## Technical SEO Integration Strategy Required:

Please develop a comprehensive technical SEO strategy that supports both channels:

1. **Technical Foundation for Integrated Performance**
   - Site architecture supporting both SEO crawling and PPC user experience
   - Page speed optimization benefiting Quality Scores and rankings
   - Mobile-first optimization for both organic and paid traffic
   - Core Web Vitals improvement for universal performance enhancement

2. **Landing Page Technical Optimization**
   - Technical SEO principles applied to PPC landing pages
   - Schema markup for both organic results and ad extensions
   - Internal linking strategy supporting conversion funnels
   - URL structure optimization for both crawling and user experience

3. **Local SEO Technical Integration**
   - Google Business Profile optimization supporting local PPC targeting
   - Local schema markup enhancing both organic and paid visibility
   - NAP consistency across all digital touchpoints
   - Location page optimization for both SEO and geo-targeted ads

4. **Analytics and Tracking Integration**
   - Unified analytics setup for cross-channel attribution
   - Conversion tracking coordination between Google Ads and GA4
   - SEO performance metrics integration with PPC insights
   - Data sharing workflows for optimization opportunities

5. **Quality Signal Optimization**
   - E-A-T signal development supporting both authority and ad trust
   - Site security and trustworthiness for improved Quality Scores
   - User experience signals benefiting both channels
   - Brand consistency across all digital properties

6. **Content Management Integration**
   - CMS optimization for both SEO and PPC content management
   - Dynamic content capabilities for personalized experiences
   - A/B testing infrastructure supporting both channels
   - Content update workflows maintaining SEO and PPC alignment

7. **Performance Monitoring Integration**
   - Technical SEO monitoring affecting PPC performance
   - Site health alerts impacting both channels
   - Competitive monitoring across organic and paid search
   - Algorithm update preparation for sustained performance

8. **International and Multi-Location Technical Setup**
   - Hreflang implementation for multi-location PPC campaigns
   - Geographic targeting technical requirements
   - Currency and language optimization for both channels
   - Regional site performance optimization

9. **Security and Compliance Integration**
   - SSL and security implementations affecting both channels
   - Privacy and compliance requirements for integrated tracking
   - Data protection measures maintaining performance
   - Accessibility improvements benefiting all users

10. **Scalability and Growth Technical Framework**
    - Technical infrastructure supporting growth across both channels
    - Automation opportunities for efficiency gains
    - Integration capabilities with marketing tools and platforms
    - Future-proofing technical decisions for sustained competitive advantage

This technical foundation should support superior performance in both SEO rankings and PPC campaign effectiveness while creating operational efficiencies.""",

                'phase7': """# Phase 7: Advanced SEO Content Strategy and Link Building

Building on the technical foundation, I need you to develop an advanced SEO content strategy and authority building plan that complements and amplifies the integrated PPC efforts.

## Strategic Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}
- **Budget Range**: {{budget_range}}

## Integration Context:
We need to build content authority and link equity that enhances both organic rankings and PPC performance through improved Quality Scores, brand trust, and conversion rates.

## Advanced SEO Content and Authority Strategy Required:

Please develop a comprehensive advanced SEO strategy that amplifies integrated campaign performance:

1. **Authority Content Architecture**
   - Expert-level content establishing industry thought leadership
   - Comprehensive resource development for link attraction
   - Original research and data content for competitive advantage
   - Authoritative guides supporting both SEO and PPC credibility

2. **Strategic Link Building Integration**
   - Link building campaigns that enhance brand authority for ads
   - Resource link acquisition supporting conversion trust signals
   - Industry relationship building benefiting both channels
   - Local link building enhancing geo-targeted campaign credibility

3. **Content Cluster Development**
   - Topic cluster organization for comprehensive coverage
   - Pillar content supporting both organic rankings and ad landing pages
   - Internal linking strategy maximizing SEO value and user experience
   - Content depth demonstrating expertise for improved Quality Scores

4. **Advanced Keyword Strategy**
   - Long-tail content strategy capturing additional search volume
   - Question-based content for featured snippet opportunities
   - Voice search optimization for emerging search behaviors
   - Semantic keyword integration for comprehensive topic coverage

5. **Multi-Format Content Integration**
   - Video content strategy supporting both SEO and display advertising
   - Infographic development for link building and social sharing
   - Podcast content for authority building and audience expansion
   - Interactive content enhancing engagement and conversion rates

6. **Local Authority and Community Engagement**
   - Local content strategy establishing geographic authority
   - Community involvement content supporting local business credibility
   - Event content and sponsorship visibility enhancement
   - Regional expertise demonstration for local market dominance

7. **Content Performance Amplification**
   - High-performing SEO content promotion through PPC
   - Social proof and testimonial integration across channels
   - User-generated content strategy for authentic authority building
   - Case study development showcasing integrated campaign success

8. **Competitive Content Strategy**
   - Content gap analysis revealing competitor weaknesses
   - Superior content development for competitive displacement
   - Unique angle development for differentiated positioning
   - Response content strategy for reputation management

9. **Seasonal and Trending Content Integration**
   - Timely content creation for trending topic authority
   - Seasonal content calendar coordinated with PPC campaigns
   - Industry event content for thought leadership positioning
   - News-jacking opportunities for increased visibility

10. **Advanced Link Building Strategies**
    - Digital PR campaigns generating high-authority links
    - Resource page link building for relevant industry sites
    - Broken link building providing value to linking sites
    - Collaborative content creation with industry partners

11. **Content Distribution and Syndication**
    - Guest posting strategy for authority site visibility
    - Industry publication relationship development
    - Content syndication for increased reach and authority
    - Influencer collaboration for content amplification

12. **Authority Measurement and Optimization**
    - Domain authority tracking and improvement strategies
    - Brand mention monitoring and optimization
    - Citation building for local authority enhancement
    - Trust signal development across all digital properties

This advanced SEO strategy should establish market-leading authority while providing substantial support for integrated PPC campaign performance and overall digital marketing effectiveness.""",

                'phase8': """# Phase 8: Link Building and Authority Strategy for Integrated Success

Completing our integrated strategy, I need you to develop a comprehensive link building and authority strategy that maximizes the synergistic effects between SEO authority building and PPC campaign performance.

## Strategic Foundation:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Target Audience**: {{target_audience}}
- **Primary Goal**: {{primary_goal}}
- **Integration Goals**: Enhanced PPC Quality Scores, improved conversion trust, and market-leading organic authority

## Integration Context:
This final phase focuses on building domain authority and industry recognition that creates a compound effect: stronger SEO rankings, improved PPC Quality Scores, higher conversion rates, and enhanced brand credibility across all marketing channels.

## Comprehensive Authority and Link Building Strategy Required:

Please develop an integrated authority building strategy that amplifies both SEO and PPC performance:

1. **Strategic Authority Building Framework**
   - Industry thought leadership positioning benefiting both channels
   - Expert recognition development for enhanced credibility in ads
   - Award and certification pursuit for trust signal amplification
   - Speaking and conference opportunities for authority demonstration

2. **High-Impact Link Building Campaigns**
   - Tier 1 publication relationship development and content placement
   - Industry association participation and link acquisition
   - Resource link building from authoritative industry sites
   - Collaborative content creation with recognized industry leaders

3. **Digital PR and Brand Awareness Integration**
   - Newsworthy story development and media outreach
   - Press release distribution for both link building and PPC credibility
   - Crisis communication planning protecting both organic and paid performance
   - Brand mention acquisition and optimization across all channels

4. **Local Authority and Community Leadership**
   - Chamber of Commerce and business organization participation
   - Local media relationship development and coverage acquisition
   - Community event sponsorship and involvement documentation
   - Local expert positioning for enhanced geographic targeting effectiveness

5. **Content-Driven Link Acquisition**
   - Original research and survey development for natural link attraction
   - Industry report creation establishing thought leadership
   - Tool and calculator development providing ongoing value
   - Comprehensive guide creation for authoritative resource positioning

6. **Strategic Partnership and Collaboration**
   - Industry partnership development for mutual link building
   - Supplier and vendor relationship leveraging for link acquisition
   - Customer success story development for social proof and links
   - Cross-industry collaboration for expanded authority building

7. **Advanced Link Building Tactics**
   - Broken link building with superior replacement content
   - Resource page inclusion through relationship building
   - Scholarship and grant programs for educational link acquisition
   - Industry conference and event link building opportunities

8. **Authority Signal Optimization**
   - Google Business Profile optimization for comprehensive local authority
   - Social media authority building supporting overall brand credibility
   - Review and testimonial acquisition for trust signal enhancement
   - Industry certification and accreditation pursuit and promotion

9. **Competitive Authority Analysis and Strategy**
   - Competitor backlink analysis and gap identification
   - Superior link target identification and acquisition planning
   - Industry influencer relationship mapping and engagement strategy
   - Market positioning for authority-based competitive advantage

10. **Link Building Performance and Risk Management**
    - Link quality assessment and maintenance protocols
    - Google algorithm compliance and penalty prevention
    - Link building ROI measurement and optimization
    - Disavow file management and toxic link monitoring

11. **Cross-Channel Authority Amplification**
    - SEO authority leveraging for improved PPC Quality Scores
    - Social proof integration across landing pages and ad extensions
    - Trust signal implementation in both organic results and ads
    - Brand credibility measurement and continuous improvement

12. **Long-Term Authority Sustainability**
    - Ongoing relationship maintenance and nurturing strategies
    - Authority building process documentation and systematization
    - Team training and capability development for sustained growth
    - Industry trend monitoring and strategy adaptation planning

13. **Authority Measurement and Reporting**
    - Domain authority tracking and competitive benchmarking
    - Brand mention monitoring and sentiment analysis
    - Link equity distribution and optimization across site
    - Integrated performance reporting showing cross-channel benefits

14. **Strategic Implementation Roadmap**
    - Priority authority building activities for immediate impact
    - Medium-term link building campaign planning and execution
    - Long-term industry positioning and thought leadership development
    - Integration checkpoints ensuring PPC and SEO synergy maximization

This comprehensive authority strategy should establish {{business_name}} as the recognized industry leader while creating powerful synergies that enhance both SEO rankings and PPC campaign performance, resulting in superior ROI and sustainable competitive advantage."""
            }

        self.print_info(f"Creating {len(templates)} customized prompts...")
        
        # Generate prompts using templates
        for phase, template in templates.items():
            try:
                jinja_template = Template(template)
                rendered_prompt = jinja_template.render(**self.business_data)
                self.generated_prompts[phase] = rendered_prompt
                self.print_success(f"✓ Generated {phase} prompt")
            except Exception as e:
                self.print_warning(f"Error generating {phase}: {str(e)}")
        
        phase_count = len(self.generated_prompts)
        client_type_display = {
            'PPC_ONLY': 'PPC-focused',
            'SEO_ONLY': 'SEO-focused', 
            'BOTH': 'integrated PPC + SEO'
        }.get(client_type, 'integrated')
        
        self.print_success(f"Generated {phase_count} {client_type_display} Claude prompts!")
        return self.generated_prompts

    def create_research_project(self):
        """Create complete research project structure"""
        self.print_header("📁 Creating Research Project Structure")
        
        # Create project context file
        client_type = self.business_data.get('client_type', 'BOTH')
        client_type_display = {
            'PPC_ONLY': 'PPC Only',
            'SEO_ONLY': 'SEO Only',
            'BOTH': 'PPC + SEO Integrated'
        }.get(client_type, 'PPC + SEO Integrated')
        
        phase_count = len(self.generated_prompts)
        
        if client_type == 'PPC_ONLY':
            phases_description = f"{phase_count} (PPC-focused research)"
            files_section = """## Files Generated
### PPC Research Phases (1-5)
- Phase 1 Prompt: phase1_business_intelligence_prompt.md
- Phase 2 Prompt: phase2_competitive_landscape_prompt.md
- Phase 3 Prompt: phase3_market_gaps_prompt.md
- Phase 4 Prompt: phase4_strategic_positioning_prompt.md
- Phase 5 Prompt: phase5_content_strategy_prompt.md"""
        elif client_type == 'SEO_ONLY':
            phases_description = f"{phase_count} (SEO-focused research)"
            files_section = """## Files Generated
### SEO Research Phases (1-6)
- Phase 1 Prompt: phase1_business_intelligence_prompt.md
- Phase 2 Prompt: phase2_competitive_landscape_prompt.md
- Phase 3 Prompt: phase3_market_gaps_prompt.md
- Phase 4 Prompt: phase4_strategic_positioning_prompt.md
- Phase 5 Prompt: phase5_seo_content_strategy_prompt.md
- Phase 6 Prompt: phase6_seo_authority_strategy_prompt.md"""
        else:
            phases_description = f"{phase_count} (PPC + SEO integrated)"
            files_section = """## Files Generated
### PPC Research Phases (1-5)
- Phase 1 Prompt: phase1_business_intelligence_prompt.md
- Phase 2 Prompt: phase2_competitive_landscape_prompt.md
- Phase 3 Prompt: phase3_market_gaps_prompt.md
- Phase 4 Prompt: phase4_strategic_positioning_prompt.md
- Phase 5 Prompt: phase5_content_strategy_prompt.md

### SEO Research Phases (6-8)
- Phase 6 Prompt: phase6_seo_foundation_prompt.md
- Phase 7 Prompt: phase7_seo_content_strategy_prompt.md
- Phase 8 Prompt: phase8_seo_authority_strategy_prompt.md"""
        
        project_context = f"""# {self.business_data['business_name']} - Claude Research Project

## Project Overview
- **Client**: {self.business_data['business_name']}
- **Industry**: {self.business_data['industry']}
- **Client Type**: {client_type_display}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Research Phases**: {phases_description}

## Business Context
{self.business_data['description']}

## Services
{self.business_data['services']}

## Target Audience
{self.business_data['target_audience']}

## Campaign Objectives
- **Primary Goal**: {self.business_data['primary_goal']}
- **Budget Range**: {self.business_data['budget_range']}
- **Success Metrics**: {self.business_data['success_metrics']}

## Competitors
{chr(10).join(f"- {comp}" for comp in self.business_data['competitors'])}

## Next Steps
1. Execute Phase 1 prompt in Claude
2. Save Claude's response in phase_outputs/phase1_business_intelligence.md
3. Continue through all {phase_count} phases sequentially
4. Compile strategic insights for {client_type_display.lower()}

{files_section}
"""

        # Save project context
        context_path = f"{self.folder_name}/02_market_research/claude_research/00_project_context.md"
        with open(context_path, 'w', encoding='utf-8') as f:
            f.write(project_context)

        # Save individual prompt files based on what was generated
        prompt_files = {
            'phase1': 'phase1_business_intelligence_prompt.md',
            'phase2': 'phase2_competitive_landscape_prompt.md',
            'phase3': 'phase3_market_gaps_prompt.md',
            'phase4': 'phase4_strategic_positioning_prompt.md',
            'phase5': 'phase5_content_strategy_prompt.md',
            'phase6': 'phase6_seo_foundation_prompt.md',
            'phase7': 'phase7_seo_content_strategy_prompt.md',
            'phase8': 'phase8_seo_authority_strategy_prompt.md'
        }

        for phase, filename in prompt_files.items():
            if phase in self.generated_prompts:
                file_path = f"{self.folder_name}/02_market_research/claude_research/{filename}"
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.generated_prompts[phase])

        # Create workflow instructions based on client type
        client_type = self.business_data.get('client_type', 'BOTH')
        phase_count = len(self.generated_prompts)
        
        if client_type == 'PPC_ONLY':
            workflow_instructions = f"""# Claude Research Workflow Instructions - PPC Focus

## How to Execute This Research

### Step 1: Prepare Claude
1. Open Claude AI (claude.ai)
2. Start a new conversation
3. Keep this conversation open for all {phase_count} phases

### Step 2: Execute PPC Research Phases (1-5)
1. Copy the entire content from `phase1_business_intelligence_prompt.md`
2. Paste it into Claude
3. Wait for Claude's comprehensive response
4. Copy Claude's response and save it as `phase_outputs/phase1_business_intelligence.md`

### Step 3: Continue PPC Phases 2-5
1. Copy the entire content from `phase2_competitive_landscape_prompt.md`
2. Paste it into the same Claude conversation
3. Wait for Claude's response
4. Save the response as `phase_outputs/phase2_competitive_landscape.md`
5. Continue this process for phases 3, 4, and 5

### Step 4: Compile Strategic Insights
1. Review all phase outputs
2. Create a master strategic document
3. Identify key insights and action items
4. Develop PPC campaign implementation roadmap

## Expected Outputs
### PPC Research Phases (1-5)
- Phase 1: Business intelligence and market position analysis
- Phase 2: Competitive landscape mapping and positioning gaps
- Phase 3: Market opportunities and gap identification
- Phase 4: Strategic positioning and differentiation strategy
- Phase 5: Content strategy and PPC campaign implementation plan

## Tips for Best Results
- Execute phases in order
- Don't skip any phases
- Keep the Claude conversation continuous
- Review and validate insights against real market data
- Use insights to inform PPC campaign strategy
- Focus on paid advertising opportunities and optimization

## Estimated Time
- Phase execution: 45-60 minutes ({phase_count} phases)
- Review and compilation: 60-90 minutes
- Total research time: 2-3 hours
"""
        elif client_type == 'SEO_ONLY':
            workflow_instructions = f"""# Claude Research Workflow Instructions - SEO Focus

## How to Execute This Research

### Step 1: Prepare Claude
1. Open Claude AI (claude.ai)
2. Start a new conversation
3. Keep this conversation open for all {phase_count} phases

### Step 2: Execute SEO Research Phases (1-6)
1. Copy the entire content from `phase1_business_intelligence_prompt.md`
2. Paste it into Claude
3. Wait for Claude's comprehensive response
4. Copy Claude's response and save it as `phase_outputs/phase1_business_intelligence.md`

### Step 3: Continue SEO Phases 2-6
1. Copy the entire content from `phase2_competitive_landscape_prompt.md`
2. Paste it into the same Claude conversation
3. Wait for Claude's response
4. Save the response as `phase_outputs/phase2_competitive_landscape.md`
5. Continue this process for phases 3, 4, 5, and 6

### Step 4: Compile Strategic Insights
1. Review all phase outputs
2. Create a master strategic document
3. Identify key insights and action items
4. Develop SEO implementation roadmap

## Expected Outputs
### SEO Research Phases (1-6)
- Phase 1: Business intelligence and market position analysis
- Phase 2: Competitive landscape mapping and positioning gaps
- Phase 3: Market opportunities and gap identification
- Phase 4: Strategic positioning and differentiation strategy
- Phase 5: SEO content strategy and keyword research
- Phase 6: Link building and authority strategy

## Tips for Best Results
- Execute phases in order
- Don't skip any phases
- Keep the Claude conversation continuous
- Review and validate insights against real market data
- Use insights to inform SEO strategy
- Focus on organic search opportunities and long-term growth

## Estimated Time
- Phase execution: 50-70 minutes ({phase_count} phases)
- Review and compilation: 90-120 minutes
- Total research time: 2.5-3.5 hours
"""
        else:  # BOTH
            workflow_instructions = f"""# Claude Research Workflow Instructions - Integrated PPC + SEO

## How to Execute This Research

### Step 1: Prepare Claude
1. Open Claude AI (claude.ai)
2. Start a new conversation
3. Keep this conversation open for all {phase_count} phases

### Step 2: Execute Foundation Research Phases (1-4)
1. Copy the entire content from `phase1_business_intelligence_prompt.md`
2. Paste it into Claude
3. Wait for Claude's comprehensive response
4. Copy Claude's response and save it as `phase_outputs/phase1_business_intelligence.md`

### Step 3: Continue Foundation Phases 2-4
1. Copy the entire content from `phase2_competitive_landscape_prompt.md`
2. Paste it into the same Claude conversation
3. Wait for Claude's response
4. Save the response as `phase_outputs/phase2_competitive_landscape.md`
5. Continue this process for phases 3 and 4

### Step 4: Execute PPC Phase (5)
1. Copy the entire content from `phase5_content_strategy_prompt.md`
2. Paste it into the same Claude conversation
3. Wait for Claude's response
4. Save the response as `phase_outputs/phase5_content_strategy.md`

### Step 5: Execute SEO Phases (6-8)
1. Copy the entire content from `phase6_seo_foundation_prompt.md`
2. Paste it into the same Claude conversation
3. Wait for Claude's response
4. Save the response as `phase_outputs/phase6_seo_foundation.md`
5. Continue this process for phases 7 and 8

### Step 6: Compile Strategic Insights
1. Review all phase outputs
2. Create a master strategic document
3. Identify key insights and action items
4. Develop integrated PPC + SEO implementation roadmap

## Expected Outputs
### Foundation Research Phases (1-4)
- Phase 1: Business intelligence and market position analysis
- Phase 2: Competitive landscape mapping and positioning gaps
- Phase 3: Market opportunities and gap identification
- Phase 4: Strategic positioning and differentiation strategy

### PPC Research Phase (5)
- Phase 5: Content strategy and PPC campaign implementation plan

### SEO Research Phases (6-8)
- Phase 6: SEO foundation and technical analysis
- Phase 7: SEO content strategy and keyword research
- Phase 8: Link building and authority strategy

## Tips for Best Results
- Execute phases in order
- Don't skip any phases
- Keep the Claude conversation continuous
- Review and validate insights against real market data
- Use insights to inform both PPC and SEO strategies
- Look for synergies between PPC and SEO opportunities
- Focus on integrated campaign approach

## Estimated Time
- Phase execution: 60-90 minutes ({phase_count} phases)
- Review and compilation: 90-120 minutes
- Total research time: 3-4 hours
"""

        workflow_path = f"{self.folder_name}/02_market_research/claude_research/claude_research_workflow.md"
        with open(workflow_path, 'w', encoding='utf-8') as f:
            f.write(workflow_instructions)

        # Create template files for outputs based on generated phases
        all_template_files = {
            'phase1': 'phase_outputs/phase1_business_intelligence.md',
            'phase2': 'phase_outputs/phase2_competitive_landscape.md',
            'phase3': 'phase_outputs/phase3_market_gaps.md',
            'phase4': 'phase_outputs/phase4_strategic_positioning.md',
            'phase5': 'phase_outputs/phase5_content_strategy.md',
            'phase6': 'phase_outputs/phase6_seo_foundation.md',
            'phase7': 'phase_outputs/phase7_seo_content_strategy.md',
            'phase8': 'phase_outputs/phase8_seo_authority_strategy.md'
        }

        # Only create template files for phases that were generated
        template_files = []
        for phase in self.generated_prompts.keys():
            if phase in all_template_files:
                template_files.append(all_template_files[phase])
        
        # Always create strategic insights file
        template_files.append('strategic_insights.md')

        for template_file in template_files:
            file_path = f"{self.folder_name}/02_market_research/claude_research/{template_file}"
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    filename_clean = os.path.basename(template_file).replace('_', ' ').replace('.md', '').title()
                    f.write(f"# {filename_clean}\n\n*Paste Claude's response here*\n\n## Instructions\n\n1. Copy the prompt from the corresponding prompt file\n2. Paste it into Claude AI (claude.ai)\n3. Copy Claude's complete response\n4. Paste the response here, replacing this placeholder text\n\n## Timestamp\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        self.print_success("Research project structure created!")
        return True

    def export_for_claude(self):
        """Create final export with instructions"""
        self.print_header("📤 Creating Claude Export Package")
        
        # Create summary file based on client type
        client_type = self.business_data.get('client_type', 'BOTH')
        client_type_display = {
            'PPC_ONLY': 'PPC Only',
            'SEO_ONLY': 'SEO Only',
            'BOTH': 'PPC + SEO Integrated'
        }.get(client_type, 'PPC + SEO Integrated')
        
        phase_count = len(self.generated_prompts)
        
        if client_type == 'PPC_ONLY':
            phases_section = """#### PPC Research Phases (1-5)
1. **Phase 1**: Business Intelligence Analysis
   - File: `phase1_business_intelligence_prompt.md`
   - Save response as: `phase_outputs/phase1_business_intelligence.md`

2. **Phase 2**: Competitive Landscape Mapping
   - File: `phase2_competitive_landscape_prompt.md`
   - Save response as: `phase_outputs/phase2_competitive_landscape.md`

3. **Phase 3**: Market Gap Identification
   - File: `phase3_market_gaps_prompt.md`
   - Save response as: `phase_outputs/phase3_market_gaps.md`

4. **Phase 4**: Strategic Positioning Development
   - File: `phase4_strategic_positioning_prompt.md`
   - Save response as: `phase_outputs/phase4_strategic_positioning.md`

5. **Phase 5**: Content & Campaign Strategy (PPC)
   - File: `phase5_content_strategy_prompt.md`
   - Save response as: `phase_outputs/phase5_content_strategy.md`"""
            
            expected_outcomes = """- Market position analysis
- Competitive landscape mapping
- Market opportunity identification
- Strategic positioning strategy
- PPC campaign implementation plan"""
            
            time_estimate = "**Total research time**: 2-3 hours"
            value_estimate = "**Implementation value**: Professional-grade strategic intelligence typically requiring 15-20 hours of manual research"
            
        elif client_type == 'SEO_ONLY':
            phases_section = """#### SEO Research Phases (1-6)
1. **Phase 1**: Business Intelligence Analysis
   - File: `phase1_business_intelligence_prompt.md`
   - Save response as: `phase_outputs/phase1_business_intelligence.md`

2. **Phase 2**: Competitive Landscape Mapping
   - File: `phase2_competitive_landscape_prompt.md`
   - Save response as: `phase_outputs/phase2_competitive_landscape.md`

3. **Phase 3**: Market Gap Identification
   - File: `phase3_market_gaps_prompt.md`
   - Save response as: `phase_outputs/phase3_market_gaps.md`

4. **Phase 4**: Strategic Positioning Development
   - File: `phase4_strategic_positioning_prompt.md`
   - Save response as: `phase_outputs/phase4_strategic_positioning.md`

5. **Phase 5**: SEO Content Strategy & Keyword Research
   - File: `phase5_seo_content_strategy_prompt.md`
   - Save response as: `phase_outputs/phase5_seo_content_strategy.md`

6. **Phase 6**: Link Building & Authority Strategy
   - File: `phase6_seo_authority_strategy_prompt.md`
   - Save response as: `phase_outputs/phase6_seo_authority_strategy.md`"""
            
            expected_outcomes = """- Market position analysis
- Competitive landscape mapping
- Market opportunity identification
- Strategic positioning strategy
- SEO content strategy and keyword research
- Link building and authority strategy"""
            
            time_estimate = "**Total research time**: 2.5-3.5 hours"
            value_estimate = "**Implementation value**: Professional-grade strategic intelligence typically requiring 18-23 hours of manual research"
            
        else:  # BOTH
            phases_section = """#### Foundation Research Phases (1-4)
1. **Phase 1**: Business Intelligence Analysis
   - File: `phase1_business_intelligence_prompt.md`
   - Save response as: `phase_outputs/phase1_business_intelligence.md`

2. **Phase 2**: Competitive Landscape Mapping
   - File: `phase2_competitive_landscape_prompt.md`
   - Save response as: `phase_outputs/phase2_competitive_landscape.md`

3. **Phase 3**: Market Gap Identification
   - File: `phase3_market_gaps_prompt.md`
   - Save response as: `phase_outputs/phase3_market_gaps.md`

4. **Phase 4**: Strategic Positioning Development
   - File: `phase4_strategic_positioning_prompt.md`
   - Save response as: `phase_outputs/phase4_strategic_positioning.md`

#### PPC Research Phase (5)
5. **Phase 5**: Content & Campaign Strategy (PPC)
   - File: `phase5_content_strategy_prompt.md`
   - Save response as: `phase_outputs/phase5_content_strategy.md`

#### SEO Research Phases (6-8)
6. **Phase 6**: SEO Foundation & Technical Analysis
   - File: `phase6_seo_foundation_prompt.md`
   - Save response as: `phase_outputs/phase6_seo_foundation.md`

7. **Phase 7**: SEO Content Strategy & Keyword Research
   - File: `phase7_seo_content_strategy_prompt.md`
   - Save response as: `phase_outputs/phase7_seo_content_strategy.md`

8. **Phase 8**: Link Building & Authority Strategy
   - File: `phase8_seo_authority_strategy_prompt.md`
   - Save response as: `phase_outputs/phase8_seo_authority_strategy.md`"""
            
            expected_outcomes = """- Market position analysis
- Competitive landscape mapping
- Market opportunity identification
- Strategic positioning strategy
- PPC campaign implementation plan
- SEO foundation and technical strategy
- Content marketing and keyword strategy
- Link building and authority strategy"""
            
            time_estimate = "**Total research time**: 3-4 hours"
            value_estimate = "**Implementation value**: Professional-grade strategic intelligence typically requiring 20-25 hours of manual research"
        
        summary_content = f"""# {self.business_data['business_name']} - Claude Research Summary

## Quick Start Guide

### 1. Open Claude AI
- Go to claude.ai
- Start a new conversation
- Keep this conversation open for all {phase_count} phases

### 2. Execute Research Phases
Execute these prompts in order:

{phases_section}

### 3. Compile Results
After completing all phases, review the outputs and create your strategic insights document.

## Business Context Summary
- **Business**: {self.business_data['business_name']}
- **Industry**: {self.business_data['industry']}
- **Client Type**: {client_type_display}
- **Primary Goal**: {self.business_data['primary_goal']}
- **Budget**: {self.business_data['budget_range']}
- **Target Audience**: {self.business_data['target_audience']}

## Generated Files
- Project context and overview
- {phase_count} customized Claude prompts
- Workflow instructions
- Output templates
- Strategic insights framework

## Expected Outcome
Comprehensive strategic intelligence for {client_type_display.lower()} campaigns, including:
{expected_outcomes}

{time_estimate}
{value_estimate}
"""

        summary_path = f"{self.folder_name}/02_market_research/claude_research/CLAUDE_RESEARCH_SUMMARY.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        # Save business data as JSON for future reference
        data_path = f"{self.folder_name}/02_market_research/claude_research/business_data.json"
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(self.business_data, f, indent=2)

        self.print_success("Claude export package created!")
        return True

    def run_setup(self):
        """Run the complete setup process"""
        try:
            # Step 1: Collect business intelligence
            self.collect_business_intelligence()
            
            # Step 2: Generate Claude prompts
            self.generate_claude_prompts()
            
            # Step 3: Create research project
            self.create_research_project()
            
            # Step 4: Export for Claude
            self.export_for_claude()
            
            # Final summary
            self.print_header("✅ Setup Complete!")
            
            client_type = self.business_data.get('client_type', 'BOTH')
            phase_count = len(self.generated_prompts)
            
            if self.console:
                table = Table(title="Generated Files")
                table.add_column("File", style="cyan")
                table.add_column("Purpose", style="green")
                
                table.add_row("00_project_context.md", "Project overview and context")
                
                # Add rows for generated phases only
                file_descriptions = {
                    'phase1': "Phase 1 Claude prompt (Foundation)",
                    'phase2': "Phase 2 Claude prompt (Foundation)",
                    'phase3': "Phase 3 Claude prompt (Foundation)",
                    'phase4': "Phase 4 Claude prompt (Foundation)",
                    'phase5': "Phase 5 Claude prompt (PPC)",
                    'phase6': "Phase 6 Claude prompt (SEO)",
                    'phase7': "Phase 7 Claude prompt (SEO)",
                    'phase8': "Phase 8 Claude prompt (SEO)"
                }
                
                for phase in self.generated_prompts.keys():
                    if phase in file_descriptions:
                        filename = f"{phase}_*.md"
                        table.add_row(filename, file_descriptions[phase])
                
                table.add_row("claude_research_workflow.md", "Step-by-step instructions")
                table.add_row("CLAUDE_RESEARCH_SUMMARY.md", "Quick start guide")
                
                self.console.print(table)
            else:
                print("\n📋 Generated Files:")
                print("  - 00_project_context.md (Project overview)")
                
                # Print generated phases only
                file_descriptions = {
                    'phase1': "Foundation",
                    'phase2': "Foundation",
                    'phase3': "Foundation",
                    'phase4': "Foundation",
                    'phase5': "PPC",
                    'phase6': "SEO",
                    'phase7': "SEO",
                    'phase8': "SEO"
                }
                
                for phase in sorted(self.generated_prompts.keys()):
                    if phase in file_descriptions:
                        phase_num = phase.replace('phase', '')
                        category = file_descriptions[phase]
                        print(f"  - {phase}_*_prompt.md ({category})")
                
                print("  - claude_research_workflow.md (Instructions)")
                print("  - CLAUDE_RESEARCH_SUMMARY.md (Quick start)")

            print(f"\n📁 Location: {self.folder_name}/02_market_research/claude_research/")
            print(f"📖 Start with: CLAUDE_RESEARCH_SUMMARY.md")
            print(f"🚀 Next: Execute Phase 1 prompt in Claude AI")
            
            return True
            
        except Exception as e:
            self.print_warning(f"Setup failed: {str(e)}")
            return False

@click.command()
@click.argument('client_name')
def main(client_name):
    """
    Claude AI Research Setup Script
    
    Replaces manual competitor research with AI-powered strategic intelligence.
    
    Usage: python3 claude_research_setup.py "Client Name"
    """
    
    if not client_name:
        print("❌ Client name is required")
        print("Usage: python3 claude_research_setup.py 'Client Name'")
        sys.exit(1)
    
    # Create and run setup
    setup = ClaudeResearchSetup(client_name)
    success = setup.run_setup()
    
    if success:
        print(f"\n🎯 Claude Research Setup completed successfully!")
        print(f"📧 Ready for strategic intelligence gathering with Claude AI")
    else:
        print(f"\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()