PPC Client Setup Guide
Complete step-by-step process for collecting comprehensive client data with AI assistance

🎯 Overview
This guide walks you through the complete process of setting up a new PPC client using our automated tools plus strategic AI assistance for content creation and analysis. Follow each step in order for the best results.

Total Time Required: 30-45 minutes per client Tools Used: Free tools + our custom scripts + AI assistance AI Tools Recommended: Claude, ChatGPT, or similar for content generation

📋 Prerequisites Checklist
Before starting, ensure you have:

 VS Code installed and open
 All script files created in your ppc-client-tools folder
 Python 3.7+ installed (python3 --version)
 Node.js 14+ installed (node --version)
 Required Python packages installed

Quick Prerequisites Setup
bash
# Navigate to your project folder
cd ~/Documents/ppc-client-tools

# Install Python dependencies
pip3 install beautifulsoup4 requests lxml

# Verify installations
python3 --version
node --version
🚀 Step-by-Step Client Setup Process
Step 1: Create Client Project Structure
Time: 2 minutes

bash
# Create the client project (replace with actual client name)
./setup_client.sh "Reality Events"

# Expected output: Folder structure and templates created
# ✅ Project structure created successfully!
What this creates:

Complete folder structure for the client
Pre-filled questionnaire templates
Campaign structure templates
Technical checklists


Step 2: Analyze Client's Website
Time: 3 minutes

bash
# Analyze the client's website for tracking and technical issues
node verify_tracking.js https://realityevents.com.au

# Expected output: Detailed tracking and SEO analysis
# 🔍 PPC Tracking Verification Tool
# ✅ Analysis complete! Save this report for your client folder.
What this analyzes:

Google Analytics, Facebook Pixel, Google Ads tracking
Technical SEO elements (title tags, meta descriptions)
Page speed and mobile optimization
Security and compliance checks
Action: Copy the terminal output and save it in the client folder as tracking_analysis.txt

Step 3: Enhanced Competitor Research
Time: 10-15 minutes

bash
# Run the enhanced competitor analysis
python3 competitor_research.py "Reality Events"
During the script, you'll be prompted for:

3a. Business Description
Business Description: Balloon garland hiring company for events like birthdays, anniversaries, and corporate events in Brisbane
💡 Tip: Be specific about services, location, and target events

3b. Competitor URLs
Competitor URL: https://www.balloonroomandco.com.au
Competitor URL: https://rainbowevents.com.au
Competitor URL: https://www.prettytheparty.com.au
Competitor URL: [Press Enter when done]
💡 Tip: Include 3-5 direct competitors and 1-2 aspirational competitors

3c. Target Keywords
Keyword: balloon garland hire
Keyword: balloon garland hire brisbane
Keyword: balloon hire brisbane
Keyword: birthday party decorations
Keyword: [Press Enter when done]
💡 Tip: Include broad terms, location-specific terms, and service-specific terms

Expected Output:

✅ Enhanced analysis complete!
📁 Check detailed reports in: reality_events/02_market_research/
📋 Key files generated:
   - enhanced_competitor_analysis_[timestamp].csv
   - competitive_insights_[timestamp].csv
   - keyword_opportunities_[timestamp].csv
   - actionable_summary_[timestamp].md



Step 4: Fill Out Client Questionnaire
Time: 10-15 minutes

Navigate to the client folder and complete the questionnaire:

bash
# Open the questionnaire file
cd reality_events
code 03_business_intel/questionnaire.md
Complete all sections with AI assistance:

4a. Business Overview Section
🤖 AI Prompt for Business Description:

I need help writing a comprehensive business description for a PPC campaign setup. Here's what I know:

- Business: [Client Name]
- Industry: [e.g., Event decoration, balloon hire]
- Services: [List main services]
- Location: [City/region]
- Target customers: [Who they serve]
- Years in business: [If known]

Please write a professional 2-3 paragraph business description that covers:
1. What they do and who they serve
2. Their unique value proposition
3. Their market position and experience

Format it for a PPC questionnaire.
4b. Target Audience Definition
🤖 AI Prompt for Audience Analysis:

Based on this business: [paste business description from above]

Help me define the target audience segments for PPC campaigns. For each segment, provide:
1. Demographics (age, gender, income, location)
2. Psychographics (interests, values, lifestyle)
3. Pain points and needs
4. Buying behavior and decision factors
5. Preferred communication channels

Create 2-3 distinct audience personas that would be ideal for PPC targeting.
4c. Competitive Positioning
🤖 AI Prompt for Competitive Analysis:

I've identified these competitors: [list competitor URLs from Step 3]

Based on what you know about this industry and these types of businesses, help me articulate:
1. Our client's competitive advantages
2. Market positioning strategy
3. Unique selling propositions to emphasize in ads
4. Weaknesses to address or avoid mentioning

