/**
 * Mississippi Literacy Database - Books Page JavaScript
 * Handles book filtering, display, and API interactions
 */

// API endpoint
const BOOKS_API_BASE = '/api/books';

// Pagination settings
const BOOKS_PER_PAGE = 20;

// State management
let allBooksCache = null;
let currentPage = 1;
let totalPages = 1;
let currentSort = 'title-asc'; // Default sort

/**
 * Initialize the books page when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeBooksPage();
});

/**
 * Initialize all page functionality
 */
async function initializeBooksPage() {
    // Set up event listeners
    setupEventListeners();

    // Load all books on initial page load
    await loadBooks();
}

/**
 * Set up event listeners for filter controls
 */
function setupEventListeners() {
    // Apply filters button
    const applyBtn = document.querySelector('.btn-apply');
    if (applyBtn) {
        applyBtn.addEventListener('click', applyFilters);
    }

    // Clear filters button
    const clearBtn = document.querySelector('.btn-clear');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearFilters);
    }

    // Book spine grade selectors
    const bookSpines = document.querySelectorAll('.book-spine');
    bookSpines.forEach(spine => {
        spine.addEventListener('click', function() {
            toggleGradeSegment(this);
        });
    });

    // Literature select - auto-apply on change
    const literatureSelect = document.getElementById('literature-select');
    if (literatureSelect) {
        literatureSelect.addEventListener('change', function() {
            // Optional: Auto-apply filters on change
            // applyFilters();
        });
    }

    // Lexile inputs - allow Enter key to apply filters
    const lexileMin = document.getElementById('lexile-min');
    const lexileMax = document.getElementById('lexile-max');

    if (lexileMin) {
        lexileMin.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyFilters();
            }
        });
    }

    if (lexileMax) {
        lexileMax.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyFilters();
            }
        });
    }
}

/**
 * Toggle grade segment selection
 * @param {HTMLElement} segment - The clicked segment element
 */
function toggleGradeSegment(segment) {
    segment.classList.toggle('selected');
    updateSelectedGradesDisplay();
}

/**
 * Update the selected grades display text
 */
function updateSelectedGradesDisplay() {
    const selectedSpines = document.querySelectorAll('.book-spine.selected');
    const selectedGradesText = document.getElementById('selected-grades-text');

    if (!selectedGradesText) return;

    if (selectedSpines.length === 0) {
        selectedGradesText.textContent = 'All Grades';
    } else {
        // Sort by grade position (low to high) and display grade names
        const sortedGrades = Array.from(selectedSpines)
            .sort((a, b) => {
                return parseInt(a.getAttribute('data-position')) - parseInt(b.getAttribute('data-position'));
            })
            .map(spine => {
                const grade = spine.getAttribute('data-grade');
                // Simplify grade names for display
                if (grade === 'Kindergarten') return 'Kindergarten';
                return grade.replace(' Grade', '').replace('st', '').replace('nd', '').replace('rd', '').replace('th', '');
            });

        selectedGradesText.textContent = sortedGrades.join(', ');
    }
}

/**
 * Clear grade selection
 */
function clearGradeSelection() {
    const selectedSpines = document.querySelectorAll('.book-spine.selected');
    selectedSpines.forEach(spine => {
        spine.classList.remove('selected');
    });
    updateSelectedGradesDisplay();
}

/**
 * Get selected grade levels from book stack selector
 * @returns {Array|null} Array of selected grade levels or null if all/none selected
 */
function getSelectedGrades() {
    const selectedSpines = document.querySelectorAll('.book-spine.selected');

    if (selectedSpines.length === 0) {
        return null; // No selection means all grades
    }

    const grades = Array.from(selectedSpines).map(spine => {
        return spine.getAttribute('data-grade');
    });

    return grades;
}

/**
 * Get current filter values
 * @returns {Object} Filter configuration object
 */
