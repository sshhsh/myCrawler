import json
import re

import os

import time

import requests
from bs4 import BeautifulSoup


def crawl(url):
    try:
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        book_list = soup.find('div', class_='all001xp1').find_all(class_='list')
    except Exception as e:
        print(e)
        print('failed in %s' % url)
        return
    for book in book_list:
        try:
            title = book.find(class_='yuyu').find('a').text
            author = book.find(class_='point').find('a')
            if author:
                author_text = author.text
            else:
                author_text = 'none'
            url2 = book.find(class_='yuyu').find('a').attrs['href']
            url_book = 'http://novel.tingroom.com' + url2
            bid = re.search('[0-9]*$', url2).group()
            doc = {
                'bid': bid,
                'title': title,
                'author': author_text,
                'url': url_book
            }
            doc_write = json.dumps(doc, ensure_ascii=False)
            print(doc_write)
            url_download = 'http://novel.tingroom.com/novel_down.php?aid=' + bid + '&dopost=txt'
            crawl_book(url_download, bid)
            with open('ting_room.txt', 'a') as f:
                f.write(doc_write)
                f.write('\n')
        except Exception as e:
            print(e)
            print('failed in %s' % url)
            continue


def crawl_book(url, file_name):
    time.sleep(5)
    try:
        r = requests.get(url, headers=headers)
        with open('books_tingroom/' + file_name + '.txt', "w+") as f:
            f.write(r.text)
        print('book downloaded')
    except Exception as e:
        raise e


isExists = os.path.exists('books_tingroom')
if not isExists:
    os.makedirs('books_tingroom')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
headers = {'User-Agent': user_agent}
for b in range(1, 210, 1):
    url_init = 'http://novel.tingroom.com/count.php?page=%d' % b
    crawl(url_init)
