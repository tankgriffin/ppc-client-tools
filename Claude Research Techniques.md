# Product Requirements Document: Claude AI Research Integration

## 📋 Overview

**Product Name**: Claude AI Research Integration for PPC Client Tools
**Version**: 2.0
**Date**: December 29, 2024
**Status**: Ready for Implementation

## 🎯 Objective

Replace the existing `competitor_research.py` script with an advanced AI-powered research system that integrates with Claude to provide comprehensive market intelligence, competitive analysis, and strategic insights for PPC campaigns.

## 📊 Current State Analysis

### Existing Tools to Replace/Enhance:
1. **competitor_research.py** - Replace with Claude AI integration
2. **Parts of GUIDE.md** - Update workflow to include Claude research
3. **setup_client.sh questionnaire** - Enhance with AI-powered business intelligence

### Tools to Keep:
1. **verify_tracking.js** - Keep as-is (technical analysis)
2. **setup_client.sh** - Enhance folder structure for Claude outputs
3. **requirements.txt** - Update dependencies

## 🚀 Feature Requirements

### Core Feature 1: Interactive Research Setup Script
**File**: `claude_research_setup.py`

**Purpose**: Replace manual competitor research with AI-guided intelligence gathering

**Functionality**:
- Interactive CLI that collects business information
- Generates customized Claude prompts automatically
- Creates structured research project folders
- Integrates with existing client folder structure from `setup_client.sh`

**Key Improvements Over Current System**:
- **AI-Powered**: Uses Claude's knowledge vs manual website scraping
- **Strategic Focus**: Goes beyond technical analysis to strategic insights
- **Customized Prompts**: No more generic templates - everything personalized
- **Comprehensive**: 5-phase research process vs single competitive analysis

### Core Feature 2: Claude Prompt Generator Engine
**File**: `prompt_generator.py`

**Purpose**: Dynamic prompt generation system for different research phases

**Functionality**:
- Template engine for research prompts
- Business context injection
- Phase-specific prompt customization
- Output formatting for Claude consumption

### Core Feature 3: Enhanced Project Structure
**Modification**: Update `setup_client.sh`

**New Folder Structure**:
```
client_name/
├── 01_brand_assets/
├── 02_market_research/
│   ├── claude_research/           # NEW
│   │   ├── 00_project_context.md
│   │   ├── phase_outputs/
│   │   └── strategic_insights.md
│   ├── competitor_analysis/       # ENHANCED
│   └── market_intelligence/       # NEW
├── 03_business_intel/
│   ├── ai_generated_insights.md   # NEW
│   └── questionnaire.md           # ENHANCED
├── 04_technical_setup/
├── 05_historical_data/
├── 06_campaign_structure/
├── 07_compliance/
└── 08_reporting/
```

### Core Feature 4: Integrated Workflow Orchestration
**File**: `research_orchestrator.py`

**Purpose**: Main controller that runs the complete research workflow

**Functionality**:
- Coordinates between different research phases
- Manages data flow between tools
- Generates executive summaries
- Creates actionable next steps

## 📋 Detailed Implementation Requirements

### 1. Replace `competitor_research.py`

**Current Issues with competitor_research.py**:
- Limited to technical website analysis
- Requires BeautifulSoup scraping (can be blocked)
- Manual competitor identification
- Basic insights without strategic depth
- No integration with AI for analysis

**New `claude_research_setup.py` Requirements**:

```python
# Core Functions Required:
def collect_business_intelligence():
    """Interactive CLI to gather business context"""
    # Replaces manual questionnaire filling
    # Collects: business description, industry, target audience, competitors, goals
    
def generate_claude_prompts():
    """Create customized research prompts"""
    # Phase 1: Business Intelligence Analysis
    # Phase 2: Competitive Landscape Mapping  
    # Phase 3: Market Gap Identification
    # Phase 4: Strategic Positioning Development
    # Phase 5: Content & Campaign Strategy
    
def create_research_project():
    """Set up complete research project structure"""
    # Integrates with existing setup_client.sh folder structure
    # Creates Claude-ready prompt files
    # Generates README and instructions
    
def export_for_claude():
    """Format outputs for Claude consumption"""
    # Creates markdown files ready for Claude
    # Includes context preservation between phases
    # Generates sequential prompt workflow
```

