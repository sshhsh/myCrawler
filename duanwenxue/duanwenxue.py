import json
import urllib.request
import re
import time
from bs4 import BeautifulSoup


def get_article(url):
    print('Crawling %s' % url)
    time.sleep(2)
    try:
        resp = urllib.request.urlopen(url)
        html = resp.read()
        bs = BeautifulSoup(html, "html.parser", from_encoding="gb18030")
        title = re.sub('<.*?>', '', str(bs.h1))
        # print(title)
        publish_date = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', str(bs.find(class_="text")))
        # print(publish_date.group())
        content = str(bs.find(class_=re.compile('article-content.*')))
        content2 = re.search('</span>\n(<p>.*?</p>\n)*', content, re.S)

        content3 = re.sub('<.*?>', '', content2.group())
        # print(content3)
        if len(content3) <= 10:
            print("failed to crawl the content")
            return
        search_author = re.search('<span>(.*)</span>', str(bs.find(class_="article-writer")))
        # print(search_author.group(1))
        doc = {
            "title": title,
            "content": content3,
            "author": search_author.group(1),
            "time": publish_date.group(),
            "url": url
        }
        data = json.dumps(doc, ensure_ascii=False)
        # print(data)
    except Exception as e:
        print("strange in %s", url)
        print(e)
        return

    with open('duanwenxue.txt', 'a') as f:
        f.write(data)
        f.write('\n')


address_list = [
    '/shanggan/ganrengushi/',
    '/qinggan/gushi/',
    '/sanwen/suibi/',
]


def crawl(url):
    print('Crawling %s' % url)
    try:
        resp = urllib.request.urlopen(url)
        html = str(resp.read().decode('gb18030'))
        search_article = re.findall('href="(/article/[0-9]*.html)', html)
        for article_address in search_article:
            get_article('https://www.duanwenxue.com' + article_address)
        search_next = re.search(u'<a href="(.*?)">\u4e0b\u4e00\u9875</a>', html)
        new_url = re.sub('list.*', '', url) + search_next.group(1)
        crawl(new_url)
    except Exception as e:
        print("failed in %s", url)
        print(e)
        return


for address in address_list:
    crawl('https://www.duanwenxue.com' + address)
