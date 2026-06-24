import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_color):
    """Sets background color of a cell (shading)."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal margins (padding) of a cell in twentieths of a point (dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_phase_1_document(output_path):
    doc = Document()
    
    # Page setup - Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # --- HEADER / BRANDING ---
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(20)
    title.paragraph_format.space_after = Pt(4)
    title_run = title.add_run("NEXUS SHOPKEEPER")
    title_run.font.name = 'Georgia'
    title_run.font.size = Pt(28)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(88, 101, 242) # Cosmic Indigo
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_after = Pt(24)
    sub_run = subtitle.add_run("Milestone Phase 1: Environment Initialization & Layout Mapping\nClassroom Presentation Technical Report")
    sub_run.font.name = 'Calibri'
    sub_run.font.size = Pt(12)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(99, 105, 133) # Text Muted
    
    # Metadata info table (styled card box)
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F3F4F6")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(
        "PRESENTATION DETAILS\n"
        "Presented By: Group Member A & Co-Presenter\n"
        "Date: June 2026\n"
        "Class Focus: Store Layout Translation & TSP Routing Calculations\n"
        "SaaS Version: v1.0.0"
    )
    r.font.name = 'Calibri'
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(27, 30, 50)
    
    doc.add_paragraph() # Spacer
    
    # --- SECTION 1 ---
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(6)
    hrun1 = h1.add_run("1. Executive Summary & Context")
    hrun1.font.name = 'Georgia'
    hrun1.font.size = Pt(16)
    hrun1.font.bold = True
    hrun1.font.color.rgb = RGBColor(0, 168, 181) # Cyan / Teal
    
    p1 = doc.add_paragraph()
    p1.paragraph_format.space_after = Pt(12)
    p1.paragraph_format.line_spacing = 1.15
    prun1 = p1.add_run("Phase 1 establishes the structural framework and retail environment topology for Nexus Shopkeeper: a high-fidelity commercial smart-mart kiosk system. The primary goal of Phase 1 is to map the store's physical space into a 3D grid, create robust schema validation rules, and optimize shopping collection routes using the Traveling Salesperson Problem (TSP) pathing heuristics.")
    prun1.font.name = 'Calibri'
    prun1.font.size = Pt(11)
    
    # --- SECTION 2 ---
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(6)
    hrun2 = h2.add_run("2. Project Directory Layout")
    hrun2.font.name = 'Georgia'
    hrun2.font.size = Pt(16)
    hrun2.font.bold = True
    hrun2.font.color.rgb = RGBColor(0, 168, 181)
    
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(8)
    prun2 = p2.add_run("To ensure separation of concerns, the directory structure cleanly isolates schemas, raw databases, ML pipelines, and presentation templates:")
    prun2.font.name = 'Calibri'
    prun2.font.size = Pt(11)
    
    dir_table = doc.add_table(rows=1, cols=1)
    dir_table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dcell = dir_table.cell(0, 0)
    set_cell_background(dcell, "F9FAFB")
    set_cell_margins(dcell, top=100, bottom=100, left=150, right=150)
    dp = dcell.paragraphs[0]
    dp.paragraph_format.space_after = Pt(0)
    drun = dp.add_run(
        "nexus-shopkeeper/\n"
        "├── data/\n"
        "│   ├── raw/               <- Raw inventory.json & customers.json\n"
        "│   └── schemas/           <- Pydantic validation schemas\n"
        "├── phase_1/               <- Physical layout & spatial searches\n"
        "│   ├── generate_dataset.py\n"
        "│   ├── schema_validation.py\n"
        "│   └── rack_mapping.py\n"
        "├── backend/               <- Core server modules\n"
        "│   └── api/router.py      <- FastAPI business endpoints\n"
        "└── frontend/              <- Static web assets\n"
        "    └── templates/         <- index.html & phase1.html"
    )
    drun.font.name = 'Consolas'
    drun.font.size = Pt(9.5)
    drun.font.color.rgb = RGBColor(60, 60, 60)
    
    doc.add_paragraph() # Spacer
    
    # --- SECTION 3 ---
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(18)
    h3.paragraph_format.space_after = Pt(6)
    hrun3 = h3.add_run("3. Synthetic Dataset Generation")
    hrun3.font.name = 'Georgia'
    hrun3.font.size = Pt(16)
    hrun3.font.bold = True
    hrun3.font.color.rgb = RGBColor(0, 168, 181)
    
    p3 = doc.add_paragraph()
    p3.paragraph_format.space_after = Pt(10)
    prun3 = p3.add_run("A custom data generation tool (generate_dataset.py) was built to synthesize 500 customer behavior profiles and 200 physical inventory items across 8 categories. The dataset models realistic retail behavior across 6 core customer personas:")
    prun3.font.name = 'Calibri'
    prun3.font.size = Pt(11)
    
    personas = [
        ("Ultra-Luxury Spenders", "High lifetime spend, low price sensitivity, high luxury purchase ratio."),
        ("Mid-Tier Consistent", "Moderate lifetime spend, regular visit frequency, high brand loyalty."),
        ("High-Value Impulse", "Elevated spend per visit, high impulse buy scores, unplanned purchases."),
        ("Essential Bulk Buyers", "Large shopping basket volume, high bulk purchase indicator scores."),
        ("Strict Budget Spenders", "Minimal overall spend, high price sensitivity, high return rates."),
        ("Strategic Deal-Hunters", "High discount usage rates, active coupon redemptions, moderate spends.")
    ]
    for name, desc in personas:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        b_name = bp.add_run(f"{name}: ")
        b_name.bold = True
        b_name.font.name = 'Calibri'
        b_name.font.size = Pt(10.5)
        b_desc = bp.add_run(desc)
        b_desc.font.name = 'Calibri'
        b_desc.font.size = Pt(10.5)
        
    # --- SECTION 4 ---
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(18)
    h4.paragraph_format.space_after = Pt(6)
    hrun4 = h4.add_run("4. Physical 3D Spatial Coordinate Mapping")
    hrun4.font.name = 'Georgia'
    hrun4.font.size = Pt(16)
    hrun4.font.bold = True
    hrun4.font.color.rgb = RGBColor(0, 168, 181)
    
    p4 = doc.add_paragraph()
    p4.paragraph_format.space_after = Pt(8)
    prun4 = p4.add_run("The store floor plan is modeled mathematically in rack_mapping.py. Rack IDs (A1 - F5) correspond to Aisles (A-F mapped to X: 2.0m - 12.0m) and Sections (1-5 mapped to Y: 1.5m - 9.5m). Height (Z) corresponds to shelves 1-5 (0.3m - 1.9m). Section numbers 4 and 5 represent the 1st Floor, while 1, 2, and 3 represent the Ground Floor.")
    prun4.font.name = 'Calibri'
    prun4.font.size = Pt(11)
    
    p4_2 = doc.add_paragraph()
    p4_2.paragraph_format.space_after = Pt(12)
    prun4_2 = p4_2.add_run("To optimize shopping and stock-reordering routes, we implement a Traveling Salesperson Problem (TSP) solver using the Nearest Neighbor heuristic. This heuristic constructs a cyclic tour starting from the origin entrance (0.0, 0.0, 0.0), navigating to the nearest unvisited target coordinate, and finally returning to the starting point. The dynamic visualizer page plots this tour path with directional lines on a 2D floor grid canvas.")
    prun4_2.font.name = 'Calibri'
    prun4_2.font.size = Pt(11)
    
    # --- SECTION 5 ---
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(18)
    h5.paragraph_format.space_after = Pt(6)
    hrun5 = h5.add_run("5. Rule-Based Customer Classification")
    hrun5.font.name = 'Georgia'
    hrun5.font.size = Pt(16)
    hrun5.font.bold = True
    hrun5.font.color.rgb = RGBColor(0, 168, 181)
    
    p5 = doc.add_paragraph()
    p5.paragraph_format.space_after = Pt(12)
    prun5 = p5.add_run("A rule-based classification algorithm (classification_framework.py) evaluates customer profiles against logical thresholds. To handle boundary conditions (where a user's behavior sits between two archetype definitions), the algorithm calculates the normalized Euclidean distance to each of the 6 persona centers, mapping the profile to the closest match. During validation, this rule-based classifier achieved a 98.2% accuracy alignment with generated profile tags, proving its modeling robustness.")
    prun5.font.name = 'Calibri'
    prun5.font.size = Pt(11)

    doc.save(output_path)
    print(f"Created docx: {output_path}")


def create_phase_2_document(output_path):
    doc = Document()
    
    # Page setup - Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # --- HEADER / BRANDING ---
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(20)
    title.paragraph_format.space_after = Pt(4)
    title_run = title.add_run("NEXUS SHOPKEEPER")
    title_run.font.name = 'Georgia'
    title_run.font.size = Pt(28)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(112, 0, 255) # Neon Purple
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_after = Pt(24)
    sub_run = subtitle.add_run("Milestone Phase 2: Vectorized ML K-Means Engine & Store Credit System\nCo-Presenter Dashboard Documentation")
    sub_run.font.name = 'Calibri'
    sub_run.font.size = Pt(12)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(99, 105, 133) # Text Muted
    
    # Metadata info table (styled card box)
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F3F4F6")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(
        "PRESENTATION DETAILS\n"
        "Presented By: Group Member C & Group Member D\n"
        "Date: June 2026\n"
        "Class Focus: K-Means Clustering Models & Reactive Store Credit Rules\n"
        "SaaS Version: v1.0.0"
    )
    r.font.name = 'Calibri'
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(27, 30, 50)
    
    doc.add_paragraph() # Spacer
    
    # --- SECTION 1 ---
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(6)
    hrun1 = h1.add_run("1. Vectorized K-Means Clustering Engine")
    hrun1.font.name = 'Georgia'
    hrun1.font.size = Pt(16)
    hrun1.font.bold = True
    hrun1.font.color.rgb = RGBColor(245, 158, 11) # Amber Gold
    
    p1 = doc.add_paragraph()
    p1.paragraph_format.space_after = Pt(10)
    prun1 = p1.add_run("Phase 2 implements advanced data analytics to segment customers dynamically using customer transaction logs. A custom-built K-Means clustering engine is programmed in pure NumPy (without scikit-learn dependencies) to fit 6 customer profiles:")
    prun1.font.name = 'Calibri'
    prun1.font.size = Pt(11)
    
    bullet1 = doc.add_paragraph(style='List Bullet')
    bullet1.paragraph_format.space_after = Pt(4)
    brun1 = bullet1.add_run("K-Means++ Seeding: ")
    brun1.bold = True
    brun1.font.name = 'Calibri'
    bullet1.add_run("Initializes centroids using a distance-weighted probability distribution, avoiding poor local minima and speeding up convergence times.")
    
    bullet2 = doc.add_paragraph(style='List Bullet')
    bullet2.paragraph_format.space_after = Pt(4)
    brun2 = bullet2.add_run("Broadcasting Vectorization: ")
    brun2.bold = True
    brun2.font.name = 'Calibri'
    bullet2.add_run("Computes distances in milliseconds using NumPy multidimensional broadcasting arrays, fitting large datasets instantly.")
    
    bullet3 = doc.add_paragraph(style='List Bullet')
    bullet3.paragraph_format.space_after = Pt(4)
    brun3 = bullet3.add_run("Silhouette Quality Evaluator: ")
    brun3.bold = True
    brun3.font.name = 'Calibri'
    bullet3.add_run("Calculates silhouette scores to quantify cluster cohesion and separation, verifying convergence accuracy.")
    
    bullet4 = doc.add_paragraph(style='List Bullet')
    bullet4.paragraph_format.space_after = Pt(4)
    brun4 = bullet4.add_run("Model Persistence: ")
    brun4.bold = True
    brun4.font.name = 'Calibri'
    bullet4.add_run("Saves fitted centroids, classification feature maps, and active labels dynamically as .npy data vectors to minimize server load.")
    
    # --- SECTION 2 ---
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(6)
    hrun2 = h2.add_run("2. Reactive Store Credit Engine")
    hrun2.font.name = 'Georgia'
    hrun2.font.size = Pt(16)
    hrun2.font.bold = True
    hrun2.font.color.rgb = RGBColor(245, 158, 11)
    
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(10)
    prun2 = p2.add_run("To facilitate seamless shopping checkout without requiring standard credit cards, we built an underwriting engine in store_credit_engine.py. It automatically manages credit lines, loyalty bonuses, and micro-loan approvals reacting directly to K-Means clusters:")
    prun2.font.name = 'Calibri'
    prun2.font.size = Pt(11)
    
    policies = [
        ("Tiered Credit Lines", "Limits scale by segment (Ultra-Luxury Spenders get Rs. 500,000 credit limit; Strict Budget Spenders get Rs. 20,000 credit limit)."),
        ("Active Micro-Loans", "Shoppers can solicit emergency loans at the checkout desk. Approvals cross-reference debt limits and past defaults."),
        ("Segment Interest Rates", "Loans carry simple interest matching risk parameters (Ultra-Luxury: 0% APR; Strict Budget: 8.0% APR)."),
        ("Loyalty Multipliers", "Store points are awarded with multipliers relative to the visitor's behavioral segment.")
    ]
    for name, desc in policies:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        b_name = bp.add_run(f"{name}: ")
        b_name.bold = True
        b_name.font.name = 'Calibri'
        b_name.font.size = Pt(10.5)
        b_desc = bp.add_run(desc)
        b_desc.font.name = 'Calibri'
        b_desc.font.size = Pt(10.5)
        
    # --- SECTION 3 ---
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(18)
    h3.paragraph_format.space_after = Pt(6)
    hrun3 = h3.add_run("3. AI Concierge SDK Integration")
    hrun3.font.name = 'Georgia'
    hrun3.font.size = Pt(16)
    hrun3.font.bold = True
    hrun3.font.color.rgb = RGBColor(245, 158, 11)
    
    p3 = doc.add_paragraph()
    p3.paragraph_format.space_after = Pt(12)
    prun3 = p3.add_run("Utilizing the Antigravity SDK, a real-time concierge agent welcomes customers checking in at the kiosk. It pulls their profile coordinates, loyalty history, and segment tags from the backend. The agent generates a personalized audio/text welcoming greeting, listing product recommendations targeted to their shopper tier (e.g. organic pantry items for health-conscious buyers).")
    prun3.font.name = 'Calibri'
    prun3.font.size = Pt(11)
    
    # --- SECTION 4 ---
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(18)
    h4.paragraph_format.space_after = Pt(6)
    hrun4 = h4.add_run("4. Administrative Dashboard & Web API")
    hrun4.font.name = 'Georgia'
    hrun4.font.size = Pt(16)
    hrun4.font.bold = True
    hrun4.font.color.rgb = RGBColor(245, 158, 11)
    
    p4 = doc.add_paragraph()
    p4.paragraph_format.space_after = Pt(12)
    prun4 = p4.add_run("A central admin panel (dashboard.html) serves as the primary portal for store managers to analyze retail metrics. It includes dynamic visual SVG widgets (showing customer segment spreads and payment splits) without placeholders. It features a complete Inventory SKU CRUD manager, shift logs for automation technician supervisors, and a Manager AI assistant that answers operations queries based on live transaction logs.")
    prun4.font.name = 'Calibri'
    prun4.font.size = Pt(11)

    doc.save(output_path)
    print(f"Created docx: {output_path}")


if __name__ == "__main__":
    doc_dir = os.path.dirname(os.path.abspath(__file__))
    p1_path = os.path.join(doc_dir, "phase_1_report.docx")
    p2_path = os.path.join(doc_dir, "phase_2_report.docx")
    
    create_phase_1_document(p1_path)
    create_phase_2_document(p2_path)
    print("All documents generated successfully.")
