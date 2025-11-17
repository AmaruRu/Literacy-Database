# Books Page Documentation

## Overview

The Books page provides an interactive interface for users to discover book recommendations based on grade level, Lexile reading level, and literature type. The page displays all 259 books from the database and allows dynamic filtering.

## Features

### 📚 Book Display
- **Grid Layout**: Books are displayed in a responsive card grid
- **Book Cards**: Each card shows:
  - Title
  - Author
  - Grade Level (badge)
  - Lexile Level (badge)
  - Literature Type (Fiction/Nonfiction badge)

### 🔍 Filtering Options

#### 1. Grade Level Filter
- **Type**: Multi-select dropdown
- **Options**: Kindergarten through 12th Grade
- **Functionality**:
  - Select one or multiple grades (hold Ctrl/Cmd)
  - "All Grades" option to show all books
  - Can combine with other filters

#### 2. Literature Type Filter
- **Type**: Single-select dropdown
- **Options**:
  - All Types
  - Fiction
  - Nonfiction
- **Functionality**: Filter books by genre

#### 3. Lexile Range Filter
- **Type**: Two numeric inputs (min and max)
- **Range**: 0-2000
- **Functionality**:
  - Set minimum Lexile level
  - Set maximum Lexile level
  - Leave blank to include all levels (including "BR" Beginning Reader)
  - Use one or both fields

### 🎯 User Actions

#### Apply Filters Button
- **Color**: Green
- **Action**: Fetches and displays books matching selected criteria
- **Result**: Updates the book grid with filtered results

#### Clear Filters Button
- **Color**: Red
- **Action**: Resets all filters to default
- **Result**: Shows all 259 books

## Technical Implementation

### Frontend (books.html)

**HTML Structure:**
```html
- Filters Container
  - Grade Level (multi-select)
  - Literature Type (select)
  - Lexile Range (number inputs)
  - Action Buttons (Apply/Clear)
- Results Info (count display)
- Books Grid (dynamic card layout)
```

**JavaScript Functions:**
- `loadBooks()` - Fetches books from API with applied filters
- `applyFilters()` - Triggers book loading with current filters
- `clearFilters()` - Resets all filter inputs
- `displayBooks()` - Renders book cards in the grid
- `getSelectedGrades()` - Returns array of selected grade levels

**API Integration:**
- Endpoint: `/api/books`
- Method: GET
- Parameters:
  - `grade_level` (string)
  - `literature_type` (string)
  - `lexile_min` (number)
  - `lexile_max` (number)
  - `limit` (number, default 500)

### Styling

**Responsive Design:**
- Desktop: 4-5 cards per row
- Tablet: 2-3 cards per row
- Mobile: 1-2 cards per row

**Color Scheme:**
- Fiction Badge: Blue (#e3f2fd)
- Nonfiction Badge: Orange (#fff3e0)
- Grade Badge: Purple (#f3e5f5)
- Lexile Badge: Green (#e8f5e9)

**Interactive Effects:**
- Card hover: Lifts up with shadow
- Button hover: Darker shade

## Usage Examples

### Example 1: Find Kindergarten Books
1. Select "Kindergarten" from Grade Level dropdown
2. Click "Apply Filters"
3. Result: 19 Kindergarten books displayed

### Example 2: Find 5th-7th Grade Fiction
1. Select "5th Grade", "6th Grade", and "7th Grade" (hold Ctrl)
2. Select "Fiction" from Literature Type
3. Click "Apply Filters"
4. Result: All fiction books for grades 5-7

### Example 3: Find Books with Lexile 600-800
1. Enter "600" in Lexile Min
2. Enter "800" in Lexile Max
3. Click "Apply Filters"
4. Result: Books with Lexile levels between 600-800

### Example 4: View All Books
1. Keep all filters at default or click "Clear Filters"
2. Result: All 259 books displayed

## Data Source

- **Database**: `literacy_db`
- **Table**: `Books`
- **Total Books**: 259
- **Grade Distribution**:
  - Kindergarten: 19 books
  - 1st-12th Grade: 20 books each
- **Literature Types**:
  - Fiction: 255 books (98.5%)
  - Nonfiction: 4 books (1.5%)

## User Experience Features

### Loading States
- Shows "Loading books..." while fetching data
- Prevents multiple simultaneous requests

### Error Handling
- Displays error message if API fails
- Shows "No books found" message when filters return no results

### Results Counter
- Displays total number of books shown
- Updates dynamically with filters
- Format: "Showing X book(s)"

### Accessibility
- Semantic HTML structure
- Clear labels for all inputs
- Keyboard navigation support
- Screen reader friendly

## Future Enhancements (Optional)

1. **Search Functionality**: Add text search for title/author
2. **Sorting Options**: Sort by title, author, or Lexile level
3. **Book Covers**: Display cover images when available
4. **Pagination**: Add pagination for large result sets
5. **Favorites**: Allow users to save favorite books
6. **Export**: Export book list to PDF or CSV
7. **Reading Level Calculator**: Help users find their Lexile level
8. **Book Details Modal**: Show more information on click

## Testing

To verify the page works correctly:

```bash
# Start the Flask server
cd /home/amaru/MS_Literacy_Database/MS_Lit
python3 website.py

# Open in browser
http://127.0.0.1:5001/books.html
```

Test scenarios:
1. ✓ Page loads all books on initial load
2. ✓ Grade filter shows correct books
3. ✓ Literature type filter works
4. ✓ Lexile range filter works
5. ✓ Multiple filters work together
6. ✓ Clear filters resets to all books
7. ✓ Results counter updates correctly
8. ✓ Cards display all book information
