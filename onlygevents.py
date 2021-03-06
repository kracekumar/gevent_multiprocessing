#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file is example for only gevent producer & consumer
"""
from gevent import monkey; monkey.patch_all();
from gevent.queue import Queue
import gevent
import datetime
from Queue import Empty
from multiprocessing import cpu_count

class Consumer(object):
    def __init__(self, q, no_tasks, name):
        self._no_tasks = no_tasks
        self._queue = q
        self.name = name
        self._rungevent(self._queue, self._no_tasks)

    def _rungevent(self, q, no_tasks):
        jobs = [gevent.spawn(self._printq, q) for x in xrange(no_tasks)]
        gevent.joinall(jobs)

    def _printq(self, q):
        try:
            while 1:
                print("{0} time: {1}, value: {2}".format(self.name,\
                                 datetime.datetime.now(), q.get_nowait()))
        except Empty:
            print("All is well")
        return

class Producer(object):
    def __init__(self, q, no_tasks, name):
       self._q = q
       self._no_tasks = no_tasks
       self.name = name
       self._rungevent(self._no_tasks)

    def _rungevent(self, no_tasks):
        jobs = [gevent.spawn(self.produce) for x in xrange(no_tasks)]
        gevent.joinall(jobs)

    def produce(self):
        for no in xrange(10000):
            print no
            self._q.put_nowait(no)
        return 

def main():
    q = Queue()
    print("Gevent on top multiprocessing with 17 gevent coroutines\
          \n 10 producers gevent and 7 consumers gevent")
    producer_gevents = 10
    consumer_gevents = 7
    cores = cpu_count()
    total_pair = cores * 2
    start = datetime.datetime.now()
    for i in xrange(total_pair):
        if not i % 2:
            p = Producer(q, producer_gevents, "producer")
        else:
            c = Consumer(q, consumer_gevents, "consumer")

    print("{0} process with {1} producer gevents and {2} consumer gevents took\
           {3} seconds to produce {4} numbers and consume".format(1, \
           producer_gevents*cores, consumer_gevents * cores, \
           datetime.datetime.now() - start, producer_gevents * cores * 10000))

   

if __name__ == '__main__':
    main()
