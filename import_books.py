#!/usr/bin/env python3
"""
Import book recommendations from Excel file to database
"""

import pandas as pd
import numpy as np
from project import create_website, db
from project.models import Books


def clean_lexile_value(lexile):
    """Clean and standardize lexile values"""
    if pd.isna(lexile) or lexile == '' or lexile == 'N/A':
        return None
    
    # Convert to string and clean
    lexile_str = str(lexile).strip()
    
    # Handle 'BR' (Beginning Reader) case
    if lexile_str.upper() == 'BR':
        return 'BR'
    
    # Try to convert to integer for numeric lexile values
    try:
        return str(int(float(lexile_str)))
    except (ValueError, TypeError):
        # If conversion fails, return as-is
        return lexile_str


def clean_string_value(value):
    """Clean string values"""
    if pd.isna(value) or value == '' or value == 'N/A':
        return None
    return str(value).strip()


def import_books():
    """Import books from Excel file into the database"""
    print("Starting book import from Excel file...")
    
    try:
        # Load Excel data
        df = pd.read_excel('book_reco/Book_Recs.xls')
        print(f"Loaded {len(df)} books from Excel file")
        
        # Create Flask app context
        app = create_website()
        
        with app.app_context():
            # Create books table if it doesn't exist
            print("Creating Books table...")
            db.create_all()
            
            # Clear existing book data (optional - remove this line if you want to keep existing data)
            print("Clearing existing book data...")
            Books.query.delete()
            db.session.commit()
            
            # Import books
            print("Importing books...")
            books_imported = 0
            books_skipped = 0
            
            for index, row in df.iterrows():
                try:
                    # Clean and validate data
                    title = clean_string_value(row['Title'])
                    author = clean_string_value(row['Author'])
                    grade_level = clean_string_value(row['Grade Level'])
                    lexile = clean_lexile_value(row['Lexile'])
                    literature_type = clean_string_value(row['Literature Type'])
                    cover_url = clean_string_value(row['Cover'])
                    
                    # Skip if essential data is missing
                    if not title or not author or not grade_level:
                        print(f"Skipping book at row {index + 1}: missing essential data")
                        books_skipped += 1
                        continue
                    
                    # Check for duplicate (same title and author)
                    existing_book = Books.query.filter_by(
                        title=title,
                        author=author,
                        grade_level=grade_level
                    ).first()
                    
                    if existing_book:
                        print(f"Skipping duplicate book: {title} by {author} (Grade: {grade_level})")
                        books_skipped += 1
                        continue
                    
                    # Create new book record
                    book = Books(
                        title=title,
                        author=author,
                        grade_level=grade_level,
                        lexile=lexile,
                        literature_type=literature_type,
                        cover_url=cover_url
                    )
                    
                    db.session.add(book)
                    books_imported += 1
                    
                    # Commit every 50 records to avoid large transactions
                    if books_imported % 50 == 0:
                        db.session.commit()
                        print(f"Imported {books_imported} books so far...")
                
                except Exception as e:
                    print(f"Error processing book at row {index + 1}: {e}")
                    books_skipped += 1
                    continue
            
            # Final commit
            db.session.commit()
            
            # Print import summary
            print(f"\n=== Book Import Summary ===")
            print(f"Books successfully imported: {books_imported}")
            print(f"Books skipped: {books_skipped}")
            print(f"Total books in database: {Books.query.count()}")
            
            # Show sample of imported books
            print(f"\n=== Sample of Imported Books ===")
            sample_books = Books.query.limit(5).all()
            for book in sample_books:
                print(f"- {book.title} by {book.author} (Grade: {book.grade_level}, Lexile: {book.lexile})")
            
            # Show grade level distribution
            print(f"\n=== Books by Grade Level ===")
            grade_counts = db.session.query(
                Books.grade_level,
                db.func.count(Books.book_id).label('count')
            ).group_by(Books.grade_level).all()
            
            for grade, count in grade_counts:
                print(f"{grade}: {count} books")
            
            print(f"\nBook import completed successfully!")
            
    except Exception as e:
        print(f"Error during book import: {e}")
        raise


if __name__ == "__main__":
    import_books()