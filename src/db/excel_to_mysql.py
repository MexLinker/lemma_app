import pandas as pd
import mysql.connector
from datetime import datetime
import time
import os

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='121.4.251.254',
            port=5034,
            user='root',
            password='root'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database_and_table(connection):
    try:
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS word_search")
        cursor.execute("USE word_search")
        
        # Get current date for table name
        current_date = datetime.now().strftime('%Y%m%d')
        table_name = f'word_search_{current_date}'
        
        # Read Excel to get column names and types
        excel_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'excel')
        df = pd.read_excel(os.path.join(excel_dir, 'processed_enWords_learn_with_freq_win_Oct28.xlsx'))
        
        # Create table with all columns from Excel
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        create_table_sql += "id INT AUTO_INCREMENT PRIMARY KEY,"
        
        for column in df.columns:
            # Use VARCHAR(1000) for text columns to accommodate long sentences
            create_table_sql += f"`{column}` VARCHAR(1000),"
        
        create_table_sql = create_table_sql.rstrip(',') + ")"
        cursor.execute(create_table_sql)
        
        return table_name
    
    except mysql.connector.Error as err:
        print(f"Error creating database/table: {err}")
        return None
    finally:
        cursor.close()

def insert_data(connection, table_name):
    try:
        cursor = connection.cursor()
        
        # Read Excel data
        excel_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'excel')
        df = pd.read_excel(os.path.join(excel_dir, 'processed_enWords_learn_with_freq_win_Oct28.xlsx'))
        
        # Prepare insert statement
        columns = ",".join([f"`{col}`" for col in df.columns])
        placeholders = ",".join(["%s"] * len(df.columns))
        insert_sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Insert data row by row with retry mechanism
        for index, row in df.iterrows():
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    values = [str(val) if pd.notna(val) else None for val in row]
                    cursor.execute(insert_sql, values)
                    connection.commit()
                    if (index + 1) % 100 == 0:
                        print(f"Processed {index + 1} rows")
                    break
                
                except mysql.connector.Error as err:
                    print(f"Error inserting row {index + 1}: {err}")
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"Retrying... Attempt {retry_count + 1} of {max_retries}")
                        time.sleep(2)  # Wait 2 seconds before retrying
                    else:
                        print(f"Failed to insert row {index + 1} after {max_retries} attempts")
        
        print("Data insertion completed")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def main():
    # Create connection
    connection = create_connection()
    if not connection:
        return
    
    try:
        # Create database and table
        table_name = create_database_and_table(connection)
        if not table_name:
            return
        
        # Insert data
        insert_data(connection, table_name)
        
    finally:
        connection.close()

if __name__ == '__main__':
    main()