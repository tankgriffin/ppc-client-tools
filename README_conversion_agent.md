# AI Conversion Optimization Agent

An intelligent agent that analyzes websites using a comprehensive 25-point Conversion Rate Optimization (CRO) framework and 11-point SEO optimization checklist, then generates detailed PDF reports with actionable recommendations.

## Features

### CRO Analysis (25 Points)
- **Headline Analysis**: 4-U Formula evaluation (Useful, Unique, Urgent, Ultra-specific)
- **Value Proposition**: Above-fold content assessment
- **CTA Analysis**: Call-to-action psychology and placement
- **Form Analysis**: Field count optimization (5-field maximum rule)
- **Social Proof**: Testimonials and trust element detection
- **Trust Signals**: Security badges and guarantee clustering
- **Mobile Optimization**: Thumb zone and responsive design
- **Content Structure**: Readability and benefit-focused language

### SEO Analysis (11 Sections)
- **Meta Tags**: Title and description optimization
- **URL Structure**: Length and keyword inclusion
- **Images**: Alt text and compression analysis
- **Internal Links**: Structure and anchor text
- **Headings**: H1-H6 hierarchy and keyword usage
- **Content Quality**: Word count and keyword placement
- **Schema Markup**: Structured data implementation

## Installation

1. Install required packages:
```bash
pip3 install -r requirements.txt
```

2. Make the script executable:
```bash
chmod +x conversion_optimization_agent.py
```

## Usage

### Interactive Mode
```bash
python3 conversion_optimization_agent.py
```

The agent will:
1. Prompt you for a website URL (with automatic typo correction)
2. Scrape and analyze the website (with multiple fallback strategies)
3. Run comprehensive CRO and SEO analysis
4. Generate a detailed PDF report with recommendations

### Smart URL Correction
The agent automatically fixes common URL typos:
- `ttps://example.com` → `https://example.com`
- `htps://example.com` → `https://example.com` 
- `https//example.com` → `https://example.com`
- `www.https://example.com` → `https://www.example.com`
- And many more common mistakes!

### Example Output
```
🚀 Conversion Optimization Agent Started
==================================================

Please enter the website URL to analyze: ttps://example.com
🔧 Auto-corrected URL: ttps://example.com → https://example.com
✅ URL set: https://example.com

🔍 Analyzing website: https://example.com
✅ Website content retrieved successfully

📊 Running CRO Analysis...
🔍 Running SEO Analysis...

✅ PDF report generated: conversion_optimization_report_20250812_215628.pdf
✅ Analysis complete! Report saved as: conversion_optimization_report_20250812_215628.pdf

📋 Summary of findings:
• 4 high priority issues identified
• 10 optimization opportunities found

Review the PDF report for detailed analysis and implementation roadmap.
```

## Report Structure

The generated PDF includes:

### Executive Summary
- Overview of analysis scope
- Key findings summary
- Priority issue count

### High Priority Issues
- Critical problems affecting conversions
- SEO issues impacting rankings
- Mobile optimization problems

### Medium Priority Recommendations
- CRO improvement opportunities
- Content optimization suggestions
- Technical SEO enhancements

### Detailed Analysis
- Section-by-section breakdown
- Specific issues and recommendations
- Best practice guidelines

### Implementation Roadmap
- Week 1-2: Critical fixes
- Week 3-4: CRO improvements
- Week 5-8: Content & SEO
- Ongoing: Testing & optimization

## Framework Based On

### CRO Framework (25 Points)
1. Headline 4-U Formula
2. Above-Fold Value Proposition
3. CTA First-Person Psychology
4. 5-Field Form Maximum
5. Message Match Precision
6. Social Proof Near CTAs
7. Cognitive Bias Stack
8. PAS Copy Framework
9. Genuine Urgency Only
10. Price Anchoring Display
11. Trust Signal Clustering
12. Visual Hierarchy F-Pattern
13. Lead Magnet Hierarchy
14. Objection Preemption
15. Mobile Thumb Zone
16. One-Variable Testing
17. Post-Conversion Momentum
18. Cart Recovery Sequence
19. Reading Level Grade 6
20. TOFU/MOFU/BOFU Logic
21. White Space = Focus
22. Benefit-First Language
23. Micro-Commitment Ladder
24. Performance Tracking Stack
25. Weekly Optimisation Ritual

### SEO Framework (11 Sections)
1. URLs (length, structure, keywords)
2. Meta Titles and Descriptions
3. Images & Alt Text
4. Internal Links
5. External Links
6. Page Speed
7. Content Quality
8. Conversion Rate Optimisation Elements
9. Mobile Optimisation
10. Headings Structure
11. Schema Markup

## Technical Details

- **Language**: Python 3.7+
- **Dependencies**: requests, beautifulsoup4, reportlab, lxml
- **Output Format**: PDF report
- **Analysis Time**: 30-60 seconds per website
- **Report Size**: Typically 5-10 pages

## Demo Test

Run the demo test to verify installation:
```bash
python3 demo_test.py
```

## Files

- `conversion_optimization_agent.py` - Main agent script
- `demo_test.py` - Demo test script
- `requirements.txt` - Python dependencies
- `Conversion Optimization Framework.md` - Source framework document

## Troubleshooting

### Common Issues

1. **SSL Certificate Errors**
   - Some websites may have SSL issues
   - The agent includes fallback handling

2. **Rate Limiting**
   - Some sites may block automated requests
   - The agent uses appropriate headers

3. **JavaScript-Heavy Sites**
   - Static scraping may miss dynamic content
   - Results focus on HTML-based analysis

4. **PDF Generation Errors**
   - Ensure reportlab is properly installed
   - Check file permissions in current directory

## Contributing

To extend the framework:

1. Add new analysis functions to the respective `analyze_*` methods
2. Update the recommendation generation logic
3. Modify the PDF template for additional sections

## License

This tool is built for conversion optimization and SEO analysis purposes. Use responsibly and respect website terms of service.