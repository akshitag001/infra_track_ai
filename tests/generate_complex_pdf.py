from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import random
import datetime

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawString(inch, 0.75 * inch, "CONFIDENTIAL - INTERNAL CIRCULATION ONLY")
    canvas.drawRightString(A4[0] - inch, 0.75 * inch, f"Page {doc.page}")
    canvas.restoreState()

def generate_complex_pdf(filename="tests/complex_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=4))
    
    # --- PAGE 1: COVER ---
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("<b>MINISTRY OF INFRASTRUCTURE DEVELOPMENT</b>", styles['Title']))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("MONTHLY PROGRESS MONITORING REPORT", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Date: {datetime.date.today().strftime('%B %d, %Y')}", styles['Normal']))
    elements.append(Spacer(1, 3*inch))
    elements.append(Paragraph("<b>Project:</b> Metro Rail Corridor Phase-II (Green Line)", styles['Heading3']))
    elements.append(Paragraph("<b>Zone:</b> North-Central Region", styles['Normal']))
    elements.append(PageBreak())

    # --- PAGE 2: EXECUTIVE SUMMARY (Key Data Mixed in Text) ---
    elements.append(Paragraph("1. Executive Summary", styles['Heading2']))
    
    intro_text = """
    The Metro Rail Corridor Phase-II project is a critical infrastructure initiative aimed at decongesting the northern districts.
    Despite heavy monsoon rains affecting the construction timeline, the project team has managed to maintain a steady pace in the last quarter.
    """
    elements.append(Paragraph(intro_text, styles['Justify']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Key Project Info Block (Semi-structured)
    elements.append(Paragraph("<b>1.1 Project Identification</b>", styles['Heading3']))
    project_info = [
        ["Project Name", ": Metro Rail Corridor Phase-II"],
        ["Project ID", ": MRC-PH2-2024-001"],
        ["Sector", ": Urban Transport / Rail"],
        ["State", ": Karnataka"],
        ["District", ": Bengaluru Urban"],
        ["Report Month", ": February 2024"]
    ]
    t1 = Table(project_info, colWidths=[150, 300])
    t1.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 1, colors.black), # Added Grid
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 0.3*inch))

    # Narrative with embedded data (Hard for simple regex?)
    elements.append(Paragraph("<b>1.2 Financial Overview</b>", styles['Heading3']))
    fin_text = """
    The total <b>Planned Cost</b> for this project was revised to <b>Rs. 12,500 Crore</b> following the approval of the supplementary budget.
    As of this month, the cumulative <b>Expenditure</b> stands at <b>Rs. 4,200.50 Crore</b>. 
    Utilization certificates for the last tranche have been submitted to the ministry.
    """
    elements.append(Paragraph(fin_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # --- Irrelevant Table (Distractor) ---
    elements.append(Paragraph("<b>1.3 Team Attendance (Last Month)</b>", styles['Heading3']))
    distractor_data = [
        ['Department', 'Headcount', 'Attendance %'],
        ['Civil Eng', '45', '92%'],
        ['Electrical', '30', '88%'],
        ['Signaling', '15', '95%']
    ]
    t2 = Table(distractor_data)
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(t2)
    elements.append(PageBreak())

    # --- PAGE 3: DETAILED PROGRESS (The Real Data Table) ---
    elements.append(Paragraph("2. Detailed Physical Progress", styles['Heading2']))
    elements.append(Paragraph("The following table summarizes the key performance indicators (KPIs) for the reporting period.", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))

    kpi_data = [
        ['Component', 'Weightage', 'Physical Progress (%)', 'Remarks'],
        ['Land Acquisition', '20%', '95.0%', 'Almost Complete'],
        ['Civil Works (Viaduct)', '40%', '42.5%', 'Delayed due to rain'],
        ['Stations (6 Nos)', '25%', '30.0%', 'Tendering Phase'],
        ['Signaling & Telecom', '15%', '10.0%', 'Design Complete'],
        ['Overall Physical Progress', '-', '58.2%', 'On Track'] 
    ]
    
    t3 = Table(kpi_data, colWidths=[150, 80, 100, 150])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'), # Bold the last row
    ]))
    elements.append(t3)
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("<i>Note: Physical progress is calculated based on weighted average of individual components.</i>", styles['Italic']))

    # Build PDF
    doc.build(elements, onFirstPage=footer, onLaterPages=footer)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_complex_pdf()