function getFilterValues() {
    return {
        grades: getSelectedGrades(),
        literatureType: document.getElementById('literature-select')?.value || '',
        lexileMin: document.getElementById('lexile-min')?.value || '',
        lexileMax: document.getElementById('lexile-max')?.value || ''
    };
}

/**
 * Apply current filters and reload books
 */
function applyFilters() {
    currentPage = 1; // Reset to page 1 when filters change
    loadBooks();
}

/**
 * Clear all filters and reload all books
 */
function clearFilters() {
    // Clear grade clock selection
    clearGradeSelection();

    // Clear literature type
    const literatureSelect = document.getElementById('literature-select');
    if (literatureSelect) {
        literatureSelect.value = '';
    }

    // Clear lexile inputs
    const lexileMin = document.getElementById('lexile-min');
    const lexileMax = document.getElementById('lexile-max');
    if (lexileMin) lexileMin.value = '';
    if (lexileMax) lexileMax.value = '';

    // Reset to page 1
    currentPage = 1;

    // Reload all books
    loadBooks();
}

/**
 * Load books from API with current filters
 */
async function loadBooks() {
    const container = document.getElementById('books-container');
    const resultsInfo = document.getElementById('results-info');

    if (!container) {
        console.error('Books container not found');
        return;
    }

    // Show loading state
    showLoading(container, resultsInfo);

    try {
        // Get filter values
        const filters = getFilterValues();

        // Fetch books with filters
        const books = await fetchBooksWithFilters(filters);

        // Remove duplicates and combine characteristics
        const uniqueBooks = removeDuplicates(books);

        // Sort books
        const sortedBooks = sortBooks(uniqueBooks, currentSort);

        // Cache all books
        allBooksCache = sortedBooks;

        // Calculate pagination
        totalPages = Math.ceil(allBooksCache.length / BOOKS_PER_PAGE);

        // Display results
        if (allBooksCache.length === 0) {
            showNoResults(container, resultsInfo);
        } else {
            displayBooksPage(container, resultsInfo);
        }

    } catch (error) {
        console.error('Error loading books:', error);
        showError(container, resultsInfo, 'Error loading books. Please try again later.');
    }
}

/**
 * Fetch books from API with given filters
 * @param {Object} filters - Filter configuration
 * @returns {Promise<Array>} Array of book objects
 */
