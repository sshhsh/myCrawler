import urllib.request

import re
from bs4 import BeautifulSoup

url = 'http://www.baidu.com'
resp = urllib.request.urlopen("https://www.duanwenxue.com/article/4620832.html")
html = resp.read()
bs = BeautifulSoup(html, "html.parser", from_encoding="gb18030")
print(bs.h1)
publishDate = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', str(bs.find(class_="text")))
print(publishDate.group())
content = str(bs.find(class_=re.compile('article-content.*')))
content2 = re.sub('<.*?>', '', content)
print(content)
searchAuthor = re.search('<span>(.*)</span>', str(bs.find(class_="article-writer")))
print(searchAuthor.group(1))
