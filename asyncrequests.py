#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    code to test aync feature of request
"""
from requests import async
import datetime 
from gevent import monkey; monkey.patch_all()
import gevent

def get_files_to_download():
    files_to_download = []
    with open('downloads.txt', 'r') as f:
        for to_download in f:
            files_to_download.append(to_download.split('\n')[0])
    return files_to_download

def write_to_disk(response):
    if response.ok:
        with open(response.headers['content-disposition'].split('=')[1],
                          'wb') as f:
            f.write(response.content)
    
def main():
    urls = get_files_to_download()
    start = datetime.datetime.now()
    print("Requests aync started")
    rs = [async.get(url) for url in urls]
    responses = async.map(rs)
    jobs = [gevent.spawn(write_to_disk, response) for response in responses]
    gevent.joinall(jobs)
    print("Requests async took {0} seconds for {1} urls".format(\
          datetime.datetime.now() - start, len(urls)))

if __name__ == "__main__":
    main()


