WITH Book_Counts AS (
    SELECT 
        author_id,
        COUNT(*) AS total_books
    FROM 
        Books
    GROUP BY 
        author_id
)


SELECT 
    a.name AS author_name,
    bc.total_books
FROM 
    Book_Counts bc
JOIN 
    Authors a ON bc.author_id = a.author_id
WHERE 
    bc.total_books > 3;
