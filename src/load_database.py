
from pathlib import Path
import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Load cleaned transactions
df = pd.read_csv(
    ROOT / "data" / "processed" / "sales_clean.csv",
    parse_dates=["transaction_date"]
)

# Create database folder
db_dir = ROOT / "data" / "database"
db_dir.mkdir(parents=True, exist_ok=True)

# Connect to persistent DuckDB database
con = duckdb.connect(str(db_dir / "novaretail.duckdb"))

# Create or replace transactions table
con.execute("""
    CREATE OR REPLACE TABLE transactions AS
    SELECT * FROM df
""")

# Verify loading
result = con.execute("""
    SELECT COUNT(*) AS total_transactions
    FROM transactions
""").fetchone()

print("Transactions loaded:", result[0])

con.close()
