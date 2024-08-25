SELECT 
    title,
    genre_id,
    price,
    RANK() OVER (PARTITION BY genre_id ORDER BY price DESC) AS price_rank
FROM 
    Books;
