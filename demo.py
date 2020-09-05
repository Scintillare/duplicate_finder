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

os.mkdir(path, mode=0o777, *, dir_fd=None)
os.makedirs(name, mode=0o777, exist_ok=False)
Recursive directory creation function. Like mkdir(), but makes all intermediate-level directories needed to contain the leaf directory.

os.remove(path, *, dir_fd=None)
Remove (delete) the file path. If path is a directory, an IsADirectoryError is raised. Use rmdir() to remove directories.

os.removedirs(name)
Remove directories recursively. Works like rmdir() except that,

os.rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None)

os.renames(old, new)

os.rmdir(path, *, dir_fd=None)
Remove (delete) the directory path.


for root, dirs, files in os.walk(base_dir):
    # print(root, "consumes", end=" ")
    # print(sum(getsize(join(root, name))/1024 for name in files), end=" ")
    # print("mbytes in", len(files), "non-directory files")
    # if 'CVS' in dirs:
    #     dirs.remove('CVS')  # don't visit CVS directories

# os.listdir(path='.')
# os.scandir(path='.')
# Return an iterator of os.DirEntry objects
# is_dir() and is_file() 

# with os.scandir(path) as it:
#     for entry in it:
#         if not entry.name.startswith('.') and entry.is_file():
#             print(entry.name)

'''
really remove
import os
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
'''