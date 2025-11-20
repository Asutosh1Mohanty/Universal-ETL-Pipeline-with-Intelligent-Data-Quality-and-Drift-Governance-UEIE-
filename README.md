Project: Universal ETL Pipeline with Automated Data Quality Checks

This project is an end-to-end Data Engineering ETL pipeline that can process ANY dataset you upload (CSV, Excel, JSON, Parquet).
It performs:
   * Extraction from local file 
   * Automatic cleaning 
   * Column standardization 
   * Missing value handling 
   * Date parsing 
   * Duplicate removal 
   * Automated data quality (DQ) checks 
   * Logging
   * And saves clean outputs + quality reports
It is designed to imitate real-world ingestion pipelines used in companies.

🎯 Goal of the Project
The goal is to create a reusable, production-inspired ETL pipeline that can:
   ✔ Accept any raw dataset
   ✔ Standardize and clean data
   ✔ Validate data quality
   ✔ Generate structured and human-readable reports
   ✔ Provide logs for traceability
   ✔ Serve as Step 1 of a full Data Engineering portfolio

This project becomes the foundation for future steps like:
   * PostgreSQL Data Warehouse
   * Airflow scheduling
   * PySpark transformations
   * AWS Data Lake 
   * Redshift Warehouse

🏗️ High-Level Architecture
             ┌─────────────────────────────────────┐
             │           RAW DATA (any file)       │
             │    CSV / Excel / JSON / Parquet     │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │              Extract                 │
             │  - Detect latest file in /raw        │
             │  - Load CSV/Excel/JSON/Parquet       │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │             Transform                │
             │  - Standardize columns               │
             │  - Drop duplicates                   │
             │  - Type conversions                  │
             │  - Missing value handling            │
             │  - Parse date-like columns           │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │                Load                  │
             │     Save cleaned CSV/Parquet         │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │          Data Quality Check          │
             │  - Null counts                       │
             │  - Duplicate records                 │
             │  - Date parsing issues               │
             │  - Numeric validation                │
             │  - PASS/FAIL verdict                 │
             │  - TXT + JSON reports                │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │                Logs                  │
             │        logs/pipeline.log            │
             └─────────────────────────────────────┘

🚀 Features
✔ Accepts ANY data file
Supports:
   * .csv
   * .xlsx
   * .xls
   * .json
   * .parquet

✔ Automatic column standardization
Converts:
   * "Order Date" → order_date
   * "Unit-Price" → unit_price

✔ Smart cleaning
   * Remove duplicates
   * Convert numeric columns
   * Parse date-like columns
   * Handle missing values based on data type

✔ Automated data quality checks
The pipeline auto-checks:
   * Null counts 
   * Duplicate rows 
   * Non-numeric numeric values 
   * Negative values 
   * Unparsable dates 
   * Column type consistency

Generates:
   * processed/quality_report.txt (readable)
   * processed/quality_report.json (machine-friendly)

✔ Logging
All activity is logged in:
   * logs/pipeline.log    

✔ Chunk support for HUGE CSV files
Automatically processes datasets in chunks for memory safety.

🧰 Tech Stack
Component	            Tools Used
Language	            Python 3.10+
Data Processing	        Pandas
Formats	                CSV / Excel / JSON / Parquet
Logging	                Python logging module
Testing	                (Optional) pytest
Storage	                Local filesystem 
Metadata	            JSON DQ report

📂 Project Structure
Data_Engineering_Projects/
│
├── etl/
│   ├── extract.py       # Load raw data (any file type)
│   ├── transform.py     # Clean, standardize, parse dates, fix types
│   ├── load.py          # Save cleaned outputs
│   └── quality.py       # Perform data quality checks
│
├── raw/                 # Place your input file here
├── processed/           # Cleaned output + quality reports
├── logs/                # Pipeline logs
├── main.py              # Orchestrator
├── requirements.txt
└── README.md

🛠️ How the ETL Pipeline Works
1) Extraction
      * Locate the latest file inside the raw/ folder. 
      * Load file depending on type:
          * pd.read_csv()
          * pd.read_excel()
          * pd.read_json()
          * pd.read_parquet()
      * If CSV is huge → optionally load in chunks.

2) Transformation
The following operations are applied:
      * Column Standardization 
      * Lowercase
      * Remove spaces and hyphens
      * Uniform naming
      * Duplicate Removal
              df = df.drop_duplicates().reset_index(drop=True)
      * Missing Value Handling 
      * Numeric column → fill with 0
      * Object column → fill with "unknown"
      * Datetime column → keep NaT for DQ check
      * Convert invalid numbers using errors='coerce'
      * Auto Date Parsing
             Column names containing "date" or "time" are converted using:
                   pd.to_datetime(df[col], errors="coerce")

3) Loading
Saves cleaned data to:
     processed/cleaned_sales.csv
(or Parquet version if selected)

4) Data Quality Checks
Checks include:

Check	              Description
Null Count	          Count missing per column
Duplicate Rows	      Identify duplicate records
Numeric validation	  Check non-numeric or negative values
Date parsing	      How many values failed to convert
Uniqueness	          Detect duplicate IDs
Verdict	              PASS/FAIL based on rules

Outputs:
   * quality_report.txt 
   * quality_report.json

5) Logging
Every run logs:
     * Timestamp 
     * Steps executed
     * Warnings
     * Errors 
     * Quality verdict

Example:
      2025-02-01 10:21:22 INFO Pipeline started
      2025-02-01 10:21:22 INFO Loaded raw dataframe with 10 rows
      2025-02-01 10:21:22 INFO Saved cleaned data to processed/cleaned_sales.csv
      2025-02-01 10:21:22 INFO Quality verdict: PASS

▶️ How to Use the Pipeline
1. Clone repo
      git clone <your-repo-url>
      cd Data_Engineering_Projects

2. Create venv
      python -m venv venv
      venv\Scripts\activate        # Windows
      source venv/bin/activate     # Mac/Linux

3. Install dependencies
       pip install -r requirements.txt

4. Put your input file 
        Place any file inside:
            raw/yourdata.xlsx
            raw/sales.csv
            raw/data.json
            raw/bigfile.parquet

5. Run
       python main.py

6. Check output
        * processed/cleaned_sales.csv 
        * processed/quality_report.txt
        * processed/quality_report.json
        * logs/pipeline.log

🧪 Example Scenario
If you upload:
raw/Sales_Q1_2024.xlsx

The pipeline will:
      ✔ Detect this file
      ✔ Load Excel
      ✔ Standardize columns
      ✔ Remove duplicates
      ✔ Parse date columns
      ✔ Convert volume/price columns
      ✔ Save cleaned CSV
      ✔ Generate a DQ report
      ✔ Log everything
You don’t need to rename the file — any name works.

🌟 Why this Project is Impressive for Data Engineering
This project demonstrates:
      * Ingestion from heterogeneous data sources 
      * ETL modularization 
      * Data quality management
      * File detection and metadata handling
      * Error handling
      * Logging & reporting 
      * Clean project structure

These are exactly the skills tested in:
      * Data Engineer interviews
      * Data Platform teams
      * ML Ops teams
      * ETL / Analytics engineering roles

📝 Resume Bullet Point
Built a universal Python-based ETL pipeline capable of ingesting CSV/Excel/JSON/Parquet files, performing automated data cleaning, type normalization, date parsing, duplicate removal, and generating detailed text/JSON data-quality reports with full logging support.