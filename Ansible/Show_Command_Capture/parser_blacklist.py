#!/usr/bin/env python

from __future__ import print_function
import re, os

ipv4_address= re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

with open('/tmp/a10_output.txt', 'r') as f:
    for line in f.readlines():
        line = eval(line.strip())
        for line in line["Result"].split("\n"):
            if re.search(ipv4_address, line): 
                result = (line.split())
                print("IP: {} State: {}".format(result[0], result[1]))

#os.remove('/tmp/a10_output.txt')


