#!/usr/bin/env python3
"""
Research Orchestrator
Coordinates between different research tools and manages data flow
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
except ImportError:
    console = None

class ResearchOrchestrator:
    """Main controller that coordinates all research tools and data flow"""
    
    def __init__(self, client_name):
        self.client_name = client_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.console = console
        
        # Find client folder
        self.folder_name = self.find_client_folder(client_name)
        if not self.folder_name:
            raise ValueError(f"Client folder not found for: {client_name}")
        
        # Research results storage
        self.research_results = {
            'technical_analysis': None,
            'claude_research': None,
            'competitor_analysis': None,
            'integrated_insights': None
        }
        
        # Workflow status
        self.workflow_status = {
            'technical_setup': False,
            'claude_research': False,
            'competitor_analysis': False,
            'integration_complete': False
        }

    def find_client_folder(self, client_name):
        """Find existing client folder"""
        sanitized = client_name.lower().replace(' ', '_')
        variations = [sanitized, client_name.replace(' ', '_'), client_name.replace(' ', '-')]
        
        for variation in variations:
            if os.path.exists(variation):
                return variation
        return None

    def print_header(self, text):
        """Print formatted header"""
        if self.console:
            self.console.print(Panel(text, style="bold blue"))
        else:
            print(f"\n{'='*70}")
            print(f"🎯 {text}")
            print('='*70)

    def print_info(self, text):
        """Print formatted info"""
        if self.console:
            self.console.print(text, style="cyan")
        else:
            print(f"💡 {text}")

    def print_success(self, text):
        """Print formatted success"""
        if self.console:
            self.console.print(text, style="green")
        else:
            print(f"✅ {text}")

    def print_warning(self, text):
        """Print formatted warning"""
        if self.console:
            self.console.print(text, style="yellow")
        else:
            print(f"⚠️  {text}")

    def run_technical_analysis(self, website_url=None):
        """Run website technical analysis"""
        self.print_header("🔧 Technical Analysis Phase")
        
        if not website_url:
            website_url = input("Enter website URL for technical analysis: ")
        
        if not website_url:
            self.print_warning("Skipping technical analysis - no website URL provided")
            return False
        
        try:
            # Run verify_tracking.js
            self.print_info(f"Analyzing {website_url}...")
            
            result = subprocess.run(
                ['node', 'verify_tracking.js', website_url],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Save technical analysis results
                analysis_path = f"{self.folder_name}/04_technical_setup/tracking_verification/technical_analysis_{self.timestamp}.md"
                os.makedirs(os.path.dirname(analysis_path), exist_ok=True)
                
                with open(analysis_path, 'w', encoding='utf-8') as f:
                    f.write(f"# Technical Analysis Results - {self.client_name}\n\n")
                    f.write(f"**Website**: {website_url}\n")
                    f.write(f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("## Technical Analysis Output\n\n")
                    f.write("```\n")
                    f.write(result.stdout)
                    f.write("\n```\n")
                
                self.research_results['technical_analysis'] = {
                    'website_url': website_url,
                    'analysis_file': analysis_path,
                    'output': result.stdout
                }
                
                self.workflow_status['technical_setup'] = True
                self.print_success("Technical analysis completed successfully")
                return True
            else:
                self.print_warning(f"Technical analysis failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_warning("Technical analysis timed out")
            return False
        except FileNotFoundError:
            self.print_warning("verify_tracking.js not found - skipping technical analysis")
            return False
        except Exception as e:
            self.print_warning(f"Technical analysis error: {str(e)}")
            return False

    def run_claude_research(self):
        """Run Claude AI research setup"""
        self.print_header("🧠 Claude AI Research Phase")
        
        try:
            # Check if Claude research already exists
            claude_dir = f"{self.folder_name}/02_market_research/claude_research"
            if os.path.exists(f"{claude_dir}/00_project_context.md"):
                self.print_info("Claude research setup already exists")
                if self.console:
                    from rich.prompt import Confirm
                    overwrite = Confirm.ask("Do you want to run Claude research setup again?")
                else:
                    overwrite = input("Claude research setup exists. Run again? (y/n): ").lower() == 'y'
                
                if not overwrite:
                    self.workflow_status['claude_research'] = True
                    return True
            
            # Run claude_research_setup.py
            self.print_info("Running Claude AI research setup...")
            
            result = subprocess.run(
                ['python3', 'claude_research_setup.py', self.client_name],
                capture_output=True,
                text=True
                # No timeout - wait indefinitely for user input
            )
            
            if result.returncode == 0:
                self.research_results['claude_research'] = {
                    'setup_complete': True,
                    'research_dir': claude_dir,
                    'output': result.stdout
                }
                
                self.workflow_status['claude_research'] = True
                self.print_success("Claude AI research setup completed")
                self.print_info("Next: Execute the generated prompts in Claude AI")
                return True
            else:
                self.print_warning(f"Claude research setup failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_warning("Claude research setup timed out")
            return False
        except FileNotFoundError:
            self.print_warning("claude_research_setup.py not found")
            return False
        except Exception as e:
            self.print_warning(f"Claude research setup error: {str(e)}")
            return False

    def run_competitor_analysis(self):
        """Run traditional competitor analysis (optional)"""
        self.print_header("🔍 Traditional Competitor Analysis Phase")
        
        # Check if user wants to run traditional analysis
        if self.console:
            from rich.prompt import Confirm
            run_traditional = Confirm.ask("Run traditional competitor analysis? (Recommended if Claude research is not complete)")
        else:
            run_traditional = input("Run traditional competitor analysis? (y/n): ").lower() == 'y'
        
        if not run_traditional:
            self.print_info("Skipping traditional competitor analysis")
            return True
        
        try:
            # Run competitor_research.py
            self.print_info("Running traditional competitor analysis...")
            
            result = subprocess.run(
                ['python3', 'competitor_research.py', self.client_name],
                capture_output=True,
                text=True,
                timeout=900  # 15 minutes timeout
            )
            
            if result.returncode == 0:
                self.research_results['competitor_analysis'] = {
                    'analysis_complete': True,
                    'output': result.stdout
                }
                
                self.workflow_status['competitor_analysis'] = True
                self.print_success("Traditional competitor analysis completed")
                return True
            else:
                self.print_warning(f"Competitor analysis failed: {result.stderr}")
                # Don't fail the whole workflow for this
                return True
                
        except subprocess.TimeoutExpired:
            self.print_warning("Competitor analysis timed out")
            return True
        except FileNotFoundError:
            self.print_warning("competitor_research.py not found - skipping")
            return True
        except Exception as e:
            self.print_warning(f"Competitor analysis error: {str(e)}")
            return True

    def generate_integrated_summary(self):
        """Generate integrated summary of all research"""
        self.print_header("📊 Generating Integrated Research Summary")
        
        summary_content = f"""# {self.client_name} - Integrated Research Summary

