import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os

class EPUBReader:
    def __init__(self, epub_paths):
        if isinstance(epub_paths, str):
            epub_paths = [epub_paths]
        self.books = {}
        for path in epub_paths:
            book_name = os.path.basename(path)
            self.books[book_name] = {
                'book': epub.read_epub(path),
                'content_map': {},
                'current_section': 0
            }
            self.process_book(book_name)

    def process_book(self, book_name):
        """Process the EPUB book and extract text content with section information."""
        book_data = self.books[book_name]
        for item in book_data['book'].get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text = soup.get_text()
                if text.strip():  # Only store non-empty sections
                    book_data['content_map'][book_data['current_section']] = {
                        'text': text,
                        'title': self.get_section_title(soup),
                        'item': item
                    }
                    book_data['current_section'] += 1

    def get_section_title(self, soup):
        """Extract the title from a section."""
        title_tag = soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        return title_tag.get_text() if title_tag else 'Untitled Section'

    def search_word(self, word):
        """Search for a word and return the first occurrence from each book."""
        results = []
        for book_name, book_data in self.books.items():
            found = False
            for section_num, content in book_data['content_map'].items():
                if found:
                    break
                text = content['text']
                index = text.lower().find(word.lower())
                
                if index != -1:
                    # Get the surrounding sentence
                    start = max(0, text.rfind('.', 0, index) + 1)
                    end = text.find('.', index) + 1
                    if end == 0:  # If no period found after the word
                        end = len(text)
                    
                    sentence = text[start:end].strip()
                    results.append({
                        'book_name': book_name,
                        'section': section_num,
                        'section_title': content['title'],
                        'sentence': sentence,
                        'position': index
                    })
                    found = True
        return results if results else None

def main():
    # Get all EPUB files from the data/epub directory
    epub_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'epub')
    epub_files = [os.path.join(epub_dir, f) for f in os.listdir(epub_dir) if f.lower().endswith('.epub')]
    available_files = epub_files
    
    if not available_files:
        print("Error: No EPUB files found")
        return

    # Create reader instance
    reader = EPUBReader(available_files)
    print(f"EPUB files loaded successfully. Ready to search!")
    print(f"Loaded books: {', '.join(available_files)}")

    # Interactive search loop
    while True:
        word = input("\nEnter a word to search (or 'quit' to exit): ").strip()
        if word.lower() == 'quit':
            break

        results = reader.search_word(word)
        if results:
            print(f"\nFound {len(results)} occurrence(s):")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. In book: {result['book_name']}")
                print(f"   Section {result['section']}: {result['section_title']}")
                print(f"   Context: {result['sentence']}")
        else:
            print(f"\nWord '{word}' not found in any of the books.")

if __name__ == '__main__':
    main()