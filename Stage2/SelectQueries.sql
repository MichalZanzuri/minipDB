-- How many orders each supplier had each year by status
--#1
SELECT 
    S.supplier_id,
    S.company_name,
    EXTRACT(YEAR FROM O.order_date) AS order_year,
    O.status,
    COUNT(*) AS total_orders
FROM 
    Order_d O
JOIN 
    Supplier S ON O.supplier_id = S.supplier_id
GROUP BY 
    S.supplier_id, S.company_name, order_year, O.status
ORDER BY 
    order_year, total_orders DESC;





--Average amount of orders per product
--#2
SELECT 
    P.product_id,
    P.product_name,
    P.category,
    ROUND(AVG(O.quantity), 2) AS avg_quantity
FROM 
    Product P
JOIN 
    ProductOrder PO ON P.product_id = PO.product_id
JOIN 
    Order_d O ON PO.order_id = O.order_id
GROUP BY 
    P.product_id, P.product_name, P.category
ORDER BY 
    avg_quantity DESC;





--Average product price by category and month of addition
--#3
SELECT 
    product_name,
    category,
    EXTRACT(MONTH FROM added_date) AS added_month,
    ROUND(AVG(price), 2) AS avg_price
FROM 
    Product
GROUP BY 
    product_name, category, added_month
ORDER BY 
    category, added_month, product_name;




--Quotations that have expired this month
--#4
SELECT 
    Q.number,
    S.company_name,
    Q.q_price,
    Q.expiration_date,
    EXTRACT(DAY FROM Q.expiration_date) AS day,
    EXTRACT(MONTH FROM Q.expiration_date) AS month,
    EXTRACT(YEAR FROM Q.expiration_date) AS year
FROM 
    Quotation Q
JOIN 
    Supplier S ON Q.supplier_id = S.supplier_id
WHERE 
    Q.expiration_date < CURRENT_DATE
    AND EXTRACT(MONTH FROM Q.expiration_date) = EXTRACT(MONTH FROM CURRENT_DATE)
ORDER BY 
    Q.expiration_date DESC;





--Employees who ordered more than 3 orders totaling more than 1000 ILS
--#5
SELECT 
    E.full_name,
    COUNT(O.order_id) AS total_orders,
    SUM(O.cost) AS total_cost
FROM 
    Order_d O
JOIN 
    Employee E ON O.employee_id = E.employee_id
GROUP BY 
    E.employee_id, E.full_name
HAVING 
    COUNT(O.order_id) > 3 AND SUM(O.cost) > 1000
ORDER BY 
    total_cost DESC;





--All returns from the last year, including supplier details
--#6
SELECT 
    R.return_id,
    R.return_date,
    R.return_status,
    R.return_reason,
    S.company_name
FROM 
    ReturnProduct R
LEFT JOIN 
    Supplier S ON R.supplier_id = S.supplier_id
WHERE 
    R.return_date < CURRENT_DATE - INTERVAL '1 year'
ORDER BY 
    R.return_date DESC;





--The amount of orders that arrived on time and the amount of orders that arrived late
--#7
SELECT
    SUM(CASE WHEN delivery_date <= arrival_date THEN 1 ELSE 0 END) AS on_time_orders,
    SUM(CASE WHEN delivery_date > arrival_date THEN 1 ELSE 0 END) AS late_orders
FROM Order_d
WHERE delivery_date IS NOT NULL AND arrival_date IS NOT NULL;





--Quantity of products by color and gender, divided by month of addition
--#8
SELECT
    color,
    gender,
    EXTRACT(MONTH FROM added_date) AS added_month,
    COUNT(*) AS product_count
FROM Product
WHERE gender IS NOT NULL
  AND color IS NOT NULL
  AND EXTRACT(MONTH FROM added_date) IS NOT NULL
GROUP BY color, gender, added_month
ORDER BY added_month, product_count DESC;

