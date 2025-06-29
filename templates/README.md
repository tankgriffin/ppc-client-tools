# Template Files Directory

This directory contains template files used by the Enhanced PPC Client Tools for generating customized prompts and outputs.

## Template Types

### Prompt Templates
- **Business Intelligence**: Templates for Phase 1 business analysis prompts
- **Competitive Analysis**: Templates for Phase 2 competitive landscape prompts  
- **Market Gap Analysis**: Templates for Phase 3 market opportunity prompts
- **Strategic Positioning**: Templates for Phase 4 positioning strategy prompts
- **Campaign Strategy**: Templates for Phase 5 implementation strategy prompts

### Output Templates
- **Integration Summary**: Template for final research integration
- **Strategic Insights**: Template for compiled strategic analysis
- **Implementation Roadmap**: Template for campaign implementation planning

## Template Engine

The tools use Jinja2 templating engine for dynamic content generation:
- Variables: `{{ variable_name }}`
- Conditionals: `{% if condition %} ... {% endif %}`
- Loops: `{% for item in list %} ... {% endfor %}`
- Comments: `{# This is a comment #}`

## Custom Templates

You can create custom templates by:
1. Adding new `.md` or `.txt` files to this directory
2. Using Jinja2 syntax for dynamic content
3. Referencing templates in the prompt generator

## Template Variables

Common variables available in templates:
- `business_name`: Client business name
- `industry`: Business industry/sector  
- `description`: Business description
- `services`: Services offered
- `target_audience`: Target audience description
- `competitors`: List of competitors
- `primary_goal`: Campaign primary goal
- `budget_range`: Budget range
- `location`: Business location
- `unique_value`: Unique value proposition

## Usage

Templates are automatically loaded and processed by the prompt generator when creating customized Claude AI research prompts.