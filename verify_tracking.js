#!/usr/bin/env node

/**
 * PPC Tracking Verification Tool
 * Usage: node verify_tracking.js <website_url>
 * Example: node verify_tracking.js https://example.com
 */

const https = require('https');
const http = require('http');
const url = require('url');

// ANSI color codes for better output
const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    reset: '\x1b[0m',
    bold: '\x1b[1m'
};

// Get website URL from command line arguments
const websiteUrl = process.argv[2];

if (!websiteUrl) {
    console.error(`${colors.red}❌ Error: Please provide a website URL${colors.reset}`);
    console.log(`${colors.blue}Usage: node verify_tracking.js <website_url>${colors.reset}`);
    console.log(`${colors.blue}Example: node verify_tracking.js https://example.com${colors.reset}`);
    process.exit(1);
}

// Validate URL format
let parsedUrl;
try {
    parsedUrl = new URL(websiteUrl);
} catch (error) {
    console.error(`${colors.red}❌ Error: Invalid URL format${colors.reset}`);
    console.log(`${colors.blue}Please use format: https://example.com${colors.reset}`);
    process.exit(1);
}

console.log(`${colors.bold}🔍 PPC Tracking Verification Tool${colors.reset}`);
console.log(`${colors.blue}Website: ${websiteUrl}${colors.reset}`);
console.log('═'.repeat(60));

// Function to fetch webpage content
function fetchWebpage(url) {
    return new Promise((resolve, reject) => {
        const client = url.startsWith('https://') ? https : http;
        
        const options = {
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        };

        const req = client.request(url, options, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                resolve({
                    statusCode: res.statusCode,
                    headers: res.headers,
                    body: data
                });
            });
        });
        
        req.on('error', (error) => {
            reject(error);
        });
        
        req.setTimeout(10000, () => {
            req.destroy();
            reject(new Error('Request timeout'));
        });
        
        req.end();
    });
}

