import json

import progressbar
from elasticsearch import Elasticsearch


es = Elasticsearch(hosts="kiddd.science:19200")
with open("gutenberg.txt") as f:
    lines = f.readlines()
    for line in progressbar.progressbar(lines, redirect_stdout=True):
        book = json.loads(line)
        book['download'] = 'gutenberg/' + book['bid'] + '.txt'
        del book['bid']
        try:
            es.create(index='ebooks', id=book['download'], doc_type='book', body=book)
        except Exception as e:
            print(e)
