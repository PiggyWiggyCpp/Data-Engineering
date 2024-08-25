CREATE OR REPLACE FUNCTION top_n_books_by_genre(id_genre INTEGER, top_n INTEGER)
RETURNS TABLE(book_id INTEGER, title VARCHAR, total_sales NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT b.book_id, b.title, SUM(s.quantity * b.price) AS total_sales
    FROM Books b
    JOIN Sales s ON b.book_id = s.book_id
    WHERE b.genre_id = id_genre
    GROUP BY b.book_id, b.title
    ORDER BY total_sales DESC
    LIMIT top_n;
END;
$$;


SELECT * FROM top_n_books_by_genre(2, 10);