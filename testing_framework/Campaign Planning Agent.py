#!/usr/bin/env python3
"""
Enhanced Campaign Planning Agent for Claude Code Integration
Analyzes client research and current account structure to generate custom testing frameworks
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import yaml
from pathlib import Path

class CampaignPlanningAgent:
    def __init__(self, client_name: str, config_path: str = "config.yaml"):
        self.client_name = client_name
        self.config = self._load_config(config_path)
        self.project_path = Path(f"./{client_name}")
        self.analysis_data = {}
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration if config file not found"""
        return {
            'testing_framework': {
                'phases': 6,
                'min_test_duration_days': 7,
                'confidence_level': 0.95,
                'budget_allocation': {
                    'testing': 0.25,
                    'proven_winners': 0.75
                }
            },
            'platforms': ['google_ads', 'meta_ads'],
            'test_priorities': [
                'product_service_selection',
                'offer_optimization', 
                'ad_format_placement',
                'creative_strategy',
                'headlines',
                'descriptions',
                'ad_extensions'
            ]
        }
    
    def analyze_client_data(self) -> Dict[str, Any]:
        """Analyze all client research and account data"""
        print(f"🔍 Analyzing client data for {self.client_name}...")
        
        analysis = {
            'business_intel': self._load_business_intel(),
            'competitive_analysis': self._load_competitive_analysis(), 
            'current_account_structure': self._analyze_current_accounts(),
            'performance_history': self._load_performance_data(),
            'market_insights': self._load_market_insights()
        }
        
        self.analysis_data = analysis
        return analysis
    
    def _load_business_intel(self) -> Dict:
        """Load business intelligence from questionnaire and AI research"""
        intel_path = self.project_path / "03_business_intel"
        ai_insights_path = self.project_path / "03_business_intel" / "ai_insights"
        
        business_intel = {}
        
        # Load questionnaire data
        questionnaire_file = intel_path / "questionnaire.md"
        if questionnaire_file.exists():
            business_intel['questionnaire'] = self._parse_questionnaire(questionnaire_file)
        
        # Load AI research insights
        if ai_insights_path.exists():
            for phase_file in ai_insights_path.glob("phase_*.md"):
                phase_name = phase_file.stem
                with open(phase_file, 'r') as f:
                    business_intel[phase_name] = f.read()
        
        return business_intel
    
    def _load_competitive_analysis(self) -> Dict:
        """Load competitive analysis and market research"""
        market_research_path = self.project_path / "02_market_research"
        
        competitive_data = {}
        
        # Load Claude research outputs
        claude_outputs_path = market_research_path / "claude_research" / "phase_outputs"
        if claude_outputs_path.exists():
            for output_file in claude_outputs_path.glob("*.md"):
                with open(output_file, 'r') as f:
                    competitive_data[output_file.stem] = f.read()
        
        # Load traditional competitor research
        competitor_files = market_research_path.glob("competitor_*.json")
        for comp_file in competitor_files:
            with open(comp_file, 'r') as f:
                competitive_data[comp_file.stem] = json.load(f)
        
        return competitive_data
    
    def _analyze_current_accounts(self) -> Dict:
        """Analyze current Google Ads and Meta account structure"""
        campaign_structure_path = self.project_path / "06_campaign_structure"
        
        account_structure = {
            'google_ads': {},
            'meta_ads': {},
            'analysis_date': datetime.now().isoformat()
        }
        
        # Load Google Ads structure
        google_structure_file = campaign_structure_path / "google_ads_structure.md"
        if google_structure_file.exists():
            account_structure['google_ads'] = self._parse_campaign_structure(google_structure_file)
        
        # Load Meta structure  
        meta_structure_file = campaign_structure_path / "meta_ads_structure.md"
        if meta_structure_file.exists():
            account_structure['meta_ads'] = self._parse_campaign_structure(meta_structure_file)
        
        return account_structure
    
    def _load_performance_data(self) -> Dict:
        """Load historical performance data"""
        historical_path = self.project_path / "05_historical_data"
        
        performance_data = {}
        
        # Load any CSV or JSON performance files
        for data_file in historical_path.glob("*.csv"):
            performance_data[data_file.stem] = str(data_file)
            
        for data_file in historical_path.glob("*.json"):
            with open(data_file, 'r') as f:
                performance_data[data_file.stem] = json.load(f)
        
        return performance_data
    
    def _load_market_insights(self) -> Dict:
        """Load market intelligence and insights"""
        market_intel_path = self.project_path / "02_market_research" / "market_intelligence"
        
        insights = {}
        
        if market_intel_path.exists():
            for insight_file in market_intel_path.glob("*.md"):
                with open(insight_file, 'r') as f:
                    insights[insight_file.stem] = f.read()
        
        return insights
    
    def generate_testing_framework(self) -> Dict[str, Any]:
        """Generate customized 6-month testing framework"""
        print(f"🧪 Generating custom testing framework for {self.client_name}...")
        
        framework = {
            'client': self.client_name,
            'generated_date': datetime.now().isoformat(),
            'framework_period': '6_months',
            'strategic_foundation': self._extract_strategic_foundation(),
            'testing_priorities': self._prioritize_tests(),
            'monthly_plans': self._generate_monthly_plans(),
            'campaign_concepts': self._generate_campaign_concepts(),
            'creative_strategies': self._generate_creative_strategies(),
            'competitive_angles': self._generate_competitive_angles(),
            'measurement_framework': self._generate_measurement_framework()
        }
        
        return framework
    
    def _extract_strategic_foundation(self) -> Dict:
        """Extract key strategic elements from analysis"""
        foundation = {
            'business_positioning': '',
            'target_audiences': [],
            'unique_value_props': [],
            'primary_goals': [],
            'budget_considerations': {},
            'competitive_advantages': []
        }
        
        # Extract from business intel
        if 'questionnaire' in self.analysis_data.get('business_intel', {}):
            questionnaire = self.analysis_data['business_intel']['questionnaire']
            foundation.update({
                'business_positioning': questionnaire.get('business_description', ''),
                'target_audiences': [questionnaire.get('target_audience', '')],
                'primary_goals': [questionnaire.get('primary_goal', '')]
            })
        
        # Extract from AI research phases
        for phase_key, phase_content in self.analysis_data.get('business_intel', {}).items():
            if phase_key.startswith('phase_') and isinstance(phase_content, str):
                # Extract key insights from each phase
                if 'positioning' in phase_content.lower():
                    foundation['business_positioning'] += f"\n{phase_content[:500]}"
        
        return foundation
    
    def _prioritize_tests(self) -> List[Dict]:
        """Prioritize tests based on client data and potential impact"""
        test_priorities = []
        
        # Base test priority framework
        base_priorities = [
            {
                'category': 'Tier 1 - Maximum Impact',
                'tests': [
                    {
                        'name': 'Product/Service Selection',
                        'impact_potential': 'High',
                        'timeline': 'Weeks 3-4',
                        'description': 'Test which products/services to advertise based on margins and demand'
                    },
                    {
                        'name': 'Offer Optimization',
                        'impact_potential': 'Very High', 
                        'timeline': 'Weeks 5-8',
                        'description': 'Test different value propositions, guarantees, and urgency tactics'
                    }
                ]
            },
            {
                'category': 'Tier 2 - High Impact',
                'tests': [
                    {
                        'name': 'Platform & Format Testing',
                        'impact_potential': 'High',
                        'timeline': 'Weeks 9-12',
                        'description': 'Test Google Search vs Display vs Meta platforms'
                    },
                    {
                        'name': 'Creative Strategy',
                        'impact_potential': 'High',
                        'timeline': 'Weeks 13-16', 
                        'description': 'Test video vs image, different messaging angles'
                    }
                ]
            }
        ]
        
        # Customize based on client analysis
        for tier in base_priorities:
            for test in tier['tests']:
                # Add client-specific customizations
                test['client_specific_notes'] = self._get_client_specific_test_notes(test['name'])
                test['estimated_budget'] = self._estimate_test_budget(test['name'])
                
            test_priorities.append(tier)
        
        return test_priorities
    
    def _generate_monthly_plans(self) -> Dict[str, Dict]:
        """Generate detailed monthly testing plans"""
        monthly_plans = {}
        
        months = ['month_1', 'month_2', 'month_3', 'month_4', 'month_5', 'month_6']
        
        for i, month in enumerate(months):
            monthly_plans[month] = {
                'month_number': i + 1,
                'focus_areas': self._get_month_focus(i + 1),
                'specific_tests': self._get_month_tests(i + 1),
                'budget_allocation': self._get_month_budget(i + 1),
                'success_metrics': self._get_month_metrics(i + 1),
                'deliverables': self._get_month_deliverables(i + 1)
            }
        
        return monthly_plans
    
    def _generate_campaign_concepts(self) -> List[Dict]:
        """Generate specific campaign concepts based on client analysis"""
        concepts = []
        
        # Generate concepts based on competitive analysis
        if 'competitive_analysis' in self.analysis_data:
            concepts.extend(self._competitive_based_concepts())
        
        # Generate concepts based on market gaps
        concepts.extend(self._market_gap_concepts())
        
        # Generate concepts based on unique positioning
        concepts.extend(self._positioning_based_concepts())
        
        return concepts
    
    def _generate_creative_strategies(self) -> Dict[str, List]:
        """Generate creative testing strategies"""
        return {
            'video_strategies': [
                'Test 15-second vs 30-second vs 60-second videos',
                'Problem/solution narrative vs product demo',
                'Customer testimonial vs founder story',
                'Animated vs live-action'
            ],
            'image_strategies': [
                'Product-focused vs lifestyle imagery',
                'Before/after comparison tests',
                'Infographic vs photography',
                'Single product vs multiple products'
            ],
            'copy_strategies': [
                'Benefit-focused vs feature-focused headlines',
                'Question vs statement formats',
                'Urgency vs scarcity messaging',
                'First person vs second person voice'
            ],
            'landing_page_strategies': [
                'Single-page vs multi-step forms',
                'Video hero vs image hero',
                'Social proof placement tests',
                'CTA button color and text variations'
            ]
        }
    
    def _generate_competitive_angles(self) -> List[Dict]:
        """Generate competitive advantage angles"""
        angles = []
        
        # Base competitive angles
        base_angles = [
            {
                'angle': 'Speed/Convenience',
                'description': 'Emphasize faster delivery, easier process, or more convenient service',
                'implementation': 'Test headlines focusing on time savings and convenience'
            },
            {
                'angle': 'Quality/Premium',
                'description': 'Position as higher quality alternative to competitors',
                'implementation': 'Test premium positioning with quality guarantees'
            },
            {
                'angle': 'Value/Price',
                'description': 'Emphasize better value or competitive pricing',
                'implementation': 'Test price comparison and value proposition messaging'
            },
            {
                'angle': 'Expertise/Authority',
                'description': 'Highlight superior knowledge, experience, or credentials',
                'implementation': 'Test authority-based messaging and social proof'
            }
        ]
        
        # Customize based on competitive analysis
        for angle in base_angles:
            angle['client_application'] = self._apply_angle_to_client(angle)
            angles.append(angle)
        
        return angles
    
    def _generate_measurement_framework(self) -> Dict:
        """Generate measurement and optimization framework"""
        return {
            'primary_kpis': [
                'Return on Ad Spend (ROAS)',
                'Cost Per Acquisition (CPA)', 
                'Conversion Rate',
                'Click-Through Rate (CTR)'
            ],
            'testing_metrics': [
                'Statistical significance (95% confidence)',
                'Sample size adequacy',
                'Test duration compliance',
                'Win rate percentage'
            ],
            'attribution_setup': {
                'recommended_tool': 'Hyros or similar attribution platform',
                'backup_tracking': 'Google Analytics 4 + platform pixels',
                'cross_platform_tracking': 'Unified customer journey tracking'
            },
            'reporting_cadence': {
                'daily': 'Performance monitoring and budget adjustments',
                'weekly': 'Test result evaluation and optimization',
                'monthly': 'Strategic review and planning next tests'
            }
        }
    
    def save_framework(self, framework: Dict) -> str:
        """Save the generated framework to file"""
        output_path = self.project_path / "testing_framework_custom.json"
        
        with open(output_path, 'w') as f:
            json.dump(framework, f, indent=2)
        
        # Also save markdown version
        md_output_path = self.project_path / "testing_framework_custom.md"
        self._save_framework_markdown(framework, md_output_path)
        
        print(f"✅ Custom testing framework saved to:")
        print(f"   JSON: {output_path}")
        print(f"   Markdown: {md_output_path}")
        
        return str(output_path)
    
    def _save_framework_markdown(self, framework: Dict, output_path: Path):
        """Save framework as formatted markdown"""
        with open(output_path, 'w') as f:
            f.write(f"# {self.client_name} - Custom 6-Month Testing Framework\n\n")
            f.write(f"Generated: {framework['generated_date']}\n\n")
            
            # Strategic Foundation
            f.write("## Strategic Foundation\n\n")
            foundation = framework['strategic_foundation']
            f.write(f"**Business Positioning:** {foundation.get('business_positioning', 'Not specified')}\n\n")
            f.write(f"**Target Audiences:** {', '.join(foundation.get('target_audiences', []))}\n\n")
            f.write(f"**Primary Goals:** {', '.join(foundation.get('primary_goals', []))}\n\n")
            
            # Testing Priorities
            f.write("## Testing Priorities\n\n")
            for tier in framework['testing_priorities']:
                f.write(f"### {tier['category']}\n\n")
                for test in tier['tests']:
                    f.write(f"#### {test['name']}\n")
                    f.write(f"- **Impact Potential:** {test['impact_potential']}\n")
                    f.write(f"- **Timeline:** {test['timeline']}\n")
                    f.write(f"- **Description:** {test['description']}\n")
                    if 'client_specific_notes' in test:
                        f.write(f"- **Client Notes:** {test['client_specific_notes']}\n")
                    f.write("\n")
            
            # Monthly Plans
            f.write("## 6-Month Implementation Timeline\n\n")
            for month_key, month_data in framework['monthly_plans'].items():
                f.write(f"### Month {month_data['month_number']}\n")
                f.write(f"**Focus Areas:** {', '.join(month_data['focus_areas'])}\n\n")
                f.write("**Specific Tests:**\n")
                for test in month_data['specific_tests']:
                    f.write(f"- {test}\n")
                f.write("\n")
    
    # Helper methods for data parsing and analysis
    def _parse_questionnaire(self, file_path: Path) -> Dict:
        """Parse questionnaire markdown file"""
        # Implementation for parsing questionnaire format
        return {}
    
    def _parse_campaign_structure(self, file_path: Path) -> Dict:
        """Parse campaign structure markdown"""
        # Implementation for parsing campaign structure
        return {}
    
    def _get_client_specific_test_notes(self, test_name: str) -> str:
        """Generate client-specific notes for tests"""
        return f"Custom considerations for {self.client_name} based on analysis"
    
    def _estimate_test_budget(self, test_name: str) -> str:
        """Estimate budget requirements for test"""
        return "TBD based on total budget allocation"
    
    def _get_month_focus(self, month_num: int) -> List[str]:
        """Get focus areas for specific month"""
        focus_map = {
            1: ['Foundation Setup', 'Baseline Measurement'],
            2: ['Product/Service Testing', 'Offer Optimization'],
            3: ['Platform Testing', 'Creative Strategy'],
            4: ['Creative Refinement', 'Audience Optimization'],
            5: ['Scale Testing', 'Advanced Optimization'],
            6: ['Performance Analysis', 'Next Phase Planning']
        }
        return focus_map.get(month_num, ['General Optimization'])
    
    def _get_month_tests(self, month_num: int) -> List[str]:
        """Get specific tests for month"""
        return [f"Month {month_num} specific test based on client analysis"]
    
    def _get_month_budget(self, month_num: int) -> Dict:
        """Get budget allocation for month"""
        return {'testing': '25%', 'proven_campaigns': '75%'}
    
    def _get_month_metrics(self, month_num: int) -> List[str]:
        """Get success metrics for month"""
        return ['ROAS improvement', 'CPA reduction', 'Conversion rate increase']
    
    def _get_month_deliverables(self, month_num: int) -> List[str]:
        """Get deliverables for month"""
        return [f"Month {month_num} deliverables based on focus areas"]
    
    def _competitive_based_concepts(self) -> List[Dict]:
        """Generate concepts based on competitive analysis"""
        return []
    
    def _market_gap_concepts(self) -> List[Dict]:
        """Generate concepts based on market gaps"""
        return []
    
    def _positioning_based_concepts(self) -> List[Dict]:
        """Generate concepts based on positioning"""
        return []
    
    def _apply_angle_to_client(self, angle: Dict) -> str:
        """Apply competitive angle to specific client"""
        return f"Client-specific application of {angle['angle']} strategy"

def main():
    """Main execution function"""
    if len(sys.argv) != 2:
        print("Usage: python campaign_planning_agent.py \"Client Name\"")
        sys.exit(1)
    
    client_name = sys.argv[1]
    
    # Initialize agent
    agent = CampaignPlanningAgent(client_name)
    
    # Analyze client data
    analysis = agent.analyze_client_data()
    
    # Generate testing framework
    framework = agent.generate_testing_framework()
    
    # Save framework
    output_path = agent.save_framework(framework)
    
    print(f"\n🎯 Custom testing framework generated for {client_name}")
    print(f"📁 Framework saved to: {output_path}")
    print(f"\n🚀 Ready for Claude Code integration!")
    print(f"💡 Use this framework to guide campaign planning and optimization")

if __name__ == "__main__":
    main()