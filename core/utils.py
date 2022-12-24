import json
import requests
from bs4 import BeautifulSoup


def open_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data


def get_page_length(url):
    page = requests.get(str(url))
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find('nav', class_='sds-pagination').find_all('li', class_='sds-pagination__item')
    return len(data)


requests_cache = {}


def get_url(url, format_parser=None):
    if url in requests_cache:
        r = requests.get(url)
        html = requests.get(r.url)
        requests_cache[url] = BeautifulSoup(html.content, format_parser)
    return requests_cache[url]
