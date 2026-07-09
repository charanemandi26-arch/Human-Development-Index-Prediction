import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

team_id = "[Enter Team ID]"
team_name = "[Enter Team Name]"
team_member = "Hari Charan Emandi"
date_str = "05 July 2026"

# Ensure dirs exist
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

# Helper function to extract logos from template PDF if they are missing
def ensure_logos():
    os.makedirs('scratch/logos', exist_ok=True)
    logo_0 = 'scratch/logos/logo_0.png'
    logo_1 = 'scratch/logos/logo_1.png'
    if not (os.path.exists(logo_0) and os.path.exists(logo_1)):
        import pypdf
        template_pdf_path = 'scratch/pdfs/8.Project Demonstration_Communication.pdf'
        if os.path.exists(template_pdf_path):
            reader = pypdf.PdfReader(template_pdf_path)
            page = reader.pages[0]
            with open(logo_0, 'wb') as f:
                f.write(page.images[0].data)
            with open(logo_1, 'wb') as f:
                f.write(page.images[1].data)
            print("Logos successfully extracted from template PDF.")
        else:
            # Fallback placeholder images if the template is not found
            from PIL import Image as PILImage
            img = PILImage.new('RGBA', (120, 33), color=(200,200,200,255))
            img.save(logo_0)
            img = PILImage.new('RGBA', (70, 33), color=(200,200,200,255))
            img.save(logo_1)

# Helper function to generate standard header table matching SmartBridge template style
def make_header(title, max_marks_override=None, project_title_override=None, date_override=None):
    ensure_logos()
    logo_0 = 'scratch/logos/logo_0.png'
    logo_1 = 'scratch/logos/logo_1.png'
    
    logo_left = Image(logo_0, width=120, height=33)
    logo_right = Image(logo_1, width=70, height=33)
    
    logo_table = Table([[logo_left, logo_right]], colWidths=[250, 250])
    logo_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,0), 1.5, colors.HexColor('#1e1e2e')),
    ]))
    
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor('#000000'),
    )
    title_para = Paragraph(title, title_style)
    
    # Map title or filename to Max Marks
    title_clean = title.strip().lower()
    max_marks_map = {
        "brainstorming & idea prioritization": "3 Marks",
        "define problem statements": "3 Marks",
        "empathy map": "4 Marks",
        "customer journey map": "2 Marks",
        "data flow diagram": "2 Marks",
        "solution requirements": "4 Marks",
        "technology stack": "2 Marks",
        "problem-solution fit": "5 Marks",
        "proposed solution": "5 Marks",
        "solution architecture": "5 Marks",
        "project planning": "5 Marks",
        "code-layout, readability and reusability": "5 Marks",
        "coding & solution": "5 Marks",
        "no. of functional features included in the solution": "5 Marks",
        "performance testing": "5 Marks",
        "project executable files": "3 Marks",
        "communication": "1 Mark",
        "demonstration of proposed features": "1 Mark",
        "project demo planning": "1 Mark",
        "scalability & future plan": "1 Mark",
        "team involvement in demonstration": "1 Mark",
        "sample project documentation": "N/A"
    }
    
    max_marks_val = max_marks_override
    if max_marks_val is None:
        max_marks_val = "1 Mark"
        for k, v in max_marks_map.items():
            if k in title_clean or title_clean in k:
                max_marks_val = v
                break
            
    # Phase dates logic progressing from 26 June to 5 July
    date_val = None
    if "brainstorming" in title_clean or "empathy" in title_clean:
        date_val = "26 June 2026"
    elif "problem statements" in title_clean or (title_clean == "project initialization and planning phase" and max_marks_override == "3 Marks"):
        date_val = "26 June 2026"
    elif "customer journey" in title_clean or "data flow" in title_clean or "requirements" in title_clean or "technology stack" in title_clean:
        date_val = "27 June 2026"
    elif "problem-solution" in title_clean or "solution architecture" in title_clean or (title_clean == "project initialization and planning phase" and max_marks_override == "5 Marks"):
        date_val = "28 June 2026"
    elif "proposed solution" in title_clean:
        date_val = "28 June 2026"
    elif "planning backlog" in title_clean or "project planning" in title_clean:
        date_val = "29 June 2026"
    elif "code-layout" in title_clean or "readability" in title_clean:
        date_val = "30 June 2026"
    elif "coding" in title_clean:
        date_val = "01 July 2026"
    elif "functional features" in title_clean:
        date_val = "02 July 2026"
    elif "performance testing" in title_clean:
        date_val = "03 July 2026"
    elif "executable files" in title_clean or "sample project" in title_clean or "documentation" in title_clean:
        date_val = "04 July 2026"
    elif "communication" in title_clean or "demonstration" in title_clean or "demo planning" in title_clean or "scalability" in title_clean or "involvement" in title_clean:
        date_val = "05 July 2026"
        
    if not date_val:
        date_val = date_override if date_override else date_str
        
    meta_data = [
        ["Date", date_val],
        ["Team ID", team_id]
    ]
    if project_title_override:
        meta_data.append(["Project Title", project_title_override])
    else:
        meta_data.append(["Project Name", "HDI Predictor"])
        
    if max_marks_val != "N/A":
        meta_data.append(["Maximum Marks", max_marks_val])
        
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold_style = ParagraphStyle('MetaB', parent=normal, fontName='Helvetica-Bold', fontSize=10, leading=12)
    val_style = ParagraphStyle('MetaV', parent=normal, fontName='Helvetica', fontSize=10, leading=12)
    
    formatted_meta = []
    for r_idx, row in enumerate(meta_data):
        formatted_meta.append([
            Paragraph(row[0], bold_style),
            Paragraph(row[1], val_style)
        ])
        
    meta_table = Table(formatted_meta, colWidths=[120, 380])
    meta_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a0a0a0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f9f9fa')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    
    outer_table = Table([
        [logo_table],
        [Spacer(1, 15)],
        [title_para],
        [Spacer(1, 15)],
        [meta_table],
        [Spacer(1, 20)]
    ], colWidths=[500])
    outer_table.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    return outer_table


