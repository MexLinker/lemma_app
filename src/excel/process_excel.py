import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from epub.epub_reader import EPUBReader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
EXCEL_DIR = os.path.join(DATA_DIR, 'excel')
EPUB_DIR = os.path.join(DATA_DIR, 'epub')

def get_epub_files():
    return [os.path.join(EPUB_DIR, f) for f in os.listdir(EPUB_DIR) if f.lower().endswith('.epub')]

def process_excel_file(excel_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Initialize EPUBReader with all EPUB files
    epub_files = get_epub_files()
    reader = EPUBReader(epub_files)
    
    # Create new columns for each book
    for book_path in epub_files:
        book_name = os.path.basename(book_path)
        df[book_name] = 'NoWord'  # Default value
    
    # Process each word in the Lemma column
    total_words = len(df)
    for idx, row in df.iterrows():
        word = row['Lemma']
        
        # Skip NaN values
        if pd.isna(word):
            print(f'Skipping row {idx + 1}/{total_words}: NaN value')
            continue
            
        print(f'Processing word {idx + 1}/{total_words}: {word}')
        
        results = reader.search_word(str(word))
        if results:  # Only process if results were found
            for result in results:
                book_name = result['book_name']
                df.at[idx, book_name] = result['sentence']
    
    # Save the updated Excel file
    output_path = os.path.join(EXCEL_DIR, 'processed_' + os.path.basename(excel_path))
    df.to_excel(output_path, index=False)
    print(f'\nResults saved to {output_path}')

if __name__ == '__main__':
    excel_dir = EXCEL_DIR
    excel_file = os.path.join(excel_dir, 'enWords_learn_with_freq_win_Oct28.xlsx')
    process_excel_file(excel_file)