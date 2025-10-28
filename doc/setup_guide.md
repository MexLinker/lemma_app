# Setup and Configuration Guide

## Environment Setup

### Python Environment
1. **Python Version**
   ```bash
   # Verify Python installation
   python --version  # Should be 3.8+
   ```

2. **Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Dependencies Installation**
   ```bash
   # Install required packages
   pip install -r requirements.txt
   ```

### MySQL Setup
1. **Server Configuration**
   - Host: 121.4.251.254
   - Port: 5034
   - User: root
   - Password: root

2. **Database Initialization**
   - Database name: word_search
   - Table naming: word_search_YYYYMMDD
   - Automatic creation on first run

## Project Structure Setup

### Directory Organization
```bash
# Create project directories
mkdir -p data/epub data/excel src/epub src/excel src/db tests doc
```

### File Placement
1. **EPUB Files**
   - Location: `data/epub/`
   - Supported formats: .epub
   - Automatic detection

2. **Excel Files**
   - Location: `data/excel/`
   - Input: enWords_learn_with_freq_win_Oct28.xlsx
   - Output: processed_enWords_learn_with_freq_win_Oct28.xlsx

## Configuration

### Excel Configuration
1. **Input Format**
   - Required columns:
     - Lemma: Words to search
     - Wordlist: Source information
     - Summary: Word descriptions
   - Optional columns preserved

2. **Output Format**
   - Original columns maintained
   - Additional columns per book
   - 'NoWord' for missing entries

### Database Configuration
1. **Table Structure**
   ```sql
   CREATE TABLE word_search_YYYYMMDD (
       id INT AUTO_INCREMENT PRIMARY KEY,
       Lemma VARCHAR(1000),
       -- Additional columns
   )
   ```

2. **Connection Parameters**
   ```python
   connection_params = {
       'host': '121.4.251.254',
       'port': 5034,
       'user': 'root',
       'password': 'root'
   }
   ```

## Running the System

### 1. EPUB Search
```bash
# Run EPUB reader
python src/epub/epub_reader.py
```

### 2. Excel Processing
```bash
# Process Excel file
python src/excel/process_excel.py
```

### 3. Database Import
```bash
# Import to MySQL
python src/db/excel_to_mysql.py

# Verify import
python src/db/verify_mysql.py
```

## Error Handling

### Common Issues
1. **File Access**
   - Verify file permissions
   - Check file paths
   - Ensure file formats

2. **Database Connection**
   - Verify network connectivity
   - Check credentials
   - Confirm server status

3. **Memory Issues**
   - Monitor resource usage
   - Consider file size limits
   - Implement batch processing

## Monitoring

### Progress Tracking
1. **Console Output**
   - Processing status
   - Error messages
   - Completion indicators

2. **Verification**
   - Row counts
   - Data samples
   - Error logs

## Maintenance

### Regular Tasks
1. **Data Cleanup**
   - Archive processed files
   - Remove temporary files
   - Manage database growth

2. **System Updates**
   - Update dependencies
   - Check for security patches
   - Maintain documentation

## Security

### Best Practices
1. **Data Protection**
   - Secure file permissions
   - Encrypt sensitive data
   - Use secure connections

2. **Access Control**
   - Manage user permissions
   - Protect credentials
   - Monitor access logs

## Troubleshooting

### Common Solutions
1. **File Issues**
   ```bash
   # Check file existence
   ls -l data/epub/
   ls -l data/excel/

   # Verify permissions
   chmod 644 data/epub/*
   chmod 644 data/excel/*
   ```

2. **Database Issues**
   ```bash
   # Test connection
   python -c "import mysql.connector; mysql.connector.connect(host='121.4.251.254', port=5034, user='root', password='root')"
   ```

3. **Python Issues**
   ```bash
   # Verify environment
   python --version
   pip list
   ```

## Support

### Getting Help
1. **Documentation**
   - Review technical docs
   - Check error guides
   - Follow setup instructions

2. **Issue Reporting**
   - Provide error messages
   - Include system details
   - Describe reproduction steps