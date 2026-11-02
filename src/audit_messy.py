
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data" / "raw" / "sales_messy.csv")

# 1. Count missing values in each column
print("Missing values:")
print(df.isna().sum())

# 2. Count duplicate transaction IDs
print('\n duplicate values:')
print(df["transaction_id"].duplicated().sum())

# 3. Count quantities <= 0
print("\n quantity <= 0 : ")
print((df["quantity"]<=0).sum())

# 4. Count discounts outside [0, 1]
print("\n discounts outside [0, 1] :  ")
print(
    (
        (df["discount_rate"] < 0) |
        (df["discount_rate"] > 1)
    ).sum()
)
# 5. Calculate the percentage of missing unit prices
missing_pct = df["unit_price"].isna().mean() * 100
print(f"Missing unit prices: {missing_pct:.2f}%")
