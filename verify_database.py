
import sqlite3
from pathlib import Path

DB_PATH = Path("database/kenyan_financial_analytics.db")

if not DB_PATH.exists():
    raise SystemExit("Database file not found.")

connection = sqlite3.connect(DB_PATH)

print("=== DATABASE VERIFICATION ===")

# 1. Confirm row count
count = connection.execute(
    "SELECT COUNT(*) FROM transactions"
).fetchone()[0]
print(f"Total transactions: {count:,}")

# 2. Confirm table structure
print("\n=== TABLE COLUMNS ===")
columns = connection.execute(
    "PRAGMA table_info(transactions)"
).fetchall()

for column in columns:
    print(f"{column[1]}: {column[2]}")

# 3. Inspect standardized dates
print("\n=== DATE RANGE ===")
print(connection.execute("""
    SELECT MIN(transaction_date), MAX(transaction_date)
    FROM transactions
""").fetchone())

# 4. Verify transaction status totals
print("\n=== STATUS SUMMARY ===")
for row in connection.execute("""
    SELECT transaction_status, COUNT(*)
    FROM transactions
    GROUP BY transaction_status
    ORDER BY COUNT(*) DESC
"""):
    print(f"{row[0]}: {row[1]:,}")

# 5. Check duplicate transaction IDs
duplicates = connection.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT transaction_id
        FROM transactions
        GROUP BY transaction_id
        HAVING COUNT(*) > 1
    )
""").fetchone()[0]

print(f"\nDuplicate transaction IDs: {duplicates}")

connection.close()
print("\nVerification complete.")