Experiments with multiprocessing, gevent, greenlet, threads
---------
    This repo consist of code which explores various performance of using
    multiprocessing, gevent, greenlet, threads with requests. 

- Install all dependencies via `pip requirements.py` its upto you to create 
  virtualenv     

- Run `python multiprocessing_gevent.py` (Here `python` is your default 
  interpreter)

- Run `python onlygevents.py` 

Results
-------
 - Machine Details
    -   Architecture: ('64bit', 'ELF')
    -   Dist: ('debian', 'squeeze/sid', '')
    -   Total Cores: 4

All the tests are carried on Heroku free account.


__onlygevents.py

- 1 process with 40 producer gevents and 28 consumer gevents took 0:00:17.100989 
  seconds to produce 400000 numbers and consume

__multiprocessing_gevent.py
- 8 process with 40 producer gevents and 28 consumer gevents took0:00:13.906008 
  seconds to produce 400000 numbers and consume

How to test in heroku
---------------------
1. Follow all the steps for creating a python application
2. Push the code to heroku
3. Run `heroku run python`
4. `from multiprocessing_gevnet import main`
5. `main()`
6. Wait for the completion
7. `from onlygevents import main`
8. `main()`
9. Compare the results
10. You can also run these tests as worker and check the logs,

Observation
-----------
- With n cpus, n/2 producer processes and n/2 consumers, gevents completes tasks
  in less time(around 18% - 20%) when compared to multiprocessing processes.

- with n cpus, n producers processes, n consumers processes multiprocessing 
  processes outperforms.

To Do
----
- Increase gevents and processes and benchmark.
- Try same result for 100 to 1000s parallel download with requests and benchmark.
- How GNU/Linux allocates processes to cores
- Memory consumption 


Commands for monitoring process
-------------------------------
- `ps -AlFH | grep multi`
- `ps -AlFH | grep gevent`

