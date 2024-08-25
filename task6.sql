CREATE OR REPLACE FUNCTION avg_price_by_genre(id_genre INTEGER)
RETURNS NUMERIC(10, 2)
LANGUAGE plpgsql
AS $$
DECLARE
    avg_price NUMERIC(10, 2);
BEGIN
    SELECT AVG(price) INTO avg_price
    FROM Books
    WHERE genre_id = id_genre;

    RETURN avg_price;
END;
$$;

SELECT avg_price_by_genre(5);