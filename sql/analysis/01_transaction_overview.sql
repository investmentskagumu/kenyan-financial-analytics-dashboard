
-- PROJECT: Kenyan Financial Analytics Dashboard
-- REPORT: Transaction Overview
-- DATA: Synthetic Kenyan-style financial transactions
-- PERIOD: January to December 2025

-- 1. Overall transaction performance
SELECT
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(
        CASE
            WHEN transaction_status = 'Successful'
            THEN transaction_amount_ksh
            ELSE 0
        END
    ), 2) AS successful_transaction_value_ksh,
    ROUND(AVG(
        CASE
            WHEN transaction_status = 'Successful'
            THEN transaction_amount_ksh
        END
    ), 2) AS avg_successful_transaction_ksh,
    ROUND(
        100.0 * SUM(
            CASE WHEN transaction_status = 'Successful'
            THEN 1 ELSE 0 END
        ) / COUNT(*), 2
    ) AS success_rate_pct,
    ROUND(
        100.0 * SUM(
            CASE WHEN transaction_status = 'Failed'
            THEN 1 ELSE 0 END
        ) / COUNT(*), 2
    ) AS failure_rate_pct
FROM transactions;


-- 2. Transaction performance by payment method
SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    SUM(
        CASE WHEN transaction_status = 'Successful'
        THEN 1 ELSE 0 END
    ) AS successful_transactions,
    SUM(
        CASE WHEN transaction_status = 'Failed'
        THEN 1 ELSE 0 END
    ) AS failed_transactions,
    ROUND(SUM(
        CASE WHEN transaction_status = 'Successful'
        THEN transaction_amount_ksh ELSE 0 END
    ), 2) AS successful_value_ksh,
    ROUND(
        100.0 * SUM(
            CASE WHEN transaction_status = 'Successful'
            THEN 1 ELSE 0 END
        ) / COUNT(*), 2
    ) AS success_rate_pct
FROM transactions
GROUP BY payment_method
ORDER BY successful_value_ksh DESC;


-- 3. Monthly transaction trends
SELECT
    SUBSTR(transaction_date, 1, 7) AS transaction_month,
    COUNT(*) AS total_transactions,
    SUM(
        CASE WHEN transaction_status = 'Successful'
        THEN 1 ELSE 0 END
    ) AS successful_transactions,
    ROUND(SUM(
        CASE WHEN transaction_status = 'Successful'
        THEN transaction_amount_ksh ELSE 0 END
    ), 2) AS successful_value_ksh,
    ROUND(SUM(
        CASE WHEN transaction_status = 'Successful'
        THEN fee_amount_ksh ELSE 0 END
    ), 2) AS successful_fees_ksh
FROM transactions
GROUP BY SUBSTR(transaction_date, 1, 7)
ORDER BY transaction_month;