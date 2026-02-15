import re
from src.utils import calculate_status, generate_project_id

def clean_text(text):
    if text:
        return text.strip()
    return None

def parse_currency(value_str):
    """
    Parses a currency string to a float.
    Removes symbols like ₹, Rs, commas, etc.
    """
    if not value_str:
        return None
    # Remove non-numeric characters except dot
    cleaned = re.sub(r'[^\d.]', '', str(value_str))
    try:
        return float(cleaned)
    except ValueError:
        return None

def parse_percentage(value_str):
    """Parses percentage string to float."""
    if not value_str:
        return None
    # Extract the first number found in the string
    match = re.search(r'(\d+(?:\.\d+)?)', str(value_str))
    if match:
        return float(match.group(1))
    return None

def find_value_in_row(row, start_index=1):
    """
    Scans a row from start_index to find the first meaningful value.
    """
    for cell in row[start_index:]:
        if cell and str(cell).strip() not in ['-', '', 'NA', 'N/A']:
            return cell
    return None

def parse_project_info(text, tables):
    """
    Parses extracted text and tables to find project details.
    
    Args:
        text (str): Full text extracted from PDF.
        tables (list): List of tables (list of lists) extracted from PDF.
        
    Returns:
        dict: A dictionary containing the structured data.
    """
    data = {
        "project_name": None,
        "sector": None,
        "report_month": None,
        "state": None,
        "district": None,
        "physical_progress_percent": None,
        "financial_progress_percent": None,
        "planned_cost_crore": None,
        "expenditure_till_date_crore": None
    }
    
    # --- 1. Regex Extraction from Text ---
    
    # Project Name (Look for "Project:" or "Project Name:")
    match = re.search(r'(?:Project Name|Project)\s*[:]\s*(.+)', text, re.IGNORECASE)
    if match:
        data["project_name"] = clean_text(match.group(1))
        
    # Sector
    match = re.search(r'Sector\s*[:]\s*(.+)', text, re.IGNORECASE)
    if match:
        data["sector"] = clean_text(match.group(1))

    # Report Month
    match = re.search(r'(?:Report Month|Date)\s*[:]\s*(.+)', text, re.IGNORECASE)
    if match:
        data["report_month"] = clean_text(match.group(1))
        
    # State
    match = re.search(r'State\s*[:]\s*([a-zA-Z\s]+)', text, re.IGNORECASE)
    if match:
        data["state"] = clean_text(match.group(1))
        
    # District (Sometimes on same line as State)
    match = re.search(r'District\s*[:]\s*([a-zA-Z\s]+)', text, re.IGNORECASE)
    if match:
        data["district"] = clean_text(match.group(1))

    # --- 2. Table Scanning for Numerical Data ---
    
    keywords_map = {
        "Physical Progress": "physical_progress_percent",
        "Financial Progress": "financial_progress_percent",
        "Planned Cost": "planned_cost_crore",
        "Expenditure": "expenditure_till_date_crore"
    }

    for table in tables:
        for row in table:
            if not row or len(row) < 2:
                continue
            
            # Clean first cell to match keyword
            first_cell = str(row[0]).strip() if row[0] else ""
            
            for key, field in keywords_map.items():
                if key.lower() in first_cell.lower() and data[field] is None:
                    # Found a match, scan row for value
                    value_cell = find_value_in_row(row, 1)
                    
                    if value_cell:
                        if field.endswith("percent"):
                            val = parse_percentage(value_cell)
                            if val is not None: data[field] = val
                        else:
                            val = parse_currency(value_cell)
                            if val is not None: data[field] = val
                    
    # --- 3. Robust Regex for Numerical Data (Narrative Text) ---
    
    # Physical Progress (in text)
    if data["physical_progress_percent"] is None:
         match = re.search(r'Physical Progress.*?(\d+(?:\.\d+)?)%', text, re.IGNORECASE | re.DOTALL)
         if match: data["physical_progress_percent"] = float(match.group(1))

    # Financial Progress (in text)
    if data["financial_progress_percent"] is None:
         match = re.search(r'Financial Progress.*?(\d+(?:\.\d+)?)%', text, re.IGNORECASE | re.DOTALL)
         if match: data["financial_progress_percent"] = float(match.group(1))
         
    # Planned Cost (Handle 'Planned Cost ... Rs. 12,500')
    if data["planned_cost_crore"] is None:
         # Look for "Planned Cost" followed by optional chars then "Rs." then number
         match = re.search(r'Planned Cost.*?(?:Rs\.?|INR)\s*([\d.,]+)', text, re.IGNORECASE | re.DOTALL)
         if match: data["planned_cost_crore"] = parse_currency(match.group(1))
         
    # Expenditure (Handle 'Expenditure ... Rs. 4,200')
    if data["expenditure_till_date_crore"] is None:
         match = re.search(r'Expenditure.*?(?:Rs\.?|INR)\s*([\d.,]+)', text, re.IGNORECASE | re.DOTALL)
         if match: data["expenditure_till_date_crore"] = parse_currency(match.group(1))

    # --- 4. Post-processing ---
    # Generate ID
    data["project_id"] = generate_project_id(data["project_name"])
    
    # Calculate Status
    data["status_flag"] = calculate_status(
        data["physical_progress_percent"],
        data["expenditure_till_date_crore"],
        data["planned_cost_crore"]
    )
    
    return data
