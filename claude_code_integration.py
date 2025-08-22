#!/usr/bin/env python3
"""
Claude Code Integration Script
Prepares client data for Claude Code analysis and generates custom testing frameworks
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
import argparse

def setup_claude_code_integration(client_name: str, project_path: str = None):
    """
    Prepare complete client analysis package for Claude Code
    """
    if not project_path:
        project_path = Path(f"./{client_name}")
    else:
        project_path = Path(project_path)
    
    print(f"🚀 Setting up Claude Code integration for {client_name}")
    
    # Create Claude Code working directory
    claude_code_dir = project_path / "claude_code_analysis"
    claude_code_dir.mkdir(exist_ok=True)
    
    # Generate comprehensive client brief
    client_brief = generate_client_brief(client_name, project_path)
    
    # Save client brief
    brief_file = claude_code_dir / "client_analysis_brief.md"
    with open(brief_file, 'w') as f:
        f.write(client_brief)
    
    # Copy relevant files for Claude Code access
    copy_analysis_files(project_path, claude_code_dir)
    
    # Generate Claude Code prompt
    claude_prompt = generate_claude_code_prompt(client_name, client_brief)
    
    # Save prompt
    prompt_file = claude_code_dir / "claude_code_prompt.md"
    with open(prompt_file, 'w') as f:
        f.write(claude_prompt)
    
    # Create instruction summary
    instruction_summary = create_instruction_summary(client_name, claude_code_dir)
    
    print(f"✅ Claude Code integration ready!")
    print(f"📁 Analysis files: {claude_code_dir}")
    print(f"📋 Client brief: {brief_file}")
    print(f"🎯 Claude prompt: {prompt_file}")
    print(f"\n🧠 Next steps:")
    print(f"1. Open Claude Code in your project directory")
    print(f"2. Reference the client brief: {brief_file}")
    print(f"3. Use the prompt: {prompt_file}")
    print(f"4. Generate custom testing framework")
    
    return str(claude_code_dir)

def generate_client_brief(client_name: str, project_path: Path) -> str:
    """
    Generate comprehensive client analysis brief for Claude Code
    """
    brief = f"""# {client_name} - Comprehensive Client Analysis Brief for Claude Code

Generated: {datetime.now().isoformat()}

## Project Overview
This brief contains all client research, account structure analysis, and strategic insights needed to generate a custom 6-month testing framework using the Enhanced Testing Framework methodology.

## 📊 Data Sources Summary

### Business Intelligence Analysis
"""
    
    # Load business intelligence
    business_intel_path = project_path / "03_business_intel"
    if business_intel_path.exists():
        brief += f"\n**Location**: `{business_intel_path}`\n"
        
        # Questionnaire summary
        questionnaire_file = business_intel_path / "questionnaire.md"
        if questionnaire_file.exists():
            brief += "\n#### Questionnaire Data Available ✅\n"
            brief += f"- Core business context and goals\n"
            brief += f"- Target audience definitions\n"
            brief += f"- Unique value propositions\n"
        
        # AI insights summary
        ai_insights_path = business_intel_path / "ai_insights"
        if ai_insights_path.exists():
            brief += "\n#### AI Research Insights Available ✅\n"
            phase_files = list(ai_insights_path.glob("phase_*.md"))
            for phase_file in phase_files:
                brief += f"- {phase_file.name}: Strategic analysis complete\n"

    # Market research summary
    market_research_path = project_path / "02_market_research"
    if market_research_path.exists():
        brief += f"\n### Market Research Analysis\n**Location**: `{market_research_path}`\n"
        
        # Claude research outputs
        claude_outputs_path = market_research_path / "claude_research" / "phase_outputs"
        if claude_outputs_path.exists():
            brief += "\n#### Claude Research Phases Available ✅\n"
            output_files = list(claude_outputs_path.glob("*.md"))
            for output_file in output_files:
                brief += f"- {output_file.name}: Competitive and market analysis\n"

    # Account structure analysis
    campaign_structure_path = project_path / "06_campaign_structure"
    if campaign_structure_path.exists():
        brief += f"\n### Current Account Structure\n**Location**: `{campaign_structure_path}`\n"
        
        google_structure = campaign_structure_path / "google_ads_structure.md"
        meta_structure = campaign_structure_path / "meta_ads_structure.md"
        
        if google_structure.exists():
            brief += "- Google Ads structure analysis available ✅\n"
        if meta_structure.exists():
            brief += "- Meta Ads structure analysis available ✅\n"

    # Performance history
    historical_path = project_path / "05_historical_data"
    if historical_path.exists():
        brief += f"\n### Performance History\n**Location**: `{historical_path}`\n"
        data_files = list(historical_path.glob("*.csv")) + list(historical_path.glob("*.json"))
        if data_files:
            brief += f"- {len(data_files)} historical data files available ✅\n"

    # Add analysis requirements
    brief += f"""

