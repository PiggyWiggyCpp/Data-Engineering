CREATE OR REPLACE FUNCTION adjust_book_price()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF (SELECT SUM(quantity) FROM Sales WHERE book_id = NEW.book_id) >= 5 THEN
        UPDATE Books
        SET price = price * 1.10
        WHERE book_id = NEW.book_id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER tr_adjust_book_price
AFTER INSERT ON Sales
FOR EACH ROW
EXECUTE FUNCTION adjust_book_price();



INSERT INTO Books (title, author_id, published_date, genre_id, price)
VALUES ('Test Book', 1, '2024-01-01', 1, 20.00);

INSERT INTO Sales (book_id, customer_id, quantity, sale_date)
VALUES ((SELECT book_id FROM Books WHERE title = 'Test Book' AND author_id=1), 1, 5, '2024-02-01');

SELECT price FROM Books WHERE title = 'Test Book';