### 2. Enhance `setup_client.sh`

**Required Modifications**:

```bash
# Add new folders for Claude research
mkdir -p "$FOLDER_NAME/02_market_research/claude_research"
mkdir -p "$FOLDER_NAME/02_market_research/claude_research/phase_outputs"
mkdir -p "$FOLDER_NAME/03_business_intel/ai_insights"

# Update questionnaire template to work with AI
# Add Claude research workflow to project README
# Include instructions for research orchestration
```

**New Template Files to Generate**:
- `claude_research_workflow.md` - Step-by-step Claude research process
- `ai_insights_template.md` - Template for capturing Claude outputs
- `strategic_summary_template.md` - Executive summary format

### 3. Update `GUIDE.md`

**Sections to Replace**:

**Current Step 3: Enhanced Competitor Research** 
Replace with:
**Step 3: AI-Powered Strategic Research**

**Current Manual Process** (15-20 minutes):
- Manual Facebook Ad Library research
- Manual Google Ads research  
- Basic website analysis

**New AI Process** (10 minutes setup + Claude analysis):
- Automated prompt generation
- 5-phase comprehensive research
- Strategic insights and recommendations
- Actionable next steps

**Updated Workflow Section**:
```markdown
### Step 3: AI-Powered Strategic Research
Time: 10 minutes setup + Claude analysis

```bash
# Run the new Claude research setup
python3 claude_research_setup.py "Client Name"

# This will:
# 1. Collect business intelligence interactively
# 2. Generate customized Claude prompts
# 3. Create complete research project
# 4. Output instructions for Claude execution
```

**What this generates:**
- 5 comprehensive research phases
- Customized prompts with no placeholders
- Strategic insights beyond basic competitor analysis
- Content strategy recommendations
- Campaign positioning suggestions
```

### 4. Create New Main Orchestrator

**File**: `main_research_workflow.py`

**Purpose**: Single command to run complete enhanced workflow

```python
#!/usr/bin/env python3
"""
Enhanced PPC Client Research Workflow
Combines technical analysis with AI-powered strategic insights
"""

def run_complete_workflow(client_name):
    """Execute the full enhanced research workflow"""
    
    # Phase 1: Technical Setup (existing tools)
    print("🔧 Phase 1: Technical Analysis")
    subprocess.run(['./setup_client.sh', client_name])
    
    # Phase 2: Website Technical Verification (existing)
    print("🔍 Phase 2: Technical Verification")
    website_url = input("Enter website URL for technical analysis: ")
    subprocess.run(['node', 'verify_tracking.js', website_url])
    
    # Phase 3: AI-Powered Strategic Research (NEW)
    print("🧠 Phase 3: AI Strategic Research")
    subprocess.run(['python3', 'claude_research_setup.py', client_name])
    
    # Phase 4: Integration & Summary (NEW)
    print("📊 Phase 4: Generating Final Strategy")
    generate_integrated_summary(client_name)
    
    print("✅ Complete workflow finished!")
    print(f"📁 Check outputs in: {client_name}/")
```

## 🎯 User Experience Flow

### Current UX Issues:
1. Multiple separate tools requiring manual coordination
2. Generic templates requiring manual customization
3. Limited strategic insights
4. No AI integration for analysis

### New Enhanced UX:

```bash
# Single command to run everything
python3 main_research_workflow.py "Acme Corporation"

# Interactive prompts guide user through:
# 1. Business context collection
# 2. Technical analysis
# 3. AI research setup
# 4. Claude execution instructions
# 5. Final strategy compilation
```

**User Journey**:
1. **Input**: Business name + basic context
2. **Automated Setup**: Technical analysis + AI prompt generation  
3. **Claude Execution**: Copy/paste prompts into Claude
4. **Strategic Output**: Comprehensive research + actionable strategy

## 📊 Technical Specifications

