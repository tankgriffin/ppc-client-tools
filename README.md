PPC Client Setup Tools
A comprehensive toolkit for collecting and analyzing PPC client data using only free tools and resources.

🚀 Quick Start
Prerequisites
Node.js 14+ (for tracking verification)
Python 3.7+ (for competitor research)
Bash shell (Linux/Mac/WSL)
Installation
Clone or download these files to your project directory
Install Python dependencies:
bash
pip3 install -r requirements.txt
Make scripts executable:
bash
chmod +x setup_client.sh
📁 Tools Overview
1. Client Setup Script (setup_client.sh)
Automatically creates a complete folder structure and templates for new PPC clients.

Usage:

bash
./setup_client.sh "Client Name"
What it creates:

Organized folder structure for all client assets
Pre-filled template files for data collection
Business intelligence questionnaire
Technical setup checklists
Campaign structure templates
2. Tracking Verification (verify_tracking.js)
Analyzes any website to detect tracking codes, technical SEO issues, and PPC readiness.

Usage:

bash
node verify_tracking.js https://example.com
What it checks:

✅ Google Analytics 4
✅ Google Ads conversion tracking
✅ Facebook Pixel
✅ LinkedIn Insight Tag
✅ SSL certificates
✅ Meta tags and SEO elements
✅ Technical performance indicators
3. Competitor Research (competitor_research.py)
Automated competitor analysis using free tools and APIs.

Usage:

bash
python3 competitor_research.py "Client Name"
What it analyzes:

🔍 Website technology stacks
💰 Pricing strategy detection
📱 Social media presence
🎯 Tracking implementation
📊 Technical performance metrics
📋 Complete Workflow
Step 1: Initial Client Setup
bash
# Create project structure
./setup_client.sh "Acme Corporation"

# Navigate to client folder
cd acme_corporation
Step 2: Technical Analysis
bash
# Verify client's website tracking
node ../verify_tracking.js https://acmecorp.com

# Analyze competitors
python3 ../competitor_research.py "Acme Corporation"
Step 3: Data Collection
Fill out questionnaire: 03_business_intel/questionnaire.md
Complete competitor research using generated templates
Collect brand assets in 01_brand_assets/
Set up tracking using 04_technical_setup/tracking_checklist.md
Step 4: Campaign Planning
Review campaign structures in 06_campaign_structure/
Complete keyword research using free tools
Finalize compliance requirements in 07_compliance/
🛠️ Free Tools Integration
Tracking & Analytics
Google Analytics 4 - Core website tracking
Google Search Console - SEO insights
Google Tag Manager - Tag management
Competitor Research
Facebook Ad Library - Competitor social ads
Google Ads Preview Tool - Search ad analysis
SimilarWeb (free tier) - Traffic analysis
Wayback Machine - Historical analysis
Keyword Research
Google Keyword Planner - Search volume data
Answer The Public - Question-based keywords
Google Trends - Trending searches
Ubersuggest (free tier) - Keyword suggestions
Technical Analysis
PageSpeed Insights - Performance testing
Mobile-Friendly Test - Mobile optimization
SSL Labs - Security analysis
📊 Output Files
Each client setup generates organized files:

client_name/
├── 01_brand_assets/
│   ├── brand_guidelines.md
│   └── [logo/image folders]
├── 02_market_research/
│   ├── competitor_analysis.md
│   ├── technical_analysis_[timestamp].csv
│   └── pricing_analysis_[timestamp].csv
├── 03_business_intel/
│   └── questionnaire.md
├── 04_technical_setup/
│   └── tracking_checklist.md
├── 06_campaign_structure/
│   ├── google_ads_structure.md
│   └── meta_ads_structure.md
└── README.md
🔧 Customization
Adding New Tracking Platforms
Edit verify_tracking.js to include additional tracking code detection:

javascript
// Add new tracking detection
const newPlatformMatch = html.match(/newplatform\.js|newPlatformInit/);
if (newPlatformMatch) {
    results.newPlatform.found = true;
}
Custom Questionnaire Fields
Modify the questionnaire template in setup_client.sh:

bash
# Add new sections to questionnaire.md
cat >> "$FOLDER_NAME/03_business_intel/questionnaire.md" << EOF
## Custom Section
- **Custom Field**: 
EOF
Additional Competitor Analysis
Extend competitor_research.py with new analysis functions:

python
def analyze_new_metric(self, html):
    # Add custom analysis logic
    return analysis_result
🚨 Troubleshooting
Common Issues
Script permissions error:

bash
chmod +x setup_client.sh
Python dependencies missing:

bash
pip3 install -r requirements.txt
Node.js not found:

bash
# Install Node.js from https://nodejs.org/
# Or use package manager:
brew install node  # Mac
sudo apt install nodejs npm  # Ubuntu
Website timeout errors:

Check if website is accessible
Try with different URL format (www vs non-www)
Some sites may block automated requests
🔒 Privacy & Ethics
Respect robots.txt - Tools include delays between requests
No scraping of private data - Only analyzes publicly available information
GDPR compliant - No personal data collection
Rate limiting - Respectful request patterns to avoid overloading servers
📈 Advanced Usage
Batch Analysis
Analyze multiple competitors:

bash
# Create competitor list file
echo "https://competitor1.com" > competitors.txt
echo "https://competitor2.com" >> competitors.txt

# Run batch analysis
while read url; do
    node verify_tracking.js "$url" >> analysis_results.txt
    sleep 5
done < competitors.txt
Automated Reporting
Generate monthly competitor reports:

bash
# Create cron job for monthly analysis
0 0 1 * * /path/to/competitor_research.py "Client Name" >> monthly_report.log
Integration with Other Tools
Export data for further analysis:

bash
# Convert CSV to JSON for other tools
python3 -c "
import csv, json
with open('technical_analysis.csv') as f:
    print(json.dumps(list(csv.DictReader(f)), indent=2))
" > analysis.json
🤝 Contributing
Fork the repository
Create a feature branch: git checkout -b new-feature
Make changes and test thoroughly
Commit: git commit -am 'Add new feature'
Push: git push origin new-feature
Submit a pull request
📄 License
MIT License - feel free to use and modify for your agency needs.

🆘 Support
For issues or questions:

Check the troubleshooting section above
Review the generated log files for error details
Open an issue with detailed error information
Built for PPC professionals who want comprehensive client analysis using only free tools.

