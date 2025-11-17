"""
Import book recommendations from Book_Rec.xls into the Books table
"""

import sys
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add parent directory to path to import from project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_db_connection(use_books_db=False):
    """Create database connection from environment variables"""
    db_user = os.getenv('MYSQL_USER', 'root')
    db_password = os.getenv('MYSQL_PASSWORD', '')
    db_host = os.getenv('MYSQL_HOST', 'localhost')
    db_port = os.getenv('MYSQL_PORT', '3306')

    # Choose between literacy_db and books_db
    if use_books_db:
        db_name = os.getenv('MYSQL_DB2', 'books_db')
    else:
        db_name = os.getenv('MYSQL_DB', 'literacy_db')

    connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    return create_engine(connection_string)

def create_books_table(engine):
    """Create Books table if it doesn't exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS Books (
      Book_ID INT AUTO_INCREMENT PRIMARY KEY,
      Title VARCHAR(500) NOT NULL,
      Author VARCHAR(255) NOT NULL,
      Grade_Level VARCHAR(50) NOT NULL,
      Lexile VARCHAR(20),
      Literature_Type ENUM('Fiction', 'Nonfiction') NOT NULL,
      Cover_URL VARCHAR(1000),
      Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      INDEX idx_grade_level (Grade_Level),
      INDEX idx_lexile (Lexile),
      INDEX idx_literature_type (Literature_Type),
      INDEX idx_author (Author)
    )
    """

    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()
        print("✓ Books table created/verified")

def import_books():
    """Import books from Book_Rec.xls file"""

    # Path to the Excel file
    excel_path = '/home/amaru/MS_Literacy_Database/MS_Lit/Book_Recs.xls'

    print(f"Reading book data from {excel_path}...")

    # Read the Excel file
    df = pd.read_excel(excel_path)

    print(f"Found {len(df)} books to import")
    print(f"Columns: {list(df.columns)}")

    # Clean the data
    # Rename columns to match database schema
    df = df.rename(columns={
        'Grade Level': 'Grade_Level',
        'Literature Type': 'Literature_Type',
        'Cover': 'Cover_URL'
    })

    # Convert Lexile to string to handle values like 'BR' (Beginning Reader)
    df['Lexile'] = df['Lexile'].astype(str)

    # Handle NaN values in Cover_URL
    df['Cover_URL'] = df['Cover_URL'].fillna('')

    # Keep only the columns we need
    df_clean = df[['Title', 'Author', 'Grade_Level', 'Lexile', 'Literature_Type', 'Cover_URL']]

    # Remove duplicates (same title, author, and grade level)
    df_clean = df_clean.drop_duplicates(subset=['Title', 'Author', 'Grade_Level'], keep='first')

    print(f"After cleaning: {len(df_clean)} unique books")

    # Ask which database to use
    print("\nWhich database should we import books into?")
    print("1. literacy_db (main database)")
    print("2. books_db (separate books database)")
    choice = input("Enter choice (1 or 2, default=1): ").strip() or "1"

    use_books_db = (choice == "2")
    db_name = "books_db" if use_books_db else "literacy_db"

    print(f"\nUsing database: {db_name}")

    # Create database connection
    engine = get_db_connection(use_books_db=use_books_db)

    try:
        # Create database if it doesn't exist (for books_db)
        if use_books_db:
            # Connect without database to create it
            admin_engine = create_engine(
                f'mysql+pymysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST", "localhost")}:{os.getenv("MYSQL_PORT", "3306")}'
            )
            with admin_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
                conn.commit()
                print(f"✓ Database {db_name} created/verified")
            admin_engine.dispose()

        # Create Books table
        create_books_table(engine)

        # Clear existing data
        with engine.connect() as conn:
            print("Clearing existing book data...")
            conn.execute(text("DELETE FROM Books"))
            conn.commit()

        # Import data
        print("Importing book data...")
        df_clean.to_sql('Books', engine, if_exists='append', index=False, method='multi', chunksize=50)

        # Verify import
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) as count FROM Books"))
            count = result.fetchone()[0]
            print(f"Successfully imported {count} books")

            # Show sample of imported data
            result = conn.execute(text("""
                SELECT Grade_Level, COUNT(*) as book_count
                FROM Books
                GROUP BY Grade_Level
                ORDER BY
                    CASE Grade_Level
                        WHEN 'Kindergarten' THEN 0
                        WHEN '1st Grade' THEN 1
                        WHEN '2nd Grade' THEN 2
                        WHEN '3rd Grade' THEN 3
                        WHEN '4th Grade' THEN 4
                        WHEN '5th Grade' THEN 5
                        WHEN '6th Grade' THEN 6
                        WHEN '7th Grade' THEN 7
                        WHEN '8th Grade' THEN 8
                        WHEN '9th Grade' THEN 9
                        WHEN '10th Grade' THEN 10
                        WHEN '11th Grade' THEN 11
                        WHEN '12th Grade' THEN 12
                        ELSE 99
                    END
            """))

            print("\nBooks per grade level:")
            for row in result:
                print(f"  {row[0]}: {row[1]} books")

            # Show literature type distribution
            result = conn.execute(text("""
                SELECT Literature_Type, COUNT(*) as book_count
                FROM Books
                GROUP BY Literature_Type
            """))

            print("\nBooks by literature type:")
            for row in result:
                print(f"  {row[0]}: {row[1]} books")

        print("\n✓ Book import completed successfully!")

    except Exception as e:
        print(f"ERROR during import: {e}")
        raise

    finally:
        engine.dispose()

if __name__ == '__main__':
    import_books()
