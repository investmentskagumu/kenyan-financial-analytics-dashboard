
import csv
from pathlib import Path
from collections import Counter

file_path = Path("data/raw/kenyan_financial_transactions.csv")

with file_path.open("r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print("=== DATASET VALIDATION REPORT ===")
print(f"File exists: {file_path.exists()}")
print(f"Total records: {len(rows):,}")
print(f"Total columns: {len(rows[0]) if rows else 0}")

if not rows:
    raise SystemExit("ERROR: Dataset is empty.")

print("\n=== COLUMN NAMES ===")
print(", ".join(rows[0].keys()))

# Check missing values
print("\n=== MISSING VALUES ===")
for column in rows[0].keys():
    missing = sum(
        1 for row in rows
        if not row.get(column, "").strip()
    )
    print(f"{column}: {missing}")

# Check duplicate transaction IDs
ids = [row["transaction_id"] for row in rows]
duplicate_ids = len(ids) - len(set(ids))
print(f"\nDuplicate transaction IDs: {duplicate_ids}")

# Check invalid amounts
invalid_amounts = 0
for row in rows:
    try:
        amount = float(row["transaction_amount_ksh"])
        if amount < 0:
            invalid_amounts += 1
    except (ValueError, TypeError):
        invalid_amounts += 1

print(f"Invalid transaction amounts: {invalid_amounts}")

# Check statuses
print("\n=== TRANSACTION STATUS COUNTS ===")
for status, count in Counter(
    row["transaction_status"] for row in rows
).items():
    print(f"{status}: {count:,}")

# Check payment methods
print("\n=== PAYMENT METHOD COUNTS ===")
for method, count in Counter(
    row["payment_method"] for row in rows
).items():
    print(f"{method}: {count:,}")

print("\nNOTE: Synthetic data; not real financial transactions.")