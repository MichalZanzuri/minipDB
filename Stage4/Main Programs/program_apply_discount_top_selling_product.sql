--פונקציה למציאת המוצר הכי נמכר
CREATE OR REPLACE FUNCTION get_top_selling_product()
RETURNS TABLE (product_id INT, total_quantity_sold BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT sp.product_id, SUM(sp.quantity) AS total_quantity_sold
    FROM saleproduct sp
    GROUP BY sp.product_id
    ORDER BY total_quantity_sold DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- פרוצדורה להוספת הנחה למוצר
CREATE OR REPLACE PROCEDURE add_discount_to_product(
    p_product_id INT,
    p_discount_rate NUMERIC,
    p_start DATE,
    p_end DATE,
    p_store_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO discount (discountrate, startdate, enddate, storeid, productid)
    VALUES (p_discount_rate, p_start, p_end, p_store_id, p_product_id);
END;
$$;


--main program
DO $$
DECLARE
    v_product_id INT;
    v_total_quantity INT;
    v_store_id INT := 1;  -- מזהה חנות לבחירתך
    r RECORD;
BEGIN
    -- שלב 1: מציאת המוצר הכי נמכר
    SELECT product_id, total_quantity_sold
    INTO v_product_id, v_total_quantity
    FROM get_top_selling_product();

    RAISE NOTICE 'המוצר הכי נמכר הוא % עם כמות %', v_product_id, v_total_quantity;

    -- שלב 2: הוספת הנחה של 15% לחנות 1, לשבוע מהיום
    CALL add_discount_to_product(
        p_product_id := v_product_id,
        p_discount_rate := 0.15,
        p_start := CURRENT_DATE,
        p_end := (CURRENT_DATE + INTERVAL '7 days')::DATE,  -- המרה ל-date
        p_store_id := v_store_id
    );

    RAISE NOTICE 'הנחה של 15%% נוספה למוצר %', v_product_id;

    -- שלב 3: הצגת ההנחות של המוצר הזה
    RAISE NOTICE 'רשימת ההנחות למוצר %:', v_product_id;

    FOR r IN
        SELECT discountrate, startdate, enddate, storeid
        FROM discount
        WHERE productid = v_product_id
        ORDER BY startdate DESC
    LOOP
        RAISE NOTICE 'הנחה: % | תאריכים: % עד % | חנות: %',
            r.discountrate, r.startdate, r.enddate, r.storeid;
    END LOOP;
END;
$$;


--בדיקה
--SELECT * FROM discount
--ORDER BY discountid DESC
--LIMIT 5;

