CREATE OR REPLACE FUNCTION check_positive_price()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price < 0 THEN
        RAISE EXCEPTION 'Price cannot be negative. Given: %', NEW.price;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_price
BEFORE INSERT OR UPDATE ON product
FOR EACH ROW
EXECUTE FUNCTION check_positive_price();

--בדיקה על הכנסת ועדכון מחירים שליליים-- מציג שגיאה
INSERT INTO product (product_id, product_name, price, amount)
VALUES (999, 'Test Product', -10, 5);

UPDATE product
SET price = -5
WHERE product_id =1;




