USE customer_churn_analysis;

SELECT COUNT(*) AS total_customers
FROM customer_churn_cleaned;

SELECT COUNT(*) AS churned_customers
FROM customer_churn_cleaned
WHERE Churn = 'Yes';

SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS churn_rate_percentage
FROM customer_churn_cleaned;

SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS churn_rate_percentage
FROM customer_churn_cleaned
GROUP BY Contract
ORDER BY churn_rate_percentage DESC;

SELECT
    InternetService,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*), 2
    ) AS churn_rate_percentage
FROM customer_churn_cleaned
GROUP BY InternetService
ORDER BY churn_rate_percentage DESC;

USE customer_churn_analysis;

SELECT
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue,
    ROUND(
        SUM(CASE WHEN Churn = 'Yes'
                 THEN MonthlyCharges ELSE 0 END), 2
    ) AS monthly_revenue_from_churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes'
                         THEN MonthlyCharges ELSE 0 END)
        / SUM(MonthlyCharges), 2
    ) AS churned_revenue_percentage
FROM customer_churn_cleaned;


WITH contract_churn AS (
    SELECT
        Contract,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
            AS churned_customers,
        ROUND(
            100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
            / COUNT(*), 2
        ) AS churn_rate
    FROM customer_churn_cleaned
    GROUP BY Contract
)
SELECT
    Contract,
    total_customers,
    churned_customers,
    churn_rate
FROM contract_churn
ORDER BY churn_rate DESC;

WITH contract_churn AS (
    SELECT
        Contract,
        COUNT(*) AS total_customers,
        ROUND(
            100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
            / COUNT(*), 2
        ) AS churn_rate
    FROM customer_churn_cleaned
    GROUP BY Contract
)
SELECT
    Contract,
    total_customers,
    churn_rate,
    RANK() OVER (ORDER BY churn_rate DESC) AS churn_rank
FROM contract_churn;