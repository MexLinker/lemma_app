# Database Operations Technical Documentation

## Overview
The Database Operations component manages MySQL database interactions, including connection handling, table creation, data insertion, and verification. It implements robust error handling and retry mechanisms for network issues.

## Module: excel_to_mysql.py

### Function: create_connection
```python
def create_connection()
```
- **Returns**:
  - mysql.connector.connection or None
- **Functionality**:
  - Establishes MySQL connection
  - Uses configured credentials
  - Handles connection errors

### Function: create_database_and_table
```python
def create_database_and_table(connection)
```
- **Parameters**:
  - `connection`: mysql.connector.connection
- **Returns**:
  - str or None - Created table name
- **Functionality**:
  - Creates word_search database
  - Generates date-based table name
  - Maps Excel columns to SQL
  - Creates table structure

### Function: insert_data
```python
def insert_data(connection, table_name)
```
- **Parameters**:
  - `connection`: mysql.connector.connection
  - `table_name`: str - Target table name
- **Functionality**:
  - Reads processed Excel data
  - Implements retry mechanism
  - Handles batch insertions
  - Tracks progress

## Module: verify_mysql.py

### Function: verify_data
```python
def verify_data()
```
- **Functionality**:
  - Connects to database
  - Counts total rows
  - Retrieves sample data
  - Displays verification results

## Database Schema

### Table Structure
```sql
CREATE TABLE word_search_YYYYMMDD (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Lemma VARCHAR(1000),
    Wordlist VARCHAR(1000),
    Summary VARCHAR(1000),
    -- Dynamic columns for each book
    book1_results VARCHAR(1000),
    book2_results VARCHAR(1000),
    -- Additional columns as needed
)
```

## Connection Configuration
```python
connection_params = {
    'host': '121.4.251.254',
    'port': 5034,
    'user': 'root',
    'password': 'root'
}
```

## Error Handling

### Connection Errors
1. Initial Connection
   - Timeout handling
   - Authentication errors
   - Server unavailability

2. Query Execution
   - Transaction management
   - Deadlock resolution
   - Connection loss recovery

### Data Validation
1. Input Validation
   - NULL handling
   - String length limits
   - Character encoding

2. Constraint Checking
   - Primary key violations
   - Foreign key constraints
   - Unique index conflicts

## Retry Mechanism

### Configuration
```python
retry_config = {
    'max_retries': 3,
    'delay_seconds': 2,
    'exponential_backoff': True
}
```

### Implementation
1. Retry Conditions
   - Network timeouts
   - Deadlock detection
   - Connection loss

2. Backoff Strategy
   - Initial delay
   - Exponential increase
   - Maximum retry limit

## Performance Optimization

### Batch Processing
1. Insert Batching
   - Configurable batch size
   - Transaction management
   - Progress tracking

2. Connection Pooling
   - Connection reuse
   - Pool size management
   - Timeout configuration

### Query Optimization
1. Index Usage
   - Primary key optimization
   - Column indexing
   - Query planning

2. Memory Management
   - Buffer allocation
   - Result set handling
   - Resource cleanup

## Data Verification

### Verification Process
1. Row Count Validation
   - Total record count
   - Batch completion
   - Data integrity

2. Data Sampling
   - Random sampling
   - Pattern matching
   - Value distribution

## Usage Examples

### Data Import
```python
# Import data to MySQL
connection = create_connection()
if connection:
    table_name = create_database_and_table(connection)
    if table_name:
        insert_data(connection, table_name)
```

### Data Verification
```python
# Verify imported data
verify_data()
```

## Limitations
- Single server configuration
- Sequential processing
- Fixed retry strategy
- Memory constraints

## Security Considerations
- Credential management
- SQL injection prevention
- Connection encryption
- Access control