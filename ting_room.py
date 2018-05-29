import json
import re
import urllib.request
from bs4 import BeautifulSoup


def crawl(url):
    try:
        response = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(response).read()
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
            bid = re.sub('/', '', url2)
            doc = {
                'bid': bid,
                'title': title,
                'author': author_text,
                'url': url_book
            }
            doc_write = json.dumps(doc, ensure_ascii=False)
            print(doc_write)
            crawl_book(url_book)
            with open('ting_room.txt', 'a') as f:
                f.write(doc_write)
                f.write('\n')
        except Exception as e:
            print(e)
            print('failed in %s' % url)
            continue


def crawl_book(url):
    try:
        response = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(response).read()
        soup = BeautifulSoup(html, 'html.parser')
        download_link = soup.find('a', href='all001xp1').find_all(class_='list')
        # TODO
    except Exception as e:
        raise e


url_init = 'http://novel.tingroom.com/count.php?page=1'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
headers = {'User-Agent': user_agent}
crawl(url_init)
