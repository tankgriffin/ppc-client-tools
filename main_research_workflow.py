#!/usr/bin/env python3
"""
Enhanced PPC Client Research Workflow
Single command to run complete enhanced workflow combining technical analysis with AI-powered strategic insights
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    console = Console()
except ImportError:
    console = None

class MainResearchWorkflow:
    """Single entry point for the complete enhanced research workflow"""
    
    def __init__(self):
        self.console = console
        self.start_time = datetime.now()
        
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

    def print_step(self, step_num, total_steps, description):
        """Print formatted step"""
        if self.console:
            self.console.print(f"[bold cyan]Phase {step_num}/{total_steps}:[/bold cyan] {description}")
        else:
            print(f"\n📊 Phase {step_num}/{total_steps}: {description}")
            print('-'*50)

    def check_prerequisites(self):
        """Check if all required tools and dependencies are available"""
        self.print_header("🔍 Checking Prerequisites")
        
        missing_tools = []
        
        # Check Python scripts
        required_scripts = [
            'setup_client.sh',
            'claude_research_setup.py',
            'research_orchestrator.py',
            'verify_tracking.js'
        ]
        
        for script in required_scripts:
            if not os.path.exists(script):
                missing_tools.append(script)
        
        # Check Python dependencies
        try:
            import click, jinja2, yaml
        except ImportError as e:
            missing_tools.append(f"Python packages: {str(e)}")
        
        # Check Node.js for verify_tracking.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, timeout=5)
            if result.returncode != 0:
                missing_tools.append("Node.js")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            missing_tools.append("Node.js")
        
        if missing_tools:
            self.print_warning("Missing required tools:")
            for tool in missing_tools:
                print(f"  ❌ {tool}")
            return False
        else:
            self.print_success("All prerequisites satisfied")
            return True

    def run_technical_setup(self, client_name):
        """Phase 1: Technical Setup"""
        self.print_step(1, 4, "Technical Analysis")
        
        try:
            # Run setup_client.sh
            self.print_info("Creating client project structure...")
            result = subprocess.run(['./setup_client.sh', client_name], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.print_success("Client project structure created")
                return True
            else:
                self.print_warning(f"Project setup failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_warning("Project setup timed out")
            return False
        except Exception as e:
            self.print_warning(f"Project setup error: {str(e)}")
            return False

    def run_website_verification(self, website_url):
        """Phase 2: Website Technical Verification"""
        self.print_step(2, 4, "Website Technical Verification")
        
        if not website_url:
            self.print_warning("No website URL provided - skipping technical verification")
            return True
        
        try:
            self.print_info(f"Analyzing website: {website_url}")
            result = subprocess.run(['node', 'verify_tracking.js', website_url], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.print_success("Website technical verification completed")
                return True
            else:
                self.print_warning(f"Website verification failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_warning("Website verification timed out")
            return False
        except Exception as e:
            self.print_warning(f"Website verification error: {str(e)}")
            return False

    def run_ai_strategic_research(self, client_name):
        """Phase 3: AI-Powered Strategic Research"""
        self.print_step(3, 4, "AI-Powered Strategic Research")
        
        try:
            self.print_info("Running Claude AI research setup...")
            self.print_info("This will ask you interactive questions about the business...")
            
            # Run without capturing output so user can see and respond to prompts
            result = subprocess.run(['python3', 'claude_research_setup.py', client_name], 
                                  timeout=600)  # Increased timeout to 10 minutes
            
            if result.returncode == 0:
                self.print_success("Claude AI research setup completed")
                self.print_info("📝 Next: Execute the generated prompts in Claude AI")
                return True
            else:
                self.print_warning("Claude research setup failed")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_warning("Claude research setup timed out")
            return False
        except Exception as e:
            self.print_warning(f"Claude research setup error: {str(e)}")
            return False

    def run_integration_summary(self, client_name):
        """Phase 4: Integration & Summary Generation"""
        self.print_step(4, 4, "Generating Final Strategy")
        
        try:
            self.print_info("Generating integrated research summary...")
            result = subprocess.run(['python3', 'research_orchestrator.py', client_name], 
                                  timeout=60)
            
            if result.returncode == 0:
                self.print_success("Integration summary completed")
                return True
            else:
                self.print_warning("Integration failed")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_warning("Integration summary timed out")
            return False
        except Exception as e:
            self.print_warning(f"Integration error: {str(e)}")
            return False

    def display_next_steps(self, client_name):
        """Display next steps for the user"""
        client_folder = client_name.lower().replace(' ', '_')
        
        if self.console:
            next_steps_panel = f"""[bold green]🎉 Enhanced Workflow Complete![/bold green]

[bold cyan]📁 Your Research Package:[/bold cyan]
• Project folder: {client_folder}/
• Claude research: {client_folder}/02_market_research/claude_research/
• Technical analysis: {client_folder}/04_technical_setup/
• Business intelligence: {client_folder}/03_business_intel/

