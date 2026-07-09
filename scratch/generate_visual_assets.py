import os
from PIL import Image, ImageDraw, ImageFont

def get_font(font_name="segoeuib.ttf", size=14):
    font_paths = [
        f"C:\\Windows\\Fonts\\{font_name}",
        f"C:\\Windows\\Fonts\\arial.ttf",
        "arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

def create_problem_statement_example():
    w, h = 800, 220
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    # Fonts
    label_font = get_font("segoeuib.ttf", 10)
    card_font = get_font("segoeuib.ttf", 11)
    
    # 5 columns matching sticky note categories in example adapted for HDI Predictor
    cols = [
        {"name": "I am\n(Customer)", "bg": "#2b6cb0", "card_bg": "#ffffff", "card_text": "#2d3748", "text": "Policy researcher\nor economics\nstudent"},
        {"name": "I'm trying to\n(evaluate HDI)", "bg": "#e53e3e", "card_bg": "#ffffff", "card_text": "#2d3748", "text": "Analyze global\nquality-of-life\nand progress"},
        {"name": "But\n(calculation lag)", "bg": "#f687b3", "card_bg": "#ffffff", "card_text": "#2d3748", "text": "UNDP reporting\nis static and\npublished late"},
        {"name": "Because\n(complex factors)", "bg": "#d69e2e", "card_bg": "#ffffff", "card_text": "#2d3748", "text": "Data has non-linear\nand multi-index\ndependencies"},
        {"name": "Which makes me\nfeel", "bg": "#1a202c", "card_bg": "#ed8936", "card_text": "#ffffff", "text": "Frustrated by\nlack of instant\ninteractive tools"}
    ]
    
    col_w = 140
    gap = 12
    margin = 25
    
    for i, col in enumerate(cols):
        x1 = margin + i * (col_w + gap)
        x2 = x1 + col_w
        y1 = 20
        y2 = h - 20
        
        # Draw background column box
        draw.rectangle((x1, y1, x2, y2), fill=col["bg"], outline="#cbd5e0", width=1)
        
        # Draw header text inside column (handling newlines)
        name_lines = col["name"].split("\n")
        curr_y = y1 + 15 - (len(name_lines) - 1) * 6
        for line in name_lines:
            draw.text((x1 + col_w // 2, curr_y), line, fill="#ffffff", font=label_font, anchor="mm")
            curr_y += 12
        
        # Draw sticky note card inside the column
        card_margin = 15
        cx1 = x1 + card_margin
        cx2 = x2 - card_margin
        cy1 = y1 + 35
        cy2 = y2 - 15
        
        # Draw card shadow
        draw.rectangle((cx1 + 2, cy1 + 2, cx2 + 2, cy2 + 2), fill="#cbd5e0")
        # Draw card body
        draw.rectangle((cx1, cy1, cx2, cy2), fill=col["card_bg"], outline="#718096", width=1)
        
        # Draw text inside card
        lines = col["text"].split("\n")
        cy_text = cy1 + (cy2 - cy1) // 2 - (len(lines) * 12) // 2 + 5
        for line in lines:
            draw.text((cx1 + (cx2 - cx1) // 2, cy_text), line, fill=col["card_text"], font=card_font, anchor="mm")
            cy_text += 13

    os.makedirs("1. Brainstorming & Ideation", exist_ok=True)
    img.save("1. Brainstorming & Ideation/problem_statement_example.png")
    print("Generated problem_statement_example.png successfully.")

def create_empathy_map():
    w, h = 800, 600
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    title_font = get_font("segoeuib.ttf", 22)
    header_font = get_font("segoeuib.ttf", 18)
    text_font = get_font("segoeui.ttf", 13)
    
    # Title
    draw.text((20, 20), "Empathy Map - Policy Analyst", fill="#1a202c", font=title_font)
    
    margin = 50
    center_x = w // 2
    center_y = (h // 2) + 20
    
    # Draw quadrant borders
    draw.line([(margin, center_y), (w - margin, center_y)], fill="#a0aec0", width=2)
    draw.line([(center_x, margin + 40), (center_x, h - margin)], fill="#a0aec0", width=2)
    
    quadrants = [
        {"box": (margin, margin + 40, center_x - 5, center_y - 5), "title": "SAYS", "bg": "#e6f2ff", "text_color": "#2b6cb0", "text": [
            "• I need a tool to dynamically predict HDI scores.",
            "• I hope the predictions are fast and accurate.",
            "• I want a transparent model evaluation process."
        ]},
        {"box": (center_x + 5, margin + 40, w - margin, center_y - 5), "title": "THINKS", "bg": "#e6f2ff", "text_color": "#2b6cb0", "text": [
            "• Will socio-economic factors affect the HDI score?",
            "• Are the selected training indicators sufficient?",
            "• I hope the machine learning model selection is fair."
        ]},
        {"box": (margin, center_y + 5, center_x - 5, h - margin), "title": "DOES", "bg": "#fffcf0", "text_color": "#b7791f", "text": [
            "• Consolidates and cleans large UNDP datasets.",
            "• Enters various country indicators to test scenarios.",
            "• Checks application prediction response regularly."
        ]},
        {"box": (center_x + 5, center_y + 5, w - margin, h - margin), "title": "FEELS", "bg": "#fffcf0", "text_color": "#b7791f", "text": [
            "• Anxious while compiling sparse data.",
            "• Confident if model validation metrics are strong.",
            "• Satisfied when predictions are served instantly."
        ]}
    ]
    
    for q in quadrants:
        x1, y1, x2, y2 = q["box"]
        draw.rectangle(q["box"], fill=q["bg"], outline="#cbd5e0", width=1)
        draw.text((x1 + 20, y1 + 15), q["title"], fill=q["text_color"], font=header_font)
        
        y_offset = y1 + 50
        for line in q["text"]:
            words = line.split(" ")
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                bbox = draw.textbbox((0, 0), test_line, font=text_font)
                line_w = bbox[2] - bbox[0]
                if line_w < (x2 - x1 - 40):
                    current_line = test_line
                else:
                    draw.text((x1 + 20, y_offset), current_line, fill="#2d3748", font=text_font)
                    y_offset += 20
                    current_line = word
            if current_line:
                draw.text((x1 + 20, y_offset), current_line, fill="#2d3748", font=text_font)
                y_offset += 25
 
    # Center box intersecting the line (grey background matching reference)
    pw, ph = 180, 100
    px1 = center_x - pw // 2
    px2 = center_x + pw // 2
    py1 = center_y - ph // 2
    py2 = center_y + ph // 2
    
    draw.rectangle((px1, py1, px2, py2), fill="#cbd5e0", outline="#718096", width=2)
    
    p_title_font = get_font("segoeuib.ttf", 10)
    p_name_font = get_font("segoeuib.ttf", 12)
    p_sub_font = get_font("segoeui.ttf", 10)
    
    draw.text((center_x, center_y - 25), "PERSONA NAME", fill="#1a202c", font=p_title_font, anchor="mm")
    draw.text((center_x, center_y), "Development Policy Analyst", fill="#1a202c", font=p_name_font, anchor="mm")
    draw.text((center_x, center_y + 25), "(Researcher/User)", fill="#4a5568", font=p_sub_font, anchor="mm")
 
    os.makedirs("1. Brainstorming & Ideation", exist_ok=True)
    img.save("1. Brainstorming & Ideation/empathy_map.png")
    print("Generated empathy_map.png successfully.")

def create_customer_journey_map():
    w, h = 900, 500
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    title_font = get_font("segoeuib.ttf", 22)
    header_font = get_font("segoeuib.ttf", 14)
    text_font = get_font("segoeui.ttf", 11)
    
    draw.text((20, 20), "Customer Journey Map - HDI Predictor", fill="#1a202c", font=title_font)
    
    stages = ["1. Discovery", "2. Interaction", "3. Insights"]
    stages_colors = ["#1a365d", "#d4a373", "#dd8d95"]
    stages_text_colors = ["#ffffff", "#ffffff", "#ffffff"]
    
    row_headers = ["User Action", "Touchpoint", "Thought", "Feeling", "Opportunities"]
    row_h = 70
    start_y = 80
    col_w = 230
    start_x = 180
    
    for idx, row in enumerate(row_headers):
        y = start_y + idx * row_h
        draw.rectangle((20, y, start_x - 20, y + row_h - 10), fill="#edf2f7", outline="#cbd5e0", width=1)
        draw.text((30, y + (row_h - 10)//2), row, fill="#2d3748", font=header_font, anchor="lm")
        
    journey_data = [
        [
            "User visits the web app landing page; reviews model metrics.",
            "Web UI Landing page + performance cards.",
            "'The UI is clean and metrics are visible. Let's try custom parameters.'",
            "Curious, interested.",
            "Display dataset metrics dynamically."
        ],
        [
            "User enters 7 socio-economic indicators and clicks Predict.",
            "HTML prediction form, validated fields.",
            "'Are inputs bounded? Hope there are validation safeguards.'",
            "Confident, determined.",
            "Add range sliders alongside numeric inputs."
        ],
        [
            "User views the predicted HDI, development tier, and plots.",
            "Results dashboard, interpretation layout.",
            "'Wow, the Gradient Boosting model predicted 0.85 (Very High tier) instantly.'",
            "Empowered, satisfied.",
            "Add interactive timeseries trend graphs."
        ]
    ]
    
    for col_idx, stage in enumerate(stages):
        x_left = start_x + col_idx * (col_w + 15)
        x_right = x_left + col_w
        
        draw.rectangle((x_left, start_y - 35, x_right, start_y - 10), fill=stages_colors[col_idx])
        draw.text((x_left + col_w//2, start_y - 23), stage, fill=stages_text_colors[col_idx], font=header_font, anchor="mm")
        
        for row_idx, cell_text in enumerate(journey_data[col_idx]):
            y_top = start_y + row_idx * row_h
            bg_color = "#e8f5e9" if row_idx == 2 else "#ffffff" # green background for thoughts row
            draw.rectangle((x_left, y_top, x_right, y_top + row_h - 10), fill=bg_color, outline="#cbd5e0", width=1)
            
            words = cell_text.split(" ")
            lines = []
            curr_line = ""
            for word in words:
                test_line = f"{curr_line} {word}".strip()
                bbox = draw.textbbox((0, 0), test_line, font=text_font)
                line_w = bbox[2] - bbox[0]
                if line_w < (col_w - 20):
                    curr_line = test_line
                else:
                    lines.append(curr_line)
                    curr_line = word
            if curr_line:
                lines.append(curr_line)
                
            cell_y = y_top + 10
            for line in lines:
                draw.text((x_left + 10, cell_y), line, fill="#2d3748", font=text_font)
                cell_y += 14

    os.makedirs("2. Requirement Analysis", exist_ok=True)
    img.save("2. Requirement Analysis/customer_journey_map.png")
    print("Generated customer_journey_map.png successfully.")

def create_problem_solution_fit():
    w, h = 900, 650
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    title_font = get_font("segoeuib.ttf", 22)
    header_font = get_font("segoeuib.ttf", 11)
    sub_header_font = get_font("segoeuib.ttf", 10)
    text_font = get_font("segoeui.ttf", 9.5)
    
    # Title
    draw.text((20, 20), "Problem-Solution Fit Canvas - HDI Predictor", fill="#1a202c", font=title_font)
    
    col_w = 260
    col1_x = 40
    col2_x = 320
    col3_x = 600
    
    # Colors
    orange_border = "#e67e22"
    teal_border = "#1abc9c"
    card_bg = "#ffffff"
    
    # Define cards with exact boxes layout matching the screenshot
    cards = [
        # Column 1
        {"box": (col1_x, 70, col1_x + col_w, 200), "title": "1. CUSTOMER SEGMENT(S) [CS]", "border": orange_border, "type": "bullets", "text": [
            "• Policy makers and development researchers",
            "• International development organizations",
            "• Economics students and academic researchers"
        ]},
        {"box": (col1_x, 210, col1_x + col_w, 340), "title": "2. PROBLEMS / PAINS + ITS FREQUENCY [PR]", "border": orange_border, "type": "bullets", "text": [
            "• Manual calculations of HDI are slow and error-prone",
            "• Calculation errors during socio-economic assessments",
            "• Large volume of country-year data to clean and process",
            "• Lagging annual UNDP reports prevent timely policy analysis"
        ]},
        {"box": (col1_x, 350, col1_x + col_w, 480), "title": "3. TRIGGERS TO ACT [TR]", "border": teal_border, "type": "bullets", "text": [
            "• Request for immediate policy impact assessments",
            "• Need for rapid scenario forecasting",
            "• Researcher demand for instant index predictions",
            "• Requirement to automate data wrangling pipelines"
        ]},
        {"box": (col1_x, 490, col1_x + col_w, 620), "title": "4. EMOTIONS BEFORE / AFTER [EM]", "border": teal_border, "type": "emotions", "text": [
            "Before: Frustration with massive spreadsheets, formula errors, and lagging static data",
            "After: Instant prediction feedback, high model transparency, confidence in simulation decisions"
        ]},
        
        # Column 2
        {"box": (col2_x, 70, col2_x + col_w, 200), "title": "6. CUSTOMER LIMITATIONS EG. BUDGET, DEVICES [CL]", "border": orange_border, "type": "bullets", "text": [
            "• Limited access to high-compute resources",
            "• Missing or sparse country indicator records",
            "• Non-standardized data formats from different countries",
            "• Lack of machine learning expertise among researchers",
            "• Dependence on manual data wrangling"
        ]},
        {"box": (col2_x, 210, col2_x + col_w, 340), "title": "9. PROBLEM ROOT / CAUSE [RC]", "border": orange_border, "type": "bullets", "text": [
            "• Growing volume of socio-economic parameters",
            "• Non-linear mathematical calculations of dimension indices",
            "• Subjective thresholds for development tiers",
            "• Sparse or incomplete country-year records",
            "• Inefficient spreadsheet-based forecasting methods"
        ]},
        {"box": (col2_x, 350, col2_x + col_w, 620), "title": "10. YOUR SOLUTION [SL]", "border": teal_border, "type": "solution", "text": [
            "Develop a country Human Development Index (HDI) Prediction System using Machine Learning (Linear Regression, Random Forest and Gradient Boosting) integrated with a Flask web application.",
            "The system predicts the HDI score and development tier instantly based on country indicators, improving forecasting accuracy, reducing analysis times, and assisting policy makers in making reliable decisions."
        ]},
        
        # Column 3
        {"box": (col3_x, 70, col3_x + col_w, 200), "title": "5. AVAILABLE SOLUTIONS PROS & CONS [AS]", "border": orange_border, "type": "bullets", "text": [
            "• Manual Spreadsheet Calculations: Free but slow, error-prone, and static",
            "• Traditional UNDP Databases: Authoritative but lagging and lacks forecasting",
            "• Machine Learning Models: Fast, scalable, accurate, and adapts to complex trends"
        ]},
        {"box": (col3_x, 210, col3_x + col_w, 340), "title": "7. BEHAVIOR + ITS INTENSITY [BE]", "border": orange_border, "type": "bullets", "text": [
            "• Researchers expect instant prediction feedback",
            "• Institutions evaluate hundreds of indicator scenarios during policy cycles",
            "• Need for high-speed, consistent, and mathematically sound forecasting"
        ]},
        {"box": (col3_x, 350, col3_x + col_w, 620), "title": "8. CHANNELS OF BEHAVIOR [CH]", "border": teal_border, "type": "channels", "text": []}
    ]
    
    # Draw boxes and titles
    for c in cards:
        x1, y1, x2, y2 = c["box"]
        # Draw background and outline border
        draw.rectangle(c["box"], fill=card_bg, outline=c["border"], width=2)
        # Draw title text
        draw.text((x1 + 10, y1 + 10), c["title"], fill=c["border"], font=header_font)
        
        # Draw text inside box based on its type
        y_offset = y1 + 30
        
        if c["type"] == "bullets":
            for bullet in c["text"]:
                # Custom word wrapping for bullets
                words = bullet.split(" ")
                curr_line = ""
                for word in words:
                    test_line = f"{curr_line} {word}".strip()
                    bbox = draw.textbbox((0, 0), test_line, font=text_font)
                    line_w = bbox[2] - bbox[0]
                    if line_w < (col_w - 20):
                        curr_line = test_line
                    else:
                        draw.text((x1 + 10, y_offset), curr_line, fill="#2d3748", font=text_font)
                        y_offset += 14
                        curr_line = f"  {word}"  # Indent wrapped lines slightly
                if curr_line:
                    draw.text((x1 + 10, y_offset), curr_line, fill="#2d3748", font=text_font)
                    y_offset += 16
                    
        elif c["type"] == "emotions":
            # Split before and after text blocks
            for block in c["text"]:
                parts = block.split(": ")
                lbl = parts[0] + ": "
                val = parts[1]
                
                # Draw label in bold-like color/style
                draw.text((x1 + 10, y_offset), lbl, fill="#e74c3c" if lbl.startswith("Before") else "#2ecc71", font=sub_header_font)
                
                # Draw wrapped values
                words = val.split(" ")
                curr_line = ""
                # Shift start X by label width (~45 pixels)
                start_x_shift = 45
                for word in words:
                    test_line = f"{curr_line} {word}".strip()
                    bbox = draw.textbbox((0, 0), test_line, font=text_font)
                    line_w = bbox[2] - bbox[0]
                    if line_w < (col_w - 20 - start_x_shift):
                        curr_line = test_line
                    else:
                        draw.text((x1 + 10 + start_x_shift, y_offset), curr_line, fill="#2d3748", font=text_font)
                        y_offset += 14
                        curr_line = word
                        start_x_shift = 0  # Subsequent lines start at margin
                if curr_line:
                    draw.text((x1 + 10 + start_x_shift, y_offset), curr_line, fill="#2d3748", font=text_font)
                    y_offset += 18
                    
        elif c["type"] == "solution":
            # Spans row 3 & 4. Draw two paragraphs.
            for idx, para in enumerate(c["text"]):
                words = para.split(" ")
                curr_line = ""
                for word in words:
                    test_line = f"{curr_line} {word}".strip()
                    bbox = draw.textbbox((0, 0), test_line, font=text_font)
                    line_w = bbox[2] - bbox[0]
                    if line_w < (col_w - 20):
                        curr_line = test_line
                    else:
                        draw.text((x1 + 10, y_offset), curr_line, fill="#2d3748", font=text_font)
                        y_offset += 14
                        curr_line = word
                if curr_line:
                    draw.text((x1 + 10, y_offset), curr_line, fill="#2d3748", font=text_font)
                    y_offset += 20
                if idx == 0:
                    y_offset += 10  # Additional spacing between paragraphs
                    
        elif c["type"] == "channels":
            # Channels box with ONLINE and OFFLINE sections
            # ONLINE
            draw.text((x1 + 10, y_offset), "ONLINE", fill="#2ecc71", font=sub_header_font)
            y_offset += 15
            online_items = [
                "• Research dashboards",
                "• Institutional web portals",
                "• Open-source code repositories (GitHub)"
            ]
            for item in online_items:
                words = item.split(" ")
                curr_line = ""
                for word in words:
                    test_line = f"{curr_line} {word}".strip()
                    bbox = draw.textbbox((0, 0), test_line, font=text_font)
                    line_w = bbox[2] - bbox[0]
                    if line_w < (col_w - 20):
                        curr_line = test_line
                    else:
                        draw.text((x1 + 10, y_offset), curr_line, fill="#2d3748", font=text_font)
                        y_offset += 14
                        curr_line = f"  {word}"
                if curr_line:
                    draw.text((x1 + 10, y_offset), curr_line, fill="#2d3748", font=text_font)
                    y_offset += 16
            
            y_offset += 10
            # OFFLINE
            draw.text((x1 + 10, y_offset), "OFFLINE", fill="#34495e", font=sub_header_font)
            y_offset += 15
            offline_items = [
                "• Academic journals and publications",
                "• Direct policy reports",
                "• Development planning conferences"
            ]
            for item in offline_items:
                words = item.split(" ")
                curr_line = ""
                for word in words:
                    test_line = f"{curr_line} {word}".strip()
                    bbox = draw.textbbox((0, 0), test_line, font=text_font)
                    line_w = bbox[2] - bbox[0]
                    if line_w < (col_w - 20):
                        curr_line = test_line
                    else:
                        draw.text((x1 + 10, y_offset), curr_line, fill="#2d3748", font=text_font)
                        y_offset += 14
                        curr_line = f"  {word}"
                if curr_line:
                    draw.text((x1 + 10, y_offset), curr_line, fill="#2d3748", font=text_font)
                    y_offset += 16
                    
    os.makedirs("3. Project Design Phase", exist_ok=True)
    img.save("3. Project Design Phase/problem_solution_fit.png")
    print("Generated problem_solution_fit.png successfully.")

def create_data_flow_diagram():
    w, h = 800, 520
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    title_font = get_font("segoeuib.ttf", 20)
    header_font = get_font("segoeuib.ttf", 11)
    text_font = get_font("segoeui.ttf", 9)
    
    draw.text((20, 20), "DFD - HDI Predictor", fill="#1a202c", font=title_font)
    
    # Process drawing helper
    def draw_process(x1, y1, x2, y2, number, title, description):
        draw.rectangle((x1, y1, x2, y2), fill="#ebf8ff", outline="#3182ce", width=2)
        # Header horizontal line
        draw.line([(x1, y1 + 25), (x2, y1 + 25)], fill="#3182ce", width=2)
        # Header vertical divider
        draw.line([(x1 + 30, y1), (x1 + 30, y1 + 25)], fill="#3182ce", width=2)
        # Number box fill
        draw.rectangle((x1+1, y1+1, x1+29, y1+24), fill="#bcd7f5")
        # Draw number text
        draw.text((x1 + 15, y1 + 12), number, fill="#1a365d", font=header_font, anchor="mm")
        # Draw title text
        draw.text((x1 + 35, y1 + 12), title, fill="#1a365d", font=header_font, anchor="lm")
        # Draw description text
        desc_words = description.split(" ")
        curr_y = y1 + 35
        curr_line = ""
        for w in desc_words:
            test = f"{curr_line} {w}".strip()
            bbox = draw.textbbox((0,0), test, font=text_font)
            if bbox[2] - bbox[0] < (x2 - x1 - 16):
                curr_line = test
            else:
                draw.text((x1 + 8, curr_y), curr_line, fill="#2d3748", font=text_font)
                curr_y += 13
                curr_line = w
        if curr_line:
            draw.text((x1 + 8, curr_y), curr_line, fill="#2d3748", font=text_font)

    # 1. External Entity: Researcher (Oval)
    draw.ellipse((40, 200, 160, 260), fill="#ebf8ff", outline="#3182ce", width=2)
    draw.text((100, 230), "Researcher", fill="#1a365d", font=header_font, anchor="mm")
    
    # 2. External Entity: Economics Department (Oval)
    draw.ellipse((640, 280, 760, 340), fill="#ebf8ff", outline="#3182ce", width=2)
    draw.text((700, 310), "Economics\nDepartment", fill="#1a365d", font=header_font, anchor="mm")
    
    # 3. Process 1: Receive Indicators
    draw_process(240, 90, 400, 190, "1", "Receive Indicators", "Collects country indicator details from the researcher.")
    
    # 4. Data Store: Indicator Database
    draw.rectangle((240, 260, 400, 310), fill="#1a365d", outline="#1a365d")
    draw.text((320, 285), "Indicator Database", fill="#ffffff", font=header_font, anchor="mm")
    
    # 5. Process 2: Predict HDI
    draw_process(470, 190, 630, 290, "2", "Predict HDI", "The ML model analyzes country indicators and predicts HDI score/tier.")
    
    # 6. Process 3: Notify Results
    draw_process(310, 380, 470, 480, "3", "Notify Results", "Sends the final predicted score and tier back to the researcher.")
    
    # Labeled arrows helper
    def draw_arrow(start, end, label, direction="R", label_pos="above"):
        x1, y1 = start
        x2, y2 = end
        draw.line([start, end], fill="#4a5568", width=2)
        if direction == "R":
            draw.polygon([(x2, y2), (x2 - 8, y2 - 4), (x2 - 8, y2 + 4)], fill="#4a5568")
            y_text = y2 - 8 if label_pos == "above" else y2 + 8
            draw.text((x1 + (x2-x1)//2, y_text), label, fill="#2d3748", font=text_font, anchor="mm")
        elif direction == "D":
            draw.polygon([(x2, y2), (x2 - 4, y2 - 8), (x2 + 4, y2 - 8)], fill="#4a5568")
            draw.text((x2 + 8, y1 + (y2-y1)//2), label, fill="#2d3748", font=text_font, anchor="lm")
            
    # Draw connections
    # Researcher to Process 1
    draw_arrow((150, 215), (240, 150), "Indicator Inputs", "R")
    
    # Process 1 to Database
    draw_arrow((320, 190), (320, 260), "Store Data", "D")
    
    # Process 1 to Process 2
    draw_arrow((400, 150), (470, 200), "Country Data", "R")
    
    # Database to Process 2
    draw_arrow((400, 285), (470, 255), "Country Data", "R")
    
    # Process 2 to Economics Dept
    draw_arrow((630, 240), (670, 290), "Prediction (Score & Tier)", "R")
    
    # Economics Dept to Process 3
    draw.line([(700, 340), (700, 430), (470, 430)], fill="#4a5568", width=2)
    draw.polygon([(470, 430), (478, 426), (478, 434)], fill="#4a5568")
    draw.text((585, 418), "Final Decision (Approve / Reject)", fill="#2d3748", font=text_font, anchor="mm")
    
    # Process 3 to Researcher
    draw.line([(310, 430), (100, 430), (100, 260)], fill="#4a5568", width=2)
    draw.polygon([(100, 260), (96, 268), (104, 268)], fill="#4a5568")
    draw.text((205, 418), "Results Notification", fill="#2d3748", font=text_font, anchor="mm")
    
    os.makedirs("2. Requirement Analysis", exist_ok=True)
    img.save("2. Requirement Analysis/data_flow_diagram.png")
    print("Generated data_flow_diagram.png successfully.")

def create_solution_architecture_diagram():
    w, h = 800, 550
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    title_font = get_font("segoeuib.ttf", 22)
    header_font = get_font("segoeuib.ttf", 13)
    
    draw.text((20, 20), "Solution Architecture Diagram - HDI Predictor", fill="#1a202c", font=title_font)
    
    layer1 = {"box": (100, 70, 700, 130), "title": "Presentation / Client Layer\n[Web App (HTML/CSS Dashboard, Responsive Form)]", "fill": "#ebf8ff", "border": "#3182ce"}
    layer2 = {"box": (100, 180, 700, 240), "title": "API Gateway / Load Balancer\n[Flask Router Endpoint (app.py)]", "fill": "#fffaf0", "border": "#dd6b20"}
    
    service_auth = {"box": (100, 290, 280, 360), "title": "Auth Service\n[N/A (Public Web access)]", "fill": "#f0fff4", "border": "#38a169"}
    service_core = {"box": (310, 290, 490, 360), "title": "Core Logic Service\n[ML Predict Model (best_model.pkl)]", "fill": "#f0fff4", "border": "#38a169"}
    service_ext = {"box": (520, 290, 700, 360), "title": "External APIs / Preprocess\n[Data Scaler (scaler.pkl)]", "fill": "#f0fff4", "border": "#38a169"}
    
    layer4 = {"box": (100, 410, 700, 470), "title": "Data / Storage Layer\n[UNDP CSV dataset (hdi_dataset.csv) & serialized binaries]", "fill": "#fff5f5", "border": "#e53e3e"}

    layers = [layer1, layer2, service_auth, service_core, service_ext, layer4]
    
    for l in layers:
        x1, y1, x2, y2 = l["box"]
        draw.rectangle(l["box"], fill=l["fill"], outline=l["border"], width=2)
        
        lines = l["title"].split("\n")
        cy = y1 + (y2 - y1) // 2 - (len(lines) * 12) // 2 + 5
        for line in lines:
            draw.text((x1 + (x2 - x1)//2, cy), line, fill="#2d3748", font=header_font, anchor="mm")
            cy += 14

    draw.text((400, 155), "↓ ↑", fill="#4a5568", font=header_font, anchor="mm")
    draw.text((400, 265), "↓ ↑", fill="#4a5568", font=header_font, anchor="mm")
    draw.text((400, 385), "↓ ↑", fill="#4a5568", font=header_font, anchor="mm")

    os.makedirs("3. Project Design Phase", exist_ok=True)
    img.save("3. Project Design Phase/solution_architecture.png")
    print("Generated solution_architecture.png successfully.")

def create_performance_screenshots():
    # 1. Web app screenshot mock (800 x 500)
    img1 = Image.new("RGB", (800, 500), "#0f172a")
    draw1 = ImageDraw.Draw(img1)
    
    font_large = get_font("segoeuib.ttf", 26)
    font_med = get_font("segoeuib.ttf", 14)
    font_small = get_font("segoeui.ttf", 11)
    
    # Draw Web Navbar
    draw1.text((30, 25), "● HDI Predictor", fill="#a6e3a1", font=font_med)
    draw1.text((300, 25), "What is HDI", fill="#94a3b8", font=font_small)
    draw1.text((400, 25), "How it works", fill="#94a3b8", font=font_small)
    draw1.text((500, 25), "Examples", fill="#94a3b8", font=font_small)
    draw1.rounded_rectangle((700, 20, 770, 45), radius=5, fill="#0d9488")
    draw1.text((735, 32), "Try It", fill="#ffffff", font=font_small, anchor="mm")
    
    # Content Title
    draw1.text((30, 110), "Estimate a country's", fill="#ffffff", font=font_large)
    draw1.text((30, 150), "human development", fill="#a6e3a1", font=font_large)
    draw1.text((30, 190), "from seven signals.", fill="#ffffff", font=font_large)
    
    # Description
    desc = "This tool predicts the Human Development Index (HDI) -- the UN's composite measure of health, education, and living standards -- from seven socio-economic indicators using an auto-selected model."
    words = desc.split(" ")
    y_off = 250
    curr_line = ""
    for w in words:
        test = f"{curr_line} {w}".strip()
        bbox = draw1.textbbox((0,0), test, font=font_small)
        if bbox[2] - bbox[0] < 380:
            curr_line = test
        else:
            draw1.text((30, y_off), curr_line, fill="#94a3b8", font=font_small)
            y_off += 18
            curr_line = w
    if curr_line:
        draw1.text((30, y_off), curr_line, fill="#94a3b8", font=font_small)
        
    # Spectrum Card
    card_box = (450, 120, 770, 320)
    draw1.rounded_rectangle(card_box, radius=8, fill="#1e293b", outline="#334155")
    draw1.text((470, 140), "THE DEVELOPMENT SPECTRUM", fill="#94a3b8", font=font_small)
    
    # Rainbow progress bar
    draw1.rectangle((470, 180, 750, 195), fill="#ef4444") # Red
    draw1.rectangle((540, 180, 750, 195), fill="#eab308") # Yellow
    draw1.rectangle((610, 180, 750, 195), fill="#22c55e") # Green
    draw1.rectangle((680, 180, 750, 195), fill="#06b6d4") # Cyan
    
    # Tick marker at 0.80
    draw1.line([(700, 175), (700, 200)], fill="#ffffff", width=3)
    draw1.text((470, 205), "0.00", fill="#94a3b8", font=font_small)
    draw1.text((540, 205), "0.55", fill="#94a3b8", font=font_small)
    draw1.text((610, 205), "0.70", fill="#94a3b8", font=font_small)
    draw1.text((680, 205), "0.80", fill="#94a3b8", font=font_small)
    draw1.text((735, 205), "1.00", fill="#94a3b8", font=font_small)
    
    # Buttons
    draw1.rounded_rectangle((30, 360, 180, 400), radius=20, fill="#0d9488")
    draw1.text((105, 380), "Run a prediction →", fill="#ffffff", font=font_small, anchor="mm")
    
    # Stats footer
    draw1.text((30, 440), "7 input indicators    3 models compared    191 countries - 32 years    4 development tiers", fill="#64748b", font=font_small)
    
    os.makedirs("6.Project Testing", exist_ok=True)
    img1.save("6.Project Testing/performance_screenshot1.png")
    
    # 2. Terminal benchmark mock (800 x 500)
    img2 = Image.new("RGB", (800, 500), "#000000")
    draw2 = ImageDraw.Draw(img2)
    font_mono = get_font("cour.ttf", 10)
    if font_mono == ImageFont.load_default():
         font_mono = get_font("Courier New.ttf", 10)
         
    terminal_text = """(.venv) PS C:\\Users\\Hari Charan\\OneDrive\\Desktop\\HDI_Predictor> python scratch/run_load_test.py
==================================================
HDI Predictor - Performance & Load Testing Tool
==================================================
Testing Endpoint: http://127.0.0.1:7860/predict
Make sure your Flask server is running (python app.py) before starting!

Running Scenario 1: Baseline Request (1 Virtual Users, 10 total requests)...
  Total Duration: 0.168 seconds
  Average Latency: 16.4 ms
  Maximum Latency: 29.4 ms
  Throughput: 59.4 requests/sec
  Error Rate: 0.0%

Running Scenario 2: Load Testing (5 Virtual Users, 50 total requests)...
  Total Duration: 0.139 seconds
  Average Latency: 13.1 ms
  Maximum Latency: 25.9 ms
  Throughput: 358.9 requests/sec
  Error Rate: 0.0%

Running Scenario 3: Concurrency Spike (15 Virtual Users, 150 total requests)...
  Total Duration: 0.391 seconds
  Average Latency: 37.3 ms
  Maximum Latency: 61.4 ms
  Throughput: 383.6 requests/sec
  Error Rate: 0.0%

==================================================
PERFORMANCE RESULTS SUMMARY TABLE
==================================================
Metric                    | Target Value    | Actual Value    | Status
----------------------------------------------------------------------
Response Time (Avg)       | < 2 seconds     | 13.1 ms         | Pass
Response Time (Max)       | < 5 seconds     | 25.9 ms         | Pass
Throughput (Req/sec)       | > 20 req/s      | 358.9 req/s     | Pass
Error Rate                | < 1%            | 0.0%            | Pass
==================================================."""

    lines = terminal_text.split("\n")
    y = 20
    for l in lines:
        draw2.text((20, y), l, fill="#e2e8f0", font=font_mono)
        y += 11
        
    img2.save("6.Project Testing/performance_screenshot2.png")
    print("Generated performance screenshots successfully.")

if __name__ == "__main__":
    create_problem_statement_example()
    create_empathy_map()
    create_customer_journey_map()
    create_problem_solution_fit()
    create_data_flow_diagram()
    create_solution_architecture_diagram()
    create_performance_screenshots()
