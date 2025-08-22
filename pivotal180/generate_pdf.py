from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def create_pdf():
    # Create the PDF document
    doc = SimpleDocTemplate("project-finance-courses-content.pdf", pagesize=letter)
    
    # Get default styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1e3a8a'),
        borderColor=colors.HexColor('#1e3a8a'),
        borderWidth=2,
        borderPadding=10
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        spaceBefore=20,
        textColor=colors.HexColor('#1e3a8a')
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=15,
        spaceBefore=25,
        textColor=colors.HexColor('#1e40af')
    )
    
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#374151')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=6
    )
    
    # Story list to hold all content
    story = []
    
    # Title
    story.append(Paragraph("Project Finance Courses Content Structure", title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # H1: Main Heading
    story.append(Paragraph("H1: Project Finance Modeling Training with Real-World Transaction Experience", h1_style))
    story.append(Paragraph("Master project finance modeling from fundamentals to advanced debt structures with courses taught by senior practitioners with real transactional experience", body_style))
    story.append(Paragraph("<b>Call-to-Action Buttons:</b>", body_style))
    story.append(Paragraph("• View All Project Finance Courses", bullet_style))
    story.append(Paragraph("• Download Brochure", bullet_style))
    story.append(Spacer(1, 0.3*inch))
    
    # H2: Comprehensive Project Finance Training Program
    story.append(Paragraph("H2: Comprehensive Project Finance Training Program", h2_style))
    story.append(Paragraph("Our project finance courses provide comprehensive training in financial modeling for infrastructure, renewable energy, and complex financing structures. Each course is designed and taught by senior practitioners with real-world transaction experience, ensuring practical, applicable skills for finance professionals.", body_style))
    
    # H3: Key Features
    story.append(Paragraph("H3: Key Features", h3_style))
    story.append(Paragraph("<b>Real Transaction Experience</b><br/>Learn from instructors with actual project finance transaction experience across multiple sectors and geographies.", body_style))
    story.append(Paragraph("<b>Comprehensive Materials</b><br/>12-month access to course materials, Excel models, and ongoing support through discussion forums.", body_style))
    story.append(Paragraph("<b>Flexible Delivery</b><br/>Choose from live streaming, self-paced online, or customized in-house training options.", body_style))
    story.append(Paragraph("<b>Professional Accreditation</b><br/>Earn CPD certificates and professional development hours recognized by leading industry organizations.", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # H2: Project Finance Courses Available
    story.append(Paragraph("H2: Project Finance Courses Available", h2_style))
    
    # H3: Introduction to Project Finance Modeling
    story.append(Paragraph("H3: Introduction to Project Finance Modeling", h3_style))
    story.append(Paragraph("Perfect for entry-level professionals seeking to enter the project finance sector. This comprehensive course covers fundamental modeling techniques, project finance structures, and essential Excel skills.", body_style))
    
    story.append(Paragraph("<b>Key Learning Outcomes:</b>", body_style))
    story.append(Paragraph("• Project finance fundamentals and structures", bullet_style))
    story.append(Paragraph("• Cash flow modeling and debt sizing", bullet_style))
    story.append(Paragraph("• Risk analysis and sensitivity testing", bullet_style))
    story.append(Paragraph("• Excel modeling best practices", bullet_style))
    story.append(Paragraph("• Due diligence and documentation review", bullet_style))
    
    story.append(Paragraph("<b>Course Details:</b>", body_style))
    story.append(Paragraph("• Duration: Comprehensive training program", bullet_style))
    story.append(Paragraph("• Delivery: Live streaming, self-paced online", bullet_style))
    story.append(Paragraph("• Pricing: $2,000 (live streaming)", bullet_style))
    story.append(Paragraph("• Includes: 12-month online access, certificate", bullet_style))
    story.append(Paragraph("• Target Audience: Entry-level analysts, students, career changers", bullet_style))
    
    story.append(Paragraph("<b>Call-to-Action Buttons:</b> Learn More | Enroll Now", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # H3: Project Finance Modeling
    story.append(Paragraph("H3: Project Finance Modeling", h3_style))
    story.append(Paragraph("Comprehensive course for analysts, associates, and vice presidents seeking advanced project finance modeling skills. Covers complex structures, debt sizing, and real-world case studies across infrastructure sectors.", body_style))
    
    story.append(Paragraph("<b>Key Learning Outcomes:</b>", body_style))
    story.append(Paragraph("• Advanced debt service coverage ratio (DSCR) analysis", bullet_style))
    story.append(Paragraph("• Equity financing structures and waterfalls", bullet_style))
    story.append(Paragraph("• Tax implications and optimization strategies", bullet_style))
    story.append(Paragraph("• Multi-tranche debt modeling", bullet_style))
    story.append(Paragraph("• International project finance considerations", bullet_style))
    
    story.append(Paragraph("<b>Course Details:</b>", body_style))
    story.append(Paragraph("• Duration: 12-section comprehensive curriculum", bullet_style))
    story.append(Paragraph("• Delivery: Online, self-paced, in-house options", bullet_style))
    story.append(Paragraph("• Pricing: $900-$1,150 depending on format", bullet_style))
    story.append(Paragraph("• Includes: 12-month access, step-by-step model walkthroughs", bullet_style))
    story.append(Paragraph("• Target Audience: Experienced analysts, associates, VPs", bullet_style))
    
    story.append(Paragraph("<b>Call-to-Action Buttons:</b> Learn More | Enroll Now", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # H3: Renewable Energy Project Finance Modeling
    story.append(Paragraph("H3: Renewable Energy Project Finance Modeling", h3_style))
    story.append(Paragraph("Specialized training focused on renewable energy project finance, covering wind and solar project modeling, power purchase agreements, tax credits, and regulatory considerations specific to clean energy projects.", body_style))
    
    story.append(Paragraph("<b>Key Learning Outcomes:</b>", body_style))
    story.append(Paragraph("• Generation forecasting and energy modeling", bullet_style))
    story.append(Paragraph("• Power purchase agreement (PPA) structures", bullet_style))
    story.append(Paragraph("• Tax credit modeling and optimization", bullet_style))
    story.append(Paragraph("• Construction funding and debt structuring", bullet_style))
    story.append(Paragraph("• Renewable energy regulatory compliance", bullet_style))
    
    story.append(Paragraph("<b>Course Details:</b>", body_style))
    story.append(Paragraph("• Duration: Comprehensive sector-specific training", bullet_style))
    story.append(Paragraph("• Delivery: Self-paced online, live streaming, in-person", bullet_style))
    story.append(Paragraph("• Pricing: $900 (self-paced) to $3,200 (premium options)", bullet_style))
    story.append(Paragraph("• Includes: 31 CPD hours, 12-month material access", bullet_style))
    story.append(Paragraph("• Target Audience: Renewable energy finance professionals", bullet_style))
    
    story.append(Paragraph("<b>Call-to-Action Buttons:</b> Learn More | Enroll Now", body_style))
    story.append(PageBreak())
    
    # H3: Advanced Project Finance Debt Modeling
    story.append(Paragraph("H3: Advanced Project Finance Debt Modeling", h3_style))
    story.append(Paragraph("Advanced course for experienced professionals focusing on sophisticated debt modeling techniques, multiple sizing constraints, refinancing calculations, and complex multi-tranche structures.", body_style))
    
    story.append(Paragraph("<b>Key Learning Outcomes:</b>", body_style))
    story.append(Paragraph("• P50/P90/P99 debt sizing methodologies", bullet_style))
    story.append(Paragraph("• Complex debt circularities and construction fees", bullet_style))
    story.append(Paragraph("• Bridging loans and construction financing", bullet_style))
    story.append(Paragraph("• Multi-tranche and junior debt structures", bullet_style))
    story.append(Paragraph("• Seasonal cash flow modeling techniques", bullet_style))
    
    story.append(Paragraph("<b>Course Details:</b>", body_style))
    story.append(Paragraph("• Duration: Intensive advanced training", bullet_style))
    story.append(Paragraph("• Delivery: Live streaming, upcoming self-paced online", bullet_style))
    story.append(Paragraph("• Pricing: $500 (with early bird and student discounts available)", bullet_style))
    story.append(Paragraph("• Includes: 12-month material access, forum support", bullet_style))
    story.append(Paragraph("• Target Audience: Senior analysts, lenders, equity investors", bullet_style))
    
    story.append(Paragraph("<b>Call-to-Action Buttons:</b> Learn More | Enroll Now", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # H2: Why Choose Pivotal180
    story.append(Paragraph("H2: Why Choose Pivotal180 for Project Finance Training?", h2_style))
    
    story.append(Paragraph("H3: Transaction-Based Learning", h3_style))
    story.append(Paragraph("Our courses are built around actual project finance transactions, providing practical insights that theoretical education cannot match.", body_style))
    
    story.append(Paragraph("H3: Senior Practitioner Instructors", h3_style))
    story.append(Paragraph("Learn from professionals with extensive real-world experience in banks, funds, and developer organizations.", body_style))
    
    story.append(Paragraph("H3: Comprehensive Support", h3_style))
    story.append(Paragraph("12-month access to materials, discussion forums, and ongoing support ensure you can apply what you learn.", body_style))
    
    story.append(Paragraph("H3: Flexible Learning Options", h3_style))
    story.append(Paragraph("Choose the delivery method that works best for your schedule and learning preferences.", body_style))
    
    story.append(Paragraph("H3: Industry Recognition", h3_style))
    story.append(Paragraph("Earn CPD certificates and professional development hours recognized across the finance industry.", body_style))
    
    story.append(Paragraph("H3: Global Perspective", h3_style))
    story.append(Paragraph("Benefit from international experience with projects across Australia, the US, and global markets.", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # H2: Career Development
    story.append(Paragraph("H2: Advance Your Project Finance Career", h2_style))
    story.append(Paragraph("Our project finance courses are designed to help professionals at every stage of their career:", body_style))
    
    story.append(Paragraph("H3: Entry Level", h3_style))
    story.append(Paragraph("Students and analysts new to project finance can build foundational skills with our Introduction course.", body_style))
    
    story.append(Paragraph("H3: Mid-Level Professionals", h3_style))
    story.append(Paragraph("Associates and senior analysts can deepen expertise with our comprehensive Project Finance Modeling course.", body_style))
    
    story.append(Paragraph("H3: Sector Specialists", h3_style))
    story.append(Paragraph("Focus on renewable energy with specialized training in clean energy project finance structures.", body_style))
    
    story.append(Paragraph("H3: Senior Practitioners", h3_style))
    story.append(Paragraph("Vice presidents and senior professionals can master advanced debt modeling techniques.", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Final CTA
    story.append(Paragraph("H2: Ready to Master Project Finance Modeling?", h2_style))
    story.append(Paragraph("Join thousands of finance professionals who have advanced their careers with Pivotal180's project finance training.", body_style))
    story.append(Paragraph("<b>Call-to-Action Buttons:</b> Download Course Brochure | Contact Us", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Image Recommendations
    story.append(Paragraph("H2: Image Placement Recommendations", h2_style))
    story.append(Paragraph("<b>Hero Section Image:</b> Professional image of people in a modern office/training environment", body_style))
    story.append(Paragraph("<b>Course Section Images:</b> Screenshots of Excel models for each course, Course materials and certificates, Professional training environment photos", body_style))
    story.append(Paragraph("<b>Features Section Images:</b> Icons representing each feature (handshake, certificate, laptop, globe), Professional headshots of instructors", body_style))
    story.append(Paragraph("<b>Career Path Section Images:</b> Professional workplace images showing career progression, Diverse group of finance professionals", body_style))
    story.append(Paragraph("<b>Call-to-Action Section Image:</b> Group photo of successful course graduates or instructors in professional setting", body_style))
    
    # Build PDF
    doc.build(story)
    print("PDF generated successfully: project-finance-courses-content.pdf")

if __name__ == "__main__":
    create_pdf()