async function fetchBooksWithFilters(filters) {
    let allBooks = [];

    // If multiple grades selected, fetch for each grade
    if (filters.grades && filters.grades.length > 0) {
        for (const grade of filters.grades) {
            const params = buildQueryParams({
                grade_level: grade,
                literature_type: filters.literatureType,
                lexile_min: filters.lexileMin,
                lexile_max: filters.lexileMax,
                limit: 500
            });

            const response = await fetch(`${BOOKS_API_BASE}?${params}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success && data.data) {
                allBooks = allBooks.concat(data.data);
            }
        }
    } else {
        // No grade filter, fetch all books with other filters
        const params = buildQueryParams({
            literature_type: filters.literatureType,
            lexile_min: filters.lexileMin,
            lexile_max: filters.lexileMax,
            limit: 500
        });

        const response = await fetch(`${BOOKS_API_BASE}?${params}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success && data.data) {
            allBooks = data.data;
        }
    }

    return allBooks;
}

/**
 * Build URL query parameters from filter object
 * @param {Object} params - Parameters to encode
 * @returns {URLSearchParams} Encoded parameters
 */
function buildQueryParams(params) {
    const searchParams = new URLSearchParams();

    for (const [key, value] of Object.entries(params)) {
        if (value !== null && value !== undefined && value !== '') {
            searchParams.append(key, value);
        }
    }

    return searchParams;
}

/**
 * Remove duplicate books and combine their unique characteristics
 * @param {Array} books - Array of book objects
 * @returns {Array} Array of unique books with combined characteristics
 */
function removeDuplicates(books) {
    const bookMap = new Map();

    books.forEach(book => {
        const key = `${book.title}|||${book.author}`;

        if (bookMap.has(key)) {
            // Book already exists, merge characteristics
            const existing = bookMap.get(key);

            // Combine grade levels (create array if not already)
            if (!Array.isArray(existing.grade_levels)) {
                existing.grade_levels = [existing.grade_level];
            }
            if (!existing.grade_levels.includes(book.grade_level)) {
                existing.grade_levels.push(book.grade_level);
            }

            // Keep the same lexile and literature type (should be the same for same book)
        } else {
            // New book, add to map
            const newBook = { ...book };
            newBook.grade_levels = [book.grade_level];
            bookMap.set(key, newBook);
        }
    });

    return Array.from(bookMap.values());
}

/**
 * Sort books based on sort criteria
 * @param {Array} books - Array of book objects
 * @param {string} sortBy - Sort criteria (e.g., 'title-asc', 'author-desc')
 * @returns {Array} Sorted array of books
 */
function sortBooks(books, sortBy) {
    const sorted = [...books]; // Create copy to avoid mutating original

    const [field, order] = sortBy.split('-');

    sorted.sort((a, b) => {
        let compareA, compareB;

        switch (field) {
            case 'title':
                compareA = a.title.toLowerCase();
                compareB = b.title.toLowerCase();
                break;

            case 'author':
                // Sort by last name
                compareA = getLastName(a.author).toLowerCase();
                compareB = getLastName(b.author).toLowerCase();
                break;

            case 'grade':
                // Convert grade to numeric for sorting
                compareA = gradeToNumber(a.grade_level);
                compareB = gradeToNumber(b.grade_level);
                break;

            case 'lexile':
                // Convert lexile to numeric (BR = -1)
                compareA = lexileToNumber(a.lexile);
                compareB = lexileToNumber(b.lexile);
                break;

            case 'type':
                compareA = a.literature_type.toLowerCase();
                compareB = b.literature_type.toLowerCase();
                break;

            default:
                return 0;
        }

        // Compare values
        let result;
        if (compareA < compareB) {
            result = -1;
        } else if (compareA > compareB) {
            result = 1;
        } else {
            result = 0;
        }

        // Apply order (ascending or descending)
        return order === 'desc' ? -result : result;
    });

    return sorted;
}

/**
 * Extract last name from author name
 * @param {string} authorName - Full author name
 * @returns {string} Last name
 */
function getLastName(authorName) {
    const parts = authorName.trim().split(' ');
    return parts[parts.length - 1];
}

/**
 * Convert grade level to number for sorting
 * @param {string} grade - Grade level (e.g., "Kindergarten", "5th Grade")
 * @returns {number} Numeric representation
 */
function gradeToNumber(grade) {
    const gradeMap = {
        'Kindergarten': 0,
        '1st Grade': 1,
        '2nd Grade': 2,
        '3rd Grade': 3,
        '4th Grade': 4,
        '5th Grade': 5,
        '6th Grade': 6,
        '7th Grade': 7,
        '8th Grade': 8,
        '9th Grade': 9,
        '10th Grade': 10,
        '11th Grade': 11,
        '12th Grade': 12
    };
    return gradeMap[grade] ?? 99;
}

/**
 * Convert lexile to number for sorting
 * @param {string} lexile - Lexile level (e.g., "600", "BR")
 * @returns {number} Numeric representation
 */
function lexileToNumber(lexile) {
    if (lexile === 'BR' || lexile === 'br') {
        return -1; // Beginning Reader comes before numeric levels
    }
    const num = parseInt(lexile);
    return isNaN(num) ? 0 : num;
}

/**
 * Apply sorting to current cached books and redisplay
 * @param {string} sortBy - Sort criteria
 */
function applySorting(sortBy) {
    if (!allBooksCache || allBooksCache.length === 0) {
        return;
    }

    currentSort = sortBy;
    currentPage = 1; // Reset to first page when sorting

    // Re-sort the cached books
    allBooksCache = sortBooks(allBooksCache, currentSort);

    // Re-display
    const container = document.getElementById('books-container');
    const resultsInfo = document.getElementById('results-info');

    if (container && resultsInfo) {
        displayBooksPage(container, resultsInfo);
    }
}

/**
 * Display current page of books
 * @param {HTMLElement} container - Container element
 * @param {HTMLElement} resultsInfo - Results info element
 */
function displayBooksPage(container, resultsInfo) {
    if (!allBooksCache || allBooksCache.length === 0) {
        showNoResults(container, resultsInfo);
        return;
    }

    // Calculate start and end indices for current page
    const startIndex = (currentPage - 1) * BOOKS_PER_PAGE;
    const endIndex = Math.min(startIndex + BOOKS_PER_PAGE, allBooksCache.length);

    // Get books for current page
    const booksToDisplay = allBooksCache.slice(startIndex, endIndex);

    // Update results counter
    if (resultsInfo) {
        resultsInfo.innerHTML = `Showing ${startIndex + 1}-${endIndex} of ${allBooksCache.length} book${allBooksCache.length !== 1 ? 's' : ''}`;
    }

    // Generate book cards HTML
    const booksHTML = booksToDisplay.map(book => createBookCard(book)).join('');

    // Update container
    container.innerHTML = booksHTML;

    // Render pagination controls
    renderPagination();
}

/**
 * Create HTML for a single book card
 * @param {Object} book - Book object from API
 * @returns {string} HTML string for book card
 */
function createBookCard(book) {
    const literatureClass = book.literature_type === 'Fiction' ? 'badge-fiction' : 'badge-nonfiction';

    // Handle multiple grade levels
    let gradeBadges = '';
    if (book.grade_levels && book.grade_levels.length > 1) {
        // Sort grade levels
        const sortedGrades = book.grade_levels.sort((a, b) => gradeToNumber(a) - gradeToNumber(b));
        gradeBadges = sortedGrades.map(grade =>
            `<span class="book-badge badge-grade">${escapeHtml(grade)}</span>`
        ).join('');
    } else {
        gradeBadges = `<span class="book-badge badge-grade">${escapeHtml(book.grade_level)}</span>`;
    }

    // Book cover image
    const coverImage = book.cover_url && book.cover_url.trim() !== ''
        ? `<img src="${escapeHtml(book.cover_url)}" alt="${escapeHtml(book.title)} cover" class="book-cover" loading="lazy" onerror="this.style.display='none'">`
        : '';

    return `
        <div class="book-card">
            ${coverImage}
            <div class="book-info">
                <div class="book-title">${escapeHtml(book.title)}</div>
                <div class="book-author">by ${escapeHtml(book.author)}</div>
                <div class="book-meta">
                    ${gradeBadges}
                    <span class="book-badge badge-lexile">Lexile: ${escapeHtml(book.lexile)}</span>
                    <span class="book-badge ${literatureClass}">
                        ${escapeHtml(book.literature_type)}
                    </span>
                </div>
            </div>
        </div>
    `;
}

/**
 * Show loading state
 * @param {HTMLElement} container - Books container
 * @param {HTMLElement} resultsInfo - Results info element
 */
function showLoading(container, resultsInfo) {
    if (container) {
        container.innerHTML = '<div class="loading">Loading books...</div>';
    }
    if (resultsInfo) {
        resultsInfo.innerHTML = '';
    }
}

/**
 * Show no results message
 * @param {HTMLElement} container - Books container
 * @param {HTMLElement} resultsInfo - Results info element
 */
function showNoResults(container, resultsInfo) {
    if (container) {
        container.innerHTML = `
            <div class="error">
                No books found matching your criteria. Try adjusting your filters.
            </div>
        `;
    }
    if (resultsInfo) {
        resultsInfo.innerHTML = '';
    }
}

/**
 * Show error message
 * @param {HTMLElement} container - Books container
 * @param {HTMLElement} resultsInfo - Results info element
 * @param {string} message - Error message to display
 */
function showError(container, resultsInfo, message) {
    if (container) {
        container.innerHTML = `<div class="error">${escapeHtml(message)}</div>`;
    }
    if (resultsInfo) {
        resultsInfo.innerHTML = '';
    }
}

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} Escaped HTML
 */
