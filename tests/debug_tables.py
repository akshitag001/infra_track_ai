import pdfplumber

def debug_pdf():
    pdf_path = "tests/complex_report.pdf"
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total Pages: {len(pdf.pages)}")
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            print(f"Page {i+1}: Found {len(tables)} tables")
            for j, table in enumerate(tables):
                print(f"  Table {j+1} First Row: {table[0] if table else 'Empty'}")

if __name__ == "__main__":
    debug_pdf()
