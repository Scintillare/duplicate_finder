# curl -X DELETE "http://localhost:9200/_all"

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
import config

es = Elasticsearch()
ses = SignatureES(es, distance_cutoff=config.DISTANCE_CUTOFF)

# ses.add_image('D:/Diana/Pictures/Диана 9+12.jpg')
# ses.add_image('D:/Diana/Pictures/Диана 3+4.jpg')
# ses.add_image('D:/Diana/Pictures/merlin.jpg')
# ses.add_image('D:/Diana/Pictures/Camera Roll/WIN_20200824_11_24_50_Pro.jpg')
# ses.add_image('D:/Diana/Pictures/merlin3.jpg')
# ses.add_image('D:/Diana/Pictures/Camera Roll/WIN_20200824_11_25_01_Pro.jpg')

# ses.delete_duplicates('D:/Diana/Pictures/Диана 9+12.jpg')
# ses.delete_duplicates('D:/Diana/Pictures/Диана 3+4.jpg')
# ses.delete_duplicates('D:/Diana/Pictures/merlin.jpg')
# ses.delete_duplicates('D:/Diana/Pictures/Camera Roll/WIN_20200824_11_24_50_Pro.jpg')
# ses.delete_duplicates('D:/Diana/Pictures/merlin3.jpg')
# ses.delete_duplicates('D:/Diana/Pictures/Camera Roll/WIN_20200824_11_25_01_Pro.jpg')


res = ses.search_image('D:/Diana/Pictures/Camera Roll/WIN_20200824_11_24_50_Pro.jpg',all_orientations=True)
print(res)

# res = ses.search_image('https://upload.wikimedia.org/wikipedia/commons/e/e0/Caravaggio_-_Cena_in_Emmaus.jpg')
# print(res)

# ses = SignatureES(es, distance_cutoff=0.3)
# # res = ses.search_image('https://pixabay.com/static/uploads/photo/2012/11/28/08/56/mona-lisa-67506_960_720.jpg')
# print(res)

