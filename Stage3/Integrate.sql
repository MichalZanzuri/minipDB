ALTER TABLE ReturnProduct
ADD return_amount INT;

ALTER TABLE Employee
DROP CONSTRAINT employee_id;

ALTER TABLE Employee
DROP COLUMN full_name;

ALTER TABLE Employee
DROP COLUMN hire_date;

ALTER TABLE Employee
DROP COLUMN employee_id;

-- הוספת עמודה PersonId
ALTER TABLE Employee
ADD COLUMN PersonId INT;


-- טבלת Discount
CREATE TABLE Discount (
    DiscountId SERIAL PRIMARY KEY,
    DiscountRate DECIMAL(5, 2),
    StartDate DATE,
    EndDate DATE,
    product_id INT,  -- מפתח זר
    StoreId INT,    -- מפתח זר
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (StoreId) REFERENCES Store(StoreId)
);

-- טבלת Store
CREATE TABLE Store (
    StoreId SERIAL PRIMARY KEY,
    OpeningHours TIME,
    StoreLocation VARCHAR(255),
    Phone VARCHAR(15),
    Revenue DECIMAL(10, 2)  -- שדה אופציונלי
);

-- טבלת StoreSale
CREATE TABLE StoreSale (
    StoreId INT,  -- מפתח זר
    SaleId INT,   -- מפתח זר
    FOREIGN KEY (StoreId) REFERENCES Store(StoreId),
    FOREIGN KEY (SaleId) REFERENCES Sale(SaleId),
    PRIMARY KEY (StoreId, SaleId)
);

-- טבלת Sale
CREATE TABLE Sale (
    SaleId SERIAL PRIMARY KEY,
    SaleDate DATE,
    TotalPrice DECIMAL(10, 2),
    CustomerId INT,  -- מפתח זר
    FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
);

-- טבלת SaleProduct
CREATE TABLE SaleProduct (
    SaleId INT,    -- מפתח זר
    product_id INT, -- מפתח זר
    Quantity INT,
    FOREIGN KEY (SaleId) REFERENCES Sale(SaleId),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    PRIMARY KEY (SaleId, product_id)
);

-- טבלת SaleReturnProduct
CREATE TABLE SaleReturnProduct (
    SaleId INT,        -- מפתח זר
    return_id INT,  -- מפתח זר
    FOREIGN KEY (SaleId) REFERENCES Sale(SaleId),
    FOREIGN KEY (return_id) REFERENCES ReturnProduct(return_id)
);


-- טבלת Person
CREATE TABLE Person (
    PersonId SERIAL PRIMARY KEY,
    FullName VARCHAR(255),
    JoinPerson DATE
);

-- טבלת Customer
CREATE TABLE Customer (
    CustomerId INT PRIMARY KEY,  -- מפתח זר
    Phone VARCHAR(15),
    Email VARCHAR(255),
    FOREIGN KEY (CustomerId) REFERENCES Person(PersonId)
);

-- טבלת EmployeeOrder
CREATE TABLE EmployeeOrder (
    PersonId INT,  -- מפתח זר
    order_id INT,   -- מפתח זר
    FOREIGN KEY (PersonId) REFERENCES Employee(PersonId),
    FOREIGN KEY (order_id) REFERENCES Order_d(order_id),
    PRIMARY KEY (PersonId, order_id)
);

select * from Sale;

CREATE EXTENSION IF NOT EXISTS dblink;

INSERT INTO Product (
    product_id,
    minAmount,
    price,
    category,
    amount,
    added_date,
    product_name,
    gender,
    color,
    productSize
)
SELECT
    ProductId::INT,
    0,                     -- minAmount – שדה חדש אצלך
    Price::DECIMAL(10,2),
    Category,
    0,                     -- amount (אין אצלם stock)
    CURRENT_DATE,
    ProductName,
    NULL, NULL, NULL       -- gender, color, productSize
FROM dblink('dbname=LHDB',
            'SELECT "ProductId", "Price", "Category", "ProductName" FROM "Product"')
AS src("ProductId" INT, "Price" DECIMAL, "Category" VARCHAR, "ProductName" VARCHAR)
WHERE ProductId NOT IN (
    SELECT product_id FROM Product
);

SELECT * FROM dblink(
  'host=localhost port=5432 dbname=LHDB user=myuser password=mypassword',
  'SELECT "productid", "price", "category", "productname" FROM "product"'
) AS src("ProductId" INT, "Price" DECIMAL, "Category" VARCHAR, "ProductName" VARCHAR);
