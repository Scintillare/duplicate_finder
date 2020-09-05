import config
import os
import shutil
from os.path import join

def prepare_images():
    base_dir = config.BASE_DIR
    oth_dir = os.path.abspath(os.path.join(base_dir, os.pardir))
    oth_dir = join(oth_dir, 'other_formats')

    if not os.path.exists(oth_dir):
        os.mkdir(oth_dir)

    for root, dirs, files in os.walk(base_dir):
        for name in files:
            fn = join(root, name)
            if not ('jpg' in fn 
                    or 'JPG' in fn
                    or 'jpeg' in fn 
                    or 'png' in fn):
                try:
                    shutil.move(fn, oth_dir)
                    os.remove(fn)
                except Exception as e:
                    with open('err_log.txt', mode='a') as log:
                        log.write(fn)
                        log.write(str(e))
            

