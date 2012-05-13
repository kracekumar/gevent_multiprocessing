#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    code to test multiprocessing and gevent
"""
from multiprocessing import Process, JoinableQueue, cpu_count
from requests import get, async
import datetime
from Queue import Empty
import gevent

def write_to_disk(response):
    print response.url
    if response.ok:
        with open(response.headers['content-disposition'].split('=')[1],
                          'wb') as f:
            f.write(response.content)
            return 1
    return 0

def download(q, result_queue, time_taken_to_download, \
            time_taken_to_read_from_queue, name):
    print("{0} process started".format(name))
    start = datetime.datetime.now()
    urls = []
    try:
        while 1:
             value = q.get()
             if value is not None:
                 urls.append(q.get())
             else:
                 break
    except Empty:
        pass
    time_taken_to_read_from_queue.put_nowait(datetime.datetime.now() - start)
    start = datetime.datetime.now()
    rs = [async.get(url) for url in urls]
    responses = async.map(rs)
    jobs = [gevent.spawn(write_to_disk, response) for response in responses]
    gevent.joinall(jobs)
    time_taken_to_download.put_nowait(datetime.datetime.now() - start)
    for job in jobs:
        result_queue.put_nowait(job.get())

def main(factor = 2):
    #E.G: if total cores is 2 , no of processes to be spawned is 2 * factor
    files_to_download = JoinableQueue()
    result_queue = JoinableQueue()
    time_taken = JoinableQueue()
    time_taken_to_read_from_queue = JoinableQueue()
    count = 0
    with open('downloads.txt', 'r') as f:
        for to_download in f:
            files_to_download.put_nowait(to_download.split('\n')[0])
            count += 1
    print count
    cores = cpu_count()
    no_of_processes = cores * factor
    for i in xrange(no_of_processes):
        files_to_download.put_nowait(None)
    jobs = []
    start = datetime.datetime.now()
    for name in xrange(no_of_processes):
        p = Process(target = download, args = (files_to_download, result_queue,\
                                time_taken, time_taken_to_read_from_queue,name))
        p.start()
        jobs.append(p)

    for job in jobs:
        job.join()

    total_downloaded_urls = 0
    try:
        while 1:
            r = result_queue.get_nowait()
            total_downloaded_urls += r

    except Empty:
        pass

    try:
        while 1:
            """
                locals() keeps track of all variable, functions, class etc.
                datetime object is different from int, one cannot perform 
                0 + datetime.datetime.now(), if when we access the queue which 
                contains time objects first time, total_time will be set to 
                first time 
            """
            if 'total_time' in locals():
                total_time += time_taken.get_nowait()
            else:
                total_time = time_taken.get_nowait()
    except Empty:
        print("{0} processes on {1} core machine took {2} time to download {3}\
              urls".format(no_of_processes, cores, total_time, \
                                          total_downloaded_urls))

    try:
        while 1:
            if 'queue_reading_time' in locals():
                queue_reading_time += time_taken_to_read_from_queue.get_nowait()
            else:
                queue_reading_time = time_taken_to_read_from_queue.get_nowait()
    except Empty:
        print("{0} processes on {1} core machine took {2} time to read {3}\
              urls from queue".format(no_of_processes, cores,queue_reading_time\
              ,time_taken_to_read_from_queue.qsize()))

if __name__ == "__main__":
    main()
