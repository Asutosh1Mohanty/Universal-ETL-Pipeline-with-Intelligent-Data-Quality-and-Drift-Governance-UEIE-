Project: Universal ETL Pipeline with Intelligent Data Quality and Drift Governance (UEIE)

This project is an production-inspired, intelligent Data Engineering ETL pipeline designed that ingest ANY dataset (CSV, Excel, JSON, Parquet).
It automatically performs:
    * Data extraction 
    * Cleaning & standardization 
    * Automated data quality checks 
    * Intelligent quality scoring 
    * Quality gating (PASS / WARN / FAIL)
    * Data drift detection across runs 
    * Drift severity classification
    * Auto-fail protection for critical drift
    * Full execution metadata & lineage
    * Centralized logging
It is designed to imitate real-world data ingestion pipelines used in modern data platforms.

🎯 Goal of the Project
The goal is to build a reusable, extensible, and governed ETL foundation that can:
    ✔ Accept any raw dataset without manual schema definition
    ✔ Automatically clean and standardize data
    ✔ Validate data quality with scoring & rules
    ✔ Detect silent data drift across pipeline runs
    ✔ Prevent bad or breaking data from flowing downstream
    ✔ Generate machine-readable metadata and human-readable reports
    ✔ Serve as the foundation for advanced data platforms

This project becomes the foundation for future steps like:
   * PostgreSQL Data Warehouse
   * Airflow scheduling
   * PySpark transformations
   * AWS Data Lake 
   * Redshift Warehouse

Key Intelligence: UEIE (Universal ETL Intelligence Engine)
UEIE is a custom-built intelligence layer added on top of the ETL pipeline that provides:
    * Dataset profiling 
    * Rule inference 
    * Quality scoring
    * Quality gates
    * Drift detection
    * Drift severity classification
    * Run-level metadata & lineage
This makes the pipeline decision-aware, not just procedural.

🏗️ High-Level Architecture
             ┌─────────────────────────────────────┐
             │           RAW DATA (any file)       │
             │    CSV / Excel / JSON / Parquet     │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │              Extract                │
             │  - Detect latest file in /raw       │
             │  - Load CSV/Excel/JSON/Parquet      │
             │  - Chunk large CSVs safely          │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │             Transform               │
             │  - Standardize columns              │
             │  - Drop duplicates                  │
             │  - Type conversions                 │
             │  - Missing value handling           │
             │  - Parse date-like columns          │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │                Load                 │
             │     Save cleaned CSV/Parquet        │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │       Data Quality & UEIE Layer     │
             │  - Quality Checks                   │
             │  - Quality Score                    │
             │  - PASS / WARN / FAIL gate          │
             │  - Drift Detection                  │
             │  - Drift Severity                   │
             │   (MINOR/MAJOR/CRITICAL)            │
             │  - Auto-fail on CRITICAL drift      │
             └─────────────────────────────────────┘
                          │
                          ▼
             ┌─────────────────────────────────────┐
             │      Metadata, Lineage and Logs     │
             │   - run_metadata.json               │
             │   - last_profile.json               │
             │   - logs/pipeline.log               │
             └─────────────────────────────────────┘

🚀 Features
✔ Universal File Ingestion
Supports:
   * .csv
   * .xlsx
   * .xls
   * .json
   * .parquet
No file renaming required

✔ Automatic column standardization
Converts:
   * "Order Date" → order_date
   * "Unit-Price" → unit_price
Ensures consistent downstream processing

✔ Smart Data Cleaning
   * Duplicate removal 
   * Numeric coercion 
   * Date parsing (auto-detected via column names)
   * Missing value handling by data type 
   * Safe handling of invalid values

✔ Automated Data Quality Checks
The pipeline auto-checks:
   * Null counts per column 
   * Duplicate records 
   * Numeric validation (non-numeric, negative values)
   * Date parsing failures 
   * Uniqueness checks 
   * Schema consistency

Generates / Outputs:
   * processed/quality_report.txt (human-readable)
   * processed/quality_report.json (machine-readable)

✔ UEIE Quality Scoring
Each dataset receives a quality score (0–100) based on profiling results.

✔ Quality Gate Enforcement (Governance)
Quality Score   |   Status  |   Behavior
≥ 80	        |   PASS    |	Pipeline continues
60–79	        |   WARN    |	Pipeline continues with warning
< 60    	    |   FAIL    |   Pipeline stops
Prevents bad data from reaching downstream systems.

