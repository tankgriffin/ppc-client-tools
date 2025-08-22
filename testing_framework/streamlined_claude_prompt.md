# Claude Code Prompt: Generate Focused Testing Framework

## Context
Analyze client research and generate a focused 4-5 page testing framework. No extensive analysis - just actionable testing strategy.

## Required Output Format

### Executive Summary (1 page)
```markdown
# [Client Name] - Custom 6-Month Testing Framework

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