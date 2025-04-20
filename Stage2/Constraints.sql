-- CHECK constraint in the Product table - the price must be positive
ALTER TABLE Product
ADD CONSTRAINT check_positive_price
CHECK (price > 0);

--DEFAULT constraint in the Order_d table - default status for an order is 'Pending'
ALTER TABLE Order_d
ALTER COLUMN status SET DEFAULT 'Pending';

-- NOT NULL constraint in the Supplier table - the company name cannot be empty
ALTER TABLE Supplier
ALTER COLUMN company_name SET NOT NULL;