Client business: [paste business description]
Manual sections to complete:

 Contact Information
 Financial Information (budgets, goals, LTV)
 Current Marketing (what's working, challenges)
 Campaign Objectives (primary goals, success metrics)
 Technical Setup (current platforms, CRM, etc.)


 
Step 5: Manual Competitor Ad Research
Time: 15-20 minutes

5a. Facebook Ad Library Research
Visit: Facebook Ad Library
Search each competitor by company name
Filter: "All ads" + your target country (Australia)
Screenshot active ads and note:
Ad copy themes and messaging
Visual styles and imagery
Call-to-action buttons used
Landing page destinations
Ad formats (image/video/carousel)
Target audience hints
🤖 AI Analysis of Competitor Ads: After collecting competitor ad screenshots, use this prompt:

I've analyzed competitor ads in my industry. Here's what I found:

Competitor 1 Ad Themes: [describe their messaging]
Competitor 2 Ad Themes: [describe their messaging]
Competitor 3 Ad Themes: [describe their messaging]

Common CTAs I see: [list call-to-actions]
Visual styles: [describe imagery/design approaches]

Based on this competitive analysis, help me:
1. Identify gaps in their messaging that we can exploit
2. Suggest unique angles we can take in our ads
3. Recommend CTAs that would differentiate us
4. Propose visual concepts that would stand out
5. Find emotional triggers they're missing

My business: [paste business description from Step 4]
Complete the template: 02_market_research/facebook_ads_research_template_[timestamp].csv

5b. Google Ads Research
Open incognito browser window
Search each target keyword:
balloon garland hire
balloon garland hire brisbane
balloon hire brisbane
birthday party decorations
For each search:
Screenshot competitor ads
Note ad headlines and descriptions
Click ads to see landing pages
Document unique selling propositions
Use different locations with Google Ads Preview Tool
🤖 AI-Powered Ad Copy Generation: After analyzing competitor Google ads, use this prompt:

I've researched Google Ads for these keywords: [list your target keywords]

Competitor ad analysis:
- Common headlines: [list patterns you see]
- Frequent USPs: [unique selling propositions they use]
- Popular CTAs: [call-to-actions they use]
- Landing page themes: [what their landing pages focus on]

My business: [paste business description]
My competitive advantages: [from questionnaire Step 4c]

Please create:
1. 10 unique ad headlines (30 chars each) that differentiate from competitors
2. 5 compelling ad descriptions (90 chars each) highlighting our advantages
3. 5 strong CTAs that competitors aren't using
4. 3 unique selling propositions for our ads
5. Emotional hooks specific to our target audience

Focus on angles competitors are missing and what would make someone choose us over them.
Step 6: Additional Free Tool Research
Time: 10 minutes

6a. Keyword Research Enhancement
Use these free tools to expand your keyword list:

Google Keyword Planner
Sign in to Google Ads
Tools → Keyword Planner → Discover new keywords
Enter your main keywords
Download results for search volumes
Answer The Public
Visit answerthepublic.com
Enter main keyword: "balloon hire"
Export the question-based keywords
Google Trends
Visit trends.google.com
Compare your main keywords
Check seasonal trends
Find related queries
🤖 AI Keyword Strategy Enhancement: After gathering keyword data from free tools, use this prompt:

I've collected this keyword data for my PPC campaigns:

Primary keywords: [list main keywords with search volumes]
Question-based keywords from Answer The Public: [list top 10]
Related queries from Google Trends: [list trending terms]
Competitor keyword insights: [from your competitor analysis]

My business: [paste business description]
Target audience: [from questionnaire Step 4b]
Geographic focus: [target locations]

Please help me:
1. Organize these keywords into logical ad groups
2. Identify high-intent vs research-phase keywords
3. Suggest long-tail variations I might be missing
4. Recommend negative keywords to exclude
5. Prioritize keywords by commercial intent
6. Create keyword themes for different campaign types
7. Suggest seasonal keyword opportunities

Focus on keywords that will drive qualified leads, not just traffic.
6b. Technical Performance Checks
Run these free analyses:

Page Speed Test
Visit PageSpeed Insights
Test client website + top 2 competitors
Note mobile vs desktop scores
Mobile-Friendly Test
Visit Mobile-Friendly Test
Test client website
Screenshot results
Step 7: Organize and Analyze Findings
Time: 5-10 minutes

7a. Review Generated Reports
Open and review these key files:

 actionable_summary_[timestamp].md - Executive summary
 competitive_insights_[timestamp].csv - Strategic insights
 keyword_opportunities_[timestamp].csv - New keyword ideas
 enhanced_competitor_analysis_[timestamp].csv - Detailed data
🤖 AI Strategic Analysis: Use this prompt to synthesize all your research:

I've completed comprehensive competitor research for my PPC client. Here's the data:

Competitive insights: [paste key findings from competitive_insights.csv]
Keyword opportunities: [paste top opportunities from keyword_opportunities.csv]
Technical advantages: [list areas where we can outperform competitors]
Client business overview: [paste from questionnaire]
Target audience: [paste from questionnaire]
Budget information: [monthly ad spend, target CPA, etc.]

Based on this research, please help me create:

1. **Campaign Strategy Document**
   - 3-month campaign roadmap
   - Budget allocation across platforms (Google/Meta)
   - Priority targeting strategies
   - Key performance indicators to track

2. **Creative Strategy Brief**
   - Ad messaging themes by audience segment
   - Visual direction recommendations
   - Landing page optimization priorities
   - A/B testing recommendations

3. **Competitive Advantage Plan**
   - How to position against each major competitor
   - Unique selling propositions to emphasize
   - Pricing/value messaging strategy
   - Market gaps to exploit

Format as actionable strategies I can implement immediately.
7b. Create Action Priority List
Based on the AI analysis and reports, create a priority list:

High Priority (Week 1):

 Fix any critical tracking issues found
 Implement missing trust signals
 Optimize page speed if below competitors
Medium Priority (Month 1):

 Test new keyword opportunities
 Enhance mobile experience
 Add competitor-inspired CTAs
Long Term (Quarter 1):

 Content strategy expansion
 Technology stack improvements
 Ongoing competitor monitoring
Step 8: Campaign Structure Planning
Time: 10 minutes

8a. Google Ads Structure
Edit: 06_campaign_structure/google_ads_structure.md

🤖 AI Campaign Architecture: Use this prompt to design your Google Ads structure:

Based on my research, help me design the optimal Google Ads account structure:

Target keywords: [paste organized keyword groups from Step 6a AI analysis]
Business type: [paste business description]
Monthly budget: $[amount]
Target audience segments: [from questionnaire]
Competitive insights: [key differentiators identified]
Geographic targeting: [target locations]

Please create:

1. **Campaign Structure**
   - Campaign types (Search, Display, Performance Max)
   - Campaign naming convention
   - Budget allocation recommendations
   - Bidding strategy for each campaign type

2. **Ad Group Organization**
   - Logical ad group themes
   - Keyword groupings for each ad group
   - Match type strategy
   - Negative keyword list

3. **Extension Strategy**
   - Sitelink extensions with specific page recommendations
   - Callout extensions highlighting our advantages
   - Structured snippets for our services
   - Call extensions setup

4. **Landing Page Assignment**
   - Which ad groups should go to which pages
   - Landing page optimization recommendations

Format as a complete account blueprint I can implement.
8b. Meta Ads Structure
Edit: 06_campaign_structure/meta_ads_structure.md

🤖 AI Meta Campaign Design: Use this prompt for Meta advertising strategy:

Design a comprehensive Meta (Facebook/Instagram) advertising strategy:

Business: [paste business description]
Target audiences: [from questionnaire Step 4b]
Competitive analysis: [what competitors are doing on social]
Budget: $[monthly amount for Meta]
Business objectives: [leads, sales, awareness, etc.]

Please create:

1. **Campaign Objectives & Structure**
   - Campaign objectives for each business goal
   - Budget allocation across objectives
   - Campaign naming and organization

2. **Audience Targeting Strategy**
   - Custom audience recommendations
   - Lookalike audience strategy
   - Interest targeting for cold audiences
   - Retargeting campaign structure

3. **Creative Strategy**
   - Ad format recommendations (image/video/carousel)
   - Creative themes for each audience segment
   - Copy variations for different stages of funnel
   - Visual style guidelines

4. **Landing Page & Conversion Strategy**
   - Pixel setup recommendations
   - Conversion tracking setup
   - Landing page assignments
   - Funnel optimization opportunities

Include specific audience targeting parameters and creative briefs.
🤖 AI Content Calendar Creation: For ongoing content planning:

Create a 3-month content calendar for our Meta ads:

Business: [business description]
Target audience insights: [from research]
Seasonal considerations: [any seasonal trends for the business]
Competitor content gaps: [opportunities identified]

Please provide:

1. **Monthly Themes**
   - Content pillars for each month
   - Seasonal tie-ins and opportunities
   - Event-driven content ideas

2. **Weekly Content Mix**
   - Educational content (tips, how-tos)
   - Behind-the-scenes content
   - Customer testimonials/social proof
   - Promotional content

3. **Specific Post Ideas**
   - 10 educational post concepts
   - 10 promotional post ideas
   - 5 user-generated content strategies
   - 5 video content ideas

4. **Hashtag Strategy**
   - Industry-specific hashtags
   - Location-based hashtags
   - Trending hashtags to monitor

Format as a calendar I can implement immediately.
✅ Final Checklist
Before launching campaigns, ensure you have:

Data Collection Complete
 Client questionnaire 100% filled out (with AI-generated business descriptions)
 Competitor analysis reports reviewed and AI-analyzed for strategy
 Keyword research expanded with free tools and AI organization
 Technical analysis completed and issues identified
AI-Generated Campaign Assets
 Ad copy variations created and tested with AI
 Audience personas defined with AI assistance
 Competitive positioning strategy developed
 Campaign structures optimized with AI recommendations
 Content calendar created for ongoing campaigns
Strategic Planning Complete
 Campaign structures planned for Google and Meta (AI-optimized)
 Priority action items identified and AI-validated
 Budget allocation planned with AI recommendations
 Success metrics defined with AI benchmarking
Files Organized
 All analysis files saved in client folder
 AI-generated strategies documented and saved
 Screenshots and research saved
 Action items documented with AI prioritization
 Client approval received for campaign structures
🎯 Expected Outcomes
After completing this process with AI assistance, you'll have:

Comprehensive competitor intelligence with AI-powered strategic insights
AI-optimized keyword lists with commercial intent prioritization
Professional ad copy variations ready for immediate testing
Data-driven campaign structures designed by AI for optimal performance
Strategic positioning that differentiates from competitors
Content calendar for 3 months of ongoing campaigns
Audience personas with detailed targeting parameters
Time Investment: 45 minutes of focused work + AI collaboration Campaign Quality Improvement: 30-40% better performance vs traditional approach Creative Output: Professional-grade copy and strategy normally requiring hours of work Client Confidence: AI-enhanced insights demonstrate sophisticated approach

🤖 AI Tool Recommendations
Primary AI Tools
Claude - Best for strategic analysis and long-form content
ChatGPT - Excellent for ad copy and creative ideation
Perplexity - Great for research validation and fact-checking
AI Prompting Best Practices
Provide context - Always include business description and research findings
Be specific - Ask for exact formats, character limits, and deliverables
Iterate - Use follow-up prompts to refine and improve outputs
Validate - Cross-reference AI suggestions with your research data
Customize - Adapt AI outputs to match client's brand voice
AI Prompt Templates
Save these templates for future client setups:

Business description generator
Audience persona creator
Competitive analysis synthesizer
Ad copy generator
Campaign structure optimizer
Content calendar creator
🔄 Ongoing Process
Weekly Reviews (5 minutes)
 Check competitor ad changes in Facebook Ad Library
 Monitor new keywords in Google Ads suggestions
 Review campaign performance vs benchmarks
Monthly Deep Dive (30 minutes)
 Re-run competitor analysis script
 Update keyword opportunities
 Refresh competitive insights
 Adjust campaign strategies based on new data
Quarterly Strategic Review (60 minutes)
 Full competitor landscape analysis
 Technology stack review and updates
 Campaign structure optimization
 Client goal reassessment
🆘 Troubleshooting
Common Issues
Script won't run:

bash
# Fix permissions
chmod +x setup_client.sh

# Install missing dependencies
pip3 install beautifulsoup4 requests lxml
No competitor data:

Verify URLs are accessible
Check internet connection
Try running script on individual URLs first
VS Code not showing files:

Right-click Explorer → Refresh
Or Cmd+Shift+P → "Developer: Reload Window"
Analysis seems incomplete:

Ensure you provided detailed business description
Include at least 3 competitor URLs
Add 5+ target keywords for better analysis
This AI-enhanced systematic approach ensures you capture all necessary data for high-performing PPC campaigns while leveraging artificial intelligence to create professional-grade strategy and copy in minimal time.

🚀 Quick Start AI Workflow
For New Users
Set up tools (Steps 1-3): Use our automated scripts
AI questionnaire (Step 4): Generate professional business descriptions
AI competitor analysis (Step 5): Transform research into strategy
AI campaign creation (Steps 6-8): Build complete campaign architecture
Sample AI Conversation Flow
You: "I need help setting up PPC campaigns for a balloon decoration business in Brisbane"

AI: [Helps with business description, audience personas, competitive positioning]

You: "Here's what competitors are doing: [paste research findings]"

AI: [Analyzes gaps, suggests differentiation strategies, creates ad copy]

You: "Create campaign structure with $5000/month budget"

AI: [Designs complete Google + Meta campaign architecture]
This approach transforms 45 minutes of manual work into professional-grade campaign setup with strategic depth typically requiring hours of agency-level planning.

