import json

import progressbar
from elasticsearch import Elasticsearch


es = Elasticsearch(hosts="kiddd.science:19200")
with open("qidian_comments.txt") as f:
    lines = f.readlines()
    for line in progressbar.progressbar(lines, redirect_stdout=True):
        book = json.loads(line)

        bid = book['id']
        del book['id']
        doc = {
            "doc": {
                "comments": book['content']
            }
        }
        try:
            es.update(index='ebooks', doc_type='book', id=bid, body=doc)
            # es.create(index='comments', id=bid, doc_type='comment', body=book)
        except Exception as e:
            print(e)
