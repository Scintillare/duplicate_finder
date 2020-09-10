import threading
import subprocess

class MyClass(threading.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen('rsync -av /etc/passwd /tmp'.split(),
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        self.stdout, self.stderr = p.communicate()

myclass = MyClass()
myclass.start()
myclass.join()
print myclass.stdout


subprocess.call(r"D:\\Important\\ElasticSearch\\7.9.1\\bin\\elasticsearch.exe")
