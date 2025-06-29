#!/bin/bash

# PPC Client Setup Script
# Usage: ./setup_client.sh "Client Name"

set -e

CLIENT_NAME=$1
if [ -z "$CLIENT_NAME" ]; then
    echo "❌ Error: Please provide a client name"
    echo "Usage: ./setup_client.sh 'Client Name'"
    echo "Example: ./setup_client.sh 'Acme Corporation'"
    exit 1
fi

# Sanitize client name for folder creation
FOLDER_NAME=$(echo "$CLIENT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g' | sed 's/__*/_/g' | sed 's/^_\|_$//g')

echo "🚀 Setting up PPC project for: $CLIENT_NAME"
echo "📁 Folder name: $FOLDER_NAME"

# Create main client directory
mkdir -p "$FOLDER_NAME"

# Create folder structure
echo "📂 Creating folder structure..."
mkdir -p "$FOLDER_NAME/01_brand_assets"/{logos,images,videos,existing_ads}
mkdir -p "$FOLDER_NAME/02_market_research"/{competitor_analysis,keyword_research,audience_insights,claude_research/phase_outputs,market_intelligence}
mkdir -p "$FOLDER_NAME/03_business_intel/ai_insights"
mkdir -p "$FOLDER_NAME/04_technical_setup"/{landing_page_analysis,tracking_verification}
mkdir -p "$FOLDER_NAME/05_historical_data"/{analytics_exports,previous_campaigns,performance_reports}
mkdir -p "$FOLDER_NAME/06_campaign_structure"/{google_ads,meta_ads,campaign_assets}
mkdir -p "$FOLDER_NAME/07_compliance"
mkdir -p "$FOLDER_NAME/08_reporting"/{weekly_reports,monthly_reports}

# Create template files
echo "📄 Creating template files..."

# Brand Guidelines Template
cat > "$FOLDER_NAME/01_brand_assets/brand_guidelines.md" << EOF
# $CLIENT_NAME - Brand Guidelines

## Brand Colors
- Primary Color: #
- Secondary Color: #
- Accent Color: #
- Background Color: #

## Typography
- Primary Font: 
- Secondary Font: 
- Heading Font: 

## Brand Voice & Tone
- Voice Description: 
- Tone Characteristics: 
- Key Messages: 

## Logo Usage
- Logo variations available: 
- Minimum size requirements: 
- Clear space requirements: 
- Usage restrictions: 

## Visual Style
- Photography style: 
- Graphic elements: 
- Design principles: 

## Brand Values
- Core values: 
- Mission statement: 
- Unique selling proposition: 

Last Updated: $(date +%Y-%m-%d)
EOF

# Business Intelligence Questionnaire
cat > "$FOLDER_NAME/03_business_intel/questionnaire.md" << EOF
# $CLIENT_NAME - Business Intelligence Questionnaire

## Contact Information
- **Primary Contact**: 
- **Email**: 
- **Phone**: 
- **Company Website**: 
- **Industry**: 

## Business Overview
- **Company Description**: 
- **Years in Business**: 
- **Number of Employees**: 
- **Geographic Markets**: 
- **Primary Revenue Streams**: 

## Financial Information
- **Monthly Advertising Budget**: $
- **Target Cost Per Acquisition**: $
- **Average Customer Lifetime Value**: $
- **Average Order Value**: $
- **Profit Margins**: %
- **Revenue Goals (Annual)**: $

## Current Marketing
- **Current Marketing Channels**: 
- **What's Working Well**: 
- **Biggest Marketing Challenges**: 
- **Previous PPC Experience**: 
- **Current Conversion Rate**: %

## Target Audience
- **Primary Demographics**: 
- **Secondary Demographics**: 
- **Customer Pain Points**: 
- **Buying Behavior**: 
- **Preferred Communication Channels**: 

## Competitors
- **Direct Competitors**: 
- **Indirect Competitors**: 
- **Competitive Advantages**: 
- **Market Position**: 

## Campaign Objectives
- **Primary Goal**: (Leads/Sales/Brand Awareness/Traffic)
- **Success Metrics**: 
- **Timeline/Deadlines**: 
- **Seasonal Considerations**: 

## Technical Setup
- **Current Website Platform**: 
- **CRM System**: 
- **Email Marketing Platform**: 
- **Analytics Tracking**: 
- **Existing Pixels/Tags**: 

Completed By: ________________
Date: $(date +%Y-%m-%d)
EOF

# AI-Powered Business Intelligence Template
cat > "$FOLDER_NAME/03_business_intel/ai_insights/ai_generated_insights.md" << EOF
# $CLIENT_NAME - AI-Generated Business Insights

## Strategic Analysis Overview
Generated using Claude AI research methodology
Date: $(date +%Y-%m-%d)

## Business Intelligence Analysis
*Paste Phase 1 Claude output here*

### Market Position Assessment
- Industry landscape analysis
- Business maturity evaluation
- Market opportunity size
- Competitive intensity

### Competitive Advantages
- Unique differentiators
- Competitive moats
- Value proposition strengths
- Sustainable advantages

### Target Market Analysis
- Primary audience segments
- Secondary opportunities
- Customer journey mapping
- Pain point prioritization

## Competitive Landscape Mapping
*Paste Phase 2 Claude output here*

### Direct Competitors
- Main competitive threats
- Service offering comparison
- Market positioning analysis
- Competitive advantages/weaknesses

### Indirect Competitors
- Alternative solutions
- Substitute services
- Adjacent industry competition
- DIY/self-service options

## Market Gap Analysis
*Paste Phase 3 Claude output here*

### Service Gaps
- Underserved market needs
- Missing service combinations
- Quality level opportunities
- Delivery method gaps

### Geographic Opportunities
- Underserved locations
- Competitor weaknesses
- Expansion potential
- Local advantages

### Audience Opportunities
- Underserved segments
- Demographic gaps
- Psychographic opportunities
- Niche targeting potential

## Strategic Positioning
*Paste Phase 4 Claude output here*

### Core Positioning Statement
- Primary positioning theme
- Unique value proposition
- Competitive differentiation
- Target audience alignment

### Positioning Pillars
- Key supporting themes
- Proof points and evidence
- Differentiation factors
- Audience relevance

## Content & Campaign Strategy
*Paste Phase 5 Claude output here*

### Campaign Architecture
- Recommended campaign types
- Budget allocation
- Platform prioritization
- Bidding strategies

### Keyword Strategy
- Primary keyword themes
- Long-tail opportunities
- Seasonal variations
- Negative keywords

### Ad Copy Strategy
- Headline variations
- Description themes
- Call-to-action options
- Extension strategies

## Implementation Roadmap

### Phase 1 (Weeks 1-2): Foundation
- [ ] Campaign setup and structure
- [ ] Initial keyword research and grouping
- [ ] Ad copy creation and testing
- [ ] Landing page optimization
- [ ] Conversion tracking setup

### Phase 2 (Weeks 3-6): Optimization
- [ ] Performance analysis and optimization
- [ ] A/B testing implementation
- [ ] Budget reallocation based on performance
- [ ] Audience refinement
- [ ] Competitive response monitoring

### Phase 3 (Weeks 7-12): Scaling
- [ ] Successful campaign scaling
- [ ] New keyword expansion
- [ ] Additional platform testing
- [ ] Creative refresh and updates
- [ ] Long-term strategy refinement

## Key Performance Indicators
- Primary success metrics
- Leading indicators
- Lagging indicators
- Optimization triggers

## Competitive Monitoring
- Competitor tracking schedule
- Market change indicators
- Response strategies
- Opportunity identification

## Next Steps
1. Complete Claude AI research phases
2. Validate insights with market data
3. Implement campaign recommendations
4. Monitor and optimize performance
5. Scale successful strategies

Analysis Completed: $(date +%Y-%m-%d)
Strategic Implementation: [Target Date]
EOF

# Claude Research Workflow Template
cat > "$FOLDER_NAME/02_market_research/claude_research/claude_research_workflow.md" << EOF
# $CLIENT_NAME - Claude AI Research Workflow

## Research Methodology
This document outlines the 5-phase Claude AI research process for strategic PPC campaign development.

## Phase Overview
1. **Business Intelligence Analysis** - Market position and opportunity assessment
2. **Competitive Landscape Mapping** - Competitive analysis and positioning gaps
3. **Market Gap Identification** - Opportunity identification and market gaps
4. **Strategic Positioning Development** - Positioning strategy and differentiation
5. **Content & Campaign Strategy** - Implementation strategy and tactics

## Execution Instructions

### Step 1: Prepare Claude Session
- Open Claude AI (claude.ai)
- Start a new conversation
- Keep this session open for all 5 phases for context continuity

### Step 2: Execute Research Phases
Execute the following prompts in order:

#### Phase 1: Business Intelligence Analysis
- **File**: phase1_business_intelligence_prompt.md
- **Purpose**: Analyze business position and market opportunities
- **Output**: Save response as phase_outputs/phase1_business_intelligence.md

#### Phase 2: Competitive Landscape Mapping  
- **File**: phase2_competitive_landscape_prompt.md
- **Purpose**: Map competitive landscape and identify positioning gaps
- **Output**: Save response as phase_outputs/phase2_competitive_landscape.md

#### Phase 3: Market Gap Identification
- **File**: phase3_market_gaps_prompt.md  
- **Purpose**: Identify market gaps and exploitation opportunities
- **Output**: Save response as phase_outputs/phase3_market_gaps.md

#### Phase 4: Strategic Positioning Development
- **File**: phase4_strategic_positioning_prompt.md
- **Purpose**: Develop strategic positioning and differentiation strategy
- **Output**: Save response as phase_outputs/phase4_strategic_positioning.md

#### Phase 5: Content & Campaign Strategy
- **File**: phase5_content_strategy_prompt.md
- **Purpose**: Create comprehensive implementation strategy
- **Output**: Save response as phase_outputs/phase5_content_strategy.md

### Step 3: Compile Strategic Insights
After completing all phases:
1. Review all phase outputs
2. Extract key strategic insights
3. Create implementation roadmap
4. Prioritize opportunities and actions
5. Document in strategic_insights.md

## Quality Checklist
- [ ] All 5 phases completed in sequence
- [ ] Claude context maintained throughout
- [ ] All outputs saved in phase_outputs folder
- [ ] Key insights extracted and documented
- [ ] Implementation roadmap created
- [ ] Stakeholder review completed

## Expected Outcomes
- Comprehensive market intelligence
- Competitive positioning strategy
- Market opportunity identification
- Strategic campaign framework
- Implementation roadmap

## Timeline
- **Research Execution**: 2-3 hours
- **Analysis and Compilation**: 1-2 hours
- **Strategy Development**: 2-3 hours
- **Total Investment**: 5-8 hours

## Success Metrics
- Strategic clarity and direction
- Competitive advantage identification
- Campaign performance improvement
- ROI optimization opportunities
- Market positioning strength

Research Initiated: $(date +%Y-%m-%d)
Expected Completion: [Add target date]
EOF

# Technical Setup Checklist
cat > "$FOLDER_NAME/04_technical_setup/tracking_checklist.md" << EOF
# $CLIENT_NAME - Technical Setup Checklist

## Website Analysis
- [ ] Page speed test completed (Mobile & Desktop)
- [ ] Mobile-friendly test passed
- [ ] SSL certificate verified
- [ ] Contact forms tested
- [ ] Checkout process documented
- [ ] Key landing pages identified

## Tracking Implementation
- [ ] Google Analytics 4 installed and configured
- [ ] Google Ads conversion tracking setup
- [ ] Facebook/Meta Pixel installed
- [ ] Enhanced ecommerce tracking (if applicable)
- [ ] Phone call tracking setup
- [ ] Form submission tracking configured

## Conversion Setup
- [ ] Primary conversion actions defined
- [ ] Secondary conversion actions identified
- [ ] Conversion values assigned
- [ ] Attribution model selected
- [ ] Goal funnels created

## UTM Parameter Strategy
- [ ] Naming convention established
- [ ] UTM templates created
- [ ] Tracking spreadsheet setup
- [ ] QR code tracking implemented (if needed)

## Testing & Verification
- [ ] All tracking codes tested
- [ ] Conversion actions verified
- [ ] Cross-device tracking confirmed
- [ ] Data accuracy validated

## Access & Permissions
- [ ] Google Analytics access granted
- [ ] Google Ads account access provided
- [ ] Facebook Business Manager access confirmed
- [ ] Search Console access verified
- [ ] Tag Manager permissions set

Setup Completed By: ________________
Date: ________________
EOF

# Competitor Analysis Template
cat > "$FOLDER_NAME/02_market_research/competitor_analysis.md" << EOF
# $CLIENT_NAME - Competitor Analysis

## Competitor 1: [Company Name]
- **Website**: 
- **Industry Position**: 
- **Estimated Monthly Ad Spend**: 
- **Primary Keywords**: 
- **Ad Copy Themes**: 
- **Landing Page Strategy**: 
- **Unique Selling Points**: 
- **Pricing Strategy**: 
- **Strengths**: 
- **Weaknesses**: 
- **Opportunities**: 

## Competitor 2: [Company Name]
- **Website**: 
- **Industry Position**: 
- **Estimated Monthly Ad Spend**: 
- **Primary Keywords**: 
- **Ad Copy Themes**: 
- **Landing Page Strategy**: 
- **Unique Selling Points**: 
- **Pricing Strategy**: 
- **Strengths**: 
- **Weaknesses**: 
- **Opportunities**: 

## Competitor 3: [Company Name]
- **Website**: 
- **Industry Position**: 
- **Estimated Monthly Ad Spend**: 
- **Primary Keywords**: 
- **Ad Copy Themes**: 
- **Landing Page Strategy**: 
- **Unique Selling Points**: 
- **Pricing Strategy**: 
- **Strengths**: 
- **Weaknesses**: 
- **Opportunities**: 

## Market Analysis Summary
- **Market Leaders**: 
- **Emerging Players**: 
- **Market Gaps**: 
- **Trending Strategies**: 
- **Opportunities for Client**: 

Analysis Completed: $(date +%Y-%m-%d)
EOF

# Campaign Structure Template
cat > "$FOLDER_NAME/06_campaign_structure/google_ads_structure.md" << EOF
# $CLIENT_NAME - Google Ads Campaign Structure

## Account Structure Overview
- **Account Name**: $CLIENT_NAME Google Ads
- **Time Zone**: 
- **Currency**: 
- **Billing Setup**: 

## Campaign 1: [Campaign Name]
- **Campaign Type**: Search/Display/Shopping/Video
- **Campaign Goal**: 
- **Budget**: $ per day
- **Bidding Strategy**: 
- **Target Locations**: 
- **Language Targeting**: 
- **Ad Schedule**: 
- **Device Targeting**: 

### Ad Groups
#### Ad Group 1: [Ad Group Name]
- **Keywords**: 
- **Match Types**: 
- **Negative Keywords**: 
- **Landing Page**: 
- **Ad Copy Themes**: 

#### Ad Group 2: [Ad Group Name]
- **Keywords**: 
- **Match Types**: 
- **Negative Keywords**: 
- **Landing Page**: 
- **Ad Copy Themes**: 

## Campaign 2: [Campaign Name]
[Repeat structure above]

## Conversion Tracking Setup
- **Primary Conversions**: 
- **Secondary Conversions**: 
- **Attribution Model**: 
- **Conversion Windows**: 

## Extensions Strategy
- **Sitelink Extensions**: 
- **Callout Extensions**: 
- **Structured Snippets**: 
- **Call Extensions**: 
- **Location Extensions**: 
- **Price Extensions**: 

Structure Created: $(date +%Y-%m-%d)
EOF

# Meta Ads Structure Template
cat > "$FOLDER_NAME/06_campaign_structure/meta_ads_structure.md" << EOF
# $CLIENT_NAME - Meta Ads Campaign Structure

## Account Setup
- **Business Manager ID**: 
- **Ad Account ID**: 
- **Page ID**: 
- **Instagram Account**: 
- **Pixel ID**: 

## Campaign 1: [Campaign Name]
- **Campaign Objective**: 
- **Budget**: $ per day
- **Budget Type**: Daily/Lifetime
- **Campaign Bid Strategy**: 
- **Campaign Start Date**: 
- **Campaign End Date**: 

### Ad Set 1: [Ad Set Name]
- **Optimization Goal**: 
- **Billing Event**: 
- **Bid Amount**: $
- **Budget**: $ per day
- **Schedule**: 
- **Audience**: 
  - **Demographics**: 
  - **Interests**: 
  - **Behaviors**: 
  - **Custom Audiences**: 
  - **Lookalike Audiences**: 
- **Placements**: 
- **Device Targeting**: 

#### Ads
- **Ad 1**: [Ad Name]
  - **Format**: 
  - **Creative**: 
  - **Copy**: 
  - **CTA**: 
  - **Landing Page**: 

- **Ad 2**: [Ad Name]
  - **Format**: 
  - **Creative**: 
  - **Copy**: 
  - **CTA**: 
  - **Landing Page**: 

## Campaign 2: [Campaign Name]
[Repeat structure above]

## Tracking Setup
- **Pixel Events**: 
- **Custom Conversions**: 
- **Attribution Setting**: 
- **Conversion Windows**: 

## Creative Strategy
- **Image Specifications**: 
- **Video Specifications**: 
- **Copy Guidelines**: 
- **Brand Compliance**: 

Structure Created: $(date +%Y-%m-%d)
EOF

# Project README
cat > "$FOLDER_NAME/README.md" << EOF
# $CLIENT_NAME - PPC Project

## Project Overview
- **Client**: $CLIENT_NAME
- **Project Start Date**: $(date +%Y-%m-%d)
- **Account Manager**: 
- **Campaign Manager**: 

## Quick Links
- [Brand Assets](./01_brand_assets/)
- [Market Research](./02_market_research/)
- [Business Intelligence](./03_business_intel/)
- [Technical Setup](./04_technical_setup/)
- [Historical Data](./05_historical_data/)
- [Campaign Structure](./06_campaign_structure/)

## Current Status
- [ ] Initial client questionnaire completed
- [ ] Brand assets collected
- [ ] Technical setup verified
- [ ] Competitor research completed
- [ ] Campaign structure approved
- [ ] Tracking implementation completed
- [ ] Campaigns launched

## Important Notes
- 
- 
- 

## Key Contacts
- **Client Primary Contact**: 
- **Client Technical Contact**: 
- **Account Manager**: 
- **Campaign Manager**: 

Last Updated: $(date +%Y-%m-%d)
EOF

echo "✅ Project structure created successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. cd $FOLDER_NAME"
echo "2. Fill out the questionnaire: 03_business_intel/questionnaire.md"
echo "3. Run tracking verification: node ../verify_tracking.js [website_url]"
echo "4. 🧠 NEW: Run Claude AI research: python3 ../claude_research_setup.py \"$CLIENT_NAME\""
echo "5. Complete traditional competitor research (optional): python3 ../competitor_research.py \"$CLIENT_NAME\""
echo "6. Set up campaign structures in Google Ads and Meta"
echo ""
echo "🚀 Enhanced AI-Powered Workflow:"
echo "   - Claude research setup generates 5-phase strategic analysis"
echo "   - AI-powered business intelligence and competitive analysis"
echo "   - Strategic positioning and campaign implementation strategy"
echo ""
echo "📁 Project location: ./$FOLDER_NAME"
echo "📖 Read the README.md file for project overview"
echo "🧠 Claude AI workflow: 02_market_research/claude_research/"