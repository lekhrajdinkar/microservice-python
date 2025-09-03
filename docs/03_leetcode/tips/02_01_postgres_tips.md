- [Top 50](https://leetcode.com/problems/rising-temperature/?envType=study-plan-v2&envId=top-sql-50)

```sql
where b.bonus  is null
where b.bonus  = null ❌

No, COUNT(col1) in PostgreSQL does not count NULLs.

-- ✔️ no on condition in "cross join"
FROM Weather yesterday CROSS JOIN Weather today 
-- A CROSS JOIN does not require a join condition. 
-- It returns the Cartesian product of the two tables

SELECT * FROM products CROSS JOIN colors;

SELECT * FROM products INNER JOIN colors; 
This is technically valid SQL, but without a join-condition, it acts like  CROSS JOIN ⬅️


→ This returns every combination of products × colors.
    avoid On large datasets
    use with - Without a filter/where condition


-- ✔️ DATE or TIMESTAMP fields diff
WHERE today.recordDate - yesterday.recordDate = 1 
WHERE today.recordDate - yesterday.recordDate = INTERVAL '1 day'

-- ✔️ rouding of timestanp
ROUND(AVG(EXTRACT(EPOCH FROM (a2.timestamp - a1.timestamp))), 3) AS processing_time

-- =============== C. Basic Aggregate Functions =========
where id % 2 = 1 -- true false in where ✔️

-- type casting ✔️
SELECT '123'::int;              -- text to integer → 123
SELECT 10 / 3;                  -- integer division → 3
SELECT 10::numeric / 3;         -- numeric division → 3.333...
SELECT 'true'::boolean;         -- → true
SELECT '2024-01-01'::date;      -- → 2024-01-01
SELECT 123::text;               -- integer to text → '123'

-- or, with function
CAST('123' AS int); -- ✔️

SELECT COALESCE(u.units, 0) FROM table1;
→ Returns the first non-NULL value from the list. ✔️

    CASE --✔️
        WHEN sum(units) = 0 THEN 0 
        WHEN sum(units) > 0 THEN round((sum(amt)::numeric / sum(units) ),2)  -- ✔️ round(numeric1, 2)
    END as col1

order by percentage DESC, r.contest_id  ASC 😶✔️

TO_CHAR(date1, 'YYYY-MM') AS year_month ✔️

string_to_array(str,'-')[1] --starts with 1, index ✔️

with cte1 as (...), cte2 as (...)

-- filter on count
COUNT(*) FILTER (WHERE temp1.del_type = 'immediate')  ⬅️
vs 
count(temp1.del_type)
--count(temp1.del_type = 'immediate') , does not on postgres

Count(distinct user_id) vs  Count(user_id) ⬅️

where (product_id , year) in ⬅️

-- reuse of alias may not always work in HAVING
```



