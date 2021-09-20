-- SQLite

-- Cross-product of unique positions, and months
        --  Making sure that if there is a month with no job postings for that position,
        --  the average salary will be Null.

--  Adding the average salary values


-- 1. Get the average monthly starting salary of keyword positions
-- 2. Union All 
-- 3. With the average monthly starting salary of queried position titles
--      a. If there is no postings for a certain position in a month, leave Null

SELECT date(publishDate, 'start of month') AS 'month',
       'keywords' AS 'positionQuery',
       ROUND(AVG(startingSalary * keywords.salaryMultiplier), 2) AS 'averageSalary'
FROM keywords
GROUP BY date(publishDate, 'start of month')

UNION ALL

SELECT default_salaries.month, default_salaries.positionQuery, averageSalary
FROM

    (
    SELECT *, 0 AS 'defaultSalary'
    FROM
         (SELECT DISTINCT positionQuery FROM positions),
         (SELECT DISTINCT date(publishDate, 'start of month') AS 'month' FROM positions)
    ORDER BY month
    ) AS default_salaries

LEFT JOIN

    (
    SELECT date(publishDate, 'start of month') AS 'month',
           positionQuery,
           ROUND(AVG(startingSalary * positions.salaryMultiplier), 2) AS 'averageSalary'
    FROM positions
    GROUP BY date(publishDate, 'start of month'), positionQuery
    ) AS salaries

ON default_salaries.month = salaries.month AND
   default_salaries.positionQuery = salaries.positionQuery

ORDER BY month, positionQuery;