USE DATABASE GET_COMPANIES;
USE SCHEMA PUBLIC;

SELECT registrationDate, COUNT(*) AS company_count
FROM companies
GROUP BY registrationDate
ORDER BY company_count DESC
LIMIT 1;