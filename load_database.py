
import csv
import sqlite3
from pathlib import Path
from datetime import datetime

CSV_PATH = Path("data/raw/kenyan_financial_transactions.csv")
DB_PATH = Path("database/kenyan_financial_analytics.db")

if not CSV_PATH.exists():
    raise SystemExit(f"CSV not found: {CSV_PATH}")

# Protect an existing database from accidental overwriting.
if DB_PATH.exists():
    raise SystemExit(
        f"Database already exists: {DB_PATH}\n"
        "Stopped without modifying it. Inspect it before proceeding."
    )

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def parse_date(value):
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%m/%d/%Y %H:%M",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date: {value}")

with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

if not rows:
    raise SystemExit("CSV contains no records.")

# Build a new database without replacing any existing database.
connection = sqlite3.connect(DB_PATH)

try:
    connection.execute("""
        CREATE TABLE transactions (
            transaction_id TEXT PRIMARY KEY,
            transaction_date TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            customer_segment TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            transaction_amount_ksh REAL NOT NULL
                CHECK (transaction_amount_ksh >= 0),
            transaction_status TEXT NOT NULL
                CHECK (transaction_status IN
                    ('Successful', 'Failed', 'Pending')),
            fee_amount_ksh REAL NOT NULL
                CHECK (fee_amount_ksh >= 0)
        )
    """)

    records = []
    for row in rows:
        records.append((
            row["transaction_id"],
            parse_date(row["transaction_date"]),
            row["customer_id"],
            row["customer_segment"],
            row["payment_method"],
            row["transaction_type"],
            float(row["transaction_amount_ksh"]),
            row["transaction_status"],
            float(row["fee_amount_ksh"]),
        ))

    connection.executemany("""
        INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    connection.execute("""
        CREATE INDEX idx_transactions_date
        ON transactions(transaction_date)
    """)
    connection.execute("""
        CREATE INDEX idx_transactions_customer
        ON transactions(customer_id)
    """)
    connection.execute("""
        CREATE INDEX idx_transactions_status
        ON transactions(transaction_status)
    """)

    connection.commit()

    count = connection.execute(
        "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    print("SQLite database created successfully.")
    print(f"Records loaded: {count:,}")
    print(f"Database: {DB_PATH}")
    print("Dates standardized to YYYY-MM-DD HH:MM:SS")

except Exception:
    connection.rollback()
    connection.close()
    DB_PATH.unlink(missing_ok=True)
    raise
else:
    connection.close()