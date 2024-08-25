CREATE TABLE Sales_Archive AS TABLE Sales WITH NO DATA;

CREATE OR REPLACE PROCEDURE archive_old_sales(archive_before_date DATE)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Sales_Archive (sale_id, book_id, customer_id, quantity, sale_date)
    SELECT sale_id, book_id, customer_id, quantity, sale_date
    FROM Sales
    WHERE sale_date < archive_before_date;

    DELETE FROM Sales
    WHERE sale_date < archive_before_date;
END;
$$;






INSERT INTO Sales (book_id, customer_id, quantity, sale_date)
VALUES (1, 1, 1, '2023-01-01'),
       (1, 1, 1, '2022-01-01'),
       (1, 1, 1, '2021-01-01');

	   
CALL archive_old_sales('2023-01-01');


SELECT * FROM Sales_Archive;
SELECT * FROM Sales WHERE sale_date < '2023-01-01';