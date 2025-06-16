-- הפונקציה מחזירה את כל ההנחות שתקפות היום בחנות ספציפית.
CREATE OR REPLACE FUNCTION get_active_discounts_by_store(p_storeid INT)
RETURNS TABLE (
    discountid INT,
    discountrate NUMERIC,
    startdate DATE,
    enddate DATE,
    storeid INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT d.discountid, d.discountrate, d.startdate, d.enddate, d.storeid
    FROM discount d
    WHERE d.storeid = p_storeid
      AND CURRENT_DATE BETWEEN d.startdate AND d.enddate;
END;
$$;



SELECT * FROM get_active_discounts_by_store(1);