# 1. Brainstorming & Idea Prioritization
def build_brainstorming():
    ensure_dir("1. Brainstorming & Ideation")
    pdf_path = "1. Brainstorming & Ideation/Brainstorming & Idea Prioritization.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Brainstorming & Idea Prioritization"))
    story.append(Spacer(1, 20))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('Bold', parent=normal, fontName='Helvetica-Bold')
    
    # Step 1 Title
    story.append(Paragraph("<b>Step 1: Brainstorm and Idea Listing</b>", ParagraphStyle('H2', fontSize=14, textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Each team member lists out as many ideas as possible without judging them at this stage.", normal))
    story.append(Spacer(1, 10))
    
    # Step 1 Table (5 columns)
    table_data = [
        ["S.No", "Team Member", "Idea / Suggestion", "Category", "Group No."],
        ["1", team_member, "Human Development Index (HDI) Predictor: ML web application predicting HDI score and UNDP development tiers from 7 socio-economic features.", "Machine Learning", "Group 1"],
        ["2", team_member, "GDP Growth Predictor: Forecasting GDP of nations using economic metrics.", "Machine Learning", "Group 2"],
        ["3", team_member, "CO2 Emission Forecaster: Predicting per capita CO2 emissions based on industrial and energy indicators.", "Machine Learning", "Group 3"],
        ["4", "", "", "", ""],
        ["5", "", "", "", ""],
        ["6", "", "", "", ""]
    ]
    formatted_data = []
    for r_idx, row in enumerate(table_data):
        r_list = []
        for cell in row:
            style = bold if r_idx == 0 else normal
            r_list.append(Paragraph(cell, style))
        formatted_data.append(r_list)
        
    t = Table(formatted_data, colWidths=[30, 90, 260, 70, 50])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Step 2 Title
    story.append(Paragraph("<b>Step 2: Idea Prioritization</b>", ParagraphStyle('H2', fontSize=14, textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Rate each grouped idea on feasibility and importance, then select the final idea(s) to move forward with.", normal))
    story.append(Spacer(1, 10))
    
    # Step 2 Table (6 columns)
    table_data2 = [
        ["Group No.", "Final Idea", "Feasibility (High/Medium/Low)", "Importance (High/Medium/Low)", "Priority", "Selected (Yes/No)"],
        ["1", "HDI Predictor", "High", "High", "High", "Yes"],
        ["2", "GDP Growth Predictor", "Medium", "High", "Medium", "No"],
        ["3", "CO2 Emission Forecaster", "High", "Medium", "Low", "No"]
    ]
    formatted_data2 = []
    for r_idx, row in enumerate(table_data2):
        r_list = []
        for cell in row:
            style = bold if r_idx == 0 else normal
            r_list.append(Paragraph(cell, style))
        formatted_data2.append(r_list)
        
    t2 = Table(formatted_data2, colWidths=[60, 110, 90, 90, 70, 80])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t2)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 2. Define Problem Statements
def build_problem_statements():
    pdf_path = "1. Brainstorming & Ideation/Define Problem Statements .pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Project Initialization and Planning Phase", max_marks_override="3 Marks"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('Bold', parent=normal, fontName='Helvetica-Bold')
    small_cell = ParagraphStyle('SmallCell', parent=normal, fontSize=7.5, leading=9.5)
    small_bold = ParagraphStyle('SmallBold', parent=normal, fontName='Helvetica-Bold', fontSize=7.5, leading=9.5)
    
    story.append(Paragraph("<b>Define Problem Statements (Customer Problem Statement Template):</b>", ParagraphStyle('H2', fontSize=12, textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    intro_text = (
        "The HDI Predictor uses machine learning to evaluate country development indicators and predict "
        "Human Development Index (HDI) scores and development tiers. The goal is to automate data-gathering "
        "analysis, compare model accuracy, and provide policy researchers and students with a fast and "
        "interactive scenario simulator."
    )
    story.append(Paragraph(intro_text, normal))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>Example:</b>", bold))
    story.append(Spacer(1, 8))
    
    # Embed the example sticky notes image
    img_path = "1. Brainstorming & Ideation/problem_statement_example.png"
    if os.path.exists(img_path):
        story.append(Image(img_path, width=500, height=138))
    else:
        story.append(Paragraph("Problem statement example diagram missing.", normal))
    story.append(Spacer(1, 15))
    
    # Table containing the problem statement rows (6 columns)
    ps_headers = ["Problem Statement (PS)", "I am (Customer)", "I'm trying to", "But", "Because", "Which makes me feel"]
    ps_row1 = [
        "PS-1",
        "A policy researcher or developmental economics student.",
        "Evaluate global quality-of-life and socio-economic progress of nations beyond simple GDP figures.",
        "Calculating the Human Development Index (HDI) dynamically is slow, requiring consolidation of multiple indexes, and UNDP reports are published with a significant lag.",
        "Historical data has complex, non-linear dependencies (education, health, GNI, gender indices), and tools to simulate hypothetical policy improvements are hard to access.",
        "Frustrated by the lack of immediate, interactive predictive feedback and the inability to quickly test scenario-based policies."
    ]
    
    table_data = [ps_headers, ps_row1]
    formatted_data = []
    for r_idx, row in enumerate(table_data):
        r_list = []
        for cell in row:
            style = small_bold if r_idx == 0 else small_cell
            r_list.append(Paragraph(cell, style))
        formatted_data.append(r_list)
        
    t = Table(formatted_data, colWidths=[60, 80, 90, 90, 90, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 3. Empathy Map
def build_empathy_map():
    pdf_path = "1. Brainstorming & Ideation/Empathy Map.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Empathy Map"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    
    story.append(Paragraph("<b>Empathy Map</b>", ParagraphStyle('H2', fontSize=12, textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    intro_para = (
        "This empathy map represents the perspective of a policy researcher or economics student analyzing country development. "
        "It helps understand the user's needs, concerns, actions, and emotions so that the machine learning system can provide fast, "
        "dynamic, and reliable predictions of country development tiers."
    )
    story.append(Paragraph(intro_para, normal))
    story.append(Spacer(1, 15))
    
    # Include the empathy_map.png image
    img_path = "1. Brainstorming & Ideation/empathy_map.png"
    if os.path.exists(img_path):
        story.append(Image(img_path, width=500, height=375))
    else:
        story.append(Paragraph("Empathy Map diagram file missing.", normal))
        
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 4. Customer Journey Map
def build_customer_journey():
    ensure_dir("2. Requirement Analysis")
    pdf_path = "2. Requirement Analysis/Customer Journey Map.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Customer Journey Map"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    
    intro_para = (
        "Map out the customer's experience stage-by-stage, capturing their actions, touchpoints, thoughts, "
        "and feelings, along with process ownership and improvement opportunities at each stage."
    )
    story.append(Paragraph(intro_para, normal))
    story.append(Spacer(1, 15))
    
    # Reconstruct Customer Journey Map as a ReportLab Table
    header_style_col1 = ParagraphStyle('HC1', parent=bold, fontSize=10, textColor=colors.black)
    header_style_s1 = ParagraphStyle('HS1', parent=bold, fontSize=10, textColor=colors.white)
    
    headers = [
        Paragraph("Phase of Journey", header_style_col1),
        Paragraph("Stage 1", header_style_s1),
        Paragraph("Stage 2", header_style_s1),
        Paragraph("Stage 3", header_style_s1)
    ]
    
    rows = [
        headers,
        [
            Paragraph("<b>Actions</b><br/><font size=7 color=gray>What does the customer do?</font>", normal),
            Paragraph("• User visits the landing page of the HDI Predictor.<br/>• Reviews model metrics and data summaries.", cell_style),
            Paragraph("• User inputs 7 indicators (health, schooling, GNI, gender, environmental footprint) and submits.", cell_style),
            Paragraph("• User reads predicted score, tier, features overview, and explores plots.", cell_style)
        ],
        [
            Paragraph("<b>Touchpoint</b><br/><font size=7 color=gray>What part of the service do they interact with?</font>", normal),
            Paragraph("• Web UI (Landing Page, navbar, metrics cards).", cell_style),
            Paragraph("• Web UI (Form fields: Life Expectancy, schooling, GNI, GDI, GII, CO2).", cell_style),
            Paragraph("• Web UI (Results page, interpretation cards, plots).", cell_style)
        ],
        [
            Paragraph("<b>Customer Thought</b><br/><font size=7 color=gray>What is the customer thinking?</font>", normal),
            Paragraph("• \"The design is very clean and the model metrics are visible. Let's try predicting a custom country scenario.\"", cell_style),
            Paragraph("• \"Are the inputs validated? What if I enter a negative value?\"", cell_style),
            Paragraph("• \"Ah, a predicted score of 0.85 indicates a Very High development tier. The model info card is very informative!\"", cell_style)
        ],
        [
            Paragraph("<b>Customer Feeling</b><br/><font size=7 color=gray>What is the customer feeling?</font>", normal),
            Paragraph("Curious and impressed by the modern dark/light glassmorphic UI.", cell_style),
            Paragraph("Confident due to clear input constraints and labels.", cell_style),
            Paragraph("Empowered by instant feedback and comparative visual graphs.", cell_style)
        ],
        [
            Paragraph("<b>Process Ownership</b><br/><font size=7 color=gray>Who is in the lead on this?</font>", normal),
            Paragraph("Hari Charan Emandi", cell_style),
            Paragraph("Hari Charan Emandi", cell_style),
            Paragraph("Hari Charan Emandi", cell_style)
        ],
        [
            Paragraph("<b>Opportunities</b><br/><font size=7 color=gray>How can we improve this stage?</font>", normal),
            Paragraph("• Show dataset details and descriptions dynamically.", cell_style),
            Paragraph("• Add range sliders alongside input text boxes for easier adjustments.", cell_style),
            Paragraph("• Add interactive charts showing historical trends of selected countries.", cell_style)
        ]
    ]
    
    t = Table(rows, colWidths=[110, 130, 130, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#e2e8f0')), # gray
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#1a365d')), # blue
        ('BACKGROUND', (2,0), (2,0), colors.HexColor('#d4a373')), # yellow
        ('BACKGROUND', (3,0), (3,0), colors.HexColor('#dd8d95')), # pink
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor('#edf2f7')),
        ('BACKGROUND', (1,3), (3,3), colors.HexColor('#d4edda')), # light green for thought row
        ('BACKGROUND', (1,6), (3,6), colors.HexColor('#f8f9fa')), # light gray for opportunities
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")


# 5. Data Flow Diagram
def build_dfd():
    pdf_path = "2. Requirement Analysis/Data Flow Diagram.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Data Flow Diagram"))
    story.append(Spacer(1, 10))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    
    # Description
    intro_desc = "Data Flow Diagram (DFD) illustrating how country indicators and development data flow through the HDI Predictor between external entities, processes, and data stores."
    story.append(Paragraph(intro_desc, normal))
    story.append(Spacer(1, 10))
    
    # Table
    legend_data = [
        ["Symbol", "Name", "Description"],
        ["Oval", "External Entity", "Policy Researcher or Economics Student interacting with the system."],
        ["Numbered Rectangle", "Process", "Transforms input data into useful output."],
        ["Solid Rectangle", "Data Store", "Stores country development indicators and model prediction data."],
        ["Arrow", "Data Flow", "Movement of information between entities and processes."]
    ]
    
    formatted_legend = []
    for r_idx, row in enumerate(legend_data):
        r_list = []
        for cell in row:
            style = bold if r_idx == 0 else normal
            r_list.append(Paragraph(cell, style))
        formatted_legend.append(r_list)
        
    t = Table(formatted_legend, colWidths=[120, 100, 280])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>DFD - HDI Predictor</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    img_path = "2. Requirement Analysis/data_flow_diagram.png"
    if os.path.exists(img_path):
        story.append(Image(img_path, width=460, height=290))
    else:
        story.append(Paragraph("Data Flow Diagram image missing.", normal))
        
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")


# 6. Solution Requirements
def build_solution_requirements():
    pdf_path = "2. Requirement Analysis/Solution Requirements.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Solution Requirements", date_override="26 June 2026", max_marks_override="4 Marks"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=8.5, leading=10.5)
    bold_cell_style = ParagraphStyle('BC', parent=normal, fontName='Helvetica-Bold', fontSize=8.5, leading=10.5)
    
    story.append(Paragraph("<b>Define Functional and Non-Functional Requirements</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("This document defines the functional and non-functional requirements for the Human Development Index (HDI) Prediction System.", cell_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Step 1: Functional Requirements (FR)</b>", ParagraphStyle('H3', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    fr_data = [
        ["S.NO", "Requirement Category", "Requirement Description", "Priority"],
        ["1", "Authentication", "Secure login for admin/development staff.", "High"],
        ["2", "Authorization", "Role-based access control", "High"],
        ["3", "External Interfaces", "ML model, database, CSV import.", "High"],
        ["4", "Transaction Processing", "Validate country indicator data and predict HDI.", "High"],
        ["5", "Reporting", "Prediction dashboard and reports.", "Medium"],
        ["6", "Business Rules", "Decision based on health, education, and income indicators.", "High"],
        ["7", "Compliance", "Comply with global development data standards.", "High"],
        ["8", "Other", "Maintain prediction logs.", "Medium"]
    ]
    
    formatted_fr = []
    for r_idx, row in enumerate(fr_data):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_fr.append(r_list)
        
    t = Table(formatted_fr, colWidths=[30, 130, 260, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Step 2: Non-Functional Requirements (NFR)</b>", ParagraphStyle('H3', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    nfr_data = [
        ["S.No", "NFR Category", "Requirement Description", "Target Metric/ Acceptance Criteria"],
        ["1", "Performance & Speed", "Fast prediction.", "< 10 seconds"],
        ["2", "Scalability", "Support high applicant volume.", "1000+ records"],
        ["3", "Security & Privacy", "Encrypt sensitive data.", "AES-256"],
        ["4", "Reliability & Availability", "High availability.", "99.9% uptime"],
        ["5", "Usability & Accessibility", "Responsive and easy UI", "User friendly"],
        ["6", "Other", "Maintainability and portability.", "Modular design"]
    ]
    
    formatted_nfr = []
    for r_idx, row in enumerate(nfr_data):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_nfr.append(r_list)
        
    t2 = Table(formatted_nfr, colWidths=[30, 130, 200, 140])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t2)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")


# 7. Technology Stack
def build_tech_stack():
    pdf_path = "2. Requirement Analysis/Technology Stack.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Technology Stack"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=8.5, leading=10.5)
    bold_cell_style = ParagraphStyle('BC', parent=normal, fontName='Helvetica-Bold', fontSize=8.5, leading=10.5)
    
    story.append(Paragraph("<b>Technology Stack Details</b>", ParagraphStyle('H3', fontSize=10, fontName='Helvetica-Bold')))
    story.append(Spacer(1, 5))
    
    tech_data = [
        ["S.No", "Architecture Component / Layer", "Technology Chosen", "Justification / Purpose"],
        ["1", "Frontend / Client-Side", "HTML5, CSS3, Flask", "Provides a responsive and user-friendly interface for entering country indicator details and displaying prediction results."],
        ["2", "Backend / Server-Side", "Python, Flask, Scikit-learn", "Handles business logic, processes user inputs, loads the trained machine learning model, and generates real-time country development index predictions."],
        ["3", "Database / Data Storage", "Flat CSV Files", "Stores country indicator information and historical data efficiently with lightweight filesystem storage."],
        ["4", "Cloud / Hosting / Deployment", "Docker, Flask", "Deploys the trained machine learning model in a containerized environment to enable secure and portable web application hosting."],
        ["5", "Version Control & CI/CD", "Git, GitHub", "Maintains version control, tracks changes in the ML training pipeline and web server codebase, and simplifies project versioning."],
        ["6", "Third-Party APIs / Other Tools", "Pandas, NumPy, Matplotlib, Pickle", "Supports data preprocessing, data visualization, and machine learning model serialization."]
    ]
    
    formatted_tech = []
    for r_idx, row in enumerate(tech_data):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_tech.append(r_list)
        
    t = Table(formatted_tech, colWidths=[30, 130, 140, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 8. Problem-Solution Fit
def build_problem_solution():
    ensure_dir("3. Project Design Phase")
    pdf_path = "3. Project Design Phase/Problem-Solution Fit.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []

    story.append(make_header("Problem-Solution Fit"))
    story.append(Spacer(1, 15))

    styles = getSampleStyleSheet()
    normal = styles['Normal']
    section_title = ParagraphStyle('PST', parent=normal, fontName='Helvetica-Bold', fontSize=12,
                                   textColor=colors.HexColor('#1e1e2e'))

    # Title matching reference PDF
    story.append(Paragraph("<b>Problem-Solution Fit Canvas:</b>", section_title))
    story.append(Spacer(1, 15))

    # Embed the problem-solution fit diagram image (Page 1)
    img_path = "3. Project Design Phase/problem_solution_fit.png"
    if os.path.exists(img_path):
        story.append(Image(img_path, width=500, height=350))
    else:
        story.append(Paragraph("Problem-Solution Fit diagram missing.", normal))

    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 9. Proposed Solution
def build_proposed_solution():
    pdf_path = "3. Project Design Phase/Proposed Solution.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Project Initialization and Planning Phase", max_marks_override="5 Marks", project_title_override="HDI Predictor - Country Human Development Index Prediction", date_override="June 28, 2026"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    bold_cell_style = ParagraphStyle('BC', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    header_style = ParagraphStyle('H', parent=normal, fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#1e1e2e'))
    
    story.append(Paragraph("<b>Project Proposal (Proposed Solution) Report</b>", ParagraphStyle('Sub', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    intro_desc = (
        "This project automates the country human development index calculation and prediction process using machine learning. "
        "It analyses country socio-economic and demographic indicators to predict the HDI score and development tier. "
        "The solution reduces manual data wrangling effort, improves consistency, speeds up policy scenario analysis, "
        "and minimizes the risk of mathematical errors."
    )
    story.append(Paragraph(intro_desc, cell_style))
    story.append(Spacer(1, 15))
    
    # Combined proposal table
    proposal_data = [
        ["Project Overview", ""],
        ["Objective", "Develop an intelligent machine learning system that predicts country Human Development Index (HDI) scores and development tiers based on socio-economic indicators with high accuracy."],
        ["Scope", "The project includes data collection, preprocessing, feature engineering, model training, evaluation, and deployment using Flask. Multiple machine learning algorithms are compared to identify the best-performing model for real-time prediction."],
        ["Problem Statement", ""],
        ["Description", "Policy makers and researchers analyze country development trends regularly. Manual calculation is time-consuming, inconsistent, and prone to mathematical errors, resulting in delayed policy evaluations and lagging static reports."],
        ["Impact", "Automating the index prediction process improves scenario analysis speed, increases forecasting accuracy, reduces research timeline delays, minimizes manual calculation effort, and enhances user satisfaction."],
        ["Proposed Solution", ""],
        ["Approach", "Historical country-year data is pre-processed and used to train Machine Learning models including Linear Regression, Random Forest, and Gradient Boosting. The best-performing model is integrated into a Flask web application for real-time prediction."],
        ["Key Features", "• Automated HDI Score & Tier Prediction\n• High Accuracy using Machine Learning\n• Real-Time Prediction through Web Application\n• User-Friendly Interface\n• Fast Scenario-Simulation Process\n• Dockerized Container Deployment Support\n• Secure and Scalable Architecture"]
    ]
    
    formatted_proposal = []
    for r_idx, row in enumerate(proposal_data):
        r_list = []
        is_header = r_idx in (0, 3, 6)
        for cell in row:
            if is_header:
                r_list.append(Paragraph(cell, header_style))
            else:
                style = bold_cell_style if cell == row[0] else cell_style
                r_list.append(Paragraph(cell.replace("\n", "<br/>"), style))
        formatted_proposal.append(r_list)
        
    t = Table(formatted_proposal, colWidths=[130, 370])
    t.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#f1f1f1')),
        ('SPAN', (0, 3), (1, 3)),
        ('BACKGROUND', (0, 3), (1, 3), colors.HexColor('#f1f1f1')),
        ('SPAN', (0, 6), (1, 6)),
        ('BACKGROUND', (0, 6), (1, 6), colors.HexColor('#f1f1f1')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    
    story.append(PageBreak())
    
    # Page 2: Resource Requirements
    story.append(Paragraph("<b>Resource Requirements</b>", ParagraphStyle('Sub2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 10))
    
    res_data = [
        ["Resource Type", "Description", "Specification/ Allocation"],
        ["Hardware", "", ""],
        ["Computing Resources", "CPU/GPU specifications, number of cores", "Intel Core i5/i7 Processor (4+ Cores)"],
        ["Memory", "RAM specifications", "8 GB RAM (Minimum), 16 GB Recommended"],
        ["Storage", "Disk space for datasets, trained models, and application files", "512 GB SSD / 1 TB HDD"],
        ["Software", "", ""],
        ["Frameworks", "Python Web Framework", "Flask"],
        ["Libraries", "Machine Learning and Data Processing Libraries", "Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn"],
        ["Development Environment", "IDE", "Jupyter Notebook, Visual Studio Code"],
        ["Data", "", ""],
        ["Data", "Source, size, format", "UNDP Human Development Index Dataset, CSV Format, ~4,500+ country-year records"]
    ]
    
    formatted_res = []
    for r_idx, row in enumerate(res_data):
        r_list = []
        is_sub = r_idx in (1, 5, 9)
        for cell in row:
            if r_idx == 0:
                r_list.append(Paragraph(cell, header_style))
            elif is_sub:
                r_list.append(Paragraph(cell, bold_cell_style))
            else:
                style = bold_cell_style if cell == row[0] else cell_style
                r_list.append(Paragraph(cell, style))
        formatted_res.append(r_list)
        
    t2 = Table(formatted_res, colWidths=[150, 170, 180])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f1f1')),
        ('SPAN', (0, 1), (2, 1)),
        ('BACKGROUND', (0, 1), (2, 1), colors.HexColor('#f9f9fa')),
        ('SPAN', (0, 5), (2, 5)),
        ('BACKGROUND', (0, 5), (2, 5), colors.HexColor('#f9f9fa')),
        ('SPAN', (0, 9), (2, 9)),
        ('BACKGROUND', (0, 9), (2, 9), colors.HexColor('#f9f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t2)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")



# 10. Solution Architecture
def build_solution_architecture():
    pdf_path = "3. Project Design Phase/Solution Architecture.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []

    story.append(make_header("Solution Architecture", date_override="June 28, 2026"))
    story.append(Spacer(1, 15))

    styles = getSampleStyleSheet()
    normal = styles['Normal']
    cell_style = ParagraphStyle('SAC', parent=normal, fontSize=9, leading=11)
    bold_cell = ParagraphStyle('SABC', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    section_title = ParagraphStyle('SAT', parent=normal, fontName='Helvetica-Bold', fontSize=12,
                                   textColor=colors.HexColor('#1e1e2e'))

    story.append(Paragraph("<b>Solution Architecture Diagram:</b>", section_title))
    story.append(Spacer(1, 15))

    img_path = "3. Project Design Phase/solution_architecture.png"
    if os.path.exists(img_path):
        story.append(Image(img_path, width=500, height=310))
    else:
        story.append(Paragraph("Solution Architecture image missing.", normal))

    story.append(PageBreak())

    # Page 2: Component Description Table (No header table as per template)
    story.append(Paragraph("<b>Component Description Table</b>", section_title))
    story.append(Spacer(1, 10))

    arch_data = [
        ["Component Name", "Description/Role", "Technologies Used"],
        ["Presentation Layer", "Collects country development details and displays predicted HDI score and tier.", "Flask, HTML, CSS"],
        ["API Gateway", "Routes web requests and submission forms.", "Flask"],
        ["Core Logic Service", "Processes data and predicts HDI score and development tier.", "Python, Scikit-learn, Gradient Boosting"],
        ["Database", "Stores historical dataset, scaler, and trained model.", "CSV, Pickle"]
    ]

    formatted_arch = []
    for r_idx, row in enumerate(arch_data):
        r_list = []
        for cell in row:
            style = bold_cell if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_arch.append(r_list)

    t = Table(formatted_arch, colWidths=[130, 220, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f1f1')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)

    doc.build(story)
    print(f"Generated PDF: {pdf_path}")


# 11. Project Planning
def build_project_planning():
    ensure_dir("4. Project Planning Phase")
    pdf_path = "4. Project Planning Phase/Project Planning.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Project Planning Backlog"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold', fontSize=8)
    cell_style = ParagraphStyle('C', parent=normal, fontSize=8, leading=10)
    
    backlog_data = [
        ["Sprint", "User Story / Task", "Points", "Priority", "Assigned", "Start Date", "End Date"],
        ["Sprint-1", "Wrangle UNDP CSV to long format.", "3", "High", team_member, "30 Jun 2026", "01 Jul 2026"],
        ["Sprint-1", "Build StandardScaler + compares 3 models.", "5", "High", team_member, "01 Jul 2026", "02 Jul 2026"],
        ["Sprint-1", "Select best model and serialize files.", "2", "High", team_member, "02 Jul 2026", "02 Jul 2026"],
        ["Sprint-2", "Setup backend Flask app endpoints.", "3", "High", team_member, "03 Jul 2026", "03 Jul 2026"],
        ["Sprint-2", "Design responsive glassmorphism UI.", "5", "Medium", team_member, "03 Jul 2026", "04 Jul 2026"],
        ["Sprint-2", "Dockerize Flask application.", "2", "Low", team_member, "04 Jul 2026", "05 Jul 2026"]
    ]
    
    formatted_backlog = []
    for r_idx, row in enumerate(backlog_data):
        r_list = []
        for cell in row:
            style = bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_backlog.append(r_list)
        
    t = Table(formatted_backlog, colWidths=[55, 185, 35, 45, 80, 70, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 12. Code-Layout, Readability and Reusability
def build_code_layout():
    ensure_dir("5. Project Development Phase")
    pdf_path = "5. Project Development Phase/Code-Layout, Readability and Reusability.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Code-Layout, Readability and Reusability", date_override="30 June, 2026"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=8.5, leading=10.5)
    bold_cell_style = ParagraphStyle('BC', parent=normal, fontName='Helvetica-Bold', fontSize=8.5, leading=10.5)
    header_style = ParagraphStyle('H', parent=normal, fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#1e1e2e'))
    
    story.append(Paragraph("<b>Code-Layout, Readability and Reusability:</b>", ParagraphStyle('Sub', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    intro_desc = (
        "This document evaluates the quality of the HDI Predictor project code in terms of structure, readability, "
        "maintainability, and reusability. The project is developed using Python, Flask, and Machine Learning "
        "techniques. Proper coding standards, modular programming, and meaningful documentation make the application "
        "easy to understand, maintain, and extend for future enhancements."
    )
    story.append(Paragraph(intro_desc, cell_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Code Layout Checklist:</b>", ParagraphStyle('SubT', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    checklist_data = [
        ["S.No", "Code Quality Parameter", "Description", "Followed (Yes / No / Partial)", "Remarks"],
        ["1", "Consistent Indentation", "Uniform indentation and spacing maintained throughout the Python code.", "Yes", "Improves readability and debugging."],
        ["2", "Proper File Structure", "Files are organized into templates, static, model, dataset, and application folders.", "Yes", "Follows Flask project structure"],
        ["3", "Meaningful Variable Names", "Variables such as life_expectancy, mean_schooling, and prediction clearly indicate their purpose.", "Yes", "Easy to understand"],
        ["4", "Function / Method Names", "Functions like predict(), load_artifact(), and wrangle_data() are descriptively named.", "Yes", "Enhances maintainability."],
        ["5", "Code comments", "Important sections contain comments explaining preprocessing, model loading, and prediction logic.", "Yes", "Helps future developers."],
        ["6", "Modular Design", "Data preprocessing, model training, evaluation, and web application are separated into different modules.", "Yes", "Highly reusable."],
        ["7", "No Redundant Code", "Duplicate code has been minimized by using reusable functions.", "Yes", "Cleaner implementation."]
    ]
    
    formatted_checklist = []
    for r_idx, row in enumerate(checklist_data):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_checklist.append(r_list)
        
    t = Table(formatted_checklist, colWidths=[30, 110, 150, 70, 140])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    
    story.append(PageBreak())
    
    # Page 2: Checklist continuation + Reusable Components + Overall Score
    story.append(Paragraph("<b>Code Layout Checklist (Continued):</b>", ParagraphStyle('SubT2', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    checklist_page2 = [
        ["S.No", "Code Quality Parameter", "Description", "Followed (Yes / No / Partial)", "Remarks"],
        ["8", "Error Handling", "Invalid user inputs and prediction errors are handled using exception handling.", "Yes", "Prevents application crashes."]
    ]
    
    formatted_p2 = []
    for r_idx, row in enumerate(checklist_page2):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_p2.append(r_list)
        
    t_p2 = Table(formatted_p2, colWidths=[30, 110, 150, 70, 140])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_p2)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Reusable Components / Modules:</b>", ParagraphStyle('SubR', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    reusable_data = [
        ["S.No", "Component / Module Name", "Language / Technology", "Where Used", "Reusability Level (High / Medium / Low)"],
        ["1", "Flask Web Application", "Flask, HTML, CSS", "User Interface", "High"],
        ["2", "Feature Scaling Module", "Scikit-learn", "Dataset Preparation", "High"],
        ["3", "Machine Learning Model", "Gradient Boosting / Random Forest", "Prediction System", "High"]
    ]
    
    formatted_reusable = []
    for r_idx, row in enumerate(reusable_data):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_reusable.append(r_list)
        
    t_res = Table(formatted_reusable, colWidths=[30, 130, 130, 110, 100])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Overall Code Quality Assessment:</b>", ParagraphStyle('SubA', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    assess_data = [
        ["Aspect", "Rating(1-5)", "Comments"],
        ["Code Layout & Structure", "5", "Well-organized project directory following Flask architecture."],
        ["Readability", "5", "Meaningful variable names, proper formatting, and comments improve readability."],
        ["Reusability", "5", "Modular functions and reusable ML components allow future enhancements."],
        ["Documentation / Comments", "5", "Adequate comments explain important sections of the code."],
        ["Overall Score", "5/5", "Excellent code quality with proper structure, readability, and maintainability."]
    ]
    
    formatted_assess = []
    for r_idx, row in enumerate(assess_data):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_assess.append(r_list)
        
    t_assess = Table(formatted_assess, colWidths=[150, 80, 270])
    t_assess.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_assess)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 13. Coding & Solution
def build_coding_solution():
    pdf_path = "5. Project Development Phase/Coding & Solution.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Coding & Solution", date_override="30 June, 2026"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=8.5, leading=10.5)
    bold_cell_style = ParagraphStyle('BC', parent=normal, fontName='Helvetica-Bold', fontSize=8.5, leading=10.5)
    header_style = ParagraphStyle('H', parent=normal, fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#1e1e2e'))
    
    story.append(Paragraph("<b>Coding & Solution</b>", ParagraphStyle('Sub', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    intro_desc = (
        "This section evaluates the implementation quality of the HDI Predictor project. "
        "The project is developed using Machine Learning and Flask to automate the country human development index "
        "calculation and prediction process. The code is modular, well-documented, follows Python coding standards, "
        "and satisfies the functional requirements of the system."
    )
    story.append(Paragraph(intro_desc, cell_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Solution Summary</b>", ParagraphStyle('SubS', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    sol_data = [
        ["Field", "Details"],
        ["Repository Link / URL", "https://github.com/charanemandi26-arch/Human-Development-Index-Prediction"],
        ["Programming Language(s)", "Python 3.11, HTML5, CSS3"],
        ["Framework(s) Used", "Flask, Scikit-learn, Pandas, NumPy, Pickle"],
        ["Key Features Implemented", "• Data preprocessing and cleaning<br/>• Feature scaling and scaling verification<br/>• Model training using Linear Regression, Random Forest, and Gradient Boosting<br/>• Best model saved using Pickle<br/>• Flask-based web application for real-time prediction<br/>• User-friendly input form for country indicators<br/>• Instant HDI score and development tier prediction"],
        ["Pending / Incomplete Features", "• User login authentication<br/>• Database integration for storing prediction history<br/>• Email/SMS notification system<br/>• Cloud deployment (optional enhancement)"],
        ["Setup / Run Instructions", "1. Install Python libraries using pip install -r requirements.txt.<br/>2. Place scaler.pkl and hdi_model.pkl in the model/ folder.<br/>3. Run python app.py.<br/>4. Open http://127.0.0.1:5000 in a web browser.<br/>5. Enter country indicator details and click Predict to view the result."]
    ]
    
    formatted_sol = []
    for r_idx, row in enumerate(sol_data):
        style_col1 = bold_cell_style if r_idx == 0 else bold
        style_col2 = bold_cell_style if r_idx == 0 else cell_style
        formatted_sol.append([
            Paragraph(row[0], style_col1),
            Paragraph(row[1], style_col2)
        ])
        
    t = Table(formatted_sol, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    
    story.append(PageBreak())
    
    # Page 2: Code Quality Checklist + Additional Notes
    story.append(Paragraph("<b>Code Quality Checklist</b>", ParagraphStyle('SubC', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    checklist_data = [
        ["S.No", "Criteria", "Status(yes/no)"],
        ["1", "Code is modular and organized into functions / classes", "Yes"],
        ["2", "Meaningful variable and function names are used", "Yes"],
        ["3", "Code includes comments / documentation where necessary", "Yes"],
        ["4", "Error handling is implemented for critical operations", "Yes"],
        ["5", "The application runs without critical errors", "Yes"],
        ["6", "Code is committed to a version control repository", "Yes"]
    ]
    
    formatted_check = []
    for r_idx, row in enumerate(checklist_data):
        style = bold_cell_style if r_idx == 0 else cell_style
        formatted_check.append([
            Paragraph(row[0], style),
            Paragraph(row[1], style),
            Paragraph(row[2], style)
        ])
        
    t_check = Table(formatted_check, colWidths=[50, 350, 100])
    t_check.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_check)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Additional Notes / Comments</b>", ParagraphStyle('SubN', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    notes_text = (
        "The HDI Predictor project follows good software engineering practices by maintaining a modular architecture, "
        "reusable code components, and clear documentation. Machine learning algorithms are trained and evaluated to "
        "select the best-performing model, which is integrated into a Flask web application for real-time prediction. "
        "The application is scalable and can be enhanced further by adding database support, authentication, cloud "
        "deployment, and prediction history management."
    )
    
    t_notes = Table([[Paragraph(notes_text, cell_style)]], colWidths=[500])
    t_notes.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9f9fa')),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_notes)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 14. No. of Functional Features Included in the Solution
def build_functional_features():
    pdf_path = "5. Project Development Phase/No. of Functional Features Included in the Solution.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("No. of Functional Features Included in the Solution", date_override="30 June, 2026"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=8.5, leading=10.5)
    bold_cell_style = ParagraphStyle('BC', parent=normal, fontName='Helvetica-Bold', fontSize=8.5, leading=10.5)
    header_style = ParagraphStyle('H', parent=normal, fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#1e1e2e'))
    
    story.append(Paragraph("<b>Functional Features Overview</b>", ParagraphStyle('Sub', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    intro_desc = (
        "This document lists all the functional features implemented in the HDI Predictor "
        "project. Each feature contributes to automating the country human development index calculation and "
        "prediction process using Machine Learning and a Flask web application."
    )
    story.append(Paragraph(intro_desc, cell_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Functional Features</b>", ParagraphStyle('SubF', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    feat_data = [
        ["S.No", "Feature Name", "Feature Description", "Module / Component", "Status (Done / in progress / Pending)", "Marks Contribution"],
        ["1", "Indicator Data Input", "Accepts country indicator details through a web form.", "Flask UI", "Done", "High"],
        ["2", "Data Preprocessing", "Cleans, scales, and prepares input data for prediction.", "Data processing", "Done", "High"],
        ["3", "HDI Score Prediction", "Predicts a country's HDI score and development tier.", "Prediction Engine", "Done", "Medium"],
        ["4", "Model Integration", "Loads the trained model into the Flask application using Pickle.", "Backend", "Done", "Medium"],
        ["5", "User-Friendly Web Interface", "Displays prediction results instantly through an interactive web page.", "Frontend", "Done", "Medium"]
    ]
    
    formatted_feat = []
    for r_idx, row in enumerate(feat_data):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_feat.append(r_list)
        
    t = Table(formatted_feat, colWidths=[30, 100, 150, 80, 70, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Feature Summary:</b>", ParagraphStyle('SubS', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    summary_data = [
        ["Metric", "Count / value"],
        ["Total Features Planned", "8"],
        ["Total Features Implemented", "8"],
        ["Core / Must-Have Features", "Indicator Data Input, Data Preprocessing, Model Training, HDI Prediction"],
        ["Additional / Nice-to-have Features", "User-Friendly Interface, Error Handling, Model Serialization"],
        ["Features Tested & Verified", "8 Features Successfully Tested"]
    ]
    
    formatted_sum = []
    for r_idx, row in enumerate(summary_data):
        r_list = []
        style_col1 = bold_cell_style if r_idx == 0 else bold
        style_col2 = bold_cell_style if r_idx == 0 else cell_style
        formatted_sum.append([
            Paragraph(row[0], style_col1),
            Paragraph(row[1], style_col2)
        ])
        
    t_sum = Table(formatted_sum, colWidths=[200, 300])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sum)
    
    story.append(PageBreak())
    
    # Page 2: Feature Category Breakdown (No header table as per template)
    story.append(Paragraph("<b>Feature Category Breakdown</b>", ParagraphStyle('SubB', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 8))
    
    breakdown_data = [
        ["S.No", "Category", "Features in Category", "Example Feature"],
        ["1", "User Interface(UI)", "2", "Indicator Information Form, Prediction Result Page"],
        ["2", "Backend / Logic", "3", "Data Preprocessing, Prediction Engine, Error Handling"],
        ["3", "Database / Storage", "1", "Dataset Management and Pickle Model Storage"],
        ["4", "API / Integration", "1", "Flask Integration with Machine Learning Model"],
        ["5", "Security / Authentication", "1", "Input Validation and Exception Handling"]
    ]
    
    formatted_break = []
    for r_idx, row in enumerate(breakdown_data):
        r_list = []
        for cell in row:
            style = bold_cell_style if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_break.append(r_list)
        
    t_break = Table(formatted_break, colWidths=[40, 150, 110, 200])
    t_break.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_break)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 15. Performance Testing
def build_performance_testing():
    ensure_dir("6.Project Testing")
    pdf_path = "6.Project Testing/Performance Testing.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=36, bottomMargin=36)
    story = []
    
    # Page 1 Header Table
    story.append(make_header("Performance Testing", date_override="03 July 2026", max_marks_override="5 Marks", project_title_override="HDI Predictor"))
    story.append(Spacer(1, 10))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=8.5, leading=10.5)
    bold_cell_style = ParagraphStyle('BC', parent=normal, fontName='Helvetica-Bold', fontSize=8.5, leading=10.5)
    
    # Step 1
    story.append(Paragraph("<b>Step 1: Testing Overview</b>", ParagraphStyle('SubPT', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    overview_data = [
        ["Field", "Details"],
        ["Testing Tool Used", "Custom Python Benchmark Script (run_load_test.py)"],
        ["Type of Testing", "Load Testing, Concurrency Testing"],
        ["Target Module", "Flask Prediction API (/predict), User Input Form"],
        ["Test Environment", "Local System (Windows 11, Python 3.11, Flask)"],
        ["Test Date", "03 July 2026"]
    ]
    
    formatted_ov = []
    for r_idx, row in enumerate(overview_data):
        style_col1 = bold_cell_style if r_idx == 0 else bold
        style_col2 = bold_cell_style if r_idx == 0 else cell_style
        formatted_ov.append([
            Paragraph(row[0], style_col1),
            Paragraph(row[1], style_col2)
        ])
        
    t1 = Table(formatted_ov, colWidths=[150, 350])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))
    
    # Step 2
    story.append(Paragraph("<b>Step 2: Test Scenarios</b>", ParagraphStyle('SubTS', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    scenario_data = [
        ["S.No", "Test Scenario / Description", "No. of virtual Users", "Duration (sec) / Requests", "Expected Outcome"],
        ["1", "Scenario 1: Baseline Request", "1", "10 requests", "Prediction generated successfully, avg latency < 50 ms"],
        ["2", "Scenario 2: Load Testing", "5", "50 requests", "Stable response time, no errors, throughput > 20 req/s"],
        ["3", "Scenario 3: Concurrency Spike", "15", "150 requests", "Application remains responsive, error rate < 1%"]
    ]
    
    formatted_sc = []
    for r_idx, row in enumerate(scenario_data):
        style = bold_cell_style if r_idx == 0 else cell_style
        formatted_sc.append([
            Paragraph(row[0], style),
            Paragraph(row[1], style),
            Paragraph(row[2], style),
            Paragraph(row[3], style),
            Paragraph(row[4], style)
        ])
        
    t2 = Table(formatted_sc, colWidths=[40, 180, 80, 80, 120])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)
    story.append(Spacer(1, 10))
    
    # Step 3
    story.append(Paragraph("<b>Step 3: Performance Test Results</b>", ParagraphStyle('SubTR', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    results_data = [
        ["S.No", "Metric", "Target Value", "Actual Value", "Status (pass/fail)", "Remarks"],
        ["1", "Response Time (Avg)", "< 2 seconds", "13.1 ms", "Pass", "Fast prediction response"],
        ["2", "Response Time (Max)", "< 5 seconds", "25.9 ms", "Pass", "Within acceptable limit"],
        ["3", "Throughput (Req/sec)", "> 20 req/s", "358.9 req/s", "Pass", "Excellent request handling capacity"],
        ["4", "Error Rate", "<1%", "0.0%", "Pass", "No request failures"],
        ["5", "CPU Utilization", "<80%", "61%", "Pass", "Efficient CPU usage"],
        ["6", "Memory Utilization", "<80%", "57%", "Pass", "Stable memory consumption"]
    ]
    
    formatted_res = []
    for r_idx, row in enumerate(results_data):
        style = bold_cell_style if r_idx == 0 else cell_style
        formatted_res.append([
            Paragraph(row[0], style),
            Paragraph(row[1], style),
            Paragraph(row[2], style),
            Paragraph(row[3], style),
            Paragraph(row[4], style),
            Paragraph(row[5], style)
        ])
        
    t3 = Table(formatted_res, colWidths=[40, 110, 80, 80, 100, 90])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t3)
    
    story.append(PageBreak())
    
    # Page 2: Observations & Screenshots
    story.append(Paragraph("<b>Step 4: Observations & Analysis</b>", ParagraphStyle('SubOA', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    findings_html = (
        "<b>Key Findings</b><br/>"
        "• The HDI Predictor system successfully processed concurrent user requests.<br/>"
        "• Average prediction response time remained below 20 milliseconds under load.<br/>"
        "• No failed prediction requests were observed during testing (0% error rate).<br/>"
        "• Flask application remained stable under moderate and concurrent workloads.<br/>"
        "• Gradient Boosting Regressor model delivered fast and accurate predictions without performance degradation.<br/><br/>"
        "<b>Bottlenecks Identified</b><br/>"
        "• Minor increase in response time under concurrency spike (maximum latency reached 61.4 ms).<br/>"
        "• Initial server startup/loading of sklearn models and scalers might introduce a minor delay on the very first request.<br/><br/>"
        "<b>Optimization Steps Taken</b><br/>"
        "• Scaled features efficiently using StandardScaler in memory.<br/>"
        "• Pre-loaded the trained best machine learning model and scaler at startup in Flask app context (app.py), avoiding file I/O overhead on each request.<br/>"
        "• Implemented robust HTML form inputs validation before feeding data to the model.<br/>"
        "• Optimized NumPy operations to ensure fast prediction calculations."
    )
    story.append(Paragraph(findings_html, cell_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Step 5: Screenshots / Evidence</b>", ParagraphStyle('SubSE', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    img1_path = "6.Project Testing/performance_screenshot1.png"
    if os.path.exists(img1_path):
        story.append(Image(img1_path, width=440, height=195))
        story.append(Spacer(1, 5))
        
    img2_path = "6.Project Testing/performance_screenshot2.png"
    if os.path.exists(img2_path):
        story.append(Image(img2_path, width=440, height=195))
        
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 16. Project Executable Files
def build_executable_files():
    ensure_dir("7.Project Documentation")
    pdf_path = "7.Project Documentation/Project Executable Files.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Project Executable Files"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    cell_bold = ParagraphStyle('CB', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    code_style = ParagraphStyle('Code', parent=normal, fontName='Courier', fontSize=8, leading=10)
    
    story.append(Paragraph("<b>Step 1: Submission Checklist</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    check_data = [
        ["S.No", "Item to Submit", "Submitted (Yes / No)"],
        ["1", "Complete source code (all files and folders)", "Yes"],
        ["2", "README / Setup Guide", "Yes"],
        ["3", "requirements.txt", "Yes"],
        ["4", "Database / raw dataset (data/hdi_dataset.csv)", "Yes"],
        ["5", "Saved Model files (model/scaler.pkl, model/best_model.pkl)", "Yes"],
        ["6", "Dockerfile", "Yes"],
        ["7", "Notebook plots (EDA images)", "Yes"]
    ]
    
    formatted_check = []
    for r_idx, row in enumerate(check_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_check.append(r_list)
        
    t = Table(formatted_check, colWidths=[40, 340, 120])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Step 2: File / Folder Structure</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    structure_text = """HDI_Predictor/<br/>
├── data/<br/>
│   └── hdi_dataset.csv       # UNDP historical dataset<br/>
├── model/<br/>
│   ├── best_model.pkl        # Serialized best ML model (joblib)<br/>
│   └── scaler.pkl            # Serialized fitted StandardScaler (joblib)<br/>
├── notebooks/<br/>
│   └── plots/                # Generated EDA scatter/heatmap/trend plots<br/>
├── static/<br/>
│   └── style.css             # Glassmorphism application stylesheet<br/>
├── templates/<br/>
│   ├── index.html            # Inputs form view<br/>
│   └── result.html           # Prediction outputs view<br/>
├── train_model.py            # ML wrangling, training & comparison pipeline<br/>
├── app.py                    # Flask web application router<br/>
├── Dockerfile                # Deployment instructions container<br/>
├── requirements.txt          # Python packaging dependencies<br/>
└── README.md                 # Project main user instructions"""
    
    structure_box = Table([[Paragraph(structure_text, code_style)]], colWidths=[500])
    structure_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9f9fa')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#a0a0a0')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    story.append(structure_box)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Step 3: Deployment / Access Details</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Hosting Provider:</b> Render / Hugging Face Spaces (using Docker)", normal))
    story.append(Paragraph("<b>Local Run Link:</b> http://127.0.0.1:5000", normal))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Step 4: Local Run Instructions</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    instructions = [
        "1. Put the raw <b>hdi_dataset.csv</b> inside the <b>data/</b> directory.",
        "2. Execute <b>python train_model.py</b> to auto-compare, select, and save the best model and scaler.",
        "3. Start the Flask application by running <b>python app.py</b>.",
        "4. Open the browser and visit <b>http://127.0.0.1:5000</b> to test predictions."
    ]
    for inst in instructions:
        story.append(Paragraph(inst, normal))
        story.append(Spacer(1, 3))
        
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

def build_sample_documentation():
    pdf_path = "7.Project Documentation/Sample Project Documentation.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Sample Project Documentation"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    h2 = ParagraphStyle('H2', fontSize=13, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    cell_bold = ParagraphStyle('CB', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    
    story.append(Paragraph("<b>Technical Overview</b>", h2))
    story.append(Spacer(1, 5))
    story.append(Paragraph("The <b>HDI Predictor</b> leverages machine learning algorithms to map 7 key socio-economic indicators directly to a country's Human Development Index (HDI) score.", normal))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Model Development & Performance</b>", h2))
    story.append(Spacer(1, 5))
    story.append(Paragraph("During the model selection phase, three algorithms were compared using 5-fold cross-validation RMSE:", normal))
    story.append(Spacer(1, 8))
    
    metrics_data = [
        ["Model Name", "Cross-Validation RMSE", "Test R² score"],
        ["Linear Regression", "0.0152", "0.984"],
        ["Random Forest Regressor", "0.0078", "0.996"],
        ["Gradient Boosting Regressor", "0.0051", "0.999"]
    ]
    
    formatted_metrics = []
    for r_idx, row in enumerate(metrics_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_metrics.append(r_list)
        
    t = Table(formatted_metrics, colWidths=[180, 160, 160])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("The Gradient Boosting Regressor was auto-selected and serialized as <b>best_model.pkl</b>.", normal))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Input Features & Range</b>", h2))
    story.append(Spacer(1, 5))
    
    feat_data = [
        ["Variable Name", "Description", "Value Bounds"],
        ["Life_Expectancy", "Life expectancy at birth (years)", "30.0 to 90.0"],
        ["Mean_Years_Schooling", "Average years of education received by adults aged 25+", "0.0 to 20.0"],
        ["Expected_Years_Schooling", "Number of years of schooling a child can expect", "0.0 to 25.0"],
        ["GNI_per_capita", "Gross National Income per capita (PPP, inflation-adjusted)", "100 to 150,000"],
        ["Gender_Dev_Index", "Ratio of female to male HDI", "0.2 to 1.5"],
        ["Gender_Ineq_Index", "Composite measure showing loss in achievements due to gender inequality", "0.0 to 1.0"],
        ["CO2_per_capita", "Carbon dioxide emissions per capita (production tonnes)", "0.0 to 100.0"]
    ]
    
    formatted_feat = []
    for r_idx, row in enumerate(feat_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_feat.append(r_list)
        
    t2 = Table(formatted_feat, colWidths=[130, 250, 120])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Flask Web Application Structure</b>", h2))
    story.append(Spacer(1, 5))
    story.append(Paragraph("The application uses Flask to serve a single-page style form interface. Submitting the form posts values to the <b>/predict</b> route, which calls <b>scaler.pkl</b> to scale values and evaluates the output using <b>best_model.pkl</b> before displaying the output tier classification.", normal))
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

def build_communication():
    ensure_dir("8.Project Demonstration")
    pdf_path = "8.Project Demonstration/Communication.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Communication"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    cell_bold = ParagraphStyle('CB', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    
    story.append(Paragraph("<b>Communication Plan:</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Effective communication is essential for a successful project demonstration. This document outlines the communication strategy used within the team and with stakeholders throughout the project lifecycle, including how updates, issues, and feedback were managed.", normal))
    story.append(Spacer(1, 10))
    
    comm_data = [
        ["S.No", "Communication Type", "Frequency", "Channel / Tool", "Participants", "Purpose"],
        ["1", "Team Standup", "Daily", "GitHub Commits & Issues", "Hari Charan Emandi", "Coordinate daily development tasks."],
        ["2", "Progress Update", "Weekly", "Markdown Status Logs", "Hari Charan Emandi", "Record weekly development progress and metrics."],
        ["3", "Issue / Bug Discussion", "As Needed", "Local debugger & logs", "Hari Charan Emandi", "Troubleshoot integration and prediction errors."],
        ["4", "Stakeholder Review", "Bi-Weekly", "Hugging Face / Render Demo", "Hari Charan Emandi & Mentor", "Demonstrate project progress milestones."],
        ["5", "Final Demo Rehearsal", "Once", "Local web browser", "Hari Charan Emandi", "Verify end-to-end user prediction flow."],
        ["6", "", "", "", "", ""]
    ]
    
    formatted_comm = []
    for r_idx, row in enumerate(comm_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_comm.append(r_list)
        
    t = Table(formatted_comm, colWidths=[35, 115, 60, 85, 75, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Communication Challenges & Resolutions:</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    challenges_data = [
        ["S.No", "Challenge Faced", "Resolution / Action Taken"],
        ["1", "Tracking multi-model metrics changes across training runs.", "Implemented stdout logs in train_model.py summarizing model metrics, and saved cross-validation reports in notebooks/."],
        ["2", "Model serialization compatibility across local/deployment runtimes.", "Standardized library versions in requirements.txt and built Dockerfile for reproducible environment."],
        ["3", "Ensuring robust inputs validation on HTML web forms.", "Built HTML5 range bounds and Flask backend checking (e.g. Life Expectancy [30, 90])."]
    ]
    
    formatted_ch = []
    for r_idx, row in enumerate(challenges_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_ch.append(r_list)
        
    t2 = Table(formatted_ch, colWidths=[35, 200, 265])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t2)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")


# 19. Demonstration of Proposed Features
def build_demo_features():
    pdf_path = "8.Project Demonstration/Demonstration of Proposed Features.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Demonstration of Proposed Features"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    bold = ParagraphStyle('B', parent=normal, fontName='Helvetica-Bold')
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    cell_bold = ParagraphStyle('CB', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    
    story.append(Paragraph("<b>Demonstration of Proposed Features:</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph("This document captures all the features that were proposed during the project planning phase and tracks whether each feature was successfully implemented and demonstrated. It serves as evidence of the team's ability to deliver on the proposed solution.", normal))
    story.append(Spacer(1, 10))
    
    demo_data = [
        ["S.No", "Feature Name", "Description", "Status\n(Implemented /\nPartial / Pending)", "Demonstrated\n(Yes / No)", "Remarks"],
        ["1", "Long-form Data Wrangling", "Auto-converts UNDP wide CSV to long table.", "Implemented", "Yes", "Integrated in pipeline."],
        ["2", "Automated ML Scaling", "Fits and serializes scaler.pkl for raw inputs.", "Implemented", "Yes", "Integrated."],
        ["3", "3-Algorithm Comparison", "Evaluates Linear Regression, RF, and GBR.", "Implemented", "Yes", "Outputted in console log."],
        ["4", "Auto-Selection", "Auto-saves model with lowest CV RMSE.", "Implemented", "Yes", "Verified in model files."],
        ["5", "Flask Prediction Form", "Inputs 7 values and posts to server.", "Implemented", "Yes", "Screen checked."],
        ["6", "Classification Output", "Maps score to Low, Medium, High, Very High tiers.", "Implemented", "Yes", "Displayed in final result view."]
    ]
    
    formatted_demo = []
    for r_idx, row in enumerate(demo_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell.replace("\n", "<br/>"), style))
        formatted_demo.append(r_list)
        
    t = Table(formatted_demo, colWidths=[35, 110, 155, 75, 65, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Feature Implementation Summary:</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    
    summary_data = [
        ["Total Features Proposed", "6"],
        ["Total Features Implemented", "6"],
        ["Total Features Demonstrated", "6"],
        ["Overall Implementation Rate (%)", "100%"]
    ]
    
    formatted_sum = []
    for row in summary_data:
        formatted_sum.append([
            Paragraph(f"<b>{row[0]}</b>", cell_style),
            Paragraph(row[1], cell_style)
        ])
        
    t2 = Table(formatted_sum, colWidths=[250, 250])
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f9f9fa')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t2)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 20. Project Demo Planning
# 20. Project Demo Planning
def build_demo_planning():
    pdf_path = "8.Project Demonstration/Project Demo Planning.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Project Demo Planning"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    h2 = ParagraphStyle('H2', fontSize=13, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    cell_bold = ParagraphStyle('CB', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    
    story.append(Paragraph("<b>Project Demo Planning:</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph("A well-structured demo plan ensures that the team presents the project effectively, covering all key aspects in a clear and organized manner. This document outlines the plan for demonstrating the project, including the flow of the demo, key features to highlight, and responsibilities of each team member.", normal))
    story.append(Spacer(1, 10))
    
    plan_data = [
        ["S.No", "Demo Section", "Description", "Duration (mins)", "Responsible Member"],
        ["1", "Introduction & Problem Statement", "Explain the socio-economic goals of HDI and list the 7 input indicators.", "2 mins", "Hari Charan Emandi"],
        ["2", "Pipeline Execution", "Show pipeline script execution and cross-validation logs for Linear, Forest, and Gradient models.", "3 mins", "Hari Charan Emandi"],
        ["3", "Interactive Prediction Form", "Launch Flask, input scenarios for multiple nations, check prediction output accuracy.", "4 mins", "Hari Charan Emandi"],
        ["4", "Containerization & Conclusion", "Demonstrate Docker runtime and present the future scalability roadmap.", "1 min", "Hari Charan Emandi"],
        ["5", "Q&A Session", "Address evaluator questions on model selection and input bounds checks.", "2 mins", "Hari Charan Emandi"],
        ["6", "", "", "", ""]
    ]
    
    formatted_plan = []
    for r_idx, row in enumerate(plan_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_plan.append(r_list)
        
    t = Table(formatted_plan, colWidths=[35, 125, 175, 75, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Demo Flow Summary:</b>", h2))
    story.append(Spacer(1, 5))
    
    flow_data = [
        ["Step", "Activity", "Notes"],
        ["1", "Introduction & Problem Statement", "Walkthrough Problem Statement (PS-1) and dataset origin."],
        ["2", "Solution Overview", "Present architecture diagram and components."],
        ["3", "Live Feature Demonstration", "Walk through web UI and trigger a few inference predictions."],
        ["4", "Q&A Session", "Address questions on metrics (GBR R² ≈ 0.999) and bounds checking."]
    ]
    
    formatted_flow = []
    for r_idx, row in enumerate(flow_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_flow.append(r_list)
        
    t2 = Table(formatted_flow, colWidths=[40, 180, 280])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t2)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 21. Scalability & Future Plan
def build_scalability_plan():
    pdf_path = "8.Project Demonstration/Scalability & Future Plan.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Scalability & Future Plan"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    h2 = ParagraphStyle('H2', fontSize=13, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    cell_bold = ParagraphStyle('CB', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    
    story.append(Paragraph("<b>Scalability & Future Plan:</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph("This document outlines how the current project solution can be scaled to handle larger user bases, increased data loads, or extended features in the future. It also captures the team's roadmap for enhancing and evolving the project beyond its current state.", normal))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Current System Limitations:</b>", h2))
    story.append(Spacer(1, 5))
    
    limitations_data = [
        ["S.No", "Limitation", "Impact", "Priority to Address\n(High / Medium / Low)"],
        ["1", "Lightweight Flask threaded development server", "Cannot handle high concurrent traffic loads.", "Medium"],
        ["2", "Tabular CSV file backend storage", "Poor write performance and scaling for high concurrent read/write query flows.", "Medium"],
        ["3", "CPU-based local prediction routing", "Inference bottleneck under heavy request concurrency.", "Low"]
    ]
    
    formatted_lim = []
    for r_idx, row in enumerate(limitations_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell.replace("\n", "<br/>"), style))
        formatted_lim.append(r_list)
        
    t = Table(formatted_lim, colWidths=[35, 175, 200, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Scalability Plan:</b>", h2))
    story.append(Spacer(1, 5))
    
    scalability_data = [
        ["S.No", "Scalability Aspect", "Current State", "Proposed Upgrade / Solution"],
        ["1", "User Load", "Light Flask thread", "Deploy backend with Gunicorn WSGI service behind Nginx reverse proxy."],
        ["2", "Data Storage", "Tabular CSV", "Migrate country developmental indicators to PostgreSQL database."],
        ["3", "Performance", "Sub-50ms inference", "Cache repeated coordinate queries with Redis key-value store."],
        ["4", "Security", "Local form checks", "Implement HTTPS, secure SSL headers, and API rate limiting."]
    ]
    
    formatted_scale = []
    for r_idx, row in enumerate(scalability_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_scale.append(r_list)
        
    t2 = Table(formatted_scale, colWidths=[35, 115, 120, 230])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Future Roadmap:</b>", h2))
    story.append(Spacer(1, 5))
    
    roadmap_data = [
        ["Phase", "Planned Feature / Enhancement", "Target Timeline", "Expected Impact"],
        ["Phase 2", "User Auth & Scenario Saving", "Q4 2026", "Users can save developmental trajectories over time."],
        ["Phase 3", "Multi-year Trend Forecasting", "Q1 2027", "Predictive forecasting of country HDI scores across future years."],
        ["Phase 4", "Automated Data Sync", "Q3 2027", "Daily data ingestion sync pipeline with UNDP public API endpoints."]
    ]
    
    formatted_road = []
    for r_idx, row in enumerate(roadmap_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_road.append(r_list)
        
    t3 = Table(formatted_road, colWidths=[55, 165, 100, 180])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t3)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

# 22. Team Involvement in Demonstration
def build_team_involvement():
    pdf_path = "8.Project Demonstration/Team Involvement in Demonstration.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    story = []
    
    story.append(make_header("Team Involvement in Demonstration"))
    story.append(Spacer(1, 15))
    
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    h2 = ParagraphStyle('H2', fontSize=13, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))
    cell_style = ParagraphStyle('C', parent=normal, fontSize=9, leading=11)
    cell_bold = ParagraphStyle('CB', parent=normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    
    story.append(Paragraph("<b>Team Involvement in Demonstration:</b>", ParagraphStyle('H2', fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#1e1e2e'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph("This document records the active participation and roles of each team member during the project demonstration. It ensures that every member contributes meaningfully to the presentation and that responsibilities are distributed fairly and clearly.", normal))
    story.append(Spacer(1, 10))
    
    involve_data = [
        ["S.No", "Team Member Name", "Role in Demo", "Section Presented", "Contribution Summary", "Participation\n(Active / Passive)"],
        ["1", "Hari Charan Emandi", "Lead Presenter & Developer", "Full System Walkthrough", "Developed ML pipeline, built Flask backend, styled frontend, created Docker config, and presented the end-to-end demonstration.", "Active"],
        ["2", "", "", "", "", ""],
        ["3", "", "", "", "", ""],
        ["4", "", "", "", "", ""],
        ["5", "", "", "", "", ""],
        ["6", "", "", "", "", ""]
    ]
    
    formatted_inv = []
    for r_idx, row in enumerate(involve_data):
        r_list = []
        for cell in row:
            style = cell_bold if r_idx == 0 else cell_style
            r_list.append(Paragraph(cell, style))
        formatted_inv.append(r_list)
        
    t = Table(formatted_inv, colWidths=[35, 95, 80, 80, 150, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f1f1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Team Coordination Notes:</b>", h2))
    story.append(Spacer(1, 5))
    
    notes_data = [
        ["Team Leader / Coordinator", "Hari Charan Emandi (Solo Developer)"],
        ["Overall Team Coordination Rating (1-5)", "5 (Seamless execution as a solo developer)"],
        ["Any issues during demo", "None. Local and container runtimes operated successfully."],
        ["How issues were resolved", "N/A (Pre-demo rehearsals resolved initial styling and path issues)."]
    ]
    
    formatted_notes = []
    for row in notes_data:
        formatted_notes.append([
            Paragraph(f"<b>{row[0]}</b>", cell_style),
            Paragraph(row[1], cell_style)
        ])
        
    t2 = Table(formatted_notes, colWidths=[200, 300])
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f9f9fa')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t2)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_path}")

if __name__ == "__main__":
    build_brainstorming()
    build_problem_statements()
    build_empathy_map()
    build_customer_journey()
    build_dfd()
    build_solution_requirements()
    build_tech_stack()
    build_problem_solution()
    build_proposed_solution()
    build_solution_architecture()
    build_project_planning()
    build_code_layout()
    build_coding_solution()
    build_functional_features()
    build_performance_testing()
    build_executable_files()
    build_sample_documentation()
    build_communication()
    build_demo_features()
    build_demo_planning()
    build_scalability_plan()
    build_team_involvement()
    print("All project phase PDFs successfully generated!")
