# curl -X DELETE "http://localhost:9200/_all"
'''
# TODO Sometimes you want to store information with your images independent of the reverse image search functionality. 
# You can do that with the metadata= field in the add_image function.

Let’s add one of the images again, with some extra data:

ses.add_image('https://c2.staticflickr.com/8/7158/6814444991_08d82de57e_z.jpg', metadata={'things': 'stuff!'})

Where we can see a little extra info. 
image-match doesn’t provide anyway to query the metadata directly, but the user can use Elasticsearch’s QL, for example with:

ses.es.search('images', body={'query': {'match': {'metadata.things': 'stuff!'}}})
'''

import config
import os
from os.path import join
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

base_dir = config.BASE_DIR
es = Elasticsearch()
ses = SignatureES(es, distance_cutoff=config.DISTANCE_CUTOFF)

for root, dirs, files in os.walk(base_dir):
    for name in files:
        fn = join(root, name)
        if ('jpg' in fn 
            or 'JPG' in fn
            or 'jpeg' in fn 
            or 'png' in fn):
            try:
                ses.add_image(fn)
                print(fn)
            except Exception as e:
                with open('err_log.txt', mode='a') as log:
                    log.write(fn)
                    log.write(str(e))


