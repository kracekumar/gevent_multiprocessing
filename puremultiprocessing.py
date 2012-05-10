#! /usr/bin/env python
# -*- coding: utf-8 -*

"""
    This is file is bench mark for downloading all files using pure 
    multiprocessing. Here we dont use threads or gevents.
"""
from multiprocessing import Process, Queue, cpu_count
from requests import get
import datetime
from Queue import Empty
import sys

def download(files_to_download):
    try:
        while 1:
            print("=== started to download ===")
            start = datetime.datetime.now()
            to_download = files_to_download.get_nowait()
            if to_download:
                dl_file = get(to_download)
                if dl_file.ok:
                    with open(dl_file.headers['content-disposition'].split('=')[1],
                          'wb') as f:
                        f.write(dl_file.content)
            print("{0} took {1} seconds".format(to_download, datetime.datetime.now(\
              ) - start))
    except Empty:
        print("queue is empty")
        sys.exit(0)
        

def main():
    files_to_download = Queue()
    with open('downloads.txt', 'r') as f:
        for to_download in f:
            files_to_download.put_nowait(to_download.split('\n')[0])
    print("=== puremultiprocessing ===")
    total_process = cpu_count()
    for i in range(total_process):
        p = Process(target = download, args=(files_to_download, ))
        p.start()
    print("=== end ===")


    

if __name__ == "__main__":
    main()
