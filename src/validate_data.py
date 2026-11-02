
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data" / "raw" / "sales_2026.csv")

# 1. Convert transaction_date into datetime
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

# 2. Count duplicate transaction IDs
duplicates = df["transaction_id"].duplicated().sum()
print("Duplicate IDs:", duplicates)

# 3. Check invalid quantities and prices
invalid_quantity = (df["quantity"] <= 0).sum()
invalid_price = (df["unit_price"] <= 0).sum()

print("Invalid quantities:", invalid_quantity)
print("Invalid prices:", invalid_price)

# 4. Check invalid discount rates
invalid_discount = (
    (df["discount_rate"] < 0) |
    (df["discount_rate"] > 1)
).sum()

print("Invalid discounts:", invalid_discount)

# 5. Check dates that failed conversion
print("Invalid dates:", df["transaction_date"].isna().sum())