## 🎯 Analysis Requirements for Claude Code

### Primary Objectives
1. **Identify Top 3-5 Competitive Advantages** from business intelligence and market research
2. **Extract Market Gaps and Opportunities** from Phase 3 competitive analysis  
3. **Generate 10-15 Testable Hypotheses** based on competitive advantages and market gaps
4. **Create Customized 6-Month Testing Timeline** adapted to client context
5. **Develop Implementation Strategy** for maximum competitive advantage

### Key Analysis Questions to Answer
1. What are {client_name}'s unique competitive advantages vs competitors?
2. Which market gaps offer the highest-impact testing opportunities?
3. How should the testing timeline be adapted for {client_name}'s specific context?
4. What campaign structure optimizations will maximize performance?
5. Which creative strategies will best exploit competitive positioning?

### Expected Deliverables
- Strategic advantage analysis and prioritization
- Custom testing hypothesis library (10-15 hypotheses)
- 6-month implementation timeline with monthly focus areas
- Campaign structure and creative strategy recommendations
- Measurement framework and success criteria

## 📋 Framework Integration Instructions

### Step 1: Load and Analyze All Client Data
- Parse business intelligence files for core positioning
- Extract competitive insights from market research phases
- Analyze current account structure for optimization opportunities
- Review performance history for baseline benchmarks

### Step 2: Apply Enhanced Testing Framework
- Use the Enhanced Testing Framework as your base methodology
- Customize test priorities based on client competitive advantages
- Adapt timeline based on client budget, volume, and seasonality
- Generate specific hypotheses that exploit identified market gaps

### Step 3: Generate Custom Implementation Plan
- Create month-by-month testing roadmap
- Specify campaign structure recommendations  
- Develop creative strategy framework
- Establish measurement and optimization protocols

## 🔍 Key Files for Analysis Priority

### Must Analyze (Critical)
1. `03_business_intel/questionnaire.md` - Core business context
2. `02_market_research/claude_research/phase_outputs/phase_2_*.md` - Competitive analysis
3. `02_market_research/claude_research/phase_outputs/phase_3_*.md` - Market gaps
4. `02_market_research/claude_research/phase_outputs/phase_4_*.md` - Strategic positioning

### Should Analyze (Important)
1. `06_campaign_structure/*.md` - Current account performance
2. `05_historical_data/*` - Performance trends and benchmarks
3. `03_business_intel/ai_insights/phase_*.md` - Additional strategic insights

### May Analyze (Supplementary)
1. `04_technical_setup/*` - Technical capabilities and constraints
2. `01_brand_assets/*` - Brand guidelines and creative assets

## 🚨 Quality Standards for Output

### Research Integration Requirements
- Every test recommendation must cite specific research insights
- Competitive advantages must be proven from market analysis data
- Hypotheses must be based on identified market gaps or competitor weaknesses

### Strategic Alignment Requirements  
- All tests must support strategic positioning from Phase 4 research
- Testing priorities must align with client business goals
- Timeline must respect client constraints and capabilities

### Actionability Requirements
- Recommendations must be implementation-ready
- Success criteria must be measurable and time-bound
- Campaign structure changes must be clearly specified

---

