# EPUB Reader Technical Documentation

## Overview
The EPUB Reader component is responsible for loading, parsing, and searching through EPUB files. It provides functionality to find the first occurrence of specified words within multiple EPUB books simultaneously.

## Class: EPUBReader

### Constructor
```python
def __init__(self, epub_paths)
```
- **Parameters**:
  - `epub_paths`: str or list[str] - Path(s) to EPUB file(s)
- **Functionality**:
  - Initializes book storage dictionary
  - Loads EPUB files using ebooklib
  - Creates content mapping for each book
  - Processes each book's content for searching

### Method: process_book
```python
def process_book(self, book_name)
```
- **Parameters**:
  - `book_name`: str - Name of the book to process
- **Functionality**:
  - Extracts text content from EPUB documents
  - Creates section-based content mapping
  - Stores section titles and text content
  - Maintains section numbering

### Method: get_section_title
```python
def get_section_title(self, soup)
```
- **Parameters**:
  - `soup`: BeautifulSoup - Parsed HTML content
- **Returns**:
  - str - Section title or 'Untitled Section'
- **Functionality**:
  - Extracts titles from HTML headings (h1-h6)
  - Provides fallback for untitled sections

### Method: search_word
```python
def search_word(self, word)
```
- **Parameters**:
  - `word`: str - Word to search for
- **Returns**:
  - list[dict] or None - Search results
- **Functionality**:
  - Performs case-insensitive word search
  - Finds first occurrence in each book
  - Extracts surrounding sentence context
  - Returns structured search results

## Data Structures

### Book Storage Dictionary
```python
self.books = {
    'book_name': {
        'book': epub.Book,
        'content_map': {
            section_number: {
                'text': str,
                'title': str,
                'item': epub.Item
            }
        },
        'current_section': int
    }
}
```

### Search Result Dictionary
```python
{
    'book_name': str,
    'section': int,
    'section_title': str,
    'sentence': str,
    'position': int
}
```

## Dependencies
- ebooklib: EPUB file parsing
- BeautifulSoup4: HTML content parsing
- os: File path handling

## Error Handling
- Handles missing EPUB files
- Manages empty or invalid sections
- Provides fallback for missing section titles
- Returns None for unsuccessful searches

## Performance Considerations
- Content is processed and stored at initialization
- Search operations use in-memory content maps
- Early exit on first word occurrence per book
- Case-insensitive search optimization

## Usage Example
```python
# Initialize with multiple EPUB files
reader = EPUBReader(['book1.epub', 'book2.epub'])

# Search for a word
results = reader.search_word('example')

# Process results
if results:
    for result in results:
        print(f"Found in {result['book_name']}: {result['sentence']}")
```

## Limitations
- Memory usage scales with EPUB file size
- Only finds first occurrence per book
- Limited to text content (no image processing)
- Case-insensitive search only