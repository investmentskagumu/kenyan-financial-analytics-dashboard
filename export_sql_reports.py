
import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("database/kenyan_financial_analytics.db")
OUTPUT_DIR = Path("reports/sql_exports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

reports = {
    "transaction_overview.csv": """
        SELECT
            transaction_status,
            COUNT(*) AS transaction_count,
            ROUND(SUM(transaction_amount_ksh), 2)
                AS transaction_value_ksh
        FROM transactions
        GROUP BY transaction_status
        ORDER BY transaction_count DESC
    """,
    "payment_method_analysis.csv": """
        SELECT
            payment_method,
            COUNT(*) AS transaction_count,
            ROUND(100.0 * SUM(
                CASE WHEN transaction_status = 'Successful'
                THEN 1 ELSE 0 END
            ) / COUNT(*), 2) AS success_rate_pct,
            ROUND(SUM(
                CASE WHEN transaction_status = 'Successful'
                THEN transaction_amount_ksh ELSE 0 END
            ), 2) AS successful_value_ksh
        FROM transactions
        GROUP BY payment_method
        ORDER BY successful_value_ksh DESC
    """,
    "monthly_trends.csv": """
        SELECT
            SUBSTR(transaction_date, 1, 7) AS transaction_month,
            COUNT(*) AS transaction_count,
            ROUND(SUM(
                CASE WHEN transaction_status = 'Successful'
                THEN transaction_amount_ksh ELSE 0 END
            ), 2) AS successful_value_ksh,
            ROUND(SUM(
                CASE WHEN transaction_status = 'Successful'
                THEN fee_amount_ksh ELSE 0 END
            ), 2) AS simulated_fees_ksh
        FROM transactions
        GROUP BY SUBSTR(transaction_date, 1, 7)
        ORDER BY transaction_month
    """,
    "customer_activity.csv": """
        SELECT
            CASE
                WHEN transaction_count = 1 THEN 'One-time'
                WHEN transaction_count BETWEEN 2 AND 5
                    THEN 'Occasional'
                ELSE 'Frequent'
            END AS activity_group,
            COUNT(*) AS customer_count
        FROM (
            SELECT customer_id, COUNT(*) AS transaction_count
            FROM transactions
            GROUP BY customer_id
        )
        GROUP BY activity_group
        ORDER BY customer_count DESC
    """
}

with sqlite3.connect(DB_PATH) as connection:
    for filename, query in reports.items():
        cursor = connection.execute(query)
        headers = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        output_path = OUTPUT_DIR / filename

        with output_path.open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"Exported: {output_path} ({len(rows)} rows)")

print("All SQL report exports completed.")