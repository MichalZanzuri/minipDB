--supplier_orders_with_employee
CREATE VIEW supplier_orders_with_employee AS
SELECT
    o.order_id,
    o.order_date,
    o.supplier_id,
    s.company_name AS supplier_name,
    o.employee_id,
    e.fullname
FROM Order_d o
JOIN supplier s ON o.supplier_id = s.supplier_id
JOIN employee e ON o.employee_id = e.personid;

--All orders placed by a specific employee
SELECT *
FROM supplier_orders_with_employee
WHERE fullname = 'Dana Snyder';

--check the name of column of views
SELECT *
FROM supplier_orders_with_employee
LIMIT 1;


--How many orders did each employee place
SELECT fullname, COUNT(*) AS total_orders
FROM supplier_orders_with_employee
GROUP BY fullname;

--customer_sales_view
CREATE OR REPLACE VIEW customer_sales_view AS
SELECT
    c.personid,
    c.fullname,
    c.email,
    c.phone,
    sa.saleid,
    sa.saledate,
    sa.totalprice
FROM customer c
LEFT JOIN sale sa ON c.personid = sa.customerid;


--All customers with their sales
SELECT * FROM customer_sales_view;

--All customers who made a sale on a specific date
SELECT *
FROM customer_sales_view
WHERE saledate = '2025-05-01';
