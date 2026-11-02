from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N_TRANSACTIONS = 5_000
rng = np.random.default_rng(SEED)

PRODUCTS = [
    ('Wireless Mouse', 'Electronics', 24.90),
    ('Bluetooth Speaker', 'Electronics', 59.90),
    ('USB-C Cable', 'Electronics', 12.50),
    ('T-Shirt', 'Clothing', 19.90),
    ('Hoodie', 'Clothing', 49.90),
    ('Jeans', 'Clothing', 44.90),
    ('Desk Lamp', 'Home', 34.90),
    ('Coffee Mug', 'Home', 9.90),
    ('Storage Box', 'Home', 17.50),
    ('Yoga Mat', 'Sports', 29.90),
    ('Water Bottle', 'Sports', 14.90),
    ('Resistance Bands', 'Sports', 22.90),
]


def generate_sales(n: int = N_TRANSACTIONS) -> pd.DataFrame:
    if n <= 0:
        raise ValueError('n must be positive')
    product_indices = rng.choice(len(PRODUCTS), size=n)
    dates = pd.Timestamp('2026-01-01') + pd.to_timedelta(
        rng.integers(0, 273, size=n), unit='D'
    )
    quantities = rng.choice([1, 2, 3, 4, 5], size=n, p=[0.55, 0.25, 0.12, 0.06, 0.02])
    discounts = rng.choice([0.0, 0.05, 0.10, 0.20], size=n, p=[0.70, 0.15, 0.10, 0.05])
    selected = [PRODUCTS[i] for i in product_indices]
    df = pd.DataFrame({
        'transaction_id': [f'TX-{i:06d}' for i in range(1, n + 1)],
        'transaction_date': dates.strftime('%Y-%m-%d'),
        'product': [p[0] for p in selected],
        'category': [p[1] for p in selected],
        'quantity': quantities,
        'unit_price': [p[2] for p in selected],
        'discount_rate': discounts,
        'payment_method': rng.choice(['Card', 'Cash', 'Bank Transfer'], size=n, p=[0.7, 0.2, 0.1]),
        'store': rng.choice(['Paris', 'Lyon', 'Bordeaux'], size=n, p=[0.5, 0.3, 0.2]),
    })
    df['revenue'] = (df['quantity'] * df['unit_price'] * (1 - df['discount_rate'])).round(2)
    return df


if __name__ == '__main__':
    project_root = Path(__file__).resolve().parents[1]
    output = project_root / 'data' / 'raw' / 'sales_2026.csv'
    output.parent.mkdir(parents=True, exist_ok=True)
    sales = generate_sales()
    sales.to_csv(output, index=False)
    print(f'Saved {len(sales):,} rows to {output}')
    print(sales.head())
