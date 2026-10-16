
import csv
from pathlib import Path
from datetime import datetime

# Project paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "raw" / "kenyan_financial_transactions.csv"
OUTPUT_FILE = (
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
]

DATE_FORMATS = [
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%m/%d/%Y %H:%M",
]


def parse_transaction_date(value):
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), date_format)
        except ValueError:
            continue

    raise ValueError(f"Unrecognized transaction date: {value!r}")


def main():
    # Protect existing work.
    if OUTPUT_FILE.exists():
        print("STOPPED: The output file already exists.")
        print(f"Nothing was overwritten: {OUTPUT_FILE}")
        print("Inspect or back up that file before deciding what to do next.")
        return

    if not INPUT_FILE.exists():
        print(f"ERROR: Source dataset not found: {INPUT_FILE}")
        return

    # Validate every record before writing any output.
    prepared_rows = []
    seen_ids = set()

    try:
        with INPUT_FILE.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("The source CSV has no header row.")

            missing_columns = [
                column for column in REQUIRED_COLUMNS
                if column not in reader.fieldnames
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}"
                )

            for row_number, row in enumerate(reader, start=2):
                for column in REQUIRED_COLUMNS:
                    if row.get(column) is None or not row[column].strip():
                        raise ValueError(
                            f"Blank value in {column}, CSV row {row_number}."
                        )

                transaction_id = row["transaction_id"].strip()

                if transaction_id in seen_ids:
                    raise ValueError(
                        f"Duplicate transaction ID {transaction_id!r} "
                        f"at CSV row {row_number}."
                    )

                seen_ids.add(transaction_id)

                transaction_date = parse_transaction_date(
                    row["transaction_date"]
                )

                amount = float(row["transaction_amount_ksh"])
                fee = float(row["fee_amount_ksh"])

                if amount < 0 or fee < 0:
                    raise ValueError(
                        f"Negative amount or fee at CSV row {row_number}."
                    )

                status = row["transaction_status"].strip()

                if status not in {"Successful", "Failed", "Pending"}:
                    raise ValueError(
                        f"Unexpected transaction status {status!r} "
                        f"at CSV row {row_number}."
                    )

                cleaned = {
                    column: row[column].strip()
                    for column in REQUIRED_COLUMNS
                }

                cleaned["transaction_date"] = (
                    transaction_date.strftime("%Y-%m-%d %H:%M:%S")
                )
                cleaned["transaction_amount_ksh"] = f"{amount:.2f}"
                cleaned["fee_amount_ksh"] = f"{fee:.2f}"
                cleaned["transaction_month"] = (
                    transaction_date.strftime("%Y-%m")
                )
                cleaned["transaction_year"] = str(
                    transaction_date.year
                )
                cleaned["transaction_hour"] = str(
                    transaction_date.hour
                )
                cleaned["day_of_week"] = (
                    transaction_date.strftime("%A")
                )
                cleaned["is_successful"] = int(status == "Successful")
                cleaned["is_failed"] = int(status == "Failed")
                cleaned["is_pending"] = int(status == "Pending")

                prepared_rows.append(cleaned)

        if not prepared_rows:
            raise ValueError("The source dataset contains no records.")

        output_columns = REQUIRED_COLUMNS + [
            "transaction_month",
            "transaction_year",
            "transaction_hour",
            "day_of_week",
            "is_successful",
            "is_failed",
            "is_pending",
        ]

        # Exclusive creation prevents overwriting an existing file.
        with OUTPUT_FILE.open(
            "x", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=output_columns)
            writer.writeheader()
            writer.writerows(prepared_rows)

    except FileExistsError:
        print("STOPPED: The output file already exists. Nothing overwritten.")
        return
    except (OSError, ValueError) as error:
        print(f"VALIDATION/PREPARATION ERROR: {error}")
        return

    print("POWER BI DATASET CREATED SUCCESSFULLY")
    print(f"Records prepared: {len(prepared_rows):,}")
    print(f"Unique transaction IDs: {len(seen_ids):,}")
    print(f"Output file: {OUTPUT_FILE}")
    print("Original raw CSV and SQLite database were not modified.")
    print(
        "Note: customer_segment is retained as supplied; "
        "it is not yet reliable for customer-level segment comparisons."
    )


if __name__ == "__main__":
    main()