[bold yellow]🧠 Immediate Next Steps:[/bold yellow]
1. Open Claude AI (claude.ai)
2. Navigate to: {client_folder}/02_market_research/claude_research/
3. Start with: CLAUDE_RESEARCH_SUMMARY.md
4. Execute Phase 1 prompt: phase1_business_intelligence_prompt.md
5. Continue through all 5 phases sequentially

[bold magenta]📊 What You'll Get:[/bold magenta]
• Market position analysis
• Competitive landscape mapping
• Strategic positioning strategy
• Content & campaign implementation plan
• Professional-grade strategic intelligence

[bold blue]⏰ Time Investment:[/bold blue]
• Claude execution: 2-3 hours
• Campaign setup: 1-2 hours
• Expected ROI: 30-40% better performance vs traditional approach"""
            
            self.console.print(Panel(next_steps_panel, title="Success!", style="green"))
        else:
            print(f"\n🎉 Enhanced Workflow Complete!")
            print(f"\n📁 Your Research Package:")
            print(f"  • Project folder: {client_folder}/")
            print(f"  • Claude research: {client_folder}/02_market_research/claude_research/")
            print(f"  • Technical analysis: {client_folder}/04_technical_setup/")
            print(f"  • Business intelligence: {client_folder}/03_business_intel/")
            print(f"\n🧠 Immediate Next Steps:")
            print(f"  1. Open Claude AI (claude.ai)")
            print(f"  2. Navigate to: {client_folder}/02_market_research/claude_research/")
            print(f"  3. Start with: CLAUDE_RESEARCH_SUMMARY.md")
            print(f"  4. Execute Phase 1 prompt: phase1_business_intelligence_prompt.md")
            print(f"  5. Continue through all 5 phases sequentially")
            print(f"\n📊 What You'll Get:")
            print(f"  • Market position analysis")
            print(f"  • Competitive landscape mapping") 
            print(f"  • Strategic positioning strategy")
            print(f"  • Content & campaign implementation plan")
            print(f"  • Professional-grade strategic intelligence")

    def run_complete_workflow(self, client_name, website_url=None):
        """Execute the complete enhanced workflow"""
        self.print_header(f"🚀 Enhanced PPC Research Workflow for {client_name}")
        
        # Track workflow success
        workflow_results = {
            'technical_setup': False,
            'website_verification': False,
            'ai_research': False,
            'integration': False
        }
        
        # Phase 1: Technical Setup
        workflow_results['technical_setup'] = self.run_technical_setup(client_name)
        
        # Phase 2: Website Technical Verification
        if website_url:
            workflow_results['website_verification'] = self.run_website_verification(website_url)
        else:
            workflow_results['website_verification'] = True  # Skip if no URL
        
        # Phase 3: AI-Powered Strategic Research
        workflow_results['ai_research'] = self.run_ai_strategic_research(client_name)
        
        # Phase 4: Integration & Summary
        workflow_results['integration'] = self.run_integration_summary(client_name)
        
        # Calculate workflow success
        total_phases = len(workflow_results)
        successful_phases = sum(workflow_results.values())
        success_rate = successful_phases / total_phases
        
        # Display results
        if success_rate >= 0.75:  # 75% success rate threshold
            self.display_next_steps(client_name)
            elapsed_time = datetime.now() - self.start_time
            self.print_success(f"Workflow completed in {elapsed_time.seconds // 60} minutes")
            return True
        else:
            self.print_warning(f"Workflow completed with issues ({successful_phases}/{total_phases} phases successful)")
            self.print_info("Check individual phase outputs for details")
            return False

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Enhanced PPC Client Research Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main_research_workflow.py "Acme Corporation"
  python3 main_research_workflow.py "Reality Events" --website https://realityevents.com.au
  python3 main_research_workflow.py "My Business" --check-only
        """
    )
    
    parser.add_argument('client_name', help='Client or business name')
    parser.add_argument('--website', help='Website URL for technical analysis')
    parser.add_argument('--check-only', action='store_true', help='Only check prerequisites')
    parser.add_argument('--skip-website', action='store_true', help='Skip website verification')
    
    args = parser.parse_args()
    
    # Create workflow instance
    workflow = MainResearchWorkflow()
    
    # Check prerequisites
    if not workflow.check_prerequisites():
        print("\n❌ Prerequisites check failed")
        print("Please install missing dependencies and try again")
        sys.exit(1)
    
    if args.check_only:
        print("\n✅ All prerequisites satisfied - ready to run workflow")
        sys.exit(0)
    
    # Get website URL if not provided
    website_url = args.website
    if not website_url and not args.skip_website:
        if console:
            website_url = Prompt.ask("Enter website URL for technical analysis (optional)", default="")
        else:
            website_url = input("Enter website URL for technical analysis (optional): ")
        
        if not website_url:
            website_url = None
    
    # Run the complete workflow
    try:
        success = workflow.run_complete_workflow(args.client_name, website_url)
        
        if success:
            print(f"\n🎯 Enhanced research workflow completed successfully!")
            print(f"📧 Ready for strategic intelligence gathering and campaign implementation")
        else:
            print(f"\n⚠️  Workflow completed with some issues")
            print(f"📋 Check individual outputs for details")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()