-- Fintech Retention Funnel Analysis
-- Assumes users and events tables already exist

WITH returns AS (
    SELECT
        e.user_id,
        u.signup_date,
        e.event_time,
        DATE_PART('day', e.event_time - u.signup_date) AS days_since_signup
    FROM events e
    JOIN users u
        ON e.user_id = u.user_id
    WHERE e.event_name = 'app_open_return'
),

retained_users AS (
    SELECT DISTINCT user_id
    FROM returns
    WHERE days_since_signup BETWEEN 2 AND 7
),

early_add_money AS (
    SELECT DISTINCT
        e.user_id
    FROM events e
    JOIN users u
        ON e.user_id = u.user_id
    WHERE e.event_name = 'add_money'
      AND DATE_PART('day', e.event_time - u.signup_date) BETWEEN 0 AND 3
),

early_payment AS (
    SELECT DISTINCT
        e.user_id
    FROM events e
    JOIN users u
        ON e.user_id = u.user_id
    WHERE e.event_name = 'make_payment'
      AND DATE_PART('day', e.event_time - u.signup_date) BETWEEN 0 AND 3
),

user_flags AS (
    SELECT
        u.user_id,
        CASE WHEN r.user_id IS NOT NULL THEN 1 ELSE 0 END AS retained_7d,
        CASE WHEN a.user_id IS NOT NULL THEN 1 ELSE 0 END AS early_add_money,
        CASE WHEN p.user_id IS NOT NULL THEN 1 ELSE 0 END AS early_payment,
        CASE
            WHEN a.user_id IS NOT NULL AND p.user_id IS NOT NULL THEN 'A'
            WHEN a.user_id IS NOT NULL AND p.user_id IS NULL THEN 'B'
            ELSE 'C'
        END AS user_group
    FROM users u
    LEFT JOIN retained_users r
        ON u.user_id = r.user_id
    LEFT JOIN early_add_money a
        ON u.user_id = a.user_id
    LEFT JOIN early_payment p
        ON u.user_id = p.user_id
)

-- Overall retention
SELECT
    COUNT(*) AS total_users,
    SUM(retained_7d) AS retained_users,
    ROUND(AVG(retained_7d), 4) AS retention_rate
FROM user_flags;

-- Early add money vs not
SELECT
    early_add_money,
    COUNT(*) AS total_users,
    SUM(retained_7d) AS retained_users,
    ROUND(AVG(retained_7d), 4) AS retention_rate
FROM user_flags
GROUP BY early_add_money
ORDER BY early_add_money DESC;

-- Retention by behavioural group
SELECT
    user_group,
    COUNT(*) AS total_users,
    SUM(retained_7d) AS retained_users,
    ROUND(AVG(retained_7d), 4) AS retention_rate
FROM user_flags
GROUP BY user_group
ORDER BY user_group;