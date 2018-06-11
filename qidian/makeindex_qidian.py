import json
import os

import progressbar
from elasticsearch import Elasticsearch


es = Elasticsearch(hosts="kiddd.science:19200")
with open("qidian.txt") as f:
    lines = f.readlines()
    for line in progressbar.progressbar(lines, redirect_stdout=True):
        book = json.loads(line)

        path = 'books_qidian/' + book['bid']
        if os.path.exists(path + '.txt'):
            book['download'] = 'qidian/' + book['bid'] + '.txt'
        elif os.path.exists(path + '.epub'):
            book['download'] = 'qidian/' + book['bid'] + '.epub'
        else:
            print('ERROR, there is no %s' % book['title'])
            continue
        del book['bid']
        try:
            es.create(index='ebooks', id=book['download'], doc_type='book', body=book)
        except Exception as e:
            print(e)
