# Books API Documentation

The Books API provides endpoints for retrieving book recommendations based on grade level, Lexile range, and literature type. This is used for the book recommendation tab of the website.

## Database

- **Database**: `literacy_db`
- **Table**: `Books`
- **Total Books**: 259 books (K-12)

## Data Structure

Each book contains:
- `Book_ID` - Unique identifier
- `Title` - Book title
- `Author` - Author name
- `Grade_Level` - Target grade (Kindergarten, 1st Grade, ..., 12th Grade)
- `Lexile` - Lexile reading level (numeric or "BR" for Beginning Reader)
- `Literature_Type` - Fiction or Nonfiction
- `Cover_URL` - URL to book cover image (optional)

## API Endpoints

### 1. Get Books with Filters
```
GET /api/books
```

**Query Parameters:**
- `grade_level` (string) - Filter by grade level (e.g., "Kindergarten", "5th Grade")
- `literature_type` (string) - Filter by type ("Fiction" or "Nonfiction")
- `lexile_min` (string) - Minimum Lexile level (numeric)
- `lexile_max` (string) - Maximum Lexile level (numeric)
- `author` (string) - Filter by author name (partial match)
- `search` (string) - Search in title or author
- `limit` (integer) - Number of results (default: 50)
- `offset` (integer) - Pagination offset (default: 0)

**Example Requests:**
```bash
# Get all 5th grade fiction books
GET /api/books?grade_level=5th%20Grade&literature_type=Fiction

# Get books with Lexile between 600-800
GET /api/books?lexile_min=600&lexile_max=800

# Search for books by Dr. Seuss
GET /api/books?author=Seuss

# Get Kindergarten books
GET /api/books?grade_level=Kindergarten&limit=20
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "book_id": 1,
      "title": "Biscuit Goes to School",
      "author": "Alyssa Satin Capucilli",
      "grade_level": "Kindergarten",
      "lexile": "160",
      "literature_type": "Fiction",
      "cover_url": ""
    }
  ],
  "count": 1,
  "total": 259,
  "filters_applied": {
    "grade_level": "Kindergarten",
    "literature_type": null,
    "lexile_min": null,
    "lexile_max": null,
    "author": null,
    "search": null,
    "limit": 50,
    "offset": 0
  }
}
```

### 2. Get Book Details
```
GET /api/books/<book_id>
```

**Example:**
```bash
GET /api/books/1
```

**Response:**
```json
{
  "success": true,
  "data": {
    "book_id": 1,
    "title": "Biscuit Goes to School",
    "author": "Alyssa Satin Capucilli",
    "grade_level": "Kindergarten",
    "lexile": "160",
    "literature_type": "Fiction",
    "cover_url": "",
    "created_at": "2025-11-16T00:00:00"
  }
}
```

### 3. Get Available Grade Levels
```
GET /api/books/grade-levels
```

Returns all grade levels with book counts.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "grade_level": "Kindergarten",
      "book_count": 19
    },
    {
      "grade_level": "1st Grade",
      "book_count": 20
    }
  ],
  "count": 13
}
```

### 4. Get Authors
```
GET /api/books/authors
```

**Query Parameters:**
- `limit` (integer) - Number of authors to return (default: 50)

Returns authors ordered by book count.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "author": "Alyssa Satin Capucilli",
      "book_count": 11
    },
    {
      "author": "Mo Willems",
      "book_count": 6
    }
  ],
  "count": 50
}
```

## Book Distribution

- **Kindergarten**: 19 books
- **1st-12th Grade**: 20 books each
- **Fiction**: 255 books (98.5%)
- **Nonfiction**: 4 books (1.5%)

## Data Import

To re-import or update book data:

```bash
cd MS_Lit
python3 dev/import_books.py
```

The script will:
1. Read data from `/home/amaru/MS_Literacy_Database/Book_Rec.xls`
2. Clean and deduplicate records
3. Create the Books table if it doesn't exist
4. Import all books into the selected database

## Notes

- Lexile values include numeric levels (160, 210, etc.) and "BR" (Beginning Reader)
- The "BR" Lexile level is for early readers before reaching numeric levels
- Grade levels range from Kindergarten through 12th Grade
- All books have Title, Author, Grade Level, and Literature Type
- Cover URLs may be empty and can be populated later
