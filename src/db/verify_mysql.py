import mysql.connector
from datetime import datetime

def verify_data():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='121.4.251.254',
            port=5034,
            user='root',
            password='root',
            database='word_search'
        )
        cursor = connection.cursor()
        
        # Get current table name
        table_name = f'word_search_{datetime.now().strftime("%Y%m%d")}'
        
        # Get total count
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        total_count = cursor.fetchone()[0]
        print(f'Total rows in database: {total_count}')
        
        # Get first 5 rows
        cursor.execute(f'SELECT * FROM {table_name} LIMIT 5')
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        print('\nFirst 5 rows:\n')
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                if value is not None:  # Only include non-None values
                    row_dict[columns[i]] = value
            print(row_dict)
            print('-' * 80)
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    verify_data()