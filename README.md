# E-Commerce ETL — Data Engineering Portfolio Project

Short description: simple ETL pipeline that ingests a sample e-commerce CSV, cleans data, runs quality checks, and stores a cleaned CSV.

## Structure
- `etl/` - modular ETL code (extract, transform, load, quality)
- `raw/` - raw input (ignored by git)
- `processed/` - outputs (ignored by git)
- `logs/` - pipeline run logs
- `main.py` - pipeline orchestrator

## How to run (local)
1. Create venv: `python -m venv venv`
2. Activate venv:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `python main.py`

## What this demonstrates
- Python ETL modularization
- Data quality checks
- Logging and reproducible project layout

## Next steps (planned)
- Orchestrate with Airflow
- Move outputs to PostgreSQL / Redshift
- Convert to PySpark for large data
