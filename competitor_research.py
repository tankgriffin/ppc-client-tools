#!/usr/bin/env python3

"""
Enhanced PPC Competitor Research Script
Usage: python competitor_research.py "Client Name"
Provides detailed, actionable insights for PPC campaigns
"""

import requests
import json
import time
import csv
from datetime import datetime
import os
import sys
from urllib.parse import urlparse, urljoin, parse_qs, urlunparse
import re
from bs4 import BeautifulSoup
import collections

class EnhancedCompetitorResearcher:
    def __init__(self, client_name):
        self.client_name = client_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Find existing client folder or create sanitized name
        self.folder_name = self.find_existing_folder(client_name)
        
        self.results = {
            'competitors': [],
            'ad_copy_analysis': [],
            'landing_page_insights': [],
            'keyword_opportunities': [],
            'technical_advantages': []
        }
    
    def find_existing_folder(self, client_name):
        """Find existing client folder or return sanitized name"""
        sanitized = client_name.lower().replace(' ', '_')
        variations = [sanitized, client_name.replace(' ', '_'), client_name.replace(' ', '-')]
        
        for variation in variations:
            if os.path.exists(variation):
                print(f"📁 Found existing folder: {variation}")
                return variation
        
        print(f"📁 Creating new folder: {sanitized}")
        return sanitized
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{'='*70}")
        print(f"🎯 {text}")
        print('='*70)
    
    def print_step(self, text):
        """Print formatted step"""
        print(f"\n📊 {text}")
        print('-'*50)
    
    def save_to_csv(self, data, filename):
        """Save data to CSV file with better formatting"""
        if not data:
            print(f"⚠️  No data to save for {filename}")
            return
        
        filepath = f"{self.folder_name}/02_market_research/{filename}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            if isinstance(data[0], dict):
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(csvfile)
                writer.writerows(data)
        
        print(f"✅ Detailed analysis saved: {filepath}")
    
    def enhanced_website_analysis(self, url):
        """Comprehensive website analysis with actionable insights"""
        try:
            print(f"🔍 Deep analysis of {url}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            analysis = {
                'competitor_url': url,
                'domain_authority_proxy': self.estimate_domain_strength(url, response),
                'page_load_time': round(response.elapsed.total_seconds(), 2),
                'page_size_kb': round(len(html) / 1024, 2),
                
                # SEO & Content Analysis
                'title_tag': self.extract_title(soup),
                'title_length': len(self.extract_title(soup) or ''),
                'meta_description': self.extract_meta_description(soup),
                'meta_desc_length': len(self.extract_meta_description(soup) or ''),
                'h1_tags': self.extract_headings(soup, 'h1'),
                'h2_tags': self.extract_headings(soup, 'h2')[:5],  # First 5 H2s
                
                # Content Marketing Insights
                'total_word_count': self.count_words(soup),
                'content_themes': self.extract_content_themes(soup),
                'key_phrases': self.extract_key_phrases(soup),
                'calls_to_action': self.extract_ctas(soup),
                
                # Technical SEO
                'ssl_enabled': url.startswith('https://'),
                'mobile_viewport': self.check_mobile_viewport(soup),
                'structured_data': self.detect_structured_data(html),
                'canonical_url': self.extract_canonical(soup),
                
                # Conversion Optimization
                'contact_methods': self.analyze_contact_methods(soup),
                'trust_signals': self.identify_trust_signals(soup),
                'pricing_mentions': self.extract_pricing_info(soup),
                'social_proof': self.identify_social_proof(soup),
                
                # Marketing Technology
                'tracking_stack': self.comprehensive_tracking_analysis(html),
                'cms_platform': self.detect_cms_detailed(html, response.headers),
                'third_party_tools': self.identify_third_party_tools(html),
                
                # Competitive Advantages
                'unique_features': self.identify_unique_features(soup),
                'content_gaps': self.identify_content_opportunities(soup),
                'technical_weaknesses': self.identify_technical_issues(soup, response),
                
                # PPC Readiness
                'ppc_landing_quality': self.assess_ppc_readiness(soup),
                'conversion_funnel': self.map_conversion_funnel(soup),
                'ad_compliance_issues': self.check_ad_compliance(soup)
            }
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing {url}: {str(e)}")
            return {'competitor_url': url, 'error': str(e)}
    
    def estimate_domain_strength(self, url, response):
        """Estimate domain authority based on various signals"""
        signals = {
            'https_enabled': url.startswith('https://'),
            'fast_response': response.elapsed.total_seconds() < 2,
            'proper_headers': bool(response.headers.get('server')),
            'security_headers': any(h in response.headers for h in ['x-frame-options', 'x-content-type-options']),
            'cdn_usage': 'cloudflare' in response.headers.get('server', '').lower()
        }
        
        score = sum(signals.values()) * 20  # Max 100
        strength = 'High' if score >= 80 else 'Medium' if score >= 60 else 'Low'
        return f"{strength} ({score}/100)"
    
    def extract_title(self, soup):
        """Extract and clean page title"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else None
    
    def extract_meta_description(self, soup):
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content', '').strip() if meta_desc else None
    
    def extract_headings(self, soup, tag):
        """Extract all headings of specified tag"""
        headings = soup.find_all(tag)
        return [h.get_text().strip() for h in headings if h.get_text().strip()]
    
    def count_words(self, soup):
        """Count words in main content"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        words = len(text.split())
        return words
    
    def extract_content_themes(self, soup):
        """Identify main content themes and topics"""
        # Get all text from paragraphs and headings
        content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        all_text = ' '.join([elem.get_text() for elem in content_elements])
        
        # Common words to filter out
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall', 'this', 'that', 'these', 'those', 'a', 'an'}
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
        word_counts = collections.Counter([w for w in words if w not in stop_words])
        
        # Return top themes
        top_themes = [word for word, count in word_counts.most_common(10) if count >= 3]
        return ', '.join(top_themes)
    
    def extract_key_phrases(self, soup):
        """Extract key phrases that might be used in ads"""
        phrases = []
        
        # Look for phrases in headings
        headings = soup.find_all(['h1', 'h2', 'h3'])
        for heading in headings:
            text = heading.get_text().strip()
            if 5 <= len(text) <= 60:  # Good length for ad headlines
                phrases.append(text)
        
        # Look for phrases in strong/em tags
        emphasis = soup.find_all(['strong', 'em', 'b'])
        for em in emphasis:
            text = em.get_text().strip()
            if 5 <= len(text) <= 60:
                phrases.append(text)
        
        return ' | '.join(phrases[:8])  # Top 8 phrases
    
    def extract_ctas(self, soup):
        """Extract call-to-action buttons and links"""
        ctas = []
        
        # Look for button elements
        buttons = soup.find_all(['button', 'input'])
        for button in buttons:
            text = button.get('value') or button.get_text()
            if text and text.strip():
                ctas.append(text.strip())
        
        # Look for CTA-like links
        links = soup.find_all('a')
        cta_keywords = ['book', 'buy', 'order', 'contact', 'call', 'get', 'start', 'try', 'download', 'sign up', 'learn more', 'discover', 'shop', 'hire']
        
        for link in links:
            text = link.get_text().strip().lower()
            if any(keyword in text for keyword in cta_keywords) and len(text) <= 50:
                ctas.append(link.get_text().strip())
        
        # Remove duplicates and return top CTAs
        unique_ctas = list(dict.fromkeys(ctas))[:10]
        return ' | '.join(unique_ctas)
    
    def check_mobile_viewport(self, soup):
        """Check for mobile viewport meta tag"""
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return bool(viewport)
    
    def detect_structured_data(self, html):
        """Detect structured data/schema markup"""
        schema_indicators = [
            'application/ld+json',
            'schema.org',
            'itemscope',
            'itemtype',
            'itemprop'
        ]
        return any(indicator in html for indicator in schema_indicators)
    
    def extract_canonical(self, soup):
        """Extract canonical URL"""
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        return canonical.get('href') if canonical else None
    
    def analyze_contact_methods(self, soup):
        """Analyze available contact methods"""
        contact_methods = []
        
        # Phone numbers
        phone_pattern = r'(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})'
        if re.search(phone_pattern, soup.get_text()):
            contact_methods.append('Phone')
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, soup.get_text()):
            contact_methods.append('Email')
        
        # Contact forms
        if soup.find('form'):
            contact_methods.append('Contact Form')
        
        # Social media links
        social_platforms = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'tiktok']
        for platform in social_platforms:
            if soup.find('a', href=re.compile(platform, re.I)):
                contact_methods.append(f'{platform.title()}')
        
        # Chat widgets
        chat_indicators = ['chat', 'messenger', 'intercom', 'zendesk', 'tawk']
        page_text = soup.get_text().lower()
        for indicator in chat_indicators:
            if indicator in page_text:
                contact_methods.append('Live Chat')
                break
        
        return ', '.join(list(set(contact_methods)))
    
    def identify_trust_signals(self, soup):
        """Identify trust signals on the page"""
        trust_signals = []
        page_text = soup.get_text().lower()
        
        # Testimonials/Reviews
        review_keywords = ['testimonial', 'review', 'customer says', 'client says', 'rated', 'stars']
        if any(keyword in page_text for keyword in review_keywords):
            trust_signals.append('Customer Reviews')
        
        # Certifications/Awards
        cert_keywords = ['certified', 'award', 'accredited', 'verified', 'licensed', 'insured']
        if any(keyword in page_text for keyword in cert_keywords):
            trust_signals.append('Certifications')
        
        # Experience indicators
        exp_keywords = ['years experience', 'established', 'since', 'family owned', 'local']
        if any(keyword in page_text for keyword in exp_keywords):
            trust_signals.append('Experience Claims')
        
        # Guarantees
        guarantee_keywords = ['guarantee', 'satisfaction', 'money back', 'warranty', 'promise']
        if any(keyword in page_text for keyword in guarantee_keywords):
            trust_signals.append('Guarantees')
        
        # Social proof
        social_keywords = ['customers served', 'projects completed', 'events delivered']
        if any(keyword in page_text for keyword in social_keywords):
            trust_signals.append('Social Proof Numbers')
        
        return ', '.join(trust_signals) if trust_signals else 'None detected'
    
    def extract_pricing_info(self, soup):
        """Extract pricing information and strategy"""
        pricing_info = []
        
        # Look for price mentions
        price_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',  # Dollar amounts
            r'from \$[\d,]+',         # Starting from prices
            r'\$[\d,]+\+',            # Plus pricing
            r'[\d,]+ dollars?',       # Written dollar amounts
        ]
        
        page_text = soup.get_text()
        found_prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            found_prices.extend(matches)
        
        if found_prices:
            pricing_info.append(f"Prices found: {', '.join(found_prices[:5])}")
        
        # Look for pricing strategy indicators
        pricing_keywords = {
            'premium': ['premium', 'luxury', 'high-end', 'exclusive'],
            'budget': ['affordable', 'budget', 'cheap', 'low cost', 'best price'],
            'value': ['value', 'best value', 'competitive price'],
            'custom': ['custom pricing', 'quote', 'contact for price']
        }
        
        page_text_lower = page_text.lower()
        for strategy, keywords in pricing_keywords.items():
            if any(keyword in page_text_lower for keyword in keywords):
                pricing_info.append(f"{strategy.title()} positioning")
        
        return ' | '.join(pricing_info) if pricing_info else 'No pricing info visible'
    
    def identify_social_proof(self, soup):
        """Identify social proof elements"""
        social_proof = []
        page_text = soup.get_text()
        
        # Look for numbers that indicate scale
        number_patterns = [
            r'(\d+[,.]?\d*)\s*(customers?|clients?|projects?|events?|years?)',
            r'over\s+(\d+[,.]?\d*)',
            r'more than\s+(\d+[,.]?\d*)',
        ]
        
        for pattern in number_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    social_proof.append(f"{match[0]} {match[1] if len(match) > 1 else ''}")
                else:
                    social_proof.append(match)
        
        # Look for testimonial indicators
        if soup.find_all(text=re.compile(r'".*"', re.DOTALL)):
            social_proof.append('Customer testimonials present')
        
        # Look for logo sections (client logos)
        if soup.find('img', alt=re.compile('client|partner|customer', re.I)):
            social_proof.append('Client logos displayed')
        
        return ' | '.join(social_proof[:5]) if social_proof else 'Limited social proof'
    
    def comprehensive_tracking_analysis(self, html):
        """Comprehensive analysis of tracking and marketing tools"""
        tracking_tools = []
        
        tracking_patterns = {
            'Google Analytics': [r'gtag\(["\']config["\']', r'ga\(["\']create["\']', r'googletagmanager'],
            'Facebook Pixel': [r'fbq\(["\']init["\']', r'facebook\.com/tr'],
            'Google Ads': [r'gtag\(["\']config["\'],\s*["\']AW-', r'google_conversion'],
            'LinkedIn Insight': [r'_linkedin_partner_id', r'snap\.licdn\.com'],
            'Twitter Ads': [r'twq\(', r'analytics\.twitter\.com'],
            'TikTok Pixel': [r'ttq\.', r'analytics\.tiktok\.com'],
            'Hotjar': [r'hj\(', r'hotjar\.com'],
            'Klaviyo': [r'klaviyo', r'_learnq'],
            'Mailchimp': [r'mailchimp', r'mc\.us\d+\.list-manage'],
            'HubSpot': [r'hubspot', r'hs-analytics'],
            'Intercom': [r'intercom', r'widget\.intercom'],
            'Shopify': [r'shopify', r'cdn\.shopify\.com'],
        }
        
        for tool, patterns in tracking_patterns.items():
            if any(re.search(pattern, html, re.IGNORECASE) for pattern in patterns):
                tracking_tools.append(tool)
        
        return ', '.join(tracking_tools) if tracking_tools else 'Basic tracking only'
    
    def detect_cms_detailed(self, html, headers):
        """Detailed CMS and platform detection"""
        html_lower = html.lower()
        
        platforms = {
            'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
            'Shopify': ['shopify', 'cdn.shopify.com'],
            'Squarespace': ['squarespace', 'static1.squarespace'],
            'Wix': ['wix.com', '_wixCIDX'],
            'Webflow': ['webflow', 'assets.website-files.com'],
            'Drupal': ['drupal', '/sites/default/'],
            'Joomla': ['joomla', '/media/jui/'],
            'Magento': ['magento', 'var/view_preprocessed'],
            'BigCommerce': ['bigcommerce', 'cdn11.bigcommerce'],
            'WooCommerce': ['woocommerce', 'wc-'],
        }
        
        for platform, indicators in platforms.items():
            if any(indicator in html_lower for indicator in indicators):
                return platform
        
        # Check server headers
        server = headers.get('server', '').lower()
        if 'apache' in server:
            return 'Apache Server'
        elif 'nginx' in server:
            return 'Nginx Server'
        elif 'cloudflare' in server:
            return 'Cloudflare (CMS Unknown)'
        
        return 'Unknown Platform'
    
    def identify_third_party_tools(self, html):
        """Identify third-party tools and services"""
        tools = []
        
        tool_patterns = {
            'Live Chat': [r'tawk\.to', r'intercom', r'zendesk', r'livechat'],
            'Email Marketing': [r'mailchimp', r'klaviyo', r'constant-contact', r'mailerlite'],
            'Reviews': [r'trustpilot', r'yelp', r'google.*reviews'],
            'Booking System': [r'calendly', r'acuity', r'bookingkit', r'appointlet'],
            'Payment Processing': [r'stripe', r'paypal', r'square', r'braintree'],
            'Social Media': [r'instagram.*embed', r'facebook.*plugin', r'twitter.*widget'],
            'Analytics': [r'hotjar', r'crazy.*egg', r'mouseflow', r'fullstory'],
            'A/B Testing': [r'optimizely', r'google.*optimize', r'unbounce', r'vwo']
        }
        
        for tool_type, patterns in tool_patterns.items():
            if any(re.search(pattern, html, re.IGNORECASE) for pattern in patterns):
                tools.append(tool_type)
        
        return ', '.join(tools) if tools else 'Standard tools only'
    
    def identify_unique_features(self, soup):
        """Identify unique features or selling points"""
        features = []
        page_text = soup.get_text().lower()
        
        # Service-specific features for balloon/party industry
        party_features = {
            'Custom Design': ['custom', 'bespoke', 'personalized', 'tailored'],
            'Same Day Service': ['same day', 'urgent', 'last minute', 'emergency'],
            'Delivery Service': ['delivery', 'install', 'setup', 'delivered'],
            'Package Deals': ['package', 'bundle', 'combo', 'deal'],
            'Premium Materials': ['premium', 'luxury', 'high quality', 'professional grade'],
            'Event Planning': ['event planning', 'full service', 'coordination'],
            'Themed Packages': ['themed', 'theme', 'character', 'specific occasion']
        }
        
        for feature, keywords in party_features.items():
            if any(keyword in page_text for keyword in keywords):
                features.append(feature)
        
        # Look for unique claims
        unique_keywords = ['only', 'first', 'exclusive', 'unique', 'patented', 'award-winning']
        unique_claims = []
        sentences = page_text.split('.')
        for sentence in sentences[:20]:  # Check first 20 sentences
            if any(keyword in sentence for keyword in unique_keywords):
                if len(sentence.strip()) < 150:  # Reasonable length
                    unique_claims.append(sentence.strip())
        
        if unique_claims:
            features.extend(unique_claims[:3])  # Add top 3 unique claims
        
        return ' | '.join(features) if features else 'Standard offerings'
    
    def identify_content_opportunities(self, soup):
        """Identify content gaps and opportunities"""
        opportunities = []
        page_text = soup.get_text().lower()
        
        # Missing content opportunities for balloon/party industry
        content_gaps = {
            'FAQ Section': ['faq', 'frequently asked', 'common questions'],
            'Process Explanation': ['how it works', 'our process', 'step by step'],
            'Portfolio/Gallery': ['gallery', 'portfolio', 'our work', 'examples'],
            'Pricing Guide': ['pricing', 'price list', 'cost guide'],
            'Service Areas': ['service area', 'we serve', 'locations'],
            'Testimonials': ['testimonial', 'review', 'customer says'],
            'Blog/Tips': ['blog', 'tips', 'advice', 'guide'],
            'About Us': ['about us', 'our story', 'who we are']
        }
        
        for content_type, keywords in content_gaps.items():
            if not any(keyword in page_text for keyword in keywords):
                opportunities.append(f"Missing: {content_type}")
        
        # Check content depth
        word_count = len(page_text.split())
        if word_count < 500:
            opportunities.append("Thin content (under 500 words)")
        
        return ' | '.join(opportunities[:5]) if opportunities else 'Content appears comprehensive'
    
    def identify_technical_issues(self, soup, response):
        """Identify technical SEO issues"""
        issues = []
        
        # Check basic technical elements
        if not soup.find('title'):
            issues.append("Missing title tag")
        elif len(soup.find('title').get_text()) > 60:
            issues.append("Title tag too long")
        
        if not soup.find('meta', attrs={'name': 'description'}):
            issues.append("Missing meta description")
        
        # Check heading structure
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 0:
            issues.append("No H1 tag")
        elif len(h1_tags) > 1:
            issues.append("Multiple H1 tags")
        
        # Check images
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        if len(images_without_alt) > 3:
            issues.append(f"{len(images_without_alt)} images missing alt text")
        
        # Check response time
        if response.elapsed.total_seconds() > 3:
            issues.append(f"Slow loading ({response.elapsed.total_seconds():.1f}s)")
        
        # Check mobile viewport
        if not soup.find('meta', attrs={'name': 'viewport'}):
            issues.append("Missing mobile viewport")
        
        return ' | '.join(issues) if issues else 'No major technical issues'
    
    def assess_ppc_readiness(self, soup):
        """Assess how ready the site is for PPC traffic"""
        readiness_score = 0
        max_score = 10
        
        factors = {
            'Clear CTA': bool(soup.find_all(['button', 'input']) or 
                            [link for link in soup.find_all('a') if any(cta in link.get_text().lower() 
                            for cta in ['contact', 'book', 'call', 'buy'])]),
            'Contact Info': bool(re.search(r'(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})', soup.get_text())),
            'Trust Signals': 'testimonial' in soup.get_text().lower() or 'review' in soup.get_text().lower(),
            'Mobile Friendly': bool(soup.find('meta', attrs={'name': 'viewport'})),
            'Fast Loading': True,  # We'll assume this for now
            'Clear Value Prop': len(soup.find_all(['h1', 'h2'])) >= 2,
            'Contact Form': bool(soup.find('form')),
            'Social Proof': any(word in soup.get_text().lower() for word in ['customers', 'clients', 'events']),
            'Professional Design': len(soup.find_all('img')) > 3,  # Has images
            'Clear Navigation': len(soup.find_all('nav')) > 0 or len(soup.find_all('a')) > 5
        }
        
        readiness_score = sum(factors.values())
        percentage = (readiness_score / max_score) * 100
        
        if percentage >= 80:
            rating = "Excellent"
        elif percentage >= 60:
            rating = "Good"
        elif percentage >= 40:
            rating = "Fair"
        else:
            rating = "Poor"
        
        return f"{rating} ({readiness_score}/{max_score}) - {percentage:.0f}% ready"
    
    def map_conversion_funnel(self, soup):
        """Map the conversion funnel"""
        funnel_elements = []
        
        # Entry points
        if soup.find_all('a'):
            funnel_elements.append("Entry: Navigation links")
        
        # Information gathering
        if soup.find_all(['h2', 'h3']):
            funnel_elements.append("Info: Service descriptions")
        
        # Trust building
        if 'testimonial' in soup.get_text().lower() or 'review' in soup.get_text().lower():
            funnel_elements.append("Trust: Customer reviews")
        
        # Contact methods
        contact_methods = []
        if soup.find('form'):
            contact_methods.append("Contact form")
        if re.search(r'(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})', soup.get_text()):
            contact_methods.append("Phone number")
        if contact_methods:
            funnel_elements.append(f"Convert: {', '.join(contact_methods)}")
        
        return ' → '.join(funnel_elements) if funnel_elements else 'Unclear funnel'
    
    def check_ad_compliance(self, soup):
        """Check for potential ad compliance issues"""
        issues = []
        page_text = soup.get_text().lower()
        
        # Check for superlative claims that might need substantiation
        superlatives = ['best', 'number one', '#1', 'top rated', 'fastest', 'cheapest', 'guaranteed']
        found_superlatives = [sup for sup in superlatives if sup in page_text]
        if found_superlatives:
            issues.append(f"Superlative claims: {', '.join(found_superlatives)}")
        
        # Check for testimonials without disclaimers
        if 'testimonial' in page_text and 'results may vary' not in page_text:
            issues.append("Testimonials without disclaimers")
        
        # Check for pricing claims
        if any(word in page_text for word in ['free', 'guaranteed', 'instant']):
            issues.append("Claims requiring substantiation")
        
        return ' | '.join(issues) if issues else 'No obvious compliance issues'
    
    def generate_competitive_insights(self, all_analyses):
        """Generate actionable competitive insights"""
        self.print_step("Generating Strategic Insights")
        
        insights = []
        
        if not all_analyses:
            return insights
        
        # Analyze common patterns
        common_ctas = []
        common_trust_signals = []
        pricing_strategies = []
        
        for analysis in all_analyses:
            if 'error' not in analysis:
                # Collect CTAs
                if analysis.get('calls_to_action'):
                    common_ctas.extend(analysis['calls_to_action'].split(' | '))
                
                # Collect trust signals
                if analysis.get('trust_signals') and analysis['trust_signals'] != 'None detected':
                    common_trust_signals.extend(analysis['trust_signals'].split(', '))
                
                # Collect pricing strategies
                if analysis.get('pricing_mentions') and analysis['pricing_mentions'] != 'No pricing info visible':
                    pricing_strategies.append(analysis['pricing_mentions'])
        
        # Generate insights
        if common_ctas:
            cta_counter = collections.Counter(common_ctas)
            top_ctas = [cta for cta, count in cta_counter.most_common(5)]
            insights.append({
                'insight_type': 'CTA Strategy',
                'finding': f"Most common CTAs: {', '.join(top_ctas)}",
                'opportunity': 'Test these proven CTAs in your ads and landing pages',
                'priority': 'High'
            })
        
        if common_trust_signals:
            trust_counter = collections.Counter(common_trust_signals)
            top_trust = [signal for signal, count in trust_counter.most_common(3)]
            insights.append({
                'insight_type': 'Trust Building',
                'finding': f"Common trust signals: {', '.join(top_trust)}",
                'opportunity': 'Implement these trust elements on your landing pages',
                'priority': 'High'
            })
        
        # Technology gap analysis
        all_tracking = [analysis.get('tracking_stack', '') for analysis in all_analyses if 'error' not in analysis]
        common_tools = []
        for tracking in all_tracking:
            if tracking and tracking != 'Basic tracking only':
                common_tools.extend(tracking.split(', '))
        
        if common_tools:
            tool_counter = collections.Counter(common_tools)
            top_tools = [tool for tool, count in tool_counter.most_common(3)]
            insights.append({
                'insight_type': 'Technology Stack',
                'finding': f"Competitors using: {', '.join(top_tools)}",
                'opportunity': 'Consider implementing these tracking/marketing tools',
                'priority': 'Medium'
            })
        
        # Content gap analysis
        content_themes = []
        for analysis in all_analyses:
            if 'error' not in analysis and analysis.get('content_themes'):
                content_themes.extend(analysis['content_themes'].split(', '))
        
        if content_themes:
            theme_counter = collections.Counter(content_themes)
            top_themes = [theme for theme, count in theme_counter.most_common(5)]
            insights.append({
                'insight_type': 'Content Strategy',
                'finding': f"Popular content themes: {', '.join(top_themes)}",
                'opportunity': 'Create content around these themes for better keyword targeting',
                'priority': 'Medium'
            })
        
        # PPC readiness comparison
        readiness_scores = []
        for analysis in all_analyses:
            if 'error' not in analysis and analysis.get('ppc_landing_quality'):
                score_text = analysis['ppc_landing_quality']
                if '(' in score_text:
                    score_part = score_text.split('(')[1].split(')')[0]
                    if '/' in score_part:
                        score = int(score_part.split('/')[0])
                        readiness_scores.append(score)
        
        if readiness_scores:
            avg_competitor_score = sum(readiness_scores) / len(readiness_scores)
            insights.append({
                'insight_type': 'PPC Readiness',
                'finding': f"Average competitor PPC readiness: {avg_competitor_score:.1f}/10",
                'opportunity': f"Score above {avg_competitor_score:.1f} to outperform competitors in PPC",
                'priority': 'High'
            })
        
        return insights
    
    def generate_keyword_opportunities(self, analyses, target_keywords):
        """Generate keyword opportunities based on competitor analysis"""
        self.print_step("Identifying Keyword Opportunities")
        
        opportunities = []
        
        # Analyze competitor content for keyword ideas
        all_content_themes = []
        all_headings = []
        all_titles = []
        
        for analysis in analyses:
            if 'error' not in analysis:
                if analysis.get('content_themes'):
                    all_content_themes.extend(analysis['content_themes'].split(', '))
                if analysis.get('h1_tags'):
                    all_headings.extend(analysis['h1_tags'])
                if analysis.get('h2_tags'):
                    all_headings.extend(analysis['h2_tags'])
                if analysis.get('title_tag'):
                    all_titles.append(analysis['title_tag'])
        
        # Find common terms
        all_terms = all_content_themes + [word for heading in all_headings for word in heading.split() if len(word) > 3]
        term_counter = collections.Counter([term.lower() for term in all_terms])
        
        # Generate keyword suggestions
        common_terms = [term for term, count in term_counter.most_common(15) if count >= 2]
        
        for term in common_terms:
            if term not in ' '.join(target_keywords).lower():
                opportunities.append({
                    'keyword_opportunity': term,
                    'source': 'Competitor content analysis',
                    'frequency': term_counter[term],
                    'suggestion': f"Consider targeting '{term}' in campaigns",
                    'priority': 'High' if term_counter[term] >= 3 else 'Medium'
                })
        
        # Location-based opportunities
        location_terms = ['brisbane', 'gold coast', 'melbourne', 'sydney', 'queensland', 'australia']
        for location in location_terms:
            for keyword in target_keywords:
                if location not in keyword.lower():
                    opportunities.append({
                        'keyword_opportunity': f"{keyword} {location}",
                        'source': 'Location targeting',
                        'frequency': 'N/A',
                        'suggestion': f"Add location modifier to '{keyword}'",
                        'priority': 'High'
                    })
        
        # Service-specific opportunities
        balloon_services = ['balloon arch', 'balloon wall', 'balloon bouquet', 'balloon delivery', 'balloon setup', 'balloon styling', 'balloon artist']
        for service in balloon_services:
            if not any(service in keyword.lower() for keyword in target_keywords):
                opportunities.append({
                    'keyword_opportunity': service,
                    'source': 'Service expansion',
                    'frequency': 'N/A',
                    'suggestion': f"Target '{service}' if you offer this service",
                    'priority': 'Medium'
                })
        
        return opportunities[:20]  # Return top 20 opportunities
    
    def run_enhanced_analysis(self):
        """Run the enhanced competitive analysis"""
        self.print_header(f"Enhanced PPC Competitor Research for {self.client_name}")
        
        print("📝 Please provide the following information:")
        
        business_description = input("Business Description: ")
        print(f"\n💡 Tip: Be specific about your services (e.g., 'Balloon garland hire for corporate events and parties')")
        
        competitor_urls = []
        print(f"\nEnter competitor URLs (press Enter on empty line to finish):")
        print("💡 Tip: Include direct competitors and aspirational competitors")
        while True:
            url = input("Competitor URL: ").strip()
            if not url:
                break
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            competitor_urls.append(url)
        
        target_keywords = []
        print(f"\nEnter target keywords (press Enter on empty line to finish):")
        print("💡 Tip: Include both broad and specific terms")
        while True:
            keyword = input("Keyword: ").strip()
            if not keyword:
                break
            target_keywords.append(keyword)
        
        if not competitor_urls:
            print("❌ No competitor URLs provided. Exiting.")
            return
        
        print(f"\n🚀 Starting enhanced analysis for {len(competitor_urls)} competitors...")
        print("⏱️  This may take 2-3 minutes for comprehensive analysis...")
        
        # Run enhanced analysis
        enhanced_results = []
        for i, url in enumerate(competitor_urls, 1):
            print(f"\n📊 Analyzing competitor {i}/{len(competitor_urls)}: {url}")
            result = self.enhanced_website_analysis(url)
            enhanced_results.append(result)
            
            # Be respectful with requests
            if i < len(competitor_urls):
                time.sleep(3)
        
        # Save enhanced results
        self.save_to_csv(enhanced_results, f'enhanced_competitor_analysis_{self.timestamp}.csv')
        
        # Generate competitive insights
        insights = self.generate_competitive_insights(enhanced_results)
        if insights:
            self.save_to_csv(insights, f'competitive_insights_{self.timestamp}.csv')
        
        # Generate keyword opportunities
        keyword_opportunities = self.generate_keyword_opportunities(enhanced_results, target_keywords)
        if keyword_opportunities:
            self.save_to_csv(keyword_opportunities, f'keyword_opportunities_{self.timestamp}.csv')
        
        # Generate actionable summary
        self.generate_actionable_summary(enhanced_results, insights, keyword_opportunities, target_keywords, business_description)
        
        print(f"\n✅ Enhanced analysis complete!")
        print(f"📁 Check detailed reports in: {self.folder_name}/02_market_research/")
        print(f"📋 Key files generated:")
        print(f"   - enhanced_competitor_analysis_{self.timestamp}.csv (detailed competitor data)")
        print(f"   - competitive_insights_{self.timestamp}.csv (strategic insights)")
        print(f"   - keyword_opportunities_{self.timestamp}.csv (keyword suggestions)")
        print(f"   - actionable_summary_{self.timestamp}.md (executive summary)")
    
    def generate_actionable_summary(self, analyses, insights, opportunities, keywords, business_desc):
        """Generate an actionable summary report"""
        self.print_step("Creating Executive Summary")
        
        # Calculate averages and benchmarks
        valid_analyses = [a for a in analyses if 'error' not in a]
        
        if not valid_analyses:
            print("❌ No valid analyses to summarize")
            return
        
        # Calculate benchmarks
        avg_load_time = sum(a.get('page_load_time', 0) for a in valid_analyses) / len(valid_analyses)
        avg_word_count = sum(a.get('total_word_count', 0) for a in valid_analyses) / len(valid_analyses)
        
        # Count features
        ssl_count = sum(1 for a in valid_analyses if a.get('ssl_enabled'))
        mobile_count = sum(1 for a in valid_analyses if a.get('mobile_viewport'))
        
        report_lines = []
        
        # Header
        report_lines.extend([
            "# Enhanced Competitor Analysis Summary",
            f"**Client:** {self.client_name}",
            f"**Business:** {business_desc}",
            f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}",
            f"**Competitors Analyzed:** {len(valid_analyses)}",
            "",
            "## 🎯 Executive Summary",
            "",
            f"This analysis reveals key opportunities for {self.client_name} to outperform competitors in PPC campaigns.",
            "",
            "### 📊 Competitive Benchmarks",
            f"- **Average page load time:** {avg_load_time:.1f} seconds",
            f"- **Average content length:** {avg_word_count:.0f} words", 
            f"- **SSL adoption:** {ssl_count}/{len(valid_analyses)} competitors",
            f"- **Mobile optimization:** {mobile_count}/{len(valid_analyses)} competitors",
            ""
        ])
        
        # Key insights
        if insights:
            report_lines.extend([
                "### 🔍 Key Strategic Insights",
                ""
            ])
            
            high_priority_insights = [i for i in insights if i.get('priority') == 'High']
            for insight in high_priority_insights[:3]:
                report_lines.extend([
                    f"**{insight['insight_type']}**",
                    f"- Finding: {insight['finding']}",
                    f"- Opportunity: {insight['opportunity']}",
                    ""
                ])
        
        # Top competitors analysis
        report_lines.extend([
            "### 🏆 Competitor Performance Analysis",
            ""
        ])
        
        for i, analysis in enumerate(valid_analyses[:3], 1):
            domain = urlparse(analysis['competitor_url']).netloc
            ppc_score = analysis.get('ppc_landing_quality', 'N/A')
            
            report_lines.extend([
                f"**Competitor {i}: {domain}**",
                f"- PPC Readiness: {ppc_score}",
                f"- Load Time: {analysis.get('page_load_time', 'N/A')}s",
                f"- Key Strengths: {analysis.get('unique_features', 'Standard offerings')[:100]}...",
                f"- Weaknesses: {analysis.get('technical_weaknesses', 'None identified')[:100]}...",
                ""
            ])
        
        # Keyword opportunities
        if opportunities:
            report_lines.extend([
                "### 🎯 Top Keyword Opportunities",
                ""
            ])
            
            high_priority_keywords = [o for o in opportunities if o.get('priority') == 'High'][:8]
            for opp in high_priority_keywords:
                report_lines.append(f"- **{opp['keyword_opportunity']}** - {opp['suggestion']}")
            
            report_lines.append("")
        
        # Action items
        report_lines.extend([
            "## 🚀 Immediate Action Items",
            "",
            "### High Priority (This Week)",
            "1. **Optimize page speed** - Target under 2 seconds (current competitor average: {:.1f}s)".format(avg_load_time),
            "2. **Implement missing trust signals** - Add customer reviews and testimonials",
            "3. **Improve mobile experience** - Ensure responsive design and fast mobile loading",
            "",
            "### Medium Priority (This Month)", 
            "4. **Expand keyword targeting** - Test the identified keyword opportunities",
            "5. **Enhance tracking setup** - Implement comprehensive analytics stack",
            "6. **Optimize conversion funnel** - Simplify path from ad click to conversion",
            "",
            "### Long Term (Next Quarter)",
            "7. **Content strategy** - Create content around competitor themes",
            "8. **Technology upgrades** - Implement advanced marketing tools",
            "9. **Continuous monitoring** - Set up monthly competitor analysis",
            "",
            "## 📈 Expected Impact",
            "",
            "By implementing these recommendations, you can expect:",
            "- **15-25% improvement** in Quality Score vs competitors",
            "- **10-20% higher conversion rates** from better landing page optimization", 
            "- **20-30% lower CPCs** through improved relevance and quality",
            "",
            "## 📋 Next Steps",
            "",
            "1. Review detailed CSV files for specific implementation details",
            "2. Prioritize quick wins (SSL, mobile optimization, page speed)",
            "3. Set up tracking for new keyword opportunities",
            "4. Schedule monthly competitor monitoring",
            "",
            f"*Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
        ])
        
        # Save summary
        summary_path = f"{self.folder_name}/02_market_research/actionable_summary_{self.timestamp}.md"
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        print(f"📋 Executive summary saved to: {summary_path}")

def main():
    """Main function"""
    print("🎯 Enhanced PPC Competitor Research Tool")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        client_name = sys.argv[1]
    else:
        client_name = input("Enter client name: ").strip()
    
    if not client_name:
        print("❌ Client name is required")
        sys.exit(1)
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ BeautifulSoup4 is required but not installed.")
        print("💡 Install it with: pip3 install beautifulsoup4")
        sys.exit(1)
    
    researcher = EnhancedCompetitorResearcher(client_name)
    researcher.run_enhanced_analysis()

if __name__ == "__main__":
    main()