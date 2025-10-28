# EPUB Word Search and Database Project

This project provides a comprehensive solution for searching words in EPUB files, processing the results with Excel, and storing the data in a MySQL database. It includes functionality for finding the first occurrence of words in multiple EPUB books, recording the context in which they appear, and managing this data through a structured database system.

## Project Structure

```
.
├── data/
│   ├── epub/        # EPUB book files
│   └── excel/       # Excel files for word processing
├── src/
│   ├── epub/        # EPUB processing modules
│   │   └── epub_reader.py
│   ├── excel/       # Excel processing modules
│   │   └── process_excel.py
│   └── db/          # Database operations modules
│       ├── excel_to_mysql.py
│       └── verify_mysql.py
├── tests/           # Test files (to be implemented)
├── requirements.txt # Project dependencies
└── .gitignore      # Git ignore rules
```

## Features

- **EPUB Processing**: Searches for words in multiple EPUB files simultaneously
- **First Occurrence**: Finds and extracts the first occurrence of each word in each book
- **Excel Integration**: Processes word lists from Excel and records search results
- **Database Storage**: Stores processed data in MySQL with date-stamped tables
- **Error Handling**: Implements retry mechanisms for network issues
- **Duplicate Prevention**: Uses INSERT IGNORE to prevent duplicate entries

## Requirements

- Python 3.8+
- MySQL Server
- Required Python packages (see requirements.txt)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd execute_EPUB
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place your EPUB files in the `data/epub/` directory
5. Place your Excel files in the `data/excel/` directory

## Usage

### EPUB Word Search

```bash
# Run the EPUB reader for interactive word search
python src/epub/epub_reader.py
```

### Excel Processing

```bash
# Process Excel file with EPUB search results
python src/excel/process_excel.py
```

### Database Operations

```bash
# Import Excel data to MySQL
python src/db/excel_to_mysql.py

# Verify imported data
python src/db/verify_mysql.py
```

## Data Flow

1. EPUB files are loaded and processed by `epub_reader.py`
2. Word list from Excel is processed by `process_excel.py`
3. Search results are saved back to Excel
4. Processed Excel data is imported to MySQL by `excel_to_mysql.py`
5. Data verification is performed by `verify_mysql.py`

## Error Handling

- Network connectivity issues are handled with retry mechanisms
- File not found errors are caught and reported
- Database connection errors are handled gracefully
- NaN values in Excel are properly managed

## Database Schema

The MySQL database (`word_search`) contains tables named with the format `word_search_YYYYMMDD`, where:
- Each table has an auto-incrementing ID
- Columns match Excel file structure
- All text fields use VARCHAR(1000) to accommodate long sentences
- INSERT IGNORE prevents duplicate entries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.