**Ready for Claude Code Analysis**: This brief provides complete context for generating a comprehensive, client-specific testing framework that maximizes competitive advantage and performance improvement opportunities.
"""
    
    return brief

def copy_analysis_files(project_path: Path, claude_code_dir: Path):
    """
    Copy relevant analysis files to Claude Code directory
    """
    import shutil
    
    # Create organized structure
    (claude_code_dir / "business_intel").mkdir(exist_ok=True)
    (claude_code_dir / "market_research").mkdir(exist_ok=True)
    (claude_code_dir / "account_structure").mkdir(exist_ok=True)
    (claude_code_dir / "performance_data").mkdir(exist_ok=True)
    
    # Copy key files
    try:
        # Business intelligence
        questionnaire = project_path / "03_business_intel" / "questionnaire.md"
        if questionnaire.exists():
            shutil.copy(questionnaire, claude_code_dir / "business_intel" / "questionnaire.md")
        
        # AI insights
        ai_insights_path = project_path / "03_business_intel" / "ai_insights"
        if ai_insights_path.exists():
            shutil.copytree(ai_insights_path, claude_code_dir / "business_intel" / "ai_insights", dirs_exist_ok=True)
        
        # Market research
        claude_research_path = project_path / "02_market_research" / "claude_research"
        if claude_research_path.exists():
            shutil.copytree(claude_research_path, claude_code_dir / "market_research" / "claude_research", dirs_exist_ok=True)
        
        # Account structure
        campaign_structure_path = project_path / "06_campaign_structure"
        if campaign_structure_path.exists():
            for file in campaign_structure_path.glob("*.md"):
                shutil.copy(file, claude_code_dir / "account_structure" / file.name)
        
        print("📂 Analysis files copied to Claude Code directory")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not copy some files: {e}")

def generate_claude_code_prompt(client_name: str, client_brief: str) -> str:
    """
    Generate the specific prompt for Claude Code to use
    """
    prompt = f"""# Claude Code Prompt: Generate Custom Testing Framework for {client_name}

## Context
You are analyzing all available client research and account data to generate a comprehensive, customized 6-month testing framework. Use the Enhanced Testing Framework as your methodology base while adapting every element to {client_name}'s specific competitive advantages, market opportunities, and business context.

## Available Data Sources
All client analysis files are available in the `claude_code_analysis/` directory:

### Critical Analysis Files
1. `business_intel/questionnaire.md` - Core business goals and positioning
2. `business_intel/ai_insights/phase_*.md` - Strategic analysis phases
3. `market_research/claude_research/phase_outputs/` - Competitive and market analysis
4. `account_structure/*.md` - Current Google Ads and Meta account structure
5. `performance_data/` - Historical performance trends

### Reference Framework
- `Ads Testing Framework.md` - Enhanced Testing Framework methodology
- `client_analysis_brief.md` - Comprehensive client context summary

## Primary Analysis Tasks

### 1. Competitive Advantage Identification
Analyze all client research to identify {client_name}'s top 3-5 competitive advantages:

**For each advantage, determine:**
- Uniqueness vs competitors (1-10 score)
- Market relevance and customer value
- Provability in advertising campaigns
- Testing opportunity potential

**Output Format:**
```markdown
## Competitive Advantages Analysis

### Advantage 1: [Specific Advantage Name]
**Source**: [Which research file/phase identified this]
**Competitive Gap**: [How competitors are weak in this area]
**Market Evidence**: [Evidence this matters to target audience]
**Testing Hypothesis**: [Specific testable approach]
**Priority Score**: X/10
```

### 2. Market Gap Exploitation Strategy
From Phase 3 research and competitive analysis, identify high-impact market gaps:

**Extract and prioritize:**
- Underserved audience segments
- Unaddressed customer pain points
- Competitor positioning weaknesses
- Untested messaging angles or value propositions

**Convert each gap into specific testing opportunities**

### 3. Testing Hypothesis Generation
Create 10-15 specific, testable hypotheses based on your analysis:

**Hypothesis Template:**
```markdown
### Hypothesis [#]: [Descriptive Name]
**Research Basis**: [Which client data supports this hypothesis]
**Competitive Context**: [How this exploits competitor weakness]
**Client Advantage**: [Which client strength this leverages]
**Test Prediction**: [Specific performance improvement prediction]
**Implementation**: 
- Control: [Current or industry standard approach]
- Test Variant 1: [Primary test approach]
- Test Variant 2: [Alternative approach]
**Success Metrics**: [Specific KPIs and improvement targets]
**Timeline**: [Minimum test duration for statistical significance]
**Priority**: [High/Medium/Low based on impact potential]
```

### 4. 6-Month Timeline Customization
Adapt the Enhanced Testing Framework timeline to {client_name}'s specific context:

**Consider these adaptation factors:**
- Current account performance and structure
- Budget constraints and conversion volume
- Competitive intensity and market dynamics
- Seasonal patterns and business cycles
- Resource and technical capabilities

**Monthly Planning Requirements:**
```markdown
## Month [X]: [Focus Theme Based on Client Priorities]

### Strategic Objectives
- [Objective tied to competitive advantage]
- [Objective based on market gap opportunity]
- [Objective aligned with business goals]

### Priority Tests
#### Test 1: [Hypothesis Name from your library]
- **Implementation Details**: [Specific campaign setup]
- **Budget Allocation**: [% of total budget]
- **Success Criteria**: [Measurable targets]
- **Risk Mitigation**: [Backup plan if test fails]

### Expected Outcomes
- [Performance improvement predictions]
- [Competitive positioning enhancement]
- [Market share impact]
```

