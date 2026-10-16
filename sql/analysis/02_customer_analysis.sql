
-- PROJECT: Kenyan Financial Analytics Dashboard
-- REPORT: Customer Behavior Analysis
-- DATA: Synthetic financial transactions

-- 1. Customer activity summary
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN transaction_count = 1 THEN 1 ELSE 0 END)
        AS one_time_customers,
    SUM(CASE WHEN transaction_count BETWEEN 2 AND 5 THEN 1 ELSE 0 END)
        AS occasional_customers,
    SUM(CASE WHEN transaction_count > 5 THEN 1 ELSE 0 END)
        AS frequent_customers,
    ROUND(AVG(transaction_count), 2)
        AS avg_transactions_per_customer
FROM (
    SELECT customer_id, COUNT(*) AS transaction_count
    FROM transactions
    GROUP BY customer_id
);


-- 2. Top 10 customers by successful transaction value
SELECT
    customer_id,
    COUNT(*) AS successful_transactions,
    ROUND(SUM(transaction_amount_ksh), 2)
        AS successful_value_ksh,
    ROUND(SUM(fee_amount_ksh), 2)
        AS simulated_fees_ksh
FROM transactions
WHERE transaction_status = 'Successful'
GROUP BY customer_id
ORDER BY successful_value_ksh DESC
LIMIT 10;


-- 3. Transaction activity by customer
SELECT
    CASE
        WHEN transaction_count = 1 THEN 'One-time'
        WHEN transaction_count BETWEEN 2 AND 5 THEN 'Occasional'
        ELSE 'Frequent'
    END AS activity_group,
    COUNT(*) AS customer_count,
    ROUND(AVG(transaction_count), 2)
        AS avg_transactions_per_customer
FROM (
    SELECT customer_id, COUNT(*) AS transaction_count
    FROM transactions
    GROUP BY customer_id
)
GROUP BY activity_group
ORDER BY customer_count DESC;
