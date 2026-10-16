
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Reproducible synthetic data
random.seed(42)

OUTPUT = Path("data/raw/kenyan_financial_transactions.csv")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

NUM_TRANSACTIONS = 10000
START_DATE = datetime(2025, 1, 1)

payment_methods = ["M-Pesa", "Bank Transfer", "Debit Card", "Airtel Money"]
transaction_types = ["Payment", "Transfer", "Withdrawal", "Deposit"]
statuses = ["Successful", "Failed", "Pending"]
customer_segments = ["Individual", "Small Business", "Corporate"]

rows = []

for i in range(1, NUM_TRANSACTIONS + 1):
    customer_id = f"CUST{random.randint(1, 2000):05d}"
    transaction_date = START_DATE + timedelta(
        minutes=random.randint(0, 365 * 24 * 60 - 1)
    )

    payment_method = random.choices(
        payment_methods, weights=[55, 20, 15, 10]
    )[0]

    transaction_type = random.choice(transaction_types)
    status = random.choices(
        statuses, weights=[92, 6, 2]
    )[0]

    amount = round(random.uniform(50, 50000), 2)

    fee_rate = {
        "M-Pesa": 0.008,
        "Bank Transfer": 0.005,
        "Debit Card": 0.015,
        "Airtel Money": 0.008,
    }[payment_method]

    fee_amount = round(amount * fee_rate, 2) if status == "Successful" else 0.00

    segment = random.choices(
        customer_segments, weights=[75, 20, 5]
    )[0]

    rows.append({
        "transaction_id": f"TXN{i:07d}",
        "transaction_date": transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
        "customer_id": customer_id,
        "customer_segment": segment,
        "payment_method": payment_method,
        "transaction_type": transaction_type,
        "transaction_amount_ksh": amount,
        "transaction_status": status,
        "fee_amount_ksh": fee_amount,
    })

with OUTPUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Dataset generated successfully.")
print(f"Records: {len(rows):,}")
print(f"Output: {OUTPUT}")
print("NOTE: This is synthetic data, not real Kenyan financial data.")