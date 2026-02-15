from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(filename="sample_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("<b>PAIMANA INFRASTRUCTURE PROGRESS REPORT</b>", styles['Title']))
    elements.append(Spacer(1, 20))
    
    # Project Info Section (Unstructured text with consistent/inconsistent spacing)
    text_content = """
    <b>Project Overview</b>
    
    Project Name:  National Highway Expansion Phase-IV  
    Sector: Road Transport & Highways
    Report Month: January 2024
    
    State: Maharashtra     District:  Pune 
    
    The project aims to widen the existing highway to 6 lanes. 
    Land acquisition is 80% complete.
    """
    elements.append(Paragraph(text_content.replace("\n", "<br/>"), styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Financial & Physical Progress Table
    data = [
        ['Parameter', 'Value', 'Unit'],
        ['Physical Progress', '45.5', '%'],
        ['Financial Progress', '42.0', '%'],
        ['Planned Cost', '1500.00', 'Rs. Crore'],
        ['Expenditure Till Date', '750.00', 'Rs. Crore'],
        ['Delay Status', 'Moderate', '-']
    ]
    
    t = Table(data, colWidths=[200, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))

    # Another messy section
    messy_text = """
    <b>Additional Details:</b>
    Project ID:  NH-MH-2023-45  
    Executing Agency: NHAI
    """
    elements.append(Paragraph(messy_text.replace("\n", "<br/>"), styles['Normal']))
    
    doc.build(elements)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_pdf("tests/sample_report.pdf")
