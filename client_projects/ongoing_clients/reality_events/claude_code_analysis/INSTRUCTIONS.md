# reality_events - Claude Code Quick Start Instructions

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
cd client_projects/ongoing_clients/reality_events/claude_code_analysis

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
**File**: `reality_events_Custom_Testing_Framework_[Date].md`
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
python3 fixed_simple_converter.py "reality_events" "client_projects/ongoing_clients/reality_events/claude_code_analysis/reality_events_Custom_Testing_Framework_[Date].md"
```

## 📞 Next Steps
1. Generate framework using Claude Code
2. Export to professional documents
3. Begin implementation of Month 1 tests
4. Set up tracking and measurement systems

---
**Integration Ready**: 2025-08-06 13:08
