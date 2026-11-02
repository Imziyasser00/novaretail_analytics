
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]

DB_PATH = ROOT / "data" / "database" / "novaretail.duckdb"
EXPORT_DIR = ROOT / "dashboards" / "exports"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(DB_PATH), read_only=True)

queries = {
    "kpis": """
        SELECT
            ROUND(SUM(revenue), 2) AS total_revenue,
            COUNT(*) AS total_transactions,
            ROUND(AVG(revenue), 2) AS average_transaction_value
        FROM transactions
    """,

    "revenue_by_store": """
        SELECT
            store,
            COUNT(*) AS total_transactions,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(AVG(revenue), 2) AS average_transaction_value
        FROM transactions
        GROUP BY store
        ORDER BY total_revenue DESC
    """,

    "top_products": """
        SELECT
            product,
            SUM(quantity) AS total_quantity,
            ROUND(SUM(revenue), 2) AS total_revenue
        FROM transactions
        GROUP BY product
        ORDER BY total_quantity DESC
        LIMIT 5
    """,

    "monthly_revenue": """
        WITH monthly_sales AS (
            SELECT
                DATE_TRUNC('month', transaction_date) AS month,
                ROUND(SUM(revenue), 2) AS monthly_revenue
            FROM transactions
            GROUP BY month
        )
        SELECT
            month,
            monthly_revenue,
            LAG(monthly_revenue) OVER (
                ORDER BY month
            ) AS previous_month_revenue,
            ROUND(
                (
                    monthly_revenue -
                    LAG(monthly_revenue) OVER (ORDER BY month)
                ) * 100.0 /
                NULLIF(
                    LAG(monthly_revenue) OVER (ORDER BY month),
                    0
                ),
                2
            ) AS growth_percentage
        FROM monthly_sales
        ORDER BY month
    """,

    "revenue_by_category": """
        SELECT
            category,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(
                SUM(revenue) * 100.0 /
                NULLIF(
                    (SELECT SUM(revenue) FROM transactions),
                    0
                ),
                2
            ) AS revenue_percentage
        FROM transactions
        GROUP BY category
        ORDER BY total_revenue DESC
    """,

    "payment_methods": """
        SELECT
            payment_method,
            COUNT(*) AS total_transactions,
            ROUND(SUM(revenue), 2) AS total_revenue,
            ROUND(AVG(revenue), 2) AS average_transaction_value,
            ROUND(
                COUNT(*) * 100.0 /
                NULLIF(
                    (SELECT COUNT(*) FROM transactions),
                    0
                ),
                2
            ) AS transaction_percentage
        FROM transactions
        GROUP BY payment_method
        ORDER BY total_transactions DESC
    """
}

try:
    for name, query in queries.items():
        df = con.execute(query).df()

        output_path = EXPORT_DIR / f"{name}.csv"

        df.to_csv(output_path, index=False)

        print(f"Exported: {name}.csv ({len(df)} rows)")
finally:
    con.close()

print("\nAll dashboard exports completed!")