function escapeHtml(text) {
    if (text === null || text === undefined) {
        return '';
    }

    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

/**
 * Render pagination controls
 */
function renderPagination() {
    const paginationContainer = document.getElementById('pagination-container');
    if (!paginationContainer) return;

    // Hide if only one page
    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }

    let paginationHTML = `
        <div class="pagination-controls">
            <button class="pagination-btn" onclick="goToPage(1)" ${currentPage === 1 ? 'disabled' : ''}>
                &laquo; First
            </button>
            <button class="pagination-btn" onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
                &lsaquo; Prev
            </button>

            <div class="page-numbers">
                ${generatePageNumbers()}
            </div>

            <button class="pagination-btn" onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
                Next &rsaquo;
            </button>
            <button class="pagination-btn" onclick="goToPage(${totalPages})" ${currentPage === totalPages ? 'disabled' : ''}>
                Last &raquo;
            </button>
        </div>
        <div class="pagination-info">
            Page ${currentPage} of ${totalPages}
        </div>
    `;

    paginationContainer.innerHTML = paginationHTML;
}

/**
 * Generate page number buttons
 * @returns {string} HTML for page numbers
 */
function generatePageNumbers() {
    const pages = [];
    const maxVisible = 7; // Maximum page numbers to show

    if (totalPages <= maxVisible) {
        // Show all pages
        for (let i = 1; i <= totalPages; i++) {
            pages.push(createPageButton(i));
        }
    } else {
        // Always show first page
        pages.push(createPageButton(1));

        if (currentPage > 3) {
            pages.push('<span class="page-ellipsis">...</span>');
        }

        // Show pages around current page
        const start = Math.max(2, currentPage - 1);
        const end = Math.min(totalPages - 1, currentPage + 1);

        for (let i = start; i <= end; i++) {
            pages.push(createPageButton(i));
        }

        if (currentPage < totalPages - 2) {
            pages.push('<span class="page-ellipsis">...</span>');
        }

        // Always show last page
        pages.push(createPageButton(totalPages));
    }

    return pages.join('');
}

