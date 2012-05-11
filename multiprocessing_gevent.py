#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file is example of getting gevent on top of multiprocessing.
"""
from multiprocessing import Process, cpu_count, Queue, JoinableQueue
from gevent import monkey; monkey.patch_all(thread = True);
import gevent
import datetime
from Queue import Empty

class Consumer(object):
    def __init__(self, q, no_tasks, name):
        self._no_tasks = no_tasks
        self._queue = q
        self.name = name
        self._rungevent(self._queue, self._no_tasks)

    def _rungevent(self, q, no_tasks):
        print("starting gevent on multiprocessing")
        jobs = [gevent.spawn(self._printq, q) for x in xrange(no_tasks)]
        gevent.joinall(jobs)

    def _printq(self, q):
        try:
            while 1:
                print("{0} time: {1}, value: {2}".format(self.name,\
                                 datetime.datetime.now(), q.get_nowait()))
        except Empty:
            print("All is well")

class Producer(object):
    def __init__(self, q, no_tasks, name):
       print(name)
       self._q = q
       self._no_tasks = no_tasks
       self.name = name
       self._rungevent(self._no_tasks)

    def _rungevent(self, no_tasks):
        print("Producer started")
        jobs = [gevent.spawn(self.produce) for x in xrange(no_tasks)]
        gevent.joinall(jobs)

    def produce(self):
        print("producer gevent started")
        for no in xrange(10000):
            print no
            self._q.put_nowait(no)

def main():
    total_cores = cpu_count()
    q = Queue()
    print("Gevent on top multiprocessing with 17 gevent coroutines\
          \n 10 producers gevent and 7 consumers gevent")
    producer_gevents = 10
    consumer_gevents = 7
    jobs = []
    start = datetime.datetime.now()
    for x in xrange(total_cores):
        if not x % 2:
            p = Process(target=Producer, args=(q, producer_gevents, \
                                                     "producer %d"%x))
            p.start()
            jobs.append(p)
        else:
            p = Process(target = Consumer, args=(q, consumer_gevents,\
                                                      "consumer %d"%x))
            p.start()
            jobs.append(p)

    for job in jobs:
        job.join()
    print("{0} process with 17 gevent coroutines took {1} seconds to produce {2}\
           numbers and consume them".format(total_cores, datetime.datetime.now()\
           - start, producer_gevents * 10000))

    



if __name__ == '__main__':
    main()
