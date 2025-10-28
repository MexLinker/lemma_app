import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from epub.epub_reader import EPUBReader

def get_epub_files():
    epub_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'epub')
    return [f for f in os.listdir(epub_dir) if f.endswith('.epub')]

def process_excel_file(excel_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Initialize EPUBReader with all EPUB files
    epub_files = get_epub_files()
    reader = EPUBReader(epub_files)
    
    # Create new columns for each book
    for book_name in epub_files:
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
    output_path = 'processed_' + os.path.basename(excel_path)
    df.to_excel(output_path, index=False)
    print(f'\nResults saved to {output_path}')

if __name__ == '__main__':
    excel_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'excel')
    excel_file = os.path.join(excel_dir, 'enWords_learn_with_freq_win_Oct28.xlsx')
    process_excel_file(excel_file)