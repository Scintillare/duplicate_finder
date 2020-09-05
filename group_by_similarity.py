import config
import os
from os.path import join
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
from PIL import Image
import shutil

base_dir = config.BASE_DIR
group_dir = config.GROUPS_DIR
es = Elasticsearch()
ses = SignatureES(es, distance_cutoff=config.DISTANCE_CUTOFF)

unic_dir = join(group_dir, 'unics')
os.mkdir(unic_dir)

for root, dirs, files in os.walk(base_dir):
    for name in files:
        fn = join(root, name)
        print(fn)
        similar = ses.search_image(fn)
        if len(similar) != 1:
            cur_dir = join(group_dir, f'{name}_{len(similar)}')
            os.mkdir(cur_dir)
        else:
            cur_dir = unic_dir
        for record in similar:
            img_path = record['path']
            yield #TODO
            try:
                # shutil.move(img_path, cur_dir)
                # os.remove(fn)
            except Exception as e:
                print(e)
                print(img_path)

        # for r in res:
        #     im = Image.open(r['path'])
        #     im.show()

        exit()