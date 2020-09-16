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

    def get_similar_groups(self):
        for root, dirs, files in os.walk(self.BASE_DIR):
            for name in files:
                similar = self.ses.search_image(join(root, name))
                if len(similar) != 1:
                    yield [record['path'] for record in similar]

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
                fn = join(root, name)
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

    def is_index_created(self):
        return self.es.indices.exists(index=self.index_name)