
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def df():
    return pd.read_csv(
        ROOT / "data" / "processed" / "sales_clean.csv"
    )


def test_no_missing_values(df):
    assert df.isna().sum().sum() == 0


def test_unique_transaction_ids(df):
    assert df["transaction_id"].is_unique


def test_positive_quantities(df):
    assert (df["quantity"] > 0).all()


def test_valid_prices(df):
    assert (df["unit_price"] > 0).all()


def test_valid_discounts(df):
    assert df["discount_rate"].between(0, 1).all()


def test_revenue_consistency(df):
    expected = (
        df["quantity"]
        * df["unit_price"]
        * (1 - df["discount_rate"])
    ).round(2)

    assert (
        (df["revenue"] - expected).abs() <= 0.01
    ).all()