### Dependencies to Add
Update `requirements.txt`:
```
# Existing
requests>=2.25.1
beautifulsoup4>=4.9.3
lxml>=4.6.3
urllib3>=1.26.5
certifi>=2021.5.25

# New additions
click>=8.0.0          # For improved CLI
jinja2>=3.0.0         # For prompt templating
pyyaml>=6.0.0         # For configuration management
rich>=13.0.0          # For better terminal output
```

### File Structure Changes

**New Files to Create**:
- `claude_research_setup.py` - Main interactive setup
- `prompt_generator.py` - Prompt templating engine
- `research_orchestrator.py` - Workflow coordination
- `main_research_workflow.py` - Single entry point
- `templates/` - Folder for prompt templates
- `config/research_config.yaml` - Configuration settings

**Files to Modify**:
- `setup_client.sh` - Add Claude research folders
- `GUIDE.md` - Update workflow documentation
- `README.md` - Update tool descriptions
- `package.json` - Add new script commands

**Files to Keep Unchanged**:
- `verify_tracking.js` - Technical analysis works well
- Core folder structure logic in `setup_client.sh`

## 📋 Success Criteria

### Functional Requirements:
- [ ] Single command launches complete workflow
- [ ] AI prompts generated without manual customization
- [ ] Integration with existing client folder structure
- [ ] Strategic insights beyond current technical analysis
- [ ] Clear instructions for Claude execution
- [ ] Professional output formatting

### Performance Requirements:
- [ ] Setup completes in under 5 minutes
- [ ] Generates 5 comprehensive research phases
- [ ] Works with any business type/industry
- [ ] Handles edge cases (missing info, etc.)

### Quality Requirements:
- [ ] Prompts require no manual editing
- [ ] Strategic insights are actionable
- [ ] Workflow is intuitive for non-technical users
- [ ] Documentation is comprehensive
- [ ] Error handling is robust

## 🚀 Implementation Phases

### Phase 1: Core Development (Week 1)
- [ ] Create `claude_research_setup.py`
- [ ] Build prompt generation engine
- [ ] Update `setup_client.sh` for new folders
- [ ] Test with sample business data

### Phase 2: Integration (Week 2)  
- [ ] Create main workflow orchestrator
- [ ] Update documentation and guides
- [ ] Add error handling and validation
- [ ] Create template system

### Phase 3: Enhancement (Week 3)
- [ ] Add advanced configuration options
- [ ] Improve CLI interface with Rich
- [ ] Add export options for different formats
- [ ] Performance optimization

### Phase 4: Documentation & Testing (Week 4)
- [ ] Complete documentation overhaul
- [ ] Create video tutorials
- [ ] Test with multiple business types
- [ ] Prepare for release

## 🎯 Claude Code Implementation Instructions

### Primary Tasks for Claude Code:

1. **Analyze Current Codebase**
   - Review existing `competitor_research.py` functionality
   - Understand `setup_client.sh` folder structure
   - Map current workflow dependencies

2. **Implement Core Research Setup Script**
   - Create interactive CLI for business data collection
   - Build prompt generation engine with templates
   - Integrate with existing client folder structure
   - Add proper error handling and validation

3. **Update Existing Tools**
   - Modify `setup_client.sh` to include Claude research folders
   - Update `GUIDE.md` with new workflow steps
   - Enhance documentation throughout

4. **Create Workflow Orchestration**
   - Build main workflow script that coordinates all tools
   - Add CLI improvements with better UX
   - Create summary generation functionality

5. **Quality Assurance**
   - Add comprehensive error handling
   - Create unit tests for core functions
   - Validate output formatting
   - Test with multiple business scenarios

### Output Requirements:
- **Working Scripts**: All Python files executable and tested
- **Updated Documentation**: Clear instructions for new workflow
- **Integration**: Seamless integration with existing tools
- **Professional Output**: Well-formatted, actionable research materials

This PRD provides the complete specification for transforming your current PPC client tools into an AI-powered strategic research platform that leverages Claude's capabilities while maintaining the technical analysis strengths of your existing toolkit.