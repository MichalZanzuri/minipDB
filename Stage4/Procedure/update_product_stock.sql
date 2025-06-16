CREATE OR REPLACE PROCEDURE update_product_stock(p_product_id INT, p_amount INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE product
    SET amount = amount + p_amount
    WHERE product_id = p_product_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Product with ID % not found', p_product_id;
    END IF;
END;
$$;


CALL update_product_stock(101, 5);
--בדיקה שהמלאי התעדכן
SELECT product_id, amount FROM product WHERE product_id = 101;