## Research Overview
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Research Orchestrator**: {self.timestamp}

## Research Components Completed

### Technical Analysis
"""
        
        if self.workflow_status['technical_setup']:
            summary_content += f"""✅ **Completed**: Website technical analysis
- Analysis File: {self.research_results['technical_analysis']['analysis_file']}
- Website: {self.research_results['technical_analysis']['website_url']}
- Key technical insights extracted

"""
        else:
            summary_content += "❌ **Not Completed**: Technical analysis\n\n"

        summary_content += "### Claude AI Research\n"
        if self.workflow_status['claude_research']:
            summary_content += f"""✅ **Completed**: Claude AI research setup
- Research Directory: {self.research_results['claude_research']['research_dir']}
- 5-phase strategic analysis framework created
- Customized prompts generated for business intelligence

**Next Steps for Claude Research**:
1. Open Claude AI (claude.ai)
2. Execute Phase 1 prompt: phase1_business_intelligence_prompt.md
3. Continue through all 5 phases sequentially
4. Save outputs in phase_outputs/ folder

"""
        else:
            summary_content += "❌ **Not Completed**: Claude AI research setup\n\n"

        summary_content += "### Traditional Competitor Analysis\n"
        if self.workflow_status['competitor_analysis']:
            summary_content += "✅ **Completed**: Traditional competitor analysis\n"
            summary_content += "- Detailed competitor data extracted\n"
            summary_content += "- Market insights and opportunities identified\n\n"
        else:
            summary_content += "❌ **Not Completed**: Traditional competitor analysis\n\n"

        summary_content += f"""## Strategic Research Workflow Status

### Immediate Next Steps
1. **Complete Claude AI Research** (High Priority)
   - Execute all 5 research phases in Claude
   - Document insights in phase_outputs folder
   - Extract strategic positioning and campaign strategies

2. **Technical Implementation** (Medium Priority)
   - Address any technical issues identified
   - Implement tracking improvements
   - Optimize website for PPC readiness

3. **Campaign Development** (High Priority)
   - Use Claude research insights for campaign strategy
   - Develop keyword targeting based on research
   - Create ad copy using strategic positioning insights

### Expected Outcomes
- **Strategic Intelligence**: Comprehensive market and competitive intelligence
- **Campaign Strategy**: Data-driven PPC campaign strategy
- **Competitive Advantage**: Unique positioning and differentiation strategy
- **Implementation Roadmap**: Clear action plan for campaign execution

### Quality Metrics
- Research Completeness: {sum(self.workflow_status.values())}/4 components completed
- Strategic Depth: {"High" if self.workflow_status['claude_research'] else "Medium"}
- Technical Readiness: {"Ready" if self.workflow_status['technical_setup'] else "Needs Review"}

