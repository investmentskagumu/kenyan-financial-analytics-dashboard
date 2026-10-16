
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "financial_transactions_powerbi.csv"
)

REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "customer_id",
    "customer_segment",
    "payment_method",
    "transaction_type",
    "transaction_amount_ksh",
    "transaction_status",
    "fee_amount_ksh",
    "transaction_month",
    "transaction_year",
    "transaction_hour",
    "day_of_week",
    "is_successful",
    "is_failed",
    "is_pending",
]

STATUS_FLAGS = {
    "Successful": (1, 0, 0),
    "Failed": (0, 1, 0),
    "Pending": (0, 0, 1),
}


def main():
    if not FILE_PATH.exists():
        print(f"ERROR: File not found: {FILE_PATH}")
        return

    errors = []
    seen_ids = set()
    row_count = 0
    status_counts = {
        "Successful": 0,
        "Failed": 0,
        "Pending": 0,
    }

    try:
        with FILE_PATH.open(
            "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("ERROR: CSV has no header.")
                return

            missing = [
                col for col in REQUIRED_COLUMNS
                if col not in reader.fieldnames
            ]

            if missing:
                print(f"ERROR: Missing columns: {missing}")
                return

            if len(reader.fieldnames) != len(set(reader.fieldnames)):
                errors.append("Duplicate column names found.")

            for line_number, row in enumerate(reader, start=2):
                row_count += 1

                transaction_id = row["transaction_id"]

                if transaction_id in seen_ids:
                    errors.append(
                        f"Duplicate ID at CSV line {line_number}."
                    )
                seen_ids.add(transaction_id)

                try:
                    date_value = datetime.strptime(
                        row["transaction_date"],
                        "%Y-%m-%d %H:%M:%S",
                    )

                    if row["transaction_month"] != date_value.strftime("%Y-%m"):
                        errors.append(
                            f"Incorrect month at line {line_number}."
                        )

                    if row["transaction_year"] != str(date_value.year):
                        errors.append(
                            f"Incorrect year at line {line_number}."
                        )

                    if row["transaction_hour"] != str(date_value.hour):
                        errors.append(
                            f"Incorrect hour at line {line_number}."
                        )

                    if row["day_of_week"] != date_value.strftime("%A"):
                        errors.append(
                            f"Incorrect weekday at line {line_number}."
                        )

                except ValueError:
                    errors.append(
                        f"Invalid date at CSV line {line_number}."
                    )

                try:
                    amount = float(row["transaction_amount_ksh"])
                    fee = float(row["fee_amount_ksh"])

                    if amount < 0 or fee < 0:
                        errors.append(
                            f"Negative amount or fee at line {line_number}."
                        )
                except (ValueError, TypeError):
                    errors.append(
                        f"Invalid numeric value at line {line_number}."
                    )

                status = row["transaction_status"]

                if status not in STATUS_FLAGS:
                    errors.append(
                        f"Unexpected status at line {line_number}."
                    )
                    continue

                status_counts[status] += 1

                expected_flags = STATUS_FLAGS[status]
                actual_flags = (
                    row["is_successful"],
                    row["is_failed"],
                    row["is_pending"],
                )

                if actual_flags != tuple(map(str, expected_flags)):
                    errors.append(
                        f"Status indicator mismatch at line {line_number}."
                    )

    except OSError as error:
        print(f"ERROR reading file: {error}")
        return

    print("\nPROCESSED DATASET VALIDATION")
    print("-" * 35)
    print(f"Total records: {row_count:,}")
    print(f"Unique transaction IDs: {len(seen_ids):,}")
    print(f"Successful: {status_counts['Successful']:,}")
    print(f"Failed: {status_counts['Failed']:,}")
    print(f"Pending: {status_counts['Pending']:,}")

    if row_count != 10000:
        errors.append(
            f"Expected 10,000 records but found {row_count}."
        )

    if len(seen_ids) != row_count:
        errors.append("Record count and unique ID count do not match.")

    if errors:
        print(f"\nVALIDATION FAILED: {len(errors)} issue(s).")
        for error in errors[:20]:
            print(f"- {error}")

        if len(errors) > 20:
            print(f"- ...and {len(errors) - 20} more issue(s).")
    else:
        print("\nVALIDATION PASSED: All checks completed successfully.")
        print("No files were modified.")


if __name__ == "__main__":
    main()