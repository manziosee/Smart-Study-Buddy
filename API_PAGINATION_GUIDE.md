# API Pagination and Filtering Guide

## Overview
The Smart Study Buddy API now includes comprehensive pagination, filtering, and sorting capabilities for better performance and user experience.

## Pagination

### Default Settings
- **Page Size**: 20 items per page
- **Max Page Size**: 100 items per page
- **Pagination Style**: Page number based

### Usage Examples
```bash
# Get first page (default)
GET /api/notes/

# Get specific page
GET /api/notes/?page=2

# Custom page size
GET /api/notes/?page_size=50

# Maximum allowed page size
GET /api/notes/?page_size=100
```

### Response Format
```json
{
  "links": {
    "next": "http://localhost:8000/api/notes/?page=3",
    "previous": "http://localhost:8000/api/notes/?page=1"
  },
  "count": 150,
  "total_pages": 8,
  "current_page": 2,
  "page_size": 20,
  "results": [...]
}
```

## Filtering

### Notes Filtering
```bash
# Filter by title (case-insensitive)
GET /api/notes/?title=python

# Filter by date range
GET /api/notes/?created_after=2024-01-01&created_before=2024-12-31

# Filter notes with summaries
GET /api/notes/?has_summary=true

# Filter notes with uploaded files
GET /api/notes/?has_file=true

# Combine filters
GET /api/notes/?title=django&has_summary=true&created_after=2024-01-01
```

### Quiz Filtering
```bash
# Filter by quiz title
GET /api/quizzes/?title=python

# Filter by note title
GET /api/quizzes/?note_title=django

# Filter by minimum questions
GET /api/quizzes/?min_questions=5

# Filter by date range
GET /api/quizzes/?created_after=2024-01-01
```

### Quiz Attempts Filtering
```bash
# Filter by quiz title
GET /api/quiz/attempts/?quiz_title=python

# Filter by score range
GET /api/quiz/attempts/?min_score=8&max_score=10

# Filter by percentage
GET /api/quiz/attempts/?min_percentage=80

# Filter by attempt date
GET /api/quiz/attempts/?attempted_after=2024-01-01
```

## Search

### Full-Text Search
```bash
# Search notes by title, content, or summary
GET /api/notes/?search=machine learning

# Search quizzes by title or note title
GET /api/quizzes/?search=python basics
```

## Sorting

### Available Sort Fields

#### Notes
- `created_at` (default: newest first)
- `updated_at`
- `title`

#### Quizzes
- `created_at` (default: newest first)
- `title`

#### Quiz Attempts
- `created_at` (default: newest first)
- `score`
- `quiz__title`

### Usage Examples
```bash
# Sort by title (ascending)
GET /api/notes/?ordering=title

# Sort by title (descending)
GET /api/notes/?ordering=-title

# Sort by creation date (oldest first)
GET /api/notes/?ordering=created_at

# Sort by creation date (newest first - default)
GET /api/notes/?ordering=-created_at

# Multiple sort fields
GET /api/notes/?ordering=-created_at,title
```

## Combined Usage

### Complex Query Example
```bash
GET /api/notes/?search=python&has_summary=true&created_after=2024-01-01&ordering=-created_at&page=2&page_size=10
```

This query:
- Searches for "python" in title, content, or summary
- Only includes notes with summaries
- Created after January 1, 2024
- Sorted by creation date (newest first)
- Returns page 2 with 10 items per page

## Performance Benefits

### Database Optimization
- **Indexed Fields**: All filter and sort fields are properly indexed
- **Query Optimization**: Efficient database queries with minimal N+1 problems
- **Pagination**: Reduces memory usage and improves response times

### Frontend Benefits
- **Faster Loading**: Smaller response payloads
- **Better UX**: Progressive loading and infinite scroll support
- **Search**: Real-time search with debouncing

## API Endpoints with Pagination

### Notes
- `GET /api/notes/` - List notes with pagination, filtering, and search
- `GET /api/notes/?page=2&search=python&ordering=-created_at`

### Quizzes
- `GET /api/quizzes/` - List quizzes with pagination and filtering
- `GET /api/quizzes/?note_title=django&min_questions=5`

### Quiz Attempts
- `GET /api/quiz/attempts/` - List attempts with pagination and filtering
- `GET /api/quiz/attempts/?min_percentage=80&ordering=-score`

## Error Handling

### Invalid Page
```json
{
  "detail": "Invalid page."
}
```

### Invalid Page Size
```json
{
  "detail": "Page size must be between 1 and 100."
}
```

### Invalid Filter Values
```json
{
  "detail": "Invalid filter value for 'created_after'. Expected date format: YYYY-MM-DD."
}
```

## Frontend Integration

### JavaScript Example
```javascript
// Fetch paginated notes
async function fetchNotes(page = 1, search = '', filters = {}) {
  const params = new URLSearchParams({
    page: page,
    search: search,
    ...filters
  });
  
  const response = await fetch(`/api/notes/?${params}`);
  const data = await response.json();
  
  return {
    notes: data.results,
    totalPages: data.total_pages,
    currentPage: data.current_page,
    hasNext: !!data.links.next,
    hasPrevious: !!data.links.previous
  };
}

// Usage
const result = await fetchNotes(1, 'python', { 
  has_summary: true, 
  ordering: '-created_at' 
});
```

### React Hook Example
```javascript
import { useState, useEffect } from 'react';

function useNotes(filters = {}) {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({});
  
  useEffect(() => {
    const fetchNotes = async () => {
      setLoading(true);
      const params = new URLSearchParams(filters);
      const response = await fetch(`/api/notes/?${params}`);
      const data = await response.json();
      
      setNotes(data.results);
      setPagination({
        totalPages: data.total_pages,
        currentPage: data.current_page,
        hasNext: !!data.links.next,
        hasPrevious: !!data.links.previous
      });
      setLoading(false);
    };
    
    fetchNotes();
  }, [filters]);
  
  return { notes, loading, pagination };
}
```

## Best Practices

### Performance
1. **Use appropriate page sizes** - Don't request more data than needed
2. **Implement caching** - Cache frequently accessed pages
3. **Use search debouncing** - Avoid excessive API calls during typing

### User Experience
1. **Show loading states** - Indicate when data is being fetched
2. **Implement infinite scroll** - For better mobile experience
3. **Preserve filter state** - Maintain filters across navigation

### API Usage
1. **Combine filters efficiently** - Use multiple filters in single request
2. **Sort consistently** - Always specify ordering for predictable results
3. **Handle errors gracefully** - Provide fallbacks for failed requests