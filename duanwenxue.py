import json
import urllib.request
from urllib.error import URLError, HTTPError
import re
import time
from bs4 import BeautifulSoup

for i in range(4729413, 1, -1):
    url = "https://www.duanwenxue.com/article/%d.html" % i
    try:
        resp = urllib.request.urlopen(url)
    except HTTPError as e:
        print('The server could not fulfill the request.')
        print('Error code: ', e.code)
        continue
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        continue
    html = resp.read()
    bs = BeautifulSoup(html, "html.parser", from_encoding="gb18030")
    title = re.sub('<.*?>', '', str(bs.h1))
    print(title)
    publishDate = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', str(bs.find(class_="text")))
    print(publishDate.group())
    content = str(bs.find(class_=re.compile('article-content.*')))
    content2 = re.search('</span>\n(<p>.*?</p>\n)*', content, re.S)

    content3 = re.sub('<.*?>', '', content2.group())
    print(content3)
    if len(content3) <= 10:
        print("failed to crawl the content")
        continue
    searchAuthor = re.search('<span>(.*)</span>', str(bs.find(class_="article-writer")))
    print(searchAuthor.group(1))
    doc = {
        "title": title,
        "content": content3,
        "author": searchAuthor.group(1),
        "time": publishDate.group(),
        "url": url
    }
    data = json.dumps(doc, ensure_ascii=False)
    print(data)
    with open('duanwenxue.txt', 'a') as f:
        f.write(data)
        f.write('\n')
    time.sleep(0.6)
