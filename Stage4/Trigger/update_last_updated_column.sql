--היא מעדכנת את העמודה last_updated לשעה הנוכחית (now()
CREATE OR REPLACE FUNCTION update_last_updated_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--הטריגר מוגדר לפעול לפני כל עדכון (BEFORE UPDATE) בטבלת product.
--הוא מפעיל את הפונקציה לכל שורה שמתעדכנת (FOR EACH ROW)
CREATE TRIGGER trg_update_last_updated
BEFORE UPDATE ON product
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_column();

--עדכון השדה
UPDATE product
SET amount = amount + 1
WHERE product_id = 101;


SELECT product_id, last_updated FROM product WHERE product_id = 101;

--שינוי אזורר זמן 
SET timezone = 'Asia/Jerusalem';


