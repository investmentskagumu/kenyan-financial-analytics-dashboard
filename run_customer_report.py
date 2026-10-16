
import sqlite3
from pathlib import Path

db_path = Path("database/kenyan_financial_analytics.db")
sql_path = Path("sql/analysis/02_customer_analysis.sql")

sql_text = sql_path.read_text(encoding="utf-8")
queries = [q.strip() for q in sql_text.split(";") if q.strip()]

with sqlite3.connect(db_path) as connection:
    for i, query in enumerate(queries, start=1):
        print(f"\n========== CUSTOMER REPORT {i} ==========")
        cursor = connection.execute(query)
        print(" | ".join(col[0] for col in cursor.description))
        for row in cursor.fetchall():
            print(" | ".join(str(value) for value in row))

print("\nCustomer analysis completed.")