### 5. Campaign Structure Optimization
Based on current account structure analysis, recommend:

**Structural Changes:**
- Campaign reorganization for better testing capability
- New campaign types that exploit competitive advantages
- Audience targeting refinements based on research insights
- Bidding strategy optimizations for client goals

**Creative Strategy Framework:**
- Messaging angles that differentiate from competitors
- Visual strategies that reinforce competitive positioning
- Format testing priorities for each platform
- Landing page strategy aligned with value propositions

## Detailed Requirements

### Research Integration Standards
- **Citation Required**: Every recommendation must reference specific client research
- **Gap Connection**: Each test must connect to identified competitive gap or market opportunity
- **Advantage Leveraging**: Tests must maximize client's unique competitive advantages
- **Strategic Alignment**: All recommendations must support Phase 4 positioning strategy

### Customization Standards
- **Context Sensitivity**: Account for client's industry, audience, and business model
- **Resource Realism**: Respect budget, team, and technical constraints
- **Performance Baseline**: Use historical data to set realistic improvement targets
- **Competitive Awareness**: Plan for potential competitor responses

### Output Quality Standards
- **Actionability**: Recommendations must be implementation-ready
- **Measurability**: Success criteria must be specific and time-bound
- **Prioritization**: Clear rationale for test sequencing and budget allocation
- **Risk Management**: Contingency plans for major test scenarios

## Expected Deliverable Structure

### Executive Summary (1 page)
- Client's primary competitive advantages
- Key market opportunities identified
- Overall testing strategy and expected outcomes
- 6-month performance improvement targets

### Strategic Analysis (2-3 pages)
- Competitive advantage deep-dive analysis
- Market gap opportunity assessment
- Strategic positioning reinforcement strategy
- Competitive landscape positioning

### Testing Framework (3-4 pages)
- Complete hypothesis library (10-15 hypotheses)
- 6-month timeline with monthly focus areas
- Test prioritization matrix and rationale
- Budget allocation and resource requirements

### Implementation Guide (2-3 pages)
- Campaign structure optimization recommendations
- Creative strategy and messaging framework
- Technical setup and tracking requirements
- Team responsibilities and workflow

### Measurement & Optimization (1-2 pages)
- KPI framework aligned with client goals
- Testing methodology and statistical requirements
- Monthly review and optimization process
- Quarterly strategic assessment protocol

### Risk Management (1 page)
- Potential failure scenarios and mitigation strategies
- Competitive response preparation
- Market change adaptation protocols
- Budget protection and reallocation guidelines

## Success Validation Checklist

Before finalizing your framework, ensure:

### Completeness
- [ ] All major competitive advantages addressed with specific tests
- [ ] Market opportunities translated into actionable hypotheses
- [ ] Current account structure optimizations included
- [ ] Performance history insights incorporated
- [ ] Client goals and constraints reflected throughout

### Quality
- [ ] Each test connects to specific research insights
- [ ] Hypotheses are testable and measurable
- [ ] Timeline accounts for statistical significance
- [ ] Budget allocation is sustainable and realistic
- [ ] Expected outcomes align with client objectives

### Innovation
- [ ] Framework exploits unique competitive advantages
- [ ] Tests include approaches competitors aren't using
- [ ] Market gaps addressed with creative solutions
- [ ] Strategic positioning reinforced through execution

## Final Output Requirements

**File Name**: `{client_name}_Custom_Testing_Framework_[Date].md`

**Length**: 10-15 pages of comprehensive, actionable strategy

**Format**: Professional markdown document with clear sections, actionable recommendations, and specific implementation guidance

**Success Measure**: Framework should enable {client_name} to achieve 2-3x performance improvement through systematic exploitation of competitive advantages and market opportunities.

---

**Begin Analysis**: Start by thoroughly reviewing all available client data files, then systematically work through each analysis task to generate a comprehensive, customized testing framework that maximizes {client_name}'s competitive advantages and market opportunities.
"""
    
    return prompt

def create_instruction_summary(client_name: str, claude_code_dir: Path) -> str:
    """
    Create a quick reference summary for using Claude Code
    """
    summary_file = claude_code_dir / "INSTRUCTIONS.md"
    
    instructions = f"""# {client_name} - Claude Code Quick Start Instructions

## 🚀 Ready to Generate Custom Testing Framework