/**
 * Create a page number button
 * @param {number} pageNum - Page number
 * @returns {string} HTML for page button
 */
function createPageButton(pageNum) {
    const isActive = pageNum === currentPage;
    return `<button class="page-number ${isActive ? 'active' : ''}" onclick="goToPage(${pageNum})" ${isActive ? 'disabled' : ''}>${pageNum}</button>`;
}

/**
 * Navigate to specific page
 * @param {number} pageNum - Page number to navigate to
 */
function goToPage(pageNum) {
    if (pageNum < 1 || pageNum > totalPages || pageNum === currentPage) {
        return;
    }

    currentPage = pageNum;

    // Re-display books for new page
    const container = document.getElementById('books-container');
    const resultsInfo = document.getElementById('results-info');

    if (container && resultsInfo) {
        displayBooksPage(container, resultsInfo);
    }

    // Scroll to top of books section
    const booksSection = document.getElementById('books-section');
    if (booksSection) {
        booksSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Make functions globally accessible for HTML onclick handlers
window.goToPage = goToPage;
window.clearGradeSelection = clearGradeSelection;
window.applySorting = applySorting;
window.applyFilters = applyFilters;
window.clearFilters = clearFilters;

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getSelectedGrades,
        getFilterValues,
        escapeHtml,
        buildQueryParams,
        createBookCard,
        clearGradeSelection,
        toggleGradeSegment,
        updateSelectedGradesDisplay
    };
}
