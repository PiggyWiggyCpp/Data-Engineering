CREATE OR REPLACE PROCEDURE update_book_prices_by_genre(
    id_genre INTEGER,
    percentage_change NUMERIC(5, 2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_updated_count INTEGER;
BEGIN
    UPDATE Books
    SET price = price + (price * percentage_change / 100)
    WHERE genre_id = id_genre;

    GET DIAGNOSTICS v_updated_count = ROW_COUNT;

    RAISE NOTICE 'Updated % books in genre %', v_updated_count, id_genre;
END;
$$;


CALL update_book_prices_by_genre(3, 5.00);


SELECT 
    title, 
    g.genre_name,
    b.price
FROM 
    Books b
JOIN 
    Genres g ON b.genre_id = g.genre_id
WHERE 
    g.genre_id = 3;
