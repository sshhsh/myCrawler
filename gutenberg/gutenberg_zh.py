import json
import os
import xml.dom.minidom
import progressbar
import re


def parse_rdf(file):
    try:
        dom = xml.dom.minidom.parse(file)
        root_element = dom.documentElement
        search_element = root_element.getElementsByTagName('dcterms:title')
        title = search_element[0].firstChild.nodeValue
        if not title:
            # print('failed in %s' % file)
            return
        search_element = root_element.getElementsByTagName('dcterms:language')
        lang = search_element[0].getElementsByTagName('rdf:value')[0].firstChild.nodeValue
        if not lang == 'zh':
            # print('The language of %s is %s' % (title, lang))
            return
        search_element = root_element.getElementsByTagName('dcterms:issued')
        time_published = search_element[0].firstChild.nodeValue
        search_element = root_element.getElementsByTagName('pgterms:ebook')
        bid = search_element[0]._attrs['rdf:about'].nodeValue
        url = "http://www.gutenberg.org/" + bid
        bid = re.search('[0-9]*$', bid).group()
        search_element = root_element.getElementsByTagName('dcterms:creator')
        author = search_element[0].getElementsByTagName('pgterms:name')[0].firstChild.nodeValue
        search_element = root_element.getElementsByTagName('dcterms:subject')
        category = search_element[0].getElementsByTagName('rdf:value')[0].firstChild.nodeValue
        doc = {
            'bid': bid,
            'title': title,
            'author': author,
            'time': time_published,
            'url': url,
            'category': category
        }
        doc_write = json.dumps(doc, ensure_ascii=False)
        f.write(doc_write)
        f.write('\n')

    except Exception as e:
        # print(e)
        # print('failed in %s' % file)
        return


path = 'epub'
with open('gutenberg_zh.txt', 'w') as f:
    for root, dirs, files in progressbar.progressbar(os.walk(path), redirect_stdout=True):
        for name in files:
            file_path = os.path.join(root, name)
            extra = os.path.splitext(file_path)
            if extra[1] == '.rdf':
                parse_rdf(file_path)
