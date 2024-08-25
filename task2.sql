WITH The_Books AS (
    SELECT 
        book_id,
        title,
        author_id,
        genre_id,
        published_date
    FROM 
        Books
    WHERE 
        title ~* '\ythe\y'
)


SELECT 
    tb.title,
    a.name AS author_name,
    g.genre_name,
    tb.published_date
FROM 
    The_Books tb
JOIN 
    Authors a ON tb.author_id = a.author_id
JOIN 
    Genres g ON tb.genre_id = g.genre_id;
