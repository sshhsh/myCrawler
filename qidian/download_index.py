import progressbar
from elasticsearch import Elasticsearch


es = Elasticsearch(hosts="kiddd.science:19200")
with open("qidian_index.txt", "w") as f:
    res = es.search(index="ebooks", body={
        "query": {"match": {"download": "qidian"}},
        "size": 100
    }, scroll="10m")
    scroll_id = res['_scroll_id']
    for hit in progressbar.progressbar(res['hits']['hits']):
        f.write(str(hit))
        f.write('\n')

    while True:
        res = es.scroll(scroll_id=scroll_id, scroll="10m")
        length = len(res['hits']['hits'])
        if length == 0:
            break
        for hit in progressbar.progressbar(res['hits']['hits']):
            f.write(str(hit))
            f.write('\n')


# with open("qidian_index.txt", "w") as f:
#     for i in range(0, 236):
#         res = es.search(index="ebooks", body={
#             "query": {"match": {"download": "qidian"}},
#             "size": 100,
#             "from": i*100
#         })
#
#         for hit in progressbar.progressbar(res['hits']['hits']):
#             f.write(str(hit))
#             f.write('\n')
