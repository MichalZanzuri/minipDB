--store table--
--change the size of value to be longer
ALTER TABLE store
ALTER COLUMN storelocation TYPE varchar(50);

ALTER TABLE store
ALTER COLUMN phone TYPE varchar(50);

--insert values from store_temp table to store table 
INSERT INTO store (storeid, openinghours, storelocation, phone, revenue)
SELECT storeid, 
       CAST(openinghours AS time), 
       location, 
       phone, 
       revenue
FROM store_temp;

DROP TABLE IF EXISTS store_temp;

--person table--
INSERT INTO person (personid, fullname, joinperson)
SELECT employee_id, full_name, hire_date
FROM employee_temp;

INSERT INTO employee (personid, job_title, hire_date)
SELECT employee_id, job_title, hire_date
FROM employee_temp;

-- copy values from -employee_temp to-person
INSERT INTO person (personid, fullname, joinperson)
SELECT employee_id, full_name, hire_date
FROM employee_temp
WHERE employee_id IS NOT NULL;

-- copy values from-costumer_temp to-person
INSERT INTO person (personid, fullname, joinperson)
SELECT customerid, fullname, joindate
FROM customer_temp
WHERE customerid IS NOT NULL;

--employee table--
CREATE TABLE employee (
    job_title TEXT
) INHERITS (person);

INSERT INTO employee (personid, fullname, joinperson, job_title)
SELECT employee_id, full_name, hire_date, job_title
FROM employee_temp;

--check that employee is a person child's
SELECT inhrelid::regclass AS child_table, inhparent::regclass AS parent_table
FROM pg_inherits
WHERE inhrelid = 'employee'::regclass;

--customer table--
CREATE TABLE customer (
    email VARCHAR(100),
    phone VARCHAR(20)
) INHERITS (person);

INSERT INTO customer (personid, fullname, joinperson, email, phone)
SELECT customerid, fullname, joindate, email, phone
FROM customer_temp;


--sale table--
INSERT INTO sale (saleid, saledate, totalprice, customerid)
SELECT saleid, saledate, totalprice, customerid
FROM sale_temp;

--saleproduct table--
INSERT INTO saleproduct (saleid, product_id, quantity)
SELECT saleid, productid, quantity
FROM saleproduct_temp;

--salereturnproduct table--
INSERT INTO salereturnproduct (saleid, return_id)
SELECT saleid, return_id
FROM sale, returnproduct;


--discount table--
ALTER TABLE discount
DROP COLUMN product_id;

INSERT INTO discount (discountid, discountrate, startdate, enddate, storeid)
SELECT discountid, discountrate, startdate, enddate, storeid
FROM discount_temp;

--product table--
INSERT INTO product (
    product_id,
    price,
    category,
    amount,
    product_name,
    minamount
)
SELECT
    pt.productid,
    pt.price,
    pt.category,
    pt.stock,
    pt.productname,
    p.minamount
FROM product_temp pt
LEFT JOIN product p ON pt.productid = p.product_id;





