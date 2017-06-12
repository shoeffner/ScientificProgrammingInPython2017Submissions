import re
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup


def text_link(href):
    """Returns a link to the cached version of a book.

    Args:
        href: the content of a top lists href attribute, usually something like
              /ebooks/1342 (this is Pride and Prejudice)
    Returns:
        The cache link for the book, this is more deterministic than scraping
        it.
    """
    id = href.split('/')[-1]
    return f'https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt'


def get_book_links(document, limit=20, id='books-last30'):
    """Filters the book links from the specified toplist.

    Args:
        document: The content of the top list page.
        limit: The number of books to retrieve.
        id: The list id, e.g. 'books-last30' or 'authors-last7'.

    Returns:
        A list of cache links to the selected books.
    """
    toplist = document.find(id=id).find_next_sibling('ol').find_all('a')
    return [text_link(a['href']) for a in toplist[:limit]]


def count_vowels(text):
    """Returns a dictionary which maps vowels to the number of occurences in
    text."""
    text = text.lower()
    return {vowel: text.count(vowel) for vowel in 'aeiou'}


def get_title(text):
    """Returns the title from the book, parsed from text.

    Searches for 'Title: ([^\r\n]*)' inside the text."""
    return re.search('Title: ([^\r\n]*)', text)[1]


def download_page(url):
    """Downloads the top page."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def download_book(url):
    """Downloads a book. Raises on error."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def process_book(url):
    """Downloads a book, extracts the title and counts its vowels.

    Args:
        url: The book url.

    Returns:
        A tuple mapping a title to a dictionary of vowel counts:
        ('Pride and Prejudice', {'a': 0, 'e': 0, ...})
    """
    try:
        text = download_book(url)
        return get_title(text), count_vowels(text)
    except (TypeError, requests.exceptions.HTTPError):
        return


def top_20(which='books-last30', limit=20, workers=4):
    """Returns a dictionary counting vowels per book.

    Args:
        which: The list id.
        limit: The number of books to process.
        workers: The number of threads to use.

    Returns:
        {
            'Pride and Prejudice': {
                'a': 0,
                'e': 0,
                'i': 0,
                'o': 0,
                'u': 0
            },
            'War and Peace': {
                'a': 0,
                'e': 0,
                'i': 0,
                'o': 0,
                'u': 0
            },
            ...
        }

    """
    toppage = download_page('https://www.gutenberg.org/browse/scores/top')
    book_links = get_book_links(toppage, limit=limit)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return dict(executor.map(process_book, book_links))


if __name__ == '__main__':
    import pprint

    limit = 20
    result = top_20(limit=limit, workers=30)

    assert len(result) == limit, f'Result does not contain {limit} items.'

    pprint.pprint(list(result.keys()))
    pprint.pprint(result)
