# Claude Code Prompt: Generate Focused Testing Framework for reality_events

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
# reality_events - Custom 6-Month Testing Framework

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

**Begin Analysis**: Start by thoroughly reviewing all available client data files, then systematically work through each analysis task to generate a focused, customized testing framework that maximizes reality_events's competitive advantages and market opportunities.
