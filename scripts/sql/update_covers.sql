-- SQL Script to Update Book Cover URLs
-- Run this script in your MySQL database to add cover URLs to existing books

-- First, let's see the current book count
SELECT COUNT(*) as total_books FROM books;

-- Sample update queries - you'll need to run these for all 259 books
-- Based on the Excel file data, here are some example updates:

UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81aeV2igJsL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit Goes to School' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';

UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61gYTpPyCDL._AC_UF1000,1000_QL80_.jpg'
WHERE title = 'Biscuit Finds a Friend' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';

UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91iqwEk-7kL._AC_UF1000,1000_QL80_.jpg'
WHERE title = "Biscuit's Day at the Farm" AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';

-- Check if updates worked
SELECT title, author, grade_level, cover_url FROM books WHERE cover_url IS NOT NULL LIMIT 5;

-- To update all books at once, you would need to:
-- 1. Export the Excel file to CSV
-- 2. Create a temporary table with the cover URLs
-- 3. Run an UPDATE JOIN statement

-- Example for bulk update (adjust table/column names as needed):
/*
CREATE TEMPORARY TABLE temp_covers (
    title VARCHAR(500),
    author VARCHAR(255), 
    grade_level VARCHAR(50),
    cover_url VARCHAR(1000)
);

-- Load data from CSV into temp table
LOAD DATA INFILE 'path/to/book_covers.csv' 
INTO TABLE temp_covers 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Update books table with cover URLs
UPDATE books b
JOIN temp_covers t ON b.title = t.title AND b.author = t.author AND b.grade_level = t.grade_level
SET b.cover_url = t.cover_url;

-- Drop temporary table
DROP TEMPORARY TABLE temp_covers;
*/

-- Check final results
SELECT 
    COUNT(*) as total_books,
    COUNT(cover_url) as books_with_covers,
    (COUNT(cover_url) / COUNT(*)) * 100 as percentage_with_covers
FROM books;