## File Locations
- **Main Project**: {self.folder_name}/
- **Claude Research**: {self.folder_name}/02_market_research/claude_research/
- **Technical Analysis**: {self.folder_name}/04_technical_setup/tracking_verification/
- **Business Intelligence**: {self.folder_name}/03_business_intel/
- **Integration Summary**: {self.folder_name}/research_integration_summary_{self.timestamp}.md

## Research Investment
- **Setup Time**: ~30 minutes (automated)
- **Claude Execution**: ~2-3 hours (strategic analysis)
- **Implementation Planning**: ~1-2 hours
- **Total Research Value**: Professional-grade strategic intelligence

## Success Criteria
- [ ] All technical issues identified and prioritized
- [ ] Claude AI research phases completed
- [ ] Strategic positioning defined
- [ ] Campaign implementation strategy documented
- [ ] Competitive advantages identified and documented

---
*Generated by Research Orchestrator v2.0*
*Next Update: Execute Claude research phases*
"""

        # Save integrated summary
        summary_path = f"{self.folder_name}/research_integration_summary_{self.timestamp}.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        self.research_results['integrated_insights'] = {
            'summary_file': summary_path,
            'workflow_completion': sum(self.workflow_status.values()) / len(self.workflow_status)
        }
        
        self.workflow_status['integration_complete'] = True
        self.print_success(f"Integrated research summary created: {summary_path}")
        return True

    def display_workflow_status(self):
        """Display current workflow status"""
        if self.console:
            table = Table(title="Research Workflow Status")
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Priority", style="yellow")
            
            components = [
                ("Technical Analysis", "✅ Complete" if self.workflow_status['technical_setup'] else "❌ Pending", "Medium"),
                ("Claude AI Research", "✅ Complete" if self.workflow_status['claude_research'] else "❌ Pending", "High"),
                ("Competitor Analysis", "✅ Complete" if self.workflow_status['competitor_analysis'] else "❌ Skipped", "Low"),
                ("Integration Summary", "✅ Complete" if self.workflow_status['integration_complete'] else "❌ Pending", "Medium")
            ]
            
            for component, status, priority in components:
                table.add_row(component, status, priority)
            
            self.console.print(table)
        else:
            print("\n📊 Research Workflow Status:")
            print(f"  Technical Analysis: {'✅' if self.workflow_status['technical_setup'] else '❌'}")
            print(f"  Claude AI Research: {'✅' if self.workflow_status['claude_research'] else '❌'}")
            print(f"  Competitor Analysis: {'✅' if self.workflow_status['competitor_analysis'] else '❌'}")
            print(f"  Integration Summary: {'✅' if self.workflow_status['integration_complete'] else '❌'}")

    def run_complete_workflow(self, website_url=None, skip_competitor=False):
        """Execute the complete research workflow"""
        self.print_header(f"🚀 Complete Research Workflow for {self.client_name}")
        
        workflow_success = True
        
        try:
            # Phase 1: Technical Analysis
            self.print_info("Phase 1/4: Technical Analysis")
            if not self.run_technical_analysis(website_url):
                workflow_success = False
            
            # Phase 2: Claude AI Research
            self.print_info("Phase 2/4: Claude AI Research Setup")
            if not self.run_claude_research():
                workflow_success = False
            
            # Phase 3: Traditional Competitor Analysis (optional)
            if not skip_competitor:
                self.print_info("Phase 3/4: Traditional Competitor Analysis")
                if not self.run_competitor_analysis():
                    workflow_success = False
            else:
                self.print_info("Phase 3/4: Skipping traditional competitor analysis")
            
            # Phase 4: Integration and Summary
            self.print_info("Phase 4/4: Generating Integration Summary")
            if not self.generate_integrated_summary():
                workflow_success = False
            
            # Display final status
            self.display_workflow_status()
            
            if workflow_success:
                self.print_success("🎉 Complete research workflow finished successfully!")
                self.print_info("📁 Check all outputs in the client folder")
                self.print_info("🧠 Next: Execute Claude AI research phases")
            else:
                self.print_warning("⚠️  Workflow completed with some issues")
                self.print_info("📋 Check the integration summary for details")
            
            return workflow_success
            
        except Exception as e:
            self.print_warning(f"Workflow error: {str(e)}")
            return False

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python3 research_orchestrator.py 'Client Name' [website_url]")
        sys.exit(1)
    
    client_name = sys.argv[1]
    website_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        orchestrator = ResearchOrchestrator(client_name)
        success = orchestrator.run_complete_workflow(website_url)
        
        if success:
            print(f"\n🎯 Research orchestration completed for {client_name}")
            print(f"📁 Results: {orchestrator.folder_name}/")
        else:
            print(f"\n❌ Research orchestration completed with issues")
            sys.exit(1)
            
    except ValueError as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure you've run './setup_client.sh \"Client Name\"' first")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()