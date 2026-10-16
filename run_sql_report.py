
import sqlite3
from pathlib import Path

db_path = Path("database/kenyan_financial_analytics.db")
sql_path = Path("sql/analysis/01_transaction_overview.sql")

if not db_path.exists():
    raise SystemExit(f"Database not found: {db_path}")

if not sql_path.exists():
    raise SystemExit(f"SQL file not found: {sql_path}")

sql_text = sql_path.read_text(encoding="utf-8")

# Split the script into individual queries using semicolons.
queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

with sqlite3.connect(db_path) as connection:
    for number, query in enumerate(queries, start=1):
        print(f"\n{'=' * 20} REPORT {number} {'=' * 20}")

        cursor = connection.execute(query)
        headers = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        print(" | ".join(headers))
        print("-" * 100)

        for row in rows:
            print(" | ".join(
                str(value) if value is not None else "NULL"
                for value in row
            ))

print("\nAll SQL reports executed successfully.")