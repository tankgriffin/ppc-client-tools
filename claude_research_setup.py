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
        """Generate customized Claude prompts for 5-phase research"""
        self.print_header("🧠 Generating Claude Prompts")
        
        # Phase 1: Business Intelligence Analysis
        phase1_template = """
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
   - Industry landscape analysis
   - Business maturity and growth potential
   - Market opportunity size

2. **Competitive Advantages**
   - Unique differentiators
   - Competitive moats
   - Value proposition strengths

3. **Target Market Analysis**
   - Primary audience segments
   - Secondary audience opportunities
   - Customer journey mapping

4. **PPC Campaign Strategy Foundation**
   - Recommended campaign types
   - Budget allocation suggestions
   - Priority targeting strategies

5. **Growth Opportunities**
   - Untapped market segments
   - Service expansion possibilities
   - Geographic expansion potential

6. **Risk Assessment**
   - Potential challenges
   - Competitive threats
   - Market risks

Please provide actionable insights that will inform our PPC strategy development.
"""

        # Phase 2: Competitive Landscape Mapping
        phase2_template = """
# Phase 2: Competitive Landscape Mapping

Based on the business intelligence from Phase 1, I need you to analyze the competitive landscape for PPC campaign planning.

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

## Competitive Analysis Required:

Please provide a comprehensive competitive landscape analysis including:

1. **Direct Competitor Identification**
   - Who are the main direct competitors?
   - What are their primary service offerings?
   - How do they position themselves in the market?

2. **Indirect Competitor Analysis**
   - Who are the indirect competitors?
   - What adjacent services compete for the same customers?
   - What alternative solutions do customers consider?

3. **Competitive Positioning Map**
   - How do competitors position themselves on price vs. quality?
   - What are the main positioning themes in the market?
   - Where are the positioning gaps?

4. **Competitor PPC Strategy Analysis**
   - What keywords are competitors likely targeting?
   - What ad messaging themes do they probably use?
   - What are their likely campaign objectives?

5. **Competitive Advantages Analysis**
   - What advantages do competitors have?
   - What are their weaknesses?
   - How can our client differentiate?

6. **Market Share Estimation**
   - Who are the market leaders?
   - What's the competitive intensity?
   - Where are the growth opportunities?

7. **Competitive Threat Assessment**
   - Which competitors pose the biggest threat?
   - What competitive responses should we expect?
   - How can we defend against competitive attacks?

Please provide specific, actionable insights for PPC campaign development.
"""

        # Phase 3: Market Gap Identification
        phase3_template = """
# Phase 3: Market Gap Identification

Building on the business intelligence and competitive analysis, I need you to identify specific market gaps and opportunities.

## Business Context:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Services**: {{services}}
- **Target Audience**: {{target_audience}}
- **Unique Value**: {{unique_value}}
- **Primary Goal**: {{primary_goal}}

## Market Gap Analysis Required:

Please identify and analyze market gaps and opportunities including:

1. **Service Gaps**
   - What services are underserved in the market?
   - What customer needs are not being met?
   - What service combinations are missing?

2. **Geographic Gaps**
   - What geographic areas are underserved?
   - Where are competitors weak or absent?
   - What location-based opportunities exist?

3. **Audience Gaps**
   - What customer segments are underserved?
   - What demographics are competitors missing?
   - What psychographic groups are overlooked?

4. **Messaging Gaps**
   - What messages are competitors not using?
   - What emotional triggers are being missed?
   - What value propositions are unexplored?

5. **Channel Gaps**
   - What marketing channels are underutilized?
   - What platforms are competitors not using effectively?
   - What touchpoints are being missed?

6. **Timing Gaps**
   - What seasonal opportunities are missed?
   - What time-based targeting is underutilized?
   - What event-driven opportunities exist?

7. **Price Point Gaps**
   - What price points are underserved?
   - What value tiers are missing?
   - What pricing strategies are unexplored?

8. **Technology Gaps**
   - What technological advantages can we leverage?
   - What automation opportunities exist?
   - What digital experiences are missing?

For each gap identified, please provide:
- Specific opportunity description
- Market size estimation
- Implementation difficulty
- Competitive advantage potential
- PPC campaign implications

Focus on gaps that can be exploited through strategic PPC campaigns.
"""

        # Phase 4: Strategic Positioning Development
        phase4_template = """
# Phase 4: Strategic Positioning Development

Based on the previous analysis, I need you to develop a comprehensive strategic positioning strategy for PPC campaigns.

## Business Context:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Services**: {{services}}
- **Target Audience**: {{target_audience}}
- **Unique Value**: {{unique_value}}
- **Budget Range**: {{budget_range}}
- **Primary Goal**: {{primary_goal}}

## Strategic Positioning Development Required:

Please develop a comprehensive positioning strategy including:

1. **Core Positioning Statement**
   - Primary positioning theme
   - Unique value proposition
   - Competitive differentiation
   - Target audience alignment

2. **Positioning Pillars**
   - 3-5 key positioning pillars
   - Supporting evidence for each pillar
   - How each pillar differentiates from competitors
   - Relevance to target audience

3. **Messaging Architecture**
   - Primary brand message
   - Secondary supporting messages
   - Audience-specific message variations
   - Emotional vs. rational messaging balance

4. **Competitive Positioning**
   - How to position against main competitors
   - Defensive positioning for competitive attacks
   - Offensive positioning for market expansion
   - Positioning for different competitive scenarios

5. **Audience Positioning**
   - Primary audience positioning
   - Secondary audience positioning
   - Positioning for different customer journey stages
   - Positioning for different customer segments

6. **Channel Positioning**
   - Google Ads positioning strategy
   - Meta/Facebook positioning strategy
   - LinkedIn positioning strategy (if applicable)
   - Platform-specific positioning adaptations

7. **Campaign Positioning Framework**
   - Brand awareness campaign positioning
   - Lead generation campaign positioning
   - Sales campaign positioning
   - Retargeting campaign positioning

8. **Positioning Proof Points**
   - Credentials and certifications
   - Customer testimonials themes
   - Case studies and success stories
   - Awards and recognition

9. **Positioning Testing Strategy**
   - Key positioning elements to test
   - A/B testing recommendations
   - Performance metrics for positioning
   - Positioning optimization approach

Please provide specific, actionable positioning strategies that can be immediately implemented in PPC campaigns.
"""

        # Phase 5: Content & Campaign Strategy
        phase5_template = """
# Phase 5: Content & Campaign Strategy

Based on all previous analysis, I need you to develop comprehensive content and campaign strategies for PPC implementation.

## Business Context:
- **Business**: {{business_name}}
- **Industry**: {{industry}}
- **Services**: {{services}}
- **Target Audience**: {{target_audience}}
- **Budget Range**: {{budget_range}}
- **Primary Goal**: {{primary_goal}}

## Content & Campaign Strategy Development Required:

Please develop comprehensive strategies including:

1. **Campaign Architecture**
   - Recommended campaign types (Search, Display, Video, Shopping, Performance Max)
   - Campaign structure and organization
   - Budget allocation across campaigns
   - Bidding strategy recommendations

2. **Keyword Strategy**
   - Primary keyword themes
   - Secondary keyword opportunities
   - Long-tail keyword suggestions
   - Negative keyword recommendations
   - Seasonal keyword variations

3. **Ad Copy Strategy**
   - Headline themes and variations
   - Description themes and variations
   - Call-to-action recommendations
   - Ad extension strategies
   - Emotional vs. rational copy balance

4. **Landing Page Strategy**
   - Landing page requirements
   - Content structure recommendations
   - Conversion optimization suggestions
   - A/B testing opportunities

5. **Audience Targeting Strategy**
   - Demographics targeting
   - Interest targeting
   - Behavioral targeting
   - Custom audience strategies
   - Lookalike audience development

6. **Content Calendar**
   - Monthly content themes
   - Weekly content types
   - Seasonal content planning
   - Event-driven content opportunities

7. **Creative Strategy**
   - Visual content themes
   - Video content opportunities
   - Image requirements and specifications
   - Brand consistency guidelines

8. **Measurement & Optimization**
   - Key performance indicators
   - Conversion tracking setup
   - Attribution modeling
   - Optimization schedule and process

9. **Budget & Timeline**
   - Phase 1 launch strategy (first 30 days)
   - Phase 2 optimization (days 31-90)
   - Phase 3 scaling (days 91-180)
   - Budget allocation and pacing

10. **Competitive Response Strategy**
    - Monitoring competitive activity
    - Responding to competitive moves
    - Defending market position
    - Capitalizing on competitive weaknesses

Please provide specific, actionable strategies that can be immediately implemented for PPC campaign launch and management.
"""

        # Generate prompts using Jinja2 templates
        templates = {
            'phase1': phase1_template,
            'phase2': phase2_template,
            'phase3': phase3_template,
            'phase4': phase4_template,
            'phase5': phase5_template
        }

        self.generated_prompts = {}
        
        for phase, template_content in templates.items():
            template = Template(template_content)
            rendered_prompt = template.render(**self.business_data)
            self.generated_prompts[phase] = rendered_prompt

        self.print_success("Claude prompts generated successfully!")
        return self.generated_prompts

    def create_research_project(self):
        """Create complete research project structure"""
        self.print_header("📁 Creating Research Project Structure")
        
        # Create project context file
        project_context = f"""# {self.business_data['business_name']} - Claude Research Project

## Project Overview
- **Client**: {self.business_data['business_name']}
- **Industry**: {self.business_data['industry']}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Research Phases**: 5

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
3. Execute Phase 2 prompt in Claude
4. Continue through all 5 phases
5. Compile strategic insights

## Files Generated
- Phase 1 Prompt: phase1_business_intelligence_prompt.md
- Phase 2 Prompt: phase2_competitive_landscape_prompt.md
- Phase 3 Prompt: phase3_market_gaps_prompt.md
- Phase 4 Prompt: phase4_strategic_positioning_prompt.md
- Phase 5 Prompt: phase5_content_strategy_prompt.md
"""

        # Save project context
        context_path = f"{self.folder_name}/02_market_research/claude_research/00_project_context.md"
        with open(context_path, 'w', encoding='utf-8') as f:
            f.write(project_context)

        # Save individual prompt files
        prompt_files = {
            'phase1': 'phase1_business_intelligence_prompt.md',
            'phase2': 'phase2_competitive_landscape_prompt.md',
            'phase3': 'phase3_market_gaps_prompt.md',
            'phase4': 'phase4_strategic_positioning_prompt.md',
            'phase5': 'phase5_content_strategy_prompt.md'
        }

        for phase, filename in prompt_files.items():
            file_path = f"{self.folder_name}/02_market_research/claude_research/{filename}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.generated_prompts[phase])

        # Create workflow instructions
        workflow_instructions = f"""# Claude Research Workflow Instructions

## How to Execute This Research

### Step 1: Prepare Claude
1. Open Claude AI (claude.ai)
2. Start a new conversation
3. Keep this conversation open for all 5 phases

### Step 2: Execute Phase 1
1. Copy the entire content from `phase1_business_intelligence_prompt.md`
2. Paste it into Claude
3. Wait for Claude's comprehensive response
4. Copy Claude's response and save it as `phase_outputs/phase1_business_intelligence.md`

### Step 3: Execute Phase 2
1. Copy the entire content from `phase2_competitive_landscape_prompt.md`
2. Paste it into the same Claude conversation
3. Wait for Claude's response
4. Save the response as `phase_outputs/phase2_competitive_landscape.md`

### Step 4: Execute Phases 3-5
1. Continue the same process for phases 3, 4, and 5
2. Save each response in the corresponding phase_outputs file
3. Keep the conversation context throughout all phases

### Step 5: Compile Strategic Insights
1. Review all phase outputs
2. Create a master strategic document
3. Identify key insights and action items
4. Develop implementation roadmap

## Expected Outputs
- Phase 1: Business intelligence and market position analysis
- Phase 2: Competitive landscape mapping and positioning gaps
- Phase 3: Market opportunities and gap identification
- Phase 4: Strategic positioning and differentiation strategy
- Phase 5: Content strategy and campaign implementation plan

## Tips for Best Results
- Execute phases in order
- Don't skip any phases
- Keep the Claude conversation continuous
- Review and validate insights against real market data
- Use insights to inform PPC campaign strategy

## Estimated Time
- Phase execution: 30-45 minutes
- Review and compilation: 60-90 minutes
- Total research time: 2-3 hours
"""

        workflow_path = f"{self.folder_name}/02_market_research/claude_research/claude_research_workflow.md"
        with open(workflow_path, 'w', encoding='utf-8') as f:
            f.write(workflow_instructions)

        # Create template files for outputs
        template_files = [
            'phase_outputs/phase1_business_intelligence.md',
            'phase_outputs/phase2_competitive_landscape.md',
            'phase_outputs/phase3_market_gaps.md',
            'phase_outputs/phase4_strategic_positioning.md',
            'phase_outputs/phase5_content_strategy.md',
            'strategic_insights.md'
        ]

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
        
        # Create summary file
        summary_content = f"""# {self.business_data['business_name']} - Claude Research Summary

## Quick Start Guide

### 1. Open Claude AI
- Go to claude.ai
- Start a new conversation
- Keep this conversation open for all phases

### 2. Execute Research Phases
Execute these prompts in order:

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

5. **Phase 5**: Content & Campaign Strategy
   - File: `phase5_content_strategy_prompt.md`
   - Save response as: `phase_outputs/phase5_content_strategy.md`

### 3. Compile Results
After completing all phases, review the outputs and create your strategic insights document.

## Business Context Summary
- **Business**: {self.business_data['business_name']}
- **Industry**: {self.business_data['industry']}
- **Primary Goal**: {self.business_data['primary_goal']}
- **Budget**: {self.business_data['budget_range']}
- **Target Audience**: {self.business_data['target_audience']}

## Generated Files
- Project context and overview
- 5 customized Claude prompts
- Workflow instructions
- Output templates
- Strategic insights framework

## Expected Outcome
Comprehensive strategic intelligence for PPC campaign development, including:
- Market position analysis
- Competitive landscape mapping
- Market opportunity identification
- Strategic positioning strategy
- Content and campaign implementation plan

**Total research time**: 2-3 hours
**Implementation value**: Professional-grade strategic intelligence typically requiring 10-15 hours of manual research
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
            
            if self.console:
                table = Table(title="Generated Files")
                table.add_column("File", style="cyan")
                table.add_column("Purpose", style="green")
                
                table.add_row("00_project_context.md", "Project overview and context")
                table.add_row("phase1_business_intelligence_prompt.md", "Phase 1 Claude prompt")
                table.add_row("phase2_competitive_landscape_prompt.md", "Phase 2 Claude prompt")
                table.add_row("phase3_market_gaps_prompt.md", "Phase 3 Claude prompt")
                table.add_row("phase4_strategic_positioning_prompt.md", "Phase 4 Claude prompt")
                table.add_row("phase5_content_strategy_prompt.md", "Phase 5 Claude prompt")
                table.add_row("claude_research_workflow.md", "Step-by-step instructions")
                table.add_row("CLAUDE_RESEARCH_SUMMARY.md", "Quick start guide")
                
                self.console.print(table)
            else:
                print("\n📋 Generated Files:")
                print("  - 00_project_context.md (Project overview)")
                print("  - phase1_business_intelligence_prompt.md")
                print("  - phase2_competitive_landscape_prompt.md")
                print("  - phase3_market_gaps_prompt.md")
                print("  - phase4_strategic_positioning_prompt.md")
                print("  - phase5_content_strategy_prompt.md")
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