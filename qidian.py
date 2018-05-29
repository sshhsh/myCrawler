# -*- coding:utf -8 -*-
import json
import os
import re
import time
import urllib.request
from bs4 import BeautifulSoup


def crawl(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers = {'User-Agent': user_agent}
    response = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(response).read()
    except Exception as e:
        print('failed in %s' % url)
        print(e)
        return
    soup = BeautifulSoup(html, 'html.parser')
    book_list = soup.find_all('div', class_='book-mid-info')
    for book in book_list:
        name = book.find('h4')
        data_bid = name.next.attrs['data-bid']
        book_address = 'https:' + name.next.attrs['href'] + '#Catalog'
        print(book_address)
        print(data_bid)
        try:
            author = book.find(class_='author').find(class_='name')
            date = book.find(class_='update').find(class_='red')
            doc = {
                'bid': data_bid,
                'title': name.next.text,
                'author': author.text,
                'time': date.text,
                'url': book_address
            }
            doc_write = json.dumps(doc, ensure_ascii=False)
            print(name.next.text)
            download_book(book_address, data_bid)
            with open('qidian.txt', 'a') as f:
                f.write(doc_write)
                f.write('\n')
        except Exception as e:
            print('failed in %s' % book_address)
            print(e)
            continue


def download_book(url, bid):
    try:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        ab = soup.find('div', class_='volume-wrap')
        chapter_list = re.finditer(
            r'<li data-rid=".*?" data-eid="qd_G55" href="(.*?) target="_blank" title=".*?">(.*?)</a>', str(ab))
        with open('books_qidian/' + bid + '.txt', 'w+') as f:
            for chapter in chapter_list:
                address_chapter = 'http:' + chapter.group(1)
                name_chapter = chapter.group(2)
                html_chapter = urllib.request.urlopen(address_chapter).read()
                soup_chapter = BeautifulSoup(html_chapter, 'html.parser')
                content_chapter = soup_chapter.find('div', class_="read-content j_readContent").get_text('\n')
                f.write(name_chapter + '\n\n' + content_chapter + '\n')
                print(name_chapter)
    except Exception as e:
        raise e


isExists = os.path.exists('books_qidian')
if not isExists:
    os.makedirs('books_qidian')
for b in range(464, 1, -1):
    url1 = "https://www.qidian.com/free/all?size=2&orderId=5&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0" \
           "&hiddenField=1&page=%d" % b
    crawl(url1)
