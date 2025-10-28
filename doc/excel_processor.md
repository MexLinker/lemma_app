# Excel Processor Technical Documentation

## Overview
The Excel Processor component handles the processing of Excel files containing word lists and integrates EPUB search results. It manages data extraction, search result integration, and output generation.

## Module: process_excel.py

### Function: get_epub_files
```python
def get_epub_files()
```
- **Returns**:
  - list[str] - List of EPUB file paths
- **Functionality**:
  - Scans data/epub directory for EPUB files
  - Returns absolute paths to EPUB files
  - Filters for .epub extension

### Function: process_excel_file
```python
def process_excel_file(excel_path)
```
- **Parameters**:
  - `excel_path`: str - Path to input Excel file
- **Functionality**:
  - Reads Excel file using pandas
  - Initializes EPUBReader with available books
  - Creates columns for each book
  - Processes words from Lemma column
  - Handles NaN values
  - Saves results to new Excel file

## Data Flow

### Input Processing
1. Excel File Reading
   - Uses pandas.read_excel
   - Loads entire file into DataFrame
   - Preserves original column structure

### EPUB Integration
1. Book Discovery
   - Scans for EPUB files
   - Creates EPUBReader instance
   - Prepares search infrastructure

2. Column Creation
   - Adds column for each EPUB book
   - Initializes with 'NoWord' default value
   - Maintains original data integrity

### Word Processing
1. Word Extraction
   - Reads from 'Lemma' column
   - Converts to string format
   - Handles NaN values safely

2. Search Integration
   - Searches each word across books
   - Captures first occurrence context
   - Updates DataFrame with results

### Output Generation
1. File Creation
   - Generates 'processed_' prefixed filename
   - Preserves original columns
   - Adds book-specific result columns

## Data Structures

### Input Excel Structure
```python
DataFrame(
    'Lemma': str,          # Word to search
    'Wordlist': str,        # Source list info
    'Summary': str,         # Word summary
    # ... other original columns
)
```

### Output Excel Structure
```python
DataFrame(
    # Original columns preserved
    'book1.epub': str,      # Search results for book1
    'book2.epub': str,      # Search results for book2
    # ... one column per book
)
```

## Dependencies
- pandas: Excel file handling
- EPUBReader: Book content searching
- os: File path management

## Error Handling
1. Data Validation
   - NaN value detection and skipping
   - String conversion safety
   - File existence checking

2. Search Result Management
   - None result handling
   - Default 'NoWord' values
   - Progress tracking

## Performance Optimization
1. Memory Management
   - Single DataFrame instance
   - In-place updates
   - Efficient string handling

2. Processing Efficiency
   - Batch file operations
   - Progress reporting
   - Early exit conditions

## Usage Example
```python
# Process an Excel file
excel_file = 'enWords_learn_with_freq_win_Oct28.xlsx'
process_excel_file(excel_file)
```

## Progress Tracking
1. Word Processing
   - Current word index
   - Total word count
   - Processing status

2. Output Generation
   - File creation status
   - Save confirmation

## Limitations
- Memory usage scales with Excel size
- Single-threaded processing
- Limited to text-based search
- Fixed output format