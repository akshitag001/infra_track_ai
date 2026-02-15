import pdfplumber

def extract_text_and_tables(pdf_path):
    """
    Extracts text and tables from a PDF file.

    Args:
        pdf_path (str or file-like object): Path to the PDF file or file object.

    Returns:
        dict: A dictionary containing 'text' (str) and 'tables' (list of lists).
    """
    extracted_data = {
        "text": "",
        "tables": []
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text
                text = page.extract_text()
                if text:
                    extracted_data["text"] += text + "\n"
                
                # Extract tables
                tables = page.extract_tables()
                if tables:
                    extracted_data["tables"].extend(tables)
                    
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

    return extracted_data
