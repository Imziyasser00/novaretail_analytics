
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    ROOT / "data" / "processed" / "sales_clean.csv"
)

# 1. Calculate expected revenue
df["expected_revenue"] = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount_rate"])
).round(2)

# 2. Calculate difference
df["revenue_difference"] = (
    df["revenue"] - df["expected_revenue"]
).abs()

# 3. Find inconsistent transactions
errors = df[df["revenue_difference"] > 0.01]

print("Total transactions:", len(df))
print("Revenue inconsistencies:", len(errors))

print(errors[[
    "transaction_id",
    "revenue",
    "expected_revenue",
    "revenue_difference"
]].head(10))
