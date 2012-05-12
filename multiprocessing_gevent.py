#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file is example of getting gevent on top of multiprocessing.
"""
from multiprocessing import Process, cpu_count, Queue, JoinableQueue
from gevent import monkey; monkey.patch_all();
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
        jobs = [gevent.spawn(self._printq) for x in xrange(no_tasks)]
        gevent.joinall(jobs)

    def _printq(self):
        while 1:
            value = self._queue.get()
            if value is None:
                self._queue.task_done()
                break
            else:
                print("{0} time: {1}, value: {2}".format(self.name,\
                                 datetime.datetime.now(), value))
        return 

class Producer(object):
    def __init__(self, q, no_tasks, name, consumers_tasks):
       print(name)
       self._q = q
       self._no_tasks = no_tasks
       self.name = name
       self.consumer_tasks = consumers_tasks
       self._rungevent()

    def _rungevent(self):
        jobs = [gevent.spawn(self.produce) for x in xrange(self._no_tasks)]
        gevent.joinall(jobs)
        for x in xrange(self.consumer_tasks):
            self._q.put_nowait(None)
        self._q.close()

    def produce(self):
        for no in xrange(10000):
            print no
            self._q.put(no, block = False)
        return 

def main():
    total_cores = cpu_count()
    total_processes = total_cores * 2
    q = JoinableQueue()
    print("Gevent on top multiprocessing with 17 gevent coroutines\
          \n 10 producers gevent and 7 consumers gevent")
    producer_gevents = 10
    consumer_gevents = 7
    jobs = []
    start = datetime.datetime.now()
    for x in xrange(total_cores):
        if not x % 2 :
            p = Process(target = Producer, args=(q, producer_gevents,\
                                            "producer %d"%1, consumer_gevents))
            p.start()
            jobs.append(p)
        else:
            p = Process(target = Consumer, args=(q, consumer_gevents,\
                                                      "consumer %d"%x))
            p.start()
            jobs.append(p)

    for job in jobs:
        job.join()

    print("{0} process with {1} producer gevents and {2} consumer gevents took{3}\
           seconds to produce {4} numbers and consume".format(total_processes,\
           producer_gevents * total_cores, consumer_gevents * total_cores, \
           datetime.datetime.now() - start,producer_gevents*total_cores*10000))

if __name__ == '__main__':
    main()
