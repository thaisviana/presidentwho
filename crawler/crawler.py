import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


HEADERS = {
    'user-agent':
        'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'accept-encoding': 'gzip, deflate',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

MAX_WORKERS = 4


def featch_url(url):
    try:
        res = requests.get(url, headers=HEADERS)
    except:
        return url, ''
    return url, res.text

def get_links(page):
    from bs4 import BeautifulSoup
    urls = []
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
    return urls

def process_urls(urls):
    result = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(featch_url, url) for url in urls]
    for future in as_completed(futures):
        url, html = future.result()
        result[url] = html
    return result


if __name__ == '__main__':
    urls = ['http://g1.globo.com/']
    crawled = set()
    while urls:
        to_process = {url for url in urls if url not in crawled}
        print('start process urls: ', to_process)
        process_result = process_urls(to_process)
        urls = []
        for url, page in process_result.items():
            crawled.add(url)
            urls = get_links(page)
            #urls += re.findall(r'(?<=href=["\'])https?://.+?(?=["\'])', page)

    print('Crawled pages: ', crawled)