// Function to check for tracking codes
function analyzeTrackingCodes(html) {
    const results = {
        googleAnalytics: {
            found: false,
            version: null,
            propertyId: null
        },
        googleAds: {
            found: false,
            conversionId: null
        },
        facebookPixel: {
            found: false,
            pixelId: null
        },
        googleTagManager: {
            found: false,
            containerId: null
        },
        linkedInInsight: {
            found: false,
            partnerId: null
        },
        bingAds: {
            found: false,
            uetTag: null
        }
    };

    // Google Analytics 4 (gtag)
    const ga4Match = html.match(/gtag\(['"]config['"],\s*['"]([^'"]+)['"]/);
    if (ga4Match) {
        results.googleAnalytics.found = true;
        results.googleAnalytics.version = 'GA4';
        results.googleAnalytics.propertyId = ga4Match[1];
    }

    // Universal Analytics (legacy)
    const uaMatch = html.match(/ga\(['"]create['"],\s*['"]([^'"]+)['"]/);
    if (uaMatch && !results.googleAnalytics.found) {
        results.googleAnalytics.found = true;
        results.googleAnalytics.version = 'Universal Analytics';
        results.googleAnalytics.propertyId = uaMatch[1];
    }

    // Google Ads Conversion Tracking
    const googleAdsMatch = html.match(/gtag\(['"]config['"],\s*['"]AW-([^'"]+)['"]/);
    if (googleAdsMatch) {
        results.googleAds.found = true;
        results.googleAds.conversionId = 'AW-' + googleAdsMatch[1];
    }

    // Facebook Pixel
    const fbPixelMatch = html.match(/fbq\(['"]init['"],\s*['"]([^'"]+)['"]/);
    if (fbPixelMatch) {
        results.facebookPixel.found = true;
        results.facebookPixel.pixelId = fbPixelMatch[1];
    }

    // Google Tag Manager
    const gtmMatch = html.match(/googletagmanager\.com\/gtm\.js\?id=([^'"&]+)/);
    if (gtmMatch) {
        results.googleTagManager.found = true;
        results.googleTagManager.containerId = gtmMatch[1];
    }

    // LinkedIn Insight Tag
    const linkedInMatch = html.match(/_linkedin_partner_id\s*=\s*['"]([^'"]+)['"]/);
    if (linkedInMatch) {
        results.linkedInInsight.found = true;
        results.linkedInInsight.partnerId = linkedInMatch[1];
    }

    // Bing Ads UET Tag
    const bingMatch = html.match(/\(function\(w,d,t,r,u\)\{[^}]*UET[^}]*\}\)\(window,document,'script'[^}]*'([^']+)'/);
    if (bingMatch || html.includes('bat.bing.com')) {
        results.bingAds.found = true;
        results.bingAds.uetTag = bingMatch ? bingMatch[1] : 'Found (ID not extracted)';
    }

    return results;
}

// Function to check technical SEO elements
function analyzeTechnicalSEO(html, headers) {
    const results = {
        ssl: false,
        metaTitle: null,
        metaDescription: null,
        h1Tags: [],
        canonicalUrl: null,
        robotsMeta: null,
        schemaMarkup: false,
        openGraph: {
            title: null,
            description: null,
            image: null
        }
    };

    // SSL Check
    results.ssl = parsedUrl.protocol === 'https:';

    // Meta Title
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    if (titleMatch) {
        results.metaTitle = titleMatch[1].trim();
    }

    // Meta Description
    const descMatch = html.match(/<meta[^>]*name=['"]description['"][^>]*content=['"]([^'"]+)['"]/i);
    if (descMatch) {
        results.metaDescription = descMatch[1];
    }

    // H1 Tags
    const h1Matches = html.match(/<h1[^>]*>([^<]+)<\/h1>/gi);
    if (h1Matches) {
        results.h1Tags = h1Matches.map(h1 => h1.replace(/<[^>]*>/g, '').trim());
    }

    // Canonical URL
    const canonicalMatch = html.match(/<link[^>]*rel=['"]canonical['"][^>]*href=['"]([^'"]+)['"]/i);
    if (canonicalMatch) {
        results.canonicalUrl = canonicalMatch[1];
    }

    // Robots Meta
    const robotsMatch = html.match(/<meta[^>]*name=['"]robots['"][^>]*content=['"]([^'"]+)['"]/i);
    if (robotsMatch) {
        results.robotsMeta = robotsMatch[1];
    }

    // Schema Markup
    results.schemaMarkup = html.includes('application/ld+json') || html.includes('schema.org');

    // Open Graph
    const ogTitleMatch = html.match(/<meta[^>]*property=['"]og:title['"][^>]*content=['"]([^'"]+)['"]/i);
    if (ogTitleMatch) results.openGraph.title = ogTitleMatch[1];

    const ogDescMatch = html.match(/<meta[^>]*property=['"]og:description['"][^>]*content=['"]([^'"]+)['"]/i);
    if (ogDescMatch) results.openGraph.description = ogDescMatch[1];

    const ogImageMatch = html.match(/<meta[^>]*property=['"]og:image['"][^>]*content=['"]([^'"]+)['"]/i);
    if (ogImageMatch) results.openGraph.image = ogImageMatch[1];

    return results;
}

// Function to display results
function displayResults(trackingResults, seoResults, headers) {
    console.log(`\n${colors.bold}📊 TRACKING CODES ANALYSIS${colors.reset}`);
    console.log('─'.repeat(40));

    // Google Analytics
    if (trackingResults.googleAnalytics.found) {
        console.log(`${colors.green}✅ Google Analytics: ${trackingResults.googleAnalytics.version}${colors.reset}`);
        console.log(`   Property ID: ${trackingResults.googleAnalytics.propertyId}`);
    } else {
        console.log(`${colors.red}❌ Google Analytics: Not Found${colors.reset}`);
    }

    // Google Ads
    if (trackingResults.googleAds.found) {
        console.log(`${colors.green}✅ Google Ads Conversion Tracking${colors.reset}`);
        console.log(`   Conversion ID: ${trackingResults.googleAds.conversionId}`);
    } else {
        console.log(`${colors.red}❌ Google Ads Conversion Tracking: Not Found${colors.reset}`);
    }

    // Facebook Pixel
    if (trackingResults.facebookPixel.found) {
        console.log(`${colors.green}✅ Facebook Pixel${colors.reset}`);
        console.log(`   Pixel ID: ${trackingResults.facebookPixel.pixelId}`);
    } else {
        console.log(`${colors.red}❌ Facebook Pixel: Not Found${colors.reset}`);
    }

    // Google Tag Manager
    if (trackingResults.googleTagManager.found) {
        console.log(`${colors.green}✅ Google Tag Manager${colors.reset}`);
        console.log(`   Container ID: ${trackingResults.googleTagManager.containerId}`);
    } else {
        console.log(`${colors.yellow}⚠️  Google Tag Manager: Not Found${colors.reset}`);
    }

    // LinkedIn Insight
    if (trackingResults.linkedInInsight.found) {
        console.log(`${colors.green}✅ LinkedIn Insight Tag${colors.reset}`);
        console.log(`   Partner ID: ${trackingResults.linkedInInsight.partnerId}`);
    } else {
        console.log(`${colors.yellow}⚠️  LinkedIn Insight Tag: Not Found${colors.reset}`);
    }

    // Bing Ads
    if (trackingResults.bingAds.found) {
        console.log(`${colors.green}✅ Bing Ads UET Tag${colors.reset}`);
        console.log(`   Tag: ${trackingResults.bingAds.uetTag}`);
    } else {
        console.log(`${colors.yellow}⚠️  Bing Ads UET Tag: Not Found${colors.reset}`);
    }

    console.log(`\n${colors.bold}🔧 TECHNICAL SEO ANALYSIS${colors.reset}`);
    console.log('─'.repeat(40));

    // SSL
    if (seoResults.ssl) {
        console.log(`${colors.green}✅ SSL Certificate: Enabled${colors.reset}`);
    } else {
        console.log(`${colors.red}❌ SSL Certificate: Not Enabled${colors.reset}`);
    }

    // Meta Title
    if (seoResults.metaTitle) {
        const titleLength = seoResults.metaTitle.length;
        const titleStatus = titleLength >= 30 && titleLength <= 60 ? colors.green : colors.yellow;
        console.log(`${titleStatus}${titleLength >= 30 && titleLength <= 60 ? '✅' : '⚠️'}  Meta Title (${titleLength} chars): ${seoResults.metaTitle}${colors.reset}`);
    } else {
        console.log(`${colors.red}❌ Meta Title: Missing${colors.reset}`);
    }

    // Meta Description
    if (seoResults.metaDescription) {
        const descLength = seoResults.metaDescription.length;
        const descStatus = descLength >= 120 && descLength <= 160 ? colors.green : colors.yellow;
        console.log(`${descStatus}${descLength >= 120 && descLength <= 160 ? '✅' : '⚠️'}  Meta Description (${descLength} chars): ${seoResults.metaDescription.substring(0, 80)}...${colors.reset}`);
    } else {
        console.log(`${colors.red}❌ Meta Description: Missing${colors.reset}`);
    }

    // H1 Tags
    if (seoResults.h1Tags.length > 0) {
        const h1Status = seoResults.h1Tags.length === 1 ? colors.green : colors.yellow;
        console.log(`${h1Status}${seoResults.h1Tags.length === 1 ? '✅' : '⚠️'}  H1 Tags (${seoResults.h1Tags.length}): ${seoResults.h1Tags[0]}${colors.reset}`);
    } else {
        console.log(`${colors.red}❌ H1 Tags: Missing${colors.reset}`);
    }

    // Schema Markup
    if (seoResults.schemaMarkup) {
        console.log(`${colors.green}✅ Schema Markup: Found${colors.reset}`);
    } else {
        console.log(`${colors.yellow}⚠️  Schema Markup: Not Found${colors.reset}`);
    }

    console.log(`\n${colors.bold}📱 ADDITIONAL CHECKS${colors.reset}`);
    console.log('─'.repeat(40));

    // Page Speed Recommendation
    console.log(`${colors.blue}🔗 Page Speed Test: https://pagespeed.web.dev/analysis?url=${encodeURIComponent(websiteUrl)}${colors.reset}`);
    
    // Mobile-Friendly Test
    console.log(`${colors.blue}📱 Mobile-Friendly Test: https://search.google.com/test/mobile-friendly?url=${encodeURIComponent(websiteUrl)}${colors.reset}`);

    // Security Headers
    const securityHeaders = ['x-frame-options', 'x-content-type-options', 'x-xss-protection'];
    securityHeaders.forEach(header => {
        if (headers[header]) {
            console.log(`${colors.green}✅ ${header}: ${headers[header]}${colors.reset}`);
        } else {
            console.log(`${colors.yellow}⚠️  ${header}: Missing${colors.reset}`);
        }
    });

    console.log(`\n${colors.bold}📋 SUMMARY & RECOMMENDATIONS${colors.reset}`);
    console.log('═'.repeat(60));

    const trackingScore = Object.values(trackingResults).filter(result => result.found).length;
    const totalTrackingChecks = Object.keys(trackingResults).length;
    
    console.log(`${colors.blue}Tracking Implementation: ${trackingScore}/${totalTrackingChecks} platforms detected${colors.reset}`);
    
    if (!trackingResults.googleAnalytics.found) {
        console.log(`${colors.red}🔥 CRITICAL: Install Google Analytics 4 for basic tracking${colors.reset}`);
    }
    
    if (!trackingResults.googleAds.found) {
        console.log(`${colors.yellow}⚠️  RECOMMENDED: Set up Google Ads conversion tracking${colors.reset}`);
    }
    
    if (!trackingResults.facebookPixel.found) {
        console.log(`${colors.yellow}⚠️  RECOMMENDED: Install Facebook Pixel for Meta campaigns${colors.reset}`);
    }

    if (!seoResults.ssl) {
        console.log(`${colors.red}🔥 CRITICAL: Enable SSL certificate (HTTPS)${colors.reset}`);
    }

    console.log(`\n${colors.green}✅ Analysis complete! Save this report for your client folder.${colors.reset}`);
}

// Main execution
async function main() {
    try {
        console.log('🔄 Fetching webpage...');
        const response = await fetchWebpage(websiteUrl);
        
        if (response.statusCode !== 200) {
            console.error(`${colors.red}❌ Error: HTTP ${response.statusCode}${colors.reset}`);
            process.exit(1);
        }

        console.log(`${colors.green}✅ Webpage fetched successfully${colors.reset}`);
        
        const trackingResults = analyzeTrackingCodes(response.body);
        const seoResults = analyzeTechnicalSEO(response.body, response.headers);
        
        displayResults(trackingResults, seoResults, response.headers);
        
    } catch (error) {
        console.error(`${colors.red}❌ Error: ${error.message}${colors.reset}`);
        process.exit(1);
    }
}

// Run the main function
main();