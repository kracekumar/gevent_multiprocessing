#! /usr/bin/env python
# -*- coding: utf-8 -*-

#This provides info about running machine

import platform
from multiprocessing import cpu_count
def print_info():
    print("=== Machine Details ===")
    print("Architecture: {0}".format(platform.architecture()))
    print("Dist: {0}".format(platform.dist()))
    print("Processor: {0}".format(platform.processor()))
    print("Total Cores: {0}".format(cpu_count()))

if __name__ == "__main__":
    print_info()
