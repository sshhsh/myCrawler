import json
import urllib.request
from urllib.error import URLError, HTTPError
import re
import time
from bs4 import BeautifulSoup


def get_article(url):
    time.sleep(12)
    try:
        resp = urllib.request.urlopen(url)
    except HTTPError as e:
        print('The server could not fulfill the request.')
        print('Error code: ', e.code)
        return
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        return
    except Exception as e:
        print("strange in %s", url)
        return
    html = resp.read()
    bs = BeautifulSoup(html, "html.parser", from_encoding="gb18030")
    title = re.sub('<.*?>', '', str(bs.h1))
    print(title)
    publish_date = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', str(bs.find(class_="text")))
    print(publish_date.group())
    content = str(bs.find(class_=re.compile('article-content.*')))
    content2 = re.search('</span>\n(<p>.*?</p>\n)*', content, re.S)

    content3 = re.sub('<.*?>', '', content2.group())
    print(content3)
    if len(content3) <= 10:
        print("failed to crawl the content")
        return
    search_author = re.search('<span>(.*)</span>', str(bs.find(class_="article-writer")))
    print(search_author.group(1))
    doc = {
        "title": title,
        "content": content3,
        "author": search_author.group(1),
        "time": publish_date.group(),
        "url": url
    }
    data = json.dumps(doc, ensure_ascii=False)
    print(data)
    with open('duanwenxue.txt', 'a') as f:
        f.write(data)
        f.write('\n')


address_list = [
    '/shanggan/rizhi/',
]


def crawl(url):
    try:
        resp = urllib.request.urlopen(url)
    except Exception as e:
        print("failed in %s", url)
        return
    html = str(resp.read().decode('gb18030'))
    search_article = re.findall('href="(/article/[0-9]*.html)',html)
    for address in search_article:
        get_article('https://www.duanwenxue.com' + address)
    search_next = re.search(u'<a href="(.*?)">\u4e0b\u4e00\u9875</a>', html)
    new_url = re.sub('list.*', '', url) + search_next.group(1)
    crawl(new_url)


for address in address_list:
    crawl('https://www.duanwenxue.com' + address)
