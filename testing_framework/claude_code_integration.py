#!/usr/bin/env python3
"""
Updated Claude Code Integration Script
Works with client_projects/ongoing_clients/ structure
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
    Supports both flat structure and client_projects/ongoing_clients/ structure
    """
    
    # Determine the correct project path
    if project_path:
        project_path = Path(project_path)
    else:
        # Try different possible locations
        possible_paths = [
            Path(f"./client_projects/ongoing_clients/{client_name}"),
            Path(f"./client_projects/{client_name}"),
            Path(f"./{client_name}"),
            Path(f"./ongoing_clients/{client_name}")
        ]
        
        project_path = None
        for path in possible_paths:
            if path.exists():
                project_path = path
                break
        
        if not project_path:
            print(f"❌ Could not find client directory for '{client_name}'")
            print("🔍 Checked these locations:")
            for path in possible_paths:
                print(f"   - {path}")
            print(f"\n💡 Try running: ./setup_client.sh \"{client_name}\"")
            print(f"💡 Or specify path: --project-path \"./path/to/{client_name}\"")
            return None
    
    print(f"🚀 Setting up Claude Code integration for {client_name}")
    print(f"📁 Using project path: {project_path}")
    
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
This brief contains all client research, account structure analysis, and strategic insights needed to generate a custom 6-month testing framework using the Ultra-Streamlined Testing Framework methodology.

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
3. **Generate 8-12 Testable Hypotheses** based on competitive advantages and market gaps
4. **Create Customized 6-Month Testing Timeline** adapted to client context
5. **Develop Implementation Strategy** for maximum competitive advantage

### Key Analysis Questions to Answer
1. What are {client_name}'s unique competitive advantages vs competitors?
2. Which market gaps offer the highest-impact testing opportunities?
3. How should the testing timeline be adapted for {client_name}'s specific context?
4. What campaign structure optimizations will maximize performance?
5. Which creative strategies will best exploit competitive positioning?

### Expected Deliverables
- Strategic advantage analysis and prioritization (3-5 advantages)
- Testing hypothesis library (8-12 hypotheses)
- Testing priority matrix with monthly assignments
- Implementation recommendations

## 📋 Framework Integration Instructions

### Step 1: Load and Analyze All Client Data
- Parse business intelligence files for core positioning
- Extract competitive insights from market research phases
- Analyze current account structure for optimization opportunities
- Review performance history for baseline benchmarks

### Step 2: Apply Ultra-Streamlined Testing Framework
- Use the Ultra-Streamlined Testing Framework as your base methodology
- Customize test priorities based on client competitive advantages
- Adapt timeline based on client budget, volume, and seasonality
- Generate specific hypotheses that exploit identified market gaps

### Step 3: Generate Focused Implementation Plan
- Create testing priority matrix with impact scores
- Specify top tests for months 1-6
- Develop brief implementation recommendations
- Establish success metrics aligned with client goals

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

## 🚨 Output Requirements

### Must Generate 4-5 Page Framework Including:
1. **Executive Summary** (1 page)
   - 3-5 competitive advantages with priority scores
   - Key market opportunities
   - 6-month performance targets

2. **Testing Hypothesis Library** (2-3 pages)
   - 8-12 specific hypotheses with implementation details
   - Research basis for each test
   - Priority scores and timeline

3. **Testing Priority Matrix** (1 page)
   - Clear testing sequence
   - Impact scores and monthly assignments

### Quality Standards
- Every test recommendation must cite specific research insights
- Competitive advantages must be proven from market analysis data
- Hypotheses must be based on identified market gaps or competitor weaknesses
- Implementation must be ready for immediate execution

---

**Ready for Claude Code Analysis**: This brief provides complete context for generating a focused, client-specific testing framework that maximizes competitive advantage and performance improvement opportunities.
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
        
        # Performance data
        historical_path = project_path / "05_historical_data"
        if historical_path.exists():
            for file in historical_path.glob("*"):
                if file.is_file():
                    shutil.copy(file, claude_code_dir / "performance_data" / file.name)
        
        print("📂 Analysis files copied to Claude Code directory")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not copy some files: {e}")

