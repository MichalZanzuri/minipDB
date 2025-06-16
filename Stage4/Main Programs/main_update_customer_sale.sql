-- פונקציה שמחזירה מכירות לפי לקוח
CREATE OR REPLACE FUNCTION get_sales_by_customer(p_customer_id INT)
RETURNS TABLE (saleid INT, saledate DATE, totalprice NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT s.saleid, s.saledate, s.totalprice
    FROM sale s
    WHERE s.customerid = p_customer_id;
END;
$$ LANGUAGE plpgsql;

-- פרוצדורה שמעדכנת סכום מכירה
CREATE OR REPLACE PROCEDURE update_sale_totalprice(p_sale_id INT, p_new_total NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE sale
    SET totalprice = p_new_total
    WHERE saleid = p_sale_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Sale with ID % not found', p_sale_id;
    END IF;
END;
$$;

-- תוכנית ראשית שמשתמשת בפונקציה ובפרוצדורה
DO $$
DECLARE
    v_customer_id INT := 1;
    v_sale_id INT := 342;
    v_new_total NUMERIC := 999.99;
    r RECORD;
BEGIN
    RAISE NOTICE 'מכירות לפני עדכון ללקוח %:', v_customer_id;

    FOR r IN SELECT * FROM get_sales_by_customer(v_customer_id)
    LOOP
        RAISE NOTICE 'מכירה: ID=% | תאריך=% | סכום=%', r.saleid, r.saledate, r.totalprice;
    END LOOP;

    CALL update_sale_totalprice(v_sale_id, v_new_total);

    RAISE NOTICE 'מכירות לאחר עדכון ללקוח %:', v_customer_id;

    FOR r IN SELECT * FROM get_sales_by_customer(v_customer_id)
    LOOP
        RAISE NOTICE 'מכירה: ID=% | תאריך=% | סכום=%', r.saleid, r.saledate, r.totalprice;
    END LOOP;
END $$;
