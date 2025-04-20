--Deleting quotes(הצעות מחיר) by selected month
--#1
DELETE FROM Quotation
WHERE EXTRACT(MONTH FROM expiration_date) = 5
  AND EXTRACT(YEAR FROM expiration_date) = 2024;




-- Deleting products that have never been ordered (according to the ProductOrder table)
--#2
DELETE FROM Product
WHERE product_id NOT IN (
    SELECT DISTINCT product_id FROM ProductOrder
);




--Deleting Quotation that were not ordered (there is no order that matched the Quotation)
--#3
DELETE FROM Quotation
WHERE order_id IS NULL;
