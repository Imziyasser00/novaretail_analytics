
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data" / "raw" / "sales_2026.csv")

rng = np.random.default_rng(42)

# 1. Introduce 50 missing unit prices
missing_idx = rng.choice(df.index, size=50, replace=False)
df.loc[missing_idx, "unit_price"] = np.nan

# 2. Introduce 30 negative quantities
negative_idx = rng.choice(df.index, size=30, replace=False)
df.loc[negative_idx, "quantity"] = -3

# 3. Introduce 20 invalid discounts
discount_idx = rng.choice(df.index, size=20, replace=False)
df.loc[discount_idx, "discount_rate"] = 1.5

# 4. Add 40 duplicate transactions
duplicates = df.sample(n=40, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# 5. Save the messy dataset
output = ROOT / "data" / "raw" / "sales_messy.csv"
df.to_csv(output, index=False)

print("Messy dataset created!")
print("Rows:", len(df))
print("Missing prices:", df["unit_price"].isna().sum())
