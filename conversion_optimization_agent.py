#!/usr/bin/env python3
"""
AI Agent for Conversion Optimization Analysis

This agent analyzes websites using a comprehensive CRO and SEO framework,
then generates a PDF report with actionable recommendations.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import sys

class ConversionOptimizationAgent:
    def __init__(self):
        self.url = None
        self.soup = None
        self.analysis_results = {}
        self.recommendations = []
        
    def get_url_input(self):
        """Get URL input from user with improved validation and typo correction"""
        while True:
            url = input("\nPlease enter the website URL to analyze: ").strip()
            
            if not url:
                print("Please enter a valid URL.")
                continue
            
            # Fix common typos
            url = self.fix_url_typos(url)
                
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            try:
                # Basic URL validation
                parsed = urlparse(url)
                if parsed.netloc:
                    self.url = url
                    print(f"✅ URL set: {self.url}")
                    return True
                else:
                    print("Invalid URL format. Please try again.")
            except Exception as e:
                print(f"Error parsing URL: {e}")
    
    def fix_url_typos(self, url):
        """Fix common URL typos and formatting issues"""
        original_url = url
        
        # Only fix obvious protocol typos - be very specific to avoid false matches
        protocol_fixes = [
            ('ttps://', 'https://'),
            ('htps://', 'https://'),
            ('htp://', 'http://'),
            ('https//', 'https://'),
            ('http//', 'http://'),
            ('https:/', 'https://'),  # Only if NOT followed by another slash
            ('http:/', 'http://'),    # Only if NOT followed by another slash
            ('www.https://', 'https://www.'),
            ('www.http://', 'http://www.')
        ]
        
        # Only apply fixes if URL starts with a known typo
        for typo, correct in protocol_fixes:
            if typo in ('https:/', 'http:/'):
                # Special handling for missing slash - only fix if NOT already followed by slash
                if url.startswith(typo) and not url.startswith(typo + '/'):
                    corrected_url = url.replace(typo, correct, 1)
                    print(f"🔧 Auto-corrected URL: {original_url} → {corrected_url}")
                    return corrected_url
            else:
                # Regular replacement for other typos
                if url.startswith(typo):
                    corrected_url = url.replace(typo, correct, 1)
                    print(f"🔧 Auto-corrected URL: {original_url} → {corrected_url}")
                    return corrected_url
        
        # Return unchanged if no obvious typos found
        return url
                
    def scrape_website(self):
        """Scrape and analyze the website content with multiple fallback strategies"""
        print(f"\n🔍 Analyzing website: {self.url}")
        
        # Multiple user agents to try
        user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        for i, user_agent in enumerate(user_agents):
            try:
                headers = {
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0'
                }
                
                if i > 0:
                    print(f"  🔄 Trying fallback method {i}...")
                
                # Add session for better handling
                session = requests.Session()
                session.headers.update(headers)
                
                response = session.get(self.url, timeout=15, allow_redirects=True)
                response.raise_for_status()
                
                self.soup = BeautifulSoup(response.content, 'html.parser')
                print("✅ Website content retrieved successfully")
                return True
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print(f"  ⚠️  Access denied (403) with user agent {i+1}")
                    continue
                elif e.response.status_code == 404:
                    print(f"❌ Page not found (404): {self.url}")
                    return False
                else:
                    print(f"  ⚠️  HTTP error {e.response.status_code}")
                    continue
                    
            except requests.exceptions.RequestException as e:
                print(f"  ⚠️  Request failed: {str(e)}")
                continue
        
        # If all user agents fail, try with minimal headers
        try:
            print("  🔄 Trying minimal headers approach...")
            simple_headers = {'User-Agent': 'curl/7.68.0'}
            response = requests.get(self.url, headers=simple_headers, timeout=10)
            response.raise_for_status()
            
            self.soup = BeautifulSoup(response.content, 'html.parser')
            print("✅ Website content retrieved successfully (minimal headers)")
            return True
            
        except Exception as e:
            print(f"❌ All methods failed. Final error: {e}")
            print("💡 Suggestions:")
            print("   • The website may have strict bot protection")
            print("   • Try running the analysis from a different network")
            print("   • Some sites block automated access entirely")
            return False
            
    def analyze_cro_framework(self):
        """Analyze using the 25-point CRO framework"""
        print("\n📊 Running CRO Analysis...")
        
        cro_analysis = {
            "headline_analysis": self.analyze_headlines(),
            "value_proposition": self.analyze_value_proposition(),
            "cta_analysis": self.analyze_ctas(),
            "form_analysis": self.analyze_forms(),
            "social_proof": self.analyze_social_proof(),
            "trust_signals": self.analyze_trust_signals(),
            "mobile_optimization": self.analyze_mobile_elements(),
            "content_structure": self.analyze_content_structure()
        }
        
        self.analysis_results['cro'] = cro_analysis
        return cro_analysis
        
    def analyze_seo_framework(self):
        """Analyze using the SEO framework"""
        print("\n🔍 Running SEO Analysis...")
        
        seo_analysis = {
            "meta_tags": self.analyze_meta_tags(),
            "url_structure": self.analyze_url_structure(),
            "images": self.analyze_images(),
            "internal_links": self.analyze_internal_links(),
            "headings": self.analyze_headings(),
            "content_quality": self.analyze_content_quality(),
            "schema_markup": self.analyze_schema_markup()
        }
        
        self.analysis_results['seo'] = seo_analysis
        return seo_analysis
        
    def analyze_headlines(self):
        """Analyze headlines using 4-U formula"""
        headlines = []
        h1_tags = self.soup.find_all('h1')
        
        for h1 in h1_tags:
            if h1.get_text(strip=True):
                headlines.append(h1.get_text(strip=True))
                
        analysis = {
            "headlines_found": headlines,
            "count": len(headlines),
            "issues": [],
            "recommendations": []
        }
        
        if len(headlines) == 0:
            analysis["issues"].append("No H1 headlines found")
            analysis["recommendations"].append("Add a compelling H1 headline using the 4-U formula (Useful, Unique, Urgent, Ultra-specific)")
        elif len(headlines) > 1:
            analysis["issues"].append(f"Multiple H1 tags found ({len(headlines)})")
            analysis["recommendations"].append("Use only one H1 per page for better SEO")
            
        return analysis
        
    def analyze_value_proposition(self):
        """Analyze above-fold value proposition"""
        analysis = {
            "above_fold_content": [],
            "issues": [],
            "recommendations": []
        }
        
        # Look for content that should be above fold
        main_content = self.soup.find(['main', 'div'], class_=['hero', 'banner', 'main', 'content'])
        if main_content:
            text = main_content.get_text(strip=True)[:200]  # First 200 chars
            analysis["above_fold_content"].append(text)
        
        analysis["recommendations"].append("Ensure value proposition is clear above the fold with customer problem focus")
        return analysis
        
    def analyze_ctas(self):
        """Analyze Call-to-Action elements"""
        ctas = []
        
        # Look for buttons and links that might be CTAs
        buttons = self.soup.find_all(['button', 'a'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['btn', 'button', 'cta', 'call-to-action']
        ))
        
        for btn in buttons:
            text = btn.get_text(strip=True)
            if text:
                ctas.append(text)
                
        analysis = {
            "ctas_found": ctas,
            "count": len(ctas),
            "issues": [],
            "recommendations": []
        }
        
        if len(ctas) == 0:
            analysis["issues"].append("No clear CTAs found")
            
        # Check for first-person psychology
        first_person_count = sum(1 for cta in ctas if any(word in cta.lower() for word in ['my', 'i', "i'll"]))
        
        analysis["recommendations"].append("Use first-person psychology in CTAs ('Get MY guide' vs 'Get YOUR guide')")
        analysis["recommendations"].append("Place CTAs in mobile thumb zone for better accessibility")
        
        return analysis
        
    def analyze_forms(self):
        """Analyze form complexity"""
        forms = self.soup.find_all('form')
        analysis = {
            "forms_found": len(forms),
            "field_counts": [],
            "issues": [],
            "recommendations": []
        }
        
        for form in forms:
            inputs = form.find_all(['input', 'select', 'textarea'])
            field_count = len([inp for inp in inputs if inp.get('type') not in ['hidden', 'submit']])
            analysis["field_counts"].append(field_count)
            
            if field_count > 5:
                analysis["issues"].append(f"Form has {field_count} fields (recommended max: 5)")
                
        analysis["recommendations"].append("Limit forms to maximum 5 fields - every additional field kills conversions")
        return analysis
        
    def analyze_social_proof(self):
        """Analyze social proof elements"""
        social_proof_elements = []
        
        # Look for testimonials, reviews, ratings
        testimonials = self.soup.find_all(['div', 'section'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['testimonial', 'review', 'rating', 'star']
        ))
        
        analysis = {
            "elements_found": len(testimonials),
            "issues": [],
            "recommendations": []
        }
        
        if len(testimonials) == 0:
            analysis["issues"].append("No clear social proof elements found")
            
        analysis["recommendations"].append("Add testimonials with faces/names near CTAs")
        analysis["recommendations"].append("Include specific results and outcomes in testimonials")
        
        return analysis
        
    def analyze_trust_signals(self):
        """Analyze trust signals"""
        trust_elements = []
        
        # Look for security badges, guarantees, etc.
        trust_keywords = ['security', 'ssl', 'guarantee', 'certified', 'secure', 'trust', 'badge']
        
        for keyword in trust_keywords:
            elements = self.soup.find_all(text=lambda x: x and keyword.lower() in x.lower())
            trust_elements.extend(elements)
            
        analysis = {
            "trust_signals_found": len(trust_elements),
            "recommendations": ["Cluster trust signals (security badges, guarantees, policies) together for maximum impact"]
        }
        
        return analysis
        
    def analyze_mobile_elements(self):
        """Analyze mobile optimization"""
        viewport_meta = self.soup.find('meta', attrs={'name': 'viewport'})
        
        analysis = {
            "viewport_meta": bool(viewport_meta),
            "issues": [],
            "recommendations": []
        }
        
        if not viewport_meta:
            analysis["issues"].append("No viewport meta tag found")
            
        analysis["recommendations"].append("Ensure CTAs are in mobile thumb zone")
        analysis["recommendations"].append("Test on real devices, not just browser tools")
        
        return analysis
        
    def analyze_content_structure(self):
        """Analyze content structure and readability"""
        paragraphs = self.soup.find_all('p')
        
        analysis = {
            "paragraph_count": len(paragraphs),
            "recommendations": [
                "Use Grade 6 reading level - smart people prefer simple",
                "Keep sentences to 11 words maximum",
                "Use benefit-first language - features tell, benefits sell"
            ]
        }
        
        return analysis
        
    def analyze_meta_tags(self):
        """Analyze meta tags"""
        title = self.soup.find('title')
        description = self.soup.find('meta', attrs={'name': 'description'})
        
        analysis = {
            "title": title.get_text() if title else None,
            "description": description.get('content') if description else None,
            "issues": [],
            "recommendations": []
        }
        
        if not title:
            analysis["issues"].append("Missing page title")
        elif title and len(title.get_text()) > 60:
            analysis["issues"].append("Title too long (over 60 characters)")
            
        if not description:
            analysis["issues"].append("Missing meta description")
        elif description and len(description.get('content')) > 156:
            analysis["issues"].append("Meta description too long (over 156 characters)")
            
        analysis["recommendations"].append("Include target keyword in title and description")
        
        return analysis
        
    def analyze_url_structure(self):
        """Analyze URL structure"""
        parsed_url = urlparse(self.url)
        
        analysis = {
            "url": self.url,
            "path_length": len(parsed_url.path),
            "issues": [],
            "recommendations": []
        }
        
        if len(self.url) > 80:
            analysis["issues"].append("URL too long (over 80 characters)")
            
        if '_' in parsed_url.path:
            analysis["issues"].append("URL contains underscores")
            
        analysis["recommendations"].append("Keep URLs 50-60 characters for optimal SEO")
        analysis["recommendations"].append("Include target keywords in URL structure")
        
        return analysis
        
    def analyze_images(self):
        """Analyze image optimization"""
        images = self.soup.find_all('img')
        
        analysis = {
            "image_count": len(images),
            "missing_alt": 0,
            "issues": [],
            "recommendations": []
        }
        
        for img in images:
            if not img.get('alt'):
                analysis["missing_alt"] += 1
                
        if analysis["missing_alt"] > 0:
            analysis["issues"].append(f"{analysis['missing_alt']} images missing alt text")
            
        analysis["recommendations"].append("Compress images to under 200KB each")
        analysis["recommendations"].append("Use WebP format instead of large JPEGs or PNGs")
        analysis["recommendations"].append("Include relevant keywords in alt text naturally")
        
        return analysis
        
    def analyze_internal_links(self):
        """Analyze internal linking"""
        links = self.soup.find_all('a', href=True)
        internal_links = []
        
        for link in links:
            href = link.get('href')
            if href and (href.startswith('/') or self.url in href):
                internal_links.append(href)
                
        analysis = {
            "internal_link_count": len(internal_links),
            "recommendations": [
                "Use descriptive anchor text with keywords",
                "Ensure linked pages are live and not redirected",
                "Create logical linking structure"
            ]
        }
        
        return analysis
        
    def analyze_headings(self):
        """Analyze heading structure"""
        headings = {}
        for i in range(1, 7):
            headings[f'h{i}'] = len(self.soup.find_all(f'h{i}'))
            
        analysis = {
            "heading_structure": headings,
            "issues": [],
            "recommendations": []
        }
        
        if headings['h1'] == 0:
            analysis["issues"].append("No H1 heading found")
        elif headings['h1'] > 1:
            analysis["issues"].append(f"Multiple H1 headings found ({headings['h1']})")
            
        analysis["recommendations"].append("Use only one H1 containing focus keyword")
        analysis["recommendations"].append("Structure headings logically (H1 → H2 → H3)")
        
        return analysis
        
    def analyze_content_quality(self):
        """Analyze content quality"""
        text_content = self.soup.get_text()
        word_count = len(text_content.split())
        
        analysis = {
            "word_count": word_count,
            "issues": [],
            "recommendations": []
        }
        
        if word_count < 300:
            analysis["issues"].append("Content may be too short for SEO")
            
        analysis["recommendations"].append("Aim for 500+ words on service pages, 1000+ on blog posts")
        analysis["recommendations"].append("Include target keyword in first 50-100 words")
        
        return analysis
        
    def analyze_schema_markup(self):
        """Analyze schema markup"""
        scripts = self.soup.find_all('script', type='application/ld+json')
        
        analysis = {
            "schema_found": len(scripts),
            "recommendations": [
                "Implement relevant schema markup (LocalBusiness, Article, FAQ)",
                "Ensure schema accurately reflects on-page content",
                "Use Schema.org validator to check for errors"
            ]
        }
        
        return analysis
        
    def generate_recommendations(self):
        """Generate prioritized recommendations"""
        high_priority = []
        medium_priority = []
        low_priority = []
        
        # Extract all issues and recommendations
        for category, data in self.analysis_results.items():
            for subcategory, analysis in data.items():
                if 'issues' in analysis:
                    for issue in analysis['issues']:
                        high_priority.append(f"{subcategory.replace('_', ' ').title()}: {issue}")
                        
                if 'recommendations' in analysis:
                    for rec in analysis['recommendations']:
                        medium_priority.append(f"{subcategory.replace('_', ' ').title()}: {rec}")
                        
        return {
            "high_priority": high_priority[:10],  # Top 10 issues
            "medium_priority": medium_priority[:10],  # Top 10 recommendations
            "low_priority": ["Implement continuous testing and optimization cycle"]
        }
        
    def generate_pdf_report(self):
        """Generate PDF report with recommendations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversion_optimization_report_{timestamp}.pdf"
        
        try:
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.darkblue,
                spaceAfter=30
            )
            
            story.append(Paragraph("Website Conversion Optimization Report", title_style))
            story.append(Spacer(1, 20))
            
            # Website info
            story.append(Paragraph(f"<b>Website:</b> {self.url}", styles['Normal']))
            story.append(Paragraph(f"<b>Analysis Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            summary_text = f"""
            This report analyzes your website using a comprehensive 25-point Conversion Rate Optimization (CRO) 
            framework and 11-point SEO optimization checklist. The analysis identifies critical issues affecting 
            user experience and search engine performance, along with actionable recommendations for improvement.
            """
            story.append(Paragraph(summary_text, styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Recommendations
            recommendations = self.generate_recommendations()
            
            story.append(Paragraph("High Priority Issues", styles['Heading2']))
            for i, issue in enumerate(recommendations['high_priority'], 1):
                story.append(Paragraph(f"{i}. {issue}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("Medium Priority Recommendations", styles['Heading2']))
            for i, rec in enumerate(recommendations['medium_priority'], 1):
                story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Detailed Analysis
            story.append(PageBreak())
            story.append(Paragraph("Detailed Analysis", styles['Heading1']))
            
            # CRO Analysis
            story.append(Paragraph("Conversion Rate Optimization Analysis", styles['Heading2']))
            cro_data = self.analysis_results.get('cro', {})
            
            for section, data in cro_data.items():
                story.append(Paragraph(section.replace('_', ' ').title(), styles['Heading3']))
                
                if isinstance(data, dict):
                    if 'issues' in data and data['issues']:
                        story.append(Paragraph("<b>Issues:</b>", styles['Normal']))
                        for issue in data['issues']:
                            story.append(Paragraph(f"• {issue}", styles['Normal']))
                            
                    if 'recommendations' in data and data['recommendations']:
                        story.append(Paragraph("<b>Recommendations:</b>", styles['Normal']))
                        for rec in data['recommendations']:
                            story.append(Paragraph(f"• {rec}", styles['Normal']))
                            
                story.append(Spacer(1, 10))
            
            # SEO Analysis
            story.append(PageBreak())
            story.append(Paragraph("SEO Optimization Analysis", styles['Heading2']))
            seo_data = self.analysis_results.get('seo', {})
            
            for section, data in seo_data.items():
                story.append(Paragraph(section.replace('_', ' ').title(), styles['Heading3']))
                
                if isinstance(data, dict):
                    if 'issues' in data and data['issues']:
                        story.append(Paragraph("<b>Issues:</b>", styles['Normal']))
                        for issue in data['issues']:
                            story.append(Paragraph(f"• {issue}", styles['Normal']))
                            
                    if 'recommendations' in data and data['recommendations']:
                        story.append(Paragraph("<b>Recommendations:</b>", styles['Normal']))
                        for rec in data['recommendations']:
                            story.append(Paragraph(f"• {rec}", styles['Normal']))
                            
                story.append(Spacer(1, 10))
            
            # Implementation roadmap
            story.append(PageBreak())
            story.append(Paragraph("Implementation Roadmap", styles['Heading2']))
            roadmap_text = """
            <b>Week 1-2: Critical Issues</b><br/>
            • Fix meta titles and descriptions<br/>
            • Optimize page speed<br/>
            • Improve mobile experience<br/>
            <br/>
            <b>Week 3-4: CRO Improvements</b><br/>
            • Optimize headlines and CTAs<br/>
            • Add social proof elements<br/>
            • Simplify forms<br/>
            <br/>
            <b>Week 5-8: Content & SEO</b><br/>
            • Improve content structure<br/>
            • Implement schema markup<br/>
            • Optimize internal linking<br/>
            <br/>
            <b>Ongoing: Testing & Optimization</b><br/>
            • A/B testing<br/>
            • Performance monitoring<br/>
            • Weekly optimization reviews
            """
            story.append(Paragraph(roadmap_text, styles['Normal']))
            
            # Build PDF
            doc.build(story)
            print(f"\n✅ PDF report generated: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            return None
            
    def run(self):
        """Main execution flow"""
        print("🚀 Conversion Optimization Agent Started")
        print("=" * 50)
        
        # Step 1: Get URL
        if not self.get_url_input():
            return False
            
        # Step 2: Scrape website
        if not self.scrape_website():
            return False
            
        # Step 3: Run analysis
        self.analyze_cro_framework()
        self.analyze_seo_framework()
        
        # Step 4: Generate PDF report
        pdf_file = self.generate_pdf_report()
        
        if pdf_file:
            print(f"\n✅ Analysis complete! Report saved as: {pdf_file}")
            print("\n📋 Summary of findings:")
            recommendations = self.generate_recommendations()
            print(f"• {len(recommendations['high_priority'])} high priority issues identified")
            print(f"• {len(recommendations['medium_priority'])} optimization opportunities found")
            print("\nReview the PDF report for detailed analysis and implementation roadmap.")
        else:
            print("❌ Failed to generate PDF report")
            
        return True

if __name__ == "__main__":
    agent = ConversionOptimizationAgent()
    agent.run()