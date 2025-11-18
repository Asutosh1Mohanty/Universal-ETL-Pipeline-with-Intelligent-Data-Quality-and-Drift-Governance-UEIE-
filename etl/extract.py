import os
import urllib.request
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "raw")
RAW_FILE = os.path.join(RAW_DIR, "raw_sales.csv")

DATA_URL = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/sales/products-sales.csv"

EMBEDDED_SAMPLE = """order_id,order_date,customer_id,product,category,unit_price,quantity,city,country
1001,2020-01-05,C001,Wireless Mouse,Electronics,15.99,2,Mumbai,India
1002,2020-01-06,C002,Keyboard,Electronics,25.50,1,Delhi,India
1003,2020-01-07,,Notebook,Stationery,2.99,5,Bengaluru,India
1004,2020-01-08,C004,T-Shirt,Apparel,9.99,3,Chennai,India
1005,2020-01-08,C005,Water Bottle,Home,5.5,2,Hyderabad,India
1006,2020-01-09,C002,Keyboard,Electronics,25.50,1,Delhi,India
1007,2020-01-10,C006,Wireless Mouse,Electronics,,1,Pune,India
1008,2020-01-11,C007,Pen,Stationery,0.99,10,Kolkata,India
1009,2020-01-12,C008,Notebook,Stationery,2.99,2,Ahmedabad,India
1010,2020-01-12,C001,Wireless Mouse,Electronics,15.99,1,Mumbai,India
"""

def ensure_raw_dir():
    os.makedirs(RAW_DIR, exist_ok=True)

def download_if_missing():
    ensure_raw_dir()
    if os.path.isfile(RAW_FILE):
        return RAW_FILE
    try:
        urllib.request.urlretrieve(DATA_URL, RAW_FILE)
        return RAW_FILE
    except Exception:
        with open(RAW_FILE, "w", encoding="utf-8") as f:
            f.write(EMBEDDED_SAMPLE)
        return RAW_FILE

def load_raw():
    path = download_if_missing()
    return pd.read_csv(path)
