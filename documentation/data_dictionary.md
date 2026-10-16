

\# Kenyan Financial Analytics Dashboard

\## Data Dictionary



\### Project overview

This project analyzes 10,000 synthetic Kenyan-style financial

transactions covering January–December 2025.



The dataset is simulated for educational and portfolio purposes.

It does not represent actual transactions from Kenyan banks,

mobile-money providers, or customers.



\### Source file

`data/raw/kenyan\_financial\_transactions.csv`



\### Database

`database/kenyan\_financial\_analytics.db`



\### Table: transactions



| Column | Data type | Description |

|---|---|---|

| transaction\_id | TEXT | Unique transaction identifier; primary key |

| transaction\_date | TEXT | Transaction date and time in ISO-style format |

| customer\_id | TEXT | Synthetic customer identifier |

| customer\_segment | TEXT | Synthetic customer segment assigned to each transaction |

| payment\_method | TEXT | Simulated payment channel |

| transaction\_type | TEXT | Payment, transfer, withdrawal, or deposit |

| transaction\_amount\_ksh | REAL | Transaction amount in Kenyan shillings |

| transaction\_status | TEXT | Successful, Failed, or Pending |

| fee\_amount\_ksh | REAL | Simulated fee amount in Kenyan shillings |



\### Data quality checks

\- 10,000 transaction records loaded.

\- Nine columns present.

\- No missing values detected in the original CSV.

\- No duplicate transaction IDs detected.

\- No negative or invalid transaction amounts detected.

\- Transaction dates standardized during database loading.



\### Analytical definitions

\- Successful transaction value: sum of amounts for successful transactions.

\- Success rate: successful transactions divided by all transactions.

\- Failure rate: failed transactions divided by all transactions.

\- Simulated fees: sum of fee amounts in the synthetic dataset.

\- One-time customer: one transaction across the dataset.

\- Occasional customer: two to five transactions.

\- Frequent customer: more than five transactions.



\### Limitations

\- All transactions and customer identifiers are synthetic.

\- Customer segments are assigned per transaction and may not remain consistent for a customer.

\- Payment methods and transaction outcomes are simulated.

\- Simulated fees are not actual revenue.

\- Findings must not be presented as evidence of actual Kenyan financial-market performance.