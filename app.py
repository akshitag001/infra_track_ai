import streamlit as st
import pandas as pd
import json
import plotly.express as px
from src.extractor import extract_text_and_tables
from src.parser import parse_project_info

# Page Config
st.set_page_config(
    page_title="InfraTrack AI",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title and Sidebar
st.title("🏗️ InfraTrack AI")
st.markdown("### Infrastructure Progress Extractor & Monitor")

st.sidebar.header("Upload Report")
uploaded_file = st.sidebar.file_uploader("Upload PAIMANA PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting and Parsing..."):
        # Save temp file or process directly
        # pdfplumber takes file-like objects so we can pass uploaded_file directly
        extracted_data = extract_text_and_tables(uploaded_file)
        
        if extracted_data:
            parsed_info = parse_project_info(extracted_data["text"], extracted_data["tables"])
            parsed_info["source_file"] = uploaded_file.name
            
            # Create DataFrame (single row for now, but scalable)
            df = pd.DataFrame([parsed_info])
            
            # Display Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Project Name", parsed_info.get("project_name", "Unknown"))
            with col2:
                st.metric("Physical Progress", f"{parsed_info.get('physical_progress_percent', 0)}%")
            with col3:
                st.metric("Financial Progress", f"{parsed_info.get('financial_progress_percent', 0)}%")
            with col4:
                status = parsed_info.get("status_flag", "Unknown")
                color = "normal"
                if "DELAYED" in status or "COST_OVERRUN" in status:
                    color = "off" # Streamlit 'off' is red-ish in delta, but let's just show text
                st.metric("Status", status)
                if "DELAYED" in status:
                    st.error(f"⚠️ {status}")
                elif "ON_TRACK" in status:
                    st.success(f"✅ {status}")

            st.divider()
            
            # Data Preview
            st.subheader("📊 Extracted Data")
            st.dataframe(df.style.applymap(lambda v: 'color: red;' if v == 'DELAYED' else None, subset=['status_flag']), use_container_width=True)
            
            # Visualizations
            st.subheader("📈 Progress Analysis")
            
            # Bar Chart: Physical vs Financial
            chart_data = pd.DataFrame({
                "Metric": ["Physical Progress (%)", "Financial Progress (%)"],
                "Value": [parsed_info.get("physical_progress_percent", 0), parsed_info.get("financial_progress_percent", 0)]
            })
            
            fig_progress = px.bar(chart_data, x="Metric", y="Value", color="Metric", 
                                  range_y=[0, 100], title="Progress Comparison")
            
            # Bar Chart: Cost Comparison
            cost_data = pd.DataFrame({
                "Metric": ["Planned Cost", "Expenditure"],
                "Amount (Cr)": [parsed_info.get("planned_cost_crore", 0), parsed_info.get("expenditure_till_date_crore", 0)]
            })
            fig_cost = px.bar(cost_data, x="Metric", y="Amount (Cr)", color="Metric",
                              title="Cost Analysis (₹ Crore)")
            
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(fig_progress, use_container_width=True)
            with c2:
                st.plotly_chart(fig_cost, use_container_width=True)


            # Downloads
            st.divider()
            st.subheader("📥 Export Data")
            
            c1, c2 = st.columns(2)
            with c1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "project_data.csv", "text/csv")
            
            with c2:
                json_str = json.dumps(parsed_info, indent=4).encode('utf-8')
                st.download_button("Download JSON", json_str, "project_data.json", "application/json")
                
            with st.expander("View Raw Extracted Text"):
                st.text(extracted_data["text"][:1000] + "...")
        else:
            st.error("Failed to extract data from the PDF.")

else:
    st.info("👈 Please upload a PDF report to begin.")
    
    # Show Demo using generated sample if it exists
    st.markdown("---")
    st.markdown("#### Don't have a file? Use the demo file:")
    with open("tests/sample_report.pdf", "rb") as f:
        st.download_button("Download Sample PDF", f, "sample_report.pdf")
