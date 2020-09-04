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