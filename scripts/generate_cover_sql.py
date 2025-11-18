#!/usr/bin/env python3
"""
Generate SQL script to update book covers from Excel file
"""

import pandas as pd


def generate_cover_update_sql():
    """Generate SQL UPDATE statements for all books"""
    
    print("Generating SQL script to update book covers...")
    
    try:
        # Load Excel data
        df = pd.read_excel('./data/book_reco/Book_Recs.xls')
        print(f"Loaded {len(df)} books from Excel file")
        
        # Create SQL file
        with open('update_all_covers.sql', 'w') as sql_file:
            sql_file.write("-- SQL Script to Update All Book Cover URLs\n")
            sql_file.write("-- Generated from Book_Recs.xls\n\n")
            sql_file.write("USE MS_DBMS;\n\n")
            
            sql_file.write("-- Check current book count\n")
            sql_file.write("SELECT COUNT(*) as total_books FROM books;\n\n")
            
            sql_file.write("-- Update book cover URLs\n")
            
            books_processed = 0
            
            for index, row in df.iterrows():
                try:
                    title = str(row['Title']).strip().replace("'", "\\'") if pd.notna(row['Title']) else None
                    author = str(row['Author']).strip().replace("'", "\\'") if pd.notna(row['Author']) else None
                    grade_level = str(row['Grade Level']).strip().replace("'", "\\'") if pd.notna(row['Grade Level']) else None
                    cover_url = str(row['Cover']).strip().replace("'", "\\'") if pd.notna(row['Cover']) else None
                    
                    if not title or not author or not grade_level or not cover_url:
                        continue
                    
                    # Generate UPDATE statement
                    sql_statement = f"""UPDATE books SET cover_url = '{cover_url}' 
WHERE title = '{title}' AND author = '{author}' AND grade_level = '{grade_level}';\n"""
                    
                    sql_file.write(sql_statement)
                    books_processed += 1
                    
                except Exception as e:
                    print(f"Error processing book at row {index + 1}: {e}")
                    continue
            
            sql_file.write("\n-- Check results\n")
            sql_file.write("SELECT \n")
            sql_file.write("    COUNT(*) as total_books,\n")
            sql_file.write("    COUNT(cover_url) as books_with_covers,\n")
            sql_file.write("    ROUND((COUNT(cover_url) / COUNT(*)) * 100, 2) as percentage_with_covers\n")
            sql_file.write("FROM books;\n\n")
            
            sql_file.write("-- Sample books with covers\n")
            sql_file.write("SELECT title, author, grade_level, LEFT(cover_url, 50) as cover_preview \n")
            sql_file.write("FROM books WHERE cover_url IS NOT NULL LIMIT 10;\n")
        
        print(f"\n✅ Generated SQL script: update_all_covers.sql")
        print(f"📊 Processed {books_processed} books with cover URLs")
        print(f"\nTo use this script:")
        print(f"1. Connect to your MySQL database")
        print(f"2. Run: source update_all_covers.sql")
        print(f"3. Or copy/paste the SQL commands")
            
    except Exception as e:
        print(f"❌ Error generating SQL script: {e}")


if __name__ == "__main__":
    generate_cover_update_sql()