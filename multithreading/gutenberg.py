import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup


def get_book_links(document, limit=20, id='books-last30'):
    toplist = document.find(id=id).find_next_sibling('ol').find_all('a')
    return [urllib.parse.urljoin('http://www.gutenberg.org', a['href'])
            for a in toplist[:limit]]


def process_book(url):
    try:
        id = url.split('/')[-1]
        cache_url = f'https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt'
        detail_page = BeautifulSoup(requests.get(url).text, 'html.parser')
        title = detail_page.find('h1', attrs={'itemprop': 'name'}).string
        try:
            textcheck = re.compile('.*text/plain.*')
            cache_url = ('https:' +
                         detail_page.find('td', attrs={'content': textcheck})
                         .find('a', attrs={'type': textcheck})['href'])
        except (AttributeError, TypeError):
            pass
        text = requests.get(cache_url).text.lower()
        return title, {vowel: text.count(vowel) for vowel in 'aeiou'}
    except (TypeError, requests.exceptions.HTTPError) as e:
        print(e)
        return 'error', e


def top_20(which='books-last30', limit=20, workers=20):
    toppage = requests.get('https://www.gutenberg.org/browse/scores/top').text
    toppage = BeautifulSoup(toppage, 'html.parser')
    book_links = get_book_links(toppage, limit=limit)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return dict(executor.map(process_book, book_links))


if __name__ == '__main__':
    import pprint
    pprint.pprint(top_20())
