# -*- coding:utf -8 -*-
import json
import os
import re

import progressbar
from elasticsearch import Elasticsearch


isExists = os.path.exists('books_duanwenxue')
if not isExists:
    os.makedirs('books_duanwenxue')
es = Elasticsearch(hosts="kiddd.science:19200")
index = 1
with open("duanwenxue.txt") as f:
    lines = f.readlines()
    for line in progressbar.progressbar(lines, redirect_stdout=True):
        # print(line, end='')
        book = json.loads(line)
        book_id = re.search('article/([0-9]*)\.html', book['url']).group(1)
        book['download'] = 'duanwenxue/' + book_id + '.txt'
        if index <= 5530:
            book['category'] = '伤感日志'
        elif 5530 < index <= 12060:
            book['category'] = '情感故事'
        else:
            book['category'] = '散文随笔'

        with open('books_duanwenxue/' + book_id + '.txt', 'w+') as w:
            w.write(book['title'])
            w.write('\n')
            w.write(book['author'])
            w.write('\n')
            w.write(book['time'])
            w.write('\n')
            w.write(book['content'])

        del book['content']
        try:
            es.create(index='ebooks', id=book['download'], doc_type='book', body=book)
        except Exception as e:
            print(e)
        index += 1
