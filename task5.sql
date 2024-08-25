CREATE OR REPLACE PROCEDURE update_customer_join_date()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Customers c
    SET join_date = (
        SELECT MIN(s.sale_date)
        FROM Sales s
        WHERE s.customer_id = c.customer_id
    )
    WHERE EXISTS (
        SELECT 1
        FROM Sales s
        WHERE s.customer_id = c.customer_id
        AND s.sale_date < c.join_date
    );
END;
$$;


INSERT INTO Customers (first_name, last_name, email, join_date)
VALUES 
('Alice', 'Smith', 'alice@google.com', '2024-01-01'),
('Bob', 'Karlson', 'bob@google.com', '2024-01-15');

INSERT INTO Sales (book_id, customer_id, quantity, sale_date)
VALUES
(1, 1, 2, '2023-12-01'),
(1, 2, 1, '2024-02-01');


CALL update_customer_join_date();

SELECT 
    first_name, 
    last_name, 
    email, 
    join_date
FROM 
    Customers;
