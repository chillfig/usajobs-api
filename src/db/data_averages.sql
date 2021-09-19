-- SQLite

-- Cross-product of unique positions, and months
        --  Making sure that if there is a month with no job postings for that position,
        --  the average salary will be Null.

--  Adding the average salary values


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
   default_salaries.positionQuery = salaries.positionQuery;