### Files Prepared for Analysis
- **Client Brief**: `client_analysis_brief.md` - Complete client context
- **Claude Prompt**: `claude_code_prompt.md` - Detailed analysis instructions
- **Reference Framework**: `../Ads Testing Framework.md` - Base methodology
- **Client Data**: Organized in subfolders for easy access

### Claude Code Execution Steps

#### 1. Initial Setup
```bash
# Ensure you're in the project directory
cd {client_name}/

# Verify Claude Code can access the analysis directory
ls claude_code_analysis/
```

#### 2. Load Context in Claude Code
Start Claude Code and provide this context:

**Primary Instruction:**
"I need you to analyze all client research data and generate a custom 6-month testing framework. Please start by reading and analyzing these files in order:

1. `claude_code_analysis/client_analysis_brief.md` - For complete client context
2. `claude_code_analysis/claude_code_prompt.md` - For detailed analysis instructions  
3. `claude_code_analysis/business_intel/` - For business goals and positioning
4. `claude_code_analysis/market_research/` - For competitive analysis and market gaps
5. `claude_code_analysis/account_structure/` - For current performance context
6. `Ads Testing Framework.md` - For base methodology reference

Then generate a comprehensive custom testing framework following the detailed requirements in the prompt file."

#### 3. Analysis Process
Claude Code will:
- Parse all client research and account data
- Identify top competitive advantages and market opportunities
- Generate 10-15 specific testing hypotheses
- Create customized 6-month implementation timeline
- Provide campaign structure and creative strategy recommendations

#### 4. Expected Output
**File**: `{client_name}_Custom_Testing_Framework_[Date].md`
**Length**: 10-15 pages of actionable strategy
**Sections**:
- Executive Summary
- Competitive Advantage Analysis  
- Testing Hypothesis Library
- 6-Month Implementation Timeline
- Campaign Strategy Recommendations
- Measurement Framework
- Risk Management Plan

### Quality Validation
Before implementing, verify the framework includes:
- [ ] Specific competitive advantages identified from research
- [ ] Market gaps translated into testable hypotheses
- [ ] Timeline adapted to client's context and constraints
- [ ] Campaign recommendations based on account structure analysis
- [ ] Success metrics aligned with client business goals

### Next Steps After Framework Generation
1. **Review and Validate**: Check framework against client research
2. **Refine if Needed**: Ask Claude Code to adjust specific sections
3. **Implementation Planning**: Begin campaign setup based on Month 1 recommendations
4. **Team Alignment**: Share framework with campaign management team
5. **Tracking Setup**: Implement measurement framework before campaign launch

### Troubleshooting
**If Claude Code can't access files:**
- Verify file paths are correct
- Check that all analysis files were copied properly
- Ensure Claude Code has permission to read the directory

**If output lacks client specificity:**
- Emphasize the requirement to cite specific research insights
- Ask for more detailed competitive advantage analysis
- Request specific examples from the client's market research

**If timeline seems generic:**
- Provide additional context about client's budget and volume
- Emphasize adaptation to client's industry and seasonality
- Request more specific monthly implementation details

## 📞 Support
If you need assistance with Claude Code integration or framework customization, review the Enhanced Testing Framework methodology or refer back to the detailed prompt instructions.

---
**Integration Ready**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
    
    with open(summary_file, 'w') as f:
        f.write(instructions)
    
    return str(summary_file)

def main():
    """
    Main function for Claude Code integration setup
    """
    parser = argparse.ArgumentParser(description='Prepare client data for Claude Code analysis')
    parser.add_argument('client_name', help='Name of the client')
    parser.add_argument('--project-path', help='Path to client project directory', default=None)
    parser.add_argument('--copy-framework', action='store_true', help='Copy enhanced testing framework to project')
    
    args = parser.parse_args()
    
    # Setup Claude Code integration
    claude_code_dir = setup_claude_code_integration(args.client_name, args.project_path)
    
    # Copy enhanced framework if requested
    if args.copy_framework:
        framework_source = Path("Ads Testing Framework.md")
        if framework_source.exists():
            import shutil
            framework_dest = Path(claude_code_dir).parent / "Enhanced_Testing_Framework.md"
            shutil.copy(framework_source, framework_dest)
            print(f"📋 Enhanced Testing Framework copied to: {framework_dest}")
    
    print(f"\n🎯 {args.client_name} is ready for Claude Code analysis!")
    print(f"💡 Use the files in {claude_code_dir} to generate a custom testing framework")

if __name__ == "__main__":
    main()