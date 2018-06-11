import json
import urllib.request

import progressbar
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
headers = {'User-Agent': user_agent}

with open("qidian_index.txt") as f:
    lines = f.readlines()
    for line in progressbar.progressbar(lines, redirect_stdout=True):
        book = eval(line)
        url = book["url"]
        response = urllib.request.Request(url, headers=headers)
        try:
            html = urllib.request.urlopen(response).read()
        except Exception as e:
            print('failed in %s' % url)
            print(e)
            continue
        soup = BeautifulSoup(html, 'html.parser')
        search = soup.find("a", attrs={"data-eid": "qd_G17"})
        comments_url = 'https:' + search.attrs['href']
        response = urllib.request.Request(comments_url, headers=headers)
        try:
            html = urllib.request.urlopen(response).read()
        except Exception as e:
            print('failed in %s' % url)
            print(e)
            continue
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all(class_='post-body')
        if len(posts) <= 0:
            continue
        comment_list = []
        for post in posts:
            comment_list.append(post.text)
        with open("qidian_comments.txt", "a") as w:
            doc = {
                "id": book['download'],
                "content": comment_list
            }
            doc_write = json.dumps(doc, ensure_ascii=False)
            w.write(doc_write)
            w.write('\n')

