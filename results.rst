Results
-------
    - __LocalMachine__
        - Total Cores + 10 producer gevents + 7 consumer gevents => 
        multiprocessor_gevents.py: 

        - onlygevents
          -----------

        1 process with 20 producer gevents and 14 consumer gevents took 
        0:00:28.176459 seconds to produce 200000 numbers and consume

        4 process with 20 producer gevents and 14 consumer gevents took
        0:00:15.555849 seconds to produce 200000 numbers and consume

- 2 process with 17 gevent coroutines took 0:00:16.685383 seconds to produce 100000           numbers and consume them
    - __heroku __
        - 1 process with 17 gevent coroutines took 0:00:06.309244 seconds to produce 100000           numbers and consume them
        - 

Requests
--------

- asyncresults.py
    - Requests async took 0:00:02.354094 seconds for 40 urls
    - Requests async took 0:00:03.859900 seconds for 46 urls

- multiprocessingrequests
    - 8 processes on 4 core machine took 0:00:03.684710 time to download 46 urls
    - 8 processes on 4 core machine took 0:00:00.002761 time to read 0 urls 
      from queue

