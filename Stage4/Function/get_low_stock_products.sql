--פונקציה זו מחזירה את רשימת המוצרים שהכמות שלהם (amount) -נמוכה מminamount .
-- הפונקציה משתמשת ב־cursor כדי לאפשר גישה שיטתית לטבלה זו.
CREATE OR REPLACE FUNCTION get_low_stock_products()
RETURNS refcursor AS $$
DECLARE
    cur refcursor := 'my_cursor';
BEGIN
    OPEN cur FOR
        SELECT product_id, product_name, amount, minamount
        FROM product
        WHERE amount < minamount;

    RETURN cur;
END;
$$ LANGUAGE plpgsql;



BEGIN;

-- שלב ראשון – קבלת שם ה־cursor
SELECT get_low_stock_products();

-- שלב שני – שליפת כל המידע מה-cursor
FETCH ALL FROM my_cursor;

-- סיום הטרנזקציה
COMMIT;

--עצירת תהליך
--ROLLBACK;