def generate_claude_code_prompt(client_name: str, client_brief: str) -> str:
    """
    Generate the specific prompt for Claude Code to use
    """
    prompt = f"""# Claude Code Prompt: Generate Focused Testing Framework for {client_name}

## Context
Analyze client research and generate a focused 4-5 page testing framework. No extensive analysis - just actionable testing strategy using the Ultra-Streamlined Testing Framework methodology.

## Available Data Sources
All client analysis files are available in the `claude_code_analysis/` directory:

### Critical Analysis Files
1. `business_intel/questionnaire.md` - Core business goals and positioning
2. `business_intel/ai_insights/phase_*.md` - Strategic analysis phases
3. `market_research/claude_research/phase_outputs/` - Competitive and market analysis
4. `account_structure/*.md` - Current Google Ads and Meta account structure
5. `performance_data/` - Historical performance trends

### Reference Framework
- `../testing_framework/ultra_streamlined_framework.md` - Base testing methodology
- `client_analysis_brief.md` - Comprehensive client context summary

## Required Output Format

### Executive Summary (1 page)
```markdown
# {client_name} - Custom 6-Month Testing Framework

**Generated**: [Date]
**Client**: [Business description]

## Primary Competitive Advantages
1. **[Advantage]** - [Description] (Priority: X/10)
2. **[Advantage]** - [Description] (Priority: X/10)  
3. **[Advantage]** - [Description] (Priority: X/10)

## Key Market Opportunities
- **[Gap 1]** - [Description]
- **[Gap 2]** - [Description]

## 6-Month Performance Targets
- **[KPI 1]**: [Target]
- **[KPI 2]**: [Target]
```

### Testing Hypotheses (2-3 pages)
Generate **8-12 hypotheses** using this exact format:

```markdown
#### Hypothesis [#]: [Test Name]
**Research Basis**: [Client data that supports this]
**Competitive Context**: [How competitors are weak here]
**Client Advantage**: [Unique strength this leverages]
**Test Prediction**: [Specific improvement expected]
**Implementation**:
- Control: [Current approach]
- Test Variant 1: [Primary test]
- Test Variant 2: [Alternative test]
**Success Metrics**: [Specific targets]
**Timeline**: [Duration]
**Priority**: High/Medium/Low (X/10)
```

### Priority Matrix (1 page)
```markdown
| Test Category | Impact Score | Priority | Month |
|---------------|--------------|----------|--------|
| [Test Name] | X/10 | HIGH | 1 |
```

## Analysis Instructions

### Step 1: Extract Key Insights
From client files, identify:
- **3-5 competitive advantages** with priority scores
- **3-5 market gaps** competitors miss
- **Current performance issues** needing solutions

### Step 2: Generate Hypotheses
Create **8-12 specific tests** that:
- Exploit competitive advantages
- Address market gaps  
- Fix performance issues
- Include exact implementation details

### Step 3: Prioritize and Schedule
Score each test (1-10) and assign to months 1-6

## Critical Requirements

### Must Include:
- ✅ Specific research citations for every test
- ✅ Exact implementation approach (control vs variants)
- ✅ Measurable success criteria
- ✅ Priority scores and timeline

### Must NOT Include:
- ❌ Extended background analysis
- ❌ Detailed competitive assessments
- ❌ Risk management sections
- ❌ Month-by-month implementation plans
- ❌ Success validation frameworks

**Target**: 4-5 pages maximum of pure testing strategy

---

**Begin Analysis**: Start by thoroughly reviewing all available client data files, then systematically work through each analysis task to generate a focused, customized testing framework that maximizes {client_name}'s competitive advantages and market opportunities.
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
- **Reference Framework**: `../testing_framework/ultra_streamlined_framework.md` - Base methodology
- **Client Data**: Organized in subfolders for easy access

### Claude Code Execution Steps

#### 1. Initial Setup
```bash
# Navigate to the Claude Code analysis directory
cd {claude_code_dir}

# Verify files are accessible
ls -la
```

#### 2. Load Context in Claude Code
Start Claude Code and provide this context:

**Primary Instruction:**
"I need you to analyze all client research data and generate a custom 6-month testing framework. Please start by reading and analyzing these files in order:

1. `client_analysis_brief.md` - For complete client context
2. `claude_code_prompt.md` - For detailed analysis instructions  
3. `business_intel/` - For business goals and positioning
4. `market_research/` - For competitive analysis and market gaps
5. `account_structure/` - For current performance context
6. `../testing_framework/ultra_streamlined_framework.md` - For base methodology reference

Then generate a focused 4-5 page testing framework following the detailed requirements in the prompt file."

#### 3. Expected Output
**File**: `{client_name}_Custom_Testing_Framework_[Date].md`
**Length**: 4-5 pages of actionable strategy
**Sections**:
- Executive Summary (1 page)
- Testing Hypothesis Library (2-3 pages)
- Testing Priority Matrix (1 page)

### Quality Validation
Before implementing, verify the framework includes:
- [ ] 3-5 competitive advantages identified from research
- [ ] 8-12 testable hypotheses with implementation details
- [ ] Priority matrix with monthly assignments
- [ ] Success metrics aligned with client business goals

### Next Steps After Framework Generation
1. **Export Documents**: Use the document export system to create Word/PDF versions
2. **Implementation Planning**: Begin campaign setup based on highest priority tests
3. **Team Alignment**: Share framework with campaign management team

### Export to Professional Documents
```bash
# Navigate back to main directory
cd ../../..

# Export the generated framework to Word and HTML
python3 fixed_simple_converter.py "{client_name}" "{claude_code_dir}/{client_name}_Custom_Testing_Framework_[Date].md"
```

## 📞 Next Steps
1. Generate framework using Claude Code
2. Export to professional documents
3. Begin implementation of Month 1 tests
4. Set up tracking and measurement systems

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
    parser.add_argument('--copy-framework', action='store_true', help='Copy ultra-streamlined testing framework to project')
    
    args = parser.parse_args()
    
    # Setup Claude Code integration
    claude_code_dir = setup_claude_code_integration(args.client_name, args.project_path)
    
    if not claude_code_dir:
        return  # Error already reported
    
    # Copy framework if requested
    if args.copy_framework:
        framework_source = Path("testing_framework/ultra_streamlined_framework.md")
        if framework_source.exists():
            import shutil
            framework_dest = Path(claude_code_dir).parent / "Ultra_Streamlined_Testing_Framework.md"
            shutil.copy(framework_source, framework_dest)
            print(f"📋 Ultra-Streamlined Testing Framework copied to: {framework_dest}")
        else:
            print(f"⚠️  Framework file not found: {framework_source}")
    
    print(f"\n🎯 {args.client_name} is ready for Claude Code analysis!")
    print(f"💡 Use the files in {claude_code_dir} to generate a custom testing framework")

if __name__ == "__main__":
    main()