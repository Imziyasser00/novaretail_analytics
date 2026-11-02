
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data" / "raw" / "sales_messy.csv")

print("Rows before cleaning:", len(df))

# Remove exact duplicate rows
df = df.drop_duplicates()

print("Rows after cleaning:", len(df))



# Detect rows with invalid or missing values
invalid_mask = (
    df["unit_price"].isna()
    | (df["unit_price"] <= 0)
    | (df["quantity"] <= 0)
    | (df["discount_rate"] < 0)
    | (df["discount_rate"] > 1)
)

# Separate valid and suspicious rows
clean_df = df.loc[~invalid_mask].copy()
quarantine_df = df.loc[invalid_mask].copy()

print("Clean rows:", len(clean_df))
print("Quarantined rows:", len(quarantine_df))


output_dir = ROOT / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

clean_df.to_csv(
    output_dir / "sales_clean.csv",
    index=False
)

quarantine_df.to_csv(
    output_dir / "sales_quarantine.csv",
    index=False
)

print("Files saved successfully!")
