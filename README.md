🔁 Universal ETL Pipeline — UEIE
Universal ETL Intelligence Engine

A production-inspired ETL pipeline that ingests any dataset, auto-cleans it, enforces data quality governance, detects drift, and logs full execution metadata — with zero manual schema definition.


🧠 What It Does
UEIE is a custom intelligence layer built on top of a modular ETL pipeline. It goes beyond basic extract-transform-load by adding automated quality scoring, governance gates, and cross-run drift detection — making the pipeline decision-aware, not just procedural.

🎯 Goals

✅ Accept any raw file without manual schema setup
✅ Auto-clean and standardize data
✅ Score data quality and enforce governance gates
✅ Detect silent data drift across runs
✅ Block bad data from reaching downstream systems
✅ Generate reports, metadata, and execution logs


Foundation for: PostgreSQL Warehouse → Airflow Scheduling → PySpark → AWS Data Lake → Redshift


🏗️ Architecture
RAW DATA (CSV / Excel / JSON / Parquet)
        │
        ▼
   [ Extract ]  →  Detect & load latest file in /raw, chunk large CSVs
        │
        ▼
  [ Transform ] →  Standardize columns, drop dupes, fix types, parse dates
        │
        ▼
    [ Load ]    →  Save cleaned CSV / Parquet to /processed
        │
        ▼
 [ UEIE Layer ] →  Quality checks → Score → Gate → Drift Detection → Severity
        │
        ▼
 [ Metadata ]   →  run_metadata.json │ last_profile.json │ pipeline.log

🚀 Key Features
Universal Ingestion
Supports .csv, .xlsx, .xls, .json, .parquet — no renaming needed.
Auto Column Standardization
"Order Date" → order_date  |  "Unit-Price" → unit_price
Smart Cleaning
Duplicate removal, numeric coercion, auto date parsing, missing value imputation by type.
Quality Scoring & Gates
ScoreStatusBehavior≥ 80✅ PASSPipeline continues60–79⚠️ WARNContinues with warning< 60❌ FAILPipeline stops
Data Drift Detection
Compares null %, uniqueness %, data types, and schema against the previous run.
Drift Severity Classification
SeverityTriggerMINORSmall statistical changesMAJORSignificant distribution shiftsCRITICALSchema/type changes or column removal → auto-fail
Outputs

processed/quality_report.txt — human-readable
processed/quality_report.json — machine-readable
processed/run_metadata.json — lineage & run info
logs/pipeline.log — full execution log


🧰 Tech Stack
ComponentToolLanguagePython 3.10+Data ProcessingPandasFile FormatsCSV, Excel, JSON, ParquetGovernanceCustom UEIE EngineMetadataJSONLoggingPython logging

📂 Project Structure
Data_Engineering_Projects/
├── etl/
│   ├── extract.py          # Load raw files
│   ├── transform.py        # Clean & standardize
│   ├── load.py             # Save outputs
│   └── quality.py          # Quality checks
├── ueie/
│   ├── detector.py         # File metadata detection
│   ├── profiler.py         # Dataset profiling
│   ├── rule_engine.py      # Quality rule inference
│   ├── scorer.py           # Quality scoring
│   ├── gate.py             # PASS / WARN / FAIL gate
│   ├── drift.py            # Drift detection
│   ├── drift_gate.py       # Drift severity & governance
│   └── metadata.py         # Run metadata & lineage
├── raw/                    # 📥 Drop your input files here
├── processed/              # 📤 Cleaned data, reports, metadata
├── logs/                   # Execution logs
├── main.py                 # Pipeline entry point
└── requirements.txt

▶️ Quick Start
bash# 1. Clone the repo
git clone https://github.com/your-username/Data_Engineering_Projects.git
cd Data_Engineering_Projects

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Drop your file into raw/
#    raw/sales.csv  |  raw/data.xlsx  |  raw/data.json  |  raw/data.parquet

# 5. Run
python main.py

🧪 What Happens When You Run It
Drop any file into raw/ → run python main.py and the pipeline will:
✅ Auto-detect file & format → ✅ Clean & standardize → ✅ Score quality → ✅ Apply governance gate → ✅ Detect drift vs. previous run → ✅ Save reports, metadata & logs

🌟 Skills Demonstrated
Multi-format ingestion · Modular ETL design · Data quality enforcement · Drift detection & governance · Metadata & lineage tracking · Production-grade logging
Relevant for: Data Engineer · Analytics Engineer · Data Platform · MLOps · ETL Engineering

📝 Resume Bullet

Built a universal, intelligence-driven ETL pipeline in Python supporting heterogeneous data formats, with automated cleaning, quality scoring, governance gating, cross-run drift detection with severity classification, and full execution metadata logging.
