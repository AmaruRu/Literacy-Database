#!/usr/bin/env python3
"""
Update existing books with cover URLs from Excel file
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from project import create_website, db
from project.models import Books


def update_book_covers():
    """Update existing books with cover URLs from Excel file"""
    print("Starting book cover update...")
    
    try:
        # Load Excel data
        df = pd.read_excel('./data/book_reco/Book_Recs.xls')
        print(f"Loaded {len(df)} books from Excel file")
        
        # Create Flask app context
        app = create_website()
        
        with app.app_context():
            books_updated = 0
            books_not_found = 0
            
            for index, row in df.iterrows():
                try:
                    title = str(row['Title']).strip() if pd.notna(row['Title']) else None
                    author = str(row['Author']).strip() if pd.notna(row['Author']) else None
                    grade_level = str(row['Grade Level']).strip() if pd.notna(row['Grade Level']) else None
                    cover_url = str(row['Cover']).strip() if pd.notna(row['Cover']) else None
                    
                    if not title or not author or not grade_level:
                        continue
                    
                    # Find existing book in database
                    existing_book = Books.query.filter_by(
                        title=title,
                        author=author,
                        grade_level=grade_level
                    ).first()
                    
                    if existing_book:
                        # Update cover URL
                        existing_book.cover_url = cover_url
                        books_updated += 1
                        
                        if books_updated % 50 == 0:
                            db.session.commit()
                            print(f"Updated {books_updated} books so far...")
                    else:
                        books_not_found += 1
                        print(f"Book not found in database: {title} by {author} (Grade: {grade_level})")
                
                except Exception as e:
                    print(f"Error processing book at row {index + 1}: {e}")
                    continue
            
            # Final commit
            db.session.commit()
            
            print(f"\n=== Book Cover Update Summary ===")
            print(f"Books updated with cover URLs: {books_updated}")
            print(f"Books not found in database: {books_not_found}")
            
            # Show sample of updated books
            print(f"\n=== Sample of Updated Books ===")
            sample_books = Books.query.filter(Books.cover_url.isnot(None)).limit(5).all()
            for book in sample_books:
                cover_preview = book.cover_url[:50] + "..." if book.cover_url and len(book.cover_url) > 50 else book.cover_url
                print(f"- {book.title} by {book.author}: {cover_preview}")
            
            print(f"\nBook cover update completed successfully!")
            
    except Exception as e:
        print(f"Error during book cover update: {e}")
        raise


if __name__ == "__main__":
    update_book_covers()