✔ Data Drift Detection (Across Runs)
Automatically compares:
    * Null percentage
    * Uniqueness percentage
    * Data types
    * Schema changes
    * Column additions/removals
Uses previous run profile as baseline.

✔ Drift Severity Classification
Detected drift is classified as:
    * MINOR – small statistical changes
    * MAJOR – significant distribution shifts
    * CRITICAL – schema/type changes or column removal

✔ Auto-Fail on Critical Drift
If CRITICAL drift is detected:
    * Pipeline fails immediately 
    * Downstream systems are protected
This mimics enterprise data governance rules.

✔ Production-Grade Logging
All activity is logged in:
   * logs/pipeline.log
Includes:
   * Execution steps
   * Warnings
   * Errors
   * Quality decisions
   * Drift alerts

✔ Chunk support for HUGE CSV files
Automatically processes datasets in chunks for memory safety.

🧰 Tech Stack
Component	            Tools Used
Language	            Python 3.10+
Data Processing	        Pandas
Formats	                CSV / Excel / JSON / Parquet
Logging	                Python logging
Governance	            Custom UEIE engine
Storage	                Local filesystem 
Metadata	            JSON

📂 Project Structure
Data_Engineering_Projects/
│
├── etl/                         # Core ETL logic
│   ├── extract.py               # Load raw data (CSV / Excel / JSON / Parquet)
│   ├── transform.py             # Clean, standardize columns, parse dates, fix types
│   ├── load.py                  # Save cleaned outputs (CSV / Parquet)
│   └── quality.py               # Perform automated data quality checks
│
├── ueie/                        # Universal ETL Intelligence Engine (governance layer)
│   ├── detector.py              # Detect file metadata (name, size, extension)
│   ├── profiler.py              # Profile dataset (null %, uniqueness, dtypes)
│   ├── rule_engine.py           # Infer quality rules from profile
│   ├── scorer.py                # Calculate overall data quality score
│   ├── gate.py                  # PASS / WARN / FAIL quality gate
│   ├── drift.py                 # Detect data drift across pipeline runs
│   ├── drift_gate.py            # Classify drift severity & enforce governance
│   └── metadata.py              # Store run metadata & profile history
│
├── raw/                         # Place your input data files here
│                                 # (CSV / Excel / JSON / Parquet)
│
├── processed/                   # Pipeline outputs & metadata
│   ├── cleaned_*.csv             # Cleaned datasets
│   ├── quality_report.txt        # Human-readable quality report
│   ├── quality_report.json       # Machine-readable quality report
│   ├── run_metadata.json         # Run-level execution metadata
│   └── last_profile.json         # Previous run profile (for drift detection)
│
├── logs/                        # Pipeline execution logs
│   └── pipeline.log
│
├── main.py                      # Pipeline orchestrator (entry point)
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation


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
        2025-12-20 13:10:36 INFO Pipeline started
        2025-12-20 13:10:36 INFO Rows processed: 10000
        2025-12-20 13:10:36 INFO UEIE quality score: 100.0
        2025-12-20 13:10:36 INFO UEIE quality gate status: PASS
        2025-12-20 13:10:36 INFO Pipeline finished


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
        * processed/run_metadata.json
        * logs/pipeline.log

🧪 Example Scenario
If you upload:
customers.csv

The pipeline will:
        ✔ Detect the file automatically
        ✔ Cleans and standardize the data
        ✔ Runs data quality checks
        ✔ Calculate a quality score
        ✔ Apply quality gate rules
        ✔ Detect data drift vs previous run
        ✔ Enforce drift severity governance 
        ✔ Saves cleaned data, reports and metadata
        ✔ Logs all decisions
You don’t need to rename the file — any name works.

🌟 Why this Project is Impressive for Data Engineering
This project demonstrates:
        * Ingestion from heterogeneous data sources 
        * Modular ETL design
        * Automated data quality enforcement 
        * Intelligent quality gating
        * Data drift detection & governance
        * Metadata & lineage tracking
        * Production-grade logging
        * Clean, scalable project architecture

These are exactly the skills tested in:
        * Data Engineer
        * Analytics Engineer
        * Data Platform teams
        * ML Ops teams
        * ETL / Analytics engineering roles

📝 Resume Bullet Point
Built a universal, intelligence-driven ETL pipeline in Python capable of ingesting heterogeneous data formats, performing automated cleaning, quality scoring, quality gating, drift detection with severity classification, and enforcing governance rules with full execution metadata and logging.
