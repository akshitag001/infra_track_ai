#  InfraTrack AI

### Infrastructure Progress Extractor & Monitor

**Public Data Extraction & Structuring | Hackathon Prototype**

🔗 **Live Demo:** [https://your-streamlit-app-url.streamlit.app ](https://infratechai.streamlit.app/)

---

##  Problem Statement

Government infrastructure progress reports (such as those published on PAIMANA portals) are released mainly as PDFs and semi-structured documents.

While this data is technically public, it is **not machine-readable**, difficult to analyze, and almost impossible to track over time without manual effort.

This creates three major problems:

* No real-time monitoring of project progress
* No easy detection of delays or cost overruns
* No unified structured dataset for analytics or dashboards

---

##  Our Solution

**InfraTrack AI** is a lightweight AI-assisted system that converts unstructured government infrastructure PDFs into clean, structured data and instantly visualizes project health.

It allows anyone to:

* Upload a monthly infrastructure progress report (PDF)
* Extract key project fields automatically
* Standardize the data into a unified schema
* Detect delays and cost overruns
* Export structured datasets (CSV + JSON)
* View progress and cost analytics instantly

---

##  Key Features

*  **PDF Upload Interface**
  Upload PAIMANA-style infrastructure reports directly from the UI.

* 📄 **Automated Data Extraction**
  Extracts:

  * Project Name
  * Sector
  * State & District
  * Report Month
  * Physical Progress (%)
  * Financial Progress (%)
  * Planned Cost (₹ Crore)
  * Expenditure Till Date (₹ Crore)

* 📊 **Progress & Cost Analysis**

  * Visual comparison of physical vs financial progress
  * Planned cost vs actual expenditure chart

* ⚠️ **Smart Status Flagging**
  Automatically assigns project status:

  * `ON_TRACK`
  * `DELAYED`
  * `COST_OVERRUN`
  * `DELAYED | COST_OVERRUN`

* 📤 **Structured Data Export**
  Download extracted data as:

  * CSV
  * JSON

* 🔍 **Raw Text Viewer**
  Inspect the raw extracted text for transparency and debugging.

---

## 📐 Unified Output Schema

InfraTrack AI standardizes every report into the following schema:

```
project_id  
project_name  
sector  
state  
district  
report_month  
physical_progress_percent  
financial_progress_percent  
planned_cost_crore  
expenditure_till_date_crore  
status_flag  
source_file  
```

---

##  How It Works

```
User uploads PDF  
      ↓  
Text & table extraction using pdfplumber  
      ↓  
Regex + heuristics-based field parsing  
      ↓  
Standardized schema generation  
      ↓  
Delay & cost overrun detection  
      ↓  
Dashboard visualization  
      ↓  
Export CSV / JSON  
```

---

##  Tech Stack

* **Frontend & App Framework:** Streamlit
* **Backend:** Python
* **PDF Processing:** pdfplumber
* **Data Handling:** pandas
* **Visualization:** matplotlib / plotly
* **Parsing Logic:** regex + heuristics

---

##  Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/infratrack-ai.git  
cd infratrack-ai  
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt  
```

### 3️⃣ Run the Application

```bash
streamlit run app.py  
```

### 4️⃣ Use the App

* Upload a PAIMANA-style PDF
* View extracted data
* Analyze progress & cost
* Download structured outputs

---

##  Use Cases

* Government monitoring dashboards
* Infrastructure project audits
* Delay and cost overrun detection
* Public transparency portals
* Policy analytics & reporting
* Open data standardization

---

## 🏁 Hackathon Context

This prototype was built for the **Public Data Extraction & Structuring** problem statement.

It demonstrates how unstructured government documents can be converted into AI-ready datasets for real-time monitoring and decision-making.

---

##  Future Scope

* Multi-PDF batch processing
* OCR support for scanned PDFs
* Indic language extraction
* Geo-mapping of project locations
* Time-series trend analysis
* API for government portals
* AI-based anomaly detection

---

##  Team 

**AKSHIT AGARWAL , SARTHAK SANAY , ROHIT ANAND**
B.Tech Student | AI, Gov-Tech & Infrastructure Analytics
Built as a hackathon prototype to demonstrate real-world public data transformation using AI.

---

## 📜 License

MIT License

---


> **InfraTrack AI** —
> Turning public infrastructure data into real-time, actionable intelligence.
