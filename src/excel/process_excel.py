import pandas as pd
import sys
import os
from pathlib import Path

# Ensure we can import sibling modules under src/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from epub.epub_reader import EPUBReader

def get_epub_files():
    # Resolve project directories cross-platform
    base_dir = Path(__file__).resolve().parents[2]  # .../lemma_app
    epub_dir = base_dir / 'data' / 'epub'
    # Return full paths for EPUB files
    return [str(p) for p in epub_dir.glob('*.epub')]

def process_excel_file(excel_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Initialize EPUBReader with all EPUB files
    epub_files = get_epub_files()
    reader = EPUBReader(epub_files)
    
    # Create new columns for each book
    for book_path in epub_files:
        book_name = Path(book_path).name
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
    
    # Save the updated Excel file under lemma_app/data/excel
    base_dir = Path(__file__).resolve().parents[2]
    excel_dir = base_dir / 'data' / 'excel'
    excel_dir.mkdir(parents=True, exist_ok=True)
    output_path = excel_dir / f"processed_{Path(excel_path).name}"
    df.to_excel(output_path, index=False)
    print(f"\nResults saved to {output_path}")

if __name__ == '__main__':
    base_dir = Path(__file__).resolve().parents[2]
    excel_dir = base_dir / 'data' / 'excel'
    excel_file = excel_dir / 'enWords_learn_with_freq_win_Oct28.xlsx'
    process_excel_file(str(excel_file))