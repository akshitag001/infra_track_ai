from src.extractor import extract_text_and_tables
from src.parser import parse_project_info
import json

def test_extraction():
    # pdf_path = "tests/sample_report.pdf" # Simple
    pdf_path = "tests/complex_report.pdf" # Complex
    
    print(f"Testing extraction on {pdf_path}...")
    
    # 1. Extract
    extracted = extract_text_and_tables(pdf_path)
    if not extracted:
        print("Extraction Failed!")
        return

    print("Text extraction length:", len(extracted["text"]))
    print("Tables found:", len(extracted["tables"]))
    
    # 2. Parse
    data = parse_project_info(extracted["text"], extracted["tables"])
    
    print("\nParsed Data:")
    print(json.dumps(data, indent=4))
    
    # Assertions for Complex Report
    assert "Metro Rail Corridor Phase-II" in data["project_name"]
    assert data["physical_progress_percent"] == 58.2
    assert data["planned_cost_crore"] == 12500.0
    assert data["expenditure_till_date_crore"] == 4200.5
    assert data["status_flag"] == "ON_TRACK"
    
    print("\n✅ Verification Successful!")

if __name__ == "__main__":
    test_extraction()
