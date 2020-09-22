# curl -X DELETE "http://localhost:9200/_all"

import os
from os.path import join
from elasticsearch import Elasticsearch, ElasticsearchException
from image_match.elasticsearch_driver import SignatureES


class ImageFinder():
    def __init__(self):
        self.BASE_DIR = None 
        self.DISTANCE_CUTOFF = 0.4
        self.es = Elasticsearch()
        self.ses = SignatureES(self.es, distance_cutoff=self.DISTANCE_CUTOFF)
        self.index_name = "images"

    def es_iterate_all_documents(self, index, pagesize=250, scroll_timeout="1m", **kwargs):
        """
        https://techoverflow.net/2019/05/07/elasticsearch-how-to-iterate-scroll-through-all-documents-in-index/
        Helper to iterate ALL values from a single index
        Yields all the documents.
        """
        is_first = True
        while True:
            # Scroll next
            if is_first: # Initialize scroll
                result = self.es.search(index=index, scroll="1m", **kwargs, body={
                    "size": pagesize
                })
                is_first = False
            else:
                result = self.es.scroll(body={
                    "scroll_id": scroll_id,
                    "scroll": scroll_timeout
                })
            scroll_id = result["_scroll_id"]
            hits = result["hits"]["hits"]
            # Stop after no more docs
            if not hits:
                break
            # Yield each entry
            yield from (hit['_source'] for hit in hits)

    def get_similar_groups(self):
        for entry in self.es_iterate_all_documents(index=self.index_name):
            similar = self.ses.search_image(entry['path'])
            if len(similar) != 1:
                yield [record for record in similar]

    def add_images(self):
        # self.es.indices.create(index=self.index_name, ignore=400)
        try:
            self.es.indices.create(index=self.index_name)
        except ElasticsearchException as es1:
            raise es1
            # with open('err_log.txt', mode='a') as log:
            #     log.write(str(es1))
        
        img_formats = ('jpeg', 'jpg', 'png')

        for root, dirs, files in os.walk(self.BASE_DIR):
            for name in files:
                fn = os.path.abspath(join(root, name))
                *_, frmt = name.split('.')
                if (frmt.lower() in img_formats):
                    try:
                        self.ses.add_image(fn)
                        yield fn
                    except Exception as err:
                        raise err
                        # with open('err_log.txt', mode='a') as log:
                        #     log.write(fn)
                        #     log.write(str(err))

    def delete_index(self):
        self.es.indices.delete(index=self.index_name, ignore=[400, 404])

    def delete_doc(self, id):
        # db.delete_by_query(index='reestr',doc_type='some_type', q={'name': 'Jacobian'})
        # self.es.delete(es_index=self.index_name, id=id)
        pass

    def is_index_created(self):
        return self.es.indices.exists(index=self.index_name)
