
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "raw" / "sales_2026.csv")

# 1. Display the first 10 rows
print(df.head(10))

# 2. Display the number of rows and columns
print(df.shape)

# 3. Display the data types
print("\n")
print(df.dtypes)

# 4. Check for missing values in each column
print("\n")
print(df.isna().sum())

# 5. Calculate total revenue
print("\n")
print(df.columns.tolist())
print("\n")
total_revenue = df["revenue"].sum()
print(f"Total revenue: €{df['revenue'].sum():,.2f}")

# 6. Calculate total revenue per category
print("\n")
revenue_by_category = (df.groupby("category")["revenue"].sum().sort_values(ascending=False))

print(revenue_by_category)


# 7. Find the 5 best-selling products by quantity
print("\n")

top_products = (
    df.groupby("product")["quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)

print(top_products)
