
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]

con = duckdb.connect(
    str(ROOT / "data" / "database" / "novaretail.duckdb"),
    read_only=True
)

# Question 1: Total revenue
result = con.execute("""
    SELECT
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM transactions
""").df()

print("TOTAL REVENUE")
print(result)


# Question 2: Total revenue per store
total_revenue_per_store = con.execute("""
    SELECT
        store,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM transactions
    GROUP BY store
    ORDER BY total_revenue DESC
""").df()

print("\nTOTAL REVENUE PER STORE")
print(total_revenue_per_store)


# Question 3: Top 5 best-selling products
top_5_products = con.execute("""
    SELECT
        product,
        SUM(quantity) AS total_quantity
    FROM transactions
    GROUP BY product
    ORDER BY total_quantity DESC
    LIMIT 5
""").df()

print("\nTOP 5 PRODUCTS")
print(top_5_products)


# Question 4: Monthly revenue
monthly_revenue = con.execute("""
    SELECT
        DATE_TRUNC('month', transaction_date) AS month,
        ROUND(SUM(revenue), 2) AS monthly_revenue
    FROM transactions
    GROUP BY month
    ORDER BY month ASC
""").df()

print("\nMONTHLY REVENUE")
print(monthly_revenue)


# Question 5: Month-over-month revenue growth
monthly_growth = con.execute("""
    WITH monthly_sales AS (
        SELECT
            DATE_TRUNC('month', transaction_date) AS month,
            ROUND(SUM(revenue), 2) AS monthly_revenue
        FROM transactions
        GROUP BY month
    ),

    growth_data AS (
        SELECT
            month,
            monthly_revenue,
            LAG(monthly_revenue) OVER (
                ORDER BY month
            ) AS previous_month_revenue
        FROM monthly_sales
    )

    SELECT
        month,
        monthly_revenue,
        previous_month_revenue,
        ROUND(
            (monthly_revenue - previous_month_revenue)
            / NULLIF(previous_month_revenue, 0) * 100,
            2
        ) AS growth_percentage
    FROM growth_data
    ORDER BY month ASC
""").df()

print("\nMONTH-OVER-MONTH REVENUE GROWTH")
print(monthly_growth)


# Question 6: Average Transaction Value (ATV)
average_transaction_value = con.execute("""
    SELECT
        ROUND(SUM(revenue), 2) AS total_revenue,
        COUNT(*) AS total_transactions,
        ROUND(
            SUM(revenue) / NULLIF(COUNT(*), 0),
            2
        ) AS average_transaction_value
    FROM transactions
""").df()

print("\nAVERAGE TRANSACTION VALUE")
print(average_transaction_value)


# Question 7: Average Transaction Value by Store
atv_per_store = con.execute("""
    SELECT
        store,
        COUNT(*) AS total_transactions,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(
            SUM(revenue) / NULLIF(COUNT(*), 0),
            2
        ) AS average_transaction_value
    FROM transactions
    GROUP BY store
    ORDER BY average_transaction_value DESC
""").df()

print("\nAVERAGE TRANSACTION VALUE PER STORE")
print(atv_per_store)


# Question 8: Revenue by Product Category
revenue_by_category = con.execute("""
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
""").df()

print("\nREVENUE BY PRODUCT CATEGORY")
print(revenue_by_category)


# Question 9: Sales Performance by Payment Method
payment_analysis = con.execute("""
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
""").df()

print("\nSALES PERFORMANCE BY PAYMENT METHOD")
print(payment_analysis)



con.close()
