--10% price increase for products sold over 100 times
--#1
UPDATE Product
SET price = price * 1.10
WHERE product_id IN (
    SELECT product_id
    FROM ProductOrder
    GROUP BY product_id
    HAVING COUNT(*) > 100
);





--Title update of employees who joined 3 years ago to "Senior"
--#2
UPDATE Employee
SET job_title = 'Senior'
WHERE hire_date < CURRENT_DATE - INTERVAL '3 years';

--צפיה בשינוי הסטטוס
--SELECT * FROM Employee
--WHERE job_title = 'Senior';




--20% discount on all products of a certain category
--#3
UPDATE Product
SET price = price * 0.80
WHERE category = 'test'
RETURNING product_id, product_name, category, price;

--צפיה במוצרי הקטגריה הנבחרת לאחר השינוי
--SELECT * FROM Product
--WHERE category='a'
