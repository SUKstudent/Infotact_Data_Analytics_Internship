WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER(
               PARTITION BY "User ID"
               ORDER BY Timestamp
           ) AS rn
    FROM marketing_data
)

SELECT
    Channel,
    COUNT(*) AS first_touch_users
FROM ranked
WHERE rn = 1
GROUP BY Channel
ORDER BY first_touch_users DESC;
