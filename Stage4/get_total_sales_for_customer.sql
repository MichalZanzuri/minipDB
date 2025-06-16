--הפונקציה מקבלת מזהה של לקוח (CustomerId), ומחזירה את סכום כל המכירות שביצע.
--אם הלקוח לא קיים או לא ביצע מכירות – הפונקציה מחזירה 0.
--הפונקציה כוללת טיפול בשגיאות (EXCEPTION) כדי למנוע קריסה במקרה של מזהה לא תקף.
CREATE OR REPLACE FUNCTION get_total_sales_for_customer(p_customer_id INT)
RETURNS NUMERIC AS $$
DECLARE
    total_sales NUMERIC := 0;
BEGIN
    SELECT COALESCE(SUM(totalprice), 0)
    INTO total_sales
    FROM Sale
    WHERE customerid = p_customer_id;

    RETURN total_sales;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'שגיאה בחישוב המכירות עבור לקוח %', p_customer_id;
        RETURN 0;
END;
$$ LANGUAGE plpgsql;



--לקוח עם id=1
SELECT get_total_sales_for_customer(1);
