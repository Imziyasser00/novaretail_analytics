# NovaRetail Sales Analytics Pipeline

Portfolio project using synthetic retail transactions. All data is fictional.

## Quick start

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/generate_data.py
```

The script creates `data/raw/sales_2026.csv` with 5,000 reproducible transactions.

## Data dictionary

- `transaction_id`: unique synthetic sale ID
- `transaction_date`: date of sale
- `product`, `category`: item and product category
- `quantity`: units sold
- `unit_price`: price in EUR per unit before discount
- `discount_rate`: fraction discounted (0.10 = 10%)
- `payment_method`: card, cash, or bank transfer
- `store`: fictional store location
- `revenue`: quantity × unit price × (1 − discount rate), rounded to cents

Next steps: quality checks, SQL analysis, dashboard, and portfolio case study.
