#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    worker file which will run only one program at a time, I know you are
    crazy what me fork all programs, but it doesn't yield what we are testing
"""

import os
files_to_run = ['puremultiprocessing.py', 'sysinfo.py']
for filename in files_to_run:
    os.system("python %